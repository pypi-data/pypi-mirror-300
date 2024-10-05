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
                {k: v for k, v in flight.items() if not k.startswith("@")}
                for flight in flights
            ],
            headers="keys",
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
                {k: v for k, v in profile.items() if not k.startswith("@")}
                for profile in profiles
            ],
            headers="keys",
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
                {k: v for k, v in trip.items() if not k.startswith("@")}
                for trip in trips
            ],
            headers="keys",
        )
    )
