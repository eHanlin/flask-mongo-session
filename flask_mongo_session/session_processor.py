
from flask.sessions import SessionMixin, SessionInterface
from pymongo import MongoClient
import uuid


class Session(dict, SessionMixin):

    def __init__(self, session_id):
        self.__id = session_id

    def get_id(self): return self.__id

    __modified_keys = set()
 
    def __call_original_method(self, name, *args, **kw):
        return getattr(super(Session, self), name)(*args, **kw)
 
 
    def __get_iterator(self, dictionary):
        if dictionary.items:
            it = dictionary.items()
        else:
            it = dictionary.iteritems()
 
        return it
 
    def clear(self, *args, **kw):
        rv = self.__call_original_method('clear', *args, **kw)
        for key in self.keys(): self.__modified_keys.add(key)
        return rv
 
    def popitem(self, *args, **kw):
        rv = self.__call_original_method('popitem', *args, **kw)
        self.__modified_keys.add(rv[0])
        return rv
 
    def update(self, *args, **kw):
        rv = self.__call_original_method('update', *args, **kw)
        it = self.__get_iterator(kw)
 
        for key,  value in it: 
            self.__modified_keys.add(key)
 
        for arg in args:
            if isinstance(arg, dict):
                it = self.__get_iterator(arg)
                for key,  value in it: 
                    self.__modified_keys.add(key)
 
        return rv
 
 
    def __setitem__(self, *args, **kw):
        rv = self.__call_original_method('__setitem__', *args, **kw)
        self.__modified_keys.add(args[0])
        return rv
 
    def __delitem__(self, *args, **kw):
        rv = self.__call_original_method('__delitem__', *args, **kw)
        self.__modified_keys.add(args[0])
        return rv

    def modified_keys(self):
        return [key for key in self.__modified_keys]

    def reset_modified_keys(self):
        self.__modified_keys.clear()


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
        unset_query = dict()
        set_query = dict()
        doc = dict()

        for key in session.modified_keys():

            value = session.get(key)

            if value is None:
                unset_query[key] = True

            else:
                set_query[key] = value

        if len(unset_query.keys()):
            doc['$unset'] = unset_query

        if len(set_query.key()):
            doc['$set'] = set_query

        if len(unset_query.keys() + set_query.keys()): self.__db.Session.update(dict(_id = session_id), doc, upsert = True)

        session.reset_modified_keys() 

        response.set_cookie(app.session_cookie_name, session_id)


    def is_null_session(self, session):
        return False




