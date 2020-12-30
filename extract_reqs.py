import re
from xlwt import Workbook
import linecache

class Requirements:


    """ 1. open requirements file (in .rst or word format)
        2. get requirements ID and line index of the first line of each requirement
        3. get the content between two line index (some of the requirements contain
        mutiple lines
        4. get the last requirement
        5 get the all the requirements
        6. create a dict, key is requirement ID, value is requirement description
    """

    def __init__(self,file,prefix):
        self.file=file
        self.prefix=prefix

    #return file content without blank line
    def file_content(self):
        with open(self.file,"r") as fin:
            orig = re.sub(r'^$\n', '', fin.read(), flags=re.MULTILINE)
        return orig

    def get_reqs(self,src):
        reqs=[]
        for r in re.findall(self.prefix+ ".*\w\W", src, flags=re.MULTILINE):
            reqs.append(r)
        return reqs

    #get req id and it's line number in the file
    @property
    def req_ids(self):
        req_ids={}
        with open(self.file,"r") as fin:
            for index,line in enumerate(fin):
                result=re.search(self.prefix+"\d+((.\d+){0,})",line)
                if result:
                    req_ids[result.group(0)]=index
        return req_ids

    def last_req(self,last_line_index):
        req=linecache.getline(self.file, last_line_index)
        begin_with = [" ","-","*"]
        for l in range(last_line_index+1,10):
            for s in begin_with:
                if linecache.getline(self.file, l).startswith(s):
                    req=req+linecache.getline(self.file, l)
        return req


    def req_full(self, req_line_index):
        begin_with = [" ", "-", "*"]
        reqs = []
        max_req = len(req_line_index)
        for l in range(max_req - 1):
            req = ""
            for r in range(req_line_index[l], req_line_index[l + 1]):
                req = req + (linecache.getline(self.file, r))
            reqs.append(req)
        last_req = linecache.getline(self.file,req_line_index[-1] )
        for l in range(req_line_index[-1], 10):
            for s in begin_with:
                if linecache.getline(self.file, l+1).startswith(s):
                    last_req = last_req + linecache.getline(self.file, l+1)
        reqs.append(last_req)
        return reqs


    #split id desc to dict(id)= desc
    def req_split(self,req_id,req_full):
        reqs={}
        for i in range(len(req_id)-1):

            req_desc=req_full[i].split(req_id[i],1)[1].strip()
            reqs[req_id[i]]=req_desc
        return reqs


    def write_csv(self,reqs):
        wb=Workbook()
        sheet1=wb.add_sheet('Requirements')
        sheet1.write(0,0,'Req #')
        sheet1.write(0,1,'Req Description')
        for index,key in enumerate(reqs):
            sheet1.write(index+1,0,key)
            sheet1.write(index+1,1,reqs[key])
        wb.save('Reqs.xls')

def main():

    req_inst=Requirements("sad.txt","SADREQ")
    req_ids=list(req_inst.req_ids.keys())
    req_line_index=list(req_inst.req_ids.values())
    req_full=req_inst.req_full(req_line_index)
    reqs=req_inst.req_split(req_ids,req_full)
    req_inst.write_csv(reqs)




if __name__=="__main__":
    main()