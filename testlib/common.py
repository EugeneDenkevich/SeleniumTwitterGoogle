import os
import tempfile
from pathlib import Path
from typing import Any, Tuple

import xlsxwriter
from dotenv import load_dotenv
from retry import retry
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import ActionChains, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome

from testlib.exceptions import VaribleNotSet

load_dotenv()


class Settings:
    google_password_changed = False
    google_was_logged = False
    twitter_password_changed = False


settings = Settings()


def save_data_in_xlsx(
    filename: str,
    cols: Tuple[str, ...],
    data: Tuple[str, ...],
) -> None:
    assets = Path(__file__).parent.parent / "assets"
    if not assets.exists():
        os.mkdir(assets)
    book = xlsxwriter.Workbook(assets / filename)
    sheet = book.add_worksheet()
    bold = book.add_format(properties={"bold": True})
    sheet.set_column(0, 4, 20)
    sheet.write_row(
        row=0,
        col=0,
        data=cols,
        cell_format=bold,
    )
    sheet.write_row(
        row=1,
        col=0,
        data=data,
    )
    book.close()


@retry(exceptions=ElementNotInteractableException, tries=5, delay=0.5)
def get_element_sefely(
    by: str,
    value: str,
    driver: Chrome,
) -> WebElement:
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, value)),
    )


@retry(exceptions=ElementNotInteractableException, tries=5, delay=0.5)
def send_keys_safely(input: WebElement, keys: Any) -> None:
    input.send_keys(keys)


def click_safely(element: WebElement, driver: Chrome) -> None:
    try:
        element.click()
    except Exception:
        try:
            driver.execute_script("arguments[0].click();", element)
        except Exception:
            ActionChains(driver).move_to_element(element).click(element).perform()


def click_safely_or_none(by: str, value: str, driver: Chrome) -> None:
    """Поиск элемента, нажатие на него или возврат None"""

    try:
        element = get_element_sefely(by=by, value=value, driver=driver)
    except Exception:
        pass
    click_safely(element=element, driver=driver)


@retry(exceptions=ElementNotInteractableException, tries=5, delay=0.5)
def clear_input_safely(input: WebElement, driver: Chrome) -> None:
    input.send_keys(Keys.CONTROL + "a")
    input.send_keys(Keys.DELETE)


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise VaribleNotSet(f"Varible for {key} is not set")
    return value


def get_chrome_with_proxy(options: ChromeOptions, user_agent: str) -> Chrome:
    """Получение драйвера Хром с проксями"""

    PROXY_HOST = get_env("PROXY_HOST")
    PROXY_PORT = get_env("PROXY_PORT")
    PROXY_USER = get_env("PROXY_USER")
    PROXY_PASS = get_env("PROXY_PASS")

    with open("proxy_config/manifest.json", "r") as f:
        manifest_json = f.read()
    with open("proxy_config/background_js.txt", "r") as f:
        background_js = f.read() % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    with tempfile.TemporaryDirectory() as tmp:
        temp_manifest = Path(tmp) / "manifest.json"
        temp_background = Path(tmp) / "background.js"
        with open(temp_manifest, "w") as f:
            f.write(manifest_json)
        with open(temp_background, "w") as f:
            f.write(background_js)
        options.add_argument(f"--load-extension={tmp}")
        options.add_argument(f"--user-agent={user_agent}")
        options.add_argument("--disable-notifications")

        return Chrome(
            options=options,
        )
