import pytest

from tests.tours.conftest import tour_data


@pytest.mark.asyncio
class TestTour:
    async def test_list_tours(self, client, list_tours):
        response = await client.get('/v1/tours/')
        assert response.status_code == 200
        assert 'status' in response.json()
        assert response.json().get('status') == 'access'
        assert 'result' in response.json()
        assert len(response.json().get('result')) == 10


    async def test_retrieve_tour(self, client, tour, tour_data):
        response = await client.get(f'/v1/tours/{tour.id}/')
        assert response.status_code == 200
        assert 'status' in response.json()
        assert response.json().get('status') == 'access'
        assert 'result' in response.json()
        assert response.json().get('result') == {'id': tour.id,
                                                  **tour_data}


@pytest.mark.asyncio
class TestLocation:
    async def test_list_locations(self, client, list_locations):
        response = await client.get('/v1/locations/')
        assert response.status_code == 200
        assert 'status' in response.json()
        assert response.json().get('status') == 'access'
        assert 'result' in response.json()
        assert len(response.json().get('result')) == 10
