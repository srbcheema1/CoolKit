import pytest


try:
    from terminaltables import AsciiTable
except:
    err = """
    You haven't installed the required dependencies.
    """
    print(err)
    sys.exit(0)


from coolkit.lib.Profile import Dummy_user

def test_Profile():
    print()
    uname='srbcheema1'
    dummy_user = Dummy_user(uname,verbose=False)
    dummy_user.print_data()
    print(AsciiTable(dummy_user.contest_table).table)
