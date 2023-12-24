import logging
import os
import zipfile
from pathlib import Path

import pandas as pd

from .device_namespace import (
    CAM_OFFSET,
    DEVICE_MAP,
    DEVICE_NUMBER,
    DEVICE_TIME_OFFSET,
    INPUT_PATH,
    NEW_INPUT,
    SENSORS,
)

logging.basicConfig(level=logging.INFO)


class FileArranger:
    def __init__(self):
        self._save_data_to_coresponding_file()

    def _save_data_to_coresponding_file(self) -> None:
        names = self._get_folder_names()

        for name in names:
            self._extract_zip(name)

    def _get_folder_names(self) -> list[str]:
        """Get names of folders in input_data/!new_input

        Returns
        -------
        list[str]
            list with names of folder for each device
        """

        path = Path(INPUT_PATH, NEW_INPUT)
        return [file.name for file in path.iterdir() if file.suffix == ".zip"]

    def _extract_zip(self, path: str) -> None:
        """Extract zip file to specific folder, add offset to txt file in that folder

        Parameters
        ----------
        path : str
            path to zip file
        """

        base_name = os.path.basename(Path(INPUT_PATH) / Path(NEW_INPUT) / path)
        date = base_name.split("_")[0]

        device_name = DEVICE_MAP[base_name.split("-")[-1][:-4]]

        # Create a new folder with the same name as the zip file
        new_date_directory = Path(INPUT_PATH) / date / device_name
        new_date_directory.mkdir(parents=True, exist_ok=True)
        logging.info(f"Device: {device_name} with date: {date} will be saved to folder")

        with zipfile.ZipFile(Path(INPUT_PATH) / Path(NEW_INPUT) / path, "r") as zip_ref:
            # Extract all the files into the new folder
            # Log the names of all the files in the zip file
            for filename in zip_ref.namelist():
                if filename[:-4] not in SENSORS:
                    logging.warning(f"No sensor data for : {filename[:-4]}")

            zip_ref.extractall(new_date_directory)

        file_path = new_date_directory / filename
        if os.stat(file_path).st_size == 0:
            logging.warning(f"The file {filename} is empty")

        # add offset to txt file
        self.add_offset(device_name, new_date_directory)

    def add_offset(self, device: str, path: Path) -> None:
        """Add offset to specific device into txt file in miliseconds

        Parameters
        ----------
        device : str
            name of device
        path : Path
            path where the offset.txt file should be created
        """
        DEVICE_NUMBER[device]
        with open(path / "offset.txt", "a") as f:
            f.write(f"{DEVICE_TIME_OFFSET[DEVICE_NUMBER[device]]}\n")

    def delete_new_inputs(self) -> None:
        """delate input files from !new_input folder"""
        path = Path(INPUT_PATH, NEW_INPUT)
        for file in path.iterdir():
            os.remove(file)
