
from flask.sessions import SessionMixin, SessionInterface
from pymongo import MongoClient
import uuid


class Session(dict, SessionMixin):

    def __init__(self, session_id):
        self.__id = session_id

    def get_id(self): return self.__id

class MongoSessionProcessor(object):

    def __init__(self, host):
        self.__client = MongoClient(host)
        self.__db = self.__client.get_default_database()

    def open_session(self, app, request):
        session_cookie_name = app.session_cookie_name
        session_id = request.cookies.get(session_cookie_name)

        if session_id:
            data = self.__db.Session.find_one(dict(_id = session_id)) or dict()
            session = Session(session_id)
            session.update(data)
        else:
            session = Session(uuid.uuid1().hex.upper())

        return session

    def save_session(self, app, session, response):
        session_id = session.get_id()
        self.__db.Session.update(dict(_id = session_id), {'$set':session}, upsert = True)
        response.set_cookie(app.session_cookie_name, session_id)

    def is_null_session(self, session):
        return False




