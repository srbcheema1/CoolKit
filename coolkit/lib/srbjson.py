import json

from srblib import abs_path, verify_file
from srblib import SrbJson

class srbjson:
    def __init__(self):
        pass

    global_template = {
        "coolkit":{
            "user":None,
            "pswd":None,
            "site": "codeforces",
            "secondary_user": None,
            "secondary_pswd": None,
            "srb_predictor": False,
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
