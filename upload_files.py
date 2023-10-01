import os
import zipfile
from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import filters
import telegram
# Replace with your own API credentials
API_TOKEN = '5502855202:AAGW3MYUov5Gb2wWgpcaNTgxDjZ98IFh4P8'
API_ID = '6534707'
API_HASH = '4bcc61d959a9f403b2f20149cbbe627a'
OWNER_ID = '1430593323'

def start(update: Update, context):
 """Send a welcome message when the command /start is issued."""
 update.message.reply_text('Hi! Send me any file and I will zip it for you.')

def zip_file(update: Update, context):
 """Zip the file sent by the user and send it back."""
 # Check if a file was sent by the user
 if not update.message.document:
  update.message.reply_text('Please send a file.')
  return

 # Get the file details
 file_id = update.message.document.file_id
 file_name = update.message.document.file_name

 # Download the file to local storage
 file_path = context.bot.get_file(file_id).download()

 # Create a ZIP archive with or without password protection
 password_protected = False # Change to True if you want password protection
 zip_file_path = os.path.join(os.getcwd(), f'{file_name}.zip')
  
 with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zf:
  if password_protected:
   zf.setpassword(b'your_password') # Replace 'your_password' with your desired password
    
  zf.write(file_path, arcname=file_name)

 # Send the ZIP archive back to the user
 context.bot.send_document(chat_id=update.effective_chat.id,
        document=open(zip_file_path, 'rb'),
        filename=f'{file_name}.zip')

def main():
 """Start the bot."""
 updater = Updater(API_TOKEN)
  
 global dp
 dp = updater.dispatcher
  
 dp.add_handler(CommandHandler("start", start))
 dp.add_handler(MessageHandler(Filters.document, zip_file))
 # Only allow owner to use commands in groups (optional)
 dp.add_handler(CommandHandler("start", start, filters=Filters.chat(OWNER_ID)))
 dp.add_handler(MessageHandler(Filters.document & Filters.chat(OWNER_ID), zip_file))

updater.start_polling()
updater.idle()

if __name__ == '__main__':
 main()
