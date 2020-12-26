from src.fruit_ui import FruitUI
from src.fruit import Fruit
from pathlib import Path
import src.config as cf
from src.aws_locators import Locators

data_dir = "/Users/yjia/testData/test_data_apricot_cntest/"
invalid_data =["SPAINT0001_1", "SPAINT0001_2", "SPAINT0001_3",
          "SPAINT0001_4", "SPAINT0002_1", "SPAINT0002_2",
          "SPAINT0003_1", "SPAINT0003_2"]
valid_data = ["SPAINT0004_1","SPAINT0004_2", "SPAINT0006_1"]

awsui = FruitUI()
spa = Fruit(cf.profile_name,data_dir)


def tc_upload():
    spa.upload_to_seq_output_s3(cf.s3_output)

def tc_cp(files):
    spa.s3_to_s3(cf.s3_output,cf.s3_testdata,files)

def tc_login():
    awsui.valid_login(cf.admin_username, cf.admin_password, cf.account)

#verify files are stored in the s3
def tc3(bucket):
    if "result" in bucket:
        for dn in spa.get_seq_output_dir_name:
            awsui.open_bucket(bucket)
            awsui.find_s3obj(dn[-15:])
            awsui.take_screenshot(dn[-15:]+"result.png")
    else:
        for dn in spa.get_seq_output_dir_name:
            awsui.open_bucket(bucket)
            awsui.find_s3obj(dn)
            awsui.take_screenshot(dn[-15:]+ "seq_output.png")


#verify logs - for region insights feature avaiable
def tc4_logs(log_group):

    awsui.open_log(log_group)
    for j in range(len(spa.get_flowcell)):
        for i in range(len(spa.get_library_id)):
            log_content = spa.log_content(log_group, spa.get_library_id[i])
            result_group_id = spa.result_group_id(log_content)
            if result_group_id is not None:
                log_stream_name = f"{result_group_id}_{spa.get_flowcell[j]}_{spa.get_library_id[i]}"
                awsui.open_log(log_group, log_stream_name)
                awsui.take_screenshot(spa.get_library_id[i] + ".png")

                logs = list(spa.get_log_events(log_group, log_stream_name))
                file = (Path(".") / "OE" / f'{log_stream_name}').absolute()
                spa.export_logs(file, logs)
            else:
                print("log stream name not found")

#verify logs - for region that the feature insight not available
def tc4_logs_b(log_group):
    awsui.open_log(log_group)
    awsui.take_screenshot(log_group + ".png")
    for i in range(len(spa.get_library_id)):
        if awsui.is_present(spa.get_library_id[i]):
            awsui.click_obj(spa.get_library_id[i])
            awsui.take_screenshot(f'{spa.get_library_id[i]}.png')
            awsui.back_to_previous_page(1)
        else:
            print(f'{spa.get_library_id[i]} are not found')

#download results
def tc_download_result():
    for i in range(len(spa.get_flowcell)):
        objs=spa.get_s3obj(cf.s3_result,spa.get_flowcell[i])
        spa.download_s3obj(objs,cf.s3_result)

#verify results
def tc_view_result():
    for i in spa.get_obj_url(cf.s3_result):
        awsui.go_to_page(i)
        awsui.take_screenshot(i.split("/")[-1]+".png")


#verify properties - versioning
def tc_versioning(bucket):
    awsui.to_s3_property_tab(bucket)

def tc_no_overwritten(bucket,dn=None):
    if "result" in bucket:
       urls = spa.s3_result_url(bucket)
       url = urls[dn[-15:]]["result_url"]
    else:
        urls = spa.s3_output_url(bucket)
        url = urls[dn]["samplesheetused_url"]
    awsui.to_s3_show_version_url(url)
    awsui.take_screenshot(dn[-15:] + "no_overwritten.png")


def tc_download_output():
    objs = spa.get_s3obj("compote-bldr-prod-seq-output-s3","190910_M70566_0043_000000000-CDCTC")
    # return objs
    spa.download_s3obj(objs,"compote-bldr-prod-seq-output-s3")



# for i in range(len(invalid_data)):
for i in range(1):
    test_dir = f'{data_dir}{invalid_data[i]}'
    setattr(spa,"dir",test_dir)
    tc_upload()
    tc_login()
    tc3(cf.s3_output)
    tc4_logs_b(cf.info_log)
    # tc4_logs_b(cf.success_log)
    # tc_download_result()
    # tc_versioning(cf.s3_output)
    # tc_versioning(cf.s3_result)
    # tc_view_result()



