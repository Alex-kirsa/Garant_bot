import asyncio
from datetime import datetime
import sqlite3
from dispatcher import bot
from database import update_balance, update_order, stop_order, get_name_user, check_waiting_order,\
    update_status_order_buy, check_waiting_order2
from config import ID_ADMIN_GROUP, id_group_log


async def check_time_orders():
    while True:
        date_format = "%d.%m.%Y, %H:%M"
        with sqlite3.connect("clients.db") as db:
            cursor = db.cursor()
            try:
                tabl = """SELECT kind FROM processing_order"""
                cursor.execute(tabl, )
            except sqlite3.OperationalError:
                cursor.execute("""ALTER TABLE processing_order ADD COLUMN kind TEXT""")
                tabl = """UPDATE processing_order SET kind = 'sell'"""
                cursor.execute(tabl,)
            tabl = """SELECT * FROM processing_order WHERE status = 'process'"""
            cursor.execute(tabl)
            result = cursor.fetchall()
        for x in result:
            date_time = datetime.strptime(x[3], date_format)
            if date_time < datetime.now() and x[5] == "process":
                if x[10] == "buy":
                    update_status_order_buy(x[1], reserve=-float(x[6]))
                    update_status_order_buy(x[1], part=-float(x[2]))
                else:
                    update_balance(x[4], float(x[6]))
                    update_order(x[1], float(x[2]))
                    stop_order(x[1])
                with sqlite3.connect("clients.db") as db:
                    cursor = db.cursor()
                    tabl = """UPDATE processing_order SET status = 'cansel' WHERE id_process = ?"""
                    cursor.execute(tabl, [x[0]])
                    ret = ""
                    draft = ""
                    if x[10] == "buy":
                        tabl = """SELECT * FROM buyer_orders WHERE NUM = ?"""
                        cursor.execute(tabl, [x[1]])
                        res = cursor.fetchall()
                    else:
                        ret = f"\n{float(x[6])} ГРН. ПОВЕРНУТО НА ВАШ БАЛАНС."
                        draft = "ВАША ЗАЯВКА ПЕРЕЙШЛА У СТАТУС: ЧЕРНЕТКА"
                        tabl = """SELECT * FROM orders WHERE NUM = ?"""
                        cursor.execute(tabl, [x[1]])
                        res = cursor.fetchall()
                    id_seller = x[7]
                    try:
                        if x[10] != "buy":
                            print(54)
                            await bot.send_message(x[4], f"ЧАС ЗАЯВКИ {x[0]} ВИЙШОВ. ПРОДАВЕЦЬ НЕ "
                                                         f"ЗРОБИВ ПЕРЕКАЗ." + ret)
                    except Exception:
                        pass
                    try:
                        await bot.send_message(id_seller, f"ЧАС ЗАЯВКИ №{x[0]} ВИЙШОВ. ВИ НЕ ЗРОБИЛИ ПЕРЕКАЗ. \n"+ draft)
                    except Exception as ex:
                        print(ex)
                    await bot.send_message(id_group_log, f"{x[4]} НЕ ПІДТВЕРДИВ ПЕРЕКАЗ ІГРОВОЇ ВАЛЮТИ {x[2]}"
                                                         f" {res[0][10]} ПО ЗАЯВЦІ №{x[0]} ВІД ПРОДАВЦЯ {id_seller}")

        with sqlite3.connect("clients.db") as db:
            cursor = db.cursor()
            tabl = """SELECT * FROM processing_order WHERE status = 'finally'"""
            cursor.execute(tabl)
            result2 = cursor.fetchall()
        for x in result2:
            date_time = datetime.strptime(x[3], date_format)
            if date_time < datetime.now() and x[5] == "finally":
                with sqlite3.connect("clients.db") as db:
                    cursor = db.cursor()
                    tabl = """UPDATE processing_order SET status = 'dispute' WHERE id_process = ?"""
                    cursor.execute(tabl, [x[0]])
                    if x[10] == "buy":
                        tabl = """SELECT * FROM buyer_orders WHERE NUM = ?"""
                    else:
                        tabl = """SELECT * FROM orders WHERE NUM = ?"""
                    cursor.execute(tabl, [x[1]])
                    res = cursor.fetchall()
                    id_seller = res[0][6]
                    username_seller = get_name_user(x[7])[4]
                    username_buyer = get_name_user(x[4])[4]
                    await bot.send_message(id_group_log, f"{x[4]} НЕ ПІДТВЕРДИВ ОТРИМАННЯ ІГРОВОЇ ВАЛЮТИ {x[2]}"
                                                         f" {res[0][10]} ПО ЗАЯВЦІ №{x[0]} ВІД ПРОДАВЦЯ {id_seller}")
                    await bot.send_message(ID_ADMIN_GROUP, f"НОВА ЗАЯВКА НА АРБІТРАЖ №{x[0]}\n\n"
                                                           f"Продавець: {x[7]}\n"
                                                           f"Псевдонім: @{username_seller}\n\n"
                                                           f"покупець: {x[4]}\n"
                                                           f"Псевдонім: @{username_buyer}".upper())
                    try:
                        await bot.send_message(x[4], f"ЧАС ЗАЯВКИ №{x[0]} ВИЙШОВ. статус: АРБІТРАЖ".upper())
                    except Exception:
                        pass
                    try:
                        await bot.send_message(x[7], f"ЧАС ЗАЯВКИ №{x[0]} ВИЙШОВ. статус: АРБІТРАЖ".upper())
                    except Exception:
                        pass

        with sqlite3.connect("clients.db") as db:
            cursor = db.cursor()
            tabl = """SELECT * FROM orders WHERE status = 'waiting'"""
            cursor.execute(tabl)
            result3 = cursor.fetchall()
        for x in result3:
            check_waiting_order(x[0])
        with sqlite3.connect("clients.db") as db:
            cursor = db.cursor()
            tabl = """SELECT * FROM buyer_orders WHERE status = 'waiting'"""
            cursor.execute(tabl)
            result3 = cursor.fetchall()
        for x in result3:
            check_waiting_order2(x[0])
        with sqlite3.connect("promoCodes.db") as db:
            cursor = db.cursor()
            data = datetime.now().date()
            tabl = """UPDATE Codes SET status = 'cansel' WHERE data < ?"""
            cursor.execute(tabl, [data])
        await asyncio.sleep(30)


loop = asyncio.get_event_loop()
loop.create_task(check_time_orders())
