import json
from pathlib import Path
from simulator import SimulatorUI
import logging
import argparse

class PrepData():


    with open(str(Path(__file__).parent.joinpath("env_data.json"))) as f:
        env_data = json.load(f)

    def __init__(self,proj):
        self.account=self.env_data[proj]['account']
        self.prefix=self.env_data[proj]['prefix']
        self.region=self.env_data[proj]['region']
        self.group=self.env_data[proj]['group']
        self.role=self.env_data[proj]['role']
        self.service=self.env_data[proj]['service']
        self.action={s:self.env_data[s] for s in self.service}

    @property
    def glist(self):
        if len(self.group)>0:
            return [f'{self.prefix}-{g}' for g in self.group]

    @property
    def rlist(self):
        if len(self.role)>0:
            return [f'{self.prefix}-{r}' for r in self.group]

    @property
    def ugr_list(self):
        ugr_list={}
        ugr_list['Groups']=self.glist
        ugr_list['Roles']=self.rlist
        return ugr_list

    @property
    def s3_arn(self):
        arn_prefix = 'arn:aws:s3:::'
        return [f'{arn_prefix}{self.prefix}-seq-output-s3',f'{arn_prefix}{self.prefix}-result-s3']

    @property
    def cw_arn(self):
        log_group=["success", "info", "error", "audit"]
        arn_prefix = 'arn:aws:logs:'
        return [f'{arn_prefix}{self.region}:{self.account}:log-group:{self.prefix}-{l}-log-group:*' for l in log_group]

    @property
    def res_arn(self):
        res_arn={}
        res_arn['S3']=self.s3_arn
        res_arn['CloudWatch Logs']=self.cw_arn
        return res_arn

    def split_arn(self,arn):
        if "s3" in arn:
            name =f'{arn.split("-")[-2]}-s3'
        elif "log-group" in arn:
            name = f'{arn.split("-")[-3]}-log'
        else:
            name="iam"
        return name


def run_sim():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--username",
        required=True,
        help="username to AWS management console",
    )
    parser.add_argument(
        "--pwd",
        required=True,
        help="password to AWS management console",
    )
    parser.add_argument(
        "--project",
        required=True,
        help="project in lower case: jackfruit, cherry, elderberry"
    )
    args = parser.parse_args()

    sim=SimulatorUI()
    data=PrepData(args.project)
    sim.to_page(f'https://{data.account}.signin.aws.amazon.com/console')
    sim.valid_login(args.username, args.pwd)
    sim.to_page("https://policysim.aws.amazon.com/home/index.jsp?#users")
    for option in data.ugr_list.keys():
        if data.ugr_list[option] is not None:
            sim.policy_sim_ugr_selector(option)
            for g in data.ugr_list[option]:
                sim.policy_sim_ugr_filter(g)
                sim.policy_sim_select_ugr(g)
                for s in data.service:
                    sim.policy_sim_select_service(s)
                    for res in data.res_arn[s]:
                        for a in data.action[s]:
                            sim.policy_sim_action_selector()
                            sim.policy_sim_select_action(a)
                            sim.policy_sim_action_selector()
                            sim.policy_sim_expand(a)
                            sim.policy_sim_enter_resource(res)
                        sim.policy_sim_run()
                        sim.policy_sim_arrow_expand()
                        sim.take_screenshot(f'{g.split("-")[-1]}_{data.split_arn(res)}.png')
                        sim.policy_sim_clear_result()
                sim.policy_sim_back()
            sim.clean()


if __name__=='__main__':
    run_sim()

