import inspect
import json
from collections import UserDict, UserList

def isiterable(p_object):
    try:
        if isinstance(p_object, str):
            return False
        iter(p_object)
    except TypeError: 
        return False
    return True

class KnownTypes(UserDict):
    def __missing__(self, key):
        if key.endswith('[]'):
            if self.__getitem__(key[:-2]):
                return list

    def __contains__(self, key):
        if key.endswith('[]'):
            return self.__contains__(key[:-2])
        return key in self.data

known_types = KnownTypes({
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'any': str,
    'string': str})

class obj(object):
    def __init__(self, dict_):
        self.__dict__.update(dict_)

def dict2obj(d):
    return json.loads(json.dumps(d), object_hook=obj)
def bytes_in_gb():
    return 1024 * 1024

def to_primitive(value):
    return value if isinstance(value, (int, float, bool, str)) else str(value)

def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except (TypeError, OverflowError):
        return False
        
def safe_json(data): 
    if data is None: 
        return True 
    elif isinstance(data, (bool, int, float, str)):
        return True 
    elif isinstance(data, (tuple, list)):
        return all(safe_json(x) for x in data) 
    elif isinstance(data, dict): 
        return all(isinstance(k, str) and safe_json(v) for k, v in data.items()) 
    return False

def convert_to_safe_json(data):
    if safe_json(data):
        return data
    elif isinstance(data, tuple):
        return tuple([convert_to_safe_json(x) for x in data])
    elif isinstance(data, list):
        return [convert_to_safe_json(x) for x in data]
    elif isinstance(data, dict):
        return {str(k): convert_to_safe_json(v) for (k, v) in data.items()}
    return str(data) # blind conversion to string (__str__ will be called for objects if available)

def all_cls_fields(aClass):
    try:
        # Try getting all relevant classes in method-resolution order
        mro = list(aClass.__mro__)
    except AttributeError:
        # If a class has no _ _mro_ _, then it's a classic class
        def getmro(aClass, recurse):
            mro = [aClass]
            for base in aClass.__bases__: mro.extend(recurse(base, recurse))
            return mro
        mro = getmro(aClass, getmro)
    mro.reverse(  )
    members = {}
    for someClass in mro:
        members.update(vars(someClass))
    return members

def all_obj_fields(obj):
    # Get instance and class members' name
    members = dir(obj)
    # Get property names from the class
    properties = [i[0] for i in inspect.getmembers(obj.__class__, lambda o: isinstance(o, property))]
    attributes = {}
    for member in members:
        if member in properties or (member.startswith('__') and member.endswith('__')):
            continue
        value = getattr(obj, member)
        if value is not None and not callable(value):
            attributes.update({member: getattr(obj, member)})
    return attributes

class AccessRights:
    NotSet = 0x00
    Read = 0x01
    Write = 0x02
    Owner = 0x07
    Request = 0x8
    
class Permission:
    NOTSET = 0x00
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    WRITE_WORKFLOWS = 0x08
    MODERATE_COMMENTS = 0x10
    MODERATE_WORKFLOWS = 0x20
    ADMINISTER = 0x80

class AccessType:
    PUBLIC = 0
    SHARED = 1
    PRIVATE = 2

class Status:
    PENDING = 'PENDING'
    RECEIVED = 'RECEIVED'
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    REVOKED = 'REVOKED'
    RETRY = 'RETRY'

class LogType:
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

class VizSciFlowList(UserList):
    def first(self):
        return self[0] if len(self) > 0 else None
    def count(self):
        return len(self)

def git_access():
    import os
    import logging
    from flask import g
    from app import app

    try:
        if not app.config['USE_GIT']:
            return None
            
        import git
        if not hasattr(g, 'git'):
            g.git = git.Repo(app.config['WORKFLOW_VERSIONS_DIR'])
        return g.git
    except git.exc.NoSuchPathError:
        os.mkdir(app.config['WORKFLOW_VERSIONS_DIR'])
        return git_access()
    except git.exc.InvalidGitRepositoryError:
        git.Repo.init(app.config['WORKFLOW_VERSIONS_DIR'])
        return git_access()
    except:
        logging.error("No local repository. Versioning of workflow will not work.")