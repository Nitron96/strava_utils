from . import auth


class StravaBaseClass:
    def __init__(self):
        a = auth.Auth()
        self.get = a.get
