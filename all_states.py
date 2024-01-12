from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMDistributor(StatesGroup):
    where = State()


class FSMAdd(StatesGroup):
    start_add = State()
    start_wh = State()
    change_sum = State()
    card = State()
    owner = State()
    change_sum2 = State()
    card2 = State()
    owner2 = State()
    promo_code = State()
    promo_code_add = State()


class FSMPhone(StatesGroup):
    add_phone = State()


class FSMCreate(StatesGroup):
    step1 = State()
    step2 = State()
    edit_usd = State()
    edit_rate = State()
    edit_min_part = State()
    edit_term = State()
    mail = State()


class FSMCreateBuyer(StatesGroup):
    step1 = State()
    step2 = State()
    edit_usd = State()
    edit_rate = State()
    edit_min_part = State()
    edit_term = State()
    mail = State()


class FSMAllOrders(StatesGroup):
    step1 = State()
    change_usd = State()
    change_mail = State()
    finally_step = State()
    approve_action = State()
    describe_action = State()
    edit = State()


class FSMAdmin(StatesGroup):
    where = State()
    add_summ = State()
    down_summ = State()
    change_balance = State()
    change_balance2 = State()
    send = State()
    admins = State()
    dispute = State()
    approve_action = State()
    approve_action_down = State()
    describe_action_down = State()
    approve_action_down2 = State()
    approve_action_add2 = State()
    describe_action_add = State()
    dispute_solution = State()
    user_info = State()
    valid = State()
    valid_approve_desc = State()
    all_users = State()
    send_msg_user = State()
    ban_user = State()
    promo = State()
    promo_term = State()
    promo_disc = State()


class FSMMyOrders(StatesGroup):
    step1 = State()
    bayer = State()
    approve1 = State()
    approve2 = State()
    edit = State()
    balance = State()
    cansel = State()



class FSMFaq(StatesGroup):
    step1 = State()


class FSMBalance(StatesGroup):
    step1 = State()


class FSMProfile(StatesGroup):
    where = State()
    change_name = State()
    add_comments = State()
