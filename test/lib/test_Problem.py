import pytest

from coolkit.lib.Problem import Problem
from coolkit.lib.Colour import Colour

def test_Problem():
    print()
    p_name = 'B'
    c_name = 1025
    prob = Problem(p_name,c_name)
    prob.pull_problem(force=False)
    prob.display_problem()
    print(Colour.CYAN+prob.link+Colour.END)
    if(prob.mult_soln):
        print('this problem is having multiple possible solutions')
    else:
        print('this problem is having unique solution')
