from dispatcher import *
from text import *
from buttons import *
from privet_room import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import approve_balance_add, approve_balance_down, check_thief, norm_sum_add, norm_sum_down
from all_states import *
from config import ID_ADMIN_GROUP, id_group_log


# функції по роботі з поповненям коштів
@dp.callback_query_handler(lambda call: True, state=FSMAdd.start_add)
async def back(call: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    if call.data == "ADD_BUT_SUMM2":
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(ADD_EDIT_SUMM, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        await FSMAdd.change_sum.set()
    elif call.data == "ADD_BUT_LAST4NUM2":
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(ADD_EDIT_CARD, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
        await FSMAdd.card.set()
    elif call.data == "ADD_BUT_OWNER2":
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(ADD_EDIT_OWNER, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdd.owner.set()
    elif call.data == "ADD_BUT_STEP2" or call.data == ADD_BUT_CANSEL_APPROVE_ADD.callback_data:
        async with state.proxy() as data:
            data["agreement"] = False
            if data["owner"] != "вкажіть власника":
                if data["card"] != "xxxx":
                    data["rules_step"] = True
                    keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0).add(ADD_BUT_CANSEL, ADD_BUT_APPROVE)
                    await bot.edit_message_text(ADD_TEXT2_2, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard)
                else:
                    await call.answer("ви не вказали останні 4 цифри карти", show_alert=True)
            else:
                await call.answer("ви не вказали власника карти", show_alert=True)
    elif call.data == "ADD_BUT_RULES0":
        async with state.proxy() as data:
            data["agreement"] = True
            await bot.send_message(id_group_log, f"{call.from_user.id} ПОГОДИВСЯ З ПРАВИЛАМИ ПОПОВНЕННЯ")
        keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES1).add(ADD_BUT_CANSEL, ADD_BUT_APPROVE)
        await bot.edit_message_text(ADD_TEXT2_2, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == "ADD_BUT_RULES1":
        async with state.proxy() as data:
            data["agreement"] = False
        keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0).add(ADD_BUT_CANSEL, ADD_BUT_APPROVE)
        await bot.edit_message_text(ADD_TEXT2_2, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == "ADD_BUT_RULES":
        await call.answer("Rules.....", show_alert=True)
    elif call.data == "ADD_BUT_APPROVE":
        async with state.proxy() as data:
            try:
                check_agreement = data["agreement"]
                if check_agreement:
                    data["rules_step"] = False
                    keyboard.add(ADD_BUT_CANSEL_APPROVE_ADD, ADD_BUT_DONE2)
                    await bot.edit_message_text(ADD_TEXT3(data["amount"]), call.message.chat.id,
                                                call.message.message_id,
                                                reply_markup=keyboard, parse_mode="MARKDOWN")
                else:
                    await call.answer("Прийміть правила сервісу")
            except KeyError:
                await call.answer("Прийміть правила сервісу")
    elif call.data == "ADD_BUT_DONE" or call.data == "ADD_BUT_CANSEL":
        async with state.proxy() as data:
            step = data["rules_step"]
            if step:
                data["rules_step"] = False
                await bot.edit_message_text(ADD_TEXT1(data["amount"]), call.message.chat.id, call.message.message_id,
                                            reply_markup=ADD_BUTTS(data["amount"], data["card"], data["owner"]))
            elif call.data == "ADD_BUT_DONE":
                keyboard.add(PRIVET_ROOM_BUT)
                await bot.edit_message_text(ADD_TEXT4, call.message.chat.id, call.message.message_id,
                                            reply_markup=keyboard)
                if data["code"]:
                    pass
                    # data['amount'] = round(float(data['amount'])/100 * get_promoCode(data["code"])[4], 2)
                approve_balance_add(data['amount'], data['card'], data['owner'], call.from_user.id,
                                    call.from_user.full_name, data["code"])
                await bot.send_message(id_group_log, f"{call.from_user.id} ПОДАВ ЗАЯВКУ НА ПОПОВНЕННЯ "
                                                     f"{data['amount']} ГРН")
                await bot.send_message(ID_ADMIN_GROUP, text_for_admin_add(data['amount'], data['card'], data['owner'],
                                                                          call.from_user.id, call.from_user.username,
                                                                          data["code"]))
                update_code(data['code'], "add")

            else:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(ADD_BUT, DOWN_BUT, CANSEL_LS,)
                await bot.edit_message_text("ОБЕРІТЬ ДІЮ:", call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard)
                await FSMDistributor.where.set()
    elif call.data == "PROMO_CODE":
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(DOWN_EDIT_PROMO, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdd.promo_code_add.set()
    elif call.data == "PRIVET_ROOM_BUT":
        await bot.send_message(call.message.chat.id, LS_TEXT(call.from_user.id),
                               reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()
    # Підказки на перший крок
    elif call.data == "ADD_BUT_SUMM":
        await call.answer(help_sum, show_alert=True)
    elif call.data == "ADD_BUT_LAST4NUM":
        await call.answer(help_4num, show_alert=True)
    elif call.data == "ADD_BUT_OWNER":
        await call.answer(help_owner, show_alert=True)
    elif call.data == PROMO_CODE_INFO.callback_data:
        await call.answer(help_promo, show_alert=True)


@dp.message_handler(content_types=['text'], state=FSMAdd.promo_code_add)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["code"] = msg.text
        code = check_promoCode(msg.text, "add")
        if code:
            await msg.answer("промокод активовано\n"
                             f"Ви отримаєте +{code[0][4]}% від суми зарахування".upper())
            summ = data["amount"]/100 * code[0][4]
            data["allSum"] = data["amount"] + summ
            await msg.answer(ADD_TEXT1(data["allSum"]), reply_markup=ADD_BUTTS(data["amount"], data["card"],
                                                                               data["owner"],
                                                                               data["code"]))
            await bot.send_message(id_group_log, f"{msg.from_user.id} ЗАСТОСУВАВ ПРОМОКОД {data['code']} НА "
                                                 f"ПОПОВНЕННЯ {code[0][4]}% {summ} ГРН")
        else:
            await msg.answer("промокод не знайдено або не дійсний".upper())
            await msg.answer(ADD_TEXT1(data["amount"]), reply_markup=ADD_BUTTS(data["amount"], data["card"], data["owner"]))
        await FSMAdd.start_add.set()


@dp.message_handler(content_types=['text'], state=FSMAdd.change_sum)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = int(msg.text.replace(" ", ""))
            if norm_sum_add("min") <= text <= norm_sum_add("max"):
                data["amount"] = text
                await msg.answer(ADD_TEXT1(data["amount"]), reply_markup=ADD_BUTTS(data["amount"], data["card"], data["owner"]))
                await FSMAdd.start_add.set()
            else:
                await msg.answer(f"дозволений мінімум {f_t(norm_sum_add('min'))} ГРН.\nдозволений максимум: "
                                 f"{f_t(norm_sum_add('max'))} ГРН.".upper())

        except ValueError:
            await msg.answer("Тільки числа кратні 1")


@dp.message_handler(content_types=['text'], state=FSMAdd.card)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = str(msg.text.strip())
            if len(text) == 4 and text.isdigit():
                data["card"] = str(msg.text.strip())
                await msg.answer(ADD_TEXT1(data["amount"]), reply_markup=ADD_BUTTS(data["amount"], data["card"], data["owner"]))
                await FSMAdd.start_add.set()
            else:
                await msg.answer("Тільки 4 цифри")

        except ValueError:
            await msg.answer("Тільки 4 цифри")


@dp.message_handler(content_types=['text'], state=FSMAdd.owner)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text.replace(" ", "").replace(".", "").isalpha():
            data["owner"] = msg.text
            await msg.answer(ADD_TEXT1(data["amount"]), reply_markup=ADD_BUTTS(data["amount"], data["card"], data["owner"]))
            await FSMAdd.start_add.set()
        else:
            await msg.answer("Власник картки не може містити цифри")


@dp.callback_query_handler(lambda call: True, state=[FSMAdd.change_sum, FSMAdd.card, FSMAdd.owner])
async def back(call, state: FSMContext):
    if call.data == "ADD_BUT_CANSEL":
        async with state.proxy() as data:
            await bot.edit_message_text(ADD_TEXT1(data["amount"]), call.message.chat.id, call.message.message_id,
                                        reply_markup=ADD_BUTTS(data["amount"], data["card"], data["owner"]))
        await FSMAdd.start_add.set()


# функції для виведення коштів
@dp.callback_query_handler(lambda call: True, state=FSMAdd.start_wh)
async def back(call: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardMarkup(row_width=2)
    # заміна значень при виведенні коштів( сумма, карта, власник)
    if call.data == "ADD_BUT_SUMM2":
        keyboard.add(ADD_BUT_CANSEL)
        if float(get_balance_by_id(call.from_user.id)) > norm_sum_down('min'):
            await bot.edit_message_text(DOWN_EDIT_SUMM, call.message.chat.id, call.message.message_id,
                                        reply_markup=keyboard)
            await FSMAdd.change_sum2.set()
        else:
            await call.answer(f"Баланс менше дозволениого мінімуму {f_t(norm_sum_down('min'))} ГРН", show_alert=True)
    elif call.data == "DOWN_BUT_LAST4NUM2":
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(DOWN_EDIT_CARD, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdd.card2.set()
    elif call.data == "ADD_BUT_OWNER2":
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(ADD_EDIT_OWNER, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdd.owner2.set()
    elif call.data == "PROMO_CODE":
        keyboard.add(ADD_BUT_CANSEL)
        await bot.edit_message_text(DOWN_EDIT_PROMO, call.message.chat.id, call.message.message_id,
                                    reply_markup=keyboard)
        await FSMAdd.promo_code.set()
    # згода з правилами та підпис
    elif call.data == "ADD_BUT_STEP2":
        async with state.proxy() as data:
            data["agreement"] = False
            if data["owner"] != "вкажіть власника":
                if float(get_balance_by_id(call.from_user.id)) >= float(data["amount"]):
                    if data["card2"] != "XXXX XXXX XXXX XXXX":
                        data["rules_step"] = True
                        keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0).add(ADD_BUT_CANSEL, ADD_BUT_APPROVE)
                        await bot.edit_message_text(ADD_TEXT2, call.message.chat.id, call.message.message_id,
                                                    reply_markup=keyboard)
                    else:
                        await call.answer("ви не вказали номер карти", show_alert=True)
                else:
                    await call.answer(f"сума виведення перевищує поточний баланс: "
                                      f"{get_balance_by_id(call.from_user.id)}".upper(), show_alert=True)
            else:
                await call.answer("ви не вказали власника карти", show_alert=True)

    elif call.data == "ADD_BUT_RULES0":
        async with state.proxy() as data:
            data["agreement"] = True
            await bot.send_message(id_group_log, f"{call.from_user.id} ПОГОДИВСЯ З ПРАВИЛАМИ ВИВЕДЕННЯ")
        keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES1).add(ADD_BUT_CANSEL, ADD_BUT_APPROVE)
        await bot.edit_message_text(ADD_TEXT2, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == "ADD_BUT_RULES1":
        async with state.proxy() as data:
            data["agreement"] = False
        keyboard.add(ADD_BUT_RULES, ADD_BUT_RULES0).add(ADD_BUT_CANSEL, ADD_BUT_APPROVE)
        await bot.edit_message_text(ADD_TEXT2, call.message.chat.id, call.message.message_id, reply_markup=keyboard)
    elif call.data == "ADD_BUT_APPROVE":
        async with state.proxy() as data:
            try:
                check_agreement = data["agreement"]
                if check_agreement:
                    keyboard.add(PRIVET_ROOM_BUT)
                    res = f"\n\nКОШТИ ЗАРЕЗЕРВОВАНІ НА ПЕРІОД РОЗГЛЯДУ ЗАЯВКИ"
                    await bot.edit_message_text(ADD_TEXT4 + res, call.message.chat.id, call.message.message_id,
                                                reply_markup=keyboard, )
                    approve_balance_down(data['amount'], data['card2'], data['owner'], call.from_user.id,
                                         call.from_user.full_name, data["code"])
                    update_balance(call.from_user.id, -data['amount'])
                    update_code(data['code'], "down")
                    await bot.send_message(id_group_log, f"{call.from_user.id} ПОДАВ ЗАЯВКУ НА ВИВЕДЕННЯ "
                                                         f"{data['amount']} ГРН\n")
                    if check_thief(call.from_user.id, "down", card=data['card2']):
                        text = []
                        for x in check_thief(call.from_user.id, "down", card=data['card2']):
                            text.append(x[0])

                        await bot.send_message(ID_ADMIN_GROUP, f"Підозріла заявка № {check_nd()}, виведення коштів \n"
                                                               f"співпадіння з такими заявками {text}\n".upper())
                    await bot.send_message(ID_ADMIN_GROUP,
                                           text_for_admin_down(data['amount'], data['card2'], data['owner'],
                                                               call.from_user.id, call.from_user.username, data["code"]))
                else:
                    await call.answer("Прийміть правила сервісу")
            except KeyError as ex:
                print(ex)
                await call.answer("Прийміть правила сервісу")
    elif call.data == "PRIVET_ROOM_BUT":
        await bot.send_message(call.message.chat.id, LS_TEXT(call.from_user.id),
                               reply_markup=LS_BUTTONS(call.from_user.id))
        await FSMDistributor.where.set()
    elif call.data == "ADD_BUT_CANSEL":
        async with state.proxy() as data:
            if data["rules_step"]:
                data["rules_step"] = False
                await bot.edit_message_text(WH_text(call.from_user.id, data["amount"]), call.message.chat.id,
                                            call.message.message_id,
                                            reply_markup=DOWN_BUTTS(data["amount"], data["card2"], data["owner"]))
            else:
                keyboard = InlineKeyboardMarkup(row_width=2)
                keyboard.add(ADD_BUT, DOWN_BUT, CANSEL_LS,)
                await bot.edit_message_text("ОБЕРІТЬ ДІЮ:", call.message.chat.id,
                                            call.message.message_id, reply_markup=keyboard)
                await FSMDistributor.where.set()
    # Підказки на перший крок
    elif call.data == "ADD_BUT_SUMM":
        await call.answer(help_sum, show_alert=True)
    elif call.data == "DOWN_BUT_LAST4NUM":
        await call.answer(help_16num, show_alert=True)
    elif call.data == "ADD_BUT_OWNER":
        await call.answer(help_owner, show_alert=True)
    elif call.data == PROMO_CODE_INFO.callback_data:
        await call.answer(help_promo, show_alert=True)


@dp.callback_query_handler(lambda call: True, state=FSMAdd.promo_code_add)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data:
        async with state.proxy() as data:
            await bot.edit_message_text(WH_text(call.from_user.id, data["amount"]), call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=DOWN_BUTTS(data["amount"], data["card"], data["owner"]))
            await FSMAdd.start_add.set()


@dp.callback_query_handler(lambda call: True, state=FSMAdd.promo_code)
async def back(call: types.CallbackQuery, state: FSMContext):
    if call.data == ADD_BUT_CANSEL.callback_data:
        async with state.proxy() as data:
            await bot.edit_message_text(WH_text(call.from_user.id, data["amount"]), call.message.chat.id,
                                        call.message.message_id,
                                        reply_markup=DOWN_BUTTS(data["amount"], data["card2"], data["owner"]))
            await FSMAdd.start_wh.set()


@dp.message_handler(content_types=['text'], state=FSMAdd.promo_code)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if check_promoCode(msg.text, "down"):
            data["code"] = msg.text
            code = check_promoCode(msg.text, "down")
            await msg.answer("промокод активовано "
                             f"Ви отримаєте -{code[0][4]}% ЗНИЖКУ НА КОМІСІЮ ВИВЕДЕННЯ КОШТІВ ".upper())
            await msg.answer(WH_text(msg.from_user.id, data["amount"], code[0][4]), reply_markup=DOWN_BUTTS(data["amount"],
                                                                                                      data["card2"],
                                                                                                      data["owner"],
                                                                                                      data["code"]))
            summ = float(data["amount"])
            await bot.send_message(id_group_log, f"{msg.from_user.id} ЗАСТОСУВАВ ПРОМОКОД {data['code']} НА "
                                                 f"ВИВЕДЕННЯ  {code[0][4]}% "
                                                 f"{(summ / 100 * tax() + get_tax_grn()) / 100 * float(code[0][4])} ГРН")

        else:
            await msg.answer("промокод не знайдено або не дійсний".upper())
            await msg.answer(WH_text(msg.from_user.id, data["amount"], False), reply_markup=DOWN_BUTTS(data["amount"],
                                                                                                       data["card2"],
                                                                                                       data["owner"]))
        await FSMAdd.start_wh.set()


@dp.message_handler(content_types=['text'], state=FSMAdd.change_sum2)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = int(msg.text.replace(" ", ""))
            if norm_sum_down('min') <= text <= norm_sum_down('max'):
                if int(float(get_balance_by_id(msg.from_user.id))) >= text:
                    data["amount"] = text
                    await msg.answer(WH_text(msg.from_user.id, data["amount"]), reply_markup=DOWN_BUTTS(data["amount"],
                                                                                                        data["card2"],
                                                                                                        data["owner"]))
                    await FSMAdd.start_wh.set()
                else:
                    await msg.answer(f"Сума перевищує поточний баланс \nбаланс зараз:"
                                     f" {get_balance_by_id(msg.from_user.id)} грн".upper())
            else:
                await msg.answer(f"дозволений мінімум {f_t(norm_sum_down('min'))} ГРН.\nдозволений максимум: "
                                 f"{f_t(norm_sum_down('max'))} ГРН.".upper())

        except Exception:
            await msg.answer("Тільки числа кратні 1")


@dp.message_handler(content_types=['text'], state=FSMAdd.card2)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            text = str(msg.text.strip().replace(" ", ""))
            if len(text) == 16 and text.isdigit():
                data["card2"] = msg.text.strip()
                await msg.answer(WH_text(msg.from_user.id, data["amount"]), reply_markup=DOWN_BUTTS(data["amount"],
                                                                                                    data["card2"],
                                                                                                    data["owner"]))
                await FSMAdd.start_wh.set()
            else:
                await msg.answer("Тільки 16 цифер")
        except ValueError:
            await msg.answer("Тільки 16 цифер")


@dp.message_handler(content_types=['text'], state=FSMAdd.owner2)
async def back(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if msg.text.replace(" ", "").replace(".", "").isalpha():
            data["owner"] = msg.text
            await msg.answer(WH_text(msg.from_user.id, data["amount"]), reply_markup=DOWN_BUTTS(data["amount"],
                                                                                                data["card2"],
                                                                                                data["owner"]))
            await FSMAdd.start_wh.set()
        else:
            await msg.answer("Власник картки не може містити цифри")


@dp.callback_query_handler(lambda call: True, state=[FSMAdd.change_sum, FSMAdd.card, FSMAdd.owner])
async def back(call, state: FSMContext):
    if call.data == "ADD_BUT_CANSEL":
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(ADD_BUT_SUMM, ADD_BUT_SUMM2). \
            add(ADD_BUT_LAST4NUM, ADD_BUT_LAST4NUM2). \
            add(ADD_BUT_OWNER, ADD_BUT_OWNER2). \
            add(ADD_BUT_CANSEL, ADD_BUT_STEP2)
        async with state.proxy() as data:
            await bot.send_message(call.message.chat.id, ADD_TEXT1(data["amount"]), reply_markup=keyboard)
            await FSMAdd.start_wh.set()


@dp.callback_query_handler(lambda call: True, state=[FSMAdd.change_sum2, FSMAdd.card2, FSMAdd.owner2])
async def back(call, state: FSMContext):
    if call.data == "ADD_BUT_CANSEL":
        async with state.proxy() as data:
            await bot.send_message(call.message.chat.id, WH_text(call.from_user.id, data["amount"]),
                                   reply_markup=DOWN_BUTTS(data["amount"], data["card2"], data["owner"]))
        await FSMAdd.start_wh.set()
