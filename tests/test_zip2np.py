from zip2np import zip2np

def test_positive_size():
    assert zip2np.load_datasets(".", (64, -64)) == -1