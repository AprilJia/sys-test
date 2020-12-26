from pathlib import Path
import boto3
import gzip,shutil
from datetime import datetime, timedelta
import time
import json
import hashlib

# PKG_ROOT = Path(__file__).parent.parent

class Fruit():

    def __init__(self,profile):
        # self.dir = PKG_ROOT / "test_data"
        self.dir="/Users/yjia/testData/test_data_apricot_cntest/SPAINT0004_1"
        self.profile_name = profile
        # self.dir = data_dir

    def get_dir_obj(self,text):
        return[d for d in Path(self.dir).rglob('*') if d.is_dir() and text in str(d.name)]

    def get_file_obj(self,text):
        return [d for d in Path(self.dir).rglob('*/*.*') if text in str(d.name)]

    @property
    # def get_library_id(self):
    #     library_id = []
    #     for f in self.get_file_obj("fastq.gz"):
    #         if str(f.name).split("_")[0]!= "Undetermined":
    #             library_id.append(str(f.name).split("_")[0])
    #     return list(dict.fromkeys(library_id))

    def get_library_id(self):
        library_id = []
        for f in self.get_file_obj("fastq.gz"):
            if str(f.name).split("_")[0]!= "Undetermined":
                flowcell = str(f.relative_to(self.dir)).split("/")[0][-15:]
                lib_id = str(f.name).split("_")[0]
                library_id.append(f'{flowcell}_{lib_id}')
        return list(dict.fromkeys(library_id))

    @property
    def get_seq_output_dir_name(self):
        seq_output_dir_name = []
        for dir in self.get_dir_obj("000000000-"):
            seq_output_dir_name.append(str(dir.name))
        return seq_output_dir_name



    @property
    def get_flowcell(self):
        return [name[-15:] for name in self.get_seq_output_dir_name]

    def get_client(self, service):
        session = boto3.Session(profile_name=self.profile_name)
        return session.client(service,region_name="us-west-2")

    def get_resource(self, service):
        session = boto3.Session(profile_name=self.profile_name)
        return session.resource(service)

    def get_s3_client(self):
        session = boto3.Session(profile_name=self.profile_name)
        return session.client('s3')

    def log_content(self,log_group,search_key):
        """ search log message by the search_key, return the dic type log message
        """
        client = self.get_client("logs")

        start_time = int((datetime.today() - timedelta(hours=48)).timestamp() * 1000)
        end_time = int(datetime.now().timestamp() * 1000)
        query = "fields @timestamp, @message | filter @message like " + f'"{search_key}"'

        resp = client.start_query(
           logGroupName=log_group,
           startTime=start_time,
           endTime=end_time,
           queryString=query
        )
        query_id = resp['queryId']
        time.sleep(5)
        response = client.get_query_results(queryId=query_id)
        if len(response['results'])> 0:
            return response
        else:
            print("log event not found")

    def log_field_value(self,log_content,search_key,length):
        """search_key for example like (patient, result_group_id, job_id)
        if search_key is 'flowcell', the length will be the length of 000000000-xxxxx which is 15
        """
        if log_content is not None:
            log_text = log_content['results'][0][1]['value']
            if search_key in log_text:
                start_index = log_text.find(search_key)+len(search_key)+4  # 3=lenght of /": "/
                end_index = start_index + length
                return log_text[start_index:end_index]
            else:
                print(f"{search_key} not found")

    def result_group_id(self,log_content):
        if log_content is not None:
            result_group_id = self.log_field_value(log_content, "result_group_id", 15)
            if result_group_id is not None:
                return result_group_id
            else:
                print(f"result_group_id not found")

    def get_absolute_path(self,dir,name):
        for f in Path(dir).rglob('*/*'):
            if f.name == name:
                return Path(f)

    def upload_dir_to_s3(self,bucket,exclude_file="CompletedJobInfo.xml"):
        for f in Path(self.dir).glob('**/*.*'):
            if f.name not in (exclude_file, ".DS_Store"):
                f_dest= f.relative_to(self.dir)
                self.get_resource("s3").meta.client.upload_file(str(f),bucket,str(f_dest))
            if f.name==".DS_Store":
                f.unlink()
        print(f'all files has been uploaded to {bucket} except "{exclude_file}"')

    def upload_file_to_s3(self,bucket,f_in,f_out=None):
        self.get_resource("s3").meta.client.upload_file(f_in,bucket,f_out)
        print(f'{f_in} is uploaded to {bucket}/{f_out}')

    #unzip file
    def unzip_file(file_in):
        file_out=file_in[:-3]
        with gzip.open(file_in, 'r') as f_in, open(file_out, "wb") as f_out:
            shutil.copyfileobj(f_in,f_out)

    #gzip file
    def zip_file(file_in):
        file_out=file_in + ".gz"
        with open(file_in, 'rb') as f_in, open (file_out,'wb') as f_out:
            shutil.copyfileobj(f_in,f_out)

    def get_file_num(self,file_pattern):
        files=[p.name for p in Path(self.dir).iterdir() if p.name.endswith(file_pattern)]
        return len(files)

    def get_s3obj(self,bucket,flowcell):
        s3 = self.get_resource("s3")
        seq_result_s3 = s3.Bucket(bucket)
        return seq_result_s3.objects.filter(Prefix=flowcell)

    def download_s3obj(self,objs,bucket):
        s3 = self.get_resource("s3")
        seq_result_s3 = s3.Bucket(bucket)
        for obj in objs:
            result_file = Path('results').joinpath(Path(obj.key).name)
            seq_result_s3.download_file(obj.key, str(result_file))

    def get_log_events(self,log_group, log_stream):
        """Generate all the log events from a CloudWatch group.
        :param log_group: Name of the CloudWatch log group.
        :param log_stream: log stream of the logs
        """
        client = self.get_client('logs')
        kwargs = {
            'logGroupName': log_group,
            'logStreamNamePrefix': log_stream,
            'limit': 1,
        }
        while True:
            resp = client.filter_log_events(**kwargs)
            yield from resp['events']
            try:
                kwargs['nextToken'] = resp['nextToken']
            except KeyError:
                break

    def export_logs(self,file,logs):
        with open(file,"w") as f:
            json.dump(logs,f,indent=4)

    def read_json(self,json_file):
        with open(json_file) as jf:
            data=json.load(jf)
        return data

    def upload_to_seq_output_s3(self, bucket_name):
        for dir in self.get_dir_obj("000000000"):
            self.upload_dir_to_s3(bucket_name, "CompletedJobInfo.xml")
            f_in = self.get_absolute_path(dir, "CompletedJobInfo.xml")
            f_out = f_in.relative_to(dir.parent)
            time.sleep(20)
            self.upload_file_to_s3(bucket_name, str(f_in), str(f_out))

    def s3_to_s3(self, s_bucket, t_bucket, files):
        s3 = self.get_resource("s3")
        for obj in self.get_s3obj(s_bucket, files):
            if not "CompletedJobInfo" in obj.key:
                s_files = {'Bucket': obj.bucket_name, 'Key': obj.key}
                s3.meta.client.copy(s_files, t_bucket, obj.key)
            else:
                complete_file=obj.key
        time.sleep(30)
        s_files = {'Bucket': obj.bucket_name, 'Key': complete_file}
        s3.meta.client.copy(s_files, t_bucket, complete_file)

    def get_obj_url(self, result_bucket):
        obj_url = []
        for i in range(len(self.get_flowcell)):
            objs = self.get_s3obj(result_bucket, self.get_flowcell[i])
            for obj in objs:
                obj_url.append(f'https://s3.console.aws.amazon.com/s3/object/{result_bucket}/{obj.key}')
        return obj_url

    def s3_result_url(self,bucket):
        result_urls = {}
        for i in range(len(self.get_flowcell)):
            result_urls[f'{self.get_flowcell[i]}'] = {}
            prefix = f"https://s3.console.aws.amazon.com/s3/buckets/{bucket}/"
            objs = self.get_s3obj(bucket, self.get_flowcell[i])
            for obj in objs:
                result_url = Path(obj.key).parent
                date_url = result_url.parent
                pipeline_url = date_url.parent
                host_url = pipeline_url.parent
                sample_id_url = host_url.parent
                demux_url = sample_id_url.parent

                result_urls[f'{self.get_flowcell[i]}']["result_url"] = prefix + str(result_url) + "/"
                result_urls[f'{self.get_flowcell[i]}']["date_url"] = prefix + str(date_url) + "/"
                result_urls[f'{self.get_flowcell[i]}']["pipeline_url"] = prefix + str(pipeline_url) + "/"
                result_urls[f'{self.get_flowcell[i]}']["sample_id_url"] = prefix + str(sample_id_url) + "/"
                result_urls[f'{self.get_flowcell[i]}']["host_url"] = prefix + str(host_url) + "/"
                result_urls[f'{self.get_flowcell[i]}']["demux_url"] = prefix + str(demux_url) + "/"
        return result_urls


    def s3_output_url(self,bucket):
        output_urls = {}
        for i in range(len(self.get_seq_output_dir_name)):
            output_urls[f'{self.get_seq_output_dir_name[i]}']= {}
            prefix = f"https://s3.console.aws.amazon.com/s3/buckets/{bucket}/"
            objs = self.get_s3obj(bucket, self.get_seq_output_dir_name[i])
            for obj in objs:
                if "SampleSheetUsed" in obj.key:
                    samplesheetused_url = Path(obj.key).parent
                    date_url = samplesheetused_url.parent
                    metrics_file_url = date_url.parent
                    output_urls[f'{self.get_seq_output_dir_name[i]}']["samplesheetused_url"] = prefix + str(Path(obj.key).parent) + "/"
                    output_urls[f'{self.get_seq_output_dir_name[i]}']["date_url"] = prefix + str(date_url) + "/"
                    output_urls[f'{self.get_seq_output_dir_name[i]}']["metircs_file_url"] = prefix + str(metrics_file_url) + "/"

        return output_urls



class Apricot(Fruit):

    # def __init__(self):
    #     super().__init__()

    pass
#
# fruit=Fruit("compote-v")
# lm=fruit.log_content("compote-bldr-staging-v2-info-log-group","LIB-144","compote-v2")
# ls=fruit.log_stream_name(lm,"000000000-CDCMR","LIB-144")
#
# print(ls)




