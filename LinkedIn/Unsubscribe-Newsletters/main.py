from playwright.sync_api import Playwright, sync_playwright
from undetected_playwright import stealth_sync
import time


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    stealth_sync(context)
    page = context.new_page()

    # goto linkedin and login
    page.goto("https://linkedin.com/")

    # manually login here
    time.sleep(25)

    # open saved newletters links text file
    with open('newsletter_links.txt', 'r') as f:
        newsletter_links = f.readlines()

    for link in newsletter_links:
        try:
            page.goto(link)
            time.sleep(2)
            unsubscribe_button = page.locator('.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view.publishing-entity-header__cta-button')
            unsubscribe_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error with link: {link}, Error: {e}")
            continue

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)