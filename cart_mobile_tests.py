import unittest
import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy as By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from test_data import TestData

class MobileCartTests(unittest.TestCase):
    
    def setUp(self):
        """Przzygotowanie środowiska testowego"""
        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '13',
            'deviceName': 'Android Emulator',
            'browserName': 'Chrome',
            'newCommandTimeout': 300,
            'connectHardwareKeyboard': True
        }
        
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.wait = WebDriverWait(self.driver, TestData.DEFAULT_TIMEOUT)
        self.login()
        
    def tearDown(self):
        """Zamknij przeglądarkę po każdym teście"""
        if self.driver:
            self.driver.quit()
    
    def login(self):
        """Zaloguj przed testami"""
        self.driver.get(TestData.LOGIN_URL)
        time.sleep(3)
        
        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys(TestData.VALID_EMAIL)
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(TestData.VALID_PASSWORD)
        
        # Ukryj klawiaturę, jeśli jest otwarta
        self.driver.hide_keyboard()
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        
        # Poczekaj na przekierowanie do konta
        self.wait.until(EC.url_contains("/account"))
        
        # Przejdź do strony głównej
        self.driver.get(TestData.BASE_URL)
        time.sleep(3)
    
    def get_cart_count(self):
        """Sprawdź liczbę produktów w koszyku"""
        try:
            cart_badge = self.driver.find_element(By.CSS_SELECTOR, "[data-test='cart-quantity']")
            return int(cart_badge.text) if cart_badge.text else 0
        except (NoSuchElementException, ValueError):
            return 0
    
    def add_first_product_to_cart(self):
        """Dodaj pierwszy produkt do koszyka"""
        try:
            # Przesuń stronę, aby zobaczyć produkty
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(2)
            
            # Znajdź i kliknij pierwszy produkt
            first_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='product-01']")))
            first_product.click()
            time.sleep(3)
            
            # Przewiń stronę, aby przycisk dodawania do koszyka był widoczny
            self.driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(2)
            
            # Dodaj produkt do koszyka
            add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']")))
            add_to_cart_btn.click()
            time.sleep(3)
            
            # Wróć do strony głównej
            self.driver.get(TestData.BASE_URL)
            time.sleep(3)
            
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def test_2_4_add_single_product_mobile(self):
        """Test ID 2.4"""
        initial_count = self.get_cart_count()
        
        success = self.add_first_product_to_cart()
        self.assertTrue(success, "Dodano produkt do koszyka")
        
        # Sprawdź, czy liczba produktów w koszyku wzrosła
        final_count = self.get_cart_count()
        self.assertEqual(final_count, initial_count + 1, "Liczba produktów w koszyku powinna wzrosnąć o 1")
    
    def test_2_5_add_multiple_products_mobile(self):
        """Test ID 2.5"""
        initial_count = self.get_cart_count()
        products_added = 0
        
        try:
            # Przesuń stronę, aby zobaczyć produkty
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(2)
            
            first_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='product-01']")))
            first_product.click()
            time.sleep(3)
            
            self.driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(2)
            
            add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']")))
            add_to_cart_btn.click()
            time.sleep(3)
            products_added += 1
            
            # Wróć do strony głównej i dodaj drugi produkt
            self.driver.get(TestData.BASE_URL)
            time.sleep(3)
            
            self.driver.execute_script("window.scrollTo(0, 400);")
            time.sleep(2)
            
            second_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='product-02']")))
            second_product.click()
            time.sleep(3)
            
            self.driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(2)
            
            add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']")))
            add_to_cart_btn.click()
            time.sleep(3)
            products_added += 1
            
            # Wróć do strony głównej
            self.driver.get(TestData.BASE_URL)
            time.sleep(3)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, initial_count + products_added, f"Ilość powinna wzrosnąć o {products_added}")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się dodać wielu produktów do koszyka")
    
    def test_2_6_add_same_product_multiple_times_mobile(self):
        """Test ID 2.6"""
        initial_count = self.get_cart_count()
        
        try:
            # Dodaj ten sam produkt kilka razy
            for i in range(2):
                self.driver.execute_script("window.scrollTo(0, 300);")
                time.sleep(2)
                
                first_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='product-01']")))
                first_product.click()
                time.sleep(3)
                
                self.driver.execute_script("window.scrollTo(0, 500);")
                time.sleep(2)
                
                add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']")))
                add_to_cart_btn.click()
                time.sleep(3)
                
                self.driver.get(TestData.BASE_URL)
                time.sleep(3)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, initial_count + 2, "Liczba produktów w koszyku powinna wzrosnąć o 2")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się dodać tego samego produktu kilka razy do koszyka")
    
    def test_2_10_remove_product_from_cart_mobile(self):
        """Test ID 2.10"""
        # Dodaj produkt do koszyka
        self.add_first_product_to_cart()
        initial_count = self.get_cart_count()
        
        try:
            # Przejdź do koszyka
            cart_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-cart']")))
            cart_link.click()
            time.sleep(3)
            
            # Przewiń stronę, aby przycisk usuwania był widoczny
            self.driver.execute_script("window.scrollTo(0, 300);")
            time.sleep(2)
            
            # Usuń produkt z koszyka
            remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='remove-from-cart']")))
            remove_button.click()
            time.sleep(3)
            
            # Sprawdź, czy koszyk został zaktualizowany
            self.driver.get(TestData.BASE_URL)
            time.sleep(3)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, initial_count - 1, "Liczba produktów w koszyku powinna zmniejszyć się o 1")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się usunąć produktu z koszyka")
    
    def test_2_11_remove_multiple_products_mobile(self):
        """Test ID 2.11"""
        # Dodaj kilka produktów do koszyka
        self.test_2_5_add_multiple_products_mobile()
        initial_count = self.get_cart_count()
        
        try:
            # Przejdź do koszyka
            cart_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-cart']")))
            cart_link.click()
            time.sleep(3)
            
            # Usuń kilka produktów z koszyka
            removed_count = 0
            
            for i in range(2):  # Usuń dwa produkty
                try:
                    self.driver.execute_script("window.scrollTo(0, 300);")
                    time.sleep(2)
                    
                    remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='remove-from-cart']")))
                    remove_button.click()
                    time.sleep(3)
                    removed_count += 1
                except (TimeoutException, NoSuchElementException):
                    break
            
            # Sprawdź, czy koszyk został zaktualizowany
            self.driver.get(TestData.BASE_URL)
            time.sleep(3)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, initial_count - removed_count, f"Ilość produktów w koszyku powinna zmniejszyć się o {removed_count}")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się usunąć wielu produktów z koszyka")
    
    def test_2_12_empty_cart_mobile(self):
        """Test ID 2.12"""
        # Dodaj produkt do koszyka
        self.add_first_product_to_cart()
        
        try:
            # Przejdź do koszyka
            cart_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-cart']")))
            cart_link.click()
            time.sleep(3)
            
            # Usuń wszystkie produkty
            while True:
                try:
                    self.driver.execute_script("window.scrollTo(0, 300);")
                    time.sleep(2)
                    
                    remove_button = self.driver.find_element(By.CSS_SELECTOR, "[data-test='remove-from-cart']")
                    remove_button.click()
                    time.sleep(3)
                except NoSuchElementException:
                    break
            
            # Sprawdź, czy koszyk jest pusty
            self.driver.get(TestData.BASE_URL)
            time.sleep(3)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, 0, "Koszyk powinien być pusty")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się opróżnić koszyka")
    
    def test_2_13_cart_persistence_mobile(self):
        """Test ID 2.13"""
        # Dodaj produkt do koszyka
        self.add_first_product_to_cart()
        initial_count = self.get_cart_count()
        
        # Nawiguj do różnych kategorii
        self.driver.get(TestData.BASE_URL + "/category/hand-tools")
        time.sleep(3)
        
        self.driver.get(TestData.BASE_URL)
        time.sleep(3)
        
        # Sprawdź, czy liczba produktów w koszyku jest taka sama
        final_count = self.get_cart_count()
        self.assertEqual(final_count, initial_count, "Liczba produktów w koszyku powinna pozostać taka sama po nawigacji")

if __name__ == "__main__":
    unittest.main()