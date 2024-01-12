from database import *


def LS_TEXT(id_user):
    add = get_all_adds(id_user)
    down = get_all_downs(id_user)
    partner_balance = get_partner_balance(id_user)
    all_order = all_orders_stat(id_user)
    all_orders_done = all_orders_done_stat(id_user)
    done_seller = round(((all_orders_done[0] + get_seller_win(id_user)) / all_order[0]) * 100) if all_order[0] else 0
    done_buyer = round(((all_orders_done[1] + get_buyer_win(id_user)) / all_order[1]) * 100) if all_order[1] else 0
    user_t_process, user_t_finally = get_aver_t_user(id_user)
    text = "Особистий кабінет\n\n" \
           f"Мій ID: {id_user}\n" \
           f"Мобільний телефон: +{get_phone_by_id(id_user)}\n\n" \
           f"Партнерський баланс: {partner_balance} ГРН.\n" \
           f"Основний баланc: {get_balance_by_id(id_user)} ГРН.\n\n" \
           f"Поповнення: {add[0]} на суму {add[1]} ГРН.\n" \
           f"Виведення: {down[0]} на суму {down[1]} ГРН.\n\n" \
           f"Кількість угод: {all_order[0] + all_order[1]}\n" \
           f"Як продавець: {all_order[0]}/{done_seller}% ВИКОНАНО\n" \
           f"СЕР. ЧАС ВИКОНАННЯ: {user_t_process} ХВ\n" \
           f"Як покупець: {all_order[1]}/{done_buyer}% ВИКОНАНО\n" \
           f"СЕР. ЧАС ПІДТВЕРДЖЕННЯ: {user_t_finally} ХВ\n\n" \
           f"Арбітраж: {dispute_by_user(id_user)}/{dispute_winner_by_user(id_user)} ВИГРАННО \n\n" \
           f"Активні заявки: {get_count_buyer_by_id(id_user) + get_count_orders_by_id(id_user)}\n" \
           f"На купівл: {get_count_buyer_by_id(id_user)}\n" \
           f"На Продаж: {get_count_orders_by_id(id_user)}\n" \
           f"ЗУСТРІЧНІ ЗАЯВКИ: {get_count_all_buyer_by_id(id_user)}"

    return text.upper()


def MEMBERS(id_user):
    add = get_all_adds(id_user)
    down = get_all_downs(id_user)
    partner_balance = get_partner_balance(id_user)
    all_order = all_orders_stat(id_user)
    all_orders_done = all_orders_done_stat(id_user)
    done_seller = round(((all_orders_done[0] + get_seller_win(id_user)) / all_order[0]) * 100) if all_order[0] else 0
    done_buyer = round(((all_orders_done[1] + get_buyer_win(id_user)) / all_order[1]) * 100) if all_order[1] else 0
    user_t_process, user_t_finally = get_aver_t_user(id_user)

    text = f"ID КОРИСТУВАЧА: {id_user}\n" \
           f"ІМ'Я: {get_name_user(id_user)[1]}\n" \
           f"ПСЕВДОНІМ: @{get_name_user(id_user)[4]}\n" \
           f"Мобільний телефон: +{get_phone_by_id(id_user)}\n\n" \
           f"Партнерський баланс: {partner_balance} ГРН.\n" \
           f"Основний баланc: {get_balance_by_id(id_user)} ГРН.\n\n" \
           f"Поповнення: {add[0]} на суму {add[1]} ГРН.\n" \
           f"Виведення: {down[0]} на суму {down[1]} ГРН.\n\n" \
           f"Кількість угод: {all_order[0] + all_order[1]}\n" \
           f"Як продавець: {all_order[0]}/{done_seller}% ВИКОНАНО\n" \
           f"СЕР. ЧАС ВИКОНАННЯ: {user_t_process} ХВ\n" \
           f"Як покупець: {all_order[1]}/{done_buyer}% ВИКОНАНО\n" \
           f"СЕР. ЧАС ПІДТВЕРДЖЕННЯ: {user_t_finally} ХВ\n\n" \
           f"Арбітраж: {dispute_by_user(id_user)}/{dispute_winner_by_user(id_user)} ВИГРАННО \n\n" \
           f"Активні заявки: {get_count_buyer_by_id(id_user) + get_count_orders_by_id(id_user)}\n" \
           f"На купівл: {get_count_buyer_by_id(id_user)}\n" \
           f"На Продаж: {get_count_orders_by_id(id_user)}\n"

    return text.upper()


