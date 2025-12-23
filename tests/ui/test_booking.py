import time
from datetime import datetime

import allure
import pytest
from dateutil.relativedelta import relativedelta

from src.ui.booker import booker


def test_check_the_room_can_be_booked_with_valid_data():
    booker.main_page.open_main_page() \
        .should_display_header() \
        .click_on_rooms_btn() \
        .should_display_rooms_section() \
        .click_on_book_now_btn()
    booker.room_page.should_display_room_page() \
        .click_on_next_btn() \
        .select_random_date_by_drag() \
        .should_have_selected_event() \
        .click_on_reserved_now_btn() \
        .should_display_contact_details_form() \
        .fill_contact_details("sviatoslav", "granatovich", "dewifi@gmail.com", "+380685474919") \
        .should_display_price_summary() \
        .click_on_confirm_reserved_now_btn() \
        .should_display_booking_confirmation() \
        .click_on_admin_btn()
    booker.login_page.login("admin", "password") \
        .click_on_messages() \
        .should_display_booking_msg("sviatoslav")


def test_check_the_room_can_be_booked_with_invalid_data():
    booker.main_page.open_main_page() \
        .click_on_rooms_btn() \
        .should_display_rooms_section() \
        .click_on_book_now_btn()
    booker.room_page.should_display_room_page() \
        .click_on_next_btn() \
        .select_random_date_by_drag() \
        .should_have_selected_event() \
        .click_on_reserved_now_btn() \
        .should_display_contact_details_form() \
        .fill_contact_details("", "gr", "dewifail.com", "685474919") \
        .should_display_price_summary() \
        .click_on_confirm_reserved_now_btn() \
        .should_display_alert_msg("size must be between 3 and 18") \
        .should_display_alert_msg("must be a well-formed email address") \
        .should_display_alert_msg("Firstname should not be blank") \
        .should_display_alert_msg("size must be between 11 and 21") \
        .should_display_alert_msg("size must be between 3 and 30")


def test_check_the_room_can_be_booked_with_unavailable_dates():
    date = (datetime.now() - relativedelta(years=1)).strftime("%d/%m/%Y")
    booker.main_page.open_main_page() \
        .fill_check_in_date(date) \
        .fill_check_out_date(date) \
        .should_be_disabled_check_availability_btn()