import tabulate
import orjson
import click
from .client import TripItClient
from .__version__ import __version__


@click.group()
@click.pass_context
@click.version_option(
    version=__version__,
    prog_name="tripit-tools",
)
@click.option(
    "--tripit-access-token",
    type=click.STRING,
    envvar="TRIPIT_ACCESS_TOKEN",
    required=True,
)
@click.option(
    "--tripit-access-token-secret",
    type=click.STRING,
    envvar="TRIPIT_ACCESS_TOKEN_SECRET",
    required=True,
)
@click.option(
    "--tripit-client-token",
    type=click.STRING,
    envvar="TRIPIT_CLIENT_TOKEN",
    required=True,
)
@click.option(
    "--tripit-client-token-secret",
    type=click.STRING,
    envvar="TRIPIT_CLIENT_TOKEN_SECRET",
    required=True,
)
def cli(
    ctx,
    tripit_access_token,
    tripit_access_token_secret,
    tripit_client_token,
    tripit_client_token_secret,
):
    ctx.obj = TripItClient(
        access_token=tripit_access_token,
        access_token_secret=tripit_access_token_secret,
        client_token=tripit_client_token,
        client_token_secret=tripit_client_token_secret,
    )


@cli.command()
@click.pass_context
@click.option(
    "--json",
    is_flag=True,
    help="Output as JSON.",
)
def flights(
    ctx,
    json,
):
    flights = ctx.obj.get_flights()
    if json:
        click.echo(
            orjson.dumps(
                {
                    "flights": list(flights),
                },
                option=orjson.OPT_SORT_KEYS,
            ),
        )
        return

    click.echo(
        tabulate.tabulate(
            [
                (
                    flight.get("start_airport_code"),
                    flight.get("end_airport_code"),
                    f'{flight["StartDateTime"]["date"]}T{flight["StartDateTime"]["time"]}{flight["StartDateTime"]["utc_offset"]}',
                    f'{flight["EndDateTime"]["date"]}T{flight["EndDateTime"]["time"]}{flight["EndDateTime"]["utc_offset"]}',
                )
                for flight in flights
            ],
            headers=(
                "Origin",
                "Destination",
                "Departure",
                "Arrival",
            ),
        )
    )


@cli.command()
@click.pass_context
@click.option(
    "--json",
    is_flag=True,
    help="Output as JSON.",
)
def profiles(
    ctx,
    json,
):
    profiles = ctx.obj.get_profiles()
    if json:
        click.echo(
            orjson.dumps(
                {
                    "profiles": list(profiles),
                },
                option=orjson.OPT_SORT_KEYS,
            ),
        )
        return

    click.echo(
        tabulate.tabulate(
            [
                (
                    profile["uuid"],
                    profile["public_display_name"],
                    profile["company"],
                    profile["home_city"],
                )
                for profile in profiles
            ],
            headers=(
                "ID",
                "Name",
                "Company",
                "Location",
            ),
        )
    )


@cli.command()
@click.pass_context
@click.option(
    "--json",
    is_flag=True,
    help="Output as JSON.",
)
def trips(
    ctx,
    json,
):
    trips = ctx.obj.get_trips()
    if json:
        click.echo(
            orjson.dumps(
                {
                    "trips": list(trips),
                },
                option=orjson.OPT_SORT_KEYS,
            ),
        )
        return

    click.echo(
        tabulate.tabulate(
            [
                (
                    trip["id"],
                    trip["display_name"],
                )
                for trip in trips
            ],
            headers=(
                "ID",
                "Name",
            ),
        )
    )
