class ProfileMixin:
    def get_profiles(
        self,
    ):
        yield from [
            {
                "ID": profile["uuid"],
                "Name": profile["public_display_name"],
                "Company": profile["company"],
                "Location": profile["home_city"],
                "@api": profile["@api"],
                "@profile": {k: v for k, v in profile.items() if k not in ["@api"]},
            }
            for profile in self.get_objects(
                "Profile",
                self.base_url / "get" / "profile",
            )
        ]
