import pytest
import os

from coolkit.lib.abs_path import abs_path
from coolkit.lib.files import remove


def test_view():
    print()
    cwd = abs_path(os.getcwd())
    try:
        loc = cwd+'/test/contests/837'
        os.chdir(loc)
        remove(loc+'/.coolkit')
        os.system('coolkit init')
        os.system('coolkit view user srbcheema1')
        os.system('coolkit view contest')
        os.system('coolkit view prob A')
        os.system('coolkit view upcomming')
        os.chdir(cwd)
    except Exception as e:
        remove(loc+'/.coolkit')
        os.chdir(cwd)
        raise e

