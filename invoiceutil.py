import os
import io
import json
import logging
from typing import Any, Dict, List
from http import HTTPStatus

import requests
import httpx
from openai import OpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


def _env(name: str, default: str | None = None, required: bool = False) -> str | None:
    value = os.getenv(name, default)
    if required and (value is None or str(value).strip() == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _get_bmw_settings() -> Dict[str, Any]:
    hostname = (_env("BMW_HOSTNAME", required=True) or "").strip()
    client_id = (_env("BMW_CLIENT_ID", required=True) or "").strip()
    client_secret = (_env("BMW_CLIENT_SECRET", required=True) or "").strip()
    api_key = (_env("BMW_API_KEY", required=True) or "").strip()
    ca_path = (_env("BMW_CA_PATH") or "").strip() or None
    llm_model = (_env("BMW_LLM_MODEL", "openai/gpt-4o") or "openai/gpt-4o").strip()

    # OpenAI-compatible base URL MUST end with /v1
    base_url = f"https://{hostname}/llmapi/v1"

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "api_key": api_key,
        "ca_path": ca_path,
        "llm_model": llm_model,
        "openai_base_url": base_url,
    }


def _resolve_ca_verify(ca_path: str | None) -> str | bool:
    if ca_path and os.path.exists(ca_path):
        return ca_path
    return True


def _get_webeam_access_token(requests_session: requests.Session, client_id: str, client_secret: str) -> str:
    auth_endpoint = (
        "https://auth-i.bmwgroup.net/auth/oauth2/realms/root/realms/machine2machine/access_token"
    )
    auth_response = requests_session.post(
        auth_endpoint,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "machine2machine",
        },
    )

    if auth_response.status_code != HTTPStatus.OK:
        raise RuntimeError(
            f"OAuth2 authentication failed. HTTP {auth_response.status_code}. Response: {auth_response.text}"
        )

    auth_data = auth_response.json()
    access_token = auth_data.get("access_token")
    if not access_token:
        raise RuntimeError(f"No access_token in response: {auth_data}")
    return access_token


def _create_httpx_client(api_key: str, ca_path: str | None) -> httpx.Client:
    verify = _resolve_ca_verify(ca_path)
    # trust_env=False prevents picking up corporate proxy env vars that can break DNS / routing.
    return httpx.Client(
        headers={"x-apikey": api_key},
        verify=verify,
        timeout=60.0,
        trust_env=False,
    )


def _create_bmw_openai_client(settings: Dict[str, Any], wen_access_token: str, http_client: httpx.Client) -> OpenAI:
    return OpenAI(
        base_url=settings["openai_base_url"],
        api_key=wen_access_token,
        http_client=http_client,
    )


def _extract_pdf_text(uploaded_file: Any) -> str:
    # Streamlit UploadedFile can only be read once; read bytes up-front.
    data = uploaded_file.read()
    reader = PdfReader(io.BytesIO(data))
    parts: list[str] = []
    for p in reader.pages:
        try:
            parts.append(p.extract_text() or "")
        except Exception:
            parts.append("")
    return "\n\n".join(parts).strip()


def _extract_json_from_text(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        snippet = text[start : end + 1]
        try:
            return json.loads(snippet)
        except Exception:
            pass

    return text.strip()


def _make_chunks(text: str, chunk_size: int = 1500, overlap: int = 150) -> List[str]:
    if not text:
        return []
    chunks: List[str] = []
    i = 0
    n = len(text)
    while i < n:
        j = min(i + chunk_size, n)
        chunks.append(text[i:j])
        if j >= n:
            break
        i = max(0, j - overlap)
    return chunks


def _validate_settings(settings: Dict[str, Any]) -> None:
    # Basic sanity checks to catch common DNS issues early.
    base_url: str = settings["openai_base_url"]
    if "//" not in base_url or "." not in base_url:
        raise RuntimeError(f"Invalid BMW openai_base_url computed: {base_url}")

    hostname = base_url.split("//", 1)[1].split("/", 1)[0]
    if " " in hostname or hostname == "":
        raise RuntimeError(f"Invalid hostname derived from BMW_HOSTNAME: {hostname!r}")

    # If someone accidentally put the full URL into BMW_HOSTNAME, we'll end up with https://https://...
    if hostname.startswith("http"):
        raise RuntimeError(
            "BMW_HOSTNAME should be a hostname only (e.g. api.int.gcp.cloud.bmw), not a URL. "
            f"Computed base_url={base_url}"
        )


def create_docs(user_pdf_list: List[Any]) -> List[Dict[str, Any]]:
    """Invoice extraction using LangChain retrieval (FAISS) + BMW GenAI gateway.

    Returns list of dicts per file:
      { filename, extracted, raw }

    Vector DB is always used.
    """

    if not user_pdf_list:
        return []

    settings = _get_bmw_settings()
    _validate_settings(settings)

    # Build a single httpx client shared by OpenAI SDK + LangChain wrappers
    shared_httpx = _create_httpx_client(settings["api_key"], settings.get("ca_path"))

    # Get WEN token once
    with requests.Session() as requests_session:
        requests_session.proxies = {"http": "", "https": ""}
        requests_session.verify = _resolve_ca_verify(settings.get("ca_path"))

        wen_token = _get_webeam_access_token(
            requests_session,
            client_id=settings["client_id"],
            client_secret=settings["client_secret"],
        )

    # OpenAI SDK client for BMW gateway (chat completions)
    bmw_openai_client = _create_bmw_openai_client(settings, wen_token, http_client=shared_httpx)

    # Embeddings through BMW gateway
    embeddings = OpenAIEmbeddings(
        model=_env("BMW_EMBEDDING_MODEL", "openai/text-embedding-3-small") or "openai/text-embedding-3-small",
        base_url=settings["openai_base_url"],
        api_key=wen_token,
        http_client=shared_httpx,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You extract structured invoice fields from provided context. "
                "Return ONLY valid JSON (no markdown, no extra text).",
            ),
            (
                "user",
                "Extract these fields: Invoice Number, Order Number, Invoice Date, Due Date, Total Due, From, To, "
                "Hrs/Qty, Service, Rate/Price, Adjust, Sub Total, Tax, Total.\n\n"
                "Context:\n{context}",
            ),
        ]
    )

    results: List[Dict[str, Any]] = []

    for uploaded in user_pdf_list:
        filename = getattr(uploaded, "name", "uploaded.pdf")
        try:
            text = _extract_pdf_text(uploaded)
            if not text:
                results.append({"filename": filename, "extracted": {"error": "Empty PDF text"}, "raw": ""})
                continue

            chunks = _make_chunks(text)
            docs = [Document(page_content=c, metadata={"source": filename}) for c in chunks]

            vector = FAISS.from_documents(docs, embeddings)
            retriever = vector.as_retriever(search_kwargs={"k": 6})

            query = "invoice header, invoice number, invoice date, due date, totals, line items"

            try:
                rel_docs = retriever.invoke(query)
            except AttributeError:
                rel_docs = retriever.get_relevant_documents(query)

            context = "\n\n".join(d.page_content for d in rel_docs)

            msg = prompt.format_messages(context=context)
            resp = bmw_openai_client.chat.completions.create(
                model=settings["llm_model"],
                temperature=0,
                max_completion_tokens=1200,
                messages=[{"role": _lc_role_to_openai(m.type), "content": m.content} for m in msg],
            )

            raw = resp.choices[0].message.content or ""
            extracted = _extract_json_from_text(raw)

            results.append({"filename": filename, "extracted": extracted, "raw": raw})
        except Exception as e:
            logger.exception("Invoice extraction failed for %s", filename)
            results.append(
                {
                    "filename": filename,
                    "extracted": {
                        "error": f"{type(e).__name__}: {e}",
                        "bmw_openai_base_url": settings.get("openai_base_url"),
                    },
                    "raw": "",
                }
            )

    return results


def _lc_role_to_openai(role: str) -> str:
    r = (role or "").lower()
    if r == "human":
        return "user"
    if r in {"ai", "assistant"}:
        return "assistant"
    if r in {"system", "user", "tool", "developer"}:
        return r
    # default fallback
    return "user"
