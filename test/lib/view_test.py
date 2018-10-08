import pytest
import os

from coolkit.lib.abs_path import abs_path
from coolkit.lib.files import remove
from coolkit.lib.utils import utils


def test_view():
    print()
    cwd = abs_path(os.getcwd())
    try:
        loc = cwd+'/test/contests/837'
        os.chdir(loc)
        remove(loc+'/.coolkit')
        assert(os.system('coolkit init')==0)
        assert(os.system('coolkit view user srbcheema1')==0)
        assert(os.system('coolkit view contest')==0)
        assert(os.system('coolkit view prob A')==0)
        assert(os.system('coolkit view upcoming')==0)
        if(utils.do_online_test()):
            assert(os.system('coolkit view friends')==0)
            assert(os.system('coolkit view standings 935')==0)
        os.chdir(cwd)
    except Exception as e:
        remove(loc+'/.coolkit')
        os.chdir(cwd)
        raise e

