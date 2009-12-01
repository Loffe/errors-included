from shared.data import Database
import data
import config

class ServerDatabase(Database):
    ''' Handles database querys '''

    def __init__(self):
        Database.__init__(self, config.server.database)
        print "Connected to database at", config.server.database

    def is_valid_login(self, username, password):
        s = self._Session()
        user = s.query(data.User).filter_by(name=username).first()
        if user is None:
            return False
        return user.password == password

    def get_all_users(self):
        s = self._Session()
        users = s.query(data.User)
        return [u for u in users]
