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
        self.dates = []
        self.dates_dirs = []
        self._save_data_to_coresponding_file()
        self.check_files_saved()

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
        self._append_date(date)
        self._append_date_dir(Path(INPUT_PATH) / date)

        device_name = DEVICE_MAP[base_name.split("-")[-1][:-4]]

        new_date_directory = Path(INPUT_PATH) / date / device_name

        new_date_directory.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(Path(INPUT_PATH) / Path(NEW_INPUT) / path, "r") as zip_ref:
            # Extract all the files into the new folder
            # Log the names of all the files in the zip file
            # for filename in zip_ref.namelist():
            #     if filename[:-4] not in SENSORS:
            #         logging.warning(f"No sensor data for : {filename[:-4]}")

            zip_ref.extractall(new_date_directory)

            # file_path = new_date_directory / filename
            # if os.stat(file_path).st_size == 0:
            #     logging.warning(f"The file {filename} is empty")

        # add offset to txt file
        self._add_offset(device_name, new_date_directory)

    def _append_date(self, date: str) -> None:
        """append date to self.dates if not already there

        Parameters
        ----------
        date : str
            date to be appended
        """
        if date not in self.dates:
            self.dates.append(date)

    def _append_date_dir(self, date_dir: str) -> None:
        """append date_dir to self.dates_dirs if not already there

        Parameters
        ----------
        date_dir : str
            date_dir to be appended
        """
        if date_dir not in self.dates_dirs:
            self.dates_dirs.append(date_dir)

    def _add_offset(self, device: str, path: Path) -> None:
        """Add offset to specific device into txt file in miliseconds

        Parameters
        ----------
        device : str
            name of device
        path : Path
            path where the offset.txt file should be created
        """
        DEVICE_NUMBER[device]
        with open(path / "offset.txt", "w") as f:
            f.write(f"{DEVICE_TIME_OFFSET[DEVICE_NUMBER[device]]}\n")

    def check_files_saved(self) -> None:
        """Check if all files were saved to specific folder"""
        total_devices = len(DEVICE_MAP.values())
        for date_dir in self.dates_dirs:
            non_missing_devices = 0
            missing_devices = []
            for device in DEVICE_MAP.values():
                if not os.path.exists(date_dir / device):
                    missing_devices.append(device)
                else:
                    non_missing_devices += 1
            print(f"\nChecking {date_dir}:")
            if non_missing_devices == total_devices:
                print(f"Devices: {non_missing_devices}/{total_devices} ✅")
            else:
                print(f"Devices: {non_missing_devices}/{total_devices} 🔥")
            if missing_devices:
                print("Missing devices:")
                for device in missing_devices:
                    print(f"{device}: ❌")

    def delete_new_inputs(self) -> None:
        """delate input files from !new_input folder"""
        path = Path(INPUT_PATH, NEW_INPUT)
        for file in path.iterdir():
            os.remove(file)
