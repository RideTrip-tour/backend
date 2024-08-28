from tests.consts import AMOUNT_ITEMS_FOR_TEST


def _validate_result(result: list[dict], related: str) -> None:
    for item in result:
        if not isinstance(item.get("id", None), int):
            assert False, "id не является int"
        if not isinstance(item.get(related, None), list):
            assert False, f"{related} не содержит список  \n {item}"


async def _check_response_with_list_result(
    client,
    url: str,
    children: list[str] = [],
):
    response = await client.get(url)
    assert response.status_code == 200, f"Страница {url} не возвращает код 200"
    json_data = response.json()
    assert (
        "status" in json_data
    ), f'Тело ответа {url} не содержит "status". Получено: {json_data}'
    assert (
        json_data.get("status") == "access"
    ), f'Статус ответа {url} не "access". Получено: {json_data.get("status")}'
    assert (
        "result" in json_data
    ), f'Тело ответа {url} не содержит "result". Получено: {json_data}'
    result = json_data.get("result")
    assert len(result) == AMOUNT_ITEMS_FOR_TEST, (
        f'Тело ответа {url} содержит неверное количество записей в "result". '
        f"Ожидалось: {AMOUNT_ITEMS_FOR_TEST}, Получено: {len(result)}"
    )
    for child in children:
        _validate_result(result, child)


async def _check_response_with_item_result(client, url):
    response = await client.get(url)
    assert response.status_code == 200, (
        f"Страница {url} не возвращает код 200. "
        f"Получено: {response.status_code}"
    )
    json_data = response.json()
    assert "status" in json_data, f'Тело ответа {url} не содержит "status"'
    assert json_data.get("status") == "access"
    assert "result" in json_data, f'Тело ответа {url} не содержит "result"'


async def _check_response_with_wrong_param(client, url):
    response = await client.get(url)
    json_data = response.json()
    assert json_data.get("status") == "access"
    assert json_data.get("result") == [], (
        f'В "result" должен быть пустой список для {url}.'
        f"Получено: {json_data}"
    )
