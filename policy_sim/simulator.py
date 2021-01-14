from aws_locators import Locators
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

class AwsUI():
    """ Class that defines method and attributes for navigation on AWS management console """

    loc = Locators()
    PKG_ROOT = Path(__file__).parent

    def __init__(self):
        # self.driver = webdriver.Chrome()
        self.driver = webdriver.Firefox(executable_path=r'/Users/yjia/Downloads/webdriver/FFDriver/geckodriver')

    #locate web elements and return a list, raise error if not found
    def locate_elements(self, loc):
        try:
            wait(self.driver, 20).until(EC.visibility_of_element_located(loc))
        except NoSuchElementException:
            print("element not found")
        return self.driver.find_elements(*loc)

    #locate one web element and raise error if not found
    def locate_element(self, loc):
        try:
            wait(self.driver, 20).until(EC.visibility_of_element_located(loc))
        except NoSuchElementException:
            print("element not found")
        return self.driver.find_element(*loc)

    # open the target page
    def to_page(self, url):
        self.driver.get(url)
        sleep(3)

    # login to AWS management console
    def valid_login(self, username, password):
        self.locate_element(self.loc.username_input).send_keys(username)
        self.locate_element(self.loc.password_input).send_keys(password)
        self.locate_element(self.loc.sign_in_button).click()
        sleep(3)

    # Create OE dir to store the screenshots
    def take_screenshot(self, filename):
        sleep(3)
        Path('OE').mkdir(parents=True, exist_ok=True)
        oe = Path('OE').joinpath(filename)
        self.driver.save_screenshot(str(oe))

    def clean(self):
        print("=====complete======")
        self.driver.quit()


class SimulatorUI(AwsUI):
    """class that defines methods and attributes for AWS IAM Policy Simulator"""

    def __init__(self):
        super().__init__()

    #select option from group/role/user dropdown list
    def policy_sim_ugr_selector(self,option):
        select=Select(self.locate_element(self.loc.ugr_option))
        select.select_by_visible_text(option)

    # enter prefix to filter field -- to display the list of searched groups/user/roles
    def policy_sim_ugr_filter(self,prefix):
        sleep(3)
        self.locate_element(self.loc.ugr_filter).clear()
        self.locate_element(self.loc.ugr_filter).send_keys(prefix, Keys.ENTER)

    #select the specified group/role/user
    def policy_sim_select_ugr(self,ugr):
        self.locate_element(self.loc.get_ugr(ugr)).click()
        sleep(3)

    #select service (s3,CW logs etc.)
    def policy_sim_select_service(self,service):
        self.locate_element(self.loc.service_selector).click()
        self.locate_element(self.loc.service_filter).clear()
        self.locate_element(self.loc.service_filter).send_keys(service, Keys.ENTER)
        self.locate_element(self.loc.select_service(service)).click()

    #display the action selector
    def policy_sim_action_selector(self):
        self.locate_element(self.loc.action_selector).click()
        sleep(3)

    #select action
    def policy_sim_select_action(self,action):
        self.locate_element(self.loc.select_action(action)).click()
        sleep(3)

    #display resource input for selected action
    def policy_sim_expand(self,action):
        self.locate_element(self.loc.expand_action(action)).click()
        sleep(3)

    def policy_sim_arrow_expand(self):
        for a in self.locate_elements(self.loc.expand_arrow):
            a.click()
            sleep(3)

    #enter resource for target action
    def policy_sim_enter_resource(self,resource):
        self.locate_element(self.loc.resource_input).clear()
        self.locate_element(self.loc.resource_input).send_keys(resource,Keys.ENTER)
        sleep(3)

    # click run button to run simulation
    def policy_sim_run(self):
        self.locate_element(self.loc.run_sim_btn).click()
        # self.locate_element(self.loc.expand_arrow).click()
        sleep(3)

    #clear results
    def policy_sim_clear_result(self):
        self.locate_element(self.loc.clear_result_btn).click()

    #click back button to start over
    def policy_sim_back(self):
        self.locate_element(self.loc.back_btn).click()



class CWlogs:
    pass
