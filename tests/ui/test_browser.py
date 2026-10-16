import allure
import pytest
from selenium import webdriver

from config import UI_BASE_URL


@pytest.mark.ui
@allure.title("Проверка запуска браузера")
@allure.story("Подготовка UI-автоматизации")
def test_open_kinopoisk() -> None:
    with allure.step("Открыть Кинопоиск в Chrome"):
        driver = webdriver.Chrome()
        try:
            driver.get(f"{UI_BASE_URL}/")
            assert "kinopoisk.ru" in driver.current_url
        finally:
            driver.quit()
