import more_itertools


class FlightMixin:
    def get_flights(
        self,
    ):
        yield from [
            {
                "Origin": segment.get("start_airport_code"),
                "Destination": segment.get("end_airport_code"),
                "Departure": f'{segment["StartDateTime"]["date"]}T{segment["StartDateTime"]["time"]}{segment["StartDateTime"]["utc_offset"]}',
                "Arrival": f'{segment["EndDateTime"]["date"]}T{segment["EndDateTime"]["time"]}{segment["EndDateTime"]["utc_offset"]}',
                "@air": {k: v for k, v in air.items() if k not in ["@api", "Segment"]},
                "@api": air["@api"],
                "@segment": segment,
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
