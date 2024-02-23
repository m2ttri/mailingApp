from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ClientCreate(BaseModel):
    phone_number: str
    mobile_operator_code: str
    tag: str
    timezone: str


class ClientResponse(BaseModel):
    id: int
    phone_number: str
    mobile_operator_code: str
    tag: str
    timezone: str

    class Config:
        orm_mode = True


class ClientUpdate(BaseModel):
    phone_number: Optional[str] = None
    mobile_operator_code: Optional[str] = None
    tag: Optional[str] = None
    timezone: Optional[str] = None


class MailingCreate(BaseModel):
    message_text: str
    start_time: datetime
    end_time: datetime
    filter_criteria: Optional[dict] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class MailingResponse(BaseModel):
    id: int
    message_text: str
    start_time: datetime
    end_time: datetime
    filter_criteria: dict

    class Config:
        orm_mode = True


class MailingStatisticsResponse(BaseModel):
    mailing_id: int
    sent: int
    delivered: int
    failed: int

    class Config:
        orm_mode = True
