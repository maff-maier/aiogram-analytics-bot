from aiogram.fsm.state import StatesGroup, State


class UploadVideo(StatesGroup):
    video_name = State()
    video = State()
