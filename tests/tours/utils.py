from tests.consts import AMOUNT_ITEMS_FOR_TEST


def _validate_result(result: list[dict], related: str):
    for item in result:
        if not isinstance(item.get("id", None), int):
            assert False, "id не является int"
        if not isinstance(item.get("name", None), str):
            assert False, "name не является str"
        if not isinstance(item.get(related, None), list):
            assert False, f"{related} не содержит список"
    return True


async def _check_page_with_list_result(client, url: str, related: str):
    response = await client.get(url)
    assert response.status_code == 200, f"Страница {url} не возвращает код 200"
    assert (
        "status" in response.json()
    ), f'Тело ответа {url} не содержит "status"'
    assert response.json().get("status") == "access"
    assert (
        "result" in response.json()
    ), f'Тело ответа {url} не содержит "result"'
    result = response.json().get("result")
    assert (
        len(result) == AMOUNT_ITEMS_FOR_TEST
    ), f'Тело ответа {url} содержит не верное количество записей в "result" '

    assert _validate_result(result, related)


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
