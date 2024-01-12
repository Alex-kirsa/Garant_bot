from all_states import *
from aiogram.dispatcher import FSMContext
from dispatcher import *
from privet_room import *
from buttons import *
from text import *
from datetime import timedelta
from aiogram.utils import exceptions
from config import id_group_log


@dp.callback_query_handler(lambda call: True, state=FSMMyOrders.step1)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == "ADD_BUT_CANSEL" or call.data == CANSEL_LS.callback_data:
        await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()
    elif call.data == CANSEL_MY_ORDER.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SELLER_BUT, BUYER_BUT, ADD_BUT_CANSEL, MY_BALANCE)
        await bot.edit_message_text("ВИБЕРІТЬ ЯКІ ЗАЯВКИ ВИВЕСТИ:", call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMMyOrders.step1.set()
    elif call.data == MY_BALANCE.callback_data:
        add_orders, down_orders = get_balance_orders(call.from_user.id)
        orders = add_orders + down_orders
        if orders:
            async with state.proxy() as data:
                data["st_filter"] = 0
                data["step"] = 0
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BALANCE[data["st_filter"]],
                             ADD_BUT_CANSEL)
                count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders)}"
            await bot.edit_message_text(text_balance(orders[data["step"]]) + count, call.message.chat.id,
                                        call.message.message_id, reply_markup=keyboard)
            await FSMMyOrders.balance.set()
        else:
            await call.answer("Заявок не має")

    elif call.data == SELLER_BUT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        my_orders = get_all_my_orders(call.from_user.id)[0]
        solds = get_all_my_orders_bought(call.from_user.id)
        finally_order = get_all_my_orders_finally(call.from_user.id)
        done_orders = get_all_my_orders_sold(call.from_user.id)
        orders = solds[0] + finally_order[0] + my_orders + done_orders[0]
        async with state.proxy() as data:
            data["st_filter"] = 0
            data["step_my_order"] = 0
            if orders:
                order = orders[0]
                # if len(order) == 10:
                if order[5] in ("finally", "done", "dispute", "process", "cansel"):
                    if order[5] == "process":
                        keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                    if order[10] == "buy":
                        text = format_approve_order_text(order, get_buyer_orders(order[4], order[1]))
                    else:
                        text = format_approve_order_text(order, solds[1][0])
                # elif order[5] in ("finally", "done", "dispute", "process", "cansel"):
                #     text = format_approve_order_text(order, finally_order[1][0])
                # elif len(order) == 11:
                elif order[8] == "pause":
                    data["active"] = my_orders[0][0]
                    keyboard.add(ACTIVE_ORDER_BUT)
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                elif order[8] == "process" or order[8] == "cansel":
                    if order[8] == "process":
                        if call.from_user.id == order[6]:
                            keyboard.add(my_order_stop)
                            keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER)
                        else:
                            keyboard.add(ADMIN_BUT_CANSEL)

                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                    data["stop_order"] = order
                else:
                    print(order)
                    data["stop_order"] = order
                keyboard.add(ARROW_LEFT,
                             ARROW_RIGHT, STATUS_FILTER_BUT,
                             LIST_STATUS_SELLER_BUT[data["st_filter"]], CANSEL_MY_ORDER)
                try:
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                    await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                except exceptions.MessageNotModified as ex:
                    print("повідомлення не змінилось")
                    pass
            else:
                await call.answer("Заявок не має",)
    elif call.data == BUYER_BUT.callback_data:
        my_orders, my_buyers = get_all_my_orders(call.from_user.id)
        my_orders_buy = get_buyer_orders(call.from_user.id)
        orders = [show_buyer_text(x) for x in my_buyers]
        orders_buy = [show_order_buyer_text(x) for x in my_orders_buy]
        orders += orders_buy
        my_buyers += my_orders_buy
        if my_buyers:
            async with state.proxy() as data:
                data["st_filter"] = 0
                data["step_my_order"] = 0
                data["order"] = orders[0]
                keyboard = InlineKeyboardMarkup(row_width=2)
                if my_buyers[0][5] == "finally":
                    keyboard.add(APPROVE_ORDER_BUT)
                elif len(my_buyers[0]) == 12 and my_buyers[0][8] == "process":
                    data["NUM_order"] = my_buyers[0][0]
                    data["len_orders"] = len(orders)
                    keyboard.add(ORDER_CANSEL, EDIT_ORDER)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                             ADD_BUT_CANSEL)
                count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
            await bot.edit_message_text(orders[0] + count, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
            await FSMMyOrders.bayer.set()
        else:
            await call.answer("Заявок не має")
    elif call.data == ARROW_LEFT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        async with state.proxy() as data:
            step = data["step_my_order"] - 1
            data["step_my_order"] = step
            if LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "ALL":
                my_orders = get_all_my_orders(call.from_user.id)[0]
                solds = get_all_my_orders_bought(call.from_user.id)
                finally_order = get_all_my_orders_finally(call.from_user.id)
                dispute_order = get_all_my_orders_dispute(call.from_user.id)
                done_orders = get_all_my_orders_sold(call.from_user.id)
                orders = solds[0] + finally_order[0] + my_orders + dispute_order[0] + done_orders[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "finally":
                solds = get_all_my_orders_finally(call.from_user.id)
                orders = solds[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "sold":
                my_orders = get_all_my_orders_bought(call.from_user.id)
                orders = my_orders[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "dispute":
                dispute_order = get_all_my_orders_dispute(call.from_user.id)
                orders = dispute_order[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "done":
                done_orders = get_all_my_orders_sold(call.from_user.id)
                orders = done_orders[0]
            else:
                stat = LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data
                orders = get_all_my_orders(call.from_user.id, status=stat)[0]
            if not orders:
                await call.answer("Заявкок не має")
            elif step <= -1:
                await call.answer("Це перша заявка")
                step = 0
                data["step_my_order"] = 0
            if orders:
                order = orders[step]
                data["order1"] = order
                # Виявляємо тип повідомлення
                # if len(order) == 10:
                if order[5] == "process" or order[5] == "cansel":
                    if order[5] == "process":
                        keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                    if order[10] == "buy":
                        text = format_approve_order_text(order, get_buyer_orders(order[4], order[1]))
                    else:
                        text = format_approve_order_text(order, solds[1][0])
                elif order[5] == "finally":
                    text = format_approve_order_text(order, finally_order[1][0])
                elif order[5] == "done" or order[5] == "SOLD":
                    text = format_approve_order_text(order, done_orders[1][0])
                elif order[5] == "dispute":
                    text = format_approve_order_text(order, dispute_order[1][0])
                # elif len(order) == 11:
                elif order[8] == "pause":
                    data["active"] = my_orders[0][0]
                    keyboard.add(ACTIVE_ORDER_BUT)
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                    data["stop_order"] = order
                elif order[8] == "process" or order[8] == "cansel":
                    if order[8] == "process":
                        if call.from_user.id == order[6]:
                            keyboard.add(my_order_stop)
                            keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER)
                        else:
                            keyboard.add(ADMIN_BUT_CANSEL)
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                    data["stop_order"] = order
                keyboard.add(ARROW_LEFT,
                             ARROW_RIGHT, STATUS_FILTER_BUT,
                             LIST_STATUS_SELLER_BUT[data["st_filter"]], CANSEL_MY_ORDER)
                try:
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                    await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                except exceptions.MessageNotModified as ex:
                    pass
                except Exception:
                    pass
    elif call.data == ARROW_RIGHT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        async with state.proxy() as data:
            step = data["step_my_order"] + 1
            data["step_my_order"] = step
            if LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "ALL":
                my_orders = get_all_my_orders(call.from_user.id)[0]
                solds = get_all_my_orders_bought(call.from_user.id)
                finally_order = get_all_my_orders_finally(call.from_user.id)
                dispute_order = get_all_my_orders_dispute(call.from_user.id)
                done_orders = get_all_my_orders_sold(call.from_user.id)
                orders = solds[0] + finally_order[0] + my_orders + dispute_order[0] + done_orders[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "finally":
                solds = get_all_my_orders_finally(call.from_user.id)
                orders = solds[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "sold":
                my_orders = get_all_my_orders_bought(call.from_user.id)
                orders = my_orders[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "dispute":
                dispute_order = get_all_my_orders_dispute(call.from_user.id)
                orders = dispute_order[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "done":
                done_orders = get_all_my_orders_sold(call.from_user.id)
                orders = done_orders[0]
            else:
                stat = LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data
                orders = get_all_my_orders(call.from_user.id, status=stat)[0]
            if not orders:
                await call.answer("Заявкок не має")
            elif len(orders) == 1:
                await call.answer("Це єдина заявка")
                step = 0
                data["step_my_order"] = 0
            elif step > len(orders) - 1:
                step = 0
                data["step_my_order"] = 0
                await call.answer("Повернулись на початок")
            if orders:
                order = orders[step]
                data["order1"] = order
               # Виявляємо тип повідомлення
               #  if len(order) == 10:
                if order[5] == "process" or order[5] == "cansel":
                    if order[5] == "process":
                        keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                    if order[10] == "buy":
                        text = format_approve_order_text(order, get_buyer_orders(order[4], order[1]))
                    else:
                        text = format_approve_order_text(order, solds[1][0])
                elif order[5] == "finally":
                    text = format_approve_order_text(order, finally_order[1][0])
                elif order[5] == "done" or order[5] == "SOLD":
                    if order[10] == "buy":
                        text = format_approve_order_text(order, get_buyer_orders(order[4], order[1]))
                    else:
                        text = format_approve_order_text(order, done_orders[1][0])
                elif order[5] == "dispute":
                    text = format_approve_order_text(order, dispute_order[1][0])
                # elif len(order) == 11:
                elif order[8] == "pause":
                    keyboard.add(ACTIVE_ORDER_BUT)
                    data["active"] = order[0]
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                    data["stop_order"] = order
                elif order[8] == "process" or order[8] == "cansel":
                    if order[8] == "process":
                        if call.from_user.id == order[6]:
                            keyboard.add(my_order_stop)
                            keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER)
                        else:
                            keyboard.add(ADMIN_BUT_CANSEL)
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                    data["stop_order"] = order
                keyboard.add(ARROW_LEFT,
                             ARROW_RIGHT, STATUS_FILTER_BUT,
                             LIST_STATUS_SELLER_BUT[data["st_filter"]], CANSEL_MY_ORDER)
                try:
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                    await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                except exceptions.MessageNotModified as ex:
                    print("повідомлення не змінилось")
                    pass

    # Активувати заявку зі стадії пауза
    elif call.data == ACTIVE_ORDER_BUT.callback_data:
        async with state.proxy() as data:
            num_stat = data["st_filter"]
            my_orders = get_all_my_orders(call.from_user.id,
                                          LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data)[0]
            active_order(data["active"])
            await bot.send_message(id_group_log, f"{call.from_user.id} АКТИВУВАВ ЗАЯВКУ №{data['active']}")
            await call.answer("Заявка активована")
            my_orders = get_all_my_orders(call.from_user.id,
                                          LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data)[0]
            if my_orders:
                order_for_print = my_orders[0]
                text = show_all_orders_text(order_for_print[7], order_for_print[0], order_for_print[6],
                                            order_for_print[1],
                                            order_for_print[2], order_for_print[3], order_for_print[4],
                                            order_for_print[5],
                                            order_for_print[8])
            else:
                text = "ЗАЯВОК НЕ МАЄ"
            keyboard = InlineKeyboardMarkup(row_width=2)
            if my_orders and my_orders[0][8] == "pause":
                data["active"] = my_orders[0][0]
                keyboard.add(ACTIVE_ORDER_BUT, ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT,
                             LIST_STATUS_SELLER_BUT[num_stat], ADD_BUT_CANSEL)
            else:
                keyboard.add(my_order_stop)
                keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER, ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT,
                             LIST_STATUS_SELLER_BUT[num_stat], ADD_BUT_CANSEL)
            await bot.edit_message_text(text, call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=keyboard)
    elif call.data == my_order_stop.callback_data:
        async with state.proxy() as data:
            num_stat = data["st_filter"]
            my_orders = get_all_my_orders(call.from_user.id,
                                          LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data)[0]
            order = data["order1"]
            if get_process_order(num=order[0], kind="sell"):
                await call.answer("За цією заявкую є не завершені зустрічні заявки.", show_alert=True)
            else:
                stop_order(order[0])
                await bot.send_message(id_group_log, f"{call.from_user.id} ПРИЗУПИНИВ ЗАЯВКУ №{order[0]}")
                await call.answer("Заявка деактивована")
                my_orders = get_all_my_orders(call.from_user.id,
                                              LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data)[0]
                if my_orders:
                    order_for_print = my_orders[0]
                    text = show_all_orders_text(order_for_print[7], order_for_print[0], order_for_print[6],
                                                order_for_print[1],
                                                order_for_print[2], order_for_print[3], order_for_print[4],
                                                order_for_print[5],
                                                order_for_print[8])
                else:
                    text = "ЗАЯВОК НЕ МАЄ"
                keyboard = InlineKeyboardMarkup(row_width=2)
                if my_orders and my_orders[0][8] == "pause":
                    data["active"] = my_orders[0][0]
                    keyboard.add(ACTIVE_ORDER_BUT).add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT,
                                                       LIST_STATUS_SELLER_BUT[num_stat], ADD_BUT_CANSEL)
                else:
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT,
                                 LIST_STATUS_SELLER_BUT[num_stat], ADD_BUT_CANSEL)
                await bot.edit_message_text(text, call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard)
    # Фільтр на статуси заявки
    elif call.data in [x.callback_data for x in LIST_STATUS_SELLER_BUT]:
        async with state.proxy() as data:
            num_stat = data["st_filter"] + 1
            data["step_my_order"] = 0
            if num_stat > len(LIST_STATUS_SELLER_BUT) - 1:
                num_stat = 0
            data["st_filter"] = num_stat
        if LIST_STATUS_SELLER_BUT[num_stat].callback_data == "sold":
            orders = get_all_my_orders_bought(call.from_user.id)
            sold = [format_approve_order_text(y, orders[1][x]) for x, y in enumerate(orders[0])]
            keyboard = InlineKeyboardMarkup(row_width=2)
            if sold:
                if sold[5] == "process":
                    keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                text = sold[0]
            else:
                text = "ЗАЯВОК НЕ МАЄ"
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT,
                         LIST_STATUS_SELLER_BUT[num_stat], CANSEL_MY_ORDER)
            async with state.proxy() as data:
                data["order1"] = orders[0]
        # Фільтр для фінального статусу підтвердження всих умов - далі арбітраж або завершення
        elif LIST_STATUS_SELLER_BUT[num_stat].callback_data == "finally":
            finally_orders = get_all_my_orders_finally(call.from_user.id)
            orders = [format_approve_order_text(y, finally_orders[1][x]) for x, y in enumerate(finally_orders[0])]
            if orders:
                text = orders[0]
            else:
                text = "ЗАЯВОК НЕ МАЄ"
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_SELLER_BUT[num_stat], CANSEL_MY_ORDER)
            async with state.proxy() as data:
                data["order1"] = finally_orders[0]
        elif LIST_STATUS_SELLER_BUT[num_stat].callback_data == "dispute":
            dispute_order = get_all_my_orders_dispute(call.from_user.id)
            orders = [format_approve_order_text(y, dispute_order[1][x]) for x, y in enumerate(dispute_order[0])]
            if orders:
                text = orders[0]
            else:
                text = "ЗАЯВОК НЕ МАЄ"
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_SELLER_BUT[num_stat], CANSEL_MY_ORDER)
            async with state.proxy() as data:
                data["order1"] = dispute_order[0]
        elif LIST_STATUS_SELLER_BUT[num_stat].callback_data == "done":
            down_orders = get_all_my_orders_sold(call.from_user.id)
            orders = [format_approve_order_text(y, down_orders[1][x]) for x, y in enumerate(down_orders[0])]
            if orders:
                text = orders[0]
            else:
                text = "ЗАЯВОК НЕ МАЄ"
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_SELLER_BUT[num_stat], CANSEL_MY_ORDER)
            async with state.proxy() as data:
                data["order1"] = down_orders[0]
        elif LIST_STATUS_SELLER_BUT[num_stat].callback_data == "ALL":
            keyboard = InlineKeyboardMarkup(row_width=2)
            my_orders = get_all_my_orders(call.from_user.id)[0]
            solds = get_all_my_orders_bought(call.from_user.id)
            finally_order = get_all_my_orders_finally(call.from_user.id)
            done_orders = get_all_my_orders_sold(call.from_user.id)
            orders = solds[0] + finally_order[0] + my_orders + done_orders[0]
            async with state.proxy() as data:
                data["st_filter"] = 0
                data["step_my_order"] = 0
                if orders:
                    order = orders[0]
                    # if len(order) == 10:
                    if order[5] in ("finally", "done", "dispute", "process", "cansel"):
                        if order[5] == "process":
                            keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                        if order[10] == "buy":
                            text = format_approve_order_text(order, get_buyer_orders(order[4], order[1]))
                        else:
                            text = format_approve_order_text(order, solds[1][0])
                    # elif order[5] in ("finally", "done", "dispute", "process", "cansel"):
                    #     text = format_approve_order_text(order, finally_order[1][0])
                    # elif len(order) == 11:
                    elif order[8] == "pause":
                        data["active"] = my_orders[0][0]
                        keyboard.add(ACTIVE_ORDER_BUT)
                        text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3],
                                                    order[4],
                                                    order[5], order[8])
                    elif order[8] == "process" or order[8] == "cansel":
                        if order[8] == "process":
                            if call.from_user.id == order[6]:
                                keyboard.add(my_order_stop)
                                keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER)
                            else:
                                keyboard.add(ADMIN_BUT_CANSEL)

                        text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3],
                                                    order[4],
                                                    order[5], order[8])
                        data["stop_order"] = order
                    else:
                        print(order)
                        data["stop_order"] = order
                    keyboard.add(ARROW_LEFT,
                                 ARROW_RIGHT, STATUS_FILTER_BUT,
                                 LIST_STATUS_SELLER_BUT[data["st_filter"]], CANSEL_MY_ORDER)
                    try:
                        count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                        await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id,
                                                    reply_markup=keyboard)
                    except exceptions.MessageNotModified as ex:
                        print("повідомлення не змінилось")
                        pass
                else:
                    await call.answer("Заявок не має", )
        # Фільтр на всі іншу стадії
        else:
            async with state.proxy() as data:
                my_orders = get_all_my_orders(call.from_user.id, LIST_STATUS_SELLER_BUT[num_stat].callback_data)[0]
                orders = [show_all_orders_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8]) for x in my_orders]
                if orders:
                    text = orders[0]
                else:
                    text = "ЗАЯВОК НЕ МАЄ"
                keyboard = InlineKeyboardMarkup(row_width=2)
                if my_orders and my_orders[0][8] == "pause":
                    data["active"] = my_orders[0][0]
                    keyboard.add(ACTIVE_ORDER_BUT).add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT,
                                                       LIST_STATUS_SELLER_BUT[num_stat], CANSEL_MY_ORDER)
                elif my_orders and my_orders[0][8] == "process":
                    if call.from_user.id == my_orders[0][6]:
                        keyboard.add(my_order_stop)
                        keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER)
                    else:
                        keyboard.add(ADMIN_BUT_CANSEL)
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_SELLER_BUT[num_stat],
                                 CANSEL_MY_ORDER)
                else:
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT,
                                 LIST_STATUS_SELLER_BUT[num_stat], CANSEL_MY_ORDER)

                data["order1"] = my_orders[0] if my_orders else False
        async with state.proxy() as data:
            count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
            if text != "ЗАЯВОК НЕ МАЄ":
                text += count
        await bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    # Підтвердження отримання коштів за заявку, далі переведення ігрової валюти
    elif call.data == APPROVE_ORDER_BUT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
        await bot.edit_message_text(APPROVE_SELLER, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        await FSMMyOrders.approve1.set()
    # Скасування заявки(видалити з вітрини)
    elif call.data == ADMIN_BUT_CANSEL.callback_data:
        my_orders, my_buyers = get_all_my_orders(call.from_user.id)
        async with state.proxy() as data:
            NUM = data["order1"][0]
            if get_process_order(num=NUM, kind="sell"):
                await call.answer("За цією заявкую є не завершені зустрічні заявки.", show_alert=True)
            else:
                update_order_status(NUM, "cansel", "orders")
                await bot.send_message(id_group_log, f"{call.from_user.id}  ВИДАЛИВ ЗАЯВКУ №{NUM}")
                await call.answer("Видалив заявку")
                if LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "ALL":
                    my_orders = get_all_my_orders(call.from_user.id)[0]
                    solds = get_all_my_orders_bought(call.from_user.id)
                    finally_order = get_all_my_orders_finally(call.from_user.id)
                    orders = solds[0] + finally_order[0] + my_orders
                else:
                    stat = LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data
                    orders = get_all_my_orders(call.from_user.id, status=stat)[0]
                step = 0
                data["step_my_order"] = 0
                if not orders:
                    await call.answer("Заявкок не має")
                elif len(orders) == 1:
                    await call.answer("Заявкок не має")
                elif step > len(orders) - 1:
                    step = 0
                    data["step_my_order"] = 0
                    await call.answer("Повернулись на початок")
                if orders:
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    order = orders[step]
                    # Виявляємо тип повідомлення
                    # if len(order) == 10:
                    if order[5] == "process" or order[5] == "cansel":
                        if order[5] == "process":
                            keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                        if order[10] == "buy":
                            text = format_approve_order_text(order, get_buyer_orders(order[4], order[1]))
                        else:
                            text = format_approve_order_text(order, solds[1][0])
                    elif order[5] == "finally":
                        text = format_approve_order_text(order, finally_order[1][0])
                    # elif len(order) == 11:
                    elif order[8] == "pause":
                        data["active"] = my_orders[0][0]
                        keyboard.add(ACTIVE_ORDER_BUT)
                        text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                    order[5], order[8])
                    elif order[8] == "process" or order[8] == "cansel":
                        if order[8] == "process":
                            if call.from_user.id == order[6]:
                                keyboard.add(my_order_stop)
                                keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER)
                            else:
                                keyboard.add(ADMIN_BUT_CANSEL)

                        text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                    order[5], order[8])
                    keyboard.add(ARROW_LEFT,
                                 ARROW_RIGHT, STATUS_FILTER_BUT,
                                 LIST_STATUS_SELLER_BUT[data["st_filter"]], ADD_BUT_CANSEL)
                    try:
                        count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                        await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id,
                                                    reply_markup=keyboard)
                    except exceptions.MessageNotModified as ex:
                        print("повідомлення не змінилось")
                        pass
                else:
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    await bot.edit_message_text("Заявкок не має".upper(), call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard.add(ARROW_LEFT,
                                                                          ARROW_RIGHT, STATUS_FILTER_BUT,
                                                                          LIST_STATUS_SELLER_BUT[data["st_filter"]],
                                                                          ADD_BUT_CANSEL))
    elif call.data == "STATUS_FILTER_BUT":
        await call.answer(help_status, show_alert=True)
    elif call.data == PRIVET_ROOM_BUT.callback_data:
        await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()
    elif call.data == EDIT_ORDER.callback_data:
        async with state.proxy() as data:
            # order = get_all_my_orders(call.from_user.id)[0][data["step_my_order"]]
            order = data["order1"]
            if get_process_order(num=order[0], kind="sell"):
                await call.answer("За цією заявкую є не завершені зустрічні заявки.", show_alert=True)
            else:
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
                                                                                               currency,
                                                                                               data["edit"]))
                await FSMCreate.step1.set()
    elif call.data == ORDER_CANSEL.callback_data:
        try:
            async with state.proxy() as data:
                order = data["fresh_order"]
            keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
            await bot.edit_message_text("ви підтверджуєте скасування зустрічної заявки?".upper(), call.message.chat.id,
                                        call.message.message_id, reply_markup=keyboard)
            await FSMMyOrders.cansel.set()
        except KeyError:
            keyboard = InlineKeyboardMarkup(row_width=2).add(CR_CANSEL)
            await bot.edit_message_text("вкажіть причину скасування зустрічної заявки".upper(),
                                        call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
        await FSMMyOrders.cansel.set()


@dp.message_handler(content_types=['text'], state=FSMMyOrders.cansel)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["reason"] = msg.text
        keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
        await bot.send_message(msg.chat.id, "ви підтверджуєте скасування зустрічної заявки з "
                                            "коментарем:\n".upper()+f"{msg.text}", reply_markup=keyboard)


@dp.callback_query_handler(lambda call: True, state=FSMMyOrders.cansel)
async def back(call: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    async with state.proxy() as data:
        try:
            step = data["step_my_order"]
            point = True
        except KeyError:
            point = False
        data["approve"] = False
        if point:
            if LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "ALL":
                my_orders = get_all_my_orders(call.from_user.id)[0]
                solds = get_all_my_orders_bought(call.from_user.id)
                finally_order = get_all_my_orders_finally(call.from_user.id)
                orders = solds[0] + finally_order[0] + my_orders
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "finally":
                solds = get_all_my_orders_finally(call.from_user.id)
                orders = solds[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "sold":
                my_orders = get_all_my_orders_bought(call.from_user.id)
                orders = my_orders[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "dispute":
                dispute_order = get_all_my_orders_dispute(call.from_user.id)
                orders = dispute_order[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "done":
                done_orders = get_all_my_orders_sold(call.from_user.id)
                orders = done_orders[0]
            else:
                stat = LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data
                orders = get_all_my_orders(call.from_user.id, status=stat)[0]
            if orders:
                order = orders[step]
                if call.data == APPROVE_YES.callback_data:
                    ret = ""
                    if order[10] == "sell":
                        update_balance(order[4], float(order[6]))
                        update_order(order[1], float(order[2]))
                        ret = f"\n{float(order[6])} ГРН. ПОВЕРНУТО НА ВАШ БАЛАНС."
                        try:
                            await bot.send_message(order[4],
                                                   f"ПРОДАВЕЦЬ СКАСУВАВ ЗЯВКУ №{order[0]}, ПРИЧИНА: {data['reason']}\n" + ret)
                        except Exception:
                            pass
                    elif order[10] == "buy":
                        update_status_order_buy(order[1], reserve=-float(order[6]))
                        update_status_order_buy(order[1], part=-float(order[2]))
                    close_process_order(order[0])
                    try:
                        await bot.send_message(id_group_log.id, f"{call.from_user.id} СКАСУВАВ ПЕРЕКАЗ ІГРОВОЇ ВАЛЮТИ "
                                                                f" ПО ЗАЯВЦІ №{order[0]} ПОКУПЦЮ {order[4]}")
                    except Exception:
                        pass
                # keyboard.add(CR_CANSEL)
                # await bot.edit_message_text(F"ЗАЯВКА №{order[0]} СКАСОВАНА, ПРИЧИНА: {data['reason']}",
                #                             call.message.chat.id, call.message.message_id, reply_markup=keyboard)
                # Виявляємо тип повідомлення
                # if len(order) == 10:
                if LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "ALL":
                    my_orders = get_all_my_orders(call.from_user.id)[0]
                    solds = get_all_my_orders_bought(call.from_user.id)
                    finally_order = get_all_my_orders_finally(call.from_user.id)
                    orders = solds[0] + finally_order[0] + my_orders
                elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "finally":
                    solds = get_all_my_orders_finally(call.from_user.id)
                    orders = solds[0]
                elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "sold":
                    my_orders = get_all_my_orders_bought(call.from_user.id)
                    orders = my_orders[0]
                elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "dispute":
                    dispute_order = get_all_my_orders_dispute(call.from_user.id)
                    orders = dispute_order[0]
                elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "done":
                    done_orders = get_all_my_orders_sold(call.from_user.id)
                    orders = done_orders[0]
                else:
                    stat = LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data
                    orders = get_all_my_orders(call.from_user.id, status=stat)[0]
                order = orders[step]
                if order[5] == "process" or order[5] == "cansel":
                    if order[5] == "process":
                        keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                    elif order[10] == "buy":
                        text = format_approve_order_text(order, get_buyer_orders(order[4], order[1]))
                    else:
                        text = format_approve_order_text(order, solds[1][0])
                elif order[5] == "finally":
                    text = format_approve_order_text(order, finally_order[1][0])
                elif order[5] == "done" or order[5] == "SOLD":
                    text = format_approve_order_text(order, done_orders[1][0])
                elif order[5] == "dispute":
                    text = format_approve_order_text(order, dispute_order[1][0])
                # elif len(order) == 11:
                elif order[8] == "pause":
                    keyboard.add(ACTIVE_ORDER_BUT)
                    data["active"] = order[0]
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                    data["stop_order"] = order
                elif order[8] == "process" or order[8] == "cansel":
                    if order[8] == "process":
                        if call.from_user.id == order[6]:
                            keyboard.add(my_order_stop)
                            keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER)
                        else:
                            keyboard.add(ADMIN_BUT_CANSEL)
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                    data["stop_order"] = order
                keyboard.add(ARROW_LEFT,
                             ARROW_RIGHT, STATUS_FILTER_BUT,
                             LIST_STATUS_SELLER_BUT[data["st_filter"]], CANSEL_MY_ORDER)
                try:
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                    await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                except exceptions.MessageNotModified as ex:
                    print("повідомлення не змінилось")
                    pass
        else:
            order = data["fresh_order"][0]
            if call.data == APPROVE_YES.callback_data:
                if order[10] == "sell":
                    update_balance(order[4], float(order[6]))
                    update_order(order[1], float(order[2]))
                    ret = f"\n{float(order[6])} ГРН. ПОВЕРНУТО НА ВАШ БАЛАНС."
                    try:
                        await bot.send_message(order[4],
                                               f"ПРОДАВЕЦЬ СКАСУВАВ ЗЯВКУ №{order[0]}, ПРИЧИНА: {data['reason']}\n" + ret)
                    except Exception:
                        pass
                elif order[10] == "buy":
                    update_status_order_buy(order[1], reserve=-float(order[6]))
                    update_status_order_buy(order[1], part=-float(order[2]))
                close_process_order(order[0])
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(CANSEL_LS)
                await bot.edit_message_text(f"скасував заявку: №{order[0]}".upper(), call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                await bot.edit_message_text(f"ПЕРЕКАЖІТЬ: {order[2]} {order[10]}\n\n"
                                            f"ПОКЕР-РУМ: {order[1]}\n"
                                            f"E-MAIL/LOGIN: {order[9]}\n\n"
                                            f"ПРОТЯГОМ {order[4]} XB.\n\n"
                                            f"КРАЙНІЙ СРОК: {data['fresh_order_time']}", call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard)
    await FSMMyOrders.step1.set()


@dp.callback_query_handler(lambda call: True, state=FSMMyOrders.balance)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data in [x.callback_data for x in LIST_STATUS_BALANCE]:
        async with state.proxy() as data:
            orders = []
            num_stat = data["st_filter"] + 1
            data["step"] = 0
            if num_stat > len(LIST_STATUS_BALANCE) - 1:
                num_stat = 0
            data["st_filter"] = num_stat
            add_orders, down_orders = get_balance_orders(call.from_user.id)
            print(LIST_STATUS_BALANCE[num_stat].callback_data)
            if LIST_STATUS_BALANCE[num_stat].callback_data == "ALL":
                orders = add_orders + down_orders
            elif LIST_STATUS_BALANCE[num_stat].callback_data == "add":
                orders = add_orders
            elif LIST_STATUS_BALANCE[num_stat].callback_data == "down":
                orders = down_orders
        if orders:
            keyboard = InlineKeyboardMarkup(row_width=2)
            if len(orders) > 1:
                keyboard.add(ARROW_LEFT, ARROW_RIGHT)
            keyboard.add(STATUS_FILTER_BUT, LIST_STATUS_BALANCE[data["st_filter"]],
                         ADD_BUT_CANSEL)
            count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders)}"
            await bot.edit_message_text(text_balance(orders[data["step"]]) + count, call.message.chat.id,
                                        call.message.message_id, reply_markup=keyboard)
        else:
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(STATUS_FILTER_BUT, LIST_STATUS_BALANCE[data["st_filter"]],
                         ADD_BUT_CANSEL)
            await bot.edit_message_text("Заявок не має".upper(), call.message.chat.id,
                                        call.message.message_id, reply_markup=keyboard)
    elif call.data == ARROW_LEFT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        async with state.proxy() as data:
            step = data["step"] - 1
            num_stat = data["st_filter"]
            add_orders, down_orders = get_balance_orders(call.from_user.id)
            if LIST_STATUS_SELLER_BUT[num_stat].callback_data == "ALL":
                orders = add_orders + down_orders
            elif LIST_STATUS_SELLER_BUT[num_stat].callback_data == "add":
                orders = add_orders
            elif LIST_STATUS_SELLER_BUT[num_stat].callback_data == "down":
                orders = down_orders
            if not orders:
                await call.answer("Заявкок не має")
            elif step <= -1:
                await call.answer("Це перша заявка")
                data["step_my_order"] = 0
            elif orders:
                data["step"] = step
                keyboard = InlineKeyboardMarkup(row_width=2)
                if len(orders) > 1:
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT)
                keyboard.add(STATUS_FILTER_BUT, LIST_STATUS_BALANCE[data["st_filter"]],
                             ADD_BUT_CANSEL)
                count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders)}"
                await bot.edit_message_text(text_balance(orders[data["step"]]) + count, call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard)

    elif call.data == ARROW_RIGHT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        async with state.proxy() as data:
            step = data["step"] + 1
            num_stat = data["st_filter"]
            add_orders, down_orders = get_balance_orders(call.from_user.id)
            if LIST_STATUS_SELLER_BUT[num_stat].callback_data == "ALL":
                orders = add_orders + down_orders
            elif LIST_STATUS_SELLER_BUT[num_stat].callback_data == "add":
                orders = add_orders
            elif LIST_STATUS_SELLER_BUT[num_stat].callback_data == "down":
                orders = down_orders
            if not orders:
                await call.answer("Заявкок не має")
            elif len(orders) == 1:
                await call.answer("Це єдина заявка")
                data["step"] = 0
            elif step > len(orders) - 1:
                data["step"] = 0
                await call.answer("Повернулись на початок")
            else:
                data["step"] = step
                keyboard = InlineKeyboardMarkup(row_width=2)
                if len(orders) > 1:
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT)
                keyboard.add(STATUS_FILTER_BUT, LIST_STATUS_BALANCE[data["st_filter"]],
                             ADD_BUT_CANSEL)
                count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders)}"
                await bot.edit_message_text(text_balance(orders[data["step"]]) + count, call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard)

    elif call.data == "STATUS_FILTER_BUT":
        await call.answer(help_status, show_alert=True)
    elif call.data == ADD_BUT_CANSEL.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SELLER_BUT, BUYER_BUT, ADD_BUT_CANSEL, MY_BALANCE)
        await bot.edit_message_text("ВИБЕРІТЬ ЯКІ ЗАЯВКИ ВИВЕСТИ:", call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=keyboard)
        await FSMMyOrders.step1.set()


@dp.callback_query_handler(lambda call: True, state=FSMMyOrders.approve1)
async def back(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        try:
            step = data["step_my_order"]
            point = True
        except KeyError:
            point = False
        data["approve"] = False
    if call.data == APPROVE_YES.callback_data:
        my_orders = get_all_my_orders_bought(call.from_user.id)
        async with state.proxy() as data:
            data["approve"] = True
            try:
                order = data["fresh_order"][0]
                sell_order = data["sell_order"]
                point = False
            except KeyError:
                order = my_orders[0][step]
                sell_order = my_orders[1][step]
        try:
            if check_status_order(order[0]) == "process":
                # update_balance(my_orders[0][step][7], float(my_orders[0][step][6]))
                time = datetime.now() + timedelta(minutes=sell_order[5])
                time = time.strftime("%d.%m.%Y, %H:%M")
                time_answer = datetime.now() - (datetime.strptime(order[3], "%d.%m.%Y, %H:%M") -
                                                timedelta(minutes=sell_order[5]))
                time_answer = int(time_answer.seconds)
                average_time(call.from_user.id, "process", time_answer)
                update_status_finally(order[0], time)
                text = f"ЗА ВАШОЮ ЗУСТРІЧНОЮ ЗАЯВКОЮ №{order[0]} ЗРОБИЛИ ПЕРЕКАЗ\n\n" \
                       f"ПЕРЕВІРТЕ ОТРИМАННЯ ТА ОБОВ'ЯЗКОВО ПІДТВЕРДІТЬ ЗАЯВКУ ПРОТЯГОМ {sell_order[5]} ХВ.\n\n" \
                       f"ЩОБ ЇЇ ПЕРЕГЛЯНУТИ ПЕРЕЙДІТЬ В ОСОБИСТИЙ КАБІНЕТ -> МОЇ ЗАЯВКИ -> ЯК ПОКУПЕЦЬ\n" .upper()
                await bot.send_message(id_group_log, f"{call.from_user.id} ПІДТВЕРДИВ ПЕРЕКАЗ ІГРОВОЇ ВАЛЮТИ "
                                                     f"{order[2]} {sell_order[10]} ПО ЗАЯВЦІ №{order[0]} "
                                                     f"ПОКУПЦЮ {order[4]}")
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(PRIVET_ROOM_BUT)
                await bot.send_message(order[4], text,)

            else:
                pass
                #await bot.send_message(call.from_user.id, "Статус цієї заявки змінився, перевірте її актуальність".upper())
        except Exception as ex:
            print(ex)
    if point:
        keyboard = InlineKeyboardMarkup(row_width=2)
        async with state.proxy() as data:
            step = data["step_my_order"]
            if LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "ALL":
                my_orders = get_all_my_orders(call.from_user.id)[0]
                solds = get_all_my_orders_bought(call.from_user.id)
                finally_order = get_all_my_orders_finally(call.from_user.id)
                orders = solds[0] + finally_order[0] + my_orders
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "finally":
                solds = get_all_my_orders_finally(call.from_user.id)
                orders = solds[0]
            elif LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data == "sold":
                my_orders = get_all_my_orders_bought(call.from_user.id)
                orders = my_orders[0]
            else:
                stat = LIST_STATUS_SELLER_BUT[data["st_filter"]].callback_data
                orders = get_all_my_orders(call.from_user.id, status=stat)[0]
            if orders:
                order = orders[step]
                # Виявляємо тип повідомлення
                # if len(order) == 10:
                if order[5] == "process" or order[5] == "cansel":
                    if order[5] == "process":
                        keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
                    if order[10] == "sell":
                        text = format_approve_order_text(order, solds[1][0])
                    elif order[10] == "buy":
                        text = format_approve_order_text(order, get_buyer_orders(order[4], order[1]))
                elif order[5] == "finally":
                    text = format_approve_order_text(order, finally_order[1][0])
                # elif len(order) == 11:
                elif order[8] == "pause":
                    data["active"] = my_orders[0][0]
                    keyboard.add(ACTIVE_ORDER_BUT)
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                elif order[8] == "process" or order[8] == "cansel":
                    if order[8] == "process":
                        if call.from_user.id == order[6]:
                            keyboard.add(my_order_stop)
                            keyboard.add(ADMIN_BUT_CANSEL, EDIT_ORDER)
                        else:
                            keyboard.add(ADMIN_BUT_CANSEL)
                    text = show_all_orders_text(order[7], order[0], order[6], order[1], order[2], order[3], order[4],
                                                order[5], order[8])
                keyboard.add(ARROW_LEFT,
                             ARROW_RIGHT, STATUS_FILTER_BUT,
                             LIST_STATUS_SELLER_BUT[data["st_filter"]], ADD_BUT_CANSEL)
                try:
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                    await bot.edit_message_text(text + count, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                except exceptions.MessageNotModified as ex:
                    print("повідомлення не змінилось")
                    pass
        await FSMMyOrders.step1.set()
    else:
        if data["approve"]:
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(CANSEL_LS)
            await bot.edit_message_text("Заявка відправлена продавцю, очікуйте підтвердження.".upper(),
                                        call.message.chat.id, call.message.message_id, reply_markup=keyboard)

        else:
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(ORDER_CANSEL, APPROVE_ORDER_BUT)
            order = data["fresh_order"][0]
            await bot.edit_message_text(f"ПЕРЕКАЖІТЬ: {order[2]} {order[10]}\n\n"
                                        f"ПОКЕР-РУМ: {order[1]}\n"
                                        f"E-MAIL/LOGIN: {order[9]}\n\n"
                                        f"ПРОТЯГОМ {order[4]} XB.\n\n"
                                        f"КРАЙНІЙ СРОК: {data['fresh_order_time']}", call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=keyboard)
        await FSMMyOrders.step1.set()


@dp.callback_query_handler(lambda call: True, state=FSMMyOrders.bayer)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ARROW_LEFT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        async with state.proxy() as data:
            step = data["step_my_order"] - 1
            data["step_my_order"] = step
            if LIST_STATUS_BAYER[data["st_filter"]].callback_data == "ALL":
                my_orders, my_buyers = get_all_my_orders(call.from_user.id)
                orders = [show_buyer_text(x) for x in my_buyers]
                my_orders_buy = get_buyer_orders(call.from_user.id)
                orders_buy = [show_order_buyer_text(x) for x in my_orders_buy]
                orders += orders_buy
                my_buyers += my_orders_buy
            elif LIST_STATUS_BAYER[data["st_filter"]].callback_data == "buy_order":
                my_orders_buy = get_buyer_orders(call.from_user.id)
                orders_buy = [show_order_buyer_text(x) for x in my_orders_buy]
                orders = orders_buy
                my_buyers = my_orders_buy
            else:
                status = LIST_STATUS_BAYER[data["st_filter"]].callback_data
                my_buyers = [x for x in get_order_by_status(status, call.from_user.id)]
                orders = [show_buyer_text(x) for x in my_buyers]
            if not orders:
                await call.answer("Заявкок не має")
            elif step <= -1:
                await call.answer("Це перша заявка")
                step = 0
                data["step_my_order"] = 0
            if orders:
                order = orders[step]
                if my_buyers[step][5] == "finally":
                    keyboard.add(APPROVE_ORDER_BUT)
                elif len(my_buyers[step]) == 12 and my_buyers[step][8] == "process":
                    data["NUM_order"] = my_buyers[step][0]
                    data["order"] = order
                    data["len_orders"] = len(orders)
                    keyboard.add(ORDER_CANSEL, EDIT_ORDER)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                             ADD_BUT_CANSEL)
                try:
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                    await bot.edit_message_text(order + count, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                except exceptions.MessageNotModified as ex:
                    print("повідомлення не змінилось")
                    pass
    elif call.data == STATUS_FILTER_BUT.callback_data:
        await call.answer(help_status, show_alert=True)
    elif call.data == ARROW_RIGHT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2)
        async with state.proxy() as data:
            step = data["step_my_order"] + 1
            data["step_my_order"] = step
            if LIST_STATUS_BAYER[data["st_filter"]].callback_data == "ALL":
                my_orders, my_buyers = get_all_my_orders(call.from_user.id)
                orders = [show_buyer_text(x) for x in my_buyers]
                my_orders_buy = get_buyer_orders(call.from_user.id)
                orders_buy = [show_order_buyer_text(x) for x in my_orders_buy]
                orders += orders_buy
                my_buyers += my_orders_buy
            elif LIST_STATUS_BAYER[data["st_filter"]].callback_data == "buy_order":
                my_orders_buy = get_buyer_orders(call.from_user.id)
                orders_buy = [show_order_buyer_text(x) for x in my_orders_buy]
                orders = orders_buy
                my_buyers = my_orders_buy
            else:
                status = LIST_STATUS_BAYER[data["st_filter"]].callback_data
                my_buyers = [x for x in get_order_by_status(status, call.from_user.id)]
                orders = [show_buyer_text(x) for x in my_buyers]
            if not orders:
                await call.answer("Заявкок не має")
            elif len(orders) == 1:
                await call.answer("Це єдина заявка")
                step = 0
                data["step_my_order"] = 0
            elif step > len(orders) - 1:
                step = 0
                data["step_my_order"] = 0
                await call.answer("Повернулись на початок")
            if orders:
                order = orders[step]
                # Виявляємо тип повідомлення
                if my_buyers[step][5] == "finally":
                    keyboard.add(APPROVE_ORDER_BUT)
                elif len(my_buyers[step]) == 12 and my_buyers[step][8] == "process":
                    data["NUM_order"] = my_buyers[step][0]
                    data["order"] = order
                    data["len_orders"] = len(orders)
                    keyboard.add(ORDER_CANSEL, EDIT_ORDER)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                             ADD_BUT_CANSEL)
                try:
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                    await bot.edit_message_text(order + count, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                except exceptions.MessageNotModified as ex:
                    print("повідомлення не змінилось")
                    pass
    elif call.data == APPROVE_ORDER_BUT.callback_data:
        keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
        await bot.edit_message_text(APPROVE_TEXT, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        await FSMMyOrders.approve2.set()
    elif call.data == "ADD_BUT_CANSEL":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(SELLER_BUT, BUYER_BUT, ADD_BUT_CANSEL, MY_BALANCE)
        await bot.edit_message_text("ВИБЕРІТЬ ЯКІ ЗАЯВКИ ВИВЕСТИ:", call.message.chat.id,
                                    call.message.message_id,
                                    reply_markup=keyboard)
        await FSMMyOrders.step1.set()
    elif call.data in [x.callback_data for x in LIST_STATUS_BAYER]:
        async with state.proxy() as data:
            num_stat = data["st_filter"] + 1
            data["step_my_order"] = 0
            if num_stat > len(LIST_STATUS_BAYER) - 1:
                num_stat = 0
            data["st_filter"] = num_stat

        if LIST_STATUS_BAYER[data["st_filter"]].callback_data == "ALL":
            my_orders, my_buyers = get_all_my_orders(call.from_user.id)
            orders = [show_buyer_text(x) for x in my_buyers]
            my_orders_buy = get_buyer_orders(call.from_user.id)
            orders_buy = [show_order_buyer_text(x) for x in my_orders_buy]
            orders += orders_buy
            my_buyers += my_orders_buy
            if my_buyers:
                async with state.proxy() as data:
                    data["step_my_order"] = 0
                    data["order"] = orders[0]
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    if my_buyers[0][5] == "finally":
                        keyboard.add(APPROVE_ORDER_BUT)
                    elif len(my_buyers[0]) == 12 and my_buyers[0][8] == "process":
                        data["NUM_order"] = my_buyers[0][0]
                        data["len_orders"] = len(orders)
                        keyboard.add(ORDER_CANSEL, EDIT_ORDER)
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                                 ADD_BUT_CANSEL)
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                await bot.edit_message_text(orders[0] + count, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                             ADD_BUT_CANSEL)
                await bot.edit_message_text("ЗАЯВОК НЕ МАЄ", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)

        elif LIST_STATUS_BAYER[data["st_filter"]].callback_data == "buy_order":
            my_orders_buy = get_buyer_orders(call.from_user.id)
            orders_buy = [show_order_buyer_text(x) for x in my_orders_buy]
            orders = orders_buy
            my_buyers = my_orders_buy
            if my_buyers:
                async with state.proxy() as data:
                    data["step_my_order"] = 0
                    data["order"] = orders[0]
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    data["NUM_order"] = my_buyers[0][0]
                    data["len_orders"] = len(orders)
                    keyboard.add(ORDER_CANSEL, EDIT_ORDER)
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                                 ADD_BUT_CANSEL)
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                await bot.edit_message_text(orders[0] + count, call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                             ADD_BUT_CANSEL)
                await bot.edit_message_text("ЗАЯВОК НЕ МАЄ", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
        else:
            status = LIST_STATUS_BAYER[data["st_filter"]].callback_data
            orders = [x for x in get_order_by_status(status, call.from_user.id)]
            if orders:
                async with state.proxy() as data:
                    data["step_my_order"] = 0
                    data["order"] = show_buyer_text(orders[0])
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    if orders[0][5] == "finally":
                        keyboard.add(APPROVE_ORDER_BUT)
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                                 ADD_BUT_CANSEL)
                    count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
                await bot.edit_message_text(data["order"] + count, call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                             ADD_BUT_CANSEL)
                await bot.edit_message_text("ЗАЯВОК НЕ МАЄ", call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
    elif call.data == ORDER_CANSEL.callback_data:
        async with state.proxy() as data:
            NUM = data["NUM_order"]
        if get_process_order(num=NUM, kind="buy"):
            await call.answer("За цією заявкую є не завершені зустрічні заявки.", show_alert=True)
        else:
            keyboard = InlineKeyboardMarkup(row_width=2).add(APPROVE_NO, APPROVE_YES)
            await bot.edit_message_text(f"ви підтверджуєте видалення заявки №{NUM}?".upper(), call.message.chat.id,
                                        call.message.message_id, reply_markup=keyboard)
    elif call.data == APPROVE_YES.callback_data:
        async with state.proxy() as data:
            order_text = data["order"].replace("РОЗМІЩЕННА", "ВИДАЛЕНА")
            NUM = data["NUM_order"]
            count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {data['len_orders']}"
        update_status_order_buy(NUM)
        order = get_buyer_orders(call.from_user.id, NUM)
        update_balance(call.from_user.id, order[11])
        await call.answer(f"Видалив заявку №{NUM}")
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                     ADD_BUT_CANSEL)
        await bot.edit_message_text(order_text + count, call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard)
    elif call.data == APPROVE_NO.callback_data or call.data == CR_CANSEL.callback_data:
        async with state.proxy() as data:
            my_orders_buy = get_buyer_orders(call.from_user.id, data["NUM_order"])
            orders_buy = show_order_buyer_text(my_orders_buy)
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(ORDER_CANSEL, EDIT_ORDER)
            keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                         ADD_BUT_CANSEL)
            count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {data['len_orders']}"
            await bot.edit_message_text(orders_buy+count, call.message.chat.id,
                                        call.message.message_id, reply_markup=keyboard)
    elif call.data == EDIT_ORDER.callback_data:
        async with state.proxy() as data:
            order = get_buyer_orders(call.from_user.id, data["NUM_order"])
            if get_process_order(num=order[0], kind="buy"):
                await call.answer("За цією заявкую є не завершені зустрічні заявки.", show_alert=True)
            else:
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
                await bot.edit_message_text(CREATE_BUYER_TEXT1(order[2], order[3]), call.message.chat.id,
                                            call.message.message_id, reply_markup=CREATE_BUTTS(order[2],
                                                                                               order[3],
                                                                                               order[4],
                                                                                               order[5],
                                                                                               room,
                                                                                               order[9],
                                                                                               currency,
                                                                                               data["edit"],
                                                                                               kind="buy"))
                await FSMCreateBuyer.step1.set()


@dp.callback_query_handler(lambda call: True, state=FSMMyOrders.approve2)
async def back(call: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    async with state.proxy() as data:
        step = data["step_my_order"]
        filter_order = data["st_filter"]
    if call.data == APPROVE_YES.callback_data:
        my_buyers = get_all_my_orders(call.from_user.id)[1]
        try:
            order = my_buyers[step]
            if check_status_order(order[0]) == "finally":
                update_status_done(order[0])
                id_seller = order[7]
                new_money = order[6]
                if order[10] == "sell":
                    first_order = get_order_by_id(order[1])
                else:
                    first_order = get_buyer_orders(order[4], order[1])
                time_answer = datetime.now() - (datetime.strptime(my_buyers[step][3], "%d.%m.%Y, %H:%M") -
                                                timedelta(minutes=first_order[5]))
                time_answer = int(time_answer.seconds)
                average_time(call.from_user.id, "finally", time_answer)
                update_balance(id_seller, new_money)
                await bot.send_message(id_seller, f"ЗУСТРІЧНУ заявку №{order[0]} успішно завершенно\nБаланс поповненно на "
                                                  f"{new_money} ГРН".upper())
                await bot.send_message(id_group_log, f"{call.from_user.id} ПІДТВЕРДИВ ОТРИМАННЯ ІГРОВОЇ ВАЛЮТИ "
                                                     f"ПО ЗАЯВЦІ №{order[0]} ВІД ПРОДАВЦЯ {order[7]}")
                await call.answer("Готово")
                log_write(call.from_user.id, f"ПІДТВЕРДИВ ОТРИМАННЯ КОШТІВ ПО ЗАЯВЦІ {my_buyers[step][1]}")
            elif check_status_order(my_buyers[step][0]) == "dispute":
                pass
                #await bot.send_message(call.from_user.id, "Статус цієї заявки: Арбітраж".upper())
        except Exception as ex:
            pass
    my_buyers = get_all_my_orders(call.from_user.id)[1]
    orders = [show_buyer_text(x) for x in my_buyers]
    if orders:
        order = orders[step]
        if my_buyers[step][5] == "finally":
            keyboard.add(APPROVE_ORDER_BUT)
        keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[filter_order], ADD_BUT_CANSEL)
        try:
            await bot.edit_message_text(order, call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
        except exceptions.MessageNotModified as ex:
            print("повідомлення не змінилось")
            pass
    await FSMMyOrders.bayer.set()
