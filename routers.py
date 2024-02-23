from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from service import Service
from schemas import (ClientCreate,
                     ClientResponse,
                     ClientUpdate,
                     MailingCreate,
                     MailingResponse,
                     MailingStatisticsResponse)

router = APIRouter()


@router.post(
    '/clients/',
    response_model=ClientResponse,
    summary='Create a new client',
    description="Add a new client to the database with all their attributes",
    response_description="The created client's data",
    status_code=status.HTTP_201_CREATED
)
async def create_client(
        client_data: ClientCreate,
        session: AsyncSession = Depends(get_async_session)
) -> ClientResponse:
    """Create a new client with the provided attributes"""
    new_client = await Service.create_client(client_data, session)
    return ClientResponse.from_orm(new_client)


@router.put(
    '/clients/{client_id}/',
    response_model=ClientResponse,
    summary='Update an existing client',
    description="Update an existing client's attributes in the database",
    response_description="The updated client's data",
    status_code=status.HTTP_200_OK
)
async def update_client(
        client_id: int,
        client_data: ClientUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> ClientResponse:
    """Update an existing client with the provided attributes"""
    updated_client = await Service.update_client(
        client_id,
        client_data,
        session
    )
    return ClientResponse.from_orm(updated_client)


@router.delete(
    '/clients/{client_id}/',
    summary='Delete a client',
    description="Remove a client from the database",
    response_description="No content, indicates successful deletion",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_client(
        client_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Delete an existing client from the database"""
    await Service.delete_client(client_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    '/mailings/',
    response_model=MailingResponse,
    summary='Create a new mailing',
    description="Create a new mailing with the specified criteria",
    response_description="The data of the created mailing",
    status_code=status.HTTP_201_CREATED
)
async def create_mailing(
        mailing_data: MailingCreate,
        session: AsyncSession = Depends(get_async_session)
):
    new_mailing = await Service.create_mailing(mailing_data, session)
    return new_mailing


@router.get(
    '/mailings/statistics',
    response_model=List[MailingStatisticsResponse],
    summary='Get mailings statistics',
    description="Retrieve statistics for each mailing",
    response_description="A list of mailings with their respective statistics",
)
async def get_mailings_statistics(session: AsyncSession = Depends(get_async_session)):
    statistics = await Service.get_mailings_statistics(session)
    return statistics


@router.get(
    '/mailings/{mailing_id}/statistics',
    response_model=MailingStatisticsResponse,
    summary='Get detailed mailing statistics',
    description="Get detailed statistics for a specific mailing",
    response_description="Detailed statistics of the mailing"
)
async def get_mailing_details_statistics(
        mailing_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await Service.get_mailing_details_statistics(mailing_id, session)


@router.put(
    '/mailings/{mailing_id}/',
    response_model=MailingResponse,
    summary='Update a mailing',
    description="Update the attributes of a mailing",
    response_description="The updated mailing's data",
    status_code=status.HTTP_200_OK
)
async def update_mailing(
        mailing_id: int,
        mailing_data: MailingCreate,
        session: AsyncSession = Depends(get_async_session)
):
    updated_mailing = await Service.update_mailing(
        mailing_id,
        mailing_data,
        session
    )
    return MailingResponse.from_orm(updated_mailing)


@router.delete(
    '/mailings/{mailing_id}/',
    summary='Delete a mailing',
    description="Delete a mailing by its ID",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_mailing(
        mailing_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    await Service.delete_mailing(mailing_id, session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
