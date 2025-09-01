from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.storage import models
from app.utils.enums import Role


class UserRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_or_create(self, tg_id: int) -> models.User:
        result = await self.session.execute(select(models.User).where(models.User.tg_id == tg_id))
        user = result.scalar_one_or_none()
        if user is None:
            user = models.User(tg_id=tg_id, role=Role.unknown)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return user
