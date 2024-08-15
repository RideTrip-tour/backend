import pytest

from .utils import _check_page_with_list_result, _check_page_with_item_result


@pytest.mark.asyncio
class TestActivities:
    async def test_list_activities(self, client, list_activities):
        url = '/v1/activities/'
        await _check_page_with_list_result(client, url)


    async def test_retrieve_activity(self, client, activity, activity_data):
        activity_id = activity.id
        url = f'/v1/activities/{activity_id}/'
        await _check_page_with_item_result(client, url, activity_id, activity_data)


@pytest.mark.asyncio
class TestLocation:
    async def test_list_locations(self, client, list_locations):
        url = '/v1/locations/'
        await _check_page_with_list_result(client, url)

    async def test_retrieve_location(self, client, location, location_data):
        location_id = location.id
        url = f'/v1/locations/{location.id}/'
        await _check_page_with_item_result(client, url, location_id, location_data)