import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from test_data import TestData

class WindowsCartTests(unittest.TestCase):
    
    def setUp(self):
        """Przygotuj Chrome WebDriver"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, TestData.DEFAULT_TIMEOUT)
        self.login()
        
    def tearDown(self):
        """Zamknij przeglądarkę po każdym teście"""
        if self.driver:
            self.driver.quit()
    
    def login(self):
        """Zaloguj przed każdym testem"""
        self.driver.get(TestData.LOGIN_URL)
        time.sleep(2)
        
        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys(TestData.VALID_EMAIL)
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(TestData.VALID_PASSWORD)
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        login_button.click()
        
        # Poczekaj na zalogowanie
        self.wait.until(EC.url_contains("/account"))
        
        # Przejdć do strony głównej
        self.driver.get(TestData.BASE_URL)
        time.sleep(2)
    
    def get_cart_count(self):
        """Sprawdź ilość przedmiotów w koszyku"""
        try:
            cart_badge = self.driver.find_element(By.CSS_SELECTOR, "[data-test='cart-quantity']")
            return int(cart_badge.text) if cart_badge.text else 0
        except (NoSuchElementException, ValueError):
            return 0
    
    def add_first_product_to_cart(self):
        """Dodaj pierwszy produkt do koszyka"""
        try:
            # Znajdź pierwszy produkt
            first_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='product-01']")))
            first_product.click()
            time.sleep(2)
            
            # Dodaj do koszyka
            add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']")))
            add_to_cart_btn.click()
            time.sleep(2)
            
            # Wróć na stronę głóną
            self.driver.get(TestData.BASE_URL)
            time.sleep(2)
            
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def test_2_1_add_single_product(self):
        """Test ID 2.1"""
        initial_count = self.get_cart_count()
        
        success = self.add_first_product_to_cart()
        self.assertTrue(success, "Dodano produkt do koszyka")
        
        # Sprawdź ilość przedmiotów w koszyku
        final_count = self.get_cart_count()
        self.assertEqual(final_count, initial_count + 1, "Liczba powinna wzrosnąć o 1")
    
    def test_2_2_add_multiple_products(self):
        """Test ID 2.2"""
        initial_count = self.get_cart_count()
        products_added = 0
        
        try:
            # Dodaj pierwszy produkt
            first_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='product-01']")))
            first_product.click()
            time.sleep(2)
            
            add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']")))
            add_to_cart_btn.click()
            time.sleep(2)
            products_added += 1
            
            # Wróć na stronę główną
            self.driver.get(TestData.BASE_URL)
            time.sleep(2)
            
            second_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='product-02']")))
            second_product.click()
            time.sleep(2)
            
            add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']")))
            add_to_cart_btn.click()
            time.sleep(2)
            products_added += 1
            
            # Wróć na stronę główną
            self.driver.get(TestData.BASE_URL)
            time.sleep(2)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, initial_count + products_added, f"Liczba powinna wzrosnąć o {products_added}")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się dodać wielu produktów do koszyka")
    
    def test_2_3_add_same_product_multiple_times(self):
        """Test ID 2.3"""
        initial_count = self.get_cart_count()
        
        try:
            # Dodaj ten sam produkt kilka razy
            for i in range(2):
                first_product = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='product-01']")))
                first_product.click()
                time.sleep(2)
                
                add_to_cart_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='add-to-cart']")))
                add_to_cart_btn.click()
                time.sleep(2)
                
                self.driver.get(TestData.BASE_URL)
                time.sleep(2)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, initial_count + 2, "Liczba powinna wzrosnąć o 2")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się dodać tego samego produktu wiele razy do koszyka")
    
    def test_2_6_remove_product_from_cart(self):
        """Test ID 2.6"""
        # Dodaj produkt do koszyka
        self.add_first_product_to_cart()
        initial_count = self.get_cart_count()
        
        try:
            # Przejdź do koszyka
            cart_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-cart']")))
            cart_link.click()
            time.sleep(2)
            
            # Usuń produkt
            remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='remove-from-cart']")))
            remove_button.click()
            time.sleep(2)
            
            # Sprawdź, czy koszyk został zaktualizowany
            self.driver.get(TestData.BASE_URL)
            time.sleep(2)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, initial_count - 1, "Ilość powinna zmaleć o 1")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się usunąć produktu z koszyka")
    
    def test_2_7_remove_multiple_products(self):
        """Test ID 2.7"""
        # Dodaj kilka produktów do koszyka
        self.test_2_2_add_multiple_products()
        initial_count = self.get_cart_count()
        
        try:
            # Przejdź do koszyka
            cart_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-cart']")))
            cart_link.click()
            time.sleep(2)
            
            # Usuń kilka produktów
            removed_count = 0
            remove_buttons = self.driver.find_elements(By.CSS_SELECTOR, "[data-test='remove-from-cart']")
            
            for i in range(min(2, len(remove_buttons))):
                try:
                    remove_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='remove-from-cart']")))
                    remove_button.click()
                    time.sleep(2)
                    removed_count += 1
                except (TimeoutException, NoSuchElementException):
                    break
            
            # Sprawdź, czy koszyk został zaktualizowany
            self.driver.get(TestData.BASE_URL)
            time.sleep(2)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, initial_count - removed_count, f"Ilość powinna zmaleć o {removed_count}")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się usunąć wielu produktów z koszyka")
    
    def test_2_8_empty_cart(self):
        """Test ID 2.8"""
        # Dodaj produkt do koszyka
        self.add_first_product_to_cart()
        
        try:
            # Przejdź do koszyka
            cart_link = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='nav-cart']")))
            cart_link.click()
            time.sleep(2)
            
            # Usuń wszystkie produkty z koszyka
            while True:
                try:
                    remove_button = self.driver.find_element(By.CSS_SELECTOR, "[data-test='remove-from-cart']")
                    remove_button.click()
                    time.sleep(2)
                except NoSuchElementException:
                    break
            
            # Sprawdź, czy koszyk jest pusty
            self.driver.get(TestData.BASE_URL)
            time.sleep(2)
            
            final_count = self.get_cart_count()
            self.assertEqual(final_count, 0, "Koszyk powinien być pusty")
            
        except (TimeoutException, NoSuchElementException):
            self.fail("Nie udało się opróżnić koszyka")
    
    def test_2_9_cart_persistence(self):
        """Test ID 2.9"""
        # Dodaj produkt do koszyka
        self.add_first_product_to_cart()
        initial_count = self.get_cart_count()
        
        # Przejdź do innej kategorii i wróć
        self.driver.get(TestData.BASE_URL + "/category/hand-tools")
        time.sleep(2)
        
        self.driver.get(TestData.BASE_URL)
        time.sleep(2)
        
        # Sprawdź, czy ilość przedmiotów w koszyku jest taka sama
        final_count = self.get_cart_count()
        self.assertEqual(final_count, initial_count, "Ilość powinna pozostać taka sama po przejściu do innej kategorii")

if __name__ == "__main__":
    unittest.main()