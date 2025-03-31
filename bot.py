# geniebot/bot.py
import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
import time
import uuid

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize Hugging Face model and tokenizer
def init_huggingface(model_name="facebook/blenderbot-400M-distill"):
    """Initializes the Hugging Face model and tokenizer."""
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = model.to(device)
        logger.info(f"Hugging Face model and tokenizer loaded: {model_name} on {device}")
        return model, tokenizer, device
    except Exception as e:
        logger.error(f"Failed to initialize Hugging Face model: {e}")
        raise

# Telegram message handling
async def handle_telegram_message(update: Update, context: ContextTypes.DEFAULT_TYPE, model, tokenizer, device):
    """Handles a single Telegram message."""
    user_message = update.message.text
    chat_id = update.effective_chat.id

    try:
        start_time = time.time()
        if 'conversation_id' not in context.chat_data:
            context.chat_data['conversation_id'] = str(uuid.uuid4())
            context.chat_data['conversation_history'] = []

        conversation_id = context.chat_data['conversation_id']
        conversation_history = context.chat_data['conversation_history']

        conversation_history.append(f"User: {user_message}")
        prompt = " ".join(conversation_history) + " Bot:"

        inputs = tokenizer([prompt], return_tensors="pt").to(device)
        outputs = model.generate(**inputs, max_length=200, num_return_sequences=1)
        bot_response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
        bot_response = bot_response.replace("Bot:", "").strip()
        conversation_history.append(f"Bot: {bot_response}")
        context.chat_data['conversation_history'] = conversation_history[-3:]

        end_time = time.time()
        response_time = end_time - start_time

        await context.bot.send_message(chat_id=chat_id, text=bot_response)
        logger.info(
            f"Sent Hugging Face response to chat {chat_id} in {response_time:.2f} seconds. Conversation ID: {conversation_id}"
        )

    except Exception as e:
        error_message = f"Sorry, I couldn't process your request. Error: {e} \n\n {traceback.format_exc()}"
        await context.bot.send_message(chat_id=chat_id, text=error_message)
        logger.error(f"Error processing user message: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a greeting message when the /start command is issued."""
    user = update.effective_user
    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Hello {user.first_name}! I'm GenieBot, your AI assistant.\n\n"
                 "**Disclaimer:** I am an AI and my responses are generated based on patterns in data. "
                 "I may not always be accurate, truthful, or appropriate.",
        )
    except Exception as e:
        logger.error(f"Error sending start message: {e}")
        await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Failed to send start message."
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and send a broadcast message to alert the developer."""
    logger.error(f"Update {update} caused error {context.error} \n\n {traceback.format_exc()}")
    print(f"Error: {context.error}")

def main():
    """Starts the bot."""
    bot_token = "YOUR_TELEGRAM_BOT_TOKEN"  # REPLACE WITH YOUR BOT TOKEN

    if not bot_token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set!")

    try:
        model_name = "facebook/blenderbot-400M-distill"
        model, tokenizer, device = init_huggingface(model_name)
    except Exception:
        logger.critical("Failed to initialize Hugging Face Transformers. Exiting.")
        return

    application = ApplicationBuilder().token(bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                          lambda update, context: handle_telegram_message(update, context, model, tokenizer, device)))  # Pass model and tokenizer
    application.add_error_handler(error_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
