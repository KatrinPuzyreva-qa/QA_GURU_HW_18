import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait



class RegistrationPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout=10)


    @allure.step("Open url")
    def open(self):
        self.driver.get('https://the-internet.herokuapp.com/login')
        self.driver.execute_script("$('#fixedban').remove()")
        self.driver.execute_script("$('footer').remove()")

    @allure.step("Fill username")
    def fill_username(self, text):
        self.driver.find_element(By.ID, 'username').send_keys(text)

    @allure.step("Fill password")
    def fill_password(self, value):
        self.driver.find_element(By.ID, 'password').send_keys(value)

    @allure.step("Click submit button")
    def submit(self):
        submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        self.driver.execute_script('arguments[0].click();', submit_button)

    @allure.step("Check form results")
    def should_have_submission_confirmation(self):
        error_message = self.driver.find_element(By.CSS_SELECTOR, '#flash-messages .flash.error')
        assert error_message.is_displayed(), "Error message not visible"
        assert "Your username is invalid!" in error_message.text, "Incorrect error message displayed"