# ============================================================
# DIALOGPT CHATBOT IMPLEMENTATION
# ============================================================
# This script implements a simple command-line chatbot using 
# Microsoft’s DialoGPT-medium model. 
# It maintains conversational context for multi-turn dialogue.
# ============================================================

# ------------------------------
# 1. Import Required Libraries
# ------------------------------
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# ------------------------------
# 2. Load Pre-trained Model and Tokenizer
# ------------------------------
# We use the 'microsoft/DialoGPT-medium' checkpoint for a medium-sized conversational model.
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Ensure we have a pad token to build attention masks reliably.
# DialoGPT often uses eos as pad; that's OK as long as we pass attention_mask explicitly.
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Put model in eval mode (no training)
model.eval()

# ------------------------------
# 3. Initialize Chat History
# ------------------------------
# 'chat_history_ids' will store the concatenated conversation context.
# Initially, it is set to None (no conversation yet).
chat_history_ids = None

# ------------------------------
# 4. Start Conversation Loop
# ------------------------------
# Use 'exit' or 'quit' to end the chat.
for step in range(50):
    # ---- Step 1: Get user input ----
    user_input = input("You: ").strip()
    if user_input.lower() in {"exit", "quit"}:
        print("Bot: Bye!")
        break

    # ---- Step 2: Encode user input ----
    # The EOS (End Of Sentence) token marks the end of the input for the model.
    new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # ---- Step 3: Append to chat history ----
    bot_input_ids = (
        torch.cat([chat_history_ids, new_input_ids], dim=-1)
        if chat_history_ids is not None
        else new_input_ids
    )

    # Build attention mask explicitly to avoid the warning and ensure correct behavior
    attention_mask = (bot_input_ids != tokenizer.pad_token_id).long()

    # ---- Step 4: Generate model response ----
    # Sampling helps avoid repetitive responses.
    with torch.no_grad():
        chat_history_ids = model.generate(
            bot_input_ids,
            attention_mask=attention_mask,
            max_new_tokens=80,
            do_sample=True,
            top_p=0.9,
            temperature=0.8,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    # ---- Step 5: Decode the model’s response ----
    response = tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1]:][0],
        skip_special_tokens=True,
    ).strip()

    # Fallback if the model returns empty
    if not response:
        response = "Could you rephrase that?"

    # ---- Step 6: Print bot response ----
    print(f"Bot: {response}")

# ============================================================
# END OF SCRIPT
# ============================================================
