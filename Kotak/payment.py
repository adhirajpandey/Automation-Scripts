from playwright.sync_api import Playwright, sync_playwright
from undetected_playwright import stealth_sync
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

CRN = os.getenv("CRN")
PASSWORD = os.getenv("PASSWORD")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
KOTAK_OTP_URL = os.getenv("KOTAK_OTP_URL")
FAV_NAME = os.getenv("FAV_NAME")

SMALL_SLEEP = 2
MEDIUM_SLEEP = 5
LONG_SLEEP = 10

AMOUNT = "2"


def get_otp():
    headers = {"Authorization": f"Bearer {AUTH_TOKEN}"}
    response = requests.get(KOTAK_OTP_URL, headers=headers)

    otp = response.json()["otp"]

    print("otp is", otp)
    return otp


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    stealth_sync(context)
    page = context.new_page()

    # goto linkedin and login
    page.goto("https://netbanking.kotak.com/knb2/")

    time.sleep(SMALL_SLEEP)

    # type crn
    crn_input = page.locator('input[formcontrolname="userName"]')
    crn_input.fill(CRN)

    # type password
    formcontrolname = page.locator('input[formcontrolname="credentialInputField"]')
    formcontrolname.fill(PASSWORD)

    time.sleep(MEDIUM_SLEEP)

    # click login
    login_button = page.locator(
        'button[class="btn btn-primary float-right marb16 btnVertualsubmit mt-3"]'
    )
    login_button.click()

    # wait for otp to be delivered
    time.sleep(LONG_SLEEP)

    # get otp
    otp = get_otp()

    # enter otp
    otp_input = page.locator('input[formcontrolname="otpMobile"]')
    otp_input.fill(str(otp))

    time.sleep(MEDIUM_SLEEP)

    # click submit
    login_button = page.locator(
        'button[class="btn btn-primary float-right btn-mar-right ng-star-inserted"]'
    )
    login_button.click()

    time.sleep(LONG_SLEEP * 2)

    # click on fund transfer which is a span with class nav-item hidemenu ng-star-inserted and text Fund Transfer
    fund_transfer = page.locator(
        'span[class="nav-item hidemenu ng-star-inserted"] >> text="Fund Transfer"'
    )
    fund_transfer.click()

    time.sleep(MEDIUM_SLEEP)

    # click on benificiary where class is fav-name
    benificiary = page.locator(f'span[class="fav-name"] >> text="{FAV_NAME}"')
    benificiary.click()

    time.sleep(MEDIUM_SLEEP)

    # enter amount
    amount_input = page.locator('input[formcontrolname="amount"]')
    amount_input.fill(AMOUNT)

    # click proceed
    proceed_button = page.locator('button[class="btn btn-kred"] >> text="Proceed"')
    proceed_button.click()

    time.sleep(MEDIUM_SLEEP)

    # click confirm
    confirm_button = page.locator('button[class="btn btn-kred"] >> text="Confirm"')
    confirm_button.click()

    print("Transaction Successful")

    time.sleep(LONG_SLEEP)

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
