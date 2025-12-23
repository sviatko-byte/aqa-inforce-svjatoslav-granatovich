from __future__ import annotations

import random as rnd

from selene import have, be
from selene.support.shared import browser
from selene.support.shared.jquery_style import s, ss
from selenium.webdriver import ActionChains

from utils.allure_helper import allure_steps


@allure_steps
class RoomPage:
    booking_card = s('.booking-card')
    room_description = s("//h2[.='Room Description']")
    next_btn = s("//button[.='Next']")
    days = ss('.rbc-button-link')
    selected = s('.rbc-event-content[title="Selected"]')
    reserved_now_btn = s('#doReservation')
    contact_details_form = s('.card-body form')
    first_name = s("input[placeholder='Firstname']")
    last_name = s("input[placeholder='Lastname']")
    email = s("input[placeholder='Email']")
    phone = s("input[placeholder='Phone']")
    price_summary = s('.card.bg-light')
    confirm_reserved_now_btn = s("//button[.='Reserve Now']")
    admin_btn = s("a[href='/admin']")
    alert_msg = ss("div[role='alert'] li")


    def should_display_room_page(self) -> RoomPage:
        self.booking_card.should(be.visible)
        self.room_description.should(be.visible)
        return self

    def click_on_next_btn(self) -> RoomPage:
        self.next_btn.click()
        return self

    def select_random_date_by_drag(self) -> RoomPage:
        visible_days = self.days.filtered_by(be.visible)
        day_el = rnd.choice(visible_days)
        we = day_el.locate()

        actions = ActionChains(browser.driver)
        actions.click_and_hold(we).move_by_offset(5, 5).release().perform()
        return self

    def should_have_selected_event(self) -> RoomPage:
        self.selected.should(have.text('Selected'))
        return self

    def click_on_reserved_now_btn(self) -> RoomPage:
        self.reserved_now_btn.click()
        return self

    def should_display_contact_details_form(self) -> RoomPage:
        self.contact_details_form.should(be.visible)
        return self

    def fill_contact_details(self, name, last_name, email, phone) -> RoomPage:
        self.first_name.send_keys(name)
        self.last_name.send_keys(last_name)
        self.email.send_keys(email)
        self.phone.send_keys(phone)
        return self

    def should_display_price_summary(self) -> RoomPage:
        self.price_summary.should(be.visible)
        return self

    def click_on_confirm_reserved_now_btn(self) -> RoomPage:
        self.confirm_reserved_now_btn.click()
        return self

    def should_display_booking_confirmation(self) -> RoomPage:
        self.booking_card.should(have.text("Booking Confirmed"))
        return self

    def click_on_admin_btn(self) -> RoomPage:
        self.admin_btn.click()
        return self

    def should_display_alert_msg(self, error) -> RoomPage:
        self.alert_msg.element_by(have.text(error)).should(be.visible)
        return self