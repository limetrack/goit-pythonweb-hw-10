from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from repositories.contacts import ContactsRepository
from schemas.contact import ContactCreate
from models.users import User


def _handle_integrity_error(e: IntegrityError):
    if "unique_contact_user" in str(e.orig):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Контакт з такою назвою вже існує.",
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Помилка цілісності даних.",
        )


class ContactsService:
    def __init__(self, db: AsyncSession):
        self.repository = ContactsRepository(db)

    async def get_contacts(
        self, user: User, skip: str, limit: str, name: str, email: str
    ):
        return await self.repository.get_contacts(user, skip, limit, name, email)

    async def get_contact_by_id(self, id: int, user: User):
        return await self.repository.get_contact_by_id(id, user)

    async def create_contact(self, body: ContactCreate, user: User):
        try:
            return await self.repository.create_contact(body, user)
        except IntegrityError as e:
            await self.repository.db.rollback()
            _handle_integrity_error(e)

    async def update_contact(self, id: int, contact: ContactCreate, user: User):
        try:
            return await self.repository.update_contact(id, contact, user)
        except IntegrityError as e:
            await self.repository.db.rollback()
            _handle_integrity_error(e)

    async def delete_contact(self, id: int, user: User):
        return await self.repository.delete_contact(id, user)

    async def get_upcoming_birthdays(self, user: User):
        return await self.repository.get_upcoming_birthdays(user)
