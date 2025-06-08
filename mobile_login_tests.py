import unittest
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from appium.options.android import UiAutomator2Options
from test_data import TestData

class MobileLoginTests(unittest.TestCase):
    
    def setUp(self):
        """Przygotuj Appium WebDriver do testów"""
        options = UiAutomator2Options().load_capabilities({
            'platformName': 'Android',
            'platformVersion': '13',
            'deviceName': 'Android Emulator',
            'browserName': 'Chrome',
            'newCommandTimeout': 300,
            'connectHardwareKeyboard': True
        })

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.wait = WebDriverWait(self.driver, TestData.DEFAULT_TIMEOUT)
        
    def tearDown(self):
        """Zamknij przeglądarkę po teście"""
        if self.driver:
            self.driver.quit()
    
    def navigate_to_login(self):
        """Przejdź do strony logowania"""
        self.driver.get(TestData.LOGIN_URL)
        time.sleep(3)
    
    def login_attempt(self, email="", password=""):
        """Zaloguj się z wykorzystaniem wskazanych danych"""
        self.navigate_to_login()
        
        if email:
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            email_field.clear()
            email_field.send_keys(email)
        
        if password:
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
            password_field.clear()
            password_field.send_keys(password)
        
        # Ukryj wyświetlanie klawiatury na ekranie telefonu
        self.driver.hide_keyboard()
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        time.sleep(3)
    
    def test_1_9_valid_login_mobile(self):
        """Test ID 1.9"""
        self.login_attempt(TestData.VALID_EMAIL, TestData.VALID_PASSWORD)
        
        # Sprawdź czy nastąpiło przekierowanie na stronę konta
        try:
            self.wait.until(EC.url_contains("/account"))
            current_url = self.driver.current_url
            self.assertIn("/account", current_url, "Przekierowanie na stronę konta")
            
            # Sprawdź czy użytkownik jest zalogowany
            user_menu = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-user-menu']")))
            self.assertTrue(user_menu.is_displayed(), "Menu użytkownika powinno być widoczne")
            
        except TimeoutException:
            self.fail("Login nieudany lub nie nastąpiło przekierowanie")
    
    def test_1_10_invalid_password_mobile(self):
        """Test ID 1.10"""
        self.login_attempt(TestData.VALID_EMAIL, TestData.INVALID_PASSWORD)
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_11_invalid_email_mobile(self):
        """Test ID 1.11"""
        self.login_attempt(TestData.INVALID_EMAIL, TestData.VALID_PASSWORD)
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_12_invalid_email_no_password_mobile(self):
        """Test ID 1.12 """
        self.login_attempt(TestData.INVALID_EMAIL, "")
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_13_no_email_valid_password_mobile(self):
        """Test ID 1.13: No email, valid password on mobile"""
        self.login_attempt("", TestData.VALID_PASSWORD)
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_14_valid_email_no_password_mobile(self):
        """Test ID 1.14"""
        self.login_attempt(TestData.VALID_EMAIL, "")
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_15_no_email_invalid_password_mobile(self):
        """Test ID 1.15"""
        self.login_attempt("", TestData.INVALID_PASSWORD)
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_16_no_credentials_mobile(self):
        """Test ID 1.16"""
        self.login_attempt("", "")
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_18_logout_mobile(self):
        """Test ID 1.18: User logout on mobile"""
        # First login
        self.login_attempt(TestData.VALID_EMAIL, TestData.VALID_PASSWORD)
        
        # Poczekaj na zalogowanie
        self.wait.until(EC.url_contains("/account"))
        
        # Przejdź na stronę główną
        self.driver.get(TestData.BASE_URL)
        time.sleep(2)
        
        # Rozwiń menu użytkownika
        user_menu = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-user-menu']")))
        user_menu.click()
        
        # Wybierz ‘sign out’
        sign_out_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-sign-out']")))
        sign_out_link.click()
        
        # Sprawdź czy nastąpiło przekierowanie
        try:
            self.wait.until(EC.url_contains("/auth/login"))
            current_url = self.driver.current_url
            self.assertIn("/auth/login", current_url, "Przekierowanie na stronę logowania po wylogowaniu")
        except TimeoutException:
            self.fail("Nie wylogowano lub nie nastąpił przekierowanie")

if __name__ == "__main__":
    unittest.main()
