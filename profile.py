from dispatcher import *
from aiogram.dispatcher import FSMContext
from all_states import FSMProfile, FSMDistributor
from database import *
from text import *
from buttons import *
from privet_room import LS_TEXT


@dp.callback_query_handler(lambda call: True, state=FSMProfile.where)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == PROFILE_NAME.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(CR_CANSEL)
        await bot.edit_message_text(text_profile_name, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMProfile.change_name.set()
    elif call.data == PROFILE_COMMENT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(CR_CANSEL)
        await bot.edit_message_text(text_profile_comm, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMProfile.add_comments.set()
    elif call.data == PROFILE_SIGNAL1_INFO.callback_data:
        await call.answer(help_notification_sell, show_alert=True)
    elif call.data == PROFILE_SIGNAL2_INFO.callback_data:
        await call.answer(help_notification_buy, show_alert=True)
    elif call.data == PROFILE_SIGNAL_ON.callback_data or call.data == PROFILE_SIGNAL_OFF.callback_data or \
            call.data == PROFILE_SIGNAL_ON2.callback_data or call.data == PROFILE_SIGNAL_OFF2.callback_data:
        if call.data == PROFILE_SIGNAL_ON2.callback_data or call.data == PROFILE_SIGNAL_OFF2.callback_data:
            update_notification(call.from_user.id, "buy")
        else:
            update_notification(call.from_user.id,)
        info = get_custom_info(call.from_user.id)
        status = "Сповіщення увімкненно"
        check = "ON"
        if info:
            check = info[2]
        if check == "ON":
            status = "Сповіщення вимкненно"

        await bot.edit_message_text(text_profile(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=profile_buttons(call.from_user.id))
        await call.answer(status)
    elif call.data == CANSEL_LS.callback_data:
        await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()


@dp.message_handler(content_types=['text'], state=FSMProfile.change_name)
async def back(msg: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(CR_CANSEL)
    if get_custom_info(nick=msg.text):
        await msg.answer("такий нікнейм вже існує".upper(),
                         reply_markup=keyboard)
    else:
        if not msg.text.isdigit() and len(msg.text) <= 20 or msg.text == msg.from_user.id:
            user_custom_name(msg.from_user.id, msg.text)
            await msg.answer(f"нікнейм зміненно на: ".upper()+msg.text, reply_markup=keyboard)
        else:
            await msg.answer("нікнейм не може зкладатись тільки з цифр або мати довжину більше за 20 символів".upper(),
                             reply_markup=keyboard)


@dp.message_handler(content_types=['text'], state=FSMProfile.add_comments)
async def back(msg: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(CR_CANSEL)
    if len(msg.text) <= 90:
        user_custom_comments(msg.from_user.id, msg.text)
        await msg.answer(f"коментар зміненно на: ".upper() + msg.text, reply_markup=keyboard)
    else:
        await msg.answer("коментар не може мати довжину більше за 90 символів".upper(),
                         reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True, state=[FSMProfile.change_name, FSMProfile.add_comments])
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == CR_CANSEL.callback_data:
        await bot.edit_message_text(text_profile(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=profile_buttons(call.from_user.id))
        await FSMProfile.where.set()
