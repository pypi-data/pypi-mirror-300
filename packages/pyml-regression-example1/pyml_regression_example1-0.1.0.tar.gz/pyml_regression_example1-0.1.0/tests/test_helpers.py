from pytest_mock.plugin import MockerFixture

from life_expectancy.config import Config
import life_expectancy.helpers as helpers
from .common import PrepareConfigDir, PrepareDataDir


class TestDownloadData:
    def test_get_gdp_data(
        self,
        mocker: MockerFixture,
        prepare_config_dir: PrepareConfigDir,
        prepare_data_dir: PrepareDataDir,
    ) -> None:
        prepare_config_dir(add_config_ini=True)
        prepare_data_dir(datafiles_exists=False)
        config = Config()
        gdp = helpers.get_gdp_data(config, download=False)
        assert gdp is None
