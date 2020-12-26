

# profile_name=f.profile_name
# loc=Locators()
# fr=Fruit(f.profile_name)
# u=FruitUI()
# u.is_present("000000000-CHKNN_s15-2").click



# u.valid_login(f.operator_username,f.operator_password,f.account)
# u.driver.get(f.cw_url)
# u.valid_login(f.qa_username,f.qa_password,f.account)
# u.open_bucket(f.s3_output)
# u.locate_element(loc.upload_btn).click()
# d="./test_data/user_access_test_file/user_access_test_file.xml"
# print(Path(d).absolute())

# time.sleep(5)
# u.driver.find_element_by_id("uploadInput").send_keys("/Users/yjia/myCode/sys_test/test_data/user_access_test_file/user_access_test_file.xml")
# print(u.locate_element(loc.upload_field))

# u.locate_element(loc.get_obj_by_text("compote-cn-01-staging-info-log-group")).click()
# u.locate_element(loc.get_obj_by_text("000000000-CHKNN_s15-2")).click()
# u.is_present("compote-cn-01-staging-info-log-group").click()

# try:
#     u.locate_element(loc.get_obj_by_text("000000000-CHKNN_s15-2")).click()
# except TimeoutException:
#     print("false")
# except NoSuchElementException:
#     print("false")

import datetime
import time
#
# datestr = "2020-09-01T12:00:00.000"
# d=time.mktime(time.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%f")) * 1000
# print(d)

t="arn:aws:logs:us-west-2:859070845359:log-group:compote-bldr-staging-v2-audit-log-group:*"
t1=t.split("-")
print(t1)
s="-"
print(s.join(t1[-3:-1]))
