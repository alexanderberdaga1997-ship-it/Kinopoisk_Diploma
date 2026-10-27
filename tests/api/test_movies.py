
import allure
import pytest
import requests

from config import API_TOKEN, BASE_URL


@pytest.mark.api
@allure.title("API-01 — Получение списка фильмов")
@allure.story("Получение информации о фильмах")
def test_get_movies_list() -> None:
    """Проверка успешного получения списка фильмов."""

    with allure.step("Проверить наличие API-токена в конфигурации"):
        assert API_TOKEN, "Не задана переменная KINOPOISK_API_TOKEN"

    with allure.step("Отправить GET-запрос для получения фильмов"):
        response = requests.get(
            f"{BASE_URL}/movie",
            headers={"X-API-KEY": API_TOKEN},
            timeout=20,
        )

    with allure.step("Проверить HTTP-статус 200"):
        assert response.status_code == 200, response.text

    with allure.step("Проверить наличие фильмов в ответе"):
        data = response.json()
        assert isinstance(data.get("docs"), list)
        assert len(data["docs"]) > 0

    with allure.step("Проверить данные первого фильма"):
        first_movie = data["docs"][0]
        assert first_movie.get("id") is not None
        assert first_movie.get("name")

    with allure.step("Проверить информацию о пагинации"):
        for field in ("total", "page", "limit", "pages"):
            assert field in data, f"Нет поля {field}"


@pytest.mark.api
@allure.title("API-02 — Получение фильма по ID")
@allure.story("Получение информации о фильмах")
def test_get_movie_by_id() -> None:
    """Проверка получения фильма «1+1» по ID."""

    with allure.step("Проверить наличие API-токена в конфигурации"):
        assert API_TOKEN, "Не задана переменная KINOPOISK_API_TOKEN"

    with allure.step("Отправить GET-запрос для фильма с ID 535341"):
        response = requests.get(
            f"{BASE_URL}/movie/535341",
            headers={"X-API-KEY": API_TOKEN},
            timeout=20,
        )

    with allure.step("Проверить HTTP-статус 200"):
        assert response.status_code == 200, response.text

    with allure.step("Проверить ID фильма"):
        data = response.json()
        assert data.get("id") == 535341

    with allure.step("Проверить название фильма"):
        assert data.get("name") == "1+1"

    with allure.step("Проверить год выпуска"):
        assert data.get("year") == 2011


@pytest.mark.api
@allure.title("API-03 — Поиск фильмов по названию")
@allure.story("Поиск фильмов")
def test_search_movie_by_title() -> None:
    """Проверка поиска фильма «Матрица»."""

    with allure.step("Проверить наличие API-токена в конфигурации"):
        assert API_TOKEN, "Не задана переменная KINOPOISK_API_TOKEN"

    with allure.step("Найти фильмы по запросу «матрица»"):
        response = requests.get(
            f"{BASE_URL}/movie/search",
            params={"query": "матрица"},
            headers={"X-API-KEY": API_TOKEN},
            timeout=20,
        )

    with allure.step("Проверить HTTP-статус 200"):
        assert response.status_code == 200, response.text

    with allure.step("Проверить наличие результатов поиска"):
        data = response.json()
        assert isinstance(data.get("docs"), list)
        assert len(data["docs"]) > 0

    with allure.step("Проверить соответствие названию фильма"):
        movie_names = [movie.get("name", "") for movie in data["docs"]]
        assert any("матрица" in name.lower() for name in movie_names)

    with allure.step("Проверить наличие ID и названия"):
        first_movie = data["docs"][0]
        assert first_movie.get("id") is not None
        assert first_movie.get("name")


@pytest.mark.api
@allure.title("API-04 — Получение фильмов без токена")
@allure.story("Проверка авторизации API")
def test_get_movies_without_token() -> None:
    """Проверка отказа в доступе без API-токена."""

    with allure.step("Отправить GET-запрос без заголовка X-API-KEY"):
        response = requests.get(
            f"{BASE_URL}/movie",
            timeout=20,
        )

    with allure.step("Проверить HTTP-статус 401"):
        assert response.status_code == 401, response.text

    with allure.step("Проверить текст ошибки Unauthorized"):
        data = response.json()
        assert data.get("error") == "Unauthorized"

    with allure.step("Проверить сообщение об отсутствующем токене"):
        assert "не указан токен" in data.get("message", "").lower()


@pytest.mark.api
@allure.title("API-05 — Получение фильмов с неверным токеном")
@allure.story("Проверка авторизации API")
def test_get_movies_with_invalid_token() -> None:
    """Проверка отказа в доступе при неверном API-токене."""

    with allure.step("Отправить GET-запрос с неверным токеном"):
        response = requests.get(
            f"{BASE_URL}/movie",
            headers={"X-API-KEY": "invalid_test_token_123"},
            timeout=20,
        )

    with allure.step("Проверить HTTP-статус 401"):
        assert response.status_code == 401, response.text

    with allure.step("Проверить тип ошибки Unauthorized"):
        data = response.json()
        assert data.get("error") == "Unauthorized"

    with allure.step("Проверить код ошибки в JSON"):
        assert data.get("statusCode") == 401
