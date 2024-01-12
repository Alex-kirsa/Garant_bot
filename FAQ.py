from all_states import *
from aiogram.dispatcher import FSMContext
from dispatcher import *
from privet_room import *
from buttons import *
from text import *


@dp.callback_query_handler(lambda call: True, state=FSMFaq.step1)
async def back(call: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(ADD_BUT_CANSEL)
    if call.data == CHAT_BUT.callback_data:
        await bot.send_message(call.message.chat.id, CHAT_TEXT, reply_markup=keyboard)
    elif call.data == ADMIN_CHAT_BUT.callback_data:
        await bot.send_message(call.message.chat.id, ADMIN_TEXT, reply_markup=keyboard)
    elif call.data == CANSEL_LS.callback_data:
        await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()
