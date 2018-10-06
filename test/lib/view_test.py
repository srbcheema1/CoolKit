import pytest
import os

from coolkit.lib.abs_path import abs_path
from coolkit.lib.files import remove


def test_view():
    print()
    try:
        cwd = abs_path(os.getcwd())
        loc = cwd+'/test/contests/837'
        os.chdir(loc)
        remove(loc+'/.coolkit')
        os.system('coolkit init')
        os.system('coolkit view user srbcheema1')
        os.system('coolkit view contest')
        os.system('coolkit view prob A')
        os.system('coolkit view upcomming')
    except Exception as e:
        remove(loc+'/.coolkit')
        raise e

