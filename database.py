import sqlite3
from datetime import datetime
from uuid import uuid4
from sheets_write import status_info_sheets, log_sheets


def check_register(id_client):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM registered WHERE id = ? """
        cursor.execute(tabl, [id_client])
        result = cursor.fetchall()
        return True if result else False


def add_new_user(id_user, name, phone, username):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """INSERT INTO registered VALUES(?,?,?,?,?) """
        cursor.execute(tabl, [id_user, name, phone, datetime.now().date(), username])


def get_all_user2():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM registered"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return result


def get_all_user():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM registered WHERE data = date('now')"""
        cursor.execute(tabl)
        result1 = cursor.fetchall()
        tabl = """SELECT * FROM registered"""
        cursor.execute(tabl)
        result2 = cursor.fetchall()
        return len(result2), len(result1)


def get_all_orders_done():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE status IN ('done', 'SOLD')"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return len(result)


def get_all_sumDown_done():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT sum(summ) FROM approve_down_balance WHERE status = 'approve'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        if result:
            if not result[0][0]:
                result = 0
            else:
                result = result[0][0]
        return result


def add_new_order(ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, login, currency="", status="process"):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """INSERT INTO orders(ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, user_id, date_order, status, login,
         currency) 
        
        VALUES(?,?,?,?,?,?,?,?,?,?) """
        cursor.execute(tabl, [ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, time_now(), status,
                              login, currency])


def add_new_order_buyer(ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, login, currency="", status="process",
                        reserve=0):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = '''CREATE TABLE IF NOT EXISTS buyer_orders (
                                                            "NUM"	INTEGER NOT NULL UNIQUE,
                                                            "ROOMS"	TEXT,
                                                            "SUMM_USD"	INTEGER,
                                                            "RATE_GRN"	INTEGER,
                                                            "MIN_PART"	INTEGER,
                                                            "TERM"	INTEGER,
                                                            "user_id"	INTEGER,
                                                            "date_order"	TEXT,
                                                            "status"	TEXT,
                                                            "login"	TEXT,
                                                            "currency"	TEXT,
                                                            "reserve" INTEGER,
                                                            PRIMARY KEY("NUM" AUTOINCREMENT))'''
        cursor.execute(tabl, )
        tabl = """INSERT INTO buyer_orders(ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, user_id, date_order, status, login,
         currency, reserve) 

        VALUES(?,?,?,?,?,?,?,?,?,?,?) """
        cursor.execute(tabl, [ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, time_now(), status,
                              login, currency, reserve])


def check_same_order(ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, currency="USD"):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM orders WHERE  ROOMS=? and user_id=? and currency = ? and status = 'process'"""
        cursor.execute(tabl, [ROOMS, id_user, currency])
        result = cursor.fetchall()
        return result


def check_same_order_buy(ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, currency="USD"):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = '''CREATE TABLE IF NOT EXISTS buyer_orders (
                                                                    "NUM"	INTEGER NOT NULL UNIQUE,
                                                                    "ROOMS"	TEXT,
                                                                    "SUMM_USD"	INTEGER,
                                                                    "RATE_GRN"	INTEGER,
                                                                    "MIN_PART"	INTEGER,
                                                                    "TERM"	INTEGER,
                                                                    "user_id"	INTEGER,
                                                                    "date_order"	TEXT,
                                                                    "status"	TEXT,
                                                                    "login"	TEXT,
                                                                    "currency"	TEXT,
                                                                    "reserve" INTEGER,
                                                                    PRIMARY KEY("NUM" AUTOINCREMENT))'''
        cursor.execute(tabl, )
        tabl = """SELECT * FROM buyer_orders WHERE  ROOMS=? and user_id=? and currency = ? and status = 'process'"""
        cursor.execute(tabl, [ROOMS, id_user, currency])
        result = cursor.fetchall()
        return result


def get_all_orders():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM orders WHERE status = 'process' ORDER BY RATE_GRN ASC """
        cursor.execute(tabl)
        result = cursor.fetchall()
        return result


def get_order_by_id(id_number):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM orders WHERE NUM = ?"""
        cursor.execute(tabl, [id_number])
        result = cursor.fetchall()
        return result[0]


def room_filter(kind):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if kind == "ВСІ РУМИ":
            tabl = """SELECT * FROM orders WHERE status = 'process' ORDER BY RATE_GRN ASC"""
            cursor.execute(tabl)
            result = cursor.fetchall()
            return result
        else:
            tabl = """SELECT * FROM orders WHERE ROOMS = ? and status = 'process' ORDER BY RATE_GRN ASC"""
            cursor.execute(tabl, [kind])
            result = cursor.fetchall()
            return result


def room_filter_buy(kind):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if kind == "ВСІ РУМИ":
            tabl = """SELECT * FROM buyer_orders WHERE status = 'process' ORDER BY RATE_GRN DESC"""
            cursor.execute(tabl)
            result = cursor.fetchall()
            return result
        else:
            tabl = """SELECT * FROM buyer_orders WHERE ROOMS = ? and status = 'process' ORDER BY RATE_GRN DESC"""
            cursor.execute(tabl, [kind])
            result = cursor.fetchall()
            return result


def time_now():
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d, %H:%M")
    return formatted_date


def add_new_processing_order(id_order, part, time, buyer, reserve, seller, login="", kind=""):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """INSERT INTO processing_order(id_order, part, time, buyer, status, reserve, seller, login, data, kind) 
        VALUES(?,?,?,?,?,?,?,?,?,?) """
        cursor.execute(tabl, [id_order, part, time, buyer, "process", reserve, seller, login, time_now(), kind])


def approve_balance_add(summ, card, name, id_user, full_name, promo=""):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        try:
            tabl = """SELECT promocode FROM approve_balance"""
            cursor.execute(tabl, )
        except sqlite3.OperationalError:
            cursor.execute("""ALTER TABLE approve_balance ADD COLUMN promocode TEXT""")
        tabl = """INSERT INTO approve_balance(summ, card, name, id_user, status, name_user, data, promocode)
                     VALUES(?,?,?,?,?,?,?,?) """
        cursor.execute(tabl, [summ, card, name, id_user, "in_process", full_name, time_now(), promo])


def get_all_balance_add():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM approve_balance WHERE status = 'in_process'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return result


def approve_balance_down(summ, card, name, id_user, name_user, promo="",):
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d, %H:%M")
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        try:
            tabl = """SELECT promocode FROM approve_down_balance"""
            cursor.execute(tabl, )
        except sqlite3.OperationalError:
            cursor.execute("""ALTER TABLE approve_down_balance ADD COLUMN promocode TEXT""")
        tabl = """INSERT INTO approve_down_balance(summ, card, name, id_user, status, name_user, data, promocode) 
        VALUES(?,?,?,?,?,?,?,?)"""
        cursor.execute(tabl, [summ, card, name, id_user, "in_process", name_user, formatted_date, promo, ])


def get_all_balance_down():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM approve_down_balance WHERE status = 'in_process'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return result


def update_balance(id_user, new_money, full_name=""):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM balance WHERE id = ?"""
        cursor.execute(tabl, [id_user])
        result = cursor.fetchall()
        if result:
            result = float(result[0][1])
            tabl = """UPDATE balance SET money = ? WHERE id = ?"""
            cursor.execute(tabl, [result + float(new_money), id_user])
        else:
            tabl = """INSERT INTO balance VALUES(?,?,?)"""
            cursor.execute(tabl, [id_user, float(new_money), full_name])


def update_balance_status(id_order, stat, where=False):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if stat == "approve":
            if where:
                tabl = """UPDATE approve_balance SET status = 'approve' WHERE id = ?"""
            else:
                tabl = """UPDATE approve_down_balance SET status = 'approve' WHERE id = ?"""
        elif stat == "cansel":
            if where:

                tabl = """UPDATE approve_balance SET status = 'cansel' WHERE id = ?"""
            else:
                tabl = """UPDATE approve_down_balance SET status = 'cansel' WHERE id = ?"""
        cursor.execute(tabl, [id_order])


def get_balance_by_id(id_user=0) -> float:
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if id_user:
            tabl = """SELECT * FROM balance WHERE id = ?"""
            cursor.execute(tabl, [id_user])
            result = cursor.fetchall()
            if result:
                return round(result[0][1], 2)
            else:
                return 0
        else:
            tabl = """SELECT SUM(money) FROM balance"""
            cursor.execute(tabl,)
            result = cursor.fetchall()
            try:
                result = round(result[0][0], 2)
            except Exception:
                result = 0
            return result


# def delete_process(where, id_order):
#     with sqlite3.connect("clients.db") as db:
#         cursor = db.cursor()
#         if where == "add":
#             tabl = """DELETE FROM approve_balance WHERE id = ?"""
#             cursor.execute(tabl, [id_order])
#         elif where == "down":
#             tabl = """DELETE FROM approve_down_balance WHERE id = ?"""
#             cursor.execute(tabl, [id_order])


def get_phone_by_id(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT phone FROM registered WHERE id = ?"""
        cursor.execute(tabl, [id_user])
        result = cursor.fetchall()
        if result:
            return result[0][0]
        else:
            tabl = """SELECT phone FROM ban WHERE id_user = ?"""
            cursor.execute(tabl, [id_user])
            result = cursor.fetchall()
            return result[0][0]


def get_count_orders_by_id(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM orders WHERE user_id = ? and status IN ('process')"""
        cursor.execute(tabl, [id_user])
        result = cursor.fetchall()
        return len(result)


def get_count_buyer_by_id(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE buyer = ? and status IN ('process', 'finally', 'dispute')"""
        cursor.execute(tabl, [id_user])
        result = cursor.fetchall()
        return len(result)


# def get_count_all_buyer_by_id(id_user):
#     with sqlite3.connect("clients.db") as db:
#         cursor = db.cursor()
#         tabl = """SELECT * FROM processing_order WHERE buyer = ? and status = 'done'"""
#         cursor.execute(tabl, [id_user])
#         result = cursor.fetchall()
#         return len(result)


def get_count_all_buyer_by_id(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE seller = ? and status IN ('process', 'finally', 
        'dispute') or buyer = ? and status IN ('process', 'finally', 'dispute')"""
        cursor.execute(tabl, [id_user, id_user])
        result = cursor.fetchall()
        return result[0][0] if result else 0


def all_orders_stat(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE buyer = ? and status != 'cansel'"""
        cursor.execute(tabl, [id_user])
        result = cursor.fetchall()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE seller = ?"""
        cursor.execute(tabl, [id_user])
        result2 = cursor.fetchall()
        return result2[0][0], result[0][0]


def all_orders_done_stat(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE buyer = ? and status IN ('done')"""
        cursor.execute(tabl, [id_user])
        result = cursor.fetchall()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE seller = ? and status IN ('done')"""
        cursor.execute(tabl, [id_user])
        result2 = cursor.fetchall()
        return result2[0][0], result[0][0]


def get_count_orders(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE seller = ?"""
        cursor.execute(tabl, [user])
        result1 = cursor.fetchall()
        tabl = """SELECT COUNT(*) FROM orders WHERE user_id = ?"""
        cursor.execute(tabl, [user])
        result2 = cursor.fetchall()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE buyer = ?"""
        cursor.execute(tabl, [user])
        result3 = cursor.fetchall()
        return [result1[0][0] + result2[0][0], result3[0][0]]


def get_count_all_orders_by_id(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE status = 'done'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        res = 0
        for x in result:
            tabl = """SELECT * FROM orders WHERE NUM = ? and user_id = ?"""
            cursor.execute(tabl, [x[1], id_user])
            if cursor.fetchall():
                res += 1
        return res


def get_all_adds(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM approve_balance WHERE status = 'approve' and id_user = ?"""
        cursor.execute(tabl, [id_user])
        result = cursor.fetchall()
        tabl = """SELECT sum(summ) FROM approve_balance WHERE status = 'approve' and id_user = ?"""
        cursor.execute(tabl, [id_user])
        result_sum = cursor.fetchall()
        res_sum = result_sum[0][0] if result_sum[0][0] else 0
        return len(result), res_sum


def get_all_downs(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM approve_down_balance WHERE status = 'approve' and id_user = ?"""
        cursor.execute(tabl, [id_user])
        result = cursor.fetchall()
        tabl = """SELECT sum(summ) FROM approve_down_balance WHERE status = 'approve' and id_user = ?"""
        cursor.execute(tabl, [id_user])
        result_sum = cursor.fetchall()
        res_sum = result_sum[0][0] if result_sum[0][0] else 0
        return len(result), res_sum


def get_all_my_orders(id_user, status=""):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if status and status != "ALL":
            tabl = """SELECT * FROM orders WHERE user_id = ? and status = ? """
            cursor.execute(tabl, [id_user, status])
        else:
            tabl = """SELECT * FROM orders WHERE user_id = ? and status IN ('process', 'pause', 'waiting', 'finally', 
            'cansel', 'valid') ORDER BY date_order DESC"""
            cursor.execute(tabl, [id_user])
        result1 = cursor.fetchall()
        tabl = """SELECT * FROM processing_order WHERE buyer = ? ORDER BY data DESC"""
        cursor.execute(tabl, [id_user])
        result2 = cursor.fetchall()
        return result1, result2


def get_all_my_orders_bought(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE seller = ? ORDER BY data DESC"""
        cursor.execute(tabl, [id_user])
        result1 = cursor.fetchall()
        result2 = []
        for x in result1:
            if x[10] == "sell":
                tabl = """SELECT * FROM orders WHERE NUM = ?"""
            elif x[10] == "buy":
                tabl = """SELECT * FROM buyer_orders WHERE NUM = ?"""
            cursor.execute(tabl, [x[1]])
            result2 += cursor.fetchall()
        return result1, result2


def get_all_my_orders_finally(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE status IN ('finally') and seller = ? ORDER BY data DESC"""
        cursor.execute(tabl, [id_user])
        result1 = cursor.fetchall()
        result2 = []
        for x in result1:
            if x[10] == "sell":
                tabl = f"""SELECT * FROM orders WHERE NUM = ?"""
            elif x[10] == "buy":
                tabl = f"""SELECT * FROM buyer_orders WHERE NUM = ?"""
            cursor.execute(tabl, [x[1]])
            result2 += cursor.fetchall()
        return result1, result2


def get_all_my_orders_sold(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE status IN ('SOLD', 'done') and seller = ? and kind = 'sell'
        ORDER BY data DESC"""
        cursor.execute(tabl, [id_user])
        result1 = cursor.fetchall()
        result2 = []
        for x in result1:
            tabl = f"""SELECT * FROM orders WHERE NUM = ?"""
            cursor.execute(tabl, [x[1]])
            result2 += cursor.fetchall()
        return result1, result2


def get_all_my_orders_dispute(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE status IN ('dispute') and seller = ?"""
        cursor.execute(tabl, [id_user])
        result1 = cursor.fetchall()
        result2 = []
        for x in result1:
            tabl = f"""SELECT * FROM orders WHERE NUM = ?"""
            cursor.execute(tabl, [x[1]])
            result2 += cursor.fetchall()
        return result1, result2


def update_order_status(id_order, stat, where=False):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if stat == "approve":
            pass
            # tabl = """UPDATE approve_down_balance SET status = 'approve' WHERE id = ?"""
        elif stat == "cansel":
            if where == "processing_order":
                tabl = """UPDATE processing_order SET status = 'cansel' WHERE id_process = ?"""

                # tabl = """UPDATE approve_balance SET status = 'cansel' WHERE id = ?"""
            elif where == "orders":
                tabl = """UPDATE orders SET status = 'cansel' WHERE NUM = ?"""
        cursor.execute(tabl, [id_order])


def update_order(id_order, new_value):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT SUMM_USD FROM orders WHERE NUM = ?"""
        cursor.execute(tabl, [id_order])
        result = cursor.fetchall()
        if result:
            result = float(result[0][0])
        else:
            result = 0
        if result or result == 0:
            tabl = """UPDATE orders SET SUMM_USD = ? WHERE NUM = ?"""
            cursor.execute(tabl, [result + new_value, id_order])
        if result + new_value <= 0:
            tabl = """UPDATE orders SET status = ? WHERE NUM = ?"""
            cursor.execute(tabl, ["waiting", id_order])
        elif result <= 0:
            tabl = """UPDATE orders SET status = ? WHERE NUM = ?"""
            cursor.execute(tabl, ["process", id_order])


def update_order_buy(id_order, new_value):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT SUMM_USD FROM buyer_orders WHERE NUM = ?"""
        cursor.execute(tabl, [id_order])
        result = cursor.fetchall()
        if result:
            result = float(result[0][0])
        else:
            result = 0
        if result or result == 0:
            tabl = """UPDATE buyer_orders SET SUMM_USD = ? WHERE NUM = ?"""
            cursor.execute(tabl, [result + new_value, id_order])
        if result + new_value <= 0:
            tabl = """UPDATE buyer_orders SET status = ? WHERE NUM = ?"""
            cursor.execute(tabl, ["waiting", id_order])
        elif result <= 0:
            tabl = """UPDATE buyer_orders SET status = ? WHERE NUM = ?"""
            cursor.execute(tabl, ["process", id_order])


def stop_order(id_order):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE orders SET status = ? WHERE NUM = ?"""
        cursor.execute(tabl, ["pause", id_order])


def active_order(id_order):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE orders SET status = ? WHERE NUM = ?"""
        cursor.execute(tabl, ["process", id_order])


def update_status_finally(id_process, time_finish):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE processing_order SET status = 'finally', time = ? WHERE id_process = ?"""
        cursor.execute(tabl, [time_finish, id_process])
        result = cursor.fetchall()


def update_status_done(id_process):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE processing_order SET status = 'done' WHERE id_process = ?"""
        cursor.execute(tabl, [id_process])


def get_all_user_balance():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM balance """
        cursor.execute(tabl, )
        result1 = cursor.fetchall()
        text = "ім'я   ід   баланс\n\n"
        for x in result1:
            text += f"{x[2]}   {x[0]}   {x[1]} грн.\n"
    return text.upper()


def switch():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM switch """
        cursor.execute(tabl, )
        result = cursor.fetchall()
        if result[0][0] == "ON":
            tabl = """UPDATE switch SET status = 'OFF'"""
            cursor.execute(tabl)
        elif result[0][0] == "OFF":
            tabl = """UPDATE switch SET status = 'ON'"""
            cursor.execute(tabl)


def switch_check():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM switch """
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return True if result[0][0] == "ON" else False


def admins():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM admins """
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return [x[0] for x in result]


def admins_delete(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """DELETE FROM admins WHERE user = ?"""
        cursor.execute(tabl, [id_user])


def admins_add(id_user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """INSERT INTO admins VALUES(?)"""
        cursor.execute(tabl, [id_user])


def check_thief(id_user, where, login="", card=""):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if where == "down":
            tabl = """SELECT * FROM approve_down_balance WHERE id_user != ? and card = ?"""
            cursor.execute(tabl, [id_user, card])
        elif where == "orders":
            tabl = """SELECT * FROM orders WHERE user_id != ? and login = ?"""
            cursor.execute(tabl, [id_user, login])
        result = cursor.fetchall()
        return result


def check_n():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT seq FROM sqlite_sequence WHERE  name = 'orders'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return result[0][0]


def check_nd():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT seq FROM sqlite_sequence WHERE  name = 'approve_down_balance'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return result[0][0]


def dispute_orders():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE  status = 'dispute'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return result


def dispute_orders_sold(number):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE processing_order SET status = 'SOLD' WHERE id_process = ?"""
        cursor.execute(tabl, [number])
        return


def update_status_close_admin(id_process):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE orders SET status = 'cansel' WHERE NUM = ?"""
        cursor.execute(tabl, [id_process])


def bot_off():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE  name = 'off'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return (result[0][0]).upper()


def work_time():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE  name = 'work_time'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return result[0][0]


def tax():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE  name = 'tax'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return float(result[0][0])


def norm_sum_add(kind):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if kind == "max":
            tabl = """SELECT text FROM text WHERE  name = 'max_sum_add'"""
        else:
            tabl = """SELECT text FROM text WHERE  name = 'min_sum_add'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return int(result[0][0])


def norm_sum_down(kind):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if kind == "max":
            tabl = """SELECT text FROM text WHERE  name = 'max_sum_down'"""
        else:
            tabl = """SELECT text FROM text WHERE  name = 'min_sum_down'"""
        cursor.execute(tabl)
        result = cursor.fetchall()
        return int(result[0][0])


def check_status_order(id_order):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT status FROM processing_order WHERE  id_process = ?"""
        cursor.execute(tabl, [id_order])
        result = cursor.fetchall()
        return result[0][0]


def get_name_user(id_client):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM registered WHERE id = ? """
        cursor.execute(tabl, [id_client])
        result = cursor.fetchall()
        try:
            if result:
                return result[0]
            else:
                cursor = db.cursor()
                tabl = """SELECT * FROM ban WHERE id_user = ?"""
                cursor.execute(tabl, [id_client])
                result = cursor.fetchall()
                return result[0]
        except Exception as ax:
            return ["NONE", "NONE", "NONE", "NONE", "NONE", ]


def dispute_solution(order, winner, losser):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """INSERT INTO dispute VALUES(?,?,?) """
        cursor.execute(tabl, [order, winner, losser])


def edit_order(ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, login, currency="", NUM=None):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE orders SET ROOMS = ?, 
                                    SUMM_USD = ?,
                                    RATE_GRN = ?,
                                    MIN_PART = ?,
                                    TERM = ?, 
                                    user_id = ?, 
                                    date_order = ?, 
                                    status = ?, 
                                    login = ?,
                                    currency = ?
                                    WHERE NUM = ? """
        cursor.execute(tabl, [ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, datetime.now().date(), 'process',
                              login, currency, NUM])


def edit_order_buy(ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, login, currency="", reserve=0, NUM=None):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE buyer_orders SET ROOMS = ?, 
                                    SUMM_USD = ?,
                                    RATE_GRN = ?,
                                    MIN_PART = ?,
                                    TERM = ?, 
                                    user_id = ?, 
                                    date_order = ?, 
                                    status = ?, 
                                    login = ?,
                                    currency = ?,
                                    reserve = ?
                                    WHERE NUM = ? """
        cursor.execute(tabl, [ROOMS, SUMM_USD, RATE_GRN, MIN_PART, TERM, id_user, datetime.now().date(), 'process',
                              login, currency, reserve, NUM])


def get_cart_info(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT DISTINCT card FROM approve_down_balance WHERE  id_user = ?"""
        cursor.execute(tabl, [user])
        result1 = (cursor.fetchall())
        tabl = """SELECT DISTINCT name FROM approve_down_balance WHERE  id_user = ?"""
        cursor.execute(tabl, [user])
        result2 = (cursor.fetchall())
        cart = ""
        owner = ""
        for x in result1:
            cart += str(x[0]) + ", "
        for x in result2:
            owner += str(x[0]) + ", "
        if not cart:
            cart = "Не вказано  "
        if not owner:
            owner = "Не вказано  "
        return cart[:-2], owner[:-2]


def arbitrage(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE  buyer = ? and status IN ('dispute', 'SOLD')"""
        cursor.execute(tabl, [user])
        result1 = cursor.fetchall()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE  seller = ? and status IN ('dispute', 'SOLD')"""
        cursor.execute(tabl, [user])
        result2 = cursor.fetchall()
        return result1[0][0] + result2[0][0]


def get_poker_log(name, user=0):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT DISTINCT login FROM orders WHERE ROOMS = ? and user_id=?"""
        cursor.execute(tabl, [name, user])
        result1 = (cursor.fetchall())
        login = ""
        for x in result1:
            login += str(x[0]) + ", "
        if not login:
            login = "Не вказано"
        return login


def get_sold(id_order):
    with sqlite3.connect("clients.db") as db:
        try:
            cursor = db.cursor()
            tabl = """SELECT winner FROM dispute WHERE  id_process = ?"""
            cursor.execute(tabl, [id_order])
            return (cursor.fetchall())[0][0]
        except Exception:
            return "-----"


def log_write(user, user_action, summ=""):
    with sqlite3.connect("garant_log.db") as db:
        cursor = db.cursor()
        try:
            tabl = """SELECT summ FROM log"""
            cursor.execute(tabl, )
        except sqlite3.OperationalError:
            cursor.execute("""ALTER TABLE log ADD COLUMN summ TEXT""")
        tabl = """INSERT INTO log(data, user, user_action, summ) VALUES(?,?,?,?) """
        time = datetime.now().strftime("%H:%M, %d.%m.%Y")
        cursor.execute(tabl, [time, user, user_action, summ])
        return


def log_info():
    title = [["НОМЕР", "ДАТА", "КОРИСТУВАЧ", "ДІЯ"]]
    with sqlite3.connect("garant_log.db") as db:
        try:
            cursor = db.cursor()
            tabl = """SELECT * FROM log """
            cursor.execute(tabl, )
            result = cursor.fetchall()

            for x in result:
                title.append(x)
            return title
        except Exception:
            pass


def get_custom_info(user=0, nick=""):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = '''CREATE TABLE IF NOT EXISTS user_castom (user INTEGER, 
                                                                   name TEXT, 
                                                                   notification_sell TEXT,
                                                                   notification_buy TEXT,
                                                                   comments TEXT)'''
        cursor.execute(tabl, )
        if nick:
            tabl = """SELECT * FROM user_castom WHERE name = ?"""
            cursor.execute(tabl, [nick])
        else:
            tabl = """SELECT * FROM user_castom WHERE user = ?"""
            cursor.execute(tabl, [user])
        check_user = cursor.fetchall()
        return check_user[0] if check_user else False


def user_info():
    title = [["ДАТА РЕЄСТРАЦІЇ",
              "ID КОРИСТУВАЧА",
              "НІКНЕЙМ У БОТІ",
              "ТГ НІКНЕЙМ",
              "ЮЗЕРНЕЙМ",
              "НОМЕР ТЕЛЕФОНУ",
              "ПОПОВНЕННЯ",
              "ВИВЕДЕННЯ",
              "ОСНОВНИЙ БАЛАНС",
              "ПАРТНЕРСКИЙ БАЛАНС",
              "КІЛЬКІСТЬ УГОД",
              "ЯК ПРОДАВЕЦЬ",
              "ЯК ПОКУПЕЦЬ",
              "АРБІТРАЖ",
              "АКТИВНІ ЗАЯВКИ",
              "НА КУПІВЛЮ",
              "НА ПРОДАЖ",
              "GGPOKER \ LOGIN",
              "POKERSTARS \ LOGIN",
              "POKERKING \ LOGIN",
              "ACR \ LOGIN",
              "888POKER \ LOGIN",
              "REDSTAR \ LOGIN",
              "ПОКЕРМАТЧ \ LOGIN",
              "POKERSTARS ES \ LOGIN",
              "КАРТКА",
              "ВЛАСНИК КАРТКИ"]]
    try:
        with sqlite3.connect("clients.db") as db:
            cursor = db.cursor()
            tabl = """SELECT * FROM registered """
            cursor.execute(tabl, )
            register_row = cursor.fetchall()
            for user in register_row:
                all_orders_seller = get_count_orders(user[0])[0]
                all_orders_bayer = get_count_orders(user[0])[1]
                all_orders = all_orders_seller + all_orders_bayer
                nick = get_custom_info(user[0])
                if nick:
                    nick = nick[1]
                partner_balance = 0
                arbit = arbitrage(user[0])
                process_bayer = get_count_buyer_by_id(user[0])
                process_seller = get_count_orders_by_id(user[0])
                process_order = process_seller + process_bayer
                card = get_cart_info(user[0])[0]
                owner = get_cart_info(user[0])[1]
                login1 = get_poker_log("GGPOKER", user[0])
                login2 = get_poker_log("POKERSTARS", user[0])
                login3 = get_poker_log("POKERKING", user[0])
                login4 = get_poker_log("ACR", user[0])
                login5 = get_poker_log("888POKER", user[0])
                login6 = get_poker_log("REDSTAR", user[0])
                login7 = get_poker_log("ПОКЕРМАТЧ", user[0])
                login8 = get_poker_log("POKERSTARS ES", user[0])
                add_list = [user[3], user[0], nick, user[1], user[4], user[2],
                            get_all_adds(user[0])[0], get_all_downs(user[0])[0], get_balance_by_id(user[0]),
                            partner_balance, all_orders, all_orders_seller, all_orders_bayer, arbit, process_order,
                            process_bayer, process_seller, login1, login2, login3, login4, login5, login6, login7,
                            login8,
                            card, owner]
                title.append(add_list)
    except Exception as ex:
        print(ex)
    return title


def status_info():
    title = [["ДАТА СТВОРЕННЯ",
              "НАПРЯМОК",
              "СТАТУС",
              "№ ЗАЯВКИ",
              "ID КОРИСТУВАЧА",
              "СУМА ЗАЯВКИ",
              "ВАЛЮТА",
              "КАРТКА",
              "ВЛАСНИК КАРТКИ",
              "ПОКУПЕЦЬ",
              "ПРОДАВЕЦЬ",
              "ПОКЕР-РУМ",
              "ЛОГІН ПРОДАВЕЦЬ",
              "ЛОГІН ПОКУПЕЦЬ",
              "№ ЗАЯВКИ ПРОДАЖУ",
              "КУРС",
              "РЕЗЕРВ",
              "ТЕРМІН ВИКОНАННЯ",
              "ДАТА ЗАВЕРШЕННЯ",
              "АРБІТРАЖ НА КОРИСТЬ"
              ]]
    try:
        with sqlite3.connect("clients.db") as db:
            cursor = db.cursor()
            tabl = """SELECT * FROM processing_order """
            cursor.execute(tabl, )
            process_orders_row = cursor.fetchall()
            tabl = """SELECT * FROM orders """
            cursor.execute(tabl, )
            orders_row = cursor.fetchall()
            tabl = """SELECT * FROM approve_down_balance """
            cursor.execute(tabl, )
            approve_down_balance_row = cursor.fetchall()
            tabl = """SELECT * FROM approve_balance """
            cursor.execute(tabl, )
            approve_balance_row = cursor.fetchall()
        for x in process_orders_row:
            status = ""
            order = get_order_by_id(x[1])
            plug1 = "-----"
            if x[5] == "done":
                status = "ВИКОНАНА"
            elif x[5] == "cansel":
                status = "ПРОДАВЕЦЬ НЕ ЗРОБИВ ПЕРЕКАЗ"
            elif x[5] == "process":
                status = "ОЧІКУЄ ПЕРЕКАЗУ ВІД ПРОДАВЦЯ"
            elif x[5] == "SOLD":
                status = "ЗАКРИТА АДМІНОМ(АРБІТРАЖ)"
                plug1 = get_sold(x[0])
            elif x[5] == "dispute":
                status = "АРБІТРАЖ"
            elif x[5] == "finally":
                status = "ОЧІКУЄ ПІДТВЕРДЖЕННЯ ВІД ПОКУПЦЯ"
            title.append(
                [x[9], "ЗУСТРІЧНА ЗАЯВКА", status, x[0], plug, x[2], order[10], plug, plug, x[4], x[7], order[1],
                 order[9], x[8], x[1], order[3], x[6], order[5], x[3], plug1])

        for x in orders_row:
            status = ""
            if x[8] == "waiting":
                status = "ОЧІКУЄ ОПЛАТИ"
            elif x[8] == "cansel":
                status = "СКАСОВАНА"
            elif x[8] == "process":
                status = "РОЗМІЩЕННА НА ВІТРИНІ"
            elif x[8] == "pause":
                status = "ЧЕРНЕТКА"
            elif x[8] == "done":
                status = "ВИКУПЛЕНА"

            title.append(
                [x[7], "ЗАЯВКА ПРОДАЖУ", status, x[0], plug, x[2], x[10], plug, plug, plug, x[6], x[1], x[9], plug,
                 plug, x[3], plug, x[5], plug, plug])
        for x in approve_down_balance_row:
            status = ""
            if x[5] == "approve":
                status = "ВИКОНАНА"
            elif x[5] == "cansel":
                status = "СКАСОВАНО"
            elif x[5] == "in_process":
                status = "ОЧІКУЄ ПІДТВЕРДЖЕННЯ"

            title.append([x[7], "ВИВЕДЕННЯ", status, x[0], x[4], str(x[1]), "ГРН", x[2], x[3]])

        for x in approve_balance_row:
            status = ""
            if x[5] == "approve":
                status = "ВИКОНАНА"
            elif x[5] == "cansel":
                status = "СКАСОВАНО"
            elif x[5] == "in_process":
                status = "ОЧІКУЄ ПІДТВЕРДЖЕННЯ"

            title.append([x[7], "ПОПОВНЕННЯ", status, x[0], x[4], x[1], "ГРН", x[2], x[3]])

        return title
    except Exception as ex:
        return False

plug = "-----"


def get_order_by_status(status="", user=0):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE status = ? and  buyer = ?"""
        cursor.execute(tabl, [status, user])
        result = cursor.fetchall()
    return result


def get_reserve(id_order):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT reserve FROM processing_order WHERE id_process = ?"""
        cursor.execute(tabl, [id_order])
        result = cursor.fetchall()
        if result:
            return result[0][0]
        else:
            return 0


def get_winner(id_order):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM dispute WHERE id_process = ?"""
        cursor.execute(tabl, [id_order])
        result = cursor.fetchall()
    return result[0] if result else False


def dispute_winner_by_user(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM dispute WHERE winner = ?"""
        cursor.execute(tabl, [user])
        result = cursor.fetchall()
    return result[0][0] if result else 0


def dispute_by_user(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE buyer = ? and status IN ('SOLD', 'dispute')"""
        cursor.execute(tabl, [user])
        result = cursor.fetchall()
        tabl = """SELECT COUNT(*) FROM processing_order WHERE seller = ? and status IN('SOLD', 'dispute')"""
        cursor.execute(tabl, [user])
        result2 = cursor.fetchall()
        result = result[0][0] if result else 0
        result2 = result2[0][0] if result2 else 0
    return result + result2


def check_valid(user, room, login):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM verification WHERE user = ? and room = ? and login = ?"""
        cursor.execute(tabl, [user, room, login])
        result = cursor.fetchall()
        return result


def reason_to_valid(room, user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM verification WHERE user = ? and room = ?"""
        cursor.execute(tabl, [user, room])
        result = cursor.fetchall()
        return result


def check_login_valid(user, login):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM verification WHERE user != ? and login = ?"""
        cursor.execute(tabl, [user, login])
        result = cursor.fetchall()
        return result


def valid_order():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM orders WHERE status = 'valid'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result


def update_status_process(id_process):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE orders SET status = 'process' WHERE NUM = ?"""
        cursor.execute(tabl, [id_process])
        return


def update_valid(user, room, login):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """INSERT INTO verification VALUES(?,?,?)"""
        cursor.execute(tabl, [user, room, login])


def ban_user(user):
    with sqlite3.connect("clients.db") as db:
        try:
            cursor = db.cursor()
            tabl = """SELECT * FROM registered WHERE id = ?"""
            cursor.execute(tabl, [user])
            result = cursor.fetchall()
            tabl = """INSERT INTO ban VALUES(?,?,?,?,?,?)"""
            add = [x for x in result[0]]
            add.append(datetime.now().date())
            cursor.execute(tabl, add)
            tabl = """DELETE FROM registered WHERE id = ?"""
            cursor.execute(tabl, [user])
            return True
        except Exception:
            return False


def unban_user(user):
    with sqlite3.connect("clients.db") as db:
        try:
            cursor = db.cursor()
            tabl = """SELECT * FROM ban WHERE id_user = ?"""
            cursor.execute(tabl, [user])
            result = cursor.fetchall()
            tabl = """INSERT INTO registered VALUES(?,?,?,?,?)"""
            add = [x for x in result[0]]
            add.pop(-1)
            cursor.execute(tabl, add)
            tabl = """DELETE FROM ban WHERE id_user = ?"""
            cursor.execute(tabl, [user])
            return True
        except Exception as ex:
            print(ex)
            return False


def check_ban(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM ban WHERE id_user = ?"""
        cursor.execute(tabl, [user])
        result = cursor.fetchall()
        return result


def get_referral_link(user_id):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT link FROM referal WHERE user = ?"""
        cursor.execute(tabl, [user_id])
        result = cursor.fetchall()
        tabl = """SELECT text FROM text WHERE name = 'bot_name'"""
        cursor.execute(tabl, )
        bot_name = cursor.fetchall()
        if result:
            return result[0][0]
        else:
            referral_token = uuid4().hex
            link = f'https://t.me/{bot_name[0][0]}?start={referral_token}_{user_id}'
            tabl = """INSERT INTO referal(user, link) VALUES(?,?)"""
            cursor.execute(tabl, [user_id, link])
            return link


def check_referral(user, ref):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM referrals WHERE user = ? and referral = ?"""
        cursor.execute(tabl, [user, ref])
        result = cursor.fetchall()
        if result:
            return False
        else:
            tabl = """INSERT INTO referrals VALUES(?,?)"""
            cursor.execute(tabl, [user, ref])
            return True


def get_ref_tax():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = ?"""
        cursor.execute(tabl, ["referral"])
        result = cursor.fetchall()
        return result[0][0]


def count_my_ref(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM referrals WHERE user = ?"""
        cursor.execute(tabl, [user])
        result = cursor.fetchall()
        if result:
            return result[0][0]
        else:
            return 0


def count_my_ref_money(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT all_cur FROM partner_balance WHERE user = ?"""
        cursor.execute(tabl, [user])
        result = cursor.fetchall()
        if result:
            return result[0][0]
        else:
            return 0


def count_ref_money():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT SUM(all_cur) FROM partner_balance """
        cursor.execute(tabl, )
        result = cursor.fetchall()
        if not result[0][0]:
            result = 0
        else:
            result = result[0][0]
        tabl = """SELECT SUM(currency) FROM partner_balance """
        cursor.execute(tabl, )
        result2 = cursor.fetchall()
        if not result2[0][0]:
            result2 = 0
        else:
            result2 = result2[0][0]
        return result - result2


def upload_partner_balance(user, new_money):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM partner_balance WHERE user = ?"""
        cursor.execute(tabl, [user])
        result = cursor.fetchall()
        if result:
            money = float(result[0][2]) + float(new_money)
            if float(new_money) < 0:
                money = float(result[0][2])
            result = float(result[0][1])
            tabl = """UPDATE partner_balance SET currency = ?, all_cur = ? WHERE user = ?"""
            cursor.execute(tabl, [result + float(new_money), money, user])
        else:
            tabl = """INSERT INTO partner_balance VALUES(?,?,?)"""
            cursor.execute(tabl, [user, float(new_money), float(new_money)])


def user_by_ref(ref):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT user FROM referrals WHERE referral = ?"""
        cursor.execute(tabl, [ref])
        result = cursor.fetchall()
        if result:
            return result[0][0]
        else:
            return False


def get_partner_balance(user=0):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if user:
            tabl = """SELECT currency FROM partner_balance WHERE user = ?"""
            cursor.execute(tabl, [user])
            result = cursor.fetchall()
            if result:
                result = float(result[0][0])
                return result
            else:
                return 0
        else:
            tabl = """SELECT SUM(currency) FROM partner_balance"""
            cursor.execute(tabl,)
            result = cursor.fetchall()
            return result[0][0]


def get_balance_orders(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM approve_balance WHERE id_user = ? ORDER BY data DESC"""
        cursor.execute(tabl, [user])
        add = cursor.fetchall()
        cursor = db.cursor()
        tabl = """SELECT * FROM approve_down_balance WHERE id_user = ? ORDER BY data DESC"""
        cursor.execute(tabl, [user])
        down = cursor.fetchall()
        return add, down


def get_login_by_order(order, user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT login FROM orders WHERE NUM = ? and user_id = ?"""
        cursor.execute(tabl, [order, user])
        result = cursor.fetchall()
        return result[0][0]


def get_seller_win(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT id_process FROM processing_order WHERE status = 'SOLD' and seller = ?"""
        cursor.execute(tabl, [user])
        result = cursor.fetchall()
        count = 0
        if result:
            for x in result:
                tabl = """SELECT * FROM dispute WHERE id_process=? and winner = ?"""
                cursor.execute(tabl, [x[0], user])
                res = cursor.fetchall()
                if res:
                    count += 1

        return count


def get_buyer_win(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT id_process FROM processing_order WHERE status = 'SOLD' and buyer = ?"""
        cursor.execute(tabl, [user])
        result = cursor.fetchall()
        count = 0
        if result:
            for x in result:
                tabl = """SELECT * FROM dispute WHERE id_process=? and winner = ?"""
                cursor.execute(tabl, [x[0], user])
                res = cursor.fetchall()
                if res:
                    count += 1

        return count


def get_cart():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'cart'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result[0][0]


def founder():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'founder'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result[0][0]


def questions():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'questions'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result[0][0]


def rules():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'rules'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result[0][0]


def get_token():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'token'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result[0][0]


def get_id_group():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'id_group'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result[0][0]


def get_tax_grn():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'tax_grn'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return float(result[0][0])


def get_bot_name():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'bot_name'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result[0][0]


def get_tax():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT text FROM text WHERE name = 'tax'"""
        cursor.execute(tabl, )
        result = cursor.fetchall()
        return result[0][0]


def delete_valid_order(user, room):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """DELETE FROM verification WHERE user = ? and room = ?"""
        cursor.execute(tabl, [user, room])
        result = cursor.fetchall()


def add_promoCodes(codes_list):
    with sqlite3.connect("promoCodes.db") as db:
        cursor = db.cursor()
        tabl = """INSERT INTO Codes VALUES(?,?,?,?,?)"""
        cursor.executemany(tabl, codes_list)


def check_promoCode(code, kind):
    with sqlite3.connect("promoCodes.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM Codes WHERE Code = ? and kind = ? and Status = 'active'"""
        cursor.execute(tabl, [code, kind])
        result = cursor.fetchall()
        return result


def create_doc(text):
    with open('Codes.txt', 'w', encoding='utf-8') as file:
        for x in text:
            file.write(x)


def update_code(code, kind):
    with sqlite3.connect("promoCodes.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE Codes SET Status = 'used' WHERE Code = ? and kind = ? and Status = 'active'"""
        cursor.execute(tabl, [code, kind])


def count_promoCodes():
    with sqlite3.connect("promoCodes.db") as db:
        cursor = db.cursor()
        tabl = """SELECT COUNT(*) FROM Codes"""
        cursor.execute(tabl, )
        all_count = cursor.fetchall()
        tabl = """SELECT COUNT(*) FROM Codes WHERE Status = 'used'"""
        cursor.execute(tabl, )
        used_count = cursor.fetchall()
        tabl = """SELECT COUNT(*) FROM Codes WHERE Status = 'active'"""
        cursor.execute(tabl, )
        active_count = cursor.fetchall()
        return [all_count[0][0], used_count[0][0], active_count[0][0]]


def get_all_promoCodes():
    with sqlite3.connect("promoCodes.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM Codes"""
        cursor.execute(tabl, )
        all_codes = cursor.fetchall()
        return all_codes


def get_promoCode(code):
    with sqlite3.connect("promoCodes.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM Codes WHERE Code = ?"""
        cursor.execute(tabl, [code])
        all_codes = cursor.fetchall()
        return all_codes[0] if all_codes else 0


def check_waiting_order(num):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE id_order = ? and status IN ('process', 'finally', 'dispute')"""
        cursor.execute(tabl, [num])
        open_orders = cursor.fetchall()
        if not open_orders:
            tabl = """UPDATE orders SET status = 'done' WHERE NUM = ?"""
            cursor.execute(tabl, [num])


def check_waiting_order2(num):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM processing_order WHERE id_order = ? and status IN ('process', 'finally', 'dispute')"""
        cursor.execute(tabl, [num])
        open_orders = cursor.fetchall()
        if not open_orders:
            tabl = """UPDATE buyer_orders SET status = 'done' WHERE NUM = ?"""
            cursor.execute(tabl, [num])


def average_time(user, step, time):
    with sqlite3.connect("clients.db") as db:
        try:
            cursor = db.cursor()
            tabl = '''CREATE TABLE IF NOT EXISTS average_time (id_user INTEGER, 
                                                           step TEXT, 
                                                           time TEXT)'''
            cursor.execute(tabl,)
            tabl = """INSERT INTO average_time VALUES(?,?,?)"""
            cursor.execute(tabl, [user, step, time])
            return True
        except Exception as ex:
            print(ex)
            return False


def get_average_t():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT AVG(time) FROM average_time WHERE step = 'finally'"""
        cursor.execute(tabl,)
        time_finally = cursor.fetchall()
        tabl = """SELECT AVG(time) FROM average_time WHERE step = 'process'"""
        cursor.execute(tabl, )
        time_process = cursor.fetchall()
        if time_process[0][0]:
            time_process = time_process[0][0] / 60
        else:
            time_process = 0
        if time_finally[0][0]:
            time_finally = time_finally[0][0] / 60
        else:
            time_finally = 0
        return round(time_process, 2), round(time_finally, 2)


def get_aver_t_user(user):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = '''CREATE TABLE IF NOT EXISTS average_time (id_user INTEGER, 
                                                                   step TEXT, 
                                                                   time TEXT)'''
        cursor.execute(tabl)
        tabl = """SELECT AVG(time) FROM average_time WHERE step = 'finally' and id_user = ?"""
        cursor.execute(tabl, [user])
        time_finally = cursor.fetchall()
        tabl = """SELECT AVG(time) FROM average_time WHERE step = 'process' and id_user = ?"""
        cursor.execute(tabl, [user])
        time_process = cursor.fetchall()
        if time_process[0][0]:
            time_process = time_process[0][0] / 60
        else:
            time_process = 0
        if time_finally[0][0]:
            time_finally = time_finally[0][0] / 60
        else:
            time_finally = 0
        return round(time_process, 2), round(time_finally, 2)


def user_custom_name(user, name):
    with sqlite3.connect("clients.db") as db:
        try:
            cursor = db.cursor()
            tabl = '''CREATE TABLE IF NOT EXISTS user_castom (user INTEGER, 
                                                           name TEXT, 
                                                           notification_sell TEXT,
                                                           notification_buy TEXT,
                                                           comments TEXT)'''
            cursor.execute(tabl,)
            tabl = """SELECT * FROM user_castom WHERE user = ?"""
            cursor.execute(tabl, [user])
            check_user = cursor.fetchall()
            if check_user:
                tabl = """UPDATE user_castom SET name = ? WHERE user = ?"""
                cursor.execute(tabl, [name, user])
            else:
                tabl = """INSERT INTO user_castom VALUES(?,?,?,?,?)"""
                cursor.execute(tabl, [user, name, "ON", "ON", ""])
            return True
        except Exception as ex:
            return False


def user_custom_comments(user, com):
    with sqlite3.connect("clients.db") as db:
        try:
            cursor = db.cursor()
            tabl = '''CREATE TABLE IF NOT EXISTS user_castom (user INTEGER, 
                                                           name TEXT, 
                                                           notification_sell TEXT,
                                                           notification_buy TEXT,
                                                           comments TEXT)'''
            cursor.execute(tabl,)
            tabl = """SELECT * FROM user_castom WHERE user = ?"""
            cursor.execute(tabl, [user])
            check_user = cursor.fetchall()
            if check_user:
                tabl = """UPDATE user_castom SET comments = ? WHERE user = ?"""
                cursor.execute(tabl, [com, user])
            else:
                tabl = """INSERT INTO user_castom VALUES(?,?,?,?,?)"""
                cursor.execute(tabl, [user, user, "ON", "ON", com])
            return True
        except Exception as ex:
            print(ex)
            return False


def update_notification(user, kind="sell"):
    info = get_custom_info(user)
    status = "ON"
    status_check = "ON"
    try:
        if kind == "sell":
            status_check = info[2]
        else:
            status_check = info[3]
    except Exception:
        pass
    if status_check == "ON":
        status = "OFF"

    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """SELECT * FROM user_castom WHERE user = ?"""
        cursor.execute(tabl, [user])
        check_user = cursor.fetchall()
        if not check_user:
            tabl = """INSERT INTO user_castom VALUES(?,?,?,?,?)"""
            cursor.execute(tabl, [user, user, "ON", "ON", ""])
        if kind == "sell":
            tabl = """UPDATE user_castom SET notification_sell = ? WHERE user = ?"""
        else:
            tabl = """UPDATE user_castom SET notification_buy = ? WHERE user = ?"""
        cursor.execute(tabl, [status, user])


def get_admin_info():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT COUNT(*) FROM registered""",)
        user = cursor.fetchall()
        user = user[0][0]
        cursor.execute("""SELECT COUNT(*) FROM orders""", )
        orders = cursor.fetchall()
        orders = orders[0][0]
    with sqlite3.connect("garant_log.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT COUNT(*) FROM Log""",)
        log = cursor.fetchall()
        log = log[0][0]
    return log, orders, user


def close_process_order(order):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = """UPDATE processing_order SET status = 'cansel' WHERE id_process = ?"""
        cursor.execute(tabl, [order])


def get_buyer_orders(user=0, order=0, all_order=0, status=""):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = '''CREATE TABLE IF NOT EXISTS buyer_orders (
                                                                    "NUM"	INTEGER NOT NULL UNIQUE,
                                                                    "ROOMS"	TEXT,
                                                                    "SUMM_USD"	INTEGER,
                                                                    "RATE_GRN"	INTEGER,
                                                                    "MIN_PART"	INTEGER,
                                                                    "TERM"	INTEGER,
                                                                    "user_id"	INTEGER,
                                                                    "date_order"	TEXT,
                                                                    "status"	TEXT,
                                                                    "login"	TEXT,
                                                                    "currency"	TEXT,
                                                                    "reserve" INTEGER,
                                                                    PRIMARY KEY("NUM" AUTOINCREMENT))'''
        cursor.execute(tabl, )
        if order:
            cursor.execute("""SELECT * FROM buyer_orders WHERE user_id = ? and NUM = ?""", [user, order])
            orders = cursor.fetchall()
            return orders[0]
        elif all_order:
            cursor.execute("""SELECT * FROM buyer_orders WHERE status = 'process' ORDER BY RATE_GRN DESC""",)
            orders = cursor.fetchall()
            return orders
        elif status and user:
            cursor.execute("""SELECT * FROM buyer_orders WHERE status = 'process' and user_id = ? ORDER BY 
            date_order DESC""", )
            orders = cursor.fetchall()
            return orders
        cursor.execute("""SELECT * FROM buyer_orders WHERE user_id = ? ORDER BY date_order DESC""", [user])
        orders = cursor.fetchall()
        return orders


def update_status_order_buy(id_process, status="cansel", reserve=0, part=0):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if reserve:
            cursor.execute("""SELECT reserve from buyer_orders WHERE NUM = ?""", [id_process])
            res = cursor.fetchall()
            tabl = """UPDATE buyer_orders SET reserve = ? WHERE NUM = ?"""
            cursor.execute(tabl, [res[0][0] - reserve, id_process])
        elif part:
            cursor.execute("""SELECT SUMM_USD from buyer_orders WHERE NUM = ?""", [id_process])
            res = cursor.fetchall()
            tabl = """UPDATE buyer_orders SET SUMM_USD = ? WHERE NUM = ?"""
            cursor.execute(tabl, [res[0][0] - part, id_process])
        else:
            tabl = """UPDATE buyer_orders SET status = ? WHERE NUM = ?"""
            cursor.execute(tabl, [status, id_process])


def get_buyer_balance():
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        tabl = '''CREATE TABLE IF NOT EXISTS buyer_orders (
                                                                    "NUM"	INTEGER NOT NULL UNIQUE,
                                                                    "ROOMS"	TEXT,
                                                                    "SUMM_USD"	INTEGER,
                                                                    "RATE_GRN"	INTEGER,
                                                                    "MIN_PART"	INTEGER,
                                                                    "TERM"	INTEGER,
                                                                    "user_id"	INTEGER,
                                                                    "date_order"	TEXT,
                                                                    "status"	TEXT,
                                                                    "login"	TEXT,
                                                                    "currency"	TEXT,
                                                                    "reserve" INTEGER,
                                                                    PRIMARY KEY("NUM" AUTOINCREMENT))'''
        cursor.execute(tabl)
        cursor.execute("""SELECT SUM(reserve) from buyer_orders WHERE status ='process'""", )
        res = cursor.fetchall()
        return res[0][0]


def get_process_order(num=0, order=None, kind=""):
    with sqlite3.connect("clients.db") as db:
        cursor = db.cursor()
        if order:
            tabl = """SELECT * FROM processing_order WHERE time = ? and buyer = ? and seller = ? and data = ?"""
            cursor.execute(tabl, [order[0], order[1], order[2], order[3]])
            open_orders = cursor.fetchall()
        elif kind and num:
            tabl = """SELECT * FROM processing_order WHERE id_order = ? and status IN('process', 'finally', 'dispute') 
            and kind=?"""
            cursor.execute(tabl, [num, kind])
            open_orders = cursor.fetchall()
        else:
            tabl = """SELECT * FROM processing_order WHERE id_order = ?"""
            cursor.execute(tabl, [num])
            open_orders = cursor.fetchall()
        return open_orders if open_orders else False

