import json

from srblib import abs_path, verify_file
from srblib import SrbJson

class srbjson:
    def __init__(self):
        pass

    @staticmethod
    def create_file(file_name,template):
        SrbJson(file_name,template)

    @staticmethod
    def extract_data(file_name,template):
        return SrbJson(file_name,template).data

    @staticmethod
    def dump_data(data,file_name,template):
        temp = SrbJson(file_name,template)
        for key in data:
            if(key in temp):
                temp.data[key] = data[key]
        temp._burn_data_to_file() # lazy burning

    global_template = {
        "coolkit":{
            "user":None,
            "pswd":None,

            "site":"codeforces"
        }
    }

    prob_template = {
        "coolkit":{
            "c_name":None,
            "c_type":"contest",
            "c_site":"codeforces",
            "p_name":None,

            "hash":"",
            "is_good":False,
            "mult_soln":False,
            "num_test":-1,
            "p_title":"",
            "subm":-1,
            "time_limit":"",

            "h_desc":"",
            "i_desc":"",
            "o_desc":"",
            "p_desc":""
        }
    }

    local_template = {
        "coolkit":{
            "c_name":None,
            "c_type":"contest",
            "c_site":"codeforces",
            "p_name":None,

            "inp":None,
            "init_date":""
        }
    }


    contest_template = {
        "coolkit":{
            "c_site":"codeforces",

            "c_name":None,
            "c_type":"contest",

            "ann_arr":[],
            "c_title":"",
            "hash":"",
            "is_good":False,
            "num_prob":-1,
            "p_name_list":[]
        }
    }
