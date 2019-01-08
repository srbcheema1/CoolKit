import pytest

from srblib import on_travis

from coolkit.lib.Contest import Contest

def test_contest():
    print()
    temp_contest = Contest('920')
    temp_contest.pull_contest()
    temp_contest.display_contest()

    Contest.upcoming_contest(display=True)
