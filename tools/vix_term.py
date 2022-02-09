import pandas as pd


class VixTermStructure:
    def __init__(self, days=1):
        assert days > 0
        self._data = self.download(days)
        self._term_structure = self._data.loc[:, 'F1':'F12']
        self._contango_data = self._data.iloc[:, -3:]

    def download(self, days=1):
        print('Downloading VIX Term-Structure...')

        url = f'http://vixcentral.com/historical/?days={days}'

        data = pd.read_html(url)[0]

        header = data.iloc[0]
        data = data[1:-1]
        data = data.set_index(0)
        del data.index.name
        data.columns = header[1:]

        print("Term-Structure downloaded.")
        return data

    def get(self, month, month2=None):
        if month2 is None:
            return float(self._term_structure.iloc[0, month-1])
        else:
            terms = self._term_structure.iloc[0, month-1: month2-1]
            terms = terms.astype(float)
            return terms

    def contango(self, months=(1, 2)):
        front = self.get(months[0])
        back = self.get(months[1])
        return (back / front - 1.0)


if __name__ == '__main__':
    vts = VixTermStructure()
    print(vts._term_structure)

    print('F1:', vts.get(1))
    print('F2:', vts.get(2))
    print()

    print(vts._contango_data)
    print()

    print('Contango (1/2):', vts.contango((1, 2)))
    print('Contango (3/5):', vts.contango((3, 5)))
    print('Contango (4/7):', vts.contango((4, 7)))
