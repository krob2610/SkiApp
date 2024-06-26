import concurrent.futures
from ast import literal_eval
from datetime import timedelta

import pandas as pd

from app.device_namespace import FINAL_DF_SENSORS, TIME
from app.labels_namespace import ORIENTATION, OTHER


class DataLoader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
        # self.granular_data = {}

    def load_transform_data(self):
        res = pd.read_csv(self.data_path)
        for col in res.columns:
            if col not in [TIME, "Curve"]:
                res[col] = res[col].apply(
                    lambda x: literal_eval(x) if isinstance(x, str) else x
                )
            elif col == TIME:
                res[col] = pd.to_datetime(res[col])
            elif col == "Curve":
                res[col] = res[col].apply(lambda x: x if x in ["L", "R"] else False)
        res.set_index(TIME, inplace=True)
        # save data for later use
        self.data = res
        return res


class SplittedLoader:
    def __init__(self, dataframe):
        self.data = dataframe
        self.splitted_data = {}

    # def split_into_granular(self):
    #     # if self.data is None:
    #     #     self.load_transform_data()
    #     data = self.data
    #     if data is None:
    #         raise ValueError("Data is None")
    #     columns = list(data.columns)
    #     granular_columns = list(
    #         filter(lambda col: col not in FINAL_DF_SENSORS, columns)
    #     )
    #     for col in FINAL_DF_SENSORS:
    #         if col not in columns:
    #             continue
    #         else:
    #             # keep only the columns that are granular columns and col - rest should be droped in new datadframne
    #             granular_data = data[granular_columns].copy()
    #             granular_data[col] = data[col]

    #             sensor_df = granular_data[col].apply(pd.Series)

    #             # Rename these columns using the names in `renames_orientation`
    #             sensor_df.columns = ORIENTATION if col == "Orientation" else OTHER

    #             # Drop the original "Orientation" column from `temp`
    #             granular_data = granular_data.drop(columns=[col])

    #             # Join the new orientation columns to `temp`
    #             granular_data = granular_data.join(sensor_df)
    #             self.granular_data[col] = granular_data
