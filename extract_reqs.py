import re
import xlwt
import linecache
import docx2txt
import pdftotext
from pathlib import Path

class PrepDocs:

    def __init__(self,src,tgt):
        self.src=src
        self.tgt=tgt
        self.file_ext=Path(self.src).suffix

    #TBD--> find a good way to remove header and footer
    def prep_txt(self,text):
        header=["Title*\n.*","Rev*\n{0,}.*","Document Number*\n.*",
                "Confidential and Proprietary*\n.*",
               "Design History File","Master document.*"]
        content = re.sub(r'^$\n', '', text, flags=re.MULTILINE)
        tout=content
        for s in header:
            tout=re.sub(s,"", tout) #remove header and footer
        tout=re.sub(r'^$\n', '', tout, flags=re.MULTILINE) #remove empty line
        tout=re.sub("\s{50}"," ",tout)
        return tout

    def word2txt(self):
        wtxt = docx2txt.process(self.src)
        return self.prep_txt(wtxt)

    def pdf2txt(self):
        txt=""
        with open(self.src,"rb") as pdfin:
            pdf=pdftotext.PDF(pdfin)
            for p in range(len(pdf)):
                txt=txt+pdf[p]
        print(self.prep_txt(txt))
        return self.prep_txt(txt)


    @property
    def write_file(self):
        with open(self.tgt, "w") as fout:
            if self.file_ext==".docx":
                print(self.word2txt(), file=fout)
            elif self.file_ext==".pdf":
                print(self.pdf2txt(), file=fout)
            else:
                pass


class Requirements:

    """ 1. open requirements file (in .rst or word format)
        2. get requirements ID and line index of the first line of each requirement:req_ids()
        3. get the content between two line index (some of the requirements contain
        mutiple lines
        4. get the last requirement
        5 get the all the requirements
        6. create a dict, key is requirement ID, value is requirement description
    """

    def __init__(self,file,prefix):
        self.file=file
        self.prefix=prefix

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
                    req_ids[result.group(0)]=index+1
        return req_ids

    def last_req(self,last_line_index):
        req=linecache.getline(self.file, last_line_index)
        begin_with = [" ","-","*"]
        for l in range(last_line_index+1,10):
            for s in begin_with:
                if linecache.getline(self.file, l).startswith(s):
                    req=req+linecache.getline(self.file, l)
        return req

    #complete req description including multiple lines
    def req_full(self, req_line_index):
        """l: line index
           r: line index (multi lines requirement)
           reqs: list
        """
        reqs = []
        max_req = len(req_line_index)
        for l in range(max_req - 1):
            req = ""
            for r in range(req_line_index[l], req_line_index[l + 1]):
                if linecache.getline(self.file, r)!='\n':   #ignore empty line
                    req = req + (linecache.getline(self.file, r))
            reqs.append(req)
        reqs.append(self.last_req(max_req))
        return reqs

    #split id desc to dict(id)= desc
    def req_split(self,req_id,req_full):
        reqs={}
        for i in range(len(req_id)-1):
            req_desc=req_full[i].split(req_id[i],1)[1].strip()
            req_desc = re.sub("^:","",req_desc) #remove leading colon
            reqs[req_id[i]]=req_desc
        return reqs

    def write_xlsx(self,reqs):
        wb=xlwt.Workbook()
        sheet1=wb.add_sheet(self.prefix)
        r1_style=xlwt.easyxf('font:bold on')
        c1_style=xlwt.easyxf('align:wrap on,vert centre, horiz left')
        sheet1.write(0,0,'Req #',r1_style)
        sheet1.write(0,1,'Req Description',r1_style)
        sheet1.col(0).width=5*1000
        sheet1.col(1).width=30*1000
        for index,key in enumerate(reqs):
            sheet1.write(index+1,0,key)
            sheet1.write(index+1,1,reqs[key],c1_style)
        wb.save('Reqs.xls')

def main():
    origin = "sad.pdf"
    txtfile = "Reqs.txt"
    predoc=PrepDocs(origin,txtfile)
    predoc.write_file
    req_inst=Requirements(txtfile,"SADREQ")
    req_num=list(req_inst.req_ids.keys())
    req_line_index=list(req_inst.req_ids.values())
    req_full=req_inst.req_full(req_line_index)
    reqs=req_inst.req_split(req_num,req_full)
    req_inst.write_xlsx(reqs)
    # print(predoc.pdf2txt())
    # print(req_num)



if __name__=="__main__":
    main()