from __future__ import annotations

from selene.support.shared import browser

import config

from src.ui.pages.booking_room_page import RoomPage
from src.ui.pages.login_page import LoginPage
from src.ui.pages.main_page import MainPage
from utils.allure_helper import allure_steps


@allure_steps
class BookerUIClient:
    main_page = MainPage()
    room_page = RoomPage()
    login_page = LoginPage()


booker = BookerUIClient()