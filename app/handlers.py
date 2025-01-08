from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from app.database.requests import add_user, get_sub_status, get_date_of_reg, get_sub_details, turn_on_sub, turn_off_sub
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import app.keyboards as kb

r = Router()

class UserState(StatesGroup):
    last_message_id = State()
    item_id_to_pay = State()

@r.message(Command('start'))
async def start_command(message: Message, bot: Bot, state: FSMContext):
    await add_user(message.from_user.id)
    sub_status = await get_sub_status(message.from_user.id)
    if type(sub_status) is str:
        msg = await turn_off_sub(message.from_user.id)
    else:
        None
    data = await state.get_data()
    last_message_id = data.get("last_message_id")

    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id=message.from_user.id, message_id=last_message_id)
        except Exception:
            None
    await message.answer('😶‍🌫️', reply_markup=kb.channel_keyboard)
    msg = await message.answer('Здесь вы сможете купить приватную подписку..', reply_markup=kb.start_keyboard)
    await state.update_data(last_message_id=msg.message_id)

@r.callback_query(F.data == 'home')
async def home_callback(callback: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    last_message_id = data.get("last_message_id")

    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
        except Exception:
            None

    msg = await callback.message.answer('Здесь вы сможете купить приватную подписку..', reply_markup=kb.start_keyboard)
    await state.update_data(last_message_id=msg.message_id)
    await callback.answer()

@r.callback_query(F.data == 'profile')
async def sub_stat(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_id = callback.from_user.id
    username = callback.from_user.username
    data = await state.get_data()
    last_message_id = data.get('last_message_id')

    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
        except Exception:
            None

    reg_date = await get_date_of_reg(user_id)
    sub_status = await get_sub_status(user_id)
    if sub_status is False:
        msg = await callback.message.answer(f'Ваш username: {username}\nИнформация по подписке: нету\nДата регистрации: {reg_date}\n', reply_markup=kb.back_to_home)
    else:
        msg = await callback.message.answer(f'Ваш username: {username}\n{sub_status}\nДата регистрации: {reg_date}\n', reply_markup=kb.back_to_home)
    await state.update_data(last_message_id=msg.message_id)
    await callback.answer()

@r.callback_query(F.data == 'categories')
async def get_sub_category(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')

    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
        except Exception:
            None
    msg = await callback.message.answer('Все категории подписки:', reply_markup=await kb.inline_categories('home'))
    await state.update_data(last_message_id=msg.message_id)
    await callback.answer()

@r.callback_query(F.data.startswith('item_'))
async def refresh_message(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')
    item_id_to_pay = data.get('item_id_to_pay')

    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
        except Exception:
            None
    details = await get_sub_details(callback.data.split('_')[1]) # 0 - time, 1 - price, 2 - description, 3 - name
    sub_status = await get_sub_status(callback.from_user.id)
    if sub_status is False:
        msg = await callback.message.answer(f'Название: {details[3]}\nОписание: {details[2]}\nЦена: {details[1]} stars\nВремя длительности: {details[0]} месяц', reply_markup=kb.pay_keyboard)
        await state.update_data(last_message_id=msg.message_id, item_id_to_pay=callback.data.split('_')[1])

    else:
        msg = await callback.message.answer('Вы уже купили подписку', reply_markup=kb.back_to_home)
        await state.update_data(last_message_id=msg.message_id)
    await callback.answer()

@r.callback_query(F.data == 'support')
async def get_sub_category(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    last_message_id = data.get('last_message_id')

    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
        except Exception:
            None

    msg = await callback.message.answer('По всем вопросом пишите: @gothboycliqu9', reply_markup=kb.back_to_home)
    await state.update_data(last_message_id=msg.message_id)
    await callback.answer()



@r.callback_query(F.data == 'go_to_pay')
async def pay_button(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    item_id = int(data.get('item_id_to_pay'))
    details = await get_sub_details(item_id) # 0 - time, 1 - price, 2 - description, 3 - name
    last_message_id = data.get('last_message_id')

    if last_message_id is not None:
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=last_message_id)
        except Exception:
            None
    price = [LabeledPrice(label='XTR', amount=details[1])]
    msg = await callback.message.answer_invoice(
        title='Приватная подписка',
        description='Покупка доступа в мой приватный канал',
        prices=price,
        provider_token='',
        payload='private_channel',
        currency='XTR',
        reply_markup=kb.star_pay()
    )
    await state.update_data(last_message_id=msg.message_id)
    await callback.answer()

 
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):  
    await pre_checkout_query.answer(ok=True)
async def success_payment_handler(message: Message):  
    await message.answer(text="Вы успешно приобрели подписку", reply_markup=kb.back_to_home)
    await turn_on_sub(message.from_user.id)


r.pre_checkout_query.register(pre_checkout_handler)
r.message.register(success_payment_handler, F.successful_payment)