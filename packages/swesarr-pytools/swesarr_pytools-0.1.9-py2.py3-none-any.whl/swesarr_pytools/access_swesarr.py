"""
This main class has the following functionality
1. Data retrieval for SWESARR flight from https://glihtdata.gsfc.nasa.gov/files/radar/SWESARR/prerelease
2. Metadata retrieval for SWESARR flight path
3. Singular Flight path download for one flight line but six frequencies
4. Singular frequency download for a given flight line
5. Flight path search using date
"""

__author__ = "Evi Ofekeze"
__authors__ = ["HP Marshal"]
__contact__ = "eviofekeze@u.boisestate.edu"
__copyright__ = "Copyright 2024, Boise State University, Boise ID"
__group__ = "Cryosphere GeoPhysics and Remote Sensing Laboratory"
__credits__ = ["Evi Ofekeze", "HP Marshal"]
__email__ = "eviofekeze@u.boisestate.edu"
__maintainer__ = "developer"
__status__ = "Research"

import itertools
import os
from os.path import join
from subprocess import Popen
from getpass import getpass
from netrc import netrc

from pathlib import Path
from typing import Dict, List, Union
from dataclasses import dataclass, field

import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from datetime import datetime
from datetime import date

try:
    from .utils.swesarr_utils import get_logger
except ImportError:
    from utils.swesarr_utils import get_logger

logger = get_logger(__file__)


def create_netrc(urs = 'urs.earthdata.nasa.gov'):
    """
    Creates netrc file for user.
    This function is adapted from: https://git.earthdata.nasa.gov/projects/LPDUR/repos/daac_data_download_python/browse/EarthdataLoginSetup.py
    """
    prompt_username = "Enter NASA Earthdata Login Username \n(or create an account at urs.earthdata.nasa.gov): "
    prompt_password = "Enter NASA Earthdata Login Password: "

    try:
        netrc_dir = os.path.expanduser("~/.netrc")
        netrc(netrc_dir).authenticators(urs)[0]

    # Below, create a netrc file and prompt user for NASA Earthdata Login Username and Password
    except FileNotFoundError:
        home_dir = os.path.expanduser("~")
        netrc_fp = join(home_dir,'.netrc')
        Popen(f'touch {netrc_fp} | chmod og-rw {netrc_fp} | echo machine {urs} >> {netrc_fp}', shell=True)
        Popen(f'echo login {getpass(prompt=prompt_username)} >> {netrc_fp}', shell=True)
        Popen(f'echo password {getpass(prompt=prompt_password)} >> {netrc_fp}', shell=True)

    # Determine OS and edit netrc file if it exists but is not set up for NASA Earthdata Login
    except TypeError:
        home_dir = os.path.expanduser("~")
        netrc_fp = join(home_dir,'.netrc')
        Popen(f'echo machine {urs} >> {netrc_fp}'.format(home_dir + os.sep, urs), shell=True)
        Popen(f'echo login {getpass(prompt=prompt_username)} >> {netrc_fp}', shell=True)
        Popen(f'echo password {getpass(prompt=prompt_password)} >> {netrc_fp}', shell=True)

    # If permission denied t
    except PermissionError:
        logger.warning('Permission error. Change permissions on netrc file.')



@dataclass
class AccessSAR:
    url: str = f"https://glihtdata.gsfc.nasa.gov/files/radar/SWESARR/prerelease"
    ext: str = ""
    flight_names: List[str] = field(default_factory=dict, init=False)
    flight_dates: List = field(default_factory=dict, init=False)
    data_meta: Dict[str, str] = field(default_factory=dict, init=False)

    def __post_init__(self):
        self.retrieve_meta()

    def retrieve_meta(self) -> None:
        response = requests.get(self.url)
        if response.ok:
            response_text = response.text
        else:
            return response.raise_for_status()

        soup = BeautifulSoup(response_text, features='html.parser')
        self.flight_names = [f"{self.url}{node.get('href')}" for node in soup.find_all('a') if
                             node.get('href').endswith(self.ext)]
        self.flight_names = self.flight_names[5:-1]
        self.flight_names = [name[62:] for name in self.flight_names]
        self.flight_dates = [datetime.strptime(date_.split('_')[4], '%y%m%d').date() for date_ in self.flight_names]
        self.data_meta = dict(zip(self.flight_names, self.flight_dates))
        return

    @staticmethod
    def validate_date(some_date: Union[str, date], date_name: str) -> date:
        """
        Parses date and returns valid data

        :param some_date: str | datetime.date
            date to be validated
        :param date_name: Name for error logging
        :return:
        """
        date_formats = ["%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d"]

        if isinstance(some_date, date):
            return some_date

        for date_format in date_formats:
            try:
                parsed_some_date = datetime.strptime(some_date, date_format).date()
                return parsed_some_date
            except (ValueError, TypeError):
                continue
        raise ValueError(f"{date_name} format not recognised")

    def available_date_within_range(self, start_date: Union[str, date], end_date: Union[str, date]) -> List:
        """
        Search for swesarr flight within a time period

        :param start_date: The start date range
        :param end_date:  The end date range
        :return: List of available dates
        """
        start_date = self.validate_date(start_date, date_name="Start Date")
        end_date = self.validate_date(end_date, date_name="End Date")

        result = [date_ for date_ in self.flight_dates if (start_date <= date_ <= end_date)]
        if not result:
            logger.info(f"No flight path was found within the specified range")
        else:
            return result

    @staticmethod
    def download_tif(base_url: str, file_name: str) -> None:
        """
        Helper function to download a specific flight path
        :param base_url: The root Url
        :param file_name: The file name corresponding the band
        :return: None
        """
        response = requests.get(base_url)
        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=5 * 1024 * 1024):
                if chunk:
                    file.write(chunk)
        logger.info(f"Downloaded: {base_url}")
        return

    def download_data(self, flight_path: str, folder_name: str, band: str = "all", dem: bool = False) -> None:
        """
        Downloads data for a specified flight path.

        This method downloads the associated data into the specified folder. It also
        allows for filtering by band and includes an option to download DEM (Digital
        Elevation Model) data.

        :param flight_path: str
            The name of the flight path to be downloaded
        :param folder_name: str
            The name of the folder where the downloaded data will be stored
        :param band: str, optional
            Specifies the band to download (e.g., "X", "KuLo", "KuHi"). Defaults to "all",
            which downloads all available bands
        :param dem: bool, optional
            If True, the Digital Elevation Model (DEM) data is downloaded along with the
            band data. Defaults to False
        :return: None
        """
        folder_name = Path(folder_name)
        band = band.lower()
        complete_url = f"{self.url}/{flight_path}/"
        response = requests.get(complete_url)
        if response.status_code != 200:
            print(f"Failed to fetch page content: {response.status_code}")
            return
        soup = BeautifulSoup(response.content, features='html.parser')

        tif_links = [urljoin(complete_url, link['href']) for link in soup.find_all(name='a', href=True) if
                     link['href'].endswith('.tif')]
        if dem:
            tif_links = tif_links
        else:
            tif_links[:] = [item for item in tif_links if "dem" not in item]

        fully_qualified_folder_name = Path(f"{folder_name}/{flight_path}")
        os.makedirs(fully_qualified_folder_name, exist_ok=True)
        if band.lower() == "all":
            for link in tif_links:
                file_name = os.path.join(fully_qualified_folder_name, os.path.basename(link))
                self.download_tif(link, file_name)

        elif band.lower() == "x":
            tif_links = [item for item in tif_links if "09225" in item]
            for link in tif_links:
                file_name = os.path.join(fully_qualified_folder_name, os.path.basename(link))
                self.download_tif(link, file_name)

        elif band.lower() == "kulo":
            tif_links = [item for item in tif_links if "13225" in item]
            for link in tif_links:
                file_name = os.path.join(fully_qualified_folder_name, os.path.basename(link))
                self.download_tif(link, file_name)

        elif band.lower() == "kuhi":
            tif_links = [item for item in tif_links if "17225" in item]
            for link in tif_links:
                file_name = os.path.join(fully_qualified_folder_name, os.path.basename(link))
                self.download_tif(link, file_name)
        return

    def download_all_data(self, folder_name: str, band: str = "all", dem: bool = False) -> None:
        """
        Downloads data for all flights.

        This method iterates over all flight paths generated in `self.flight_names` list
        and downloads the associated data into the specified folder. It also
        allows for filtering by band and includes an option to download DEM (Digital
        Elevation Model) data.

        :param folder_name: str
            The name of the folder where the downloaded data will be stored
        :param band: str, optional
            Specifies the band to download (e.g., "X", "KuLo", "KuHi"). Defaults to "all",
            which downloads all available bands
        :param dem: bool, optional
            If True, the Digital Elevation Model (DEM) data is downloaded along with the
            band data. Defaults to False

        :return: None
        """
        for this_flight_path in self.flight_names:
            self.download_data(
                flight_path=this_flight_path,
                folder_name=folder_name,
                dem=dem,
                band=band
            )
        return


@dataclass
class AccessRadiometer:
    urs_url: str = "https://n5eil01u.ecs.nsidc.org/SNOWEX/SNEX20_SWESARR_TB.001/"
    radiometer_meta: Dict[str, list] = field(default_factory=dict)

    def __post_init__(self):
        create_netrc()
        self.retrieve_meta()

    def retrieve_meta(self) -> None:
        flight_days = ["10", "11", "12"]

        for flight_day in flight_days:
            response = requests.get(f"{self.urs_url}2020.02.{flight_day}/")
            if response.ok:
                response_text = response.text
            else:
                return response.raise_for_status()

            soup = BeautifulSoup(response_text, features='html.parser')
            csv_links = [link['href'] for link in soup.find_all('a') if link['href'].endswith('.csv')]
            csv_links = list(set(csv_links))
            self.radiometer_meta[f"2020.02.{flight_day}"] = csv_links

    def download_radiometer(self, file_name: str, destination_folder: str = ".") -> None:
        """

        :param file_name: file to download
        :param destination_folder: destination to store file
        :return: None
        """
        day: str = file_name.split('_')[7][-2:]
        url_builder: str = f"{self.urs_url}2020.02.{day}/{file_name}"

        response = requests.get(url_builder)

        destination = Path(f"{destination_folder}/2020_02_{day}")
        if destination.exists():
            pass
        else:
            os.makedirs(f"{destination_folder}/2020_02_{day}")

        with open(f"{destination_folder}/2020_02_{day}/{file_name}", 'wb') as handle:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    handle.write(chunk)
                    handle.flush()
        logger.info(f"Downloaded: {file_name}")
        return

    def bulk_download_radiometer(self, destination_folder: str = ".", day: str = "all") -> None:
        """

        :param destination_folder: The folder to store the downloaded data
        :param day: any of  "10", "11", "12" defaults to all which will download all
        :return:
        """
        if day.lower() != "all":
            file_list: List = self.radiometer_meta[f"2020.02.{day}"]
            for file in file_list:
                self.download_radiometer(file_name=file, destination_folder=destination_folder)
        else:
            flight_days = ["10", "11", "12"]
            file_list: List = []

            for day in flight_days:
                file_list.append(self.radiometer_meta[f"2020.02.{day}"])

            file_list = list(itertools.chain(*file_list))
            for file in file_list:
                self.download_radiometer(file_name=file, destination_folder=destination_folder)

        return



if __name__ == '__main__':
    logger.info(f"Nothing to report... Moving on")




