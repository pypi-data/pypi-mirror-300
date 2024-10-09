import enum


class FileNames:
    lifesat_csv = "lifesat.csv"
    lifesat_full_csv = "oecd_bli_2024.csv"
    gdb_per_capita_csv = "gdp-per-capita-worldbank.csv"


class Inequality(enum.Enum):
    """Inequality measures."""

    TOTAL = "TOT"
    WOMAN = "WMN"
    MAN = "MN"
    LOW = "LW"
    HIGH = "HGH"

    @staticmethod
    def keys() -> set[str]:
        return set(Inequality.__members__.keys())

    @staticmethod
    def values() -> set[str]:
        return {member.value for member in Inequality}
