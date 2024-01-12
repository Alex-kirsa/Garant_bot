from all_states import *
from config import ID_ADMIN_GROUP, id_group_log
from dispatcher import *
from main import rate
from text import *
from buttons import *
from privet_room import *
from aiogram.dispatcher import FSMContext
from database import add_new_order, check_same_order


@dp.callback_query_handler(lambda call: True, state=FSMCreate.step1)
async def back(call, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    # підказки до кнопок
    if call.data == "CR_ROOMS":
        await call.answer(help_poker_room, show_alert=True)
    elif call.data == "CR_GET_LOGIN":
        await call.answer(help_login, show_alert=True)
    elif call.data == "CR_SUMM_USD":
        await call.answer(help_sum_usd, show_alert=True)
    elif call.data == "CR_RATE_GRN":
        await call.answer(help_rate, show_alert=True)
    elif call.data == "CR_MIN_PART":
        async with state.proxy() as data:
            cur = LIST_POKE_CURRENCY[data["currency"]]
            await call.answer(help_min_part+cur.text, show_alert=True)
    elif call.data == "CR_TERM":
        await call.answer(help_term, show_alert=True)
    elif call.data == "CR_GET_currency":
        await call.answer(help_currency, show_alert=True)
    # кнопка повернення назад
    elif call.data == "CR_CANSEL":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(CREATE_ORDER_SELL, CREATE_ORDER_BUY, CANSEL_LS)
        await bot.edit_message_text("ВИ ХОЧЕТЕ КУПИТИ ЧИ ПРОДАТИ ІГРОВУ ВАЛЮТУ?", call.message.chat.id,
                                    call.message.message_id, reply_markup=keyboard)
        await FSMDistributor.where.set()
    # кнопка подати заявку
    elif call.data == "CR_GET_ORDER":
        async with state.proxy() as data:
            data["agreement_create"] = False
            kn = LIST_POKE_ROOMS_BUT[data["kind_number"]].text
            try:
                if data["login"] == "вкажіть дані" or not data["login"]:
                    await call.answer("ви не вказали e-mail/login", show_alert=True)
                else:
                    if check_login_valid(call.from_user.id, data["login"]):
                        await call.answer("Цей e-mail/login вже зареєстрованно іншим користувачем", show_alert=True)
                    else:
                        if not check_same_order(kn, data["USD"], data["RATE"], data["min_part"], data["term"],
                                                call.from_user.id, LIST_POKE_CURRENCY[data["currency"]].text):
                            if data["edit"]:
                                edit_order(kn, data["USD"], data["RATE"], data["min_part"], data["term"], call.from_user.id,
                                           data["login"], LIST_POKE_CURRENCY[data["currency"]].text, data["NUM"])

                                keyboard = InlineKeyboardMarkup(row_width=2).add(CR_CANSEL)
                                await bot.send_message(id_group_log, f"{call.from_user.id} ВІДРЕДАГУВАВ "
                                                                     f"ЗАЯВКУ НА ПРОДАЖ №{data['NUM']}")
                                await bot.edit_message_text(EDIT_TEXT, call.message.chat.id,
                                                            call.message.message_id,
                                                            reply_markup=keyboard)
                                await FSMMyOrders.approve1.set()
                            else:
                                keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0).add(CR_CANSEL, ADD_BUT_APPROVE)
                                await bot.edit_message_text(CREATE_ORDER_TEXT2(data["term"]), call.message.chat.id,
                                                            call.message.message_id,
                                                            reply_markup=keyboard)
                                await FSMCreate.step2.set()
                        else:
                            await call.answer("Заявка з такими даними вже існує", show_alert=True)

            except TypeError as ex:
                print(ex)
                await call.answer("ЩОСЬ ПІШЛО НЕ ТАК, ПОВТОРІТЬ СПРОБУ", show_alert=True)
    # кнопки заміни значень
    elif call.data == "currency":
        async with state.proxy() as data:
            if data["currency"] >= len(LIST_POKE_CURRENCY) - 1:
                data["currency"] = 0
            else:
                data["currency"] += 1
            currency = LIST_POKE_CURRENCY[data["currency"]].text
            data["RATE"] = rate(LIST_POKE_CURRENCY[data["currency"]].text)
            await bot.edit_message_text(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                                        call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=CREATE_BUTTS(data["USD"],
                                                                  data["RATE"],
                                                                  data["min_part"],
                                                                  data["term"],
                                                                  data["kind_number"],
                                                                  data["login"],
                                                                  data["currency"],
                                                                  data["edit"]))
    elif call.data == "CR_ROOMS2":
        async with state.proxy() as data:
            if not data["edit"]:
                if data["kind_number"] >= len(LIST_POKE_ROOMS_BUT) - 1:
                    data["kind_number"] = 0
                else:
                    data["kind_number"] += 1
                currency = LIST_POKE_CURRENCY[data["currency"]].text
                await bot.edit_message_text(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                                            call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=CREATE_BUTTS(data["USD"],
                                                                      data["RATE"],
                                                                      data["min_part"],
                                                                      data["term"],
                                                                      data["kind_number"],
                                                                      data["login"],
                                                                      data["currency"],
                                                                      data["edit"]))
            else:
                await call.answer("Не можна редагувати покер-рум", show_alert=True)
    elif call.data == "CR_SUMM_USD2":
        keyboard.add(CR_CANSEL)
        await bot.edit_message_text(CR_EDIT_USD, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMCreate.edit_usd.set()

    elif call.data == "CR_RATE_GRN2":
        keyboard.add(CR_CANSEL)
        await bot.edit_message_text(CR_EDIT_RATE, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        await FSMCreate.edit_rate.set()
    elif call.data == "CR_MIN_PART2":
        keyboard.add(CR_CANSEL)
        await bot.edit_message_text(CR_EDIT_MIN_PART, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMCreate.edit_min_part.set()
    elif call.data == "CR_TERM2":
        keyboard.add(CR_CANSEL)
        await bot.edit_message_text(CR_EDIT_TERM, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        await FSMCreate.edit_term.set()

    elif call.data == "CR_GET_LOGIN2":
        async with state.proxy() as data:
            if not data["edit"]:
                keyboard.add(CR_CANSEL)
                await bot.edit_message_text("ВВЕДІТЬ ВАШ E-MAIL АБО LOGIN".upper(), call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
                await FSMCreate.mail.set()
            else:
                await call.answer("Не можна редагувати e-mail/login", show_alert=True)


# функція зміни долару
@dp.message_handler(content_types=['text'], state=FSMCreate.edit_usd)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = msg.text.strip().replace(" ", "").replace(",", ".")
            if not int(text) % 1 and int(text) >= 1:
                data["USD"] = int(msg.text.strip())
                currency = LIST_POKE_CURRENCY[data["currency"]].text
                await msg.answer(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                                 reply_markup=CREATE_BUTTS(data["USD"], data["RATE"], data["min_part"], data["term"],
                                                           data["kind_number"],
                                                           data["login"],
                                                           data["currency"],data["edit"]))
                await FSMCreate.step1.set()
            else:
                await msg.answer("Тільки числа кратні 1")

        except ValueError:
            await msg.answer("Тільки числа кратні 1")


# функція зміни курсу гривні
@dp.message_handler(content_types=['text'], state=FSMCreate.edit_rate)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = msg.text.strip().replace(" ", "").replace(",", ".")
            if float(text):
                data["RATE"] = float(msg.text)
                currency = LIST_POKE_CURRENCY[data["currency"]].text
                print(currency)
                if currency == "USD" or currency == "EUR":
                    print(180)
                    r = rate(currency)
                    if r/100*20 + r >= float(text) >= r - r/100*20:
                        await msg.answer(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                                         reply_markup=CREATE_BUTTS(data["USD"], data["RATE"], data["min_part"], data["term"],
                                                                   data["kind_number"],
                                                                   data["login"],
                                                                   data["currency"], data["edit"]))
                        await FSMCreate.step1.set()
                    else:
                        await msg.answer(f"Курс бути у діапазоні +-20% від офіційного курсу: \n"
                                         f"від {r - r/100*20}ГРН \nдо {r/100*20 + r}ГРН".upper())

            else:
                await msg.answer("Тільки числа")

        except ValueError:
            await msg.answer("Тільки числа")


# функція зміни мін частки
@dp.message_handler(content_types=['text'], state=FSMCreate.edit_min_part)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = msg.text.strip().replace(" ", "").replace(",", ".")
            if int(text) <= data["USD"]:
                data["min_part"] = int(msg.text)
                currency = LIST_POKE_CURRENCY[data["currency"]].text
                await msg.answer(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                                 reply_markup=CREATE_BUTTS(data["USD"], data["RATE"], data["min_part"], data["term"],
                                                           data["kind_number"],
                                                           data["login"],
                                                           data["currency"], data["edit"]))
                await FSMCreate.step1.set()
            else:
                await msg.answer(f"Тільки числа, не менше {data['min_part'] } та не більше {data['USD']}")

        except ValueError:
            await msg.answer("Тільки числа")


# функція зміни терміну
@dp.message_handler(content_types=['text'], state=FSMCreate.edit_term)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = msg.text.strip().replace(" ", "").replace(",", ".")
            if int(text) >= 15:
                data["term"] = int(msg.text)
                currency = LIST_POKE_CURRENCY[data["currency"]].text
                await msg.answer(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                                 reply_markup=CREATE_BUTTS(data["USD"], data["RATE"], data["min_part"], data["term"],
                                                           data["kind_number"],
                                                           data["login"],
                                                           data["currency"], data["edit"]))
                await FSMCreate.step1.set()
            else:
                await msg.answer("Тільки числа від 15")

        except ValueError:
            await msg.answer("Тільки числа")


@dp.callback_query_handler(lambda call: True, state=[FSMCreate.edit_min_part, FSMCreate.edit_term, FSMCreate.edit_rate,
                                                     FSMCreate.edit_usd, FSMCreate.mail])
async def back(call, state: FSMContext):
    if call.data == "CR_CANSEL":
        async with state.proxy() as data:
            currency = LIST_POKE_CURRENCY[data["currency"]].text
            await bot.edit_message_text(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                                        call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=CREATE_BUTTS(data["USD"],
                                                                  data["RATE"],
                                                                  data["min_part"],
                                                                  data["term"],
                                                                  data["kind_number"],
                                                                  data["login"],
                                                                  data["currency"],
                                                                  data["edit"]))
        await FSMCreate.step1.set()


@dp.callback_query_handler(lambda call: True, state=FSMCreate.step2)
async def back(call, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    if call.data == "ADD_BUT_RULES0":
        async with state.proxy() as data:
            data["agreement_create"] = True
            await bot.send_message(id_group_log, f"{call.from_user.id} ПОГОДИВСЯ З ПРАВИЛАМИ СТВОРЕННЯ ЗАЯВКИ НА ПРОДАЖ")
            keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES1).add(CR_CANSEL, ADD_BUT_APPROVE)
            await bot.edit_message_text(CREATE_ORDER_TEXT2(data["term"]), call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
    elif call.data == "ADD_BUT_RULES1":
        async with state.proxy() as data:
            data["agreement_create"] = False
            keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0).add(CR_CANSEL, ADD_BUT_APPROVE)
            await bot.edit_message_text(CREATE_ORDER_TEXT2(data["term"]), call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
    elif call.data == "ADD_BUT_RULES":
        await call.answer("Rules.....", show_alert=True)
    elif call.data == "ADD_BUT_APPROVE":
        async with state.proxy() as data:
            try:
                check_agreement = data["agreement_create"]
                if check_agreement:
                    kn = LIST_POKE_ROOMS_BUT[data["kind_number"]].text
                    if check_valid(call.from_user.id, kn, data["login"]):
                        add_new_order(kn, data["USD"], data["RATE"], data["min_part"], data["term"], call.from_user.id,
                                      data["login"], LIST_POKE_CURRENCY[data["currency"]].text)
                        await bot.send_message(id_group_log, f"{call.from_user.id} "
                                                             f"СТВОРИВ НОВУ ЗАЯВКУ НА ПРОДАЖ")
                        keyboard.add(PRIVET_ROOM_BUT)
                        for x in get_all_user2():
                            try:
                                info = get_custom_info(x[0])
                                if info:
                                    if info[2] == "ON":
                                        text = "НА ВІТРИНІ З'ЯВИЛАСЯ НОВА ЗАЯВКА\n\n" \
                                               "ПРОДАМ\n" \
                                               f"ПРОДАВЕЦЬ: {call.from_user.id}\n" \
                                               f"ПОКЕР-РУМ: {kn}\n" \
                                               f"СУМА USD: {data['USD']}\n" \
                                               f"КУРС ГРН: {data['RATE']}\n"
                                        await bot.send_message(x[0], text)
                                else:
                                    text = "НА ВІТРИНІ З'ЯВИЛАСЯ НОВА ЗАЯВКА\n\n" \
                                           "ПРОДАМ\n" \
                                           f"ПРОДАВЕЦЬ: {call.from_user.id}\n" \
                                           f"ПОКЕР-РУМ: {kn}\n" \
                                           f"СУМА USD: {data['USD']}\n" \
                                           f"КУРС ГРН: {data['RATE']}\n"
                                    await bot.send_message(x[0], text)
                            except Exception as ex:
                                pass
                        await bot.edit_message_text(CR_TEXT_DONE, call.message.chat.id, call.message.message_id,
                                                    reply_markup=keyboard)
                    else:
                        add_new_order(kn, data["USD"], data["RATE"], data["min_part"], data["term"], call.from_user.id,
                                      data["login"], LIST_POKE_CURRENCY[data["currency"]].text, status="valid")
                        await bot.send_message(id_group_log, f"{call.from_user.id} "
                                                             f"СТВОРИВ ПЕРШУ ЗАЯВКУ НА ПРОДАЖ")
                        if reason_to_valid(kn, call.from_user.id):
                            await bot.send_message(ID_ADMIN_GROUP, f"НОВА ЗАЯВКА НА вітрину для перевірки \nпродавець: "
                                                                   f"{call.from_user.id}\n"
                                                                   f"ПСЕВДОНІМ: @{call.from_user.username}\n"
                                                                   f"Причина: змінив логін до покер-рум".upper())
                        else:
                            await bot.send_message(ID_ADMIN_GROUP, f"НОВА ЗАЯВКА НА вітрину для перевірки \nпродавець: "
                                                                   f"{call.from_user.id}\n"
                                                                   f"ПСЕВДОНІМ: @{call.from_user.username}\n"
                                                                   f"Причина: перша заявка у цьому румі".upper())

                        await call.answer("Ця заявка перевіряється адміністратором. після перевірки вона "
                                          "з'явиться на вітрині", show_alert=True)
                        keyboard.add(PRIVET_ROOM_BUT)
                        await bot.edit_message_text(CR_TEXT_DONE_admin, call.message.chat.id, call.message.message_id,
                                                    reply_markup=keyboard)
                    if check_thief(call.from_user.id, "orders", login=data["login"]):
                        text = []
                        for x in check_thief(call.from_user.id, "orders", login=data["login"]):
                            text.append(x[0])
                        for x in admins():
                            await bot.send_message(x, f"Підозріла заявка № {check_n()}, створення заявки ну вітрину \n"
                                                      f"співпадіння з такими заявками {text}\n".upper())


                else:
                    await call.answer("Прийміть правила сервісу")
            except KeyError:
                await call.answer("Прийміть правила сервісу")
    elif call.data == "PRIVET_ROOM_BUT":
        await bot.send_message(call.message.chat.id, LS_TEXT(call.from_user.id),
                               reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()
    elif call.data == "CR_CANSEL":
        async with state.proxy() as data:
            currency = LIST_POKE_CURRENCY[data["currency"]].text
            await bot.edit_message_text(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                                        call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=CREATE_BUTTS(data["USD"],
                                                                  data["RATE"],
                                                                  data["min_part"],
                                                                  data["term"],
                                                                  data["kind_number"],
                                                                  data["login"],
                                                                  data["currency"],
                                                                  data["edit"]))
        await FSMCreate.step1.set()


@dp.message_handler(content_types=['text'], state=FSMCreate.mail)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["login"] = msg.text
        currency = LIST_POKE_CURRENCY[data["currency"]].text
        await msg.answer(CREATE_ORDER_TEXT1(data["USD"], data["RATE"], currency),
                         reply_markup=CREATE_BUTTS(data["USD"],
                                                   data["RATE"],
                                                   data["min_part"],
                                                   data["term"],
                                                   data["kind_number"],
                                                   data["login"],
                                                   data["currency"],
                                                   data["edit"]))
        await FSMCreate.step1.set()


