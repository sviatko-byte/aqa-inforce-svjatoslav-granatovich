from __future__ import annotations

from selene import have, be
from selene.support.shared import browser
from selene.support.shared.jquery_style import s, ss

from utils.allure_helper import allure_steps


@allure_steps
class MainPage:
    header = s('.navbar-brand')
    booking_btn = s("a[href='/#booking']")
    rooms_btn = s("a[href='/#rooms']")
    rooms_section = s('#rooms')
    book_now_btn = rooms_section.ss('.btn-primary').first
    datapicker = ss(".react-datepicker-wrapper input")
    check_in = datapicker.first
    check_out = datapicker.second
    check_availability_btn = s("//button[.='Check Availability']")

    def open_main_page(self) -> MainPage:
        browser.driver.maximize_window()
        browser.open("https://automationintesting.online/")
        return self

    def should_display_header(self) -> MainPage:
        self.header.should(have.text("Shady Meadows B&B"))
        return self

    def click_on_rooms_btn(self) -> MainPage:
        self.rooms_btn.click()
        return self

    def should_display_rooms_section(self) -> MainPage:
        self.rooms_section.should(be.visible)
        return self

    def click_on_book_now_btn(self) -> MainPage:
        self.book_now_btn.click()
        return self

    def fill_check_in_date(self, date) -> MainPage:
        self.check_in.send_keys(date)
        return self

    def fill_check_out_date(self, date) -> MainPage:
        self.check_out.send_keys(date)
        return self

    def should_be_disabled_check_availability_btn(self) -> MainPage:
        self.check_availability_btn.should(have.attribute('disabled'))
        return self
