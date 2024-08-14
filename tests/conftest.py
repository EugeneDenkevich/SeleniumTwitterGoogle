import os
import tempfile
from pathlib import Path
from typing import Any, Generator, Optional

import openai
import pytest
from dotenv import load_dotenv
from selenium.webdriver import ChromeOptions
from selenium.webdriver.remote.webdriver import By
from tweepy import Client
from undetected_chromedriver import Chrome

from testlib.common import (
    click_safely,
    click_safely_or_none,
    get_element_sefely,
    get_env,
    send_keys_safely,
    settings,
)

load_dotenv()


@pytest.fixture(scope="session")
def chrome_driver() -> Generator[Chrome, Any, Any]:
    """Драйвер хрома"""

    PROXY_HOST = get_env("PROXY_HOST")
    PROXY_PORT = get_env("PROXY_PORT")
    PROXY_USER = get_env("PROXY_USER")
    PROXY_PASS = get_env("PROXY_PASS")

    with open("proxy_config/manifest.json", "r") as f:
        manifest_json = f.read()
    with open("proxy_config/background_js.txt", "r") as f:
        background_js = f.read() % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )

    options = ChromeOptions()
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

        driver = Chrome(
            options=options,
        )

    yield driver


@pytest.fixture
def google_email() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TESTS_GOOGLE_EMAIL")


@pytest.fixture
def google_old_password() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TESTS_GOOGLE_OLD_PASSWORD")


@pytest.fixture
def google_new_password() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TESTS_GOOGLE_NEW_PASSWORD")


@pytest.fixture
def google_first_name() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TESTS_GOOGLE_FIRSTNAME")


@pytest.fixture
def google_second_name() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TESTS_GOOGLE_SECONDNAME")


@pytest.fixture()
def google_password(
    google_old_password: str,
    google_new_password: str,
) -> Generator[Optional[str], Any, Any]:
    yield (
        google_new_password if settings.google_password_changed else google_old_password
    )


@pytest.fixture()
def google_login(
    google_email: str,
    google_password: str,
    chrome_driver: Chrome,
) -> Generator[Any, Any, Any]:
    chrome_driver.get("https://www.google.com/")

    login_button = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="gb"]/div/div[2]/a',
        driver=chrome_driver,
    )
    click_safely(element=login_button, driver=chrome_driver)

    if settings.google_was_logged:
        change_account_element = get_element_sefely(
            by=By.XPATH,
            value='.//*[@class="aZvCDf B682ne W7Aapd zpCp3 SmR8"]',
            driver=chrome_driver,
        )
        click_safely(element=change_account_element, driver=chrome_driver)

    email_input = get_element_sefely(
        by=By.NAME,
        value="identifier",
        driver=chrome_driver,
    )
    send_keys_safely(input=email_input, keys=google_email)

    email_button = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="identifierNext"]',
        driver=chrome_driver,
    )
    click_safely(element=email_button, driver=chrome_driver)

    password_input = get_element_sefely(
        by=By.NAME,
        value="Passwd",
        driver=chrome_driver,
    )
    send_keys_safely(input=password_input, keys=google_password)

    password_button = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="passwordNext"]',
        driver=chrome_driver,
    )
    click_safely(element=password_button, driver=chrome_driver)

    get_element_sefely(  # Проверяем, перенаправило ли нас на главную
        by=By.ID,
        value="APjFqb",
        driver=chrome_driver,
    )

    settings.google_was_logged = True

    yield

    chrome_driver.delete_all_cookies()
    chrome_driver.get("https://www.google.com/")

    get_element_sefely(  # Проверяем, находимся ли на главной
        by=By.ID,
        value="APjFqb",
        driver=chrome_driver,
    )

    chrome_driver.refresh()


@pytest.fixture(scope="function")
def twitter_email() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TEST_TWITTER_EMAIL")


@pytest.fixture(scope="function")
def twitter_old_password() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TEST_TWITTER_OLD_PASSWORD")


@pytest.fixture(scope="function")
def twitter_new_password() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TEST_TWITTER_NEW_PASSWORD")


@pytest.fixture(scope="function")
def twitter_password(
    twitter_old_password: str,
    twitter_new_password: str,
) -> Generator[Optional[str], Any, Any]:
    yield (
        twitter_new_password
        if settings.twitter_password_changed else twitter_old_password
    )


@pytest.fixture(scope="function")
def twitter_phone() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("TEST_TWITTER_PHONE")


@pytest.fixture(scope="function")
def twitter_login(
    twitter_email: str,
    twitter_password: str,
    twitter_phone: str,
    chrome_driver: Chrome,
) -> Generator[Any, Any, Any]:
    chrome_driver.get("https://x.com")

    click_safely_or_none(
        by=By.XPATH,
        value="//span[contains(text(), 'Accept all cookies')]",
        driver=chrome_driver,
    )
    chrome_driver.refresh()

    sign_in_element = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[4]/a/div",
        driver=chrome_driver,
    )
    click_safely(element=sign_in_element, driver=chrome_driver)

    email_input = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input",
        driver=chrome_driver,
    )
    send_keys_safely(input=email_input, keys=twitter_email)

    next_element = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div",
        driver=chrome_driver,
    )
    click_safely(element=next_element, driver=chrome_driver)

    try:
        unusual_activity_email_input_element = get_element_sefely(
            by=By.XPATH,
            value="/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input",
            driver=chrome_driver,
        )
        send_keys_safely(input=unusual_activity_email_input_element, keys=twitter_phone)

        unusual_activity_next_element = get_element_sefely(
            by=By.XPATH,
            value="//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div",
            driver=chrome_driver,
        )
        click_safely(element=unusual_activity_next_element, driver=chrome_driver)
    except Exception:
        pass

    password_input_element = get_element_sefely(
            by=By.NAME,
            value="password",
            driver=chrome_driver,
    )

    send_keys_safely(input=password_input_element, keys=twitter_password)

    send_password_element = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div",
        driver=chrome_driver,
    )
    click_safely(element=send_password_element, driver=chrome_driver)

    yield

    chrome_driver.get("https://x.com")

    account_actions_element = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='react-root']/div/div/div[2]/header/div/div/div/div[2]/div/button",
        driver=chrome_driver,
    )
    click_safely(element=account_actions_element, driver=chrome_driver)

    exit_element = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='layers']/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div/a[2]/div[1]/div",
        driver=chrome_driver,
    )
    click_safely(element=exit_element, driver=chrome_driver)

    sure_exit_element = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='layers']/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/button[1]",
        driver=chrome_driver,
    )
    click_safely(element=sure_exit_element, driver=chrome_driver)

    chrome_driver.refresh()


@pytest.fixture(scope="function")
def twitter_client() -> Generator[Client, Any, Any]:
    yield Client(
        consumer_key = os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET"),
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN"),
        access_token = os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )


@pytest.fixture(scope="function")
def gpt_client() -> Generator[Optional[openai.OpenAI], Any, Any]:
    yield openai.Client(
        api_key=os.getenv("OPENAI_API_KEY"),
    )


@pytest.fixture(scope="function")
def gpt_model() -> Generator[Optional[str], Any, Any]:
    yield os.getenv("OPENAI_MODEL")
