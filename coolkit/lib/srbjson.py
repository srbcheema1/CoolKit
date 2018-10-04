import json

from .abs_path import abs_path
from .files import verify_file

class srbjson:
    def __init__(self):
        pass

    @staticmethod
    def create_file(fille,template):
        verify_file(fille)
        jfile = open(fille, 'w')
        json.dump(template,jfile,indent = 4,ensure_ascii = False)
        jfile.close()


    @staticmethod
    def extract_data(file_name,template):
        """
        Extracts json data from the given file
        if there is no such file
            it will create one
        if there is currupt file
            it will create new
        if file is ok
            it will return its content
        """
        fille = abs_path(file_name)
        try:
            jfile = open(fille)
        except FileNotFoundError:
            srbjson.create_file(fille,template)
        jfile = open(fille)
        data = json.load(jfile)
        if(not 'coolkit' in data.keys()):
            srbjson.create_file(fille,template)
            jfile = open(fille)
            data = json.load(jfile)
        return data['coolkit']


    @staticmethod
    def _write_data(data,file_name):
        """
        Write RAW data into a json file
        """
        fille = abs_path(file_name)
        jfile = open(fille, 'w')
        data = {'coolkit':data}
        json.dump(data,jfile,indent = 4,ensure_ascii = False)
        jfile.close()


    @staticmethod
    def dump_data(data,file_name,template):
        """
        create RAW data from LIST
        uses _write_data
        """
        fille = abs_path(file_name)
        dictt = srbjson.extract_data(fille,template)
        for key in data:
            if(key in dictt):
                dictt[key] = data[key]
        srbjson._write_data(dictt,file_name)

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
