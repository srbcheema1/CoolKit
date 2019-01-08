import pytest

from srblib import show_dependency_error_and_exit
from srblib import on_travis

try:
    from terminaltables import AsciiTable
except:
    show_dependency_error_and_exit()


from coolkit.lib.Profile import Dummy_user

def test_Profile():
    print()
    uname='srbcheema1'
    dummy_user = Dummy_user(uname,verbose=False)
    dummy_user.print_data()
    print(AsciiTable(dummy_user.contest_table).table)
