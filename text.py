from datetime import datetime, timedelta
from database import *


def START_MESS(name):
    text = f"ЛАСКАВО ПРОСИМО, {name} \n\n" \
           "P2P БОТ ПРИЗНАЧЕНИЙ ДЛЯ ПРОВЕДЕННЯ БЕЗПЕЧНИХ УГОД КУПІВЛІ / ПРОДАЖУ ІГРОВОЇ ВАЛЮТИ В ПОКЕР-РУМАХ.\n\n" \
           "ЯК ЦЕ ВЛАШТОВАННО?\n" \
           f"{get_bot_name()} - ЦЕ ДОДАТКОВА ЛАНКА В УГОДІ, ЧЕРЕЗ ЯКУ ПРОВОДЯТЬ ГРОШІ ТАКИМ ЧИНОМ, ЩОБ ЗАБЕЗПЕЧИТИ БЕЗПЕКУ ОБОХ УЧАСНИКІВ.\n\n" \
           f"СЕРВІС СТЯГУЄ КОМІСІЮ ЗА ВИВІД З БОТА В {get_tax()}% + {get_tax_grn()} ГРН\n\n" \
           "10% ВІД ПРИБУТКУ ЙДЕ НА БЛАГОДІЙНІСТЬ"
    return text.upper()


def ADD_TEXT1(summ):
    text = f"Поповнення балансу\n\n БАЛАНС БУДЕ ПОПОВНЕНО НА: {summ} ГРН \n\n" \
          f"Ви можете дізнатись опис налаштувань, натиснувши на його назву.".upper()
    return text


ADD_TEXT2 = "Подаючи заявку, я приймаю правила сервісу і підтверджую достовірність зазначених даних".upper()
wh_text2 = "Подаючи заявку, я приймаю правила сервісу і підтверджую достовірність зазначених даних".upper()


# WH_TEXT_DONE = "ЗАЯВКА ПЕРЕДАНА АДМІНАМ\nЧЕКАЙТЕ НА ЗАРАХУВАННЯ ПРОТЯГОМ 60 ХВ.\n\nУ РОБОЧИЙ ЧАС\n" \
#                "ГРАФІК РОБОТИ: З 12:00 ДО 00:00"

ADD_TEXT2_2 = "Подаючи заявку, я приймаю правила сервісу і підтверджую достовірність зазначених даних\n\n" \
              "ЗАБОВ'ЯЗУЮСЬ ЗРОБИТИ ПЕРЕКАЗ КОШТІВ ПРОТЯГОМ: 15 ХВ. ПІСЛЯ ОТРИМАННЯ РЕКВІЗИТІВ".upper()


def ADD_TEXT3(amount):
    text = f"ПЕРЕКАЖІТЬ: {amount} ГРН\n\nКАРТКА: `{card}` \nВЛАСНИК: {founder()}\n\nПІСЛЯ ПЕРЕКАЗУ НАТИСНІТЬ 'ГОТОВО'"
    return text.upper()


ADD_TEXT4 = work_time()
ADD_EDIT_SUMM = f"ВВЕДІТЬ СУММУ ВІД: {norm_sum_add('min')} ГРН.".upper()
DOWN_EDIT_SUMM = f"ВВЕДІТЬ СУММУ ВІД: {norm_sum_down('min')} ГРН.".upper()
ADD_EDIT_CARD = "Введіть остані 4 цифри".upper()
ADD_EDIT_OWNER = "ВВЕДІТЬ ПІБ КАРТКИ ОДЕРЖУВАЧА".upper()
DOWN_EDIT_CARD = "ВВЕДІТЬ 16-ЗНАЧНИЙ НОМЕР КАРТКИ ОДЕРЖУВАЧА".upper()
DOWN_EDIT_PROMO = "введіть ваш промокод".upper()


def WH_text(id_user, summ, promo=""):
    if promo:
        all_tax = summ/100*tax()+get_tax_grn()
        amount = summ - (all_tax - (all_tax / 100 * float(promo)))
    else:
        amount = round((summ - (summ / 100 * tax())) - get_tax_grn(), 2)
    text = "ВИВЕДЕННЯ КОШТІВ \n\n" \
           f"КОМІСІЯ ЗА ВИВІД {tax()}% + {get_tax_grn()} ГРН.\n\n" \
           f"ВАШ БАЛАНС: {get_balance_by_id(id_user)} ГРН.\n" \
           f"СУМА ВИВОДУ: {summ} ГРН. \n" \
           f"ОТРИМАЄТЕ НА КАРТКУ: {amount} ГРН.\n\n" \
           "ВИ МОЖЕТЕ ДІЗНАТИСЯ ОПИС НАЛАШТУВАННЯ, НАТИСНУВШИ НА ЙОГО НАЗВУ."
    return text.upper()


RULES_LINK = rules()


def CREATE_ORDER_TEXT1(usd, rate, currency="USD"):
    text = "ЗАЯВКА НА ВИВЕДЕННЯ КОШТІВ З ПОКЕР-РУМУ\n\n" \
           f"ЗА {usd} {currency} ВИ ОТРИМАЄТЕ {round(usd * rate,2)} ГРН\n\n" \
           "ВИ МОЖЕТЕ ДІЗНАТИСЯ ОПИС НАЛАШТУВАННЯ, " \
           "НАТИСНУВШИ НА ЙОГО НАЗВУ."
    return text.upper()


def CREATE_BUYER_TEXT1(usd, rate, currency="USD"):
    text = "ЗАЯВКА НА КУПІВЛЮ КОШТІВ З ПОКЕР-РУМУ \n\n" \
           f"ЗА {usd} {currency} ВИ ВІДДАЄТЕ {round(usd * rate,2)} ГРН\n\n" \
           "ВИ МОЖЕТЕ ДІЗНАТИСЯ ОПИС НАЛАШТУВАННЯ, " \
           "НАТИСНУВШИ НА ЙОГО НАЗВУ."
    return text.upper()


def CREATE_ORDER_TEXT2(term):
    text = "ПОДАЮЧИ ЗАЯВКУ, Я ПРИЙМАЮ ПРАВИЛА СЕРВІСУ І ПІДТВЕРДЖУЮ ДОСТОВІРНІСТЬ ЗАЗНАЧЕНИХ ДАНИХ\n\n" \
            f"ЗОБОВ'ЯЗУЮСЬ ЗРОБИТИ ПЕРЕКАЗ КОШТІВ ПРОТЯГОМ: {term} ХВ. ПІСЛЯ ОТРИМАННЯ ЗУСТРІЧНОЇ ЗАЯВКИ"
    return text


def CREATE_ORDER_TEXT_buy(term):
    text = "ПОДАЮЧИ ЗАЯВКУ, Я ПРИЙМАЮ ПРАВИЛА СЕРВІСУ І ПІДТВЕРДЖУЮ ДОСТОВІРНІСТЬ ЗАЗНАЧЕНИХ ДАНИХ\n\n" \
            f"ЗОБОВ'ЯЗУЮСЬ ПІДТВЕРДИТИ ОТРИМАННЯ ІГРОВОЇ ВАЛЮТИ ПРОТЯГОМ: {term} ХВ. ПІСЛЯ ОТРИМАННЯ ЗУСТРІЧНОЇ ЗАЯВКИ"
    return text


CR_EDIT_USD = "Введіть суму кратну 1".upper()
CR_EDIT_RATE = "Введіть курс гривні".upper()
CR_EDIT_MIN_PART = "Введіть мінімальну частку".upper()
CR_EDIT_TERM = "Введіть термін".upper()
CR_TEXT_DONE = "Заявку розміщено на сервісі".upper()
CR_TEXT_DONE_admin = "ЗАЯВКА ВІДПРАВЛЕНА АДМІНІСТРАТОРАМ".upper()


def f_t(text):
    return '{0:,}'.format(round(text)).replace(',', ' ')


def text_balance(order):
    status = ""
    text = ""
    kind = ""
    if order[5] == "approve":
        status = "підтверджена"
    if order[5] == "cansel":
        status = "скасована"
    if order[5] == "in_process":
        status = "чекає підтвердженя"
    code = order[8]
    if len(str(order[2])) == 16:
        text += "заявка виведення\n\n"
        kind = f"СУМА ВИВЕДЕННЯ: {order[1]} ГРН\nномер КАРТКИ: {order[2]}\n"
        if code and get_promoCode(code):
            promo_code = get_promoCode(code)
            all_tax = (order[1] / 100 * tax() + get_tax_grn()) - \
                      (order[1] / 100 * tax() + get_tax_grn()) / 100 * float(promo_code[4])
            code = f"\nПРОМОКОД: {code} ({promo_code[4]}%, " \
                   f"{(order[1] / 100 * tax() + get_tax_grn()) / 100 * float(promo_code[4])} ГРН)\n" \
                   f"ЗАРАХOВАНO: {order[1] -  all_tax} ГРН\n".upper()
        else:
            code = ""
    elif len(str(order[2])) == 4:
        text += "заявка поповнення\n\n"
        kind = f"СУМА поповнення: {order[1]} ГРН\nОСТАНІ 4 ЦИФРИ КАРТКИ: {order[2]}\n"
        if code and get_promoCode(code):
            promo_code = get_promoCode(code)
            code = f"\nПРОМОКОД: {code} ({promo_code[4]}%, {order[1] / 100 * float(promo_code[4])} ГРН)\n" \
                   f"ПОПОВНЕНО: {order[1] + order[1] / 100 * float(promo_code[4])} ГРН\n".upper()
        else:
            code = ""
    text += f"ДАТА: {order[7]}\n\n" \
            f"НОМЕР ЗАЯВКИ: {order[0]}\n\n" \
            f"СТАТУС: {status}\n\n".upper()
    text += f"{kind}"
    text = text.upper()
    text += f"ПІБ: {order[3]}\n"

    return text + code


def show_market_text_admin(date, order, seller, ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, status="", currency="USD"):
    all_order = all_orders_stat(seller)
    all_orders_done = all_orders_done_stat(seller)
    done_seller = round(((all_orders_done[0] + get_seller_win(seller)) / all_order[0]) * 100) if all_order[0] else 0
    done_buyer = round(((all_orders_done[1] + get_buyer_win(seller)) / all_order[1]) * 100) if all_order[1] else 0
    user_t_process, user_t_finally = get_aver_t_user(seller)
    text = f"ДАТА: {date}\n\n" \
           f"ЗАЯВКА №: {order}\n\n" \
           f"ПРОДАВЕЦЬ: {seller}\n" \
           f"ПСЕВДОНІМ: @{get_name_user(seller)[4]}\n\n" \
           f"Кількість угод: {all_order[0]}/{done_seller}% ВИКОНАНО\n" \
           f"СЕР. ЧАС ВИКОНАННЯ: {user_t_process} ХВ\n" \
           f"Арбітраж: {dispute_by_user(seller)}/{dispute_winner_by_user(seller)} ВИГРАННО \n\n" \
           f"ПОКЕР-РУМ: {ROOMS}\n".upper()
    text += f"E-MAIL/LOGIN: {get_order_by_id(order)[9]}\n"

    text += f"СУМА: {f_t(SUMM_USD)} {currency}\n" \
            f"КУРС: {RATE_GRN} ГРН\n" \
            f"МІН. ЧАСТКА: {MIN_PART} {get_order_by_id(order)[10]}\n" \
            f"ТЕРМІН ВИКОНАННЯ: {TERM} ХВ.\n".upper()
    return text


def show_market_text(date, order, seller, ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, status="", currency="USD"):
    all_order = all_orders_stat(seller)
    all_orders_done = all_orders_done_stat(seller)
    p1 = (((all_orders_done[0] + get_seller_win(seller)) / all_order[0])*100) if all_order[0] else 0
    done = p1
    user_t_process, user_t_finally = get_aver_t_user(seller)
    custom = get_custom_info(seller)
    seller = custom[1] if custom else seller
    comments = custom[3] if custom else ""
    text = f"ДАТА: {date}\n\n" \
           f"ЗАЯВКА №: {order}\n\n" \
           f"ПРОДАВЕЦЬ: {seller}\n" \
           f"КІЛЬКІСТЬ УГОД: {all_order[0]}/{round(done)}% ВИКОНАНО \n" \
           f"СЕР. ЧАС ВИКОНАННЯ: {user_t_process} ХВ\n" \
           f"АРБІТРАЖ: {dispute_by_user(seller)}/{dispute_winner_by_user(seller)} ВИГРАННО \n\n" \
           f"ПРОДАМ:\n" \
           f"ПОКЕР-РУМ: {ROOMS}\n" \
           f"СУМА: {f_t(SUMM_USD)} {currency}\n" \
           f"КУРС: {RATE_GRN} ГРН\n" \
           f"МІН. ЧАСТКА: {MIN_PART} {get_order_by_id(order)[10]}\n" \
           f"ТЕРМІН ВИКОНАННЯ: {TERM} ХВ.\n"
    return text


def show_all_orders_text(date, order, seller, ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, status="", currency="USD"):
    if status:
        if status == "pause":
            status = "ПАУЗА"
        elif status == "process":
            status = "Розміщена".upper()
        elif status == "waiting":
            status = "ОЧІКУВАННЯ ОПЛАТИ"
        elif status == "cansel":
            status = "СКАСОВАНА"
        elif status == "valid":
            status = "НА ПЕРЕВІРЦІ"
        log = get_login_by_order(order, seller)
        text = f"ДАТА: {date}\n\n" \
               f"ЗАЯВКА №: {order}\n\n" \
               f"СТАТУС: {status}\n\n" \
               f"ПОКЕР-РУМ: {ROOMS}\n" \
               f"E-MAIL/LOGIN: {log}\n" \
               f"СУМА: {f_t(SUMM_USD)} {currency}\n" \
               f"КУРС: {RATE_GRN} ГРН\n" \
               f"МІН. ЧАСТКА: {MIN_PART} {get_order_by_id(order)[10]}\n" \
               f"ТЕРМІН ВИКОНАННЯ: {TERM} ХВ.\n"
    else:
        log = get_login_by_order(order, seller)
        text = f"ДАТА: {date}\n\n" \
               f"ЗАЯВКА №: {order}\n\n" \
               f"ПОКЕР-РУМ: {ROOMS}\n" \
               f"E-MAIL/LOGIN: {log}" \
               f"СУМА: {f_t(SUMM_USD)} {currency}\n" \
               f"КУРС: {RATE_GRN} ГРН\n" \
               f"МІН. ЧАСТКА: {MIN_PART} {get_order_by_id(order)[10]}\n" \
               f"ТЕРМІН ВИКОНАННЯ: {TERM} ХВ.\n"
    return text


def show_all_buyer_text(date, id_order_buyer, part, id_order, status, login_bayer="", id_bayer=""):
    order = get_order_by_id(id_order)
    if status == "finally":
        status = "Підтвердження переказу коштів".upper()
    elif status == "done":
        status = "завершенно успішно".upper()
    elif status == "cansel":
        status = "закрита неуспішно".upper()
    elif status == "dispute":
        status = "арбітраж".upper()
    elif status == "process":
        status = "Розміщена".upper()
    user_name1 = get_name_user(order[6])[4]
    full_name1 = get_name_user(order[6])[1]
    user_name2 = get_name_user(id_bayer)[4]
    full_name2 = get_name_user(id_bayer)[1]
    text = f"НОМЕР ЗАЯВКИ: {order[0]}\n" \
           f"ЗУСТРІЧНА ЗАЯВКА №: {id_order_buyer}\n\n" \
           f"САТУС ЗАЯВКИ: {status} \n\n" \
           f"ID ПРОДАВЦЯ: {order[6]} \n" \
           f"ПСЕВДОНІМ: {user_name1}; {full_name1}\n" \
           f"EMAIL / LOGIN: {order[9]} \n" \
           f"ID ПОКУПЦЯ: {id_bayer}\n" \
           f"ПСЕВДОНІМ: {user_name2}; {full_name2}\n" \
           f"EMAIL / LOGIN: {login_bayer}\n\n" \
           f"ПОКЕР-РУМ: {order[2]}\n" \
           f"СУМА ПЕРЕКАЗУ: {part} {order[10]} ПО {order[3]}"
    return text.upper()


def show_all_dispute_text(order):
    if order[10] == "sell":
        start_order = get_order_by_id(order[1])
    elif order[10] == "buy":
        start_order = get_buyer_orders(order[4], order[1])
    status = order[5]
    if status == "finally":
        status = "Підтвердження переказу коштів".upper()
    elif status == "done":
        status = "завершенно успішно".upper()
    elif status == "cansel":
        status = "закрита неуспішно".upper()
    elif status == "dispute":
        status = "арбітраж".upper()
    elif status == "process":
        status = "Розміщена".upper()
    user_name1 = get_name_user(order[4])[4]
    full_name1 = get_name_user(order[6])[1]
    user_name2 = get_name_user(order[6])[4]
    full_name2 = get_name_user(order[4])[1]
    text = f"ДАТА: {order[7]}\n\n" \
           f"НОМЕР ЗАЯВКИ: {order[0]}\n" \
           f"ЗУСТРІЧНА ЗАЯВКА №: {order[1]}\n\n" \
           f"САТУС ЗАЯВКИ: {status.upper()} \n\n" \
           f"ID ПРОДАВЦЯ: {order[4]} \n" \
           f"ПСЕВДОНІМ: @{user_name1} \n" \
           f"EMAIL/LOGIN: {order[8]} \n\n" \
           f"ID ПОКУПЦЯ: {order[7]}\n" \
           f"ПСЕВДОНІМ: @{user_name2}\n" \
           f"EMAIL/LOGIN: {start_order[9]}\n\n" \
           f"ПОКЕР-РУМ: {start_order[1]}\n" \
           f"СУМА ПЕРЕКАЗУ: {order[2]} {start_order[10]} ПО {start_order[3]}\n" \
           f"ЗАМОРОЖЕНО: {get_reserve(order[0])} ГРН\n"
    return text


def show_buyer_text(order):
    custom = get_custom_info(order[7])
    buyer_cast = custom[1] if custom else order[7]
    if order[10] == "buy":
        sel_order = get_buyer_orders(order[4], order[1])
        login = order[8]
    else:
        sel_order = get_order_by_id(order[1])
        login = sel_order[9]
    status = order[5]
    dispute = False
    w = "НЕ ВКАЗАНО"
    date_time = datetime.strptime(order[3], "%d.%m.%Y, %H:%M") - datetime.now()
    date_time = date_time.total_seconds()
    minutes = divmod(date_time, 60)[0]
    if status == "finally":
        status = "ПІДТВЕРДЖЕННЯ ОТРИМАННЯ КОШТІВ".upper()
    elif status == "done":
        status = "завершенно успішно".upper()
    elif status == "cansel":
        status = "ПРОСРОЧЕНА".upper()
    elif status == "dispute":
        status = "арбітраж".upper()
    elif status == "process":
        status = "ЧЕКАЄ ПЕРЕКАЗУ".upper()
    elif status == "SOLD":
        result_dispute = get_winner(order[0])
        w = "НЕ ВКАЗАНО"
        if result_dispute:
            winner = result_dispute[1]
            if winner == order[4]:
                w = f"ПОКУПЦЯ({winner})"
            elif winner == order[7]:
                w = f"ПРОДАВЦЯ({winner})"
            else:
                w = str(winner)
        status = "Арбітраж завершенно".upper()
        dispute = True
    if not minutes or minutes < 0:
        minutes = -1
    text = f"дата створення: {order[9]}\n\n" \
           f"НОМЕР ЗАЯВКИ: {order[1]}\n" \
           f"ЗУСТРІЧНА ЗАЯВКА №: {order[0]}\n\n" \
           f"Сатус заявки: {status} \n\n".upper()

    if dispute:
        text += f"На користь: {w}\n\n"
    all_order = all_orders_stat(order[7])
    all_orders_done = all_orders_done_stat(order[7])
    p1 = (((all_orders_done[0] + get_seller_win(order[7])) / all_order[0]) * 100) if all_order[0] else 0
    done = p1
    user_t_process, user_t_finally = get_aver_t_user(order[7])
    text1 = f"ПРОДАВЕЦЬ: {buyer_cast}\n" \
            f"СЕР. ЧАС ВИКОНАННЯ: {user_t_process} ХВ\n" \
            f"КІЛЬКІСТЬ УГОД: {all_order[0]}/{round(done)}% ВИКОНАНО \n" \
            f"АРБІТРАЖ: {dispute_by_user(order[7])}/{dispute_winner_by_user(order[7])} ВИГРАННО \n\n" \
            f"ПОКЕР-РУМ: {sel_order[1]}\n" \
            f"СУМА ПЕРЕКАЗУ: {order[2]} {sel_order[10]} по {sel_order[3]}\n" \
            f"ВІДДАЄТЕ: {order[6]} ГРН\n\n".upper()
    text += text1
    if order[5] == "finally":
        text += f"ПІДТВЕРДІТЬ ОТРИМАННЯ: {order[2]} {sel_order[10]}\n" \
                f"ВІД EMAIL/LOGIN: {login}\n" + \
                f"ПРОТЯГОМ {round(minutes)} XB.\n\n".upper()
    text += f"КРАЙНІЙ СРОК: {order[3]}\n".upper()
    return text


def show_order_buyer_text(order, show=None):
    custom = get_custom_info(order[6])
    # all_order = all_orders_stat(order[6])
    # all_orders_done = all_orders_done_stat(order[7])
    # p1 = (((all_orders_done[0] + get_seller_win(order[7])) / all_order[0]) * 100) if all_order[0] else 0
    # done = p1
    buyer_cast = custom[1] if custom else order[6]
    buyer = order[6]
    comments = custom[3] if custom else ""
    all_order = all_orders_stat(order[6])
    all_orders_done = all_orders_done_stat(order[6])
    done_seller = round(((all_orders_done[0] + get_seller_win(order[6])) / all_order[0]) * 100) if all_order[0] else 0
    done_buyer = round(((all_orders_done[1] + get_buyer_win(order[6])) / all_order[1]) * 100) if all_order[1] else 0
    # {all_order[0]}/{round(done)}
    status = order[8]
    if status == "cansel":
        status = "ВИДАЛЕНА".upper()
    elif status == "process":
        status = "розміщенна".upper()
    elif status == "done":
        status = "закрита".upper()
    else:
        status = ""
    text = f"ДАТА: {order[7]} \n\n" \
           f"ЗАЯВКА: {order[0]} \n"
    if not show:
        text += f"СТАТУС: {status}\n"
    user_t_process, user_t_finally = get_aver_t_user(buyer)
    text += f"\nПОКУПЕЦЬ: {buyer_cast} \n" \
            f"КІЛЬКІСТЬ УГОД: {all_order[1]}/{done_buyer}% ВИКОНАНО\n" \
            f"СЕР. ЧАС ПІДТВЕРДЖЕННЯ: {user_t_finally} ХВ\n" \
            f"АРБІТРАЖ: {dispute_by_user(order[4])}/{dispute_winner_by_user(order[4])} ВИГРАННО\n\n" \
            f"КУПЛЮ: \n" \
            f"ПОКЕР-РУМ: {order[1]} \n" \
            f"СУМА: {order[2]} {order[10]} \n" \
            f"КУРС: {order[3]} ГРН \n" \
            f"МІН. ЧАСТКА: {order[4]}\n" \
            f"ТЕРМІН ПІДТВЕРДЖЕННЯ: {order[5]} ХВ. \n"
    return text


def BY_FINALLY_TEXT(time):
    return "ПОДАЮЧИ ЗАЯВКУ, Я ПРИЙМАЮ ПРАВИЛА СЕРВІСУ І ПІДТВЕРДЖУЮ ДОСТОВІРНІСТЬ ЗАЗНАЧЕНИХ ДАНИХ\n\n" \
           f"ЗОБОВ'ЯЗУЮСЬ ПІДТВЕРДИТИ ОТРИМАННЯ КОШТІВ ПРОТЯГОМ: {time} ХВ. ПІСЛЯ ОТРИМАННЯ ПЕРЕКАЗУ"


def BY_FINALLY_TEXT2(time):
    return "ПОДАЮЧИ ЗАЯВКУ, Я ПРИЙМАЮ ПРАВИЛА СЕРВІСУ І ПІДТВЕРДЖУЮ ДОСТОВІРНІСТЬ ЗАЗНАЧЕНИХ ДАНИХ\n\n" \
           f"ЗОБОВ'ЯЗУЮСЬ ПЕРЕКАЗАТИ ІГРОВУ ВАЛЮТУ ПРОТЯГОМ: {time} ХВ. ПІСЛЯ ОТРИМАННЯ ПЕРЕКАЗУ"


def text_process_admin_add(x):
    text = f"ДАТА: {x[7]}\n\n" \
           f"НОМЕР ЗАЯВКИ: {x[0]}\n\n" \
           f"ID КЛІЄНТА: {x[4]}\n" \
           f"ім'я КЛІЄНТА:  {x[6]}\n" \
           f"ПСЕВДОНІМ: @{get_name_user(x[4])[4]}\n\n" \
           f"СУМА ПОПОВНЕННЯ: {x[1]} грн\n" \
           f"ОСТАНІ 4 ЦИФРИ КАРТКИ: {x[2]}\n".upper()
    text += f"ПІБ: {x[3]}\n\n"
    if x[8] and get_promoCode(x[8]):
        bonus = round(float(x[1])/100 * get_promoCode(x[8])[4], 2)
        text += f"ПРОМОКОД: {x[8]} (+{get_promoCode(x[8])[4]}%, {bonus} грн)\n" \
                f"БУДЕ ЗАРАХОВАНО: {float(x[1]) + bonus} ГРН\n\n"
    else:
        text += f"БУДЕ ЗАРАХОВАНО: {x[1]} грн\n\n"

    return text


def text_process_admin_down(x):
    summ = x[1]
    text = f"ДАТА: {x[7]}\n\n" \
           f"НОМЕР ЗАЯВКИ: {x[0]}\n\n" \
           f"ID КЛІЄНТА: {x[4]}\n" \
           f"ім'я КЛІЄНТА:  {x[6]}\n" \
           f"ПСЕВДОНІМ: @{get_name_user(x[4])[4]}\n\n" \
           f"СУМА ВИВЕДЕННЯ:  {summ} грн\n" \
           f"номер КАРТКИ:  {x[2]}\n".upper()
    text += f"ПІБ: {x[3]}\n\n"
    if x[8] and get_promoCode(x[8]):
        promo_code = get_promoCode(x[8])
        all_tax = (summ / 100 * tax() + get_tax_grn()) - \
                  (summ / 100 * tax() + get_tax_grn()) / 100 * float(promo_code[4])
        code = f"ПРОМОКОД: {x[8]} ({promo_code[4]}%, " \
               f"{(summ / 100 * tax() + get_tax_grn()) / 100 * float(promo_code[4])} ГРН)\n" \
               f"ЗАРАХOВАНO: {summ - all_tax} ГРН\n".upper()
        text += code
    else:
        text += f"до зарахування: {round((summ - (summ / 100 * tax())) - get_tax_grn(), 2)} грн\n\n".upper()
    return text


def FAQ_text():
    work_day = datetime.now().date() - datetime.strptime("2023-05-03", "%Y-%m-%d").date()
    all_user = get_all_user()[0]
    all_user_today = get_all_user()[1]
    done_orders = get_all_orders_done()
    sum_done_orders = 0
    sum_downs = get_all_sumDown_done()
    aver_t_process, aver_t_finally = get_average_t()
    text = f"ПРо бота\n\n" \
           f"працюємо днів: {work_day.days}\n" \
           f"усього користувачів:  {all_user}\n" \
           f"нових за сьогодні: {all_user_today}\n\n" \
           f"угод проведено: {done_orders}\n\n" \
           f"СЕР. ЧАС ВИКОНАННЯ: {aver_t_process} ХВ\n" \
           f"СЕР. ЧАС ПІДТВЕРДЖЕННЯ: {aver_t_finally} ХВ\n\n" \
           f"виплаченно рефералам: {f_t(round(count_ref_money(), 2))}\n" \
           f"основні виплати: {f_t(round(sum_downs - count_ref_money(),2))} ГРН\n"
    return text.upper()


def format_approve_order_text(order: tuple, sel_order: tuple):
    status = ""
    if order[5] == "pause":
        status = "ПАУЗА"
    elif order[5] == "process":
        status = "ЧЕКАЄ ПЕРЕКАЗУ"
    elif order[5] == "waiting":
        status = "ОЧІКУВАННЯ ОПЛАТИ"
    elif order[5] == "cansel":
        status = "СКАСОВАНА"
    elif order[5] == "finally":
        status = "Очікує закриття"
    elif order[5] == "SOLD":
        status = "Закрита адміном"
    elif order[5] == "dispute":
        status = "арбітраж"
    elif order[5] == "done":
        status = "успішно завершена"
    date_time = datetime.strptime(order[3], "%d.%m.%Y, %H:%M") - datetime.now()
    date_time = date_time.total_seconds()
    minutes = divmod(date_time, 60)[0]
    if not minutes or minutes < 0:
        minutes = -1
    all_order = all_orders_stat(order[4])
    all_orders_done = all_orders_done_stat(order[4])
    p1 = (((all_orders_done[0] + get_seller_win(order[4])) / all_order[0]) * 100) if all_order[0] else 0
    done = p1
    user_t_process, user_t_finally = get_aver_t_user(order[4])
    text = f"дата створення: {order[9]}\n\n" \
           f"НОМЕР ЗАЯВКИ: {order[1]}\n" \
           f"ЗУСТРІЧНА ЗАЯВКА №: {order[0]}\n\n" \
           f"Сатус заявки: {status} \n\n" \
           f"ПОКУПЕЦЬ: {order[4]}\n" \
           f"КІЛЬКІСТЬ УГОД: {all_order[0]}/{round(done, 2)}% ВИКОНАНО \n" \
           f"СЕР. ЧАС ПІДТВЕРДЖЕННЯ: {user_t_finally} ХВ\n\n" \
           f"АРБІТРАЖ: {dispute_by_user(order[4])}/{dispute_winner_by_user(order[4])} ВИГРАННО \n\n" \
           f"ПОКЕР-РУМ: {sel_order[1]}\n" \
           f"СУМА ПЕРЕКАЗУ: {order[2]} {sel_order[10]} по {sel_order[3]}\n" \
           f"ОТРИМАЄТЕ: {order[6]} ГРН\n\n" \
           f"ЗРОБІТЬ ПЕРЕКАЗ: {order[2]} {sel_order[10]}\n"
    text = text.upper()
    text += f"НА EMAIL/LOGIN: {order[8]}\n" \
            f"ПРОТЯГОМ {round(minutes)} XB.\n\n" \
            f"КРАЙНІЙ СРОК: {order[3]}\n" \

    return text


FAQ_text_1 = questions()
CHAT_TEXT = "тут щось буде"
ADMIN_TEXT = "тут щось буде"

APPROVE_TEXT = "ВИ ПІДТВЕРДЖУЄТЕ ОТРИМАННЯ ІГРОВОЇ ВАЛЮТИ ВІД ПРОДАВЦЯ?"
APPROVE_SELLER = "ВИ ПІДТВЕРДЖУЄТЕ ПЕРЕКАЗ ІГРОВОЇ ВАЛЮТИ ПОКУПЦЮ?"
APPROVE_DELETE = "ВИ ПІДТВЕРДЖУЄТЕ ВИДАЛЕНЯ ЗАЯВКИ?"
APPROVE_ADD_SUMM = "ВИ ПІДТВЕРДЖУЄТЕ Поповнення балансу?".upper()
APPROVE_DOWN_SUMM = "ВИ ПІДТВЕРДЖУЄТЕ ВИВЕДЕННЯ коштів?".upper()
APPROVE_down_SUMM = "ВИ ПІДТВЕРДЖУЄТЕ скасування заявки виведення?".upper()
APPROVE_down_ADD = "ВИ ПІДТВЕРДЖУЄТЕ скасування заявки поповнення?".upper()
APPROVE_ORDER_CANSEL = "ВИ ПІДТВЕРДЖУЄТЕ скасування заявки?".upper()


def APPROVE_DOWN_SUMM2(order):
    return f"ВИ ПІДТВЕРДЖУЄТЕ ВИВЕДЕННЯ КОШТІВ ПО ЗАЯВЦІ №{order}?"


def text_for_admin_add(summ, cart, owner, id_user, username="", promo=""):
    text = f"нова заявка на поповнення балансу \n\n" \
           f"користувач: {id_user}\n" \
           f"ПСЕВДОНІМ: @{username}\n\n" \
           f"На суму: {summ} ГРН\n" \
           f"Останні 4 цифри карти: {cart}\n".upper()
    text += f"ІМ'Я ВЛАСНИКА: {owner}\n\n"
    if promo:
        bonus = round(float(summ)/100 * get_promoCode(promo)[4], 2)
        percent = 0
        try:
            percent = check_promoCode(promo, 'add')[0][4]
        except Exception:
            pass
        text += f"ПРОМОКОД: {promo} (+{percent}%, {bonus} ГРН)\n"
        text += f"БУДЕ ЗАРАХОВАНО {summ + bonus} ГРН\n"
    else:
        text += f"БУДЕ ЗАРАХОВАНО {summ} ГРН"
    return text


def text_for_admin_down(summ, cart, owner, id_user, username="", code=""):
    if get_promoCode(code):
        promo_code = get_promoCode(code)
        all_tax = (summ / 100 * tax() + get_tax_grn()) - \
                  (summ / 100 * tax() + get_tax_grn()) / 100 * float(promo_code[4])
        code = f"ПРОМОКОД: {code} ({promo_code[4]}%, " \
               f"{(summ / 100 * tax() + get_tax_grn()) / 100 * float(promo_code[4])} ГРН)\n" \
               f"ЗАРАХOВАНO: {summ - all_tax} ГРН\n".upper()
    else:
        amount = round((summ - (summ / 100 * tax())) - get_tax_grn(), 2)
        code = f"ДО ЗАРАХУВАННЯ: {amount} грн\n\n"
    text = f"нова заявка на виведення коштів \n\n" \
           f"користувач: {id_user}\n" \
           f"ПСЕВДОНІМ: @{username}\n\n" \
           f"сума: {summ} грн\n" \
           f"поточний баланс: {get_balance_by_id(id_user)+summ} грн\n\n" \
           f"НОМЕР КАРТИ: {cart}\n" \
           f"Ім'я власника: {owner}\n\n".upper()
    return text.upper() + code


def START_TEXT_ADMIN():
    b1 = get_balance_by_id()
    b2 = get_buyer_balance()
    if not b1:
        b1 = 0
    if not b2:
        b2 = 0
    balance = b1+b2
    text = f"ПАРТНЕРСЬКІ БАЛАНСИ: {round(get_partner_balance())} ГРН.\n" \
           f"ОСНОВНІ БАЛАНCИ: {balance} ГРН.\n\n" \
           f"ЗАЯВКИ НА ПОПОВНЕННЯ: {len(get_all_balance_add())}\n" \
           f"ЗАЯВКИ НА ВИВЕДЕННЯ: {len(get_all_balance_down())}\n" \
           f"ПЕРЕВІРКА ЗАЯВОК: {len(valid_order())}\n" \
           f"АРБАТРАЖ: {len(dispute_orders())}\n".upper()
    return text


NO_MAIL = "ви не вказали e-mail/login"


def order_by_text(x):
    text = f"ЗА ВАШОЮ ЗАЯВКОЮ №{x[0]} З'ЯВИЛАСЯ ЗУСТРІЧНА ЗАЯВКА\n\n" \
           f"ЗРОБІТЬ ПЕРЕКАЗ ПО РЕКВІЗИТАМ ПОКУПЦЯ ПРОТЯГОМ {x[5]} ХВ.\n\n" \
           f"ЩОБ ЇЇ ПЕРЕГЛЯНУТИ ПЕРЕЙДІТЬ В ОСОБИСТИЙ КАБІНЕТ -> МОЇ ЗАЯВКИ -> ЯК ПРОДАВЕЦЬ\n".upper()
    # text += show_all_orders_text(x[7], x[0], x[6], x[1], x[2], x[3], x[4], x[5])
    # text += "\n\nПідтвердити заявку можна в особистому кабинеті".upper()
    return text


help_sum = "введіть суму поповнення балансу в грн."
help_4num = "введіть останні 4 цифри номеру власника картки"
help_16num = "введіть 16 цифр номеру картки"
help_owner = "введіть ПІБ власника картки"
help_poker_room = "виберіть покер-рум"
help_by_usd = "введіть кількість USD яку ви хочете придбати"
help_login = "вкажіть e-mail або login для переказу в залежності від покер-руму"
help_sum_usd = "вкажіть суму яку бажаєте вивести"
help_rate = "вкажіть курс за яким бажаєте вивести"
help_min_part = "вкажіть мінімальну частку для викупу у "
help_term = "вкажіть максимальний термін виконання ваших забов'язань по цій заявці"
help_status = "фільтр по статусам заявки"
help_currency = "фільтр валюті заявки"
help_promo = "введіть промокод при наявності"
help_notification_sell = "Сповіщення про нові заявки продажу на вітрині"
help_notification_buy = "Сповіщення про нові заявки покупки на вітрині"

card = get_cart()

no_orders = "3явок немає"
alon_order = "Це єдина заявка"

EDIT_TEXT = "Оновив заявки.\nВи можете перевірити зміни на вітрині або у особистому кабінеті".upper()

plug = "-----"


def referral_text(user):
    text = "РЕФЕРАЛЬНА СИСТЕМА\n\n" \
           "ЩОБ ПАСИВНО КАПАЛИ ГРОШІ НА БАЛАНС, БАГАТО ЧОГО РОБИТИ НЕ ПОТРІБНО. " \
           "КЛИЧ СВОЇХ ДРУЗІВ І ОТРИМУЙ З НИХ МОНЕТКУ\n\n" \
           f"У ВАС: {count_my_ref(user)} РЕФЕРАЛІВ\n" \
           f"ВЖЕ ЗАРОБЛЕНО: {count_my_ref_money(user)} ГРН\n\n" \
           f"ПОСИЛАННЯ ДЛЯ ЗАПРОШЕННЯ: `{get_referral_link(user)}`\n\n" \
           f"ВИ ОТРИМУЄТЕ {get_ref_tax()}% ВІД РЕФЕРАЛІВ З УГОД НА ВИВЕДЕННЯ НА БАЛАНС БОТА."

    return text


def convert_balance_text(user):
    text = f"зараз ваш партнерський баланс становить {get_partner_balance(user)} ГРН. \n\n" \
           "бажаєете перевести усі кошти на основний баланс?"
    return text.upper()


def promo_text():
    stat = count_promoCodes()
    text = f"Всього створенно промокодів: {stat[0]}\n\n" \
                 f"використано: {stat[1]}\n" \
                 f"Активні: {stat[2]}\n".upper()
    return text

link_but = "https://docs.google.com/document/d/1J8Iw62pXKhxhVe61XLCe8d3YjBmQyZKFxnzvl2dRcRg/edit?usp=sharing"
link_help = "https://youtu.be/gWUcbytY5Cc"
often_q = "https://docs.google.com/document/d/1J8Iw62pXKhxhVe61XLCe8d3YjBmQyZKFxnzvl2dRcRg/edit?usp=sharing"


def text_profile(user):
    text = " "
    data = get_custom_info(user)
    if data:
        if data[2] == "ON":
            signal = "УВІМКНЕНО"
        else:
            signal = "ВИМКНЕННО"
        if data[3] == "ON":
            signal2 = "УВІМКНЕНО"
        else:
            signal2 = "ВИМКНЕННО"
        text = "ВАШІ ДАНІ\n\n" \
               f"НІКНЄЙМ: {data[1]}\n" \
               f"КОМЕНТАР:  {data[4]}\n" \
               f"СПОВІЩЕННЯ ПРОДАЖ: {signal}\n" \
               f"СПОВІЩЕННЯ ПОКУПКА: {signal2}\n"
    else:
        text = "ВАШІ ДАНІ\n\n" \
               f"НІКНЄЙМ: {user}\n" \
               f"КОМЕНТАР: \n" \
               f"СПОВІЩЕННЯ ПРОДАЖ: УВІМКНЕНО\n" \
               f"СПОВІЩЕННЯ ПОКУПКА: УВІМКНЕНО\n"
    return text


text_profile_name = "Введіть новий нікнейм".upper()
text_profile_comm = "Введіть свій комент".upper()
