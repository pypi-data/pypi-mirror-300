from .__version__ import __version__
from pathlib import Path
from appdirs import user_config_dir
from dotenv import load_dotenv
from os import environ
from queue import Queue
from requests_cache import CacheMixin
from requests_oauthlib import OAuth1Session
from yarl import URL
import datetime
import more_itertools

load_dotenv(override=True)

ACCESS_TOKEN = environ.get("TRIPIT_ACCESS_TOKEN", None)
ACCESS_TOKEN_SECRET = environ.get("TRIPIT_ACCESS_TOKEN_SECRET", None)
CLIENT_TOKEN = environ.get("TRIPIT_CLIENT_TOKEN", None)
CLIENT_TOKEN_SECRET = environ.get("TRIPIT_CLIENT_TOKEN_SECRET", None)

CACHE_NAME = Path(user_config_dir()) / "illallangi-tripit.db"


class Session(
    CacheMixin,
    OAuth1Session,
):
    pass


def try_long(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return value


class TripItClient:
    def __init__(
        self,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        client_token=CLIENT_TOKEN,
        client_token_secret=CLIENT_TOKEN_SECRET,
        base_url="https://api.tripit.com/v1",
    ):
        assert isinstance(access_token, str) and access_token
        assert isinstance(access_token_secret, str) and access_token_secret
        assert isinstance(client_token, str) and client_token
        assert isinstance(client_token_secret, str) and client_token_secret
        if not isinstance(base_url, URL):
            base_url = URL(base_url)

        self.base_url = base_url

        self._session = Session(
            client_key=client_token,
            client_secret=client_token_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
            cache_name=CACHE_NAME,
            backend="sqlite",
            expire_after=3600,
        )

    def get_info(
        self,
    ):
        return {
            "returned": int(datetime.datetime.now().timestamp()),
            "version": __version__,
        }

    def get_objects(
        self,
        key,
        *args,
    ):
        queue = Queue()
        seen = set()

        for arg in args:
            queue.put(
                arg
                % {
                    "format": "json",
                    "page_size": 13,
                    "page_num": 1,
                }
            )

        while not queue.empty():
            url = queue.get()

            if url in seen:
                continue

            seen.add(url)

            response = self._session.get(url)

            response.raise_for_status()

            json = response.json()

            yield from [
                {
                    **o,
                    "@api": {
                        **{
                            k: try_long(v)
                            for k, v in json.items()
                            if k
                            not in [
                                "AirObject",
                                "Profile",
                                "Trip",
                            ]
                        },
                        "from_cache": response.from_cache,
                        "expires": int(response.expires.timestamp()),
                        "url": url.human_repr(),
                        **self.get_info(),
                    },
                }
                for o in more_itertools.always_iterable(
                    json.get(key, []),
                    base_type=dict,
                )
            ]

            if "max_page" in json:
                for page_num in range(
                    1,
                    int(json["max_page"]) + 1,
                ):
                    queue.put(
                        url
                        % {
                            "format": "json",
                            "page_size": 13,
                            "page_num": page_num,
                        }
                    )

    def get_flights(
        self,
    ):
        yield from [
            {
                **segment,
                "@air": {k: v for k, v in air.items() if k not in ["@api", "Segment"]},
                "@api": air["@api"],
            }
            for air in self.get_objects(
                "AirObject",
                self.base_url
                / "list"
                / "object"
                / "traveler"
                / "true"
                / "past"
                / "true"
                / "include_objects"
                / "false"
                / "type"
                / "air",
                self.base_url
                / "list"
                / "object"
                / "traveler"
                / "true"
                / "past"
                / "false"
                / "include_objects"
                / "false"
                / "type"
                / "air",
            )
            for segment in more_itertools.always_iterable(
                air.get("Segment", []),
                base_type=dict,
            )
        ]

    def get_profiles(
        self,
    ):
        return self.get_objects(
            "Profile",
            self.base_url / "get" / "profile",
        )

    def get_trips(
        self,
    ):
        return self.get_objects(
            "Trip",
            self.base_url
            / "list"
            / "trip"
            / "traveler"
            / "true"
            / "past"
            / "true"
            / "include_objects"
            / "false",
            self.base_url
            / "list"
            / "trip"
            / "traveler"
            / "true"
            / "past"
            / "false"
            / "include_objects"
            / "false",
        )
