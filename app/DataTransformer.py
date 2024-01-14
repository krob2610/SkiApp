from pathlib import Path

import pandas as pd
from device_namespace import DATA_PATH, INPUT_PATH


class DataTransformer:
    def __init__(self, date: str) -> None:
        self.date = date

    def _select_folders(self, date: str) -> None:
        # open folder under INPUT_PATH/date
        path = Path(INPUT_PATH, date)
        # get all folders in INPUT_PATH/date
        folders = [file.name for file in path.iterdir() if file.is_dir()]

        self._select_date_dir()

    # TODO iterate over folders and seek for csv to applay changes

    def _transform_save(self, path: Path) -> None:
        """transform and save single data file

        Parameters
        ----------
        path : Path
            path to single csv file
        """
        df = pd.read_csv(path, sep=",")
        df_time = df.copy()
        df_time["time"] = pd.to_datetime(df["time"], unit="ns")
        offset_path = Path(path.parent, "offset.txt")

        df_real = self._apply_offset(offset_path, df_time)

        last_parts = path.parts[-3:]
        final_path = Path(DATA_PATH, *last_parts)
        folders = final_path.parts[:-1]
        folders = Path(*folders)

        folders.mkdir(parents=True, exist_ok=True)
        df_real.to_csv(final_path, index=False)

    def _apply_offset(self, offset_path: Path, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply an offset to the 'time' column of the DataFrame.

        Parameters:
        offset_path (Path): The path to the file containing the offset value.
        df (pd.DataFrame): The DataFrame to apply the offset to.

        Returns:
        pd.DataFrame: The DataFrame with the offset applied to the 'time' column.
        """
        f = open(offset_path, "r")
        offset = int(f.readline())
        df["time"] = df["time"] + pd.Timedelta(offset, unit="ms")
        return df
