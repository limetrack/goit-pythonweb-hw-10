from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, extract

from typing import List
from datetime import datetime, timedelta

from models.users import User
from models.contacts import Contact
from schemas.contact import ContactCreate


class ContactsRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self,
        user: User,
        skip: int = 0,
        limit: int = 10,
        name: str = None,
        email: str = None,
    ) -> List[Contact]:
        stmt = select(Contact).filter_by(user_id=user.id).offset(skip).limit(limit)
        if name:
            stmt = stmt.filter(
                or_(
                    Contact.first_name.ilike(f"%{name}%"),
                    Contact.last_name.ilike(f"%{name}%"),
                )
            )
        if email:
            stmt = stmt.filter(Contact.email.ilike(f"%{email}%"))
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()

    async def get_contact_by_id(self, id: int, user: User) -> Contact | None:
        stmt = select(Contact).filter_by(id=id, user_id=user.id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactCreate, user: User) -> Contact:
        contact = Contact(**body.model_dump(exclude_unset=True), user_id=user.id)
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, id: int, body: ContactCreate, user: User
    ) -> Contact | None:
        contact = await self.get_contact_by_id(id, user)
        if not contact:
            return None
        for key, value in body.dict().items():
            setattr(contact, key, value)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def delete_contact(self, id: int, user: User) -> Contact | None:
        contact = await self.get_contact_by_id(id, user)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthdays(self, user: User) -> List[Contact]:
        today = datetime.today().date()
        today_month = today.month
        today_day = today.day

        next_week = today + timedelta(days=7)
        next_week_month = next_week.month
        next_week_day = next_week.day

        stmt = (
            select(Contact)
            .filter_by(user_id=user.id)
            .filter(
                and_(
                    and_(
                        extract("month", Contact.birthday) == today_month,
                        extract("day", Contact.birthday) >= today_day,
                    ),
                    and_(
                        extract("month", Contact.birthday) == next_week_month,
                        extract("day", Contact.birthday) <= next_week_day,
                    ),
                )
            )
        )

        result = await self.db.execute(stmt)

        return result.scalars().all()
