import pandas as pd
import random
import string
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Load existing data from the Excel sheet
try:
    df = pd.read_excel("referral_data.xlsx")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Username", "Points"])

# Function to generate a unique referral link
def generate_referral_link(username):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

# Function to track referrals and assign points
def track_referral(referrer, referee):
    if referrer in df["Username"].values:
        referrer_index = df.index[df["Username"] == referrer].tolist()[0]
        df.at[referrer_index, "Points"] += 1
    else:
        df = df.append({"Username": referrer, "Points": 1}, ignore_index=True)

# Start command handler
def start(update, context):
    update.message.reply_text("Welcome to Solanus affiliate! Enter your wallet address by command /setwallet <your wallet address>")

# Setwallet command handler
def set_wallet(update, context):
    wallet_address = context.args[0] if context.args else None
    if wallet_address:
        # Save wallet address to a sheet (for simplicity, let's just print here)
        update.message.reply_text(f"Wallet address set successfully: {wallet_address}")

        # Here, you can save the wallet address along with the user's Telegram username in your database or Excel sheet
        # For demonstration purposes, let's just print it
        print(f"User {update.effective_user.username} set wallet address: {wallet_address}")
    else:
        update.message.reply_text("Please provide a valid wallet address.")

# Referral command handler
def referral(update, context):
    # You can fetch the number of referrals for the user from your database or Excel sheet
    username = update.effective_user.username
    referrals = df[df["Username"] == username]["Points"].values[0] if username in df["Username"].values else 0
    update.message.reply_text(f"You have {referrals} referral(s).")

# Sample usage
def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("6404944134:AAE2C-O9zx_l8-C-UQVczXJODhUk_rVhbwc", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("setwallet", set_wallet))
    dp.add_handler(CommandHandler("referral", referral))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()

