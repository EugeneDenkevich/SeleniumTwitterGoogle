from typing import Any

import openai
from selenium.webdriver.remote.webdriver import By
from tweepy import Client
from undetected_chromedriver import Chrome

from testlib.common import (
    click_safely,
    get_element_sefely,
    save_data_in_xlsx,
    send_keys_safely,
    settings,
)


def test_change_password(
    chrome_driver: Chrome,
    twitter_login: Any,
    twitter_old_password: str,
    twitter_new_password: str,
) -> None:
    """Изменение пароля пользователя"""

    more_element = get_element_sefely(
        by=By.XPATH,
        value="/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/button/div",
        driver=chrome_driver,
    )
    click_safely(element=more_element, driver=chrome_driver)

    settings_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[5]/a/div',
        driver=chrome_driver,
    )
    click_safely(element=settings_element, driver=chrome_driver)

    change_password_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/div[3]',
        driver=chrome_driver,
    )
    click_safely(element=change_password_element, driver=chrome_driver)

    current_password_input_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[1]/div[1]/label/div/div[2]/div/input',
        driver=chrome_driver,
    )
    send_keys_safely(input=current_password_input_element, keys=twitter_old_password)

    new_password_input_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[1]/div[3]/label/div/div[2]/div/input',
        driver=chrome_driver,
    )
    send_keys_safely(input=new_password_input_element, keys=twitter_new_password)

    new_password_confirm_input_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[1]/div[4]/label/div/div[2]/div/input',
        driver=chrome_driver,
    )
    send_keys_safely(
        input=new_password_confirm_input_element,
        keys=twitter_new_password,
    )

    save_new_password_button_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[3]/button',
        driver=chrome_driver,
    )
    click_safely(element=save_new_password_button_element, driver=chrome_driver)

    settings.twitter_password_changed = True


def test_get_twitter_additional_data(
    chrome_driver: Chrome,
    twitter_login: Any,
    twitter_password: str,
) -> None:
    """Получение данных о пользователе и сохранение в xlsx файл"""

    more_element = get_element_sefely(
        by=By.XPATH,
        value="/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/button/div",
        driver=chrome_driver,
    )
    click_safely(element=more_element, driver=chrome_driver)

    settings_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="layers"]/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[5]/a/div',
        driver=chrome_driver,
    )
    click_safely(element=settings_element, driver=chrome_driver)

    account_settings_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/div[2]',
        driver=chrome_driver,
    )
    click_safely(element=account_settings_element, driver=chrome_driver)

    password_input_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[3]/label/div/div[2]/div/input',
        driver=chrome_driver,
    )
    send_keys_safely(input=password_input_element, keys=twitter_password)

    password_button_element = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div[4]/button',
        driver=chrome_driver,
    )
    click_safely(element=password_button_element, driver=chrome_driver)

    username = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/a[1]/div/div/div[2]/span',
        driver=chrome_driver,
    ).text

    phone = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/a[2]/div/div/div[2]/span',
        driver=chrome_driver,
    ).text

    email = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/a[3]/div/div/div[2]/span',
        driver=chrome_driver,
    ).text

    sex = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/a[7]/div/div/div[2]/span',
        driver=chrome_driver,
    ).text

    age = get_element_sefely(
        by=By.XPATH,
        value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/section[2]/div[2]/div/a[8]/div/div/div[2]/span',
        driver=chrome_driver,
    ).text

    save_data_in_xlsx(
        filename="twitter_results.xlsx",
        cols=("Почта", "Юзернейм", "Телефон", "Пол", "Возраст"),
        data=(email, username, phone, sex, age),
    )


def test_create_tweet(
    twitter_client: Client,
    gpt_client: openai.OpenAI,
    gpt_model: str,
) -> None:
    """Тест создания твита"""

    completion = gpt_client.chat.completions.create(
        model=gpt_model,
        messages=[
            {
                "role": "user",
                "content": (
                    "Сгенерируй пост для Твиттера на случайную тему, "
                    "длинной 20-30 символов, на русском языке"
                ),
            },
        ],
    )
    tweet_content_gpt = completion.choices[0].message.content
    twitter_client.create_tweet(text=tweet_content_gpt)
