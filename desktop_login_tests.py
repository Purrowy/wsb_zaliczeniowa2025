import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from test_data import TestData

class WindowsLoginTests(unittest.TestCase):
    
    def setUp(self):
        """Przygotuj webdriver do testów"""
        self.driver = webdriver.Chrome()
        #self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TestData.DEFAULT_TIMEOUT)
        
    def tearDown(self):
        """Wyłącz przeglądarkę po każdym teście"""
        if self.driver:
            self.driver.quit()
    
    def navigate_to_login(self):
        """Przejdź do strony logowania"""
        self.driver.get(TestData.LOGIN_URL)
        time.sleep(2)
    
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
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        time.sleep(3)
    
    def test_1_1_valid_login(self):
        """Test ID 1.1"""
        self.login_attempt(TestData.VALID_EMAIL, TestData.VALID_PASSWORD)
        
        # Sprawdź czy nastąpiło przekierowanie
        try:
            self.wait.until(EC.url_contains("/account"))
            current_url = self.driver.current_url
            self.assertIn("/account", current_url, "Przekierowanie na stronę konta")
            
        except TimeoutException:
            self.fail("Login failed or redirect did not occur")
    
    def test_1_2_invalid_password(self):
        """Test ID 1.2"""
        self.login_attempt(TestData.VALID_EMAIL, TestData.INVALID_PASSWORD)
        
        
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger")))
            self.assertTrue(error_element.is_displayed(), " Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony ")
    
    def test_1_3_invalid_email(self):
        """Test ID 1.3"""
        self.login_attempt(TestData.INVALID_EMAIL, TestData.VALID_PASSWORD)
        
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger")))
            self.assertTrue(error_element.is_displayed(), " Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony ")
    
    def test_1_4_invalid_email_no_password(self):
        """Test ID 1.4 """
        self.login_attempt(TestData.INVALID_EMAIL, "")
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_5_no_email_valid_password(self):
        """Test ID 1.5 """
        self.login_attempt("", TestData.VALID_PASSWORD)
        
        # Sprawdź czy pojawił się komunikat o braku e-mail
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), " Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony ")
    
    def test_1_6_valid_email_no_password(self):
        """Test ID 1.6 """
        self.login_attempt(TestData.VALID_EMAIL, "")
        
        # Sprawdź czy pojawił się komunikat błędu o brakującym haśle
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), "Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_7_no_email_invalid_password(self):
        """Test ID 1.7 """
        self.login_attempt("", TestData.INVALID_PASSWORD)
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), " Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony ")
    
    def test_1_8_no_credentials(self):
        """Test ID 1.8"""
        self.login_attempt("", "")
        
        # Sprawdź czy pojawił się komunikat z błędem
        try:
            error_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-danger, .invalid-feedback")))
            self.assertTrue(error_element.is_displayed(), " Komunikat błędu wyświetlony")
        except TimeoutException:
            self.fail("Komunikat błędu nie został wyświetlony")
    
    def test_1_17_logout(self):
        """Test ID 1.17 """
        
        self.login_attempt(TestData.VALID_EMAIL, TestData.VALID_PASSWORD)
        
        # Poczekaj na zalogowanie
        self.wait.until(EC.url_contains("/account"))
                
        # Rozwiń menu użytkownika
        user_menu = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-menu']")))
        user_menu.click()
        
        # Wybierz ‘sign out’
        sign_out_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-sign-out']")))
        sign_out_link.click()
        
        # Sprawdź czy nastąpiło przekierowanie
        try:
            self.wait.until(EC.url_contains("/auth/login"))
            current_url = self.driver.current_url
            self.assertIn("/auth/login", current_url, "Przekierowanie na stronę główną")
        except TimeoutException:
            self.fail("Nie wylogowano poprawnie lub nie nastąpiło przekierowanie na stronę główną")

if __name__ == "__main__":
    unittest.main()