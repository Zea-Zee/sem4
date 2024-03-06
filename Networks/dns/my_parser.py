import random
import time
from colorama import Fore, Back, init as colorama_init
from fake_useragent import UserAgent
from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


colorama_init()


def get_driver(headless=False):
    # chrome_options = Options()
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    # chrome_options.add_argument(f"user-agent={user_agent}")
    # if headless:
    #     chrome_options.add_argument('--headless')
    # return webdriver.Chrome(options=chrome_options)
    chrome_options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def mvideo_prod_cards_parser(url: str) -> str:
    try:
        driver = get_driver(headless=True)
        driver.get(url)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "product-picture__img")))
        wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "price__main-value")))
        wait.until(EC.visibility_of_any_elements_located((By.CLASS_NAME, "cart-button")))
        product_cars_rows = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "product-cards-row")))

        # Перебор всех карточек товаров
        products = []
        for row in product_cars_rows:
            titles = row.find_elements(By.CLASS_NAME, "product-title__text")
            prices = row.find_elements(By.CLASS_NAME, "price__main-value")
            buttons = row.find_elements(By.CLASS_NAME, "cart-button")

            for t, p, b in zip(titles, prices, buttons):
                product = {
                    "Title": t.text.strip(),
                    "Price": p.text.strip(),
                    "In stock": True if b else False,
                }
                # print(f"""
                #     Title: {t.text.strip()}
                #     Price: {p.text.strip()}
                #     In stock: {True if b else False}
                #        """)
                products.append(product)

        driver.quit()
        print(f"{Back.GREEN}There are {len(products)} product cards{Back.RESET}")
        print(f"{Fore.GREEN}{products}{Fore.RESET}")
        return products
    except Exception as e:
        print(f"{Back.RED}An exception occurred in mvideo_prod_cards_parser: {e}{Back.RESET}")
        return f"An exception occurred in mvideo_prod_cards_parser: {e}"


def rand_enter():
    driver = get_driver()
    search_box = driver.find_element(
        By.CSS_SELECTOR,
        "#body > mvid-root > div > mvid-primary-layout > mvid-layout > div > main > mvid-plp > mvid-product-list-block > div.plp__card-grid > mvid-product-list > mvid-plp-product-cards-layout > div > mvid-product-cards-row > div:nth-child(1) > mvid-plp-product-picture:nth-child(20) > div > div.product-picture.product-picture--grid > a > mvid-slide-panel > div > div > mvid-floating-controls > div > div > div > div:nth-child(1) > picture > img",
    )
    actions = ActionChains(driver)
    actions.move_to_element(search_box)
    actions.click()
    actions.perform()

    # Случайные задержки и рывки при вводе запроса
    query = "видеокарты"
    for char in query:
        actions.send_keys(char)
        actions.pause(
            random.uniform(0.1, 0.3)
        )  # Рандомная задержка между вводом символов
        actions.move_by_offset(
            random.uniform(-5, 5), random.uniform(-5, 5)
        )  # Рандомные рывки мыши
        actions.perform()

    # Нажатие Enter для выполнения поиска
    actions.send_keys(Keys.RETURN)
    actions.perform()

    # Случайные движения мыши и клик по первой ссылке
    time.sleep(2)  # Небольшая задержка перед кликом
    search_result = driver.find_element(By.CSS_SELECTOR, "h3")
    actions.move_to_element(search_result)
    actions.move_by_offset(
        random.uniform(-10, 10), random.uniform(-10, 10)
    )  # Рандомные движения мыши
    actions.click()
    actions.perform()

    # Закрытие браузера
    time.sleep(50)
    driver.quit()


# mvideo_prod_cards_parser("https://www.mvideo.ru/playstation-4327/ps5-konsoli-8627")
