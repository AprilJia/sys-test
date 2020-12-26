from src.fruit_ui import FruitUI
import src.config as cf
from src.fruit import Fruit
from time import sleep

from src.aws_locators import Locators
from src.fruit import Apricot
from pathlib import Path
import json

class User:
    loc = Locators()
    awsui = FruitUI()
    spa = Fruit(cf.profile_name)
    bucket = [cf.s3_output, cf.s3_result, cf.s3_output_replica, cf.s3_result_replica]
    bucket_a = [cf.s3_output_replica, cf.s3_result_replica]
    log_group = [cf.info_log, cf.error_log, cf.success_log]
    s3_url_prefix = cf.s3_url_prefix

    def __init__(self,user=None):
        if user is None:
            self.username = user[0]
            self.password = user[1]
            self.account = user[2]

    @property
    def login(self):
        self.awsui.valid_login(self.username, self.password, self.account)

    @property
    def s3_view_access(self):
        self.awsui.to_s3_page
        for i in range(len(self.bucket)):
            self.awsui.find_s3obj(self.bucket[i])
            self.awsui.click_obj(self.bucket[i])
            self.awsui.take_screenshot(f'{self.username}-{self.bucket[i]}.png')
            if self.awsui.s3_deny_msg:
                self.awsui.take_screenshot(f'{self.username}-{self.bucket[i]}.png')
            self.awsui.back_to_previous_page(1)

    # def s3_upload_test_file(self,bucket):
    #    f_out = "user_access_test_file/user_access_test_file.xml"
    #    self.spa.upload_file_to_s3(bucket,"../test_data/user_access_test_file/user_access_test_file.xml",f_out)
    #    url = f'{self.s3_url_prefix}{bucket}/{Path(f_out).parent}/'
    #    self.awsui.go_to_page(url)
    #    self.awsui.take_screenshot(self.username + "_upload.png")
    #    self.awsui.rename_file(url)

    def upload_file(self):
        self.awsui.upload_file(cf.s3_output)

    def rename_s3_obj(self):
        for i in range(2):
            url = f'{self.s3_url_prefix}{self.bucket[i]}'
            self.awsui.rename_file(url)
            return url

    @property
    def ec2_access(self):
        self.awsui.to_ec2_page
        self.awsui.take_screenshot(f'{self.username}_ec2.png')

    @property
    def log_access(self):
        self.awsui.to_log_page
        if self.awsui.log_deny_msg:
            self.awsui.take_screenshot(f'{self.username}_log_access_denied.png')
        else:
            for i in range(len(self.log_group)):
                self.awsui.filter_log(self.log_group[i])
                self.awsui.click_obj(self.log_group[i])
                self.awsui.take_screenshot(f'{self.username}_{self.log_group[i]}.png')
                self.awsui.back_to_previous_page(2)

    def clean_up(self):
        for i in range(2):
            self.awsui.delete_file(self.bucket[i])
        self.awsui.close_page




admin = [cf.admin_username, cf.admin_password, cf.account]
qa = [cf.qa_username, cf.qa_password, cf.account]
operator = [cf.operator_username, cf.operator_password, cf.account]
root = [cf.root_username, cf.root_password, cf.account]

users=[operator,qa,admin,root]

user=User(users[1])
# user.login
# user.upload_file()

# for i in range(len(users)):
#     user = User(users[i])
#     user.login
#     if users[i]== root:
#         user.clean_up()
#     else:
#         user.s3_view_access
#         user.ec2_access
#         user.log_access
#         if users[i] == qa:
#             user.rename_s3_obj()
#         if users[i] == admin:
#             user.s3_upload_test_file(cf.s3_output)




# if __name__=='__Main__':
#
# ad=User()
# ad.login
# ad.s3_upload_test_file(cf.s3_output)

# ad.s3_modify_access()
# ad.s3_view_access
# ad.ec2_access
# ad.log_access
print(user.username)



