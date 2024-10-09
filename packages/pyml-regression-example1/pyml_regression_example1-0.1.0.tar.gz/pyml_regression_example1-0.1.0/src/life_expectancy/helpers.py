import logging
import requests

import pandas as pd
from pathlib import Path
from life_expectancy.config import Config
from life_expectancy.constants import FileNames


def download_data(datadir: Path) -> None:
    """Download data files from various URLs."""
    download_items = []
    filename1 = FileNames.lifesat_csv
    data_url1 = f"https://github.com/ageron/data/raw/main/lifesat/{filename1}"
    download_items.append((filename1, data_url1))
    data_url2 = "https://sdmx.oecd.org/archive/rest/data/OECD,DF_BLI,/all?dimensionAtObservation=AllDimensions&format=csvfilewithlabels"
    filename2 = FileNames.lifesat_full_csv
    download_items.append((filename2, data_url2))
    filename3 = FileNames.gdb_per_capita_csv
    # NOTE: I was not able to find a direct download URL at:
    #     https://ourworldindata.org/grapher/gdp-per-capita-worldbank
    #  instead I downloaded the data manually and uploaded it to my own GitHub repo
    data_url3 = f"https://raw.githubusercontent.com/hakonhagland/pyml-regression-example1/refs/heads/main/data/{filename3}"
    download_items.append((filename3, data_url3))
    download_data_from_url(datadir, download_items=download_items)


def download_file(savename: Path, data_url: str) -> None:
    response = requests.get(data_url)
    response.raise_for_status()  # Ensure we notice bad responses
    savename.parent.mkdir(parents=True, exist_ok=True)
    with open(savename, "w", encoding="utf-8") as f:
        f.write(response.content.decode("utf-8"))
    logging.info(f"Data downloaded and saved to {savename}")


def download_data_from_url(
    datadir: Path, download_items: list[tuple[str, str]]
) -> None:
    for filename, data_url in download_items:
        savename = Path(datadir) / filename
        if savename.exists():
            logging.info(f"Data file {savename} already exists, skipping download")
            continue
        download_file(savename, data_url)


def get_gdp_data(config: Config, download: bool = True) -> pd.DataFrame | None:
    """Return the data from the CSV file as a pandas DataFrame."""
    return get_data(config, download=download, filename=FileNames.gdb_per_capita_csv)


def get_lifesat_data(config: Config, download: bool = True) -> pd.DataFrame | None:
    """Return the data from the CSV file as a pandas DataFrame."""
    return get_data(config, download=download, filename=FileNames.lifesat_csv)


def get_bli_data(config: Config, download: bool = True) -> pd.DataFrame | None:
    """Return the data from the CSV file as a pandas DataFrame."""
    return get_data(config, download=download, filename=FileNames.lifesat_full_csv)


def get_data(config: Config, download: bool, filename: str) -> pd.DataFrame | None:
    """Return the data from the CSV file as a pandas DataFrame."""
    datadir = config.get_data_dir()
    data_file = Path(datadir) / filename
    # Check that the data file exists, if not download it
    if not data_file.exists():
        if download:
            logging.info(f"Data file {data_file} not found. Downloading data ...")
            download_data(datadir)
        else:
            return None
    return pd.read_csv(data_file)
