from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc
from .models import Book
from .schema import BookCreateModal, BookUpdateModal
from datetime import datetime


class BookService:
    """Function for get all books from db"""

    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    """Function for get book by id"""

    async def get_book(
        self,
        book_uuid: str,
        session: AsyncSession,
    ):
        statement = select(Book).where(Book.uuid == book_uuid)
        result = await session.execute(statement)
        book = result.first()
        return book if book is not None else None

    """Function for create book"""

    async def create_book(self, book_data: BookCreateModal, session: AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = Book(**book_data_dict)
        print(book_data_dict, "book_data_dict")
        new_book.published_date = datetime.strptime(
            book_data_dict["published_date"], "%Y-%m-%d"
        )
        print(new_book, "new_book")
        session.add(new_book)
        await session.commit()
        return new_book

    """Function for update book"""

    async def update_book(
        self, book_uuid: str, update_data: BookUpdateModal, session: AsyncSession
    ):
        book_to_update = await self.get_book(book_uuid, session)
        if book_to_update is None:
            return None
        update_data_dict = update_data.model_dump()

        for k, v in update_data_dict.items():
            setattr(book_to_update, k, v)

        await session.commit()
        return book_to_update

    """Function for delete book"""

    async def delete_book(self, book_uuid: str, session: AsyncSession):
        book_to_delete = await self.get_book(book_uuid, session)
        if book_to_delete is None:
            return None
        await session.delete(book_to_delete)
        await session.commit()
