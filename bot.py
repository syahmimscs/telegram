import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE,data=None):
    """
    If passed from the onboarding bot, can have a deep link like this:
    faq_bot_start_command = f'/start?data={user_identifier}'
    onboarding_bot.send_message(chat_id=user_id, text=faq_bot_start_command)
    Then handle the data below:
    """
    if data:
        # Process the data to identify the user from the onboarding bot
        return
    
    # Send a welcome message
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to the FAQ bot! How can I assist you?"
    )

    # Create the main menu
    main_menu_keyboard = [
        [InlineKeyboardButton("Topic 1", callback_data="topic1")],
        [InlineKeyboardButton("Topic 2", callback_data="topic2")],
        [InlineKeyboardButton("Topic 3", callback_data="topic3")],
        [InlineKeyboardButton("Back to Main Page", callback_data="back")]
    ]
    reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

    # Send the main menu to the user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Please select a topic:",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am a FAQ bot! Please type something so I can respond!")


# For now handle inputs/add-ons: AI implementation
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    query = update.callback_query
    data = query.data

    # Handle different button clicks based on the data received
    if data == "topic1":
        # Handle topic 1 button click
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You clicked on Topic 1. Here's the information for Topic 1."
        )
    elif data == "topic2":
        # Handle topic 2 button click
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You clicked on Topic 2. Here's the information for Topic 2."
        )
    elif data == "topic3":
        # Handle topic 3 button click
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You clicked on Topic 3. Here's the information for Topic 3."
        )
    elif data == "back":
        # Send the user back to the onboarding bot
        # Perform the necessary action to redirect the user
        return 


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Retrieve the user's message
    message = update.message.text

    # Process the message and provide a response
    # Add your AI implementation or processing logic here
    response = "This is a placeholder response. You can customize it based on your implementation."

    # Send the response to the user
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == "__main__":
    print('Starting bot...')
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    start_handler = CommandHandler("start", start_command)
    app.add_handler(start_handler)
    help_handler = CommandHandler("help", help_command)
    app.add_handler(help_handler)

    # Button Click
    button_click_handler = CallbackQueryHandler(button_click)
    app.add_handler(button_click_handler)

    # Messages
    message_handler = MessageHandler(filters.Text, handle_message)
    app.add_handler(message_handler)

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling()
