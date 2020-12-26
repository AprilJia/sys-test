import configparser


config=configparser.ConfigParser()
config.read("/Users/yjia/myCode/sys_test/setup/apricot_cn.ini")

url = config["url"]["login_url"]
s3_url = config["url"]["s3_url"]
cw_url = config["url"]["cw_url"]
ec2_run_inst_url = config["url"]["ec2_run_inst_url"]
ec2_home_url = config["url"]["ec2_home_url"]
s3_url_prefix = config["url"]["s3_url_prefix"]

region = config["region"]["region"]

account=config["account"]["account_id"]
profile_name=config["account"]["profile_name"]

root_username=config["root"]["username"]
root_password=config["root"]["password"]

admin_username=config["admin"]["username"]
admin_password=config["admin"]["password"]

qa_username=config["qa"]["username"]
qa_password=config["qa"]["password"]

operator_username=config["operator"]["username"]
operator_password=config["operator"]["password"]

s3_output=config["s3"]["output"]
s3_output_replica=config["s3"]["output_replica"]
s3_result=config["s3"]["result"]
s3_result_replica=config["s3"]["result_replica"]


info_log=config["log"]["info"]
error_log=config["log"]["error"]
success_log=config["log"]["success"]
