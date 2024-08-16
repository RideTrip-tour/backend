from tests.consts import AMOUNT_ITEMS_FOR_TEST


async def _check_page_with_list_result(client, url):
    response = await client.get(url)
    assert response.status_code == 200, f"Страница {url} не возвращает код 200"
    assert (
        "status" in response.json()
    ), f'Тело ответа {url} не содержит "status"'
    assert response.json().get("status") == "access"
    assert (
        "result" in response.json()
    ), f'Тело ответа {url} не содержит "result"'
    assert (
        len(response.json().get("result")) == AMOUNT_ITEMS_FOR_TEST
    ), f'Тело ответа {url} содержит не верное количество записей в "result" '


async def _check_page_with_item_result(client, url, item_id, data):
    response = await client.get(url)
    assert response.status_code == 200, f"Страница {url} не возвращает код 200"
    assert (
        "status" in response.json()
    ), f'Тело ответа {url} не содержит "status"'
    assert response.json().get("status") == "access"
    assert (
        "result" in response.json()
    ), f'Тело ответа {url} не содержит "result"'
    assert response.json().get("result") == {
        "id": item_id,
        **data,
    }, f'Данные в "result" не соответствую объекту {url}'
