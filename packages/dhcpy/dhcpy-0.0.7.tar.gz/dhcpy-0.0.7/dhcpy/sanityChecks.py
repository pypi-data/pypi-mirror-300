class SanityChecks(object):
    """The sanity checks for the service"""
    def __init__(self):
        self.extended_info_checks = ""
        self.lease_checks = ""
        self.is_set = False
    def __dict__(self):
        """Return the dictionary representation of the object, or an empty dictionary if the object is not set"""
        if not self.is_set:
            return {}
        return {"extended-info-checks": self.extended_info_checks, "lease-checks": self.lease_checks}
    def fill_from_json(self, data):
        self.extended_info_checks = data["extended-info-checks"]
        self.lease_checks = data["lease-checks"]
        self.is_set = True
