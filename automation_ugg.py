import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.uu-gg.one/")
    page.get_by_label("账号").click()
    page.get_by_label("账号").fill("lexiaoyao00")
    page.get_by_label("密码").click()
    page.get_by_label("密码").fill("Xc1290435868+")
    page.get_by_role("button", name="登录").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
