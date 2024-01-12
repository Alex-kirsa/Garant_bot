from dispatcher import *
from aiogram.dispatcher import FSMContext
from all_states import *
from database import *
from text import *
from buttons import *
from privet_room import *
from aiogram.utils.exceptions import BadRequest
from sheets_write import log_sheets, user_info_sheets
from config import id_group_log


@dp.callback_query_handler(lambda call: True, state=FSMBalance.step1)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == APPROVE_NO.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(CONVERT_BUT, CANSEL_LS)
        await bot.edit_message_text(referral_text(call.from_user.id), call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard, parse_mode="MARKDOWN")
        await FSMDistributor.where.set()
    elif call.data == APPROVE_YES.callback_data:
        user = call.from_user.id
        try:
            p_balance = float(get_partner_balance(user))
            update_balance(user, p_balance)
            upload_partner_balance(user, -p_balance)
            await bot.send_message(id_group_log, f"{call.from_user.id} КОНВЕРТУВАВ ПАРТНЕРСЬКИЙ БАЛАНС {p_balance} ГРН")
            await call.answer("Перевів кошти на основний баланс", show_alert=True)
            await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                        reply_markup=LS_BUTTONS(call.from_user.id))
            await FSMDistributor.where.set()
        except Exception as ex:
            print(ex)