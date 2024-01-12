import asyncio
import profile

from aiogram.utils import executor
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup

from add_or_withdraw import *
import my_orders
from CREATE_ORDER import *
from admin import *
from database import check_register, add_new_user, admins
from aiogram import Bot, types
from pertner_balance import *
from all_orders import *
import loop_check
import FAQ
from CREATE_BUYER import *
from rate import rate


@dp.message_handler(commands=['start'], state="*")
async def send_welcome(msg: types.Message, state: FSMContext):
    ref = msg.text.split(" ")
    if len(ref) >= 2:
        user = ref[1].split("_")[1]
        async with state.proxy() as data:
            data["referal"] = user
        # if check_register(user) and msg.from_user.id != int(user):
        #     if check_referral(user, msg.from_user.id):
        #         try:
        #             await bot.send_message(user, f"за вашим реферальним посиланням приєднався новий користувач:"
        #                                          f" {msg.from_user.full_name}".upper())
        #         except Exception:
        #             pass

    if msg.from_user.id in admins():
        if check_register(msg.from_user.id):
            async with state.proxy() as data:
                data["kind_number"] = 0
            orders0 = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                       get_all_orders()]
            my_orders_buy = get_buyer_orders(all_order=True)
            orders2 = [show_order_buyer_text(x, "show") for x in my_orders_buy]
            orders = orders0 + orders2
            if orders:
                async with state.proxy() as data:
                    data["step"] = 0
                    data["id_order"] = get_all_orders()[0] if get_all_orders() else my_orders_buy[0]
                    data["order"] = orders[0]
                    data["kind"] = "sell" if get_all_orders() else "buy"
                    keyboard = InlineKeyboardMarkup(row_width=2)
                    if msg.from_user.id in admins():
                        keyboard.insert(ADMIN_BUT_CANSEL)
                    count = ""
                    if orders0:
                        keyboard.add(BUY_lower, SELL)
                        count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders0)}"
                    elif orders2:
                        keyboard.add(BUY, SELL_lower)
                        count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders2)}"
                    keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER,
                                 LIST_POKER_ROOMS_BUT2[data["kind_number"]], CANSEL_LS, GET_ORDER)
                    with open("FAQ.jpg", "rb") as photo:
                        chat = await bot.get_chat(msg.chat.id)
                        if chat.pinned_message:
                            pass
                            # await bot.unpin_chat_message(chat_id=msg.chat.id)
                        else:
                            keyboard2 = InlineKeyboardMarkup(row_width=2).add(
                                InlineKeyboardButton(text="ІНСТРУКЦІЯ".upper(), url=link_but))
                            sent_message = await bot.send_photo(chat_id=msg.chat.id, photo=photo,
                                                                reply_markup=keyboard2, parse_mode='HTML')
                            await bot.pin_chat_message(chat_id=msg.chat.id, message_id=sent_message.message_id,)
                await bot.send_message(msg.chat.id, orders[0] + count, reply_markup=keyboard)
                await FSMAllOrders.step1.set()
            else:
                keyboard = InlineKeyboardMarkup(row_width=2).add(CANSEL_LS)
                await bot.send_message(msg.chat.id, "ЗАЯВОК НЕМАЄ", reply_markup=keyboard)
                await FSMAllOrders.step1.set()
        else:
            await msg.answer(START_MESS(msg.from_user.full_name))
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Відправити номер телефону", request_contact=True))
            await msg.answer("Для продовження потрібно поділитись номером телефону".upper(), reply_markup=keyboard)
            await FSMPhone.add_phone.set()
    else:
        if not check_ban(msg.from_user.id):
            if switch_check():

                if check_register(msg.from_user.id):
                    # await msg.answer(LS_TEXT(msg.from_user.id), reply_markup=LS_BUTTONS(msg.from_user.id))
                    # await FSMDistributor.where.set()
                    async with state.proxy() as data:
                        data["kind_number"] = 0
                    orders0 = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                              get_all_orders()]
                    my_orders_buy = get_buyer_orders(all_order=True)
                    orders2 = [show_order_buyer_text(x, "show") for x in my_orders_buy]
                    orders = orders0 + orders2
                    if orders:
                        async with state.proxy() as data:
                            data["step"] = 0
                            data["id_order"] = get_all_orders()[0] if get_all_orders() else my_orders_buy[0]
                            data["order"] = orders[0]
                            data["kind"] = "sell" if get_all_orders() else "buy"
                            keyboard = InlineKeyboardMarkup(row_width=2)
                            if msg.from_user.id in admins():
                                keyboard.insert(ADMIN_BUT_CANSEL)
                            count = f""
                            if orders0:
                                keyboard.add(BUY_lower, SELL)
                                count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders0)}"
                            elif orders2:
                                keyboard.add(BUY, SELL_lower)
                                count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders2)}"
                            keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER,
                                         LIST_POKER_ROOMS_BUT2[data["kind_number"]], CANSEL_LS, GET_ORDER)
                        with open("FAQ.jpg", "rb") as photo:
                            chat = await bot.get_chat(msg.chat.id)
                            if chat.pinned_message:
                                # pass
                                await bot.unpin_chat_message(chat_id=msg.chat.id)
                            # else:
                            #     keyboard2 = InlineKeyboardMarkup(row_width=2).add(
                            #         InlineKeyboardButton(text="ІНСТРУКЦІЯ".upper(), url=link_but))
                            #     sent_message = await bot.send_photo(chat_id=msg.chat.id, photo=photo,
                            #                                         reply_markup=keyboard2, parse_mode='HTML')
                            #     await bot.pin_chat_message(chat_id=msg.chat.id, message_id=sent_message.message_id)

                        await bot.send_message(msg.chat.id, orders[0]+count, reply_markup=keyboard)
                        await FSMAllOrders.step1.set()
                    else:
                        keyboard = InlineKeyboardMarkup(row_width=3).add(CANSEL_LS)
                        await bot.send_message(msg.chat.id, "ЗАЯВОК НЕМАЄ", reply_markup=keyboard)
                        await FSMAllOrders.step1.set()
                else:
                    await msg.answer(START_MESS(msg.from_user.full_name))
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                    keyboard.add(types.KeyboardButton(text="Відправити номер телефону", request_contact=True))
                    await msg.answer("Для продовження потрібно поділитись номером телефону".upper(), reply_markup=keyboard)
                    await FSMPhone.add_phone.set()
            else:
                await msg.answer(bot_off())
        else:
            await msg.answer("БАН")


@dp.message_handler(commands=['account'], state="*")
async def send_welcome(msg: types.Message, state: FSMContext):
    ref = msg.text.split(" ")
    if len(ref) >= 2:
        user = ref[1].split("_")[1]
        async with state.proxy() as data:
            data["referal"] = user
        # if check_register(user) and msg.from_user.id != int(user):
        #     if check_referral(user, msg.from_user.id):
        #         try:
        #             await bot.send_message(user, f"за вашим реферальним посиланням приєднався новий користувач:"
        #                                          f" {msg.from_user.full_name}".upper())
        #         except Exception:
        #             pass

    if msg.from_user.id in admins():
        if check_register(msg.from_user.id):
            await msg.answer(LS_TEXT(msg.from_user.id), reply_markup=LS_BUTTONS(msg.from_user.id))
            await FSMDistributor.where.set()
        else:
            await msg.answer(START_MESS(msg.from_user.full_name))
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            keyboard.add(types.KeyboardButton(text="Відправити номер телефону", request_contact=True))
            await msg.answer("Для продовження потрібно поділитись номером телефону".upper(), reply_markup=keyboard)
            await FSMPhone.add_phone.set()
    else:
        if not check_ban(msg.from_user.id):
            if switch_check():
                if check_register(msg.from_user.id):
                    await msg.answer(LS_TEXT(msg.from_user.id), reply_markup=LS_BUTTONS(msg.from_user.id))
                    await FSMDistributor.where.set()
                else:
                    await msg.answer(START_MESS(msg.from_user.full_name))
                    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                    keyboard.add(types.KeyboardButton(text="Відправити номер телефону", request_contact=True))
                    await msg.answer("Для продовження потрібно поділитись номером телефону".upper(),
                                     reply_markup=keyboard)
                    await FSMPhone.add_phone.set()
            else:
                await msg.answer(bot_off())
        else:
            await msg.answer("БАН")


@dp.message_handler(commands=['about'], state="*")
async def send_welcome(msg: types.Message, state: FSMContext):
    if switch_check():
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(FAQ_BUT, CHAT_BUT, ADMIN_CHAT_BUT, ADD_BUT_CANSEL)
        await bot.send_message(msg.chat.id, FAQ_text(), reply_markup=keyboard)
        await FSMFaq.step1.set()

    else:
        await msg.answer(bot_off())


@dp.message_handler(commands=['seller'], state="*")
async def send_welcome(call: types.Message, state: FSMContext):
    if switch_check():
        keyboard = InlineKeyboardMarkup(row_width=2)
        my_orders = get_all_my_orders(call.from_user.id)[0]
        solds = get_all_my_orders_bought(call.from_user.id)
        finally_order = get_all_my_orders_finally(call.from_user.id)
        orders = solds[0] + finally_order[0] + my_orders
        async with state.proxy() as data:
            data["st_filter"] = 0
            data["step_my_order"] = 0
            if orders:
                # text = "Упс... щось не так"
                order = orders[0]
                if len(order) == 10:
                    if order[5] == "process":
                        keyboard.add(APPROVE_ORDER_BUT)
                        text = format_approve_order_text(order, solds[1][0])
                    elif order[5] == "finally":
                        text = format_approve_order_text(order, finally_order[1][0])
                elif len(order) == 11:
                    if order[8] == "pause":
                        data["active"] = my_orders[0][0]
                        keyboard.add(ACTIVE_ORDER_BUT)
                    elif order[8] == "process":
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
                    await bot.send_message(call.chat.id, text + count, reply_markup=keyboard)
                except Exception:
                    pass
            else:
                await call.answer("Заявок не має", )
        await FSMMyOrders.step1.set()
    else:
        await call.answer(bot_off())


@dp.message_handler(commands=['buyer'], state="*")
async def send_welcome(call: types.Message, state: FSMContext):
    if switch_check():
        my_orders, my_buyers = get_all_my_orders(call.from_user.id)
        orders = [show_buyer_text(x) for x in my_buyers]
        if my_buyers:
            async with state.proxy() as data:
                data["st_filter"] = 0
                data["step_my_order"] = 0
                data["order"] = orders[0]
                keyboard = InlineKeyboardMarkup(row_width=2)
                if my_buyers[0][5] == "finally":
                    keyboard.add(APPROVE_ORDER_BUT)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT, STATUS_FILTER_BUT, LIST_STATUS_BAYER[data["st_filter"]],
                             ADD_BUT_CANSEL)
                count = f"\nПОКАЗАНА {data['step_my_order'] + 1} З {len(orders)}"
            await bot.send_message(call.chat.id, orders[0] + count, reply_markup=keyboard)
            await FSMMyOrders.bayer.set()
        else:
            await call.answer("Заявок не має")
            await FSMMyOrders.step1.set()
    else:
        await call.answer(bot_off())


@dp.message_handler(commands=['profile'], state="*")
async def send_welcome(msg: types.Message, state: FSMContext):
    if switch_check():
        await bot.send_message(msg.chat.id, text_profile(msg.from_user.id), reply_markup=profile_buttons(msg.from_user.id))
        await FSMProfile.where.set()
    else:
        await msg.answer(bot_off())


@dp.message_handler(commands=['cashier'], state="*")
async def send_welcome(msg: types.Message, state: FSMContext):
    if switch_check():
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(ADD_BUT, DOWN_BUT, CANSEL_LS, CONVERT_BUT)
        await bot.send_message(msg.chat.id, "Оберіть наступний розділ:", reply_markup=keyboard)
        await FSMDistributor.where.set()
    else:
        await msg.answer(bot_off())


@dp.callback_query_handler(lambda call: True)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == PRIVET_ROOM_BUT.callback_data:
        await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                    reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=FSMPhone.add_phone)
async def send_welcome(msg: types.Message, state: FSMContext):
    try:
        phone = msg.contact.phone_number
        add_new_user(msg.from_user.id, msg.from_user.full_name, phone, msg.from_user.username)
        keyword = types.ReplyKeyboardRemove()
        await msg.answer("ДЯКУЮ ЗА РЕЄСТРАЦІЮ, ТЕПЕР ВИ МОЖЕТЕ КОРИСТУВАТИСЬ БОТОМ", reply_markup=keyword)
        await state.finish()
        async with state.proxy() as data:
            data["kind_number"] = 0
            try:
                user = data["referal"]
                if check_register(user) and msg.from_user.id != int(user) and check_referral(user, msg.from_user.id):
                    await bot.send_message(user, f"за вашим реферальним посиланням приєднався новий користувач:"
                                                 f" {msg.from_user.full_name}".upper())
            except Exception:
                pass
        orders = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10]) for x in
                  get_all_orders()]
        if orders:
            async with state.proxy() as data:
                data["step"] = 0
                data["id_order"] = get_all_orders()[0] if get_all_orders() else False
                data["order"] = orders[0]
                keyboard = InlineKeyboardMarkup(row_width=3)
                if msg.from_user.id == get_all_orders()[0][6]:
                    keyboard.add(EDIT_ORDER)
                if msg.from_user.id in admins():
                    keyboard.add(ADMIN_BUT_CANSEL)
                keyboard.add(ARROW_LEFT, ARROW_RIGHT).add(ROOM_FILTER,
                                                          LIST_POKER_ROOMS_BUT2[data["kind_number"]]). \
                    add(CANSEL_LS, GET_ORDER)
                count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders)}"
            await bot.send_message(msg.chat.id, orders[0] + count, reply_markup=keyboard)
            await FSMAllOrders.step1.set()
        else:
            keyboard = InlineKeyboardMarkup(row_width=3).add(ADD_BUT_CANSEL)
            await bot.send_message(msg.chat.id, "ЗАЯВОК НЕМАЄ", reply_markup=keyboard)
            await FSMAllOrders.step1.set()
    except Exception as ex:
        print(ex)
        await msg.answer("Щось пішло не так")


@dp.callback_query_handler(lambda call: True, state=FSMDistributor.where)
async def back(call: types.CallbackQuery, state: FSMContext):
    if not check_ban(call.from_user.id):
        if switch_check() or call.from_user.id in admins():
            if call.data == "ADD_BUT":
                async with state.proxy() as data:
                    data["amount"] = norm_sum_add("min")
                    data["card"] = "xxxx"
                    data["owner"] = "вкажіть власника"
                    data["rules_step"] = False
                    data["code"] = False
                    await bot.edit_message_text(ADD_TEXT1(data["amount"]), call.message.chat.id, call.message.message_id,
                                                reply_markup=ADD_BUTTS(data["amount"], data["card"], data["owner"]))
                await FSMAdd.start_add.set()
            elif call.data == "DOWN_BUT":
                async with state.proxy() as data:
                    data["amount"] = norm_sum_down("min")
                    data["card2"] = "xxxx xxxx xxxx xxxx"
                    data["owner"] = "вкажіть власника"
                    data["rules_step"] = False
                    data["code"] = False
                    await bot.edit_message_text(WH_text(call.from_user.id, data["amount"]), call.message.chat.id,
                                                call.message.message_id,
                                                reply_markup=DOWN_BUTTS(data["amount"], data["card2"], data["owner"]))
                await FSMAdd.start_wh.set()
            elif call.data == "CREATE_ORDER_BUT":
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(CREATE_ORDER_SELL, CREATE_ORDER_BUY, CANSEL_LS)
                await bot.edit_message_text("ВИ ХОЧЕТЕ КУПИТИ ЧИ ПРОДАТИ ІГРОВУ ВАЛЮТУ?", call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard)
            elif call.data == CREATE_ORDER_SELL.callback_data:
                async with state.proxy() as data:
                    data["USD"] = 10
                    data["RATE"] = rate(LIST_POKE_CURRENCY[0].text)
                    data["min_part"] = 1
                    data["term"] = 30
                    data["kind_number"] = 0
                    data["login"] = "вкажіть дані"
                    data["currency"] = 0
                    data["edit"] = False
                    cur = LIST_POKE_CURRENCY[data["currency"]].text
                await bot.edit_message_text(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], cur),
                                            call.message.chat.id,
                                            call.message.message_id, reply_markup=CREATE_BUTTS(data["USD"],
                                                                                               data["RATE"],
                                                                                               data["min_part"],
                                                                                               data["term"],
                                                                                               data["kind_number"],
                                                                                               data["login"],
                                                                                               data["currency"]))
                await FSMCreate.step1.set()
            elif call.data == CREATE_ORDER_BUY.callback_data:
                if get_balance_by_id(call.from_user.id) > 10:
                    async with state.proxy() as data:
                        data["USD"] = 10
                        data["RATE"] = rate(LIST_POKE_CURRENCY[0].text)
                        data["min_part"] = 1
                        data["term"] = 30
                        data["kind_number"] = 0
                        data["login"] = "вкажіть дані"
                        data["currency"] = 0
                        data["edit"] = False
                        cur = LIST_POKE_CURRENCY[data["currency"]].text
                    await bot.edit_message_text(CREATE_BUYER_TEXT1(data["USD"], data["RATE"], cur),
                                                call.message.chat.id,
                                                call.message.message_id, reply_markup=CREATE_BUTTS(data["USD"],
                                                                                                   data["RATE"],
                                                                                                   data["min_part"],
                                                                                                   data["term"],
                                                                                                   data["kind_number"],
                                                                                                   data["login"],
                                                                                                   data["currency"],
                                                                                                   kind="buy"))
                    await FSMCreateBuyer.step1.set()
                else:
                    await call.answer("На балансі не достатньо коштів для ствоення заявки.", show_alert=True)
            elif call.data == ALL_ORDER_BUT.callback_data:
                async with state.proxy() as data:
                    data["kind_number"] = 0
                orders0 = [show_market_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5], x[8], x[10])
                          for x in get_all_orders()]
                my_orders_buy = get_buyer_orders(all_order=True)
                orders2 = [show_order_buyer_text(x, "show") for x in my_orders_buy]
                orders = orders0 + orders2
                if orders:
                    async with state.proxy() as data:
                        data["step"] = 0
                        data["id_order"] = get_all_orders()[0] if get_all_orders() else my_orders_buy[0]
                        data["order"] = orders[0]
                        data["kind"] = "sell" if get_all_orders() else "buy"
                        keyboard = InlineKeyboardMarkup(row_width=2)
                        # if call.from_user.id == get_all_orders()[0][6]:
                        #     keyboard.add(EDIT_ORDER)
                        if call.from_user.id in admins():
                            keyboard.insert(ADMIN_BUT_CANSEL)
                        count = f""
                        if orders0:
                            keyboard.add(BUY_lower, SELL)
                            count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders0)}"
                        elif orders2:
                            keyboard.add(BUY, SELL_lower)
                            count = f"\nПОКАЗАНА {data['step'] + 1} З {len(orders2)}"
                        keyboard.add(ARROW_LEFT, ARROW_RIGHT, ROOM_FILTER,
                                     LIST_POKER_ROOMS_BUT2[data["kind_number"]],
                                     CANSEL_LS, GET_ORDER)
                    await bot.edit_message_text(orders[0] + count, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                    await FSMAllOrders.step1.set()
                else:
                    keyboard = InlineKeyboardMarkup(row_width=2).add(CANSEL_LS)
                    await bot.edit_message_text("ЗАЯВОК НЕМАЄ", call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                    await FSMAllOrders.step1.set()
            elif call.data == ABOUT_BOT_BUT.callback_data:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(FAQ_BUT, CHAT_BUT, ADMIN_CHAT_BUT, CANSEL_LS)
                await bot.edit_message_text(FAQ_text(), call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
                await FSMFaq.step1.set()
            elif call.data == ADD_BUT_CANSEL.callback_data:
                await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id,
                                            call.message.message_id, reply_markup=LS_BUTTONS(call.from_user.id))
            elif call.data == REFERRAL_BUT.callback_data:
                keyboard = InlineKeyboardMarkup(row_width=1)
                keyboard.add(CONVERT_BUT, CANSEL_LS)
                await bot.edit_message_text(referral_text(call.from_user.id), call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard, parse_mode="MARKDOWN")
            elif call.data == CONVERT_BUT.callback_data:
                keyboard = InlineKeyboardMarkup(row_width=3)
                keyboard.add(APPROVE_NO, APPROVE_YES)
                await bot.edit_message_text(convert_balance_text(call.from_user.id), call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard)
                await FSMBalance.step1.set()
            elif call.data == MY_ORDER_BUT.callback_data:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(SELLER_BUT, BUYER_BUT, ADD_BUT_CANSEL, MY_BALANCE)
                await bot.edit_message_text("ВИБЕРІТЬ ЯКІ ЗАЯВКИ ВИВЕСТИ:", call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=keyboard)
                await FSMMyOrders.step1.set()
            elif call.data == "ADMIN":
                await bot.edit_message_text(START_TEXT_ADMIN(), call.message.chat.id, call.message.message_id,
                                            reply_markup=admin_but())
                await FSMAdmin.where.set()
            elif call.data == LS_KASA.callback_data:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(ADD_BUT, DOWN_BUT, CANSEL_LS)
                await bot.edit_message_text("ОБЕРІТЬ ДІЮ:", call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard)
            elif call.data == CANSEL_LS.callback_data:
                await bot.edit_message_text(LS_TEXT(call.from_user.id), call.message.chat.id, call.message.message_id,
                                            reply_markup=LS_BUTTONS(call.from_user.id))
            elif call.data == PROFILE.callback_data:
                await bot.edit_message_text(text_profile(call.from_user.id), call.message.chat.id, call.message.message_id,
                                            reply_markup=profile_buttons(call.from_user.id))
                await FSMProfile.where.set()
        else:
            await bot.send_message(call.from_user.id, bot_off())
    else:
        await bot.send_message(call.from_user.id, "БАН")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
