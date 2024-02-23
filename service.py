from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func

from models import Client, Mailing, Message
from schemas import ClientCreate, ClientUpdate, MailingCreate, MailingStatisticsResponse


class Service:

    @staticmethod
    async def create_client(
            client_data: ClientCreate,
            session: AsyncSession
    ) -> Client:
        """Create a new client in the database"""
        new_client = Client(
            phone_number=client_data.phone_number,
            mobile_operator_code=client_data.mobile_operator_code,
            tag=client_data.tag,
            timezone=client_data.timezone
        )
        session.add(new_client)
        await session.commit()
        await session.refresh(new_client)
        return new_client

    @staticmethod
    async def update_client(
            client_id: int,
            client_data: ClientUpdate,
            session: AsyncSession
    ) -> Client:
        """Update an existing client in the database"""
        query = (
            update(Client)
            .where(Client.id == client_id)
            .values(**client_data.dict(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(query)
        await session.commit()

        result = await session.execute(
            select(Client).where(Client.id == client_id)
        )
        return result.scalars().first()

    @staticmethod
    async def delete_client(client_id: int, session: AsyncSession) -> None:
        """Delete an existing client from the database"""
        query = delete(Client).where(Client.id == client_id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def create_mailing(
            mailing_data: MailingCreate,
            session: AsyncSession
    ) -> Mailing:
        """Create a new mailing in the database"""

        start_time_naive = mailing_data.start_time.replace(
            tzinfo=None) if mailing_data.start_time.tzinfo is not None else mailing_data.start_time
        end_time_naive = mailing_data.end_time.replace(
            tzinfo=None) if mailing_data.end_time.tzinfo is not None else mailing_data.end_time

        new_mailing = Mailing(
            message_text=mailing_data.message_text,
            start_time=start_time_naive,
            end_time=end_time_naive,
            filter_criteria=mailing_data.filter_criteria
        )
        session.add(new_mailing)
        await session.commit()
        await session.refresh(new_mailing)
        return new_mailing

    @staticmethod
    async def get_mailings_statistics(session: AsyncSession) -> list[dict]:
        """Get statistics for each mailing"""
        mailings_stats = []
        mailings = await session.execute(select(Mailing))
        for mailing in mailings.scalars().all():
            messages_stats = await session.execute(
                select(Message.status, func.count(Message.status))
                .where(Message.mailing_id == mailing.id)
                .group_by(Message.status)
            )
            stats = {status: count for status, count in messages_stats}
            mailings_stats.append({
                'mailing_id': mailing.id,
                'sent': stats.get('sent', 0),
                'delivered': stats.get('delivered', 0),
                'failed': stats.get('failed', 0)
            })
        return mailings_stats

    @staticmethod
    async def get_mailing_details_statistics(
            mailing_id: int,
            session: AsyncSession
    ) -> MailingStatisticsResponse:
        messages_stats = await session.execute(
            select(Message.status, func.count(Message.status))
            .where(Message.mailing_id == mailing_id)
            .group_by(Message.status)
        )
        stats = {status: count for status, count in messages_stats}
        return MailingStatisticsResponse(
            mailing_id=mailing_id,
            sent=stats.get('sent', 0),
            delivered=stats.get('delivered', 0),
            failed=stats.get('failed', 0)
        )

    @staticmethod
    async def update_mailing(
            mailing_id: int,
            mailing_data: MailingCreate,
            session: AsyncSession
    ) -> Mailing:
        query = (
            update(Mailing)
            .where(Mailing.id == mailing_id)
            .values(**mailing_data.dict())
            .execution_options(synchronize_session="fetch")
        )
        await session.execute(query)
        await session.commit()

        result = await session.execute(
            select(Mailing).where(Mailing.id == mailing_id)
        )
        return result.scalars().first()

    @staticmethod
    async def delete_mailing(mailing_id: int, session: AsyncSession) -> None:
        query = delete(Mailing).where(Mailing.id == mailing_id)
        await session.execute(query)
        await session.commit()
