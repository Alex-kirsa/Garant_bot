from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
from all_states import *
from dispatcher import *
from buttons import *
from privet_room import *
from database import *
from text import *
from aiogram.utils.exceptions import MessageNotModified
from config import id_group_log


@dp.callback_query_handler(lambda call: True, state=FSMAllOrders.step1)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == "ADD_BUT_CANSEL" or call.data == PRIVET_ROOM_BUT.callback_data:
        await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()
    elif call.data == CANSEL_ALL_ORDERS.callback_data:
        async with state.proxy() as data:
            keyboard = InlineKeyboardMarkup(row_width=2)
            orders = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10])
                      for x in room_filter(LIST_POKER_ROOMS_BUT2[data["kind_number"]].text)]
            data["id_order"] = room_filter(LIST_POKER_ROOMS_BUT2[data["kind_number"]].text)[data['step']]
            data["order"] = orders[data['step']]
            # if call.from_user.id == orders[data['step']]:
            #     keyboard.add(EDIT_ORDER)
            if call.from_user.id in admins():
                keyboard.insert(ADMIN_BUT_CANSEL)
            if data["kind"] == "sell":
                keyboard.add(BUY, SELL_lower,)
            else:
                keyboard.add(BUY_lower, SELL, )
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER, LIST_POKER_ROOMS_BUT2[data["kind_number"]]). \
                add(CANSEL_LS, GET_ORDER)
            count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders)}"
            await bot.edit_message_text(f"{orders[data['step']]}{count}", call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
    elif call.data == CANSEL_ALL_GET_ORDER.callback_data:
        async with state.proxy() as data:
            if data["id_order"][6] != 13: # call.from_user.id треба замінити
                part = data["by_usd"]
                full_order = data["id_order"]
                order = data["order"] + f"\nНА ВАШОМУ БАЛАНСІ: {get_balance_by_id(call.from_user.id)} грн.\nЗА {part} " \
                                        f"{data['id_order'][10]} ви віддаєте {part * full_order[3]} ГРН.".upper()
                mail = data["by_mail"]
                if not order:
                    await call.answer("ЯК ГАДАЄШЬ ЩО БУДЕ КОЛИ ОБРАТИ НЕ ІСНУЮЧУ ЗАЯВКУ", show_alert=True)
                else:
                    await bot.send_message(call.message.chat.id, order,
                                           reply_markup=BY_ORDER_FINAL(part, mail, data["id_order"][10]))
            else:
                await call.answer("Не можна купляти власні заявки", show_alert=True)
    elif call.data == ARROW_LEFT.callback_data:
        async with state.proxy() as data:
            kind_order = data["kind"]
            kind = LIST_POKER_ROOMS_BUT2[data["kind_number"]]
            if kind_order == "sell":
                if room_filter(kind.text):
                    orders = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10])
                              for x in room_filter(kind.text)]
            elif kind_order == "buy":
                orders_raw = room_filter_buy(kind.text)
                if orders_raw:
                    orders = [show_order_buyer_text(x, "show") for x in orders_raw]
            step = data["step"] - 1
            if len(orders) == 1:
                data["step"] = 0
                data["order"] = orders[0]
                await call.answer("Це єдина заявка")
            elif len(orders) <= 0:
                data["step"] = 0
                data["order"] = False
                await call.answer("Я ж кажу, заявок немає")
            elif step < 0:
                data["order"] = orders[0]
                data["step"] = 0
                await call.answer("Це найперша заявка")
            else:
                data["step"] = step
                data["order"] = orders[step]
                if data["kind"] == "sell":
                    data["id_order"] = room_filter(LIST_POKER_ROOMS_BUT2[data["kind_number"]].text)[step]
                else:
                    data["id_order"] = room_filter_buy(LIST_POKER_ROOMS_BUT2[data["kind_number"]].text)[step]
                keyboard = InlineKeyboardMarkup(row_width=2)
                # if call.from_user.id == data["id_order"][6]:
                #     keyboard.add(EDIT_ORDER)
                if call.from_user.id in admins():
                    keyboard.insert(ADMIN_BUT_CANSEL)
                if data["kind"] == "sell":
                    keyboard.add(BUY, SELL_lower, )
                else:
                    keyboard.add(BUY_lower, SELL, )
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER,
                             LIST_POKER_ROOMS_BUT2[data["kind_number"]], CANSEL_LS, GET_ORDER)
                count = f"\nПОКАЗАНА {data['step']+1} З {len(orders)}"
                await bot.edit_message_text(f"{orders[step]}{count}", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
    elif call.data == ARROW_RIGHT.callback_data:
        async with state.proxy() as data:
            kind_order = data["kind"]
            kind = LIST_POKER_ROOMS_BUT2[data["kind_number"]]
            if kind_order == "sell":
                if room_filter(kind.text):
                    orders = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10])
                              for x in room_filter(kind.text)]
                    orders_raw = room_filter(kind.text)
            elif kind_order == "buy":
                orders_raw = room_filter_buy(kind.text)
                if orders_raw:
                    orders = [show_order_buyer_text(x, "show") for x in orders_raw]
            step = data["step"] + 1
            data["step"] = step
            if len(orders) == 1:
                data["order"] = orders[0]
                await call.answer("Це єдина заявка")
            elif len(orders) <= 0:
                data["order"] = False
                await call.answer("Я ж кажу, заявок немає")
            elif step > len(orders) - 1:
                step = 0
                data["step"] = 0
                data["order"] = orders[step]
                data["id_order"] = orders_raw[step]
                keyboard = InlineKeyboardMarkup(row_width=2)
                # if call.from_user.id == get_all_orders()[step][6]:
                #     keyboard.add(EDIT_ORDER)
                if call.from_user.id in admins():
                    keyboard.insert(ADMIN_BUT_CANSEL)
                if data["kind"] == "sell":
                    keyboard.add(BUY_lower, SELL, )
                else:
                    keyboard.add(BUY, SELL_lower, )
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER,
                             LIST_POKER_ROOMS_BUT2[data["kind_number"]], CANSEL_LS, GET_ORDER)
                count = f"\nПОКАЗАНА {data['step']+1} З {len(orders)}"
                await bot.edit_message_text(f"{orders[step]}{count}", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            else:
                data["order"] = orders[step]
                if data["kind"] == "sell":
                    data["id_order"] = room_filter(LIST_POKER_ROOMS_BUT2[data["kind_number"]].text)[step]
                else:
                    data["id_order"] = room_filter_buy(LIST_POKER_ROOMS_BUT2[data["kind_number"]].text)[step]

                keyboard = InlineKeyboardMarkup(row_width=2)
                # if call.from_user.id == data["id_order"][6]:
                #     keyboard.add(EDIT_ORDER)
                if call.from_user.id in admins():
                    keyboard.insert(ADMIN_BUT_CANSEL)
                if data["kind"] == "sell":
                    keyboard.add(BUY_lower, SELL, )
                else:
                    keyboard.add(BUY, SELL_lower, )
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER,
                             LIST_POKER_ROOMS_BUT2[data["kind_number"]], CANSEL_LS, GET_ORDER)
                count = f"\nПОКАЗАНА {data['step']+1} З {len(orders)}"
                await bot.edit_message_text(f"{orders[step]}{count}", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
    elif call.data == "ROOMS":
        async with state.proxy() as data:
            data["step"] = 0
            step = data["step"]
            if data["kind_number"] >= len(LIST_POKER_ROOMS_BUT2) - 1:
                data["kind_number"] = 0
            else:
                data["kind_number"] += 1
            kind = LIST_POKER_ROOMS_BUT2[data["kind_number"]]
            kind_order = data["kind"]
        keyboard = InlineKeyboardMarkup(row_width=2)
        if kind_order == "sell":
            if room_filter(kind.text):
                orders = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10])
                          for x in room_filter(kind.text)]
                async with state.proxy() as data:
                    data["order"] = orders[step]
                    data["id_order"] = room_filter(LIST_POKER_ROOMS_BUT2[data["kind_number"]].text)[step]
                # if call.from_user.id == data["id_order"][6]:
                #     keyboard.add(EDIT_ORDER)
                if call.from_user.id in admins():
                    keyboard.insert(ADMIN_BUT_CANSEL)
                if data["kind"] == "sell":
                    keyboard.add(BUY, SELL_lower, )
                else:
                    keyboard.add(BUY_lower, SELL, )
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER, kind, CANSEL_LS, GET_ORDER)
                count = f"\nПОКАЗАНА {data['step']+1} З {len(orders)}"
                await bot.edit_message_text(f"{orders[step]}{count}", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            else:
                keyboard.add(ROOM_FILTER, kind, CANSEL_LS)
                async with state.proxy() as data:
                    data["order"] = False
                await bot.edit_message_text("3А ЦИМ ФІЛЬТРОМ НЕ МАЄ ЗАЯВОК", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
        elif kind_order == "buy":
            orders_raw = room_filter_buy(kind.text)
            if orders_raw:
                orders = [show_order_buyer_text(x, "show") for x in orders_raw]
                async with state.proxy() as data:
                    data["order"] = orders[step]
                    data["id_order"] = room_filter_buy(LIST_POKER_ROOMS_BUT2[data["kind_number"]].text)[step]
                # if call.from_user.id == data["id_order"][6]:
                #     keyboard.add(EDIT_ORDER)
                if call.from_user.id in admins():
                    keyboard.insert(ADMIN_BUT_CANSEL)
                if data["kind"] == "sell":
                    keyboard.add(BUY, SELL_lower, )
                else:
                    keyboard.add(BUY_lower, SELL, )
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER, kind, CANSEL_LS, GET_ORDER)
                count = f"\nПОКАЗАНА {data['step']+1} З {len(orders)}"
                await bot.edit_message_text(f"{orders[step]}{count}", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            else:
                keyboard.add(ROOM_FILTER, kind, CANSEL_LS, )
                async with state.proxy() as data:
                    data["order"] = False
                await bot.edit_message_text("3А ЦИМ ФІЛЬТРОМ НЕ МАЄ ЗАЯВОК", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)

    elif call.data == ROOM_FILTER.callback_data:
        await call.answer(help_poker_room, show_alert=True)
    elif call.data == GET_ORDER.callback_data:
        async with state.proxy() as data:
            if data["id_order"][6] != call.from_user.id:
                data["by_usd"] = data["id_order"][4]
                part = data["by_usd"]
                full_order = data["id_order"]
                data["by_mail"] = "вкажіть дані"
                mail = data["by_mail"]
                comments = ""
                if get_custom_info(full_order[6]):
                    comments = f"\nКОМЕНТАР: {get_custom_info(full_order[6])[4]}\n"
                if data["kind"] == "sell":
                    order = data["order"] + comments + f"\nНА ВАШОМУ БАЛАНСІ: {get_balance_by_id(call.from_user.id)} " \
                                                       f"грн.\nЗА {part}{data['id_order'][10]} ви віддаєте " \
                                                       f"{part * full_order[3]} ГРН.".upper()

                    if not order:
                        await call.answer("ЯК ГАДАЄШЬ ЩО БУДЕ КОЛИ ОБРАТИ НЕ ІСНУЮЧУ ЗАЯВКУ", show_alert=True)
                    else:
                        await bot.send_message(call.message.chat.id, order,
                                               reply_markup=BY_ORDER_FINAL(part, mail, data["id_order"][10]))
                elif data["kind"] == "buy":
                    order = data[
                                "order"] + comments + f"\nНА ВАШОМУ БАЛАНСІ: {get_balance_by_id(call.from_user.id)}" \
                                                      f" грн.\nЗА {part} " \
                                                      f"{data['id_order'][10]} ви ОТРИМАЄТЕ " \
                                                      f"{part * full_order[3]} ГРН.".upper()
                    if not order:
                        await call.answer("ЯК ГАДАЄШЬ ЩО БУДЕ КОЛИ ОБРАТИ НЕ ІСНУЮЧУ ЗАЯВКУ", show_alert=True)
                    else:
                        await bot.send_message(call.message.chat.id, order,
                                               reply_markup=BY_ORDER_FINAL_SELL(part, mail, data["id_order"][10]))
            else:
                await call.answer("Не можна купляти власні заявки", show_alert=True)
    elif call.data == "BY_ORDER_FINAL":
        await call.answer(help_by_usd, show_alert=True)
    elif call.data == "BY_ORDER_FINAL2":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text("ВВЕДІТЬ СУММУ ПОКУПКИ:", call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAllOrders.change_usd.set()
    elif call.data == "BY_ORDER_MAIL":
        await call.answer(help_login, show_alert=True)
    elif call.data == "BY_ORDER_MAIL2":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text("ВВЕДІТЬ ВАШ E-MAIL АБО LOGIN:", call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAllOrders.change_mail.set()
    elif call.data == "BY_ORDER_GET_ORDER":
        async with state.proxy() as data:
            usd = data["by_usd"] * data["id_order"][3]
            if data["kind"] == "sell" and usd > get_balance_by_id(call.from_user.id):
                await call.answer("На балансі не достатньо коштів", show_alert=True)
            elif data["by_mail"] == "вкажіть дані":
                await call.answer(NO_MAIL, show_alert=True)
            else:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0, CANSEL_ALL_GET_ORDER, ADD_BUT_STEP2)
                text = BY_FINALLY_TEXT(data["id_order"][5])
                if data["kind"] == "buy":
                    text = BY_FINALLY_TEXT2(data["id_order"][5])
                else:
                    text = BY_FINALLY_TEXT(data["id_order"][5])
                await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == ADD_BUT_RULES0.callback_data:
        async with state.proxy() as data:
            data["agreement"] = True
            # if data["kind"] == "sell":
            #     # await bot.send_message(id_group_log, f"{call.from_user.id} ПОГОДИВСЯ З ПРАВИЛАМИ КУПІВЛІ")
            # else:
            #     await bot.send_message(id_group_log, f"{call.from_user.id} ПОГОДИВСЯ З ПРАВИЛАМИ ПРОДАЖУ")
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES1, CANSEL_ALL_GET_ORDER, ADD_BUT_STEP2)
            if data["kind"] == "buy":
                text = BY_FINALLY_TEXT2(data["id_order"][5])
            else:
                text = BY_FINALLY_TEXT(data["id_order"][5])
            await bot.edit_message_text(text, call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=keyboard)
    elif call.data == ADD_BUT_RULES1.callback_data:
        async with state.proxy() as data:
            data["agreement"] = False
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0, CANSEL_ALL_GET_ORDER, ADD_BUT_STEP2)
            if data["kind"] == "buy":
                text = BY_FINALLY_TEXT2(data["id_order"][5])
            else:
                text = BY_FINALLY_TEXT(data["id_order"][5])
            await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == ADD_BUT_STEP2.callback_data:
        async with state.proxy() as data:
            try:
                keyboard = InlineKeyboardMarkup(row_width=2)
                check_agreement = data["agreement"]
                if data["kind"] == "sell":
                    check_order = get_order_by_id(data["id_order"][0])
                elif data["kind"] == "buy":
                    check_order = get_buyer_orders(data["id_order"][6], data["id_order"][0])
                if data["id_order"][3] == check_order[3]:
                    if check_agreement:
                        keyboard.add(PRIVET_ROOM_BUT)
                        order = data["id_order"]
                        time = datetime.now() + timedelta(minutes=order[5])
                        time = time.strftime("%d.%m.%Y, %H:%M")
                        reserve = order[3] * data["by_usd"]
                        if data["kind"] == "sell":
                            add_new_processing_order(order[0], data["by_usd"], time, call.from_user.id, reserve, order[6],
                                                     data["by_mail"], "sell")
                            update_balance(call.from_user.id, -float(reserve))
                            update_order(order[0], -float(data["by_usd"]))
                            # await bot.send_message(id_group_log, f"{call.from_user.id} ПОДАВ ЗАЯВКУ НА КУПІВЛЮ "
                            #                                      f"{data['by_usd']} "
                            #                                      f"{get_order_by_id(order[0])[10]} ЗАЯВКИ №{order[0]}")
                            await bot.edit_message_text("ВАША ЗУСТРІЧНА ЗАЯВКА ВІДПРАВЛЕНА ПРОДАВЦЮ\n"
                                                        f"ЧЕКАЙТЕ НА ЗАРАХУВАННЯ ПРОТЯГОМ {order[5]} ХВ.", call.message.chat.id,
                                                        call.message.message_id,
                                                        reply_markup=keyboard)
                            await bot.send_message(order[6], order_by_text(order))
                        elif data["kind"] == "buy":
                            keyboard = InlineKeyboardMarkup(row_width=2)
                            keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                            update_status_order_buy(order[0], reserve=reserve)
                            update_order_buy(order[0], -data["by_usd"])
                            add_new_processing_order(order[0], data["by_usd"], time, order[6], reserve,
                                                     call.from_user.id, data["by_mail"], "buy")
                            # raw_order = get_buyer_orders(order[6], order[0])

                            # await bot.send_message(id_group_log, f"{call.from_user.id} ПОДАВ ЗАЯВКУ НА ПРОДАЖ "
                            #                                      f"{data['by_usd']} {order[10]}\nЗАЯВКА ПОКУПКИ "
                            #                                      f"{order[0]}")
                            await bot.edit_message_text(f"ПЕРЕКАЖІТЬ: {data['by_usd']} {order[10]}\n\n"
                                                        f"ПОКЕР-РУМ: {order[1]}\n"
                                                        f"E-MAIL/LOGIN: {order[9]}\n\n"
                                                        f"ПРОТЯГОМ {order[5]} XB.\n\n"
                                                        f"КРАЙНІЙ СРОК: {time}", call.message.chat.id,
                                                        call.message.message_id,
                                                        reply_markup=keyboard)
                            data["fresh_order"] = get_process_order(order=[time, order[6], call.from_user.id,
                                                                           time_now()])
                            data["sell_order"] = order
                            data["fresh_order_time"] = time
                            await FSMMyOrders.step1.set()
                    else:
                        await call.answer("Прийміть правила сервісу")
                else:
                    await call.answer(f"За цією заявкою змінився курс!\nПопередній курс: {data['id_order'][3]}\n"
                                      f"Поточний курс: {check_order[3]}", show_alert=True)
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0, CANSEL_ALL_GET_ORDER, ADD_BUT_STEP2)
                    data["agreement"] = False
                    await bot.edit_message_text(BY_FINALLY_TEXT(data["id_order"][5]), call.message.chat.id,
                                                call.message.message_id,
                                                reply_markup=keyboard)
            except KeyError:
                await call.answer("Прийміть правила сервісу")
    elif call.data == PRIVET_ROOM_BUT.callback_data:
        await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()

    elif call.data == ADMIN_BUT_CANSEL.callback_data:

        keyboard = InlineKeyboardMarkup(row_width=2).add(ADD_BUT_CANSEL)
        await bot.edit_message_text("вкажіть причину скасування:".upper(), call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard)
        await FSMAllOrders.describe_action.set()

    elif call.data == EDIT_ORDER.callback_data:
        async with state.proxy() as data:
            order = data["id_order"]
            for x, y in enumerate(LIST_POKE_ROOMS_BUT):
                if y['text'] == order[1]:
                    room = x
                    break
            currency = 0
            for x, y in enumerate(LIST_POKE_CURRENCY):
                if y['text'] == order[10]:
                    currency = x
                    break
            data["NUM"] = order[0]
            data["USD"] = order[2]
            data["RATE"] = order[3]
            data["min_part"] = order[4]
            data["term"] = order[5]
            data["kind_number"] = room
            data["login"] = order[9]
            data["currency"] = currency
            data["edit"] = True
        await bot.edit_message_text(CREATE_ORDER_TEXT1(order[2], order[3]), call.message.chat.id,
                                    call.message.message_id, reply_markup=CREATE_BUTTS(order[2],
                                                                                       order[3],
                                                                                       order[4],
                                                                                       order[5],
                                                                                       room,
                                                                                       order[9],
                                                                                       currency))
        await FSMCreate.step1.set()
    elif call.data == BUY.callback_data or call.data == SELL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        async with state.proxy() as data:
            data["kind_number"] = 0
            data["step"] = 0
            if call.data == BUY.callback_data:
                orders_raw = get_all_orders()
                orders = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                          orders_raw]
                data["id_order"] = orders_raw[0] if orders_raw else None
                data["order"] = orders[0] if orders else None
                data["kind"] = "sell"
                await call.answer("Заявки на продаж")
                if call.from_user.id in admins() and orders:
                    keyboard.insert(ADMIN_BUT_CANSEL)
                keyboard.add(BUY_lower, SELL)
            elif call.data == SELL.callback_data:
                my_orders_buy = get_buyer_orders(all_order=True)
                orders = [show_order_buyer_text(x, "show") for x in my_orders_buy]
                data["id_order"] = my_orders_buy[0] if my_orders_buy else None
                data["order"] = orders[0] if orders else None
                data["kind"] = "buy"
                await call.answer("Заявки на купівлю")
                if call.from_user.id in admins() and orders:
                    keyboard.insert(ADMIN_BUT_CANSEL)
                keyboard.add(BUY, SELL_lower)
        if orders:
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER,
                         LIST_POKER_ROOMS_BUT2[data["kind_number"]],
                         CANSEL_LS, GET_ORDER)
            count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders)}"
            try:
                await bot.edit_message_text(orders[0] + count, call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            except MessageNotModified:
                pass
        else:
            keyboard.add(CANSEL_LS)
            try:
                await bot.edit_message_text("ЗАЯВОК ПОКУПКИ НЕМАЄ", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            except MessageNotModified:
                pass


@dp.message_handler(content_types=['text'], state=FSMAllOrders.describe_action)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["describe"] = msg.text
    keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
    await bot.send_message(msg.from_user.id, APPROVE_DELETE, reply_markup=keyboard)
    await FSMAllOrders.approve_action.set()


@dp.callback_query_handler(lambda call: True, state=FSMAllOrders.describe_action)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data:
        async with state.proxy() as data:
            keyboard = InlineKeyboardMarkup(row_width=2)
            # if call.from_user.id == data["id_order"][6]:
            #     keyboard.add(EDIT_ORDER)
            if call.from_user.id in admins():
                keyboard.insert(ADMIN_BUT_CANSEL)
            if data["kind"] == "sell":
                keyboard.add(BUY, SELL_lower,)
            else:
                keyboard.add(BUY_lower, SELL,)
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER, LIST_POKER_ROOMS_BUT2[data["kind_number"]],
                         CANSEL_LS, GET_ORDER)
            await bot.edit_message_text(data["order"], call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
        await FSMAllOrders.step1.set()


@dp.callback_query_handler(lambda call: True, state=FSMAllOrders.approve_action)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == APPROVE_YES.callback_data:
        async with state.proxy() as data:
            reason = data["describe"]
            text2 = ""
            if data["kind"] == "sell":
                order = get_all_orders()[data["step"]]
                text = "ПРОДАЖУ"
                delete_valid_order(order[6], order[1])
                update_status_close_admin(order[0])
            elif data["kind"] == "buy":
                order = get_buyer_orders(all_order=True)[data["step"]]
                text = "ПОКУПКИ"
                update_status_order_buy(order[0])
                update_balance(order[6], order[11])
                text2 = f"\n\n{order[11]} ГРН було повернуто на баланс".upper()

            try:
                await bot.send_message(order[6], f"заявку {text} №{order[0]}, було знято з вітрини адміністратором.\n"
                                                 f"причина: ".upper() + reason + text2)
            except Exception:
                pass
            # await bot.send_message(id_group_log, f"{call.from_user.id} АДМІН ВИДАЛИВ ЗАЯВКУ {text} З ВІТРИНИ "
            #                                      f"№{order[0]}")
    orders = False
    async with state.proxy() as data:
        if data["kind"] == "sell":
            orders = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                      get_all_orders()]
        elif data["kind"] == "buy":
            orders = [show_order_buyer_text(x, "show") for x in get_buyer_orders(all_order=True)]
    if orders:
        async with state.proxy() as data:
            keyboard = InlineKeyboardMarkup(row_width=2)
            if call.from_user.id in admins():
                keyboard.add(ADMIN_BUT_CANSEL)
            if data["kind"] == "sell":
                keyboard.add(BUY, SELL_lower,)
            else:
                keyboard.add(BUY_lower, SELL, )
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER, LIST_POKER_ROOMS_BUT2[data["kind_number"]],
                         CANSEL_LS, GET_ORDER)
            count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders)}"
        await bot.edit_message_text(orders[data["step"]]+count, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAllOrders.step1.set()
    else:
        keyboard = InlineKeyboardMarkup(row_width=2).add(ADD_BUT_CANSEL)
        await bot.edit_message_text("ЗАЯВОК НЕМАЄ", call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        await FSMAllOrders.step1.set()


@dp.message_handler(content_types=['text'], state=FSMAllOrders.change_usd)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = float(msg.text)
            min_part = data["id_order"][4]
            all_sum = data["id_order"][2]
            if text <= all_sum:
                if text >= min_part:
                    data["by_usd"] = float(msg.text)
                    part = data["by_usd"]
                    mail = data["by_mail"]
                    full_order = data["id_order"]
                    order = data["order"] + f"\nНА ВАШОМУ БАЛАНСІ: {round(get_balance_by_id(msg.from_user.id), 2)}" \
                                            f"ГРН.\nЗА {part} " \
                                            f"USD ви віддаєте {round(part * full_order[3], 2)} ГРН."
                    if data["kind"] == "sell":
                        await msg.answer(order, reply_markup=BY_ORDER_FINAL(part, mail, data["id_order"][10]))
                    else:
                        await msg.answer(order, reply_markup=BY_ORDER_FINAL_SELL(part, mail, data["id_order"][10]))
                    await FSMAllOrders.step1.set()
                else:
                    await msg.answer(F"ТІЛЬКИ СУМА більша ніж МІН. ЧАСТЦІ {min_part}")

            else:
                await msg.answer(F"ТІЛЬКИ СУМА МЕНШЕ або дорівнює {all_sum}".upper())
        except ValueError:
            await msg.answer("ТІЛЬКИ ЦИФРИ")


@dp.message_handler(content_types=['text'], state=FSMAllOrders.change_mail)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        part = data["by_usd"]
        full_order = data["id_order"]
        order = data["order"] + f"\nНА ВАШОМУ БАЛАНСІ: {get_balance_by_id(msg.from_user.id)}ГРН.\nЗА {part} " \
                                f"USD ви віддаєте {part * full_order[3]} ГРН.".upper()
        data["by_mail"] = msg.text
        mail = data["by_mail"]
    if data["kind"] == "sell":
        await msg.answer(order, reply_markup=BY_ORDER_FINAL(part, mail, data["id_order"][10]))
    else:
        await msg.answer(order, reply_markup=BY_ORDER_FINAL_SELL(part, mail, data["id_order"][10]))
    await FSMAllOrders.step1.set()


@dp.callback_query_handler(lambda call: True, state=[FSMAllOrders.change_usd, FSMAllOrders.change_mail])
async def back(call, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data:
        async with state.proxy() as data:
            await bot.send_message(call.message.chat.id, data["order"],
                                   reply_markup=BY_ORDER_FINAL(data["by_usd"], data["by_mail"], data["id_order"][10]))
        await FSMAllOrders.step1.set()
