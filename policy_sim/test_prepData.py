from config import PrepData
import json
from pathlib import Path

class TestPrepData():

    file=Path(__file__).parent.joinpath("env_data.json")
    with open(str(file)) as f:
        data = json.load(f)
    d = PrepData("cherry")

    def test_service(self):
        assert self.d.service[0]=="S3"
        assert self.d.service[1] == "CloudWatch Logs"

    def test_glist(self):
        assert self.d.glist[0] == "compote-bldr-staging-v2-qa"
        assert self.d.glist[1] == "compote-bldr-staging-v2-operator"

    def test_ugr_list(self):
        assert self.d.ugr_list['Roles'] is None

    def test_s3_arn(self):
        assert self.d.s3_arn[0]=="arn:aws:s3:::compote-bldr-staging-v2-seq-output-s3"
        assert self.d.s3_arn[1]=="arn:aws:s3:::compote-bldr-staging-v2-result-s3"

    def test_cw_arn(self):
        assert self.d.cw_arn[3]=="arn:aws:logs:us-west-2:859070845359:log-group:compote-bldr-staging-v2-audit-log-group:*"

    def test_res_arn(self):
        assert self.d.res_arn["S3"][0]=="arn:aws:s3:::compote-bldr-staging-v2-seq-output-s3"
        assert self.d.res_arn["CloudWatch Logs"][3] =="arn:aws:logs:us-west-2:859070845359:log-group:compote-bldr-staging-v2-audit-log-group:*"

    def test_action(self):
        assert self.d.action['S3'][0]=="GetObject"
        assert self.d.action['CloudWatch Logs'][2]=="DeleteLogStream"

    def test_split_arn(self):
        assert self.d.split_arn("arn:aws:logs:us-west-2:859070845359:log-group:compote-bldr-staging-v2-error-log-group:*") \
               == "error-log"
        assert self.d.split_arn("arn:aws:s3:::compote-bldr-staging-v2-seq-output-s3")=="output-s3"



