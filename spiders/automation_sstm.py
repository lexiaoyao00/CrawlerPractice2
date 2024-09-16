from .automation import Automation

import time
from datetime import datetime

from logger import main_logger

class SSTM_Auto(Automation):

    def __init__(self):
        super().__init__()

        today = datetime.now()
        self.formatted_date = f"{today.year}/{today.month}/{today.day}"
        main_logger.enable_console_output()

        self.browser_driver.launch_browser()
        self.browser_driver.page.goto("https://sstm.moe/")

    def __del__(self):
        main_logger.enable_console_output(False)


    def SignIn(self,email,password):
        self.Submit(email,password)
        time.sleep(1)
        self.CheckInArea()
        time.sleep(1)
        self.CheckIn()
        time.sleep(10)


    def Submit(self,email,password):
        bt_dengru = self.browser_driver.page.locator('a#elUserSignIn')
        bt_submit = self.browser_driver.page.locator('button#elSignIn_submit[type="submit"]')
        input_email = self.browser_driver.page.locator('input[type="email"]')
        input_pw = self.browser_driver.page.locator('input[type="password"]')


        try:
            bt_dengru.click()

            input_email.fill(email)
            input_pw.fill(password)

            bt_submit.click()

            main_logger.debug("Submit over")

        except Exception as e:
            main_logger("Error submitting : " + str(e))

    def CheckInArea(self):
        bt_HuoQuJieCao = self.browser_driver.page.locator('a#elNavigation_43')
        bt_WotaoQianDao = self.browser_driver.page.locator('li.ipsMenu_item').filter(has_text="我要签到")
        bt_QianDao = self.browser_driver.page.locator(f'span.ipsType_break.ipsContained a[title*="{self.formatted_date}"]')

        try:
            bt_HuoQuJieCao.click()

            bt_WotaoQianDao.click()

            bt_QianDao.click()
            main_logger.debug("CheckInArea over")

        except Exception as e:
            main_logger("Error CheckInArea : " + str(e))

    def CheckIn(self):
        #ipsLayout_mainArea > div.ipsClearfix > ul > li > span > a
        bt_HuiFu = self.browser_driver.page.locator('span[data-controller="forums.front.topic.reply"] a').filter(has_text="回复此主题")
        area_HuiFu = self.browser_driver.page.locator('div.ipsComposeArea_dummy.ipsJS_show')
        text_compos = self.browser_driver.page.locator('#cke_1_contents > div')
        bt_TiJiao =  self.browser_driver.page.get_by_role("button", name="提交回复")

        try:
            bt_HuiFu.click()
            area_HuiFu.click()
            text_compos.fill(self.formatted_date)

            bt_TiJiao.click()

            main_logger.debug("CheckIn over")
            
        except Exception as e:
            main_logger("Error CheckIn : " + str(e))

