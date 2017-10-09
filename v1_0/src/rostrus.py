import json

from .constants.constants import Ros_CONST
from django.conf import settings


class Rostrus:
    CONST = Ros_CONST()

    @staticmethod
    def get_config_file_path():
        return settings.BASE_DIR + "/v1_0/restricted/config.ini"

    @staticmethod
    def dict_fetchall(cursor):
        """Return all rows from a cursor as a dict"""

        if cursor.rowcount == 0:
            return False

        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row)) for row in cursor.fetchall()
            ]

    @staticmethod
    def process_resp_data(data):
        return json.dumps(data)

# print (os.path.abspath('../restricted/config.ini'))
# print ( ROS_ROOT_DIR )
