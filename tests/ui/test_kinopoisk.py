import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from config import UI_BASE_URL


@pytest.mark.ui
@allure.title("UI-03 — Отображение названия фильма «1+1»")
@allure.story("Карточка фильма")
def test_movie_title_is_displayed() -> None:
    """Проверка названия и года фильма в карточке."""

    driver = webdriver.Chrome()

    try:
        with allure.step("Открыть карточку фильма «1+1»"):
            driver.get(f"{UI_BASE_URL}/film/535341/")

        with allure.step("Проверить название фильма и год выпуска"):
            wait = WebDriverWait(driver, 20)

            title = wait.until(lambda browser: browser.find_element(By.TAG_NAME, "h1"))

            assert "1+1" in title.text
            assert "2011" in title.text

    finally:
        driver.quit()


@pytest.mark.ui
@allure.title("UI-02 — Переход из поиска в карточку фильма")
@allure.story("Поиск и навигация")
def test_open_movie_from_search() -> None:
    """Проверка перехода к фильму «1+1» из результатов поиска."""

    driver = webdriver.Chrome()

    try:
        with allure.step("Открыть результаты поиска фильма «1+1»"):
            driver.get(f"{UI_BASE_URL}/new-search/?text=1%2B1")

        with allure.step("Найти и открыть фильм «1+1»"):
            wait = WebDriverWait(driver, 20)
            movie_link = wait.until(
                lambda browser: browser.find_element(
                    By.CSS_SELECTOR, 'a[href*="/film/535341/"]'
                )
            )
            movie_link.click()

        with allure.step("Проверить переход в карточку фильма"):
            wait.until(lambda browser: "/film/535341/" in browser.current_url)
            assert "/film/535341/" in driver.current_url

    finally:
        driver.quit()


@pytest.mark.ui
@allure.title("UI-01 — Поиск фильма «1+1»")
@allure.story("Поиск фильмов")
def test_search_movie() -> None:
    """Проверка поиска фильма через строку поиска."""

    driver = webdriver.Chrome()

    try:
        with allure.step("Открыть главную страницу Кинопоиска"):
            driver.get(f"{UI_BASE_URL}/")

        with allure.step("Ввести название фильма и запустить поиск"):
            wait = WebDriverWait(driver, 20)

            search_field = wait.until(
                lambda browser: browser.find_element(
                    By.CSS_SELECTOR, 'input[placeholder*="Фильмы"]'
                )
            )

            search_field.send_keys("1+1")
            search_field.send_keys(Keys.ENTER)

        with allure.step("Проверить появление фильма в результатах"):
            wait.until(lambda browser: "/new-search/" in browser.current_url)

            movie_link = wait.until(
                lambda browser: browser.find_element(
                    By.CSS_SELECTOR, 'a[href*="/film/535341/"]'
                )
            )

            assert movie_link.is_displayed()

    finally:
        driver.quit()


@pytest.mark.ui
@allure.title("UI-04 — Открытие раздела «Фильмы»")
@allure.story("Навигация по каталогу")
def test_open_movies_section() -> None:
    """Проверка перехода в каталог фильмов через меню."""

    driver = webdriver.Chrome()

    try:
        with allure.step("Открыть главную страницу Кинопоиска"):
            driver.get(f"{UI_BASE_URL}/")

        with allure.step("Открыть каталог фильмов"):
            driver.get(f"{UI_BASE_URL}/lists/categories/movies/1/")
            wait = WebDriverWait(driver, 20)

        with allure.step("Проверить открытие каталога фильмов"):
            wait.until(
                lambda browser: "/lists/categories/movies/1/" in browser.current_url
            )

            collection = wait.until(
                lambda browser: browser.find_element(
                    By.XPATH,
                    "//*[contains(text(), '250 лучших фильмов')]",
                )
            )
            assert collection.is_displayed()

    finally:
        driver.quit()


@pytest.mark.ui
@allure.title("UI-05 — Открытие раздела «Сериалы»")
@allure.story("Навигация по каталогу")
def test_open_series_section() -> None:
    """Проверка перехода из раздела фильмов в раздел сериалов."""

    driver = webdriver.Chrome()

    try:
        with allure.step("Открыть раздел «Фильмы»"):
            driver.get(f"{UI_BASE_URL}/lists/categories/movies/1/")

        with allure.step("Нажать на вкладку «Сериалы»"):
            wait = WebDriverWait(driver, 20)

            series_link = wait.until(
                lambda browser: browser.find_element(
                    By.CSS_SELECTOR,
                    'a[href*="/lists/categories/movies/3/"]',
                )
            )
            series_link.click()

        with allure.step("Проверить переход в раздел сериалов"):
            wait.until(
                lambda browser: "/lists/categories/movies/3/" in browser.current_url
            )

        with allure.step("Проверить наличие подборки сериалов"):
            collection = wait.until(
                lambda browser: browser.find_element(
                    By.XPATH,
                    "//*[contains(text(), '250 лучших сериалов')]",
                )
            )
            assert collection.is_displayed()

    finally:
        driver.quit()
