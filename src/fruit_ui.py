from .aws_locators import Locators
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from . import config as cf

class FruitUI():

    loc = Locators()
    PKG_ROOT = Path(__file__).parent.parent

    def __init__(self):
        self.driver = webdriver.Chrome()


    def locate_element(self,loc):
        try:
            wait(self.driver, 20).until(EC.visibility_of_element_located(loc))
        except NoSuchElementException:
            print("element not found")
        return self.driver.find_element(*loc)

    def take_screenshot(self,filename="screenshots.png"):
        sleep(5)
        Path('./OE').mkdir(parents=True, exist_ok=True)
        oe = Path('OE').joinpath(filename)
        self.driver.save_screenshot(str(oe))

    @property
    def to_s3_page(self):
        self.driver.get(cf.s3_url)
        sleep(5)

    def find_s3obj(self,name):
        self.locate_element(self.loc.s3_filter).send_keys(name,Keys.ENTER)
        sleep(5)

    def click_obj(self,name):
        self.locate_element(self.loc.get_obj_by_text(name)).click()
        sleep(5)

    def select_obj(self,loc):
        self.locate_element(loc).click()
        sleep(5)

    def is_present(self,partial_text):
        sleep(5)
        try:
            self.locate_element(self.loc.get_obj_by_text(partial_text))
            return True
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False

    @property
    def log_deny_msg(self):
        sleep(5)
        msg = "This IAM user does not have permission to view Log Groups in this account."
        try:
            self.locate_element(self.loc.log_deny_msg).text == msg
            return True
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False

    def s3_deny_msg(self):
        sleep(5)
        msg = "Access Denied"
        try:
            self.locate_element(self.loc.s3_access_deny).text == msg
            return True
        except TimeoutException:
            return False
        except NoSuchElementException:
            return False

    @property
    def to_log_page(self):
        self.driver.get(cf.cw_url)
        sleep(5)

    def filter_log(self,search_key):
        self.locate_element(self.loc.log_filter_box).send_keys(search_key,Keys.ENTER)
        sleep(5)

    def valid_login_console(self,username,password,account):
        self.driver.get(self.loc.base_url)
        # navigate to login page
        self.locate_element(self.loc.my_acct_dropdown).click()
        self.locate_element(self.loc.management_console_link).click()
        # signin
        self.locate_element(self.loc.accountID_input_signin).send_keys(account)
        self.locate_element(self.loc.next_button).click()
        self.locate_element(self.loc.username_input).send_keys(username)
        self.locate_element(self.loc.password_input).send_keys(password)
        self.locate_element(self.loc.sign_in_button).click()
        sleep(5)

    def valid_login(self,username,password,account):
        self.driver.get(cf.url)
        self.locate_element(self.loc.username_input).send_keys(username)
        self.locate_element(self.loc.password_input).send_keys(password)
        self.locate_element(self.loc.sign_in_button).click()
        sleep(5)


    def back_to_previous_page(self,n):
        self.driver.execute_script(f"window,history.go(-{n})")
        sleep(5)

    def go_to_page(self,resource_url):
        self.driver.get(resource_url)
        sleep(5)

    @property
    def to_ec2_page(self):
        self.go_to_page(cf.ec2_run_inst_url)
        sleep(5)

    @property
    def page_refresh(self):
        sleep(5)
        self.driver.refresh()

    @property
    def close_page(self):
        self.driver.close()
        self.driver.quit()


    @property
    def open_search_result(self):
        result = self.locate_element(self.loc.first_item)
        if result is not None:
            result.click()

    @property
    def find_search_result(self):
        return self.locate_element(self.loc.first_item).text

    def to_s3_property_tab(self,bucket):
        property_tab_url = f'{self.loc.s3_url_prefix}{bucket}/?region={cf.region}&tab=properties'
        self.go_to_page(property_tab_url)
        self.take_screenshot(bucket+"version_enabled.png")

    def to_s3_show_version_url(self,url):
        suffix = f'?region={cf.region}&tab=overview&showversions=true'
        self.go_to_page(f'{url}{suffix}')


    def rename_file(self,url):
        self.go_to_page(url)
        self.select_obj(self.loc.check_box)
        self.locate_element(self.loc.actions_btn).click()
        self.locate_element(self.loc.action_rename).click()
        orig = self.locate_element(self.loc.action_rename_input).get_attribute('value')
        self.locate_element(self.loc.action_rename_input).clear()
        self.locate_element(self.loc.action_rename_input).send_keys(orig+"rename")
        self.locate_element(self.loc.action_rename_input_save).click()
        self.take_screenshot("rename1.png")
        self.page_refresh
        self.take_screenshot("rename2.png")
        # self.select_obj(self.loc.check_box)
        # self.locate_element(self.loc.actions_btn).click()
        # self.locate_element(self.loc.action_rename).click()
        # self.locate_element(self.loc.action_rename_input).clear()
        # self.locate_element(self.loc.action_rename_input).send_keys("user_access_test_file.xml")
        # self.locate_element(self.loc.action_rename_input_save).click()


    def open_bucket(self,bucket):
        self.to_s3_page
        self.find_s3obj(bucket)
        self.click_obj(bucket)

    def open_s3obj(self,obj):
        self.find_s3obj(obj)
        self.click_obj(obj)

    def open_log(self,log_group,*log_stream):
        if log_stream:
            self.to_log_page
            self.filter_log(log_group)
            self.click_obj(log_group)
            self.filter_log(log_stream)
            if self.locate_element(self.loc.flog):
                  self.locate_element(self.loc.flog).click()
        else:
            self.to_log_page
            self.filter_log(log_group)
            self.click_obj(log_group)

    def loop_through_output_dir(self,dir_name):
        for r in dir_name:
            self.find_s3obj(r)
            self.take_screenshot(r+".png")

    def delete_file(self,bucket):
        self.open_bucket(bucket)
        if self.is_present("user_access_test_file"):
            self.find_s3obj("user_access_test_file")
            self.select_obj(self.loc.check_box)
            self.locate_element(self.loc.actions_btn).click()
            self.locate_element(self.loc.action_delete).click()
            self.locate_element(self.loc.action_delete_delete).click()
            self.take_screenshot(f'delete_from_{bucket}.png')

    def upload_file(self,bucket):
        self.open_bucket(bucket)
        self.locate_element(self.loc.upload_btn).click()
        f_in = f'{self.PKG_ROOT}/test_data/user_access_test_file/user_access_test_file.xml'
        sleep(5)
        file_input = self.driver.find_element_by_id("uploadInput")
        file_input.send_keys(f_in)
        self.locate_element(self.loc.upload_upload_btn).click()
    # def check_s3_msg(self):
        self.locate_element(self.loc.view_details).click()
        self.locate_element(self.loc.forbidden).click()
        self.take_screenshot(f"{bucket}_upload_forbidden.png")






