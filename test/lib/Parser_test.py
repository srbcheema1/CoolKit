import pytest

from srblib import on_travis

from coolkit.lib.Parser import Parser

def test_Parser():
    print()
    parser = Parser.create_parser()
