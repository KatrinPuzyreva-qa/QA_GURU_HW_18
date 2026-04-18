import os
import allure
import pytest
from pages.registration_page import RegistrationPage
from tests.conftest import setup_browser


@allure.title("Successful fill form")
def test_fill_form(setup_browser, request):
    cli_url = request.config.getoption("--site-url")

    site_url = cli_url if cli_url is not None else os.getenv("SITE_URL")


    if not site_url:
        pytest.skip("URL сайта не указан. Пропускаем тест.")

    registration_page = RegistrationPage(setup_browser, site_url)

    with allure.step("Открываем форму регистрации"):
        registration_page.open()

    with allure.step("Заполняем поля формы"):
        registration_page.fill_username('Таисия')
        registration_page.fill_password('12345678')
        registration_page.submit()

    with allure.step("Проверяем результат отправки"):
        registration_page.should_have_submission_confirmation()
