import logging
import re

import pandas as pd
import plotly.express as px  # type: ignore
import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner
from pytest_mock.plugin import MockerFixture

from life_expectancy.constants import FileNames
import life_expectancy.main as main
from .common import DataFileContents, MockRequestGet, PrepareConfigDir, PrepareDataDir


@pytest.mark.parametrize("verbose", [True, False])
class TestMainCmd:
    def test_help(
        self,
        verbose: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["download-data", "--help"]
        if verbose:
            args.insert(0, "-v")
        result = runner.invoke(main.main, args)
        assert result.stdout.startswith("Usage: main download-data [OPTIONS]")


class TestDownloadDataCmd:
    @pytest.mark.parametrize("datafile_exists", [True, False])
    def test_invoke(
        self,
        datafile_exists: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
        datafile_contents: DataFileContents,
        mock_requests_get: MockRequestGet,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=datafile_exists)
        prepare_config_dir(add_config_ini=True)
        if not datafile_exists:
            file_contents = datafile_contents(FileNames.lifesat_csv)
            mock_requests_get(file_contents)
        runner = CliRunner()
        args = ["download-data"]
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0


class TestPlotDataCmd:
    @pytest.mark.parametrize("datafile_exists, plotly", [(True, False), (False, True)])
    def test_invoke(
        self,
        datafile_exists: bool,
        plotly: bool,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
        mock_requests_get: MockRequestGet,
        datafile_contents: DataFileContents,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=datafile_exists)
        prepare_config_dir(add_config_ini=True)
        if not datafile_exists:
            file_contents = datafile_contents(FileNames.lifesat_csv)
            # Create a mock response object
            mock_requests_get(datafile_contents=file_contents)
        if plotly:
            # mocker.patch("plotly.express.scatter", return_value=None)
            mock_scatter = mocker.patch.object(px, "scatter", autospec=True)
            mock_fig = mocker.MagicMock()  # Create a mock for the figure
            mock_scatter.return_value = mock_fig  # px.scatter returns a figure
        else:
            mock_plot = mocker.patch.object(pd.DataFrame, "plot")
            mocker.patch("matplotlib.pyplot.show", return_value=None)
            import matplotlib

            matplotlib.use("Agg")
        runner = CliRunner()
        args = ["plot-simplified"]
        if plotly:
            args.append("--plotly")
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0
        if plotly:
            mock_scatter.assert_called_once_with(
                mocker.ANY,  # lifesat dataframe
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
            mock_fig.update_traces.assert_called_once_with(textposition="top center")
            mock_fig.show.assert_called_once()
        else:
            mock_plot.assert_called_once_with(
                kind="scatter",
                grid=True,
                x="GDP per capita (USD)",
                y="Life satisfaction",
            )


class TestInfoCmd:
    @pytest.mark.parametrize(
        "datafiles_exists,details",
        [(True, False), (True, True), (False, True), (False, False)],
    )
    def test_invoke(
        self,
        datafiles_exists: bool,
        details: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=datafiles_exists)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["info"]
        if details:
            args.append("--details")
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0


class TestInfoGdpCmd:
    def test_invoke(
        self,
        caplog: LogCaptureFixture,
        # capsys: CaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True)
        prepare_config_dir(add_config_ini=True)
        runner = CliRunner()
        args = ["info-gdp"]
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0
        assert "Number of countries: 1" in result.output
        assert caplog.records[-1].message.startswith("Read config file:")


class TestPlotGdpCmd:
    @pytest.mark.parametrize("plotly", [True, False])
    def test_invoke(
        self,
        plotly: bool,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=True)
        prepare_config_dir(add_config_ini=True)
        if plotly:
            # mocker.patch("plotly.express.scatter", return_value=None)
            mock_bar = mocker.patch.object(px, "bar", autospec=True)
            mock_fig = mocker.MagicMock()  # Create a mock for the figure
            mock_bar.return_value = mock_fig  # px.bar returns a figure
        else:
            import matplotlib.pyplot

            mock_plt = mocker.patch(
                "life_expectancy.main.plt", autospec=matplotlib.pyplot
            )
        runner = CliRunner()
        args = ["plot-gdp"]
        if plotly:
            args.append("--plotly")
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0
        if plotly:
            mock_bar.assert_called_once_with(
                mocker.ANY,  # lifesat dataframe
                x="Entity",
                y="GDP per capita, PPP (constant 2017 international $)",
                title="GDP per Capita by Country for the Year 2021",
                labels=mocker.ANY,
            )
            mock_fig.update_layout.assert_called_once_with(xaxis_tickangle=-90)
            mock_fig.show.assert_called_once()
        else:
            gdp_column = "GDP per capita, PPP (constant 2017 international $)"
            mock_plt.bar.assert_called_with(mocker.ANY, mocker.ANY, color="skyblue")
            mock_plt.xticks.assert_called_with(rotation=90)
            mock_plt.xlabel.assert_called_with("Country")
            mock_plt.ylabel.assert_called_with(gdp_column)
            mock_plt.title.assert_called_with(
                "GDP per Capita by Country for the Year 2021"
            )
            mock_plt.tight_layout.assert_called_once()
            mock_plt.show.assert_called_once()


class TestBliExtractColumnCmd:
    @pytest.mark.parametrize("datafiles_exists,unique", [(True, False), (False, True)])
    def test_invoke(
        self,
        datafiles_exists: bool,
        unique: bool,
        caplog: LogCaptureFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
        mock_requests_get: MockRequestGet,
        datafile_contents: DataFileContents,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=datafiles_exists)
        prepare_config_dir(add_config_ini=True)
        if not datafiles_exists:
            # Create a mock response object
            file_contents = datafile_contents(FileNames.lifesat_full_csv)
            mock_requests_get(datafile_contents=file_contents)
        runner = CliRunner()
        args = ["bli-extract-column", "INEQUALITY"]
        if unique:
            args.append("--unique")
        result = runner.invoke(main.main, args)
        assert result.exit_code == 0
        if unique:
            assert "['TOT' 'MN']" in result.output
        else:
            assert "TOT" in result.output


class TestBliExtractSubTableCmd:
    @pytest.mark.parametrize(
        "datafile_exists,bad_inequality,inequality",
        [(True, False, "TOT"), (False, True, "BAD"), (False, False, "TOTAL")],
    )
    def test_invoke(
        self,
        datafile_exists: bool,
        bad_inequality: bool,
        inequality: str,
        caplog: LogCaptureFixture,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
        mock_requests_get: MockRequestGet,
        datafile_contents: DataFileContents,
    ) -> None:
        caplog.set_level(logging.INFO)
        prepare_data_dir(datafiles_exists=datafile_exists)
        prepare_config_dir(add_config_ini=True)
        if not datafile_exists:
            # Create a mock response object
            file_contents = datafile_contents(FileNames.lifesat_full_csv)
            mock_requests_get(datafile_contents=file_contents)
        runner = CliRunner()
        args = ["bli-extract-subtable", "--inequality", inequality]
        result = runner.invoke(main.main, args)
        if bad_inequality:
            assert result.exit_code != 0
            assert result.exception is not None
        else:
            assert result.exit_code == 0
            # Windows uses '\r\n' for newlines, so normalize the output
            normalized_output = re.sub(r"\r\n?", "\n", result.output)
            assert normalized_output.startswith(
                "Country|Labour market insecurity\nAustria"
            )
