from . import auth


class StravaBaseClass:
    def __init__(self):

        # IF AUTH BROKEN TRY THIS!!!
        # self.auth.update_access_token()

        a = auth.Auth()
        self.get = a.get
