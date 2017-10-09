from .user_portal.auth import Google_Cloud_Manager


class Rostrus_Application:
    @staticmethod
    def initialise_application():
        Google_Cloud_Manager.initialise_gcp()

