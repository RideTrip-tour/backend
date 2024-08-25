import random

import pytest
from sqlalchemy import select

from src.core.tours import models

from ..consts import AMOUNT_ITEMS_FOR_TEST
from .utils import (
    _check_response_with_item_result,
    _check_response_with_list_result,
    _check_response_with_wrong_param,
)


@pytest.mark.asyncio
class TestActivities:
    base_url = "/v1/activities"

    async def test_list_activities(self, client, list_activities):
        url = self.base_url
        await _check_response_with_list_result(client, url, ["locations"])

    async def test_retrieve_activity(self, client, activity_with_locations):
        activity_id = activity_with_locations.id
        url = f"{self.base_url}/{activity_id}"
        await _check_response_with_item_result(client, url)

    async def test_list_activities_with_param_loc(
        self,
        activities_locations,
        client,
        session,
    ):
        location_id = activities_locations[
            random.choice(range(AMOUNT_ITEMS_FOR_TEST))
        ].get("location_id")
        url = f"{self.base_url}?loc={location_id}"
        response = await client.get(url)
        assert response.status_code == 200, (
            f"Страница {url} не возвращает код 200. "
            f"Получено: {response.status_code}"
        )
        # Получаем все id активностей из result
        activity_ids_result = [
            item.get("id") for item in response.json().get("result")
        ]

        # Получаем из БД id активностей для заданной локации
        query = (
            select(models.activities_locations_table.c.activity_id)
            .where(
                models.activities_locations_table.c.location_id == location_id
            )
            .order_by(models.activities_locations_table.c.activity_id)
        )
        result = await session.execute(query)
        activity_ids_current = result.scalars().unique().all()
        assert activity_ids_result == activity_ids_current, (
            f'В "result" есть Активность не относящаяся '
            f"к локации {location_id}"
        )

    async def test_list_activity_with_wrong_param(self, client, session):
        url = f"{self.base_url}?loc=9999"
        await _check_response_with_wrong_param(client, url)


@pytest.mark.asyncio
class TestLocation:
    base_url = "/v1/locations"

    async def test_list_locations(self, client, list_locations):
        url = self.base_url
        await _check_response_with_list_result(client, url, ["activities"])

    async def test_retrieve_location(
        self,
        client,
        location_with_activity,
    ):
        location_id = location_with_activity.id
        url = f"{self.base_url}/{location_id}"
        await _check_response_with_item_result(
            client,
            url,
        )

    async def test_list_location_with_param_act(
        self, activities_locations, client, session
    ):
        activity_id = activities_locations[
            random.choice(range(AMOUNT_ITEMS_FOR_TEST))
        ].get("activity_id")
        url = f"{self.base_url}?act={activity_id}"
        response = await client.get(url)
        assert response.status_code == 200, (
            f"Страница {url} не возвращает код 200. "
            f"Получено: {response.status_code}"
        )
        # Получаем все id локаций из result
        location_ids_result = [
            item.get("id") for item in response.json().get("result")
        ]

        # Получаем из БД id локаций для заданной активности
        query = select(models.activities_locations_table.c.location_id).where(
            models.activities_locations_table.c.activity_id == activity_id
        )
        result = await session.execute(query)
        location_ids_current = result.scalars().unique().all()
        assert set(location_ids_result) == set(location_ids_current), (
            f'В "result" есть Локация не относящаяся к '
            f"активности {activity_id}"
        )

    async def test_list_location_with_wrong_param(self, client, session):
        url = f"{self.base_url}?act=9999"
        await _check_response_with_wrong_param(client, url)


class TestTours:
    base_url = "/v1/tours"

    async def test_list_tours(self, client, list_tours):
        url = self.base_url
        await _check_response_with_list_result(client, url)

    async def test_retrieve_tour(self, client, tour):
        tour_id = tour.id
        url = f"{self.base_url}/{tour_id}"
        await _check_response_with_item_result(
            client,
            url,
        )

    async def test_list_tour_with_param_act(self, client, session, list_tours):
        activity_id = list_tours[
            random.choice(range(AMOUNT_ITEMS_FOR_TEST))
        ].activity_id
        url = f"{self.base_url}?act={activity_id}"
        response = await client.get(url)
        assert response.status_code == 200, (
            f"Страница {url} не возвращает код 200. "
            f"Получено: {response.status_code}"
        )

        # Получаем все id туров из result
        location_ids_result = [
            item.get("id") for item in response.json().get("result")
        ]

        # Получаем из БД id туров для заданной активности
        query = select(models.Tour.id).where(
            models.Tour.activity_id == activity_id
        )
        result = await session.execute(query)
        location_ids_current = result.scalars().unique().all()
        assert set(location_ids_result) == set(location_ids_current), (
            f'В "result" есть Тур(ы) не относящаяся к '
            f"активности {activity_id}"
        )

    async def test_list_tour_with_param_loc(self, client, session, list_tours):
        location_id = list_tours[
            random.choice(range(AMOUNT_ITEMS_FOR_TEST))
        ].target_location_id
        url = f"{self.base_url}?loc={location_id}"
        response = await client.get(url)
        assert response.status_code == 200, (
            f"Страница {url} не возвращает код 200. "
            f"Получено: {response.status_code}"
        )

        # Получаем все id туров из result
        location_ids_result = [
            item.get("id") for item in response.json().get("result")
        ]

        # Получаем из БД id туров для заданной активности
        query = select(models.Tour.id).where(
            models.Tour.target_location_id == location_id
        )
        result = await session.execute(query)
        location_ids_current = result.scalars().unique().all()
        assert set(location_ids_result) == set(location_ids_current), (
            f'В "result" есть Тур(ы) не относящаяся к '
            f"активности {location_id}"
        )

    async def test_list_tours_with_wrong_param(
        self, client, session, list_tours
    ):
        url = f"{self.base_url}?act=9999"
        await _check_response_with_wrong_param(client, url)
        url = f"{self.base_url}?loc=9999"
        await _check_response_with_wrong_param(client, url)
        url = f"{self.base_url}?act=9999&loc=9999"
        await _check_response_with_wrong_param(client, url)
