import pytest


@pytest.mark.asyncio
class TestActivities:
    async def test_list_activities(self, client, list_activities):
        response = await client.get('/v1/activities/')
        assert response.status_code == 200
        assert 'status' in response.json()
        assert response.json().get('status') == 'access'
        assert 'result' in response.json()
        assert len(response.json().get('result')) == 10


    async def test_retrieve_activity(self, client, activity, activity_data):
        response = await client.get(f'/v1/activities/{activity.id}/')
        assert response.status_code == 200
        assert 'status' in response.json()
        assert response.json().get('status') == 'access'
        assert 'result' in response.json()
        assert response.json().get('result') == {'id': activity.id,
                                                  **activity_data}


@pytest.mark.asyncio
class TestLocation:
    async def test_list_locations(self, client, list_locations):
        response = await client.get('/v1/locations/')
        assert response.status_code == 200
        assert 'status' in response.json()
        assert response.json().get('status') == 'access'
        assert 'result' in response.json()
        assert len(response.json().get('result')) == 10
