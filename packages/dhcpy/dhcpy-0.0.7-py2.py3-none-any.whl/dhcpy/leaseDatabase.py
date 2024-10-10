class LeaseDatabase(object):
    """
    How KEA will store the leases
    """
    def __init__(self):
        self.name = ""
        self.persist = False
        self.type = ""
        self.is_set = False
    def __dict__(self):
        """
        Return a dictionary representation of the object, or an empty dictionary if the object is not set
        """
        if not self.is_set:
            return {}
        return {"name": self.name, "persist": self.persist, "type": self.type}
    def fill_from_json(self, data):
        self.name = data["name"]
        self.persist = data["persist"]
        self.type = data["type"]
        self.is_set = True
