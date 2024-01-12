from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from text import RULES_LINK, FAQ_text_1
from database import switch_check, admins, get_custom_info

PRIVET_ROOM_BUT = InlineKeyboardButton(text="Особистий кабінет".upper(), callback_data="PRIVET_ROOM_BUT")
ADD_BUT = InlineKeyboardButton(text="ПОПОВНИТИ БОТ".upper(), callback_data="ADD_BUT")
DOWN_BUT = InlineKeyboardButton(text="ВИВЕСТИ З БОТА".upper(), callback_data="DOWN_BUT")
CONVERT_BUT = InlineKeyboardButton(text="Конвертувати".upper(), callback_data="CONVERT_BUT")
ALL_ORDER_BUT = InlineKeyboardButton(text=" ВІТРИНА ЗАЯВОК".upper(), callback_data="ALL_ORDER_BUT")
MY_ORDER_BUT = InlineKeyboardButton(text="Мої заявки".upper(), callback_data="MY_ORDER_BUT")
CREATE_ORDER_BUT = InlineKeyboardButton(text="Створити заявку".upper(), callback_data="CREATE_ORDER_BUT")
REFERRAL_BUT = InlineKeyboardButton(text="ПАРТНЕРКА".upper(), callback_data="REFERRAL_BUT")
ABOUT_BOT_BUT = InlineKeyboardButton(text="ПРО БОТА".upper(), callback_data="ABOUT_BOT_BUT")
LS_KASA = InlineKeyboardButton(text="КАСА".upper(), callback_data="LS_KASA")
CREATE_ORDER_SELL = InlineKeyboardButton(text="ПРОДАТИ".upper(), callback_data="CREATE_ORDER_SELL")
CREATE_ORDER_BUY = InlineKeyboardButton(text="КУПИТИ".upper(), callback_data="CREATE_ORDER_BUY")

ADD_BUT_STEP2 = InlineKeyboardButton(text="Подати заявку".upper(), callback_data="ADD_BUT_STEP2")
CHOOSE_ORDER = InlineKeyboardButton(text="обрати заявку".upper(), callback_data="ADD_BUT_STEP2")
CHOOSE_ORDER2 = InlineKeyboardButton(text="КУпити".upper(), callback_data="ADD_BUT_STEP2")
ADD_BUT_CANSEL = InlineKeyboardButton(text="НАЗАД".upper(), callback_data="ADD_BUT_CANSEL")
CANSEL_ALL_ORDERS = InlineKeyboardButton(text="НАЗАД".upper(), callback_data="CANSEL_ALL_ORDERS")
CANSEL_ALL_GET_ORDER = InlineKeyboardButton(text="НАЗАД".upper(), callback_data="CANSEL_ALL_GET_ORDER")
CANSEL_MY_ORDER = InlineKeyboardButton(text="НАЗАД".upper(), callback_data="CANSEL_MY_ORDER")
CANSEL_LS = InlineKeyboardButton(text="ОСОБИСТИЙ КАБІНЕТ".upper(), callback_data="ADD_BUT_CANSEL")
ADD_BUT_CANSEL_APPROVE_ADD = InlineKeyboardButton(text="НАЗАД".upper(), callback_data="ADD_BUT_CANSEL_APPROVE_ADD")
ADD_BUT_APPROVE = InlineKeyboardButton(text="Підтвердити".upper(), callback_data="ADD_BUT_APPROVE")
ADD_BUT_DONE = InlineKeyboardButton(text="Підтвердити".upper(), callback_data="ADD_BUT_DONE")
ADD_BUT_DONE2 = InlineKeyboardButton(text="Готово".upper(), callback_data="ADD_BUT_DONE")
ADD_BUT_RULES = InlineKeyboardButton(text="Правила сервісу".upper(), url=RULES_LINK)
ADD_BUT_RULES0 = InlineKeyboardButton(text="❌", callback_data="ADD_BUT_RULES0")
ADD_BUT_RULES1 = InlineKeyboardButton(text="✅", callback_data="ADD_BUT_RULES1")
ADD_BUT_SUMM = InlineKeyboardButton(text="Сумма грн".upper(), callback_data="ADD_BUT_SUMM")
ADD_BUT_SUMM2 = InlineKeyboardButton(text="1000", callback_data="ADD_BUT_SUMM2")
ADD_BUT_LAST4NUM = InlineKeyboardButton(text="Останні 4 цифри".upper(), callback_data="ADD_BUT_LAST4NUM")
ADD_BUT_LAST4NUM2 = InlineKeyboardButton(text="XXXX XXXX XXXX XXXX", callback_data="ADD_BUT_LAST4NUM2")
ADD_BUT_OWNER = InlineKeyboardButton(text="Власник карти".upper(), callback_data="ADD_BUT_OWNER")
ADD_BUT_OWNER2 = InlineKeyboardButton(text="Вкажіть власника".upper(), callback_data="ADD_BUT_OWNER2")
PROMO_CODE_INFO = InlineKeyboardButton(text="ПРомокод".upper(), callback_data="PROMO_CODE_INFO")

PROFILE = InlineKeyboardButton(text="Профіль".upper(), callback_data="PROFILE")
PROFILE_NAME = InlineKeyboardButton(text="Змінити НІК".upper(), callback_data="PROFILE_NAME")
PROFILE_COMMENT = InlineKeyboardButton(text="Змінити комент".upper(), callback_data="PROFILE_COMMENT")
PROFILE_SIGNAL1_INFO = InlineKeyboardButton(text="СПОВІЩЕННЯ ПРОДАЖ".upper(), callback_data="PROFILE_SIGNAL_INFO")
PROFILE_SIGNAL2_INFO = InlineKeyboardButton(text="СПОВІЩЕННЯ ПОКУПКА".upper(), callback_data="PROFILE_SIGNAL_INFO")
PROFILE_SIGNAL_ON = InlineKeyboardButton(text="УВІМКНУТИ".upper(), callback_data="PROFILE_SIGNAL_ON")
PROFILE_SIGNAL_OFF = InlineKeyboardButton(text="ВИМКНУТИ".upper(), callback_data="PROFILE_SIGNAL_OFF")
PROFILE_SIGNAL_ON2 = InlineKeyboardButton(text="УВІМКНУТИ".upper(), callback_data="PROFILE_SIGNAL_ON2")
PROFILE_SIGNAL_OFF2 = InlineKeyboardButton(text="ВИМКНУТИ".upper(), callback_data="PROFILE_SIGNAL_OFF2")


LIST_POKE_ROOMS_BUT = [InlineKeyboardButton(text="GGPOKER".upper(), callback_data="CR_ROOMS2"),
                       InlineKeyboardButton(text="POKERSTARS".upper(), callback_data="CR_ROOMS2"),
                       InlineKeyboardButton(text="POKERKING".upper(), callback_data="CR_ROOMS2"),
                       InlineKeyboardButton(text="ACR".upper(), callback_data="CR_ROOMS2"),
                       InlineKeyboardButton(text="888POKER".upper(), callback_data="CR_ROOMS2"),
                       InlineKeyboardButton(text="REDSTAR".upper(), callback_data="CR_ROOMS2"),
                       InlineKeyboardButton(text="POKERMATCH".upper(), callback_data="CR_ROOMS2")]

LIST_POKER_ROOMS_BUT2 = [InlineKeyboardButton(text="ВСІ РУМИ".upper(), callback_data="ROOMS"),
                         InlineKeyboardButton(text="GGPOKER".upper(), callback_data="ROOMS"),
                         InlineKeyboardButton(text="POKERSTARS".upper(), callback_data="ROOMS"),
                         InlineKeyboardButton(text="POKERKING".upper(), callback_data="ROOMS"),
                         InlineKeyboardButton(text="ACR".upper(), callback_data="ROOMS"),
                         InlineKeyboardButton(text="888POKER".upper(), callback_data="ROOMS"),
                         InlineKeyboardButton(text="REDSTAR".upper(), callback_data="ROOMS"),
                         InlineKeyboardButton(text="POKERMATCH".upper(), callback_data="ROOMS")]

LIST_STATUS_BAYER = [InlineKeyboardButton(text="ВСІ ЗАЯВКИ".upper(), callback_data="ALL"),
                     InlineKeyboardButton(text="розміщенна".upper(), callback_data="buy_order"),
                     InlineKeyboardButton(text="ПРОСРОЧЕНА".upper(), callback_data="cansel"),
                     InlineKeyboardButton(text="ВИКОНАНА".upper(), callback_data="done"),
                     InlineKeyboardButton(text="АРБІТРАЖ".upper(), callback_data="dispute"),
                     InlineKeyboardButton(text="АРБІТРАЖ завершенно ".upper(), callback_data="SOLD"),
                     InlineKeyboardButton(text="ОЧІКУЄМО ПЕРЕКАЗ".upper(), callback_data="process")]

LIST_POKE_CURRENCY = [InlineKeyboardButton(text="USD".upper(), callback_data="currency"),
                      InlineKeyboardButton(text="UAH".upper(), callback_data="currency"),
                      InlineKeyboardButton(text="EUR".upper(), callback_data="currency"),
                      InlineKeyboardButton(text="C$".upper(), callback_data="currency"),
                      InlineKeyboardButton(text="T$".upper(), callback_data="currency")]

CR_CANSEL = InlineKeyboardButton(text="НАЗАД".upper(), callback_data="CR_CANSEL")


def CREATE_BUTTS(value, RATE, MIN_PART, TERM, kind_numb, login, currency, editing=False, kind=""):
    keyboard = InlineKeyboardMarkup(row_width=2)
    CR_ROOMS = InlineKeyboardButton(text="ПОКЕР-РУМ".upper(), callback_data="CR_ROOMS")
    CR_SUMM_USD = InlineKeyboardButton(text=f"СУМА {LIST_POKE_CURRENCY[currency].text}".upper(),
                                       callback_data="CR_SUMM_USD")
    CR_SUMM_USD2 = InlineKeyboardButton(text=f"{value}".upper(), callback_data="CR_SUMM_USD2")
    CR_RATE_GRN = InlineKeyboardButton(text="КУРС ГРН".upper(), callback_data="CR_RATE_GRN")
    CR_RATE_GRN2 = InlineKeyboardButton(text=f"{RATE}".upper(), callback_data="CR_RATE_GRN2")
    CR_MIN_PART = InlineKeyboardButton(text="МІН. ЧАСТКА".upper(), callback_data="CR_MIN_PART")
    CR_MIN_PART2 = InlineKeyboardButton(text=f"{MIN_PART}".upper(), callback_data="CR_MIN_PART2")
    CR_TERM = InlineKeyboardButton(text="ТЕРМІН ВИКОНАННЯ ХВ.".upper(), callback_data="CR_TERM")
    CR_TERM1 = InlineKeyboardButton(text="ТЕРМІН ПІДТВЕРДЖЕННЯ ХВ.".upper(), callback_data="CR_TERM")
    CR_TERM2 = InlineKeyboardButton(text=f"{TERM}".upper(), callback_data="CR_TERM2")
    CR_GET_ORDER = InlineKeyboardButton(text="ПОДАТИ ЗАЯВКУ".upper(), callback_data="CR_GET_ORDER")
    EDIT_ORDER_FINAL = InlineKeyboardButton(text="ЗБЕРЕГТИ ЗМІНИ".upper(), callback_data="CR_GET_ORDER")
    CR_GET_LOGIN = InlineKeyboardButton(text="E-MAIL/LOGIN".upper(), callback_data="CR_GET_LOGIN")
    CR_GET_LOGIN2 = InlineKeyboardButton(text=login, callback_data="CR_GET_LOGIN2")
    CR_GET_currency = InlineKeyboardButton(text="ВАЛЮТА", callback_data="CR_GET_currency")
    if kind == "buy":
        CR_TERM = CR_TERM1
    keyboard.add(CR_ROOMS, LIST_POKE_ROOMS_BUT[kind_numb],
                 CR_GET_LOGIN, CR_GET_LOGIN2,
                 CR_GET_currency, LIST_POKE_CURRENCY[currency],
                 CR_SUMM_USD, CR_SUMM_USD2,
                 CR_RATE_GRN, CR_RATE_GRN2,
                 CR_MIN_PART, CR_MIN_PART2,
                 CR_TERM, CR_TERM2, CR_CANSEL, )
    if editing:
        keyboard.insert(EDIT_ORDER_FINAL)
    else:
        keyboard.insert(CR_GET_ORDER)
    return keyboard


def ADD_BUTTS(amount, card, owner, promo="вкажіть промокод"):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(ADD_BUT_SUMM, InlineKeyboardButton(text=f"{amount}", callback_data="ADD_BUT_SUMM2"), ADD_BUT_LAST4NUM,
                 InlineKeyboardButton(text=f"XXXX XXXX XXXX {card}", callback_data="ADD_BUT_LAST4NUM2"),
                 ADD_BUT_OWNER, InlineKeyboardButton(text=f"{owner}", callback_data="ADD_BUT_OWNER2"), PROMO_CODE_INFO,
                 InlineKeyboardButton(text=f"{promo}", callback_data="PROMO_CODE"), ADD_BUT_CANSEL, ADD_BUT_STEP2)
    return keyboard


DOWN_BUT_LAST4NUM = InlineKeyboardButton(text="НОМЕР КАРТКИ", callback_data="DOWN_BUT_LAST4NUM")


def DOWN_BUTTS(amount, card, owner, promo="вкажіть промокод"):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(ADD_BUT_SUMM, InlineKeyboardButton(text=f"{amount}", callback_data="ADD_BUT_SUMM2"),
                 DOWN_BUT_LAST4NUM, InlineKeyboardButton(text=f"{card}", callback_data="DOWN_BUT_LAST4NUM2"),
                 ADD_BUT_OWNER, InlineKeyboardButton(text=f"{owner}", callback_data="ADD_BUT_OWNER2"), PROMO_CODE_INFO,
                 InlineKeyboardButton(text=f"{promo}", callback_data="PROMO_CODE"), ADD_BUT_CANSEL, ADD_BUT_STEP2)
    return keyboard


def LS_BUTTONS(id_user):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(ALL_ORDER_BUT, CREATE_ORDER_BUT, MY_ORDER_BUT, LS_KASA, REFERRAL_BUT, PROFILE, ABOUT_BOT_BUT)
    if id_user in admins():
        keyboard.add(InlineKeyboardButton(text="АДМІНКА", callback_data="ADMIN"))
    return keyboard


START_ALL_ORDERS = InlineKeyboardButton(text=f"ДАЛІ".upper(), callback_data="NEXT")
ALL_ORDERS_MORE = InlineKeyboardButton(text=f"БІЛЬШЕ".upper(), callback_data="MORE")
ALL_ORDERS_CHANGE = InlineKeyboardButton(text=f"БІЛЬШЕ".upper(), callback_data="MORE")
ARROW_LEFT = InlineKeyboardButton(text="ВЛІВО".upper(), callback_data="ARROW_LEFT")
ARROW_RIGHT = InlineKeyboardButton(text="ВПРАВО".upper(), callback_data="ARROW_RIGHT")
GET_ORDER = InlineKeyboardButton(text="ОБРАТИ ЗАЯВКУ".upper(), callback_data="GET_ORDER")
ROOM_FILTER = InlineKeyboardButton(text="ПОКЕР-РУМ".upper(), callback_data="ROOM_FILTER")


def ALL_ORDERS_CHOOSE(number):
    keyboard = InlineKeyboardButton(text=f"ОБРАТИ".upper(), callback_data=f"GET_ORDER_{number}")
    return keyboard


def BY_ORDER_FINAL(number, mail, currency="USD"):
    keyboard = InlineKeyboardMarkup(row_width=2)
    BY_ORDER_FINAL = InlineKeyboardButton(text=f"КУПИТИ {currency}".upper(), callback_data="BY_ORDER_FINAL")
    BY_ORDER_FINAL2 = InlineKeyboardButton(text=f"{number}".upper(), callback_data="BY_ORDER_FINAL2")
    BY_ORDER_MAIL = InlineKeyboardButton(text="E-MAIL/LOGIN".upper(), callback_data="BY_ORDER_MAIL")
    BY_ORDER_MAIL2 = InlineKeyboardButton(text=f"{mail}", callback_data="BY_ORDER_MAIL2")
    BY_ORDER_GET_ORDER = InlineKeyboardButton(text="КУпити".upper(), callback_data="BY_ORDER_GET_ORDER")
    keyboard.add(BY_ORDER_FINAL, BY_ORDER_FINAL2, BY_ORDER_MAIL, BY_ORDER_MAIL2, CANSEL_ALL_ORDERS, BY_ORDER_GET_ORDER)
    return keyboard


def BY_ORDER_FINAL_SELL(number, mail, currency="USD"):
    keyboard = InlineKeyboardMarkup(row_width=2)
    BY_ORDER_FINAL = InlineKeyboardButton(text=f"ПРОДАТИ {currency}".upper(), callback_data="BY_ORDER_FINAL")
    BY_ORDER_FINAL2 = InlineKeyboardButton(text=f"{number}".upper(), callback_data="BY_ORDER_FINAL2")
    BY_ORDER_MAIL = InlineKeyboardButton(text="E-MAIL/LOGIN".upper(), callback_data="BY_ORDER_MAIL")
    BY_ORDER_MAIL2 = InlineKeyboardButton(text=f"{mail}", callback_data="BY_ORDER_MAIL2")
    BY_ORDER_GET_ORDER = InlineKeyboardButton(text="ПРОДАТИ".upper(), callback_data="BY_ORDER_GET_ORDER")
    keyboard.add(BY_ORDER_FINAL, BY_ORDER_FINAL2, BY_ORDER_MAIL, BY_ORDER_MAIL2, CANSEL_ALL_ORDERS, BY_ORDER_GET_ORDER)
    return keyboard


ADMIN_BUT_APPROVE = InlineKeyboardButton(text="Підтвердити".upper(), callback_data="ADMIN_BUT_APPROVE")
ADMIN_BUT_CANSEL = InlineKeyboardButton(text="СКАСУВАТИ".upper(), callback_data="ADMIN_BUT_CANSEL")


def promo_buttons(kind="add", amount=1, term=1, discount=0):
    keyboard = InlineKeyboardMarkup(row_width=2)
    TYPE_INFO = InlineKeyboardButton(text="ПРОМО ДЛЯ:".upper(), callback_data="TYPE_INFO")
    AMOUNT_INFO = InlineKeyboardButton(text="КІЛЬКІСТЬ".upper(), callback_data="AMOUNT_INFO")
    PROMO_ADD = InlineKeyboardButton(text="НА ПОПОВНЕННЯ".upper(), callback_data="PROMO_ADD")
    PROMO_DOWN = InlineKeyboardButton(text="НА ВИВЕДЕННЯ".upper(), callback_data="PROMO_DOWN")
    PROMO_AMOUNT = InlineKeyboardButton(text=f"{amount}", callback_data="PROMO_AMOUNT")
    TERM_INFO = InlineKeyboardButton(text="Термін дії".upper(), callback_data="TERM_INFO")
    PROMO_TERM = InlineKeyboardButton(text=f"{term}", callback_data="PROMO_TERM")
    DISCOUNT_INFO = InlineKeyboardButton(text=f"БОНУС %".upper(), callback_data="DISCOUNT_INFO")
    DISCOUNT_INFO_DOWN = InlineKeyboardButton(text=f"ЗНИЖКА %".upper(), callback_data="DISCOUNT_INFO_DOWN")
    PROMO_DISCOUNT = InlineKeyboardButton(text=f"{discount}", callback_data="PROMO_DISCOUNT")
    keyboard.add(TYPE_INFO)
    if kind == "add":
        keyboard.insert(PROMO_ADD)
        keyboard.add(AMOUNT_INFO, PROMO_AMOUNT, TERM_INFO, PROMO_TERM, DISCOUNT_INFO, PROMO_DISCOUNT)
    elif kind == "down":
        keyboard.insert(PROMO_DOWN)
        keyboard.add(AMOUNT_INFO, PROMO_AMOUNT, TERM_INFO, PROMO_TERM, DISCOUNT_INFO_DOWN, PROMO_DISCOUNT)
    keyboard.add(CR_CANSEL, ADD_BUT_APPROVE)

    return keyboard


def admin_but():
    keyboard = InlineKeyboardMarkup(row_width=2)
    ADMIN_BUT_ALL_ADD = InlineKeyboardButton(text="ЗАЯВКИ НА ПОПОВНЕННЯ".upper(), callback_data="ADMIN_BUT_ALL_ADD")
    ADMIN_BUT_ALL_DOWN = InlineKeyboardButton(text="ЗАЯВКИ НА ВИВЕДЕННЯ".upper(), callback_data="ADMIN_BUT_ALL_DOWN")
    ADMIN_BUT_MEMBERS = InlineKeyboardButton(text="УЧАСНИКИ".upper(), callback_data="ADMIN_BUT_MEMBERS")
    ADMIN_BUT_SEND = InlineKeyboardButton(text="РОзсилка".upper(), callback_data="ADMIN_BUT_SEND")
    ADMIN_BUT_DOWNLOAD = InlineKeyboardButton(text="Вигрузити інфо".upper(), callback_data="ADMIN_BUT_DOWNLOAD")
    ON = InlineKeyboardButton(text="увімкнути бот".upper(), callback_data="ON")
    OFF = InlineKeyboardButton(text="ВИМКНУТИ БОТ".upper(), callback_data="OFF")
    # CHANGE_ADMIN = InlineKeyboardButton(text="ЗМІНИТИ АДМІНА".upper(), callback_data="CHANGE_ADMIN")
    DISPUTE_ADMIN = InlineKeyboardButton(text="АРБІТРАЖ".upper(), callback_data="DISPUTE_ADMIN")
    VALID_ADMIN = InlineKeyboardButton(text="перевірка заявок".upper(), callback_data="VALID_ADMIN")
    PROMO_ADMIN = InlineKeyboardButton(text="ПРОМОКОД".upper(), callback_data="PROMO_ADMIN")
    keyboard.add(ADMIN_BUT_ALL_ADD, ADMIN_BUT_ALL_DOWN, ADMIN_BUT_SEND, VALID_ADMIN, ADMIN_BUT_DOWNLOAD, DISPUTE_ADMIN,
                 ADMIN_BUT_MEMBERS)
    if switch_check():
        keyboard.insert(OFF)
    else:
        keyboard.insert(ON)
    keyboard.add(PROMO_ADMIN, CR_CANSEL)
    return keyboard


SELLER_BUT = InlineKeyboardButton(text="ПРОДАВЕЦЬ".upper(), callback_data="SELLER_BUT")
BUYER_BUT = InlineKeyboardButton(text="ПОКУПЕЦЬ".upper(), callback_data="BUYER_BUT")

FAQ_BUT = InlineKeyboardButton(text="ЧАСТІ ПИТАННЯ".upper(), url=FAQ_text_1)
CHAT_BUT = InlineKeyboardButton(text="ЧАТ".upper(), callback_data="CHAT_BUT")
ADMIN_CHAT_BUT = InlineKeyboardButton(text="АДМІНІСТРАТОР".upper(), callback_data="ADMIN_CHAT_BUT")
ACTIVE_ORDER_BUT = InlineKeyboardButton(text="АКТИВУВАТИ".upper(), callback_data="ACTIVE_ORDER_BUT")

STATUS_FILTER_BUT = InlineKeyboardButton(text="СТАТУС ЗАЯВКИ".upper(), callback_data="STATUS_FILTER_BUT")
APPROVE_ORDER_BUT = InlineKeyboardButton(text="підтверджую переказ".upper(), callback_data="APPROVE_ORDER_BUT")

LIST_STATUS_SELLER_BUT = [InlineKeyboardButton(text="Всі ЗАЯВКИ".upper(), callback_data="ALL"),
                          InlineKeyboardButton(text="арбіртаж".upper(), callback_data="dispute"),
                          InlineKeyboardButton(text="ЧЕКАЄ ПЕРЕКАЗУ".upper(), callback_data="sold"),
                          InlineKeyboardButton(text="ОЧІКУЄ ПІДТВЕРДЖЕННЯ".upper(), callback_data="finally"),
                          InlineKeyboardButton(text="очікую оплати".upper(), callback_data="waiting"),
                          InlineKeyboardButton(text="РОЗМІЩЕНА".upper(), callback_data="process"),
                          InlineKeyboardButton(text="ЧЕРНЕТКА".upper(), callback_data="pause"),
                          InlineKeyboardButton(text="завершені".upper(), callback_data="done"),
                          InlineKeyboardButton(text="скасована".upper(), callback_data="cansel"), ]

APPROVE_YES = InlineKeyboardButton(text="ТАК".upper(), callback_data="APPROVE_YES")
APPROVE_NO = InlineKeyboardButton(text="НІ".upper(), callback_data="APPROVE_NO")


def send_but(text, link):
    keyboard = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text=text.upper(), url=link))
    return keyboard


change_admin2 = InlineKeyboardButton(text="змінити".upper(), callback_data="change_admin2")
close_dispute = InlineKeyboardButton(text="Закрити".upper(), callback_data="close_dispute")

LOG_INFO = InlineKeyboardButton(text="Логи".upper(), callback_data="LOG_INFO")
ORDER_INFO = InlineKeyboardButton(text="ЗАЯВКИ".upper(), callback_data="ORDER_INFO")
USER_INFO = InlineKeyboardButton(text=f"КОРИСТУВАЧІ ", callback_data="USER_INFO")
EDIT_ORDER = InlineKeyboardButton(text="РЕДАГУВАТИ".upper(), callback_data="EDIT_ORDER")

SEND_MSG = InlineKeyboardButton(text="повідомлення".upper(), callback_data="SEND_MSG")
CHANGE_BALANCE = InlineKeyboardButton(text="ЗМІНИТИ БАЛАНС".upper(), callback_data="ADM_CHANGE_BALANCE")
BAN = InlineKeyboardButton(text="забанити".upper(), callback_data="BAN")
UNBAN = InlineKeyboardButton(text="розбанити".upper(), callback_data="UNBAN")
MY_BALANCE = InlineKeyboardButton(text="Баланс".upper(), callback_data="MY_BALANCE")

LIST_STATUS_BALANCE = [InlineKeyboardButton(text="Всі".upper(), callback_data="ALL"),
                       InlineKeyboardButton(text="Поповнення".upper(), callback_data="add"),
                       InlineKeyboardButton(text="Виведення".upper(), callback_data="down")]

my_order_stop = InlineKeyboardButton(text="призупинити".upper(), callback_data="my_order_stop")

CREATE_PROMO = InlineKeyboardButton(text="створити".upper(), callback_data="CREATE_PROMO")
PROMO_INFO = InlineKeyboardButton(text="вигрузити інфо".upper(), callback_data="PROMO_INFO")

PROMO_CANSEL = InlineKeyboardButton(text="НАЗАД".upper(), callback_data="PROMO_CANSEL")
ORDER_CANSEL = InlineKeyboardButton(text="Скасувати".upper(), callback_data="ORDER_CANSEL")


def profile_buttons(user):
    keyboard = InlineKeyboardMarkup(row_width=2)
    info = get_custom_info(user)
    signal_status1 = PROFILE_SIGNAL_ON
    signal_status2 = PROFILE_SIGNAL_ON2
    if info:
        if info[2] == "ON":
            signal_status1 = PROFILE_SIGNAL_OFF
        if info[3] == "ON":
            signal_status2 = PROFILE_SIGNAL_OFF2
    keyboard.add(PROFILE_NAME, PROFILE_COMMENT, PROFILE_SIGNAL1_INFO, signal_status1, PROFILE_SIGNAL2_INFO,
                 signal_status2, CANSEL_LS)
    return keyboard

BUY = InlineKeyboardButton(text="КУПИТИ".upper(), callback_data="BUY")
SELL = InlineKeyboardButton(text="ПРОДАТИ".upper(), callback_data="SELL")
BUY_lower = InlineKeyboardButton(text="КУПИТИ".lower(), callback_data="BUY")
SELL_lower = InlineKeyboardButton(text="ПРОДАТИ".lower(), callback_data="SELL")

