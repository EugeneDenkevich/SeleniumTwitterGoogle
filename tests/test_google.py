from datetime import datetime, timedelta
from typing import Any

from selenium.webdriver import Chrome
from selenium.webdriver.remote.webdriver import By

from testlib.common import (
    clear_input_safely,
    click_safely,
    get_element_sefely,
    save_data_in_xlsx,
    send_keys_safely,
    settings,
)


def test_change_password(
    chrome_driver: Chrome,
    google_login: Any,
    google_new_password: str,
) -> None:
    """Изменение пароля пользователя"""

    chrome_driver.get("https://myaccount.google.com/personal-info?hl=ru-BY&utm_source=google&utm_medium=pref-page")

    password_page = get_element_sefely(
        by=By.XPATH,
        value="/html/body/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[10]",
        driver=chrome_driver,
    )
    click_safely(element=password_page, driver=chrome_driver)

    password_input = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='i6']",
        driver=chrome_driver,
    )
    send_keys_safely(input=password_input, keys=google_new_password)

    password_confirm_input = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='i12']",
        driver=chrome_driver,
    )
    send_keys_safely(input=password_confirm_input, keys=google_new_password)

    change_password_button = get_element_sefely(
        by=By.XPATH,
        value="/html/body/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/form/div/div[2]/div/div/button",
        driver=chrome_driver,
    )
    click_safely(element=change_password_button, driver=chrome_driver)

    confirm_change_password_button = get_element_sefely(
        by=By.XPATH,
        value="//*[@id='yDmH0d']/div[14]/div[2]/div/div[2]/div[2]/button",
        driver=chrome_driver,
    )
    click_safely(element=confirm_change_password_button, driver=chrome_driver)

    chrome_driver.get("https://myaccount.google.com/security?hl=ru")

    while True:
        password_changed_element = get_element_sefely(
            by=By.XPATH,
            value="/html/body/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[3]/div/div/div[2]/div/a/div/div[1]/div/div[1]/div/div",
            driver=chrome_driver,
        )
        password_change_text = password_changed_element.text
        if password_change_text == "Пароль изменен":
            break
        chrome_driver.refresh()

    password_change_time_element = get_element_sefely(
        by=By.XPATH,
        value="/html/body/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[3]/div/div/div[2]/div/a/div/div[1]/div/div[2]/div/div",
        driver=chrome_driver,
    )
    password_change_time = password_change_time_element.text[:5]

    password_change_time_obj = datetime.strptime(password_change_time, "%H:%M")

    before = password_change_time_obj - timedelta(minutes=1)
    after = password_change_time_obj + timedelta(minutes=1)

    settings.google_password_changed = True

    assert password_change_text == "Пароль изменен"
    assert before <= password_change_time_obj <= after


def test_fullname(
    chrome_driver: Chrome,
    google_login: Any,
    google_first_name: str,
    google_second_name: str,
) -> None:
    """Изменение имени и фамилии пользователя"""

    url = "https://myaccount.google.com/personal-info?hl=ru-BY&utm_source=google&utm_medium=pref-page"
    chrome_driver.get(url)

    fullname_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[2]/div/div/div[3]/div[2]/a',
        driver=chrome_driver,
    )
    click_safely(element=fullname_element, driver=chrome_driver)

    change_fullname_element = get_element_sefely(
        by=By.XPATH,
        value="/html/body/c-wiz[2]/div/div[2]/div[2]/c-wiz/div/div[3]/div/div/ul/li[1]/div/div[2]/div/a",
        driver=chrome_driver,
    )
    click_safely(element=change_fullname_element, driver=chrome_driver)


    firstname_input = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="i7"]',
        driver=chrome_driver,
    )
    clear_input_safely(input=firstname_input, driver=chrome_driver)
    send_keys_safely(input=firstname_input, keys=google_first_name)

    secondname_input = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="i12"]',
        driver=chrome_driver,
    )
    clear_input_safely(input=secondname_input, driver=chrome_driver)
    send_keys_safely(input=secondname_input, keys=google_second_name)

    save_button = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div[2]/div/div/div[3]/div[2]/div/div/button',
        driver=chrome_driver,
    )
    click_safely(element=save_button, driver=chrome_driver)

    fullname_ready_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/c-wiz/div/div[3]/div/div/ul/li[1]/div/div[1]/div[2]/div',
        driver=chrome_driver,
    )
    fullname = fullname_ready_element.text

    assert fullname == f"{google_first_name} {google_second_name}"


def test_get_google_additional_data(
    chrome_driver: Chrome,
    google_login: Any,
    google_password: str,
) -> None:
    """Сохранение данных о пользователе в xlsx файл"""

    chrome_driver.get("https://myaccount.google.com/email")

    email_element = get_element_sefely(
        by=By.XPATH,
        value="/html/body/c-wiz/div/div[2]/div[2]/c-wiz/div/div[4]/article/ul/li/div/a/div/div[1]/div",
        driver=chrome_driver,
    )
    email = email_element.text

    reserved_email_element = get_element_sefely(
        by=By.XPATH,
        value="/html/body/c-wiz/div/div[2]/div[2]/c-wiz/div/div[5]/article/ul/li/div/div/div[1]",
        driver=chrome_driver,
    )
    reserved_email = reserved_email_element.text

    chrome_driver.get("https://myaccount.google.com/personal-info")

    fullname_element = get_element_sefely(
        by=By.XPATH,
        value="/html/body/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[2]/div/div/div[3]/div[2]/a/div/div[1]/div/div[2]/div/div",
        driver=chrome_driver,
    )
    fullname = fullname_element.text

    birthday_element = get_element_sefely(
        by=By.XPATH,
        value="/html/body/c-wiz/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/c-wiz/section/div[2]/div/div/div[4]/div[2]/a/div/div[1]/div/div[2]/div/div",
        driver=chrome_driver,
    )
    birthday = birthday_element.text.replace("\u202f", "")

    save_data_in_xlsx(
        filename="google_results.xlsx",
        cols=("Почта", "Резервная почта", "Имя и Фамилия", "Пароль", "Дата рождения"),
        data=(email, reserved_email, fullname, google_password, birthday),
    )
