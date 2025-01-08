from app.database.models import async_session, User, Sub_Category
from sqlalchemy import select, func, update, values
from datetime import datetime, date
from dateutil.relativedelta import relativedelta



async def add_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, register_date=datetime.today().date()))
            await session.commit()


async def get_sub_status(tg_id):
    async with async_session() as session:
        data = await session.scalar(select(User.sub_status).where(User.tg_id == tg_id))
        if data:
            end_date = await session.scalar(select(User.date_of_end_sub).where(User.tg_id == tg_id))
            today_date = str(datetime.today().date())
            date1 = datetime.strptime(str(today_date), '%Y-%m-%d')
            date2 = datetime.strptime(str(end_date), '%Y-%m-%d')
            return f'Информация по подписке:\nStart date: {str(date1)[0:10]}\nEnd date: {str(date1)[0:10]}'
        else:
            return False

async def get_date_of_reg(tg_id):
    async with async_session() as session:
        data = await session.scalar(select(User.register_date).where(User.tg_id == tg_id))
        return data
    
async def get_sub_category():
    async with async_session() as session:
        return await session.scalars(select(Sub_Category))
    
async def get_sub_name(category_id):
    async with async_session() as session:
        return await session.scalar(select(Sub_Category.name).where(Sub_Category.id == category_id))
    
async def get_sub_description(category_id):
    async with async_session() as session:
        return await session.scalar(select(Sub_Category.description).where(Sub_Category.id == category_id))
    
async def get_sub_details(category_id):
    async with async_session() as session:
        details = []
        time = await session.scalar(select(Sub_Category.time).where(Sub_Category.id == category_id))
        price = await session.scalar(select(Sub_Category.price).where(Sub_Category.id == category_id))
        description = await session.scalar(select(Sub_Category.description).where(Sub_Category.id == category_id))
        name = await session.scalar(select(Sub_Category.name).where(Sub_Category.id == category_id))
        details.append(time)
        details.append(price)
        details.append(description)
        details.append(name)
        return details
    
async def turn_on_sub(tg_id):
    async with async_session() as session:
        today_date = datetime.today().date()
        date_of_end = today_date + relativedelta(months=3)
        update_dates = update(User).where(User.tg_id==tg_id).values(date_of_start_sub=today_date, date_of_end_sub=date_of_end,sub_status=True)
        await session.execute(update_dates)
        await session.commit()

async def check_sub_date(tg_id):
    async with async_session() as session:
        today_date = str(datetime.today().date())
        end_date = await session.scalar(select(User.date_of_end_sub).where(User.tg_id == tg_id))
        if end_date == 'none':
            return False
        today_date_obj = today_date
        end_date_obj = datetime.strptime(str(end_date), "%Y-%m-%d").date()
        return today_date_obj < end_date


async def turn_off_sub(tg_id):
    async with async_session() as session:
        end_date = await session.scalar(select(User.date_of_end_sub).where(User.tg_id == tg_id))
        today_date = str(datetime.today().date())
        date1 = datetime.strptime(str(today_date), '%Y-%m-%d')
        date2 = datetime.strptime(str(end_date), '%Y-%m-%d')
        if date1 > date2:
            data = update(User).where(User.tg_id == tg_id).values(date_of_start_sub='none', date_of_end_sub='none', sub_status=False)
            await session.execute(data)
            await session.commit()
