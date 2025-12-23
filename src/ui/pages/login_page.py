from __future__ import annotations

import random as rnd

from selene import have, be
from selene.support.shared import browser
from selene.support.shared.jquery_style import s, ss
from selenium.webdriver import ActionChains

from utils.allure_helper import allure_steps


@allure_steps
class LoginPage:
    username = s('#username')
    password = s('#password')
    login_btn = s('#doLogin')
    message_btn = s("a[href='/admin/message']")
    messages = ss(".messages .row")

    def login(self, login, password) -> LoginPage:
        self.username.send_keys(login)
        self.password.send_keys(password)
        self.login_btn.click()
        return self

    def click_on_messages(self) -> LoginPage:
        self.message_btn.click()
        return self

    def should_display_booking_msg(self, name) -> LoginPage:
        self.messages.element_by(have.text(name)).should(be.visible)
        return self