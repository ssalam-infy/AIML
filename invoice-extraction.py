# This RAG Application takes in an Invoice PDF, loads the data into a Vector Database,
# Send the Invoice information as context to the OpenAI GPT LLM and
# comes back with extracted Details

import streamlit as st
from dotenv import load_dotenv
import invoiceutil as iu

def main():
    load_dotenv()

    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Invoice Extraction Bot")
    st.subheader("Extract invoice data")

    st.caption("Run this app with: streamlit run invoice-extraction.py")

    pdf = st.file_uploader(
        "Upload invoices (PDF)",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if st.button("Extract Data"):
        if not pdf:
            st.warning("Please upload at least one PDF.")
            return

        with st.spinner("Extracting..."):
            results = iu.create_docs(pdf)

        st.success("Done")

        for i, item in enumerate(results or [], start=1):
            filename = item.get("filename") or f"invoice_{i}.pdf"
            with st.expander(f"Result: {filename}", expanded=True):
                st.write("Extracted")
                st.json(item.get("extracted"))

                raw = item.get("raw")
                if raw:
                    st.divider()
                    st.write("Raw model output")
                    st.code(raw)

# Invoke the main function
if __name__ == "__main__":
    main()