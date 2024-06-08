from ast import literal_eval
from datetime import timedelta
from typing import Optional

import pandas as pd


def calculate_camera_time_offset(PHONE_TIME: list, CAMERA_TIME: list) -> int:
    """Calculate offset for camera time

    Parameters
    ----------
    PHONE_TIME : list
        list with phone time
    PHONE_OFFSET : int
        offset for phone time
    CAMERA_TIME : int
        camera time

    Returns
    -------
    int
        offset for camera time
    """
    phone_delta_time = timedelta(
        hours=PHONE_TIME[0],
        minutes=PHONE_TIME[1],
        seconds=PHONE_TIME[2],
        milliseconds=PHONE_TIME[3] * 100,
    )
    camerta_delta_time = timedelta(
        hours=CAMERA_TIME[0],
        minutes=CAMERA_TIME[1],
        seconds=CAMERA_TIME[2],
    )
    # = phone_delta_time + timedelta(milliseconds=PHONE_OFFSET)
    return (phone_delta_time - camerta_delta_time).total_seconds() * 1000


def load_data_for_device(device_names: list, current_date: str) -> dict:
    """
    Load data for each device for a given date.

    Parameters
    ----------
    device_names : list
        List of device names for which data is to be loaded.
    current_date : str
        The date for which data is to be loaded, in the format 'YYYY-MM-DD'.

    Returns
    -------
    dict
        A dictionary where the keys are device names and the values are pandas DataFrames containing the data for each device.
    """
    df_dict = {}
    for device_name in device_names:
        res = None
        print(f"device_name: {device_name}")
        try:
            res = pd.read_csv(f"data/{current_date}/{device_name}/final_df.csv")
            for col in res.columns:
                if col != "time":
                    res[col] = res[col].apply(
                        lambda x: literal_eval(x) if isinstance(x, str) else x
                    )
                else:
                    res[col] = pd.to_datetime(res[col])
        except FileNotFoundError:
            print(f"data/{current_date}/{device_name}/")
        except pd.errors.EmptyDataError:
            print(f"data/{current_date}/{device_name}/")

        df_dict[device_name] = res
    return df_dict
