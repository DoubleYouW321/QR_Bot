from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

import qrcode
import re
import os

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('QR-bot запущен, отправьте нам ссылку и я конвертирую её в QR-code')

@router.message()
async def create_qr(message: Message):
    link_to_convert = message.text

    def clean_filename(filename):
        cleaned = re.sub(r'^https?://', '', filename)
        cleaned = re.sub(r'[^\w\-_.]', '_', cleaned)
        cleaned = re.sub(r'_+', '_', cleaned)
        if len(cleaned) > 100:
            cleaned = cleaned[:100]
        return cleaned
    
    os.makedirs("images", exist_ok=True)
    filename = clean_filename(link_to_convert)
    filepath = f"images/{filename}.png"
      
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10, 
        border=4,
    )      
    qr.add_data(link_to_convert)
    qr.make(fit=True) 
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)
    try:
        photo = FSInputFile(filepath)
        await message.answer_photo(photo=photo, caption=f"QR-код для: {link_to_convert}")
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
    