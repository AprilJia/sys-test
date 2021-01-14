from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class Locators():
    """the list of web element locators for AWS management console"""

    #----- aws base page --------
    my_acct_dropdown=(By.XPATH,"//a[@data-lb-popover-trigger='popover-my-account']")
    management_console_link=(By.XPATH, "//div[@data-id='popover-my-account']/ul/li[1]/a")

    # ----login page (account ID not specified) ---
    accountID_input_signin = (By.ID, "resolving_input")
    next_button = (By.ID, "next_button")

    # ----login page (account ID specified) ---
    accountID_input = (By.ID,"account")
    username_input = (By.ID,"username")
    password_input = (By.ID,"password")
    sign_in_button = (By.ID,"signin_button")

    #-----policy simulator page----
    # ugr is abbr. of "users, groups and roles"
    ugr_option = (By.ID, "typeSelector")
    ugr_filter = (By.ID, "entityFilter")

    def get_ugr(self, ugr):
        return (By.XPATH, "//*[@id='groupList']/li[(text()='%s')]" % ugr)

    service_selector = (By.XPATH, "//*[@id='service_selector']/div[1]")
    service_filter=(By.XPATH, '//*[@id="serviceFilter"]')

    def select_service(self,service):
        return (By.CSS_SELECTOR,"a[title$='%s']"%service)

    action_selector = (By.XPATH,"//*[@id='actions_selector']/ul/li[1]/div[1]/span")
    action_select_menu = (By.ID,"actions_select_menu")

    #get action locator
    def select_action(self,action):
        return (By.CSS_SELECTOR,"input.action_item_input[value='%s']"%action)

    def expand_action(self,action):
        return (By.XPATH,f'//div[contains(text(),"{action}")]')

    #enter resource
    resource_input = (By.CSS_SELECTOR,'input.resource_param_value.width400[title="Specify the resource to simulate with this action."]')
    expand_arrow = (By.XPATH, '//*[@id="simulationResults"]/div[1]/div[1]/i')
    # expand_arrow=(By.CLASS_NAME,"action-open-icon.cursor-hover.icon-caret-right")

    run_sim_btn = (By.ID,'init_simulation')
    clear_result_btn = (By.ID,"clear_results")
    # back_btn = (By.ID,"backBtn")
    back_btn = (By.XPATH,f'//button[contains(text(),"Back")]')

    # ---- s3 buckets -------
    #s3 page tabs
    s3_properties_tab = (By.XPATH, "//a[.='Properties']")
    s3_overview_tab = (By.XPATH, "//a[.='Overview']")

    #s3 page search field
    s3_filter = (By.ID, "get-filter-value")

    #select-box
    check_box = (By.XPATH, "//div[@class='awsui-checkbox-styled-box']")

    upload_btn = (By.XPATH,"//button[@type='submit']/span[2]")
    upload_field = (By.ID, "uploadInput")
    upload_addFile = (By.ID, "uploadInputNoFilesSelected")
    # upload_upload_btn = (By.XPATH, "//awsui-button[@text='Upload']/button/span")
    upload_upload_btn = (By.XPATH,"//*[@id='uploadModal']/div/div[1]/div[3]/div[2]/modal-footer/div/awsui-button[1]/button/span")
    upload_next_btn =(By.XPATH, "//awsui-button[@id='next']/button/span")


    actions_btn = (By.XPATH, "//div/button/span[2]")
    action_rename = (By.XPATH, "//ul/li[2]/ul/li[7]/a")
    action_rename_input = (By.ID, "awsui-textfield-0")
    action_rename_input_save = (By.XPATH, "//awsui-button[@text='Save']")
    action_delete = (By.XPATH,"//ul/li[3]/ul/li[1]/a")
    action_delete_delete = (By.ID, "create-primary")

    #view error msg
    view_details = (By.XPATH, "//*[@id='sidebarNavDiv']/div[2]/div[1]/div[2]/div/div[1]/table/tbody/tr/th[1]/div[2]/awsui-button/button/span")
    forbidden = (By.XPATH,"//awsui-expandable-section[@header='Forbidden']/h3")

    def get_obj_by_text(self, text):
        obj = (By.XPATH, "//a[contains(text(),'{}')]".format(text))
        return obj

    def get_obj_by_exact_text(self, text):
        obj = (By.XPATH, "//a[contains(text()='{}')]".format(text))
        return obj

    def get_obj_by_id(self,id):
        obj=(By.XPATH,id)
        return obj

    object_link = (By.ID, "object-link")
    #the first item on search results page
    first_item=(By.XPATH, "//table/tbody/tr[1]/td[2]/a[contains(@class,'list-view-item')]")

    #s3 Hide and show button
    s3_show_btn = (By.XPATH, "//button/span[.='Show']")
    s3_hide_btn = (By.XPATH, "//button/span[.='Hide']")

    s3_access_deny = (By.XPATH, "//error-message[@error='currLocation.objects.error']/span[@ng-if='!error.isSecurityError']")

    #------- cloudwatch page ------
    log_filter_box = (By.ID, "gwt-debug-prefixFilterTextBox")
    flog = (By.XPATH, "//tbody[1]/tr/td[2]/div/a")

    log_deny_msg = (By.XPATH,"//div[@class='content']/div[@class='gwt-HTML']")

    log_menu_insight = (By.ID, 'gwt-debug-logsInsightsLink')

     #insight page
    log_insight_group_input=(By.XPATH, "//input[@class='awsui-multi-select__selector']")
    insight=(By.ID, "awsui-textfield-1")
    ace_editor_id="cce3bd4e-157f-401e-993f-ceae8d46cc3e"

    log_display_radio_btn_row = (By.XPATH,"//label[@for='awsui-radio-button-7']")
    log_display_radio_btn_text = (By.XPATH, "//label[@for='awsui-radio-button-8']")

    #------EC2-----
    ec2_runing_instance_select=(By.XPATH, "//div[contains(text(),'Running instances')]")

    # ------ url -----------
    china_login_url="https://119441807317.signin.amazonaws.cn/console"
    base_url = "https://aws.amazon.com"
    url='https://us-west-2.console.aws.amazon.com/console/home?region=us-west-2#'

    s3_url= 'https://s3.console.aws.amazon.com/s3/home?region=us-west-2'
    s3_url_prefix = "https://s3.console.aws.amazon.com/s3/buckets/"

    cw_url= 'https://us-west-2.console.aws.amazon.com/cloudwatch/home?region=us-west-2#logs:'
    ec2_home_url='https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#Home:'
    ec2_run_inst_url='https://us-west-2.console.aws.amazon.com/ec2/v2/home?region=us-west-2#Instances:sort=instanceId'


# loc=Locators()



