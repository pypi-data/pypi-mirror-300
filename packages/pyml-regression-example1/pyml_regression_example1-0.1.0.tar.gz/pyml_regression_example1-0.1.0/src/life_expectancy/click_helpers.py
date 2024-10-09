from life_expectancy.constants import Inequality
from typing import Union
import click


def validate_inequality(
    ctx: click.Context, param: Union[click.Option, click.Parameter], value: str
) -> Inequality:
    if value in Inequality.keys():
        return Inequality[value]
    try:
        return Inequality(value)
    except ValueError:
        values = ", ".join(list(Inequality.values()))
        keys = ", ".join(list(Inequality.keys()))
        raise click.BadParameter(
            f"Invalid inequality value '{value}'. Must be one of: {values}. "
            f"Or alternatively, use the full names: {keys}."
        )
