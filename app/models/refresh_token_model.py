from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.session import Base
from app.models.user_model import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column( ForeignKey( "users.id", ondelete="CASCADE"), nullable=False )
    token: Mapped[str] = mapped_column(unique=True , nullable= False, index=True)
    created_at : Mapped[datetime] = mapped_column(DateTime , server_default=func.now())
    expires_at : Mapped[datetime] = mapped_column(DateTime)
    is_revoked: Mapped[bool] = mapped_column(default=False)
    user:Mapped["User"] =  relationship(back_populates="refresh_tokens")