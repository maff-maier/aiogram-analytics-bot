import time
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import UploadVideo
from keyboards import cancel_processing_kb, upload_video_kb

router = Router()
last_update_time = time.time()
media_group_id = -1

@router.message(F.text == 'Загрузить видео')
async def start_upload_cycle(message: Message, state: FSMContext):
    await state.set_state(UploadVideo.video_name)
    await message.answer('Введите название, под которым будет сохранено видео', reply_markup=cancel_processing_kb)


@router.message(UploadVideo.video_name, F.text == 'Отменить процесс загрузки видео')
async def cancel_uploading(message: Message, state: FSMContext):
    await message.answer('Загрузка видео отменена. Вы можете загрузить новое видео, кликнув на кнопку "Загрузить видео"',
                         reply_markup=upload_video_kb)

    await state.clear()


@router.message(UploadVideo.video, F.text == 'Отменить процесс загрузки видео')
async def cancel_uploading(message: Message, state: FSMContext):
    await message.answer('Загрузка видео отменена. Вы можете загрузить новое видео, кликнув на кнопку "Загрузить видео"',
                         reply_markup=upload_video_kb)

    await state.clear()


@router.message(UploadVideo.video_name, F.text)
async def set_video_name(message: Message, state: FSMContext):
    await state.update_data(video_name=message.text)
    await state.set_state(UploadVideo.video)
    await message.answer('Отправьте само видео', reply_markup=cancel_processing_kb)


@router.message(UploadVideo.video_name, ~F.text)
async def incorrect_video_name(message: Message, state: FSMContext):
    await message.answer('Недопустимый тип названия. Введине название, под которым будет сохранено видео.')


@router.message(UploadVideo.video)
async def upload_video(message: Message, state: FSMContext):
    doc = message.document
    video = message.video

    global media_group_id
    global last_update_time

    '''Тут тема в том, что сообщения трекаются не одновременно, а тогда, когда загрузились.
        То, что происходит ниже: смотрим на последний сохраненный айди карусели. Если он не равен текущему,
        то задаем его равным текущему. Обновляем время последнего обновления айди. Если равен, смотрим разность текущего тайма
        и времени последней обновы. Если меньше n(300 в текущем кейсе), то скипаем соо. Если норм, то обрабатываем. 
        Вроде как одинаковые карусели имеют разный айди. Но вообще это всё бордер кейс, потому что не подразумевается получение
        карусели. Если получаем, смотрим на первый айтем, остальное скип. Если одно сообщение, то всё нормально, работаем
        в штатном режиме'''
    if message.media_group_id != media_group_id:
        media_group_id = message.media_group_id
        last_update_time = time.time()
    else:
        if time.time() - last_update_time < 300:
            last_update_time = time.time()
            return
        else:
            last_update_time = time.time()


    if not video and not doc:
        return await message.answer('Отправьте видео (можно файлом)!')

    if doc:
        if doc.mime_type.startswith('video/'):
            data = await state.get_data()
            await state.clear()

            full_data = []
            [full_data.append(f"{key}: {value}")
             for key, value in data.items()]

            # ТУТ РАБОТА С ВИДЕО, НА СЕРВАК ОТПРАВИТЬ, НАПРИМЕР

            await message.answer('\n'.join(full_data), reply_markup=upload_video_kb)
        else:
            return await message.answer('Отправьте видео (можно файлом)!')
    else:
        if video.mime_type.startswith('video/'):
            data = await state.get_data()
            await state.clear()

            full_data = []
            [full_data.append(f"{key}: {value}")
             for key, value in data.items()]

            # ТУТ РАБОТА С ВИДЕО, НА СЕРВАК ОТПРАВИТЬ, НАПРИМЕР


            await message.answer('\n'.join(full_data), reply_markup=upload_video_kb)
        else:
            return await message.answer('Отправьте видео (можно файлом)!')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет. Чтобы загрузить видео, жми на кнопку!', reply_markup=upload_video_kb)
