import pytest
from pathlib import Path
from nbcheckmate.nbcheckmate import ResultsTests

@pytest.fixture
def results():
    pickle_name = Path(__file__).stem + '.pkl'
    return ResultsTests.load(pickle_name)


def test_description(results):
    assert results.variables['v'] == "amazing", "Come on, this challenge was amazing !"
    

    
