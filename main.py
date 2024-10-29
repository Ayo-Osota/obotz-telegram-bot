import random
from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, Application

TOKEN: Final = '7913087098:AAENuyglFEY8yEuDwAC01ylX67hF2DPO28c'
BOT_USERNAME: Final = '@osotzBot'
WORDS: Final = ["python", "telegram",
                "developer", "bot", "hangman", "programming", "superteam", 'nigeria',
                'canada', 'saka', 'arsenal', 'ayomikun', 'trade', 'solana', 'information',
                'grateful', 'motunrayo', 'happy', 'football', 'music', 'love', 'blossom',
                'tired', 'give', 'employ', 'me', 'snow', 'wait', 'revv', 'uppercut', 'ace']
games = {}


def start_game(chat_id):
    word = random.choice(WORDS)
    games[chat_id] = {
        "word": word,
        "guessed": ["_" for _ in word],
        "attempts": 6,
        "used_letters": set()
    }


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! I am a Ayo\'s bot')


async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in games:
        await update.message.reply_text(
            "Please cancel ongoing game with /cancel first.")
        return
    await update.message.reply_text(f'Hello {update.message.chat.first_name} {update.message.chat.last_name}. EA Sports, it\'s in the game.')
    chat_id = update.message.chat_id
    start_game(chat_id)
    game_data = games[chat_id]
    await update.message.reply_text(
        f"Welcome to Hangman! You have {game_data['attempts']} attempts.\n"
        f"Word: {' '.join(game_data['guessed'])}\n"
        "Guess a letter by typing it."
    )


def handle_guess(guess: str, game_data) -> str:

    if len(guess) != 1 or not guess.isalpha():
        return "Please guess one letter at a time."

    if guess in game_data["used_letters"]:
        return f"You already guessed '{
            guess}'. Try another letter."

    game_data["used_letters"].add(guess)

    if guess in game_data["word"]:
        # Correct guess
        for i, letter in enumerate(game_data["word"]):
            if letter == guess:
                game_data["guessed"][i] = guess
        if "_" not in game_data["guessed"]:
            return f"Congratulations! You guessed the word: {
                ''.join(game_data['guessed'])}"

        else:
            return f"Correct! Word: {' '.join(game_data['guessed'])}"
    else:
        # Incorrect guess
        game_data["attempts"] -= 1
        if game_data["attempts"] <= 0:
            return f"Game over! The word was: {game_data['word']}"
        else:
            return f"Incorrect! You have {game_data['attempts']} attempts left.\n Word: {' '.join(game_data['guessed'])}"


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in games:
        games.pop(chat_id)
        await update.message.reply_text("Game canceled.")
    else:
        await update.message.reply_text("No game in progress to cancel.")


async def dance_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in games:
        await update.message.reply_text(
            "Please cancel ongoing game with /cancel first.")
        return
    await update.message.reply_text('You can bere mole, ko ma ra or you can upstanding ko ma jo.')


async def open_app_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in games:
        await update.message.reply_text("Please cancel the ongoing game with /cancel first.")
        return

    # Define the button that links to your mini app
    button = InlineKeyboardButton(
        "Open the App", url="https://t.me/osotzBot/shakitiBotBot")
    keyboard = InlineKeyboardMarkup([[button]])

    await update.message.reply_text(
        "Check out my awesome Telegram mini app!",
        reply_markup=keyboard
    )


async def play_melon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in games:
        await update.message.reply_text("Please cancel the ongoing game with /cancel first.")
        return

    # Define the button that links to your mini app
    button = InlineKeyboardButton(
        "Open the App", url="https://t.me/osotzBot/melon")
    keyboard = InlineKeyboardMarkup([[button]])

    await update.message.reply_text(
        "Check out my awesome Telegram mini game. Melon smasher!",
        reply_markup=keyboard
    )


def handle_response(text: str) -> str:

    processed: str = text.lower()

    if 'hello' in processed or 'hi' in processed:
        return 'Hello! How can I help you today?'

    if 'how are you' in processed or 'how\'s it going' in processed:
        return 'I\'m just a bot, but I\'m here to help you! How are you?'

    if 'who are you' in processed or 'what are you' in processed:
        return 'I\'m a friendly bot here to chat and play games with you!'

    if 'play' in processed or 'start game' in processed:
        return 'Let\'s start the game! Type /play to begin.'

    if 'help' in processed or 'what can you do' in processed:
        return 'I can play games with you, chat a bit, and assist you. Type /play to start a game or say hello!'

    if 'bye' in processed or 'goodbye' in processed:
        return 'Goodbye! Hope to see you again soon.'

    if 'joke' in processed or 'funny' in processed:
        return 'Why did the computer go to the doctor? It had a virus! 😄'

    if 'what\'s up' in processed or 'what are you doing' in processed:
        return 'Just here, ready to chat and play games! What’s up with you?'

    if 'favorite color' in processed:
        return 'I\'d say blue… like a nice, clear sky! What’s yours?'

    if 'tell me something' in processed:
        return 'Did you know that honey never spoils? Archaeologists have found pots of honey in ancient tombs that are over 3,000 years old!'

    return 'I don\'t understand that... \n You start a game with /play.'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in games:
        game_data = games[chat_id]
        guess = update.message.text.lower()
        game_result: str = handle_guess(guess, game_data)
        await update.message.reply_text(game_result)
        if 'congratulations' in game_result.lower() or 'game over' in game_result.lower():
            games.pop(chat_id)

    else:
        message_type: str = update.message.chat.type
        text: str = update.message.text

        print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

        if message_type == 'group':
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                response: str = handle_response(new_text)
            else:
                return
        else:
            response: str = handle_response(text)

        print('Bot:', response)
        await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused Error: {context.error}")


if __name__ == '__main__':
    print('starting bot')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('play', play_command))
    app.add_handler(CommandHandler('dance', dance_command))
    app.add_handler(CommandHandler('open_app', open_app_command))
    app.add_handler(CommandHandler('play_melon', play_melon_command))
    app.add_handler(CommandHandler('cancel', cancel_command))

    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    print('polling')
    app.run_polling(poll_interval=3)
