from extract_reqs import PrepDocs
from extract_reqs import Requirements
import pytest

txtfile="sysTest/Reqs.txt"
prefix="STTSAD"
req_inst=Requirements(txtfile,prefix)

def test_req_ids():
    assert len(req_inst.req_ids) >10