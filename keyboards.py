from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


upload_video_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Загрузить видео')]], resize_keyboard=True)


cancel_processing_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отменить процесс загрузки видео'),
     ],
], resize_keyboard=True)
