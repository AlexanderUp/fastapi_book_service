from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserDB(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(50), unique=True)
    email: Mapped[str] = mapped_column(sa.String(50))
    first_name: Mapped[str] = mapped_column(sa.String(50))
    last_name: Mapped[str] = mapped_column(sa.String(50))
    disabled: Mapped[bool] = mapped_column(sa.Boolean(), default=False)
    password_hash: Mapped[str] = mapped_column(sa.String(255), nullable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
