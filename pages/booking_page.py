from playwright.sync_api import Page, Locator, expect
from locators import booking_page_locators
from generators.generator_booking_page import BookingData, ROOM_LABELS

class BookingPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_form(self, data: BookingData):
        self.page.select_option(booking_page_locators.ROOM_SELECT, data.room)
        self.page.fill(booking_page_locators.DATE_INPUT, data.date)
        self.page.fill(booking_page_locators.START_TIME_INPUT, data.start_time)
        self.page.fill(booking_page_locators.END_TIME_INPUT, data.end_time)
        self.page.fill(booking_page_locators.PARTICIPANTS_INPUT, data.participants)
        self.page.fill(booking_page_locators.NAME_INPUT, data.name)
        self.page.fill(booking_page_locators.EMAIL_INPUT, data.email)

    def click_submit(self):
        self.page.click(booking_page_locators.SUBMIT_BUTTON)

    def get_form_status(self) -> Locator:
        return self.page.locator(booking_page_locators.FORM_STATUS)

    def check_form_status_success(self, data: BookingData):
        status = self.get_form_status()
        expected_room_label = ROOM_LABELS[data.room]
        expect(status).to_have_class("form-status success")
        expect(status).to_contain_text("Бронирование создано.")
        expect(status).to_contain_text(expected_room_label)
        expect(status).to_contain_text(data.date)
        expect(status).to_contain_text(f"{data.start_time}–{data.end_time}")
        expect(status).to_contain_text(data.name)

    def check_form_status_error(self):
        status = self.get_form_status()
        expect(status).to_have_class("form-status error")
        expect(status).to_contain_text("Проверьте, пожалуйста, заполнение формы.")

    def check_date_input_error(self, error_text):
        error = self.page.locator(booking_page_locators.DATE_INPUT_ERROR)
        expect(error).to_have_class("field-error")
        expect(error).to_contain_text(error_text)

    def check_endtime_input_error(self, error_text):
        error = self.page.locator(booking_page_locators.ENDTIME_INPUT_ERROR)
        expect(error).to_have_class("field-error")
        expect(error).to_contain_text(error_text)