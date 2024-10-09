import pytest
from pathlib import Path
from nbcheckmate.nbcheckmate import ResultsTests

@pytest.fixture
def results():
    pickle_name = Path(__file__).stem + '.pkl'
    return ResultsTests.load(pickle_name)


def test_returns(results):
    assert results.functions['f']() == None, "This function should not return anything"
    
def test_print(capsys, results):
    results.functions['f']()
    captured = capsys.readouterr()
    assert captured.out.split('\n').count('True') == 2, "This function should print two True"
    
