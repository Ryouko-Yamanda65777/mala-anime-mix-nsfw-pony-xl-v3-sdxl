import logging
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from diffusers import StableDiffusionPipeline
import torch
from io import BytesIO

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Hugging Face model (ensure you have the correct access)
MODEL_ID = "John6666/mala-anime-mix-nsfw-pony-xl-v3-sdxl"
PIPELINE = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
PIPELINE.to("cuda")  # Use GPU if available

# Define /start command handler
async def start(update: Update, context):
    await update.message.reply_text("Hi! I'm a text-to-image bot. Send me a description and I'll generate an image.")

# Define text handler for image generation
async def generate_image(update: Update, context):
    user_input = update.message.text
    try:
        # Generate image from the user prompt
        image = PIPELINE(user_input).images[0]

        # Convert image to byte stream to send as a file
        bio = BytesIO()
        bio.name = 'image.png'
        image.save(bio, 'PNG')
        bio.seek(0)

        # Send image to the user
        await update.message.reply_photo(photo=InputFile(bio))
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        await update.message.reply_text("Sorry, something went wrong while generating the image.")

# Define the main function to start the bot
def main():
    token = "YOUR_TELEGRAM_BOT_API_TOKEN"  # Replace with your bot token

    # Create the application
    app = ApplicationBuilder().token(token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    # Start polling for updates
    app.run_polling()

if __name__ == "__main__":
    main()
