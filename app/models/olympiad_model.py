from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column , relationship
from enum import Enum
from sqlalchemy import DateTime,ForeignKey,Enum as SqlEnum
from datetime import datetime
from typing import List
from sqlalchemy.sql import func


   
class Olympiad(Base):
    
    __tablename__="olympiads"
    
    
    id:Mapped[int]=mapped_column(primary_key=True)
    

    title:Mapped[str] = mapped_column()

    description:Mapped[str] = mapped_column()

    registration_start:Mapped[datetime] = mapped_column()

    registration_end:Mapped[datetime] = mapped_column()

    exam_date:Mapped[datetime] = mapped_column()

    is_active:Mapped[bool]=mapped_column(default=True)

    created_by_id:Mapped[int | None]=mapped_column(ForeignKey("users.id",ondelete="SET NULL"), nullable=True)

    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now())

    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now())
    
    creator:Mapped["User"]=relationship(back_populates="created_olympiads")
    
    applications:Mapped[List["Application"]]=relationship(back_populates="olympiad")
    