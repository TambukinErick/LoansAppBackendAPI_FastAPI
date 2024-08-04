import enum
import datetime
from typing import Optional, List, Literal, get_args
from sqlalchemy import ForeignKey, String, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..database import Base

ItemStatus = Literal["INSTORAGE", "LOANEDOUT", "DAMAGED", "LOST"]
TransactionStatus = Literal["ONGOING", "COMPLETED", "DAMAGED", "LOST"]

class Transaction(Base):
    __tablename__ = "Transaction"

    transactionId: Mapped[int] =  mapped_column(autoincrement=True, primary_key=True)
    itemCat: Mapped[str] = mapped_column(ForeignKey("LoanItem.itemCat"), primary_key=True)
    clientId: Mapped[int] = mapped_column(ForeignKey("Client.clientId"), primary_key=True)
    
    loaningMemberName: Mapped[str] = mapped_column(String(30))
    remarks: Mapped[Optional[str]] = mapped_column(String(254))
    dateLoaned: Mapped[datetime.datetime] 
    dueDate: Mapped[datetime.datetime]

    transactionStatus: Mapped[TransactionStatus] = mapped_column(Enum(
        *get_args(TransactionStatus),
        name="transactionstatus",
        create_constraint=True,
        validate_strings=True,
    ), nullable=False)

    dateReturned: Mapped[Optional[datetime.datetime]]
    overdueDays: Mapped[int] = mapped_column(default=0)
    overdueHours: Mapped[int] = mapped_column(default=0)
    overDueMinutes: Mapped[int] = mapped_column(default=0)
    recievingMemberName: Mapped[Optional[str]] = mapped_column(String(30))
    returnRemarks: Mapped[Optional[str]] = mapped_column(String(254))

    client: Mapped["Client"] = relationship(back_populates="loanitem")
    loanitem: Mapped["LoanItem"] = relationship(back_populates="client")


class LoanItem(Base):
    __tablename__ = "LoanItem"

    itemCat: Mapped[str] = mapped_column(String(8), primary_key=True)
    status: Mapped[ItemStatus] = mapped_column(Enum(
        *get_args(ItemStatus),
        name="itemstatus",
        create_constraint=True,
        validate_strings=True,
    ), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(254))
    dateReg: Mapped[datetime.datetime] = mapped_column(default=func.now())

    client: Mapped[List["Transaction"]] = relationship(back_populates="loanitem")


class Client(Base):
    __tablename__ = "Client"

    clientId: Mapped[int] = mapped_column(primary_key=True)
    lastName: Mapped[str] = mapped_column(String(25)) 
    firstName: Mapped[str] = mapped_column(String(25))
    middleInitial: Mapped[Optional[str]] = mapped_column(String(3))
    suffix: Mapped[Optional[str]] = mapped_column(String(3))
    contactNum: Mapped[str] = mapped_column(String(15), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    yearLevel: Mapped[int]
    course: Mapped[str] = mapped_column(String(10))
    hasWednesdayClasses: Mapped[bool] = mapped_column(default=True)
    graduating: Mapped[bool] = mapped_column(default=False)
    registeringMemberName: Mapped[str] = mapped_column(String(30))
    regDate: Mapped[datetime.datetime]

    borrowing: Mapped[bool] = mapped_column(default=False)
    blackListed: Mapped[bool] = mapped_column(default=False)
    tempBlackList: Mapped[bool] = mapped_column(default=False)
    holdOrder: Mapped[bool] = mapped_column(default=False)
    excuseLetter: Mapped[bool] = mapped_column(default=False)
    fineAmount: Mapped[int] = mapped_column(default=0)

    warningCount: Mapped[int] = mapped_column(default=0)
    borrowCount: Mapped[int] = mapped_column(default=0)

    loanitem: Mapped[List["Transaction"]] = relationship(back_populates="client")


class BlockOutDate(Base):
    __tablename__ = "BlockOutDate"
    blockId: Mapped[int] =  mapped_column(autoincrement=True, primary_key=True)
    dateBlocked: Mapped[datetime.date]
    remarks: Mapped[Optional[str]] = mapped_column(String(255))

class BlockOutTime(Base):
    __tablename__ = "BlockOutTime"
    blockId: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    dateBlocked: Mapped[datetime.date]
    startTime: Mapped[datetime.datetime]
    endTime: Mapped[datetime.datetime]
    remarks: Mapped[Optional[str]] = mapped_column(String(255))