class TestData:
    # Adresy stron aplikacji webowej
    BASE_URL = "https://practicesoftwaretesting.com"
    LOGIN_URL = "https://practicesoftwaretesting.com/auth/login"
    
    # Prawidłowe dane logowania
    VALID_EMAIL = "customer@practicesoftwaretesting.com"
    VALID_PASSWORD = "welcome01"
    
    # Nieprawidłowe dane logowania
    INVALID_EMAIL = "invalid@test.com"
    INVALID_PASSWORD = "wrongpassword"
    EMPTY_STRING = ""
            
    # Maksymalne czasy oczekiwania
    DEFAULT_TIMEOUT = 10
    LONG_TIMEOUT = 30
    
    # Dane do Appium
    MOBILE_PLATFORM = "Android"
    MOBILE_BROWSER = "Chrome"