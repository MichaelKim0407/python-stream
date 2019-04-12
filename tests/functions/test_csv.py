from stream.functions.csv import Csv


def test_csv():
    reader = Csv()
    assert tuple(reader(['x,y', '1,2'])) == (
        ['x', 'y'],
        ['1', '2'],
    )


def test_delimiter():
    reader = Csv(delimiter='\t')
    assert tuple(reader(['x\ty', '1\t2'])) == (
        ['x', 'y'],
        ['1', '2'],
    )
