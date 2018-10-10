import pytest


try:
    from terminaltables import AsciiTable
except:
    err = """
    You haven't installed the required dependencies.
    """
    print(err)
    import sys, traceback,os
    if(os.environ['HOME'] == 'srb'):
        traceback.print_exc()
    sys.exit(1)


from coolkit.lib.Profile import Dummy_user

def test_Profile():
    print()
    uname='srbcheema1'
    dummy_user = Dummy_user(uname,verbose=False)
    dummy_user.print_data()
    print(AsciiTable(dummy_user.contest_table).table)
