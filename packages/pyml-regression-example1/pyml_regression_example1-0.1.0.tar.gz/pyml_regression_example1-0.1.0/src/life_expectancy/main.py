import locale
import logging
import os
import platform

from pathlib import Path

import click
import colorama
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px  # type: ignore

# import plotly.graph_objects as go
from plotly.graph_objs import Figure  # type: ignore
from sphinx_click.rst_to_ansi_formatter import make_rst_to_ansi_formatter

from life_expectancy import click_helpers, helpers
from life_expectancy.config import Config
from life_expectancy.constants import FileNames, Inequality


# Most users should depend on colorama >= 0.4.6, and use just_fix_windows_console().
colorama.just_fix_windows_console()
# Set the locale to the user's default setting
locale.setlocale(locale.LC_ALL, "")
# Set the documentation URL for make_rst_to_ansi_formatter()
doc_url = "https://hakonhagland.github.io/pyml-regressions-example1/main/index.html"
# CLI colors for make_rst_to_ansi_formatter()
cli_colors = {
    "heading": {"fg": colorama.Fore.GREEN, "style": colorama.Style.BRIGHT},
    "url": {"fg": colorama.Fore.CYAN, "style": colorama.Style.BRIGHT},
    "code": {"fg": colorama.Fore.BLUE, "style": colorama.Style.BRIGHT},
}
click_command_cls = make_rst_to_ansi_formatter(doc_url, colors=cli_colors)

np.random.seed(42)  # make the output stable across runs
plt.rc("font", size=12)
plt.rc("axes", labelsize=14, titlesize=14)
plt.rc("legend", fontsize=12)
plt.rc("xtick", labelsize=10)
plt.rc("ytick", labelsize=10)
# Check for a display (relevant for Linux)
if platform.system() != "Windows":  # pragma: no cover
    if os.environ.get("DISPLAY") is None:
        # Set to a non-interactive backend if there's no display, e.g. GitHub Actions
        matplotlib.use("Agg")


@click.group(cls=make_rst_to_ansi_formatter(doc_url, group=True, colors=cli_colors))
@click.option("--verbose", "-v", is_flag=True, help="Show verbose output")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """``life-expectancy`` let's you explore life expectancy data presented in Chapter
    1 of the book `Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow (3rd ed.) <https://github.com/ageron/handson-ml3>`_.


    * ``download-data``: downloads the ``.csv`` data file from
      `the book web page <https://github.com/ageron/handson-ml3>`_.

    * ``plot-data``: plots the data using `matplotlib <https://matplotlib.org/stable/index.html>`_.

    """
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        # logging.basicConfig(level=logging.WARNING)


@main.command(cls=click_command_cls)
def download_data() -> None:
    """``life-expectancy download-data`` downloads the life-expectancy data. First,
    the simplified data from `the book's web page
    <https://github.com/ageron/handson-ml3>`_, is downloaded, then the
    full `better life index` data will be downloaded from
    `sdmx.oecd.org <https://sdmx.oecd.org/archive/>`_,
    and finally the GDP per capita data will be downloaded from
    `ourworldindata.org <https://ourworldindata.org/grapher/gdp-per-capita-worldbank>`_. NOTE:
    The last data file is not available for direct download, so it has been uploaded
    to the author's GitHub repo instead."""
    config = Config()
    datadir = config.get_data_dir()
    helpers.download_data(datadir)


@main.command(cls=click_command_cls)
@click.option("--plotly", "-p", is_flag=True, help="Use Plotly for plotting")
def plot_simplified(plotly: bool) -> None:
    """``life-expectancy plot-simplified`` scatter plots the simplified downloaded data. If the data
    is not found, it will be downloaded. The data can be plotted using Matplotlib or Plotly, with the
    ``--plotly`` option."""
    logging.info(f"Matplotlib backend: {matplotlib.get_backend()}")
    config = Config()
    lifesat = helpers.get_lifesat_data(config, download=True)
    if plotly:
        fig = px.scatter(
            lifesat,
            x="GDP per capita (USD)",
            y="Life satisfaction",
            text="Country",
            title="Life Satisfaction vs GDP per Capita",
            labels={
                "GDP per capita (USD)": "GDP per Capita (USD)",
                "Life satisfaction": "Life Satisfaction",
            },
            hover_name="Country",
        )
        fig.update_traces(textposition="top center")
        fig.show()
    else:
        if lifesat is not None:
            lifesat.plot(
                kind="scatter",
                grid=True,
                x="GDP per capita (USD)",
                y="Life satisfaction",
            )
            plt.axis([23_500, 62_500, 4, 9])  # [xmin, xmax, ymin, ymax]
            plt.show()  # type: ignore


@main.command(cls=click_command_cls)
@click.option(
    "--details", "-d", is_flag=True, help="Show detailed data about each file"
)
def info(details: bool) -> None:
    """``life-expectancy info`` prints information about the downloaded data files."""
    config = Config()
    datadir = config.get_data_dir()
    lifesat_file = Path(datadir) / FileNames.lifesat_csv
    lifesat_full_file = Path(datadir) / FileNames.lifesat_full_csv
    gdp_file = Path(datadir) / FileNames.gdb_per_capita_csv
    if lifesat_file.exists():
        if details:
            lifesat = pd.read_csv(lifesat_file)
            lifesat.info()
        else:
            print(f"Found: {lifesat_file}")
    if lifesat_full_file.exists():
        if details:
            lifesat_full = pd.read_csv(lifesat_full_file)
            lifesat_full.info()
        else:
            print(f"Found: {lifesat_full_file}")
    if gdp_file.exists():
        if details:
            gdp = pd.read_csv(gdp_file)
            gdp.info()
        else:
            print(f"Found: {gdp_file}")


@main.command(cls=click_command_cls)
def info_gdp() -> None:
    """``life-expectancy info-gdp`` prints information about the GDP data file."""
    config = Config()
    gdp = helpers.get_gdp_data(config, download=False)
    if gdp is not None:
        # Count the number of unique countries in the 'Entity' column
        num_unique_countries = gdp["Entity"].nunique()
        print(f"Number of countries: {num_unique_countries}")


@main.command(cls=click_command_cls)
@click.option("--year", "-y", type=int, default=2021, help="Year to filter the data")
@click.option("--plotly", "-p", is_flag=True, help="Use Plotly for plotting")
def plot_gdp(year: int, plotly: bool) -> None:
    """``life-expectancy plot-gdp`` creates a bar plot of the GDP data. If the data
    is not found, it will be downloaded. The data is filtered by the year
    specified with the ``--year`` option. The default year is 2021.
    The data can be plotted using Matplotlib or Plotly, with the ``--plotly``
    option."""
    logging.info(f"Matplotlib backend: {matplotlib.get_backend()}")
    config = Config()
    gdp = helpers.get_gdp_data(config, download=True)
    if gdp is not None:
        gdp_year = gdp[gdp["Year"] == year]
        gdp_column = "GDP per capita, PPP (constant 2017 international $)"
        gdp_year = gdp_year.sort_values(by=gdp_column, ascending=False)
        if plotly:
            fig_plotly: Figure = px.bar(
                gdp_year,
                x="Entity",
                y=gdp_column,
                title=f"GDP per Capita by Country for the Year {year}",
                labels={"Entity": "Country", gdp_column: gdp_column},
            )
            fig_plotly.update_layout(xaxis_tickangle=-90)
            fig_plotly.show()
        else:
            # plt.figure(figsize=(23, 10))
            plt.bar(gdp_year["Entity"], gdp_year[gdp_column], color="skyblue")
            plt.xticks(rotation=90)
            plt.xlabel("Country")
            plt.ylabel(gdp_column)
            plt.title(f"GDP per Capita by Country for the Year {year}")
            plt.tight_layout()
            # manager = plt.get_current_fig_manager()
            # manager.full_screen_toggle()
            plt.show()  # type: ignore


@main.command(cls=click_command_cls)
@click.argument("column_name", type=str)
@click.option("--unique", "-u", is_flag=True, help="Show unique values")
def bli_extract_column(column_name: str, unique: bool) -> None:
    """``life-expectancy bli-extract-column`` extracts a column from the full
    Better Life Index data file."""
    config = Config()
    bli = helpers.get_bli_data(config, download=True)
    if bli is not None:
        if unique:
            print(bli[column_name].unique())
        else:
            print(bli[column_name])


@main.command(cls=click_command_cls)
@click.option(
    "--inequality",
    callback=click_helpers.validate_inequality,
    default="TOT",
    help="Which sub table to include",
)
def bli_extract_subtable(inequality: Inequality) -> None:
    """``life-expectancy bli-extract-subtable`` extracts a sub table from the full Better Life Index data file.
    It extracts all rows where the 'INEQUALITY' column matches the inequality argument. Then, creates
    a pivot table with the 'Country' column as the index, the 'Indicator' column as the columns,
    and the 'OBS_VALUE' column as the values. Valid values for the inequality argument are:
    TOT, WMN, MN, LW, and HGH. (Or alternatively use the full names: TOTAL, WOMAN, MAN, LOW, HIGH)."""
    config = Config()
    bli = helpers.get_bli_data(config, download=True)
    if bli is not None:
        # Extract the sub table
        bli_inequality = bli[bli["INEQUALITY"] == inequality.value]
        bli_sub = bli_inequality.pivot(
            index="Country", columns="Indicator", values="OBS_VALUE"
        )
        print(bli_sub.to_csv(sep="|"))
