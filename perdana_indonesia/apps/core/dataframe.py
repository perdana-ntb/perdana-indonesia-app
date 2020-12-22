import pandas as pd


class DataframeUtil(object):
    @staticmethod
    def getValidatedDataframe(path: str) -> pd.DataFrame:
        df = pd.read_excel(path, dtype=str)
        df.columns = df.columns.str.lower()
        df = df.fillna(-1)
        return df.mask(df == -1, None)
