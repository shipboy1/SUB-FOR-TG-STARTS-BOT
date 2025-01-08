from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///tgdb.sqlite3')
# нужно в добавок заинсталить pip install greenlet
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    register_date: Mapped[str] = mapped_column(String(20))
    sub_status: Mapped[bool] = mapped_column(default=False)
    date_of_start_sub: Mapped[str] = mapped_column(String(15), default='none')
    date_of_end_sub: Mapped[str] = mapped_column(String(15), default='none')


class Sub_Category(Base):
    __tablename__ = 'sub_categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    description: Mapped[str] = mapped_column(String(150)) # макс 150 символов
    time: Mapped[int] = mapped_column() # число в месяцах
    price: Mapped[int] = mapped_column() # число в звездах



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
