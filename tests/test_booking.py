import pytest
from playwright.sync_api import Page, expect
from generators.generator_booking_page import generate_booking_data
from datetime import date, datetime, timedelta
from pages.booking_page import BookingPage
from locators import booking_page_locators

def test_successful_booking(page: Page, base_url: str):
    booking_page = BookingPage(page)
    data = generate_booking_data()
    page.goto(base_url)
    booking_page.fill_form(data)
    booking_page.click_submit()
    booking_page.check_form_status_success(data)

def test_invalid_booking(page: Page, base_url: str):
    past_date = (date.today() - timedelta(days=1)).isoformat()
    booking_page = BookingPage(page)
    data = generate_booking_data(date=past_date)
    page.goto(base_url)
    booking_page.fill_form(data)
    booking_page.click_submit()
    booking_page.check_form_status_error()
    booking_page.check_date_input_error("Дата не может быть в прошлом.")

@pytest.mark.xfail(
    strict=True,
    reason="BUG-02: Не проверяется диапазон длительности встречи (от 30 минут до 4 часов)",
    raises=AssertionError
)
@pytest.mark.parametrize(
    "start_time, end_time",
    [
        ("10:00", "10:00"),
        ("10:00", "10:15"),
        ("10:00", "15:00"),
    ],
)
def test_discovered_defect(page: Page, base_url: str, start_time: str, end_time: str):
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    booking_page = BookingPage(page)
    data = generate_booking_data(date=tomorrow, start_time=start_time, end_time=end_time)
    page.goto(base_url)
    booking_page.fill_form(data)
    booking_page.click_submit()
    booking_page.check_form_status_error()
    booking_page.check_endtime_input_error("Длительность встречи должна быть от 30 минут до 4 часов.")
