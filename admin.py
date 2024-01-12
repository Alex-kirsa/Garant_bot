from dispatcher import *
from aiogram.dispatcher import FSMContext
from all_states import FSMAdmin, FSMDistributor
from database import *
from text import *
from buttons import *
from privet_room import *
from aiogram.utils.exceptions import BadRequest
from sheets_write import log_sheets, user_info_sheets, promo_info_sheets
from promo.promoCodes import generate_promo_code
from config import id_group_log


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.where)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == "ADMIN_BUT_ALL_ADD":
        all_adds = [text_process_admin_add(x) for x in get_all_balance_add()]
        if len(all_adds) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_adds[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
            await bot.edit_message_text(all_adds[0], call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.add_summ.set()
        else:
            await call.answer(no_orders)
    elif call.data == "ADMIN_BUT_ALL_DOWN":
        all_downs = [text_process_admin_down(x) for x in get_all_balance_down()]
        if len(all_downs) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_downs[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
            await bot.edit_message_text(all_downs[0], call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.down_summ.set()
        else:
            await call.answer(no_orders)
    elif call.data == "ADM_CHANGE_BALANCE":
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text("введіть ід юзера".upper(), call.message.chat.id, call.message.message_id, )
        await bot.send_message(call.message.chat.id, get_all_user_balance(), reply_markup=keyboard)
        await FSMAdmin.change_balance.set()
    elif call.data == "ADMIN_BUT_MEMBERS":
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        text = "ВВЕДІТЬ ID КЛІЄНТА"
        # for x in get_all_user2():
        #     text += f"{x[1]} ----> `{x[0]}`\n"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard, parse_mode="MARKDOWN")
        await FSMAdmin.all_users.set()
    elif call.data == "VALID_ADMIN":
        all_valid = [show_market_text_admin(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in valid_order()]
        if len(all_valid) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_valid[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                if len(all_valid) > 1:
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT)
                keyboard.add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_valid[0], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            async with state.proxy() as data:
                data["valid_step"] = 0
                print(69)
            await FSMAdmin.valid.set()
        else:
            await call.answer("Заявок не має", show_alert=True)
    elif call.data == "ADD_BUT_CANSEL":
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
    elif call.data == "ADMIN_BUT_SEND":
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        text = "введіть текст розсилки".upper()
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdmin.send.set()
    elif call.data == "ADMIN_BUT_DOWNLOAD":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(ORDER_INFO, USER_INFO, ADD_BUT_CANSEL)
        log, orders, user = get_admin_info()
        await bot.edit_message_text(f"ЗАЯВКИ: {orders}\nКОРИСТУВАЧІ: {user}", call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=keyboard)
        # if write_sheets(stat()):
        #     await call.answer("успішно вигрузив інфо".upper(), show_alert=True)
        # else:
        #     await call.answer("щось пішло не так", show_alert=True)
    elif call.data == ORDER_INFO.callback_data:
        if status_info_sheets(status_info()):
            await call.answer("успішно вигрузив інфо по заявкам", show_alert=True)
    elif call.data == USER_INFO.callback_data:
        if user_info_sheets(user_info()):
            await call.answer("успішно вигрузив інфо по користувачам", show_alert=True)
        else:
            await call.answer("щось пішло не так", show_alert=True)
    elif call.data == LOG_INFO.callback_data:
        if log_sheets(log_info()):
            await call.answer("успішно вигрузив логи", show_alert=True)
        else:
            await call.answer("щось пішло не так", show_alert=True)

        # keyboard = InlineKeyboardMarkup(row_width=3)
        # keyboard.add(ADD_BUT_CANSEL)
        # await bot.edit_message_text("ID КОРИСТУВАЧА", call.message.chat.id, call.message.message_id,
        #                             reply_markup=keyboard)
        # await FSMAdmin.user_info.set()
    elif call.data == "ON" or call.data == "OFF":
        switch()
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
    elif call.data == "DISPUTE_ADMIN":
        async with state.proxy() as data:
            data["dispute"] = 0
        if dispute_orders():
            x = dispute_orders()[0]
            text = show_all_dispute_text(x)
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(close_dispute).add(ARROW_LEFT, ARROW_RIGHT, ADD_BUT_CANSEL)
            count = f"\nПОКАЗАНА {data['dispute'] + 1} З {len(dispute_orders())}"
            await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
            await FSMAdmin.dispute.set()
        else:
            await call.answer(no_orders, show_alert=True)
    elif call.data == "PROMO_ADMIN":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(CREATE_PROMO, PROMO_INFO, PROMO_CANSEL)
        await bot.edit_message_text(promo_text(), call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
    elif call.data == CREATE_PROMO.callback_data:
        async with state.proxy() as data:
            data["kind"] = "add"
            data["amount"] = 1
            data["term"] = 10
            data["discount"] = 10
        await bot.edit_message_text("Вкажіть дані для промокоду".upper(), call.message.chat.id, call.message.message_id,
                                    reply_markup=promo_buttons(data["kind"], data["amount"], data["term"], data["discount"]))
        await FSMAdmin.promo.set()
    elif call.data == PROMO_INFO.callback_data:
        try:
            codes = [["ПРОМОКОД", "СТАТУС", "ДІЄ ДО:", "ТИП", "ЗНИЖКА/БОНУС"]]
            for code in get_all_promoCodes():
                status = ""
                if code[1] == "used":
                    status = "Використаний"
                elif code[1] == "active":
                    status = "Активний"
                elif code[1] == "close":
                    status = "Просрочений"
                kind = ""
                if code[3] == "add":
                    kind = "Поповнення"
                elif code[3] == "down":
                    kind = "Виведення"
                codes.append([code[0], status, code[2], kind, f"{code[4]}%"])
            if promo_info_sheets(codes):
                await call.answer("Успішно вигрузив інфо")
            else:
                await call.answer("Щось пішло не так")
        except Exception:
           await call.answer("Щось пішло не так")
    elif call.data == CR_CANSEL.callback_data:
        await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()
    elif call.data == PROMO_CANSEL.callback_data:
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
        await FSMAdmin.where.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.promo)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == CR_CANSEL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(CREATE_PROMO, PROMO_INFO, PROMO_CANSEL)
        await bot.edit_message_text(promo_text(), call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdmin.where.set()
    elif call.data == "TYPE_INFO":
        await call.answer("oберіть до яких заявок цей код", show_alert=True)
    elif call.data == "AMOUNT_INFO":
        await call.answer("введіть кількість промокодів", show_alert=True)
    elif call.data == "TERM_INFO":
        await call.answer("термін дії у днях", show_alert=True)
    elif call.data == "DISCOUNT_INFO":
        await call.answer("введіть % бонусу", show_alert=True)
    elif call.data == "DISCOUNT_INFO_DOWN":
        await call.answer("введіть % знижки", show_alert=True)
    elif call.data == "PROMO_ADD":
        async with state.proxy() as data:
            data["kind"] = "down"
            data["discount"] = 100
        await bot.edit_message_text("Вкажіть дані для промокоду".upper(), call.message.chat.id, call.message.message_id,
                                    reply_markup=promo_buttons(data["kind"], data["amount"], data["term"], data["discount"]))
    elif call.data == "PROMO_DOWN":
        async with state.proxy() as data:
            data["kind"] = "add"
        await bot.edit_message_text("Вкажіть дані для промокоду".upper(), call.message.chat.id, call.message.message_id,
                                    reply_markup=promo_buttons(data["kind"], data["amount"], data["term"], data["discount"]))
    elif call.data == "PROMO_DISCOUNT":
        async with state.proxy() as data:
            if data["kind"] == "add":
                text = "введіть скільки % бонусу буде нараховано".upper()
            elif data["kind"] == "down":
                text = "введіть  % знижки на комісію виведення".upper()
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
        await FSMAdmin.promo_disc.set()
    elif call.data == "PROMO_AMOUNT":
        await bot.edit_message_text("введіть скільки потрібно промокодів".upper(), call.message.chat.id,
                                    call.message.message_id)
    elif call.data == "PROMO_TERM":
        await bot.edit_message_text("введіть скільки днів буде дійсний промокод".upper(), call.message.chat.id,
                                    call.message.message_id)
        await FSMAdmin.promo_term.set()
    elif call.data == "ADD_BUT_APPROVE":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(APPROVE_NO, APPROVE_YES)
        async with state.proxy() as data:
            if data["kind"] == "add":
                kind = "ПОПОВНЕННЯ"
            elif data["kind"] == "down":
                kind = "ВИВЕДЕННЯ"
            amount = data["amount"]
        await bot.edit_message_text(f"підтверджуєте створення {amount} промокодів для заявок {kind}".upper(),
                                    call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == APPROVE_NO.callback_data:
        async with state.proxy() as data:
            data["kind"] = "add"
            data["amount"] = 1
            data["term"] = 10
        await bot.edit_message_text("Вкажіть дані для промокоду".upper(), call.message.chat.id, call.message.message_id,
                                    reply_markup=promo_buttons(data["kind"], data["amount"], data["term"], data["discount"]))
    elif call.data == APPROVE_YES.callback_data:
        async with state.proxy() as data:
            amount = data["amount"]
            kind = data["kind"]
            term = data["term"]
            disc = data["discount"]

        codes = generate_promo_code(amount=int(amount))
        codes_for_data = []
        data = datetime.now().date() + timedelta(days=int(term))
        codes_for_admin = f"промокоди дійсні до {data}\n".upper()
        for num, code in enumerate(codes):
            codes_for_data.append([code, "active", data, kind, disc])
            codes_for_admin += f"{num+1}. {code}\n"
        add_promoCodes(codes_for_data)
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(CR_CANSEL)
        text = codes_for_admin
        if len(codes_for_data) > 10:
            text = "Bідправляю файл з промокодами"
            create_doc(codes_for_admin)
            await bot.edit_message_text(text,
                                        call.message.chat.id, call.message.message_id, reply_markup=keyboard)
            with open('Codes.txt', 'rb', ) as file:
                document = types.InputFile(file)
                await bot.send_document(call.from_user.id, document)

        else:
            await bot.edit_message_text(text,
                                        call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        if kind == "add":
            await bot.send_message(id_group_log, f"{call.from_user.id} АДМІН СГЕНЕРУВАВ ({len(codes_for_data)})"
                                                 f"ПРОМОКОД(ІВ) НА ПОПОВНЕННЯ")
        elif kind == "down":
            await bot.send_message(id_group_log, f"{call.from_user.id} АДМІН СГЕНЕРУВАВ ({len(codes_for_data)})"
                                                 f"ПРОМОКОД(ІВ) НА ВИВЕДЕННЯ")


@dp.message_handler(content_types=['text'], state=FSMAdmin.promo_disc)
async def back(msg: types.Message, state: FSMContext):
    try:
        if msg.text.isdigit() and 100 >= int(msg.text) > 0:
            async with state.proxy() as data:
                data["discount"] = int(msg.text)

            await bot.send_message(msg.from_user.id, "Вкажіть дані для промокоду".upper(), reply_markup=promo_buttons(data["kind"],
                                                                                            data["amount"],
                                                                                            data["term"],
                                                                                            data["discount"]))
            await FSMAdmin.promo.set()
        else:
            await bot.send_message(msg.from_user.id, "тільки цілі числа від 1".upper())
    except TypeError:
        await bot.send_message(msg.from_user.id, "тільки цілі числа від 1".upper())


@dp.message_handler(content_types=['text'], state=FSMAdmin.promo_term)
async def back(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            data["kind"] = "add"
            data["term"] = msg.text

        await bot.send_message(msg.from_user.id, "Вкажіть дані для промокоду".upper(), reply_markup=promo_buttons(data["kind"],
                                                                                        data["amount"],
                                                                                        data["term"],
                                                                                        data["discount"]))
        await FSMAdmin.promo.set()
    else:
        await bot.send_message(msg.from_user.id, "тільки цілі числа від 1".upper())


@dp.message_handler(content_types=['text'], state=FSMAdmin.promo)
async def back(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            data["amount"] = msg.text
        await bot.send_message(msg.from_user.id, "Вкажіть дані для промокоду".upper(), reply_markup=promo_buttons(data["kind"],
                                                                                        data["amount"],
                                                                                        data["term"],
                                                                                        data["discount"]))
    else:
        await bot.send_message(msg.from_user.id, "тільки цілі числа від 1".upper())


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.all_users)
async def back(call: types.CallbackQuery, state: FSMContext):

    if call.data == "ADD_BUT_CANSEL":
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
        await FSMAdmin.where.set()
    elif call.data == CR_CANSEL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        text = "ВВЕДІТЬ ID КЛІЄНТА"
        # for x in get_all_user2():
        #     text += f"{x[1]} ----> `{x[0]}`\n"
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard, parse_mode="MARKDOWN")

    elif call.data == CHANGE_BALANCE.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        try:
            async with state.proxy() as data:
                id_user = int(data["user"])
                text = f"поточний баланс: {get_balance_by_id(id_user)} грн\n\n" \
                       f"введіть сумму на яку змінити баланс".upper()
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
                await FSMAdmin.change_balance2.set()
        except Exception:
            pass
    elif call.data == SEND_MSG.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text("введіть текст повідомлення".upper(), call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdmin.send_msg_user.set()
    elif call.data == BAN.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(APPROVE_NO, APPROVE_YES)
        async with state.proxy() as data:
            id_user = int(data["user"])
        await bot.edit_message_text(f"Ви підтверджуєте бан користувача {id_user}\n", call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard)
        await FSMAdmin.ban_user.set()
    elif call.data == UNBAN.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(APPROVE_NO, APPROVE_YES)
        async with state.proxy() as data:
            id_user = int(data["user"])
        await bot.edit_message_text(f"Ви підтверджуєте розбан користувача {id_user}\n", call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard)
        await FSMAdmin.ban_user.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.ban_user)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == APPROVE_NO.callback_data or call.data == ADD_BUT_CANSEL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SEND_MSG, CHANGE_BALANCE, BAN)
        keyboard.add(CR_CANSEL)
        async with state.proxy() as data:
            await bot.send_message(call.from_user.id,
                                   MEMBERS(data["user"]),reply_markup=keyboard)
        await FSMAdmin.all_users.set()
    elif call.data == APPROVE_YES.callback_data:
        async with state.proxy() as data:
            id_user = int(data["user"])
        if check_ban(id_user):
            if unban_user(id_user):
                await bot.send_message(id_group_log, f"{call.from_user.id} АДМІН РОЗБАНИВ КОРИТСУВАЧА {id_user}")
                await call.answer(f"Користувач {id_user} більше не в бані", show_alert=True)
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ADD_BUT_CANSEL)
                text = "ВВЕДІТЬ ID КЛІЄНТА"
                # for x in get_all_user2():
                #     text += f"{x[1]} ----> `{x[0]}`\n"
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard, parse_mode="MARKDOWN")
                await FSMAdmin.all_users.set()
            else:
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ADD_BUT_CANSEL)
                await bot.edit_message_text("Щось пішло не так", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard,)
        else:
            if ban_user(id_user):
                await bot.send_message(id_group_log, f"{call.from_user.id} АДМІН ЗАБАНИВ КОРИТСУВАЧА {id_user}")
                await call.answer(f"користувач {id_user} в бані", show_alert=True)
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ADD_BUT_CANSEL)
                text = "ВВЕДІТЬ ID КЛІЄНТА"
                # for x in get_all_user2():
                #     text += f"{x[1]} ----> `{x[0]}`\n"
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard, parse_mode="MARKDOWN")
                await FSMAdmin.all_users.set()
            else:
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ADD_BUT_CANSEL)
                await bot.edit_message_text("Щось пішло не так", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard,)


@dp.message_handler(content_types=['text'], state=FSMAdmin.send_msg_user)
async def back(msg: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(APPROVE_NO, APPROVE_YES)
    async with state.proxy() as data:
        id_user = int(data["user"])
        data["send_text"] = msg.text
    await msg.answer(f"Ви підтверджуєте відправку повідомлення юзеру {id_user}\n"
                     f"з текстом: {msg.text}", reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.send_msg_user)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data or call.data == APPROVE_NO.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SEND_MSG, CHANGE_BALANCE, BAN)
        keyboard.add(CR_CANSEL)
        async with state.proxy() as data:
            await bot.send_message(call.from_user.id,
                                   LS_TEXT(data["user"]).replace("ОСОБИСТИЙ КАБІНЕТ", "").replace("МІЙ", ""),
                                   reply_markup=keyboard)
        await FSMAdmin.all_users.set()
    elif call.data == APPROVE_YES.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SEND_MSG, CHANGE_BALANCE, BAN)
        keyboard.add(CR_CANSEL)
        async with state.proxy() as data:
            await bot.send_message(data["user"], data["send_text"])
            await call.answer("Повідомлення відправлено", show_alert=True)
            await bot.edit_message_text(LS_TEXT(data["user"]).replace("ОСОБИСТИЙ КАБІНЕТ", "").replace("МІЙ", ""),
                                        call.from_user.id, call.message.message_id, reply_markup=keyboard)
        await FSMAdmin.all_users.set()


@dp.message_handler(content_types=['text'], state=FSMAdmin.all_users)
async def back(msg: types.Message, state: FSMContext):
    try:
        user_id = msg.text
        user = get_custom_info(nick=user_id)
        if user:
            user_id = user[0]
        keyboard = InlineKeyboardMarkup(row_width=2)
        if check_ban(user_id):
            keyboard.add(SEND_MSG, CHANGE_BALANCE, UNBAN)
        else:
            keyboard.add(SEND_MSG, CHANGE_BALANCE, BAN)
        keyboard.add(CR_CANSEL)
        await msg.answer(MEMBERS(user_id), reply_markup=keyboard)
        async with state.proxy() as data:
            data["user"] = user_id
    except Exception:
        print(Exception)
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(CR_CANSEL)
        await msg.answer("НЕ знайшов користувача в базі".upper(), reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.valid)
async def back(call: types.CallbackQuery, state: FSMContext):
    print(277)
    if call.data == "ADD_BUT_CANSEL":
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
        await FSMAdmin.where.set()
    elif call.data == ARROW_LEFT.callback_data:
        async with state.proxy() as data:
            step = data["valid_step"]
            step -= 1
            if step < 0:
                await call.answer("Hайперша заявка")
            else:
                all_valid = [show_market_text_admin(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                             valid_order()]
                if len(all_valid) > 0:
                    data["valid_step"] = step
                    data["order"] = all_valid[step]
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    if len(all_valid) > 1:
                        keyboard.add(ARROW_LEFT, ARROW_RIGHT)
                    keyboard.add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                    await bot.edit_message_text(all_valid[step], call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                else:
                    await call.answer("Заявок не має", show_alert=True)
                    await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                                reply_markup=admin_but())
    elif call.data == ARROW_RIGHT.callback_data:
        async with state.proxy() as data:
            step = data["valid_step"]
            step += 1
            all_valid = [show_market_text_admin(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                         valid_order()]

            if len(all_valid) > 0:
                if len(all_valid) == 1:
                    await call.answer("Єдина заявка")
                elif step > len(all_valid) - 1:
                    step = 0
                    data["valid_step"] = 0
                    await call.answer("Перша заявка")
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    if len(all_valid) > 1:
                        keyboard.add(ARROW_LEFT, ARROW_RIGHT)
                    keyboard.add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                    await bot.edit_message_text(all_valid[step], call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                else:
                    data["valid_step"] = step
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    if len(all_valid) > 1:
                        keyboard.add(ARROW_LEFT, ARROW_RIGHT)
                    keyboard.add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                    await bot.edit_message_text(all_valid[step], call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
            else:
                await call.answer("Заявок не має", show_alert=True)
                await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                            reply_markup=admin_but())

    elif call.data == ADMIN_BUT_APPROVE.callback_data:
        async with state.proxy() as data:
            step = data["valid_step"]
            order = valid_order()[step]
        await bot.edit_message_text(f"ВИ ПІДТВЕРДЖУЄТЕ розміщення заявки №{order[0]} на вітрині?".upper(),
                                    call.message.chat.id, call.message.message_id,
                                    reply_markup=InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES))
    elif call.data == APPROVE_YES.callback_data:
        async with state.proxy() as data:
            step = data["valid_step"]
            order = valid_order()[step]
            update_status_process(order[0])
            update_valid(order[6], order[1], order[9])
            for x in get_all_user2():
                try:
                    info = get_custom_info(x[0])
                    if info:
                        if info[2] == "ON":
                            text = "НА ВІТРИНІ З'ЯВИЛАСЯ НОВА ЗАЯВКА\n\n" \
                                   "ПРОДАМ\n" \
                                   f"ПРОДАВЕЦЬ: {order[6]}\n" \
                                   f"ПОКЕР-РУМ: {order[1]}\n" \
                                   f"СУМА: {order[2]} {order[10]}\n" \
                                   f"КУРС: {order[3]} ГРН\n"
                            await bot.send_message(x[0], text)
                    else:
                        text = "НА ВІТРИНІ З'ЯВИЛАСЯ НОВА ЗАЯВКА\n\n" \
                               "ПРОДАМ\n" \
                               f"ПРОДАВЕЦЬ: {order[6]}\n" \
                               f"ПОКЕР-РУМ: {order[1]}\n" \
                               f"СУМА: {order[2]} {order[10]}\n" \
                               f"КУРС: {order[3]} ГРН\n"
                        await bot.send_message(x[0], text)
                except Exception:
                    pass
            await bot.edit_message_text(f"заявка №{order[0]} розміщенна на вітрині".upper(),
                                        call.message.chat.id, call.message.message_id,
                                        reply_markup=InlineKeyboardMarkup(row_width=2).add(CR_CANSEL))
            try:
                await bot.send_message(order[6], f"ВАША ЗАЯВКА №{order[0]} РОЗМІЩЕНА НА ВІТРИНІ")
            except Exception:
                pass
    elif call.data == ADMIN_BUT_CANSEL.callback_data:
        await bot.edit_message_text(f"вкажіть причину скасування заявки".upper(),
                                    call.message.chat.id, call.message.message_id,
                                    reply_markup=InlineKeyboardMarkup(row_width=2).add(ADD_BUT_CANSEL))
        await FSMAdmin.valid_approve_desc.set()
    elif call.data == CR_CANSEL.callback_data or call.data == APPROVE_NO.callback_data:
        all_valid = [show_market_text_admin(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                     valid_order()]
        if len(all_valid) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_valid[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                if len(all_valid) > 1:
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT)
                keyboard.add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_valid[0], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            async with state.proxy() as data:
                data["valid_step"] = 0
            await FSMAdmin.valid.set()
        else:
            await call.answer("Заявок не має", show_alert=True)
            await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                        reply_markup=admin_but())
            await FSMAdmin.where.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.valid_approve_desc)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data or call.data == APPROVE_NO.callback_data:
        all_valid = [show_market_text_admin(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                     valid_order()]
        if len(all_valid) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_valid[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                if len(all_valid) > 1:
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT)
                keyboard.add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_valid[0], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            async with state.proxy() as data:
                data["valid_step"] = 0
            await FSMAdmin.valid.set()
        else:
            await call.answer("Заявок не має", show_alert=True)
            await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                        reply_markup=admin_but())
            await FSMAdmin.where.set()
    elif call.data == APPROVE_YES.callback_data:
        async with state.proxy() as data:
            step = data["valid_step"]
            order = valid_order()[step]
            reason = data["describe_order_cansel"]
        update_order_status(order[0], "cansel", "orders")
        await bot.send_message(order[6], f"Розміщення Заявки №{order[0]} на вітрині було скасавоно адміністратором.\n"
                                         f"причина: ".upper()+reason)
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(f"заявка №{order[0]} була скасована".upper(),
                                    call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)


@dp.message_handler(content_types=['text'], state=FSMAdmin.valid_approve_desc)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["describe_order_cansel"] = msg.text
    keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
    await bot.send_message(msg.from_user.id, APPROVE_ORDER_CANSEL, reply_markup=keyboard)


@dp.message_handler(content_types=['text'], state=FSMAdmin.user_info)
async def back(msg: types.Message, state: FSMContext):
    if check_register(msg.text):
        print(12313)
    else:
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        await msg.answer("Hе знайшов такого користувача".upper(), reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.user_info)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(USER_INFO, ADD_BUT_CANSEL)
        await bot.edit_message_text("ВИГРУЗИТИ ІНФО", call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdmin.where.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.approve_action)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == APPROVE_YES.callback_data:
        all_adds = [text_process_admin_add(x) for x in get_all_balance_add()]
        async with state.proxy() as data:
            step = data["step"]
            order = get_all_balance_add()[step]
        before = get_balance_by_id(order[4])
        promo = 0
        if get_promoCode(order[8]):
            promo = get_promoCode(order[8])[4]
        summ_add = float(order[1]) + ((float(order[1]) / 100) * float(promo))
        update_balance(order[4], summ_add, order[6])
        now = get_balance_by_id(order[4])
        update_balance_status(order[0], "approve", True)
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        await bot.send_message(id_group_log, f"{call.from_user.id} АДМІН ПІДТВЕРДИВ ЗАЯВКУ №{order[0]}"
                                             f"НА ПОПОВНЕННЯ {order[1]} ГРН")
        await bot.send_message(order[4], "заявку на поповнення балансу підтвердили, "
                                         "перевірте свій баланс!".upper())
        await bot.send_message(call.message.chat.id, f"ПІДТВЕРДЖЕНО ПОПОВНЕННЯ БАЛАНСУ\n\n{all_adds[step]}" +
                                                     f"попередний баланс: {before} ГРН\n"
                                                     f"поточний баланс: {now} ГРН".upper(), reply_markup=keyboard)

    elif call.data == APPROVE_NO.callback_data or call.data == ADD_BUT_CANSEL.callback_data:
        all_adds = [text_process_admin_add(x) for x in get_all_balance_add()]
        if len(all_adds) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_adds[0]
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
            await bot.edit_message_text(all_adds[0], call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.add_summ.set()
        else:
            await call.answer("Заявок не має")
            await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                        reply_markup=admin_but())
            await FSMAdmin.where.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.dispute)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == "ADD_BUT_CANSEL":
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
        await FSMAdmin.where.set()
    elif call.data == ARROW_LEFT.callback_data:
        async with state.proxy() as data:
            step = data["dispute"]
            step -= 1
            if step < 0:
                data["dispute"] = 0
                await call.answer("Hайперша заявка")
            else:
                data["dispute"] = step
                x = dispute_orders()[step]
                text = show_all_dispute_text(x)
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(close_dispute).add(ARROW_LEFT, ARROW_RIGHT, ADD_BUT_CANSEL)
                count = f"\nПОКАЗАНА {data['dispute'] + 1} З {len(dispute_orders())}"
                await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif call.data == ARROW_RIGHT.callback_data:
        async with state.proxy() as data:
            step = data["dispute"]
            step += 1
            if len(dispute_orders()) == 1:
                await call.answer("Єдина заявка")
            elif step > len(dispute_orders()) - 1:
                step = 0
                await call.answer("Hайперша заявка")
                data["dispute"] = step
                x = dispute_orders()[step]
                text = show_all_dispute_text(x)
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(close_dispute).add(ARROW_LEFT, ARROW_RIGHT, ADD_BUT_CANSEL)
                count = f"\nПОКАЗАНА {data['dispute'] + 1} З {len(dispute_orders())}"
                await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
            else:
                data["dispute"] = step
                x = dispute_orders()[step]
                text = show_all_dispute_text(x)
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(close_dispute).add(ARROW_LEFT, ARROW_RIGHT, ADD_BUT_CANSEL)
                count = f"\nПОКАЗАНА {data['dispute'] + 1} З {len(dispute_orders())}"
                await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id, reply_markup=keyboard)

    elif call.data == close_dispute.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SELLER_BUT, BUYER_BUT, ADD_BUT_CANSEL)
        async with state.proxy() as data:
            x = dispute_orders()[data["dispute"]]
            seller = x[7]
            buyer = x[4]
        await bot.edit_message_text("НА ЧИЮ КОРИСТЬ ЗАКРИВАЄМО СУПЕРЕЧКУ?\n\n"
                                    f"ID ПРОДАВЦЯ: {seller}\n"
                                    f"ПСЕВДОНІМ: @{get_name_user(seller)[4]} \n\n"
                                    f"ID ПОКУПЦЯ: {buyer}\n"
                                    f"ПСЕВДОНІМ: @{get_name_user(buyer)[4]}\n".upper(), call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard)
        await FSMAdmin.dispute_solution.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.dispute_solution)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data:
        async with state.proxy() as data:
            step = data["dispute"]
        if dispute_orders():
            x = dispute_orders()[step]
            text = show_all_dispute_text(x)
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(close_dispute).add(ARROW_LEFT, ARROW_RIGHT, ADD_BUT_CANSEL)
            count = f"\nПОКАЗАНА {data['dispute'] + 1} З {len(dispute_orders())}"
            await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
            await FSMAdmin.dispute.set()
        else:
            await call.answer(no_orders, show_alert=True)
    elif call.data == SELLER_BUT.callback_data or call.data == BUYER_BUT.callback_data:
        async with state.proxy() as data:
            if call.data == SELLER_BUT.callback_data:
                winner2 = "продавця"
                data["win"] = winner2
                data["winner"] = dispute_orders()[data["dispute"]][7]
                data["looser"] = dispute_orders()[data["dispute"]][4]
            elif call.data == BUYER_BUT.callback_data:
                winner2 = "покупця"
                data["win"] = winner2
                data["winner"] = dispute_orders()[data["dispute"]][4]
                data["looser"] = dispute_orders()[data["dispute"]][7]
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(APPROVE_NO, APPROVE_YES)
        await bot.edit_message_text(f"Підтверджуєте закриття заявки на користь: {winner2}".upper(), call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=keyboard)
    elif call.data == APPROVE_YES.callback_data or call.data == APPROVE_NO.callback_data:
        if call.data == APPROVE_YES.callback_data:
            async with state.proxy() as data:
                step = data["dispute"]
                order = dispute_orders()[step]
                dispute_orders_sold(order[0])
                winner = data["winner"]
                looser = data["looser"]
                winner2 = data["win"]
                dispute_solution(order[0], winner, looser)
                text_seller = f"АРБІТРАЖ ПО ЗАЯВЦІ {order[0]} ЗАКРИТО НА КОРИСТЬ {winner2}\n".upper()
                text_buyer = f"АРБІТРАЖ ПО ЗАЯВЦІ {order[0]} ЗАКРИТО НА КОРИСТЬ {winner2}\n".upper()
                update_balance(winner, float(order[6]))
                if winner == order[7]:
                    text_seller += f"{float(order[6])} ГРН Зараховано НА ВАШ БАЛАНС.".upper()
                elif winner == order[4]:
                    text_buyer += f"{float(order[6])} ГРН повернуто НА ВАШ БАЛАНС.".upper()
                await call.answer(f"Закрив заявку під номером {order[0]} на користь: {winner2}", show_alert=True)
                await bot.send_message(id_group_log, f"{call.from_user.id} АДМІН ЗАКРИВ АРБІТРАЖ "
                                                     f"№{order[0]} НА КОРИСТЬ {winner2} {data['winner']}".upper())
                try:
                    await bot.send_message(order[4], text_buyer.upper())
                except Exception:
                    pass
                try:
                    await bot.send_message(order[7], text_seller.upper())
                except Exception:
                    pass

        if dispute_orders():
            x = dispute_orders()[0]
            text = show_all_dispute_text(x)
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(close_dispute).add(ARROW_LEFT, ARROW_RIGHT, ADD_BUT_CANSEL)
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
            await FSMAdmin.dispute.set()
        else:
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(ADD_BUT_CANSEL)
            await bot.edit_message_text("Заявок не має".upper(), call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.dispute.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.add_summ)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ARROW_LEFT.callback_data:
        print(579)
        async with state.proxy() as data:
            all_adds = [text_process_admin_add(x) for x in get_all_balance_add()]
            step = data["step"] - 1
            if len(all_adds) == 1:
                data["step"] = 0
                await call.answer("Це єдина заявка")
            elif step < 0:
                data["step"] = 0
                await call.answer("Це найперша заявка")
            else:
                data["step"] = step
                data["order"] = all_adds[step]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_adds[step], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
    elif call.data == ARROW_RIGHT.callback_data:
        print(597)
        async with state.proxy() as data:
            all_adds = [text_process_admin_add(x) for x in get_all_balance_add()]
            step = data["step"] + 1
            data["step"] = step
            if len(all_adds) == 1:
                data["step"] = 0
                await call.answer(alon_order)
            elif len(all_adds) <= 0:
                await call.answer(no_orders)
            elif step > len(all_adds) - 1:
                step = 0
                data["step"] = 0
                data["order"] = all_adds[step]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_adds[step], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_adds[step], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
    elif call.data == "ADD_BUT_CANSEL":
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
        await FSMAdmin.where.set()
    elif call.data == ADMIN_BUT_APPROVE.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
        await bot.send_message(call.message.chat.id, APPROVE_ADD_SUMM, reply_markup=keyboard)
        await FSMAdmin.approve_action.set()
    elif call.data == ADMIN_BUT_CANSEL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2).add(ADD_BUT_CANSEL)
        await bot.edit_message_text("вкажіть причину скасування:".upper(), call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard)
        await FSMAdmin.describe_action_add.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.down_summ)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ARROW_LEFT.callback_data:
        async with state.proxy() as data:
            all_downs = [text_process_admin_down(x) for x in get_all_balance_down()]
            step = data["step"] - 1
            if len(all_downs) == 1:
                data["step"] = 0
                await call.answer("Це єдина заявка")
            elif step < 0:
                data["step"] = 0
                await call.answer("Це найперша заявка")
            else:
                data["step"] = step
                data["order"] = all_downs[step]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_downs[step], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
    elif call.data == ARROW_RIGHT.callback_data:
        async with state.proxy() as data:
            all_downs = [text_process_admin_down(x) for x in get_all_balance_down()]
            step = data["step"] + 1
            data["step"] = step
            if len(all_downs) == 1:
                data["step"] = 0
                await call.answer("Це єдина заявка")
            elif len(all_downs) <= 0:
                await call.answer(no_orders)
            elif step > len(all_downs) - 1:
                step = 0
                data["step"] = 0
                data["order"] = all_downs[step]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_downs[step], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
                await bot.edit_message_text(all_downs[step], call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
    elif call.data == ADD_BUT_CANSEL.callback_data:
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
        await FSMAdmin.where.set()
    elif call.data == ADMIN_BUT_APPROVE.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
        async with state.proxy() as data:
            order = get_all_balance_down()[data["step"]]
        await bot.send_message(call.message.chat.id, APPROVE_DOWN_SUMM2(order[0]), reply_markup=keyboard)
        await FSMAdmin.approve_action_down2.set()
    elif call.data == ADMIN_BUT_CANSEL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2).add(ADD_BUT_CANSEL)
        await bot.edit_message_text("вкажіть причину скасування:".upper(), call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard)
        await FSMAdmin.describe_action_down.set()


@dp.callback_query_handler(lambda call: True, state=[FSMAdmin.approve_action_add2, FSMAdmin.describe_action_add,])
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == APPROVE_YES.callback_data:
        all_adds = [text_process_admin_add(x) for x in get_all_balance_add()]
        async with state.proxy() as data:
            step = data["step"]
            order = get_all_balance_add()[step]
        now = get_balance_by_id(order[4])
        update_balance_status(order[0], "cansel", True)
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(id_group_log, f"{call.from_user.id} АДМІН Скасував ЗАЯВКУ №{order[0]} "
                                                  f"НА ПОПОВЕННЯ {order[1]} ГРН".upper())
        await bot.send_message(order[4], f"заявку на ПОПОВНЕННЯ балансу скасовано адміністратором.\nпричина: "
                                         f"{data['describe_add']}".upper())
        await bot.send_message(call.message.chat.id, f"СКАСОВАНО ПОПОВЕННЯ БАЛАНСУ\n\n{all_adds[step]}\n"
                                                     f"поточний баланс кліента: {now} ГРН".upper(),
                               reply_markup=keyboard)
    elif call.data == APPROVE_NO.callback_data or call.data == ADD_BUT_CANSEL.callback_data:
        all_adds = [text_process_admin_add(x) for x in get_all_balance_add()]
        if len(all_adds) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_adds[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
            await bot.edit_message_text(all_adds[0], call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.add_summ.set()
        else:
            keyboard = InlineKeyboardMarkup(row_width=3)
            keyboard.add(ADD_BUT_CANSEL)
            await bot.edit_message_text("3АЯВОК НЕ МАЄ", call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.add_summ.set()


@dp.message_handler(content_types=['text'], state=FSMAdmin.describe_action_add)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["describe_add"] = msg.text
    keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
    await bot.send_message(msg.from_user.id, APPROVE_down_ADD, reply_markup=keyboard)
    await FSMAdmin.approve_action_add2.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.approve_action_down2)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == APPROVE_YES.callback_data:
        all_downs = [text_process_admin_down(x) for x in get_all_balance_down()]
        async with state.proxy() as data:
            step = data["step"]
            order = get_all_balance_down()[step]
        before = get_balance_by_id(order[4])
        # update_balance(order[4], -order[1])
        now = get_balance_by_id(order[4])
        update_balance_status(order[0], "approve")
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        user_ref = user_by_ref(order[4])
        if user_ref:
            new_money = float(order[1]) / 100 * int(get_ref_tax())
            upload_partner_balance(user_ref, new_money)
        now = get_balance_by_id(order[4])
        await bot.edit_message_text(id_group_log, f"{call.from_user.id} АДМІН ПІДТВЕРДИВ ЗАЯВКУ №{order[0]} "
                                                  f"НА ВИВЕДЕННЯ {order[1]} ГРН")
        await bot.send_message(order[4], "ЗАЯВКУ НА ВИВЕДЕННЯ КОШТІВ СХВАЛЕНО. ОЧІКУЙТЕ ПЕРЕКАЗ НАЙБЛИЖЧИМ ЧАСОМ".upper())
        await bot.send_message(call.message.chat.id, f"{all_downs[step]}"
                                                     f"Попередній баланс: {before} ГРН\n"
                                                     f"поточний баланс: {now} ГРН".upper(), reply_markup=keyboard)
    elif call.data == APPROVE_NO.callback_data or call.data == ADD_BUT_CANSEL.callback_data:
        all_downs = [text_process_admin_down(x) for x in get_all_balance_down()]
        if len(all_downs) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_downs[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
            await bot.edit_message_text(all_downs[0], call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.down_summ.set()
        else:
            keyboard = InlineKeyboardMarkup(row_width=3)
            keyboard.add(ADD_BUT_CANSEL)
            await bot.edit_message_text("3АЯВОК НЕ МАЄ", call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.down_summ.set()


@dp.message_handler(content_types=['text'], state=FSMAdmin.describe_action_down)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["describe_down"] = msg.text
    keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
    await bot.send_message(msg.from_user.id, APPROVE_down_SUMM, reply_markup=keyboard)
    await FSMAdmin.approve_action_down.set()


@dp.callback_query_handler(lambda call: True, state=[FSMAdmin.approve_action_down, FSMAdmin.describe_action_down])
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == APPROVE_YES.callback_data:
        all_downs = [text_process_admin_down(x) for x in get_all_balance_down()]
        async with state.proxy() as data:
            step = data["step"]
            order = get_all_balance_down()[step]
        update_balance_status(order[0], "cansel")
        update_balance(order[4], order[1])
        now = get_balance_by_id(order[4])
        keyboard = InlineKeyboardMarkup(row_width=3)
        keyboard.add(ADD_BUT_CANSEL)
        await bot.send_message(id_group_log, f"{call.from_user.id} АДМІН скасував ЗАЯВКУ №{order[0]} "
                                             f"НА ВИВЕДЕННЯ {order[1]} ГРН".upper())
        await bot.send_message(order[4], f"заявку на виведення коштів скасовано адміністратором. \nпричина: "
                                         f"{data['describe_down']}\n\n{order[1]} ГРН повернуто на баланс".upper())
        await bot.send_message(call.message.chat.id, f"СКАСОВАНО ВИВЕДЕННЯ КОШТІВ\n\n{all_downs[step]}"
                                                     f"Поточний баланс: {now} ГРН", reply_markup=keyboard)
    elif call.data == APPROVE_NO.callback_data or call.data == ADD_BUT_CANSEL.callback_data:
        all_downs = [text_process_admin_down(x) for x in get_all_balance_down()]
        if len(all_downs) > 0:
            async with state.proxy() as data:
                data["step"] = 0
                data["order"] = all_downs[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ADMIN_BUT_CANSEL, ADMIN_BUT_APPROVE).add(ADD_BUT_CANSEL)
            await bot.edit_message_text(all_downs[0], call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.down_summ.set()
        else:
            keyboard = InlineKeyboardMarkup(row_width=3)
            keyboard.add(ADD_BUT_CANSEL)
            await bot.edit_message_text("3АЯВОК НЕ МАЄ", call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdmin.down_summ.set()


@dp.message_handler(content_types=['text'], state=FSMAdmin.change_balance)
async def back(msg: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.add(ADD_BUT_CANSEL)
    try:
        id_user = int(msg.text)
        if get_balance_by_id(id_user):
            async with state.proxy() as data:
                data["user_id"] = id_user
            text = "користувача знайдено:\n" \
                   f"поточний баланс: {get_balance_by_id(id_user)} грн\n\n" \
                   f"введіть сумму для зміни".upper()
            await bot.send_message(msg.chat.id, text, reply_markup=keyboard)
            await FSMAdmin.change_balance2.set()
        else:
            await bot.send_message(msg.chat.id, "за цим Ід користувача не знайдено".upper(),
                                   reply_markup=keyboard)

    except ValueError:
        await bot.send_message(msg.chat.id, "це не схоже на ІД користувача".upper(),
                               reply_markup=keyboard)


@dp.message_handler(content_types=['text'], state=FSMAdmin.change_balance2)
async def back(msg: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(ADD_BUT_CANSEL)
    try:
        value = float(msg.text)
        async with state.proxy() as data:
            update_balance(data["user"], value)
            await bot.send_message(id_group_log, f"{msg.from_user.id} АДМІН ЗМІНИВ БАЛАНС КОРИСТУВАЧА "
                                                 f"{data['user']} НА {value} ГРН")
            text = f"оновив баланс користувача: {data['user']}\n" \
                   f"поточний баланс: {get_balance_by_id(data['user'])} ГРН"
        await bot.send_message(msg.chat.id, text.upper(), reply_markup=keyboard)
    except ValueError:
        await bot.send_message(msg.chat.id, "щось не так".upper(), reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True, state=FSMAdmin.change_balance2)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SEND_MSG, CHANGE_BALANCE, BAN)
        keyboard.add(CR_CANSEL)
        async with state.proxy() as data:
            await bot.edit_message_text(MEMBERS(data["user"]), call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
    await FSMAdmin.all_users.set()


@dp.callback_query_handler(lambda call: True, state=[FSMAdmin.approve_action_down, FSMAdmin.describe_action_down])
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == "ADD_BUT_CANSEL" or call.data == APPROVE_NO.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SEND_MSG, CHANGE_BALANCE, BAN)
        keyboard.add(CR_CANSEL)
        async with state.proxy() as data:
            await bot.send_message(call.message.message_id,
                                   LS_TEXT(data["user"]).replace("ОСОБИСТИЙ КАБІНЕТ", "").replace("МІЙ", ""),
                                   reply_markup=keyboard)
        await FSMAdmin.all_users.set()


@dp.callback_query_handler(lambda call: True, state=[FSMAdmin.change_balance, FSMAdmin.send, FSMAdmin.admins,])
async def back(call, state: FSMContext):
    if call.data == "ADD_BUT_CANSEL" or call.data == APPROVE_NO.callback_data:
        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
    elif call.data == APPROVE_YES.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(ADD_BUT_CANSEL)
        async with state.proxy() as data:
            count = 0
            users = get_all_user2()
            for x in users:
                try:
                    but = data["send_but"]
                    await bot.send_message(x[0], data["send"], parse_mode='HTML',
                                           reply_markup=send_but(data["send_but"][0], data["send_but"][1]))
                    count += 1
                except KeyError:
                    await bot.send_message(x[0], data["send"], parse_mode='HTML', )
                    count += 1
                except Exception:
                    pass
        await call.answer(f"Розсилка відправлена\n"
                          f"Всього юзерів: {len(users)}\n"
                          f"Отримали повідомлення: {count}", show_alert=True)

        await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                    reply_markup=admin_but())
    await FSMAdmin.where.set()


@dp.message_handler(content_types=['text'], state=FSMAdmin.send)
async def back(msg: types.Message, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(APPROVE_NO, APPROVE_YES, ADD_BUT_CANSEL)
    async with state.proxy() as data:
        data["send"] = msg.text
        if "#" in msg.text:
            f = msg.text.split("#")
            but_name = f[-2]
            but_link = f[-1]
            if len(f) == 3:
                data["send"] = f[0]
                data["send_but"] = (but_name, but_link)
                try:
                    await bot.send_message(msg.chat.id, data["send"], parse_mode='HTML',
                                           reply_markup=send_but(data["send_but"][0],
                                                                 data["send_but"][1]))
                except BadRequest:
                    await bot.send_message(msg.chat.id, "Цей лінк не працює перевір його та спробуй ще".upper(), )
            else:
                await bot.send_message(msg.chat.id, "щось тут не так".upper(), )
        else:
            await bot.send_message(msg.chat.id, data["send"], parse_mode='HTML')
        await bot.send_message(msg.chat.id, "Ви підтверджуєте розсилку за цим текстом?".upper(),
                               parse_mode='HTML',
                               reply_markup=keyboard)


# @dp.message_handler(content_types=['text'], state=FSMAdmin.admins)
# async def back(msg: types.Message, state: FSMContext):
#     if msg.text.isdigit():
#         keyboard = InlineKeyboardMarkup(row_width=2)
#         keyboard.add(ADD_BUT_CANSEL)
#         try:
#             id_user = int(msg.text)
#             if id_user in admins():
#                 admins_delete(id_user)
#                 text = "Ось оновлений список адмінів \n"
#                 for x in admins():
#                     text += f"{x}\n"
#                 await msg.answer(("видалив адміна\n" + text).upper(), reply_markup=keyboard)
#             else:
#                 admins_add(id_user)
#                 text = "Ось оновлений список адмінів \n"
#                 for x in admins():
#                     text += f"{x}\n"
#                 await msg.answer(("додав адміна\n" + text).upper(), reply_markup=keyboard)
#
#         except ValueError:
#             keyboard = InlineKeyboardMarkup(row_width=2)
#             keyboard.add(ADD_BUT_CANSEL)
#             await msg.answer("щось не так".upper(), reply_markup=keyboard)
#     else:
#         keyboard = InlineKeyboardMarkup(row_width=2)
#         keyboard.add(ADD_BUT_CANSEL)
#         await msg.answer("цен не сxоже на ід".upper(), reply_markup=keyboard)
