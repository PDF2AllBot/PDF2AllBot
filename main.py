from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from PyPDF2 import PdfMerger
from docx import Document
from PIL import Image
import os

TOKEN = "8434985374:AAEZ-wNpKT2fxmvBxLEzRBBWsmJcsPcw7l8"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello! I'm your PDF Converter Bot.\n\n"
        "Send me images or PDF/Word/Excel files to convert.\n"
        "Available commands:\n"
        "/img2pdf - Convert images to PDF\n"
        "/pdf2img - Convert PDF pages to images\n"
        "/pdf2word - Convert PDF to Word\n"
        "/pdf2excel - Convert PDF to Excel\n"
        "/word2pdf - Convert Word to PDF\n"
        "/excel2pdf - Convert Excel to PDF\n"
        "/merge - Merge multiple PDFs\n"
        "/watermark - Add watermark to PDF"
    )

def img2pdf(update: Update, context: CallbackContext):
    photos = []
    for photo in update.message.photo:
        file = context.bot.getFile(photo.file_id)
        file.download('temp.jpg')
        photos.append(Image.open('temp.jpg').convert('RGB'))

    if photos:
        photos[0].save('output.pdf', save_all=True, append_images=photos[1:])
        update.message.reply_document(document=open('output.pdf', 'rb'))
        os.remove('output.pdf')
    for photo in photos:
        photo.close()
        if os.path.exists('temp.jpg'):
            os.remove('temp.jpg')

def merge_pdfs(update: Update, context: CallbackContext):
    update.message.reply_text("Merge feature coming soon!")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, img2pdf))
    dp.add_handler(CommandHandler("merge", merge_pdfs))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
