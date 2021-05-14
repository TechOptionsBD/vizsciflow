import os
import logging

from flask import current_app, request

import psutil
import hashlib
from datetime import datetime
from collections import UserList, namedtuple

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login.mixins import UserMixin

from dsl.datatype import DataType
from .loader import Loader
from ..common import Status, LogType, AccessRights, Permission, bytes_in_gb, VizSciFlowList, convert_to_safe_json, all_obj_fields

from elasticsearch.exceptions import NotFoundError

import arrow
def convert_to_datetime(value):
    return value if isinstance(value, datetime) else arrow.get(value).naive

def session():
    from elasticsearch import Elasticsearch
    from flask import g
    
    try:
        if hasattr(g, 'es'):
            g.es = Elasticsearch()
        return g.es
    except:
        return Elasticsearch()

class ElasticManager():
    
    @staticmethod
    def update(obj):
        payload = convert_to_safe_json(all_obj_fields(obj))
        return ElasticManager.update_fields(**payload)

    @staticmethod
    def update_fields(**kwargs):
        index = kwargs.pop('label', None)
        if index is None:
            raise ValueError("No index specified for update.")
        
        id = kwargs.get('id', None)
        if id is None:
            raise ValueError("No document id specified for update.")

        session().update(index=index, id=id, body = {"doc": kwargs})
    
    @staticmethod
    def push(obj):
        payload = all_obj_fields(obj)
        index = payload.pop('label', obj.label)
        id = payload.get('id', None)
        payload = convert_to_safe_json(payload)
        if id is not None:
            item = ElasticManager.and_query(obj.__class__, id=id)
            #check if item with id exist. If yes, update. Otherwise insert
            if item:
                session().update(index=index, id=id, body = {"doc": payload})
                return obj
        try:
            result = session().count(index = index)
            id = int(result['count']) + 1
        except:
            id = 1
        
        payload['id'] = id
        session().index(index=index, id = id, body=payload, refresh= True)
        obj.id = id
        return obj

    @staticmethod
    def and_query_with_entities(*args, **kwargs):
        index = kwargs.pop('label', None)
        if not index:
            raise ValueError("No index is specified for elastic search.")

        if not session().indices.exists(index=index):
            return VizSciFlowList([]) # if no index for this label created, return empty list

        fields = list(args) if args else ["*"] # no args given means all fields
        search = None
        id = kwargs.pop('id', None)
        
        if id: # return items with id directly
            search = session().search(index = index, body = {'query': {'match': {'id': id}}, 'fields': fields})
        if search is None or not search['hits']['hits']:
            try:
                query_list = [{'match' : {str(k): v} } for k,v in convert_to_safe_json(kwargs).items()]
                search = session().search(index = index, body = {'fields': fields, "sort" : [{ "id" : "asc" }], "query": {"bool": {"should": query_list}}})
            except NotFoundError:
                logging.error("Index {0} cannot be retrieved from elasticsearch.".format(index))
                return VizSciFlowList([])

        result = search['hits']['hits']['fields']
        if args:
            keys = list(result.keys())  # copy the keys because we will be modifying the dictionary
            for k in keys:
                if k not in args:
                    keys.pop(k)

        return VizSciFlowList([dict(zip(result,t)) for t in zip(*result.values())])

    @staticmethod
    def and_query(cls_, **kwargs):
        index = kwargs.pop('label', cls_.label)
        if not index:
            raise ValueError("No index is specified for elastic search.")

        if not session().indices.exists(index=index):
            return VizSciFlowList([]) # if no index for this label created, return empty list

        search = None
        id = kwargs.pop('id', None)
        # return items with id directly
        if id:
            search = session().search(index = index, body = {'query': {'match': {'id': id}}})
        if search is None or not search['hits']['hits']:
            try:
                query_list = [{'match' : {str(k): v} } for k,v in convert_to_safe_json(kwargs).items()]
                search = session().search(index = index, body = {"sort" : [{ "id" : "asc" }], "query": {"bool": {"should": query_list}}})
            except NotFoundError:
                return VizSciFlowList([])

        return VizSciFlowList([cls_(**hit['_source']) for hit in search['hits']['hits']])

class ElasticNode(object):
    id = None
    created_on = None
    modified_on = None
    properties = {}
    
    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)
        self.created_on = convert_to_datetime(kwargs.pop('created_on', datetime.utcnow()))
        self.modified_on = convert_to_datetime(kwargs.pop('modified_on', datetime.utcnow()))
        
        # other properties
        for k, v in kwargs.items():
            if k.lower() == 'properties' and isinstance(v, dict):
                self.properties = v # if a dictionary named properties comes, replace self.properties with it.
            else:
                self.properties.update({k: v})
                    
    @staticmethod
    def get_with_or(cls_, **kwargs):
        # return items with id directly
        id = kwargs.pop('id', None)
        #query with other attributes
        query = ""
        for k in kwargs:
            if query:
                query += " OR"
            if isinstance(kwargs[k], str):
                query += " _.{0}='{1}'".format(k, kwargs[k])
            else:
                query += " _.{0}={1}".format(k, kwargs[k])

        if id:
            if query:
                query += " OR "
            query += "ID(id)={0}".format(id)
        return ElasticManager.get(query)

    def json(self):
        
        j = {
            'id': self.id,
            'created_on': str(self.created_on),
            'modified_on': str(self.modified_on),
        }
        for k, v in self.properties.items():
            j.update({k: v})
        return j

class ElasticDataSource(ElasticNode):
    label = 'datasources'
    name = None
    type = None
    url = None
    root = None
    public = True
    prefix = None
    active = True
    temp = False

    #user name and password if authentication is needed for the data source (e.g. hdfs, ftp)
    user = None
    password = None
    
    def __init__(self, **kwargs):
        self.label = kwargs.pop('label', ElasticDataSource.label)
        self.name = kwargs.pop('name', None)
        self.type = kwargs.pop('type', None)
        self.url = kwargs.pop('url', None)
        self.public = kwargs.pop('public', True)
        self.user = kwargs.pop('user', None)
        self.password = kwargs.pop('password', None)
        self.prefix = kwargs.pop('prefix', None)
        self.active = kwargs.pop('active', True)
        self.temp = kwargs.pop('temp', False)
        self.root = kwargs.pop('root', None)

        super(ElasticDataSource, self).__init__(**kwargs)

    @staticmethod
    def insert_datasources():
        try:
            datasources = Loader.get_datasources()
            datasourceitems = []
            for datasrc in datasources:
                datasourceitem = ElasticDataSource(**datasrc)
                ElasticManager.push(datasrc)
                datasourceitems.append(datasourceitem)
            return datasourceitems

        except Exception as e:
            logging.error("Error creating data sources: " + str(e))
            raise

    def __repr__(self):
        return '<ElasticDataSource %r>' % self.name

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticDataSource, **kwargs)

class ElasticRole(ElasticNode):
    label = 'roles'
    name = None
    default = None
    permissions = None

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.default = kwargs.pop('default', False)
        self.permissions = kwargs.pop('permissions', 0x00)
        super(ElasticRole, self).__init__(**kwargs)

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticRole, **kwargs)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES |
                     Permission.WRITE_WORKFLOWS, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.WRITE_WORKFLOWS |
                          Permission.MODERATE_COMMENTS |
                          Permission.MODERATE_WORKFLOWS, False),
            'Administrator': (0xff, False)
        }
        try:
            for r in roles:
                role = None
                if session().indices.exists(index='roles'):
                    role = ElasticRole.get(name=r)
                if role is None or role == []:
                    role = ElasticRole(name=r, permissions= roles[r][0], default = roles[r][1])
                ElasticManager.push(role)         
        except:
            logging.error("Error creating default roles")
            raise

    def __repr__(self):
        return '<Role %r>' % self.name

class ElasticUser(ElasticNode, UserMixin): 
    label = 'users'

    email = None
    username = None
    password_hash = None
    confirmed = None
    name = None
    location = None
    about_me = None
    member_since = None
    last_seen = None
    avatar_hash = None
    oid = None
    role_id = None
    
    @property
    def workflowaccesses(self):
        return ElasticWorkflowAccess.get(user_id = self.id)

    def __init__(self, **kwargs):
        self.email = kwargs.pop('email', None)
        self.username = kwargs.pop('username', None)
        self.confirmed = kwargs.pop('confirmed', True)
        self.location = kwargs.pop('location', None)
        self.about_me = kwargs.pop('about_me', None)
        self.member_since = convert_to_datetime(kwargs.pop('member_since', datetime.now()))
        self.last_seen = convert_to_datetime(kwargs.pop('last_seen', datetime.now()))
        self.avatar_hash = kwargs.pop('avatar_hash', None)
        self.oid = kwargs.pop('oid', 0)
        self.role_id = kwargs.pop('role_id', None)
        self.name = kwargs.pop('name', None)
        self.password_hash = kwargs.pop('password_hash', None)
        if not self.password_hash:
            self.password = kwargs.pop('password', None)

        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

        super(ElasticUser, self).__init__(**kwargs)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        
        hash = None
        if self.email:
            hash = self.avatar_hash or hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @property
    def role(self):
        roles = ElasticRole.get(id = self.role_id)
        return roles[0] if roles else None

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password) if password else None

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_and_update_password(self, oldpassword, password):
        if not check_password_hash(self.password_hash, oldpassword):
            return False
        self.password = password
        ElasticManager.update_fields(label=self.__class__.label, id = self.id, password = self.password)
        return True

    @staticmethod
    def first(**kwargs):
        return ElasticUser.get(**kwargs).first()

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticUser, **kwargs)

    @staticmethod
    def load(es_item):

        return ElasticUser(**es_item)

    @staticmethod
    def Create(**kwargs):
        user = ElasticUser(**kwargs)
        if user.role_id is None:
            if user.email == current_app.config['PHENOPROC_ADMIN']:
                roles = ElasticRole.get(permissions=0xff)
                user.role_id = roles[0].id
            else:
                roles = ElasticRole.get(default=True)
                user.role_id = roles[0].id

        # if user.email is not None and user.avatar_hash is None:
        #     user.avatar_hash = hashlib.md5(user.email.encode('utf-8')).hexdigest()

        ElasticManager.push(user)
        return user

    @property
    def Runs(self):
        return ElasticRunnable.get(user_id = self.id)
    
    @property
    def Workflows(self):
        return ElasticWorkflow.get(user_id = self.id)
    
    @property
    def modules(self):
        return ElasticModule.get(user_id = self.id)

    def ping(self):
        self.last_seen = datetime.utcnow()
        ElasticManager.update_fields(label=self.__class__.label, id = self.id, last_seen = self.last_seen)
    
    def can(self, permissions):
        return self.role is not None and \
            self.role.permissions is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
    
    def add_module(self, module_id, access):
        module = ElasticModule.get(id=module_id).first()
        self.modules.add(module)
    
    def add_modules_access(self, function, package, rights):
        modules = ElasticModule.get(name=function, package=package)
        for module in modules:
            self.modules.add(module)

    @staticmethod
    def get_other_users_with_entities(id, *args):
        return ElasticManager.and_query_with_entities(id = id, label = ElasticUser.label, *args)

class ElasticModuleAccess(ElasticNode):
    user_id = None
    module_id = None
    rights = None

    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.module_id = kwargs.pop('module_id', None)
        self.rights = kwargs.pop('rights', None)
    
    @staticmethod
    def add(module_id, user_id, rights):
        access = ElasticModuleAccess(module_id = module_id, user_id = user_id, rights = rights)
        ElasticManager.push(access)
        return access

    @property
    def user(self):
        return ElasticUser.first(id = self.user_id)

    @property
    def module(self):
        return ElasticModule.first(id = self.module_id)

class ElasticModuleParam(ElasticNode):
    label = 'moduleparams'
    module_id = None
    name = None
    type = None
    default = None
    desc = None

    def __init__(self, **kwargs):
        self.module_id = kwargs.pop('module_id', None)
        self.name = kwargs.pop('name', None)
        self.type = kwargs.pop('type', None)
        self.default = kwargs.pop('default', None)
        self.desc = kwargs.pop('desc', None)
        
        super(ElasticModuleParam, self).__init__(**kwargs)

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticModuleParam, **kwargs)

    @property
    def module(self):
        return ElasticModule.get(id = self.module_id)

    def json(self):
        return all_obj_fields(self)

class ElasticModuleReturn(ElasticModuleParam):
    label = 'modulereturns'

    def __init__(self, **kwargs):
        super(ElasticModuleReturn, self).__init__(**kwargs)

class ElasticWorkflowReturn(ElasticModuleParam):
    label = 'workflowreturns'

    def __init__(self, **kwargs):
        super(ElasticWorkflowReturn, self).__init__(**kwargs)

class ElasticWorkflowParam(ElasticModuleParam):
    label = 'workflowparams'

    def __init__(self, **kwargs):
        super(ElasticWorkflowParam, self).__init__(**kwargs)

class ElasticModule(ElasticNode):
    label = 'modules'
    org = None
    name = None
    package = None
    public = False
    active = True
    group = None
    example = None
    desc = None
    href = None
    internal = None
    module = None
    user_id = None

    def __init__(self, **kwargs):
        self.org = kwargs.pop('org', "")
        self.name = kwargs.pop('name', None)
        self.internal = kwargs.pop('internal', None)
        self.package = kwargs.pop('package', None)
        self.public = kwargs.pop('public', False)
        self.active = kwargs.pop('active', True)
        self.group = kwargs.pop('group', "")
        self.example =  kwargs.pop('example', "")
        self.desc =  kwargs.pop('desc', "")
        self.href =  kwargs.pop('href', "")
        self.module = kwargs.pop('module', None)
        self.user_id = kwargs.pop('user_id', None)

        super(ElasticModule, self).__init__(**kwargs)
        
    @staticmethod
    def add_user_access(id, users, access):
        return [ElasticModuleAccess.add(id, user, access) for user in users]

    def add_owner(self, user_id):
        self.user_id = user_id
        ElasticManager.update_fields(label=self.__class__.label, id = self.id, user_id = self.user_id)

    @staticmethod
    def first(**kwargs):
        return ElasticModule.get(**kwargs).first()

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticModule, **kwargs)
    
    @staticmethod
    def add(owner_id, value, access, users):
        module = ElasticModule(**value)
        module.user_id = owner_id

        module = ElasticManager.push(module)

        if users:
            if owner_id in users:
                users.remove(owner_id)

            if users:    
                ElasticModule.add_user_access(module.id, users, access)

        return module 

    @property
    def params(self):
        return ElasticModuleParam.get(module_id = self.id)

    @property
    def returns(self):
        return ElasticModuleReturn.get(module_id = self.id)

    def json(self):
        j = all_obj_fields(self)
        params = [p.json() for p in self.params]
        returns = [r.json() for r in self.returns]
        j.update({'params': params})
        j.update({'returns': returns})
        return j
        # return {
        #     'id': self.id,
        #     #'user': self.user.username,
        #     'org': self.org if self.org else "",
        #     'name': self.name,
        #     'internal': self.internal if self.internal else "",
        #     'package': self.package  if self.package else "",
        #     'public': self.public,
        #     'module': self.module,
        #     'group': self.group if self.group else "",
        #     'desc': self.desc if self.desc else "",
        #     'href': self.href if self.href else "",
        #     'example': self.example if self.example else "",
        #     'is_owner': False,
        #     'params': params,
        #     'returns': returns
        # }

    def add_param(self, **p):
        return ElasticManager.push(ElasticModuleParam(module_id = self.id, **p))

    def add_return(self, **p):
        return ElasticManager.push(ElasticModuleReturn(module_id = self.id, **p))

    @staticmethod
    def insert_modules(url):
        admin = ElasticUser.first(username = "admin")
        funclist = Loader.load_funcs_recursive_flat(url)

        modules = []
        for f in funclist:
            user_id = f.pop("user_id", None)
            if not user_id and admin:
                user_id = admin.id

            f["public"] = True
            params = f.pop('params', None)
            returns = f.pop('returns', None)
            module = ElasticModule.add(user_id, f, None, None)

            if params:
                for p in params:
                    module.add_param(**p)
            
            if returns:
                for p in returns:
                    module.add_return(**p)

            modules.append(module)
            
        return modules

    
    def func_to_internal_name(self, funcname):
        for f in self.funcs:
            if f.get("name") and self.iequal(f["name"], funcname):
                return f["internal"]

    @staticmethod
    def get_module_by_name_package_for_user_access(user_id, name, package = None):
        service = ElasticModule.get(name=name, package=package).first()
        if service:
            jsonval = service.json()
            if service.public:
                jsonval["access"] = "public"
            # else:
            #     for access in service.accesses:
            #         if access.user_id == user_id:
            #             value["access"] = "shared" if service.user_id != user_id else "private"
            #             break
            return jsonval

class ElasticWorkflowAccess(ElasticNode):
    label = 'workflowaccesses'

    user_id = None
    workflow_id = None
    rights = None

    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.workflow_id = kwargs.pop('workflow_id', None)
        self.rights = kwargs.pop('rights', None)

        super(ElasticWorkflowAccess, self).__init__(**kwargs)
    
    @staticmethod
    def add(workflow_id, user_id, rights):
        access = ElasticWorkflowAccess(workflow_id = workflow_id, user_id = user_id, rights = rights)
        return ElasticManager.push(access)

    @property
    def user(self):
        return ElasticUser.first(id = self.user_id)

    @property
    def workflow(self):
        return ElasticWorkflow.first(id = self.workflow_id)
    
    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticWorkflowAccess, **kwargs)

class ElasticWorkflow(ElasticNode):
    label = 'workflows'
    name = None
    desc = None
    script = None
    public = True
    temp = False
    derived = 0
    user_id = None
    args = None
       
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.desc = kwargs.pop('desc', "")
        self.script = kwargs.pop('script', None)
        self.public = kwargs.pop('public', True)
        self.temp = kwargs.pop('temp', False)
        self.derived = kwargs.pop('derived', 0)
        self.user_id = kwargs.pop('user_id', None)
        self.args = kwargs.pop('args', None)

        super(ElasticWorkflow, self).__init__(**kwargs)

        # if args:
        #     for arg in args:
        #         param = DataPropertyItem(arg)
        #         graph().push(param)
        #         self.params.add(param)
    
    # def add_module(self, **kwargs):
    #     module = ElasticModule.get(**kwargs).first()
    #     if module:
    #         self.modules.add(module)
    #         .push(self)
    #         return module

    def update_script(self, script):
        if self.script == script:
            return True                       
        try:
            self.script = script
            self.modified_on = datetime.utcnow()
            ElasticManager.update_fields(label=self.__class__.label, id = self.id, script=self.script, modified_on=self.modified_on)
            try:
                #self.git_write(script)
                pass
            except Exception as e:
                logging.error("Git error while updating workflow: " + e.message)
        except:
            raise

    def add_param(self, **p):
        return ElasticManager.push(ElasticWorkflowParam(workflow_id = self.id, **p))

    def add_return(self, **p):
        return ElasticManager.push(ElasticWorkflowReturn(workflow_id = self.id, **p))

    @staticmethod
    def Create(**kwargs):
        users =  kwargs.pop('users', None)
        params = kwargs.pop('params', None)
        returns = kwargs.pop('returns', None)
        access = kwargs.pop('access', AccessRights.Read)

        workflow = ElasticManager.push(ElasticWorkflow(**kwargs))
        if users:
            users = users.split(",")
            for username in users:
                user = ElasticUser.first(username=username)
                ElasticWorkflowAccess(workflow_id = workflow.id, user_id = user.id, rights = access)

        if params:
            for p in params:
                workflow.add_param(**p)
            
        if returns:
            for p in returns:
                workflow.add_return(**p)

        return workflow
            
    @property
    def Runs(self):
        return list(self.runs)
    
    @property
    def user(self):
        if self.user_id:
            return ElasticUser.first(id = self.user_id)

    @property
    def useraccesses(self):
        return ElasticWorkflowAccess.get(workflow_id = id)

    @property
    def accesses(self):
        rights = []
        for user in self.useraccesses:
            v = {'user_id': user.user_id, 'rights': user.rights}
            rights.append(namedtuple("WorkflowAccess", v.keys())(*v.values()))

        return rights

    def to_json_info(self):
        return {
            'id': self.id,
            'user': self.user.username if self.user else "",
            'name': self.name
        }

    @property
    def params(self):
        return ElasticWorkflowParam.get(module_id = self.id)

    @property
    def returns(self):
        return ElasticWorkflowReturn.get(module_id = self.id)

    def to_json(self):
        params = [param.json() for param in self.params]
        user = self.user
        return {
            'id': self.id,
            'user': user.username if user else '',#self.user.username,
            'name': self.name,
            'desc': self.desc,
            'script': self.script,
            'args': params
        }

    @staticmethod
    def get_workflows_as_list(access, user_id, *args):
        user = ElasticUser.first(id=user_id)
        workflows = [ownedwf for ownedwf in user.Workflows]
        workflows.extend([accesswf for accesswf in user.workflowaccesses])

        public_workflows = ElasticWorkflow.get(public=True)
        if not workflows:
            return public_workflows
        if not public_workflows:
            return workflows

        unique_workflows = []
        for pwf in public_workflows:
            if not any(pwf.id == wf.id for wf in workflows):
                unique_workflows.append(pwf)

        workflows.extend(unique_workflows)
        return workflows
    
    @staticmethod
    def first(**kwargs):
        return ElasticWorkflow.get(**kwargs).first()

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticWorkflow, **kwargs)

    @staticmethod
    def insert_workflows(path):
        admin = ElasticUser.first(username='admin')
        samples = Loader.load_samples_recursive(path)
        for sample in samples:
            if isinstance(sample["script"], list):
                sample["script"] = "\n".join(sample["script"])
            if admin and "user_id" not in sample:
                sample["user_id"] = admin.id

        return [ElasticWorkflow.Create(**s) for s in samples]

class ElasticData(ElasticNode):
    label = 'data'
    name = ""
    value = ""

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', "")
        self.value = ElasticData.to_primitive(kwargs.pop('value', ""))

        super(ElasticData, self).__init__(**kwargs)   
   
    @staticmethod
    def create(**kwargs):
        return ElasticManager.push(ElasticData(*kwargs))
    
    def json(self):
        return all_obj_fields(self)

    @staticmethod
    def to_primitive(value):
        return value if isinstance(value, (int, float, bool, str)) else str(value)

class ElasticValue(ElasticData):
    label = 'datavalues'
    datatype = None
    type = None
    
    # inputs = RelatedTo("ModuleInvocationItem", "INPUT")
    # outputs = RelatedFrom("ModuleInvocationItem", "OUTPUT")
    
    # #allocations = RelatedTo("DataAllocationItem", "ALLOCATION")
    # users = RelatedFrom(UserItem, 'ACCESS')
    
    def __init__(self, **kwargs):
        self.type = kwargs.pop('type', DataType.Value) # if type else str(DataType.Value) #str(type(self.value))
        super(ElasticValue, self).__init__(**kwargs)
        
        self.datatype =  str(type(self.value)) #str(self.__class__.__name__) #val_type#
    
    def set_name(self, value):
        self.name = value
    
    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticValue, **kwargs)

    @staticmethod
    def Create(**kwargs):
        item = ElasticValue(**kwargs)
        item.name = "value"
        return ElasticManager.push(item)
    
    def get_allocation_for_user(self, user_id):
        return next((a for a in self.allocations if a.user_id == user_id), None)

    def allocate_for_user(self, user_id, rights):
        access = ElasticDataAccess.get(id = self.id, user_id = user_id).first()
        if access and rights > access.rights:
            ElasticManager.update_fields(label=self.__class__.label, id = self.id, rights = rights)
            return self
        
        ElasticDataAccess.add(self.id, user_id, rights)
        return self
                    
    def json(self):
        j = ElasticData.json(self)
        j.update({
            'event': 'VAL-SAVE',
            'datatype': str(self.datatype),
            'type': self.type,
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb(),
            'cpu': (psutil.cpu_percent()),
            'name': self.name
        })
        return j
            
    @staticmethod
    def get_by_type_value(type, value):
        return ElasticValue.get(type=type, value=value).first()
        
    @staticmethod
    def check_access_rights(user_id, path, checkRights):
        matcher = NodeMatcher(graph())
        return matcher.match(id=user_id)
    
    @staticmethod
    def get_access_rights(user_id, path):
        defaultRights = AccessRights.NotSet
        
        if path == os.sep:
            defaultRights = AccessRights.Read # we are giving read access to our root folder to all logged in user

        matcher = NodeMatcher(graph())

class ElasticDataAccess(ElasticNode):
    label = 'dataaccesses'

    user_id = None
    data_id = None
    rights = None

    def __init__(self, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        self.data_id = kwargs.pop('data_id', None)
        self.rights = kwargs.pop('rights', None)

        super(ElasticDataAccess, self).__init__(**kwargs)
    
    @staticmethod
    def add(data_id, user_id, rights):
        return ElasticManager.push(ElasticDataAccess(data_id = data_id, user_id = user_id, rights = rights))

    @property
    def user(self):
        return ElasticUser.first(id = self.user_id)

    @property
    def data(self):
        return ElasticValue.first(id = self.data_id)
    
    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticDataAccess, **kwargs)
    
    @staticmethod
    def first(**kwargs):
        return ElasticNode.get(**kwargs).first()

class ElasticDataPropertyItem(ElasticValue):
    label = 'dataproperties'
    desc = None

    #data = RelatedFrom(ValueItem, "ALLOCATION")
    
    def __init__(self, **kwargs):
        self.desc = kwargs.pop('desc', None)

        super(ElasticDataPropertyItem, self).__init__(**kwargs)
    
    def json(self):
        # j = NodeItem.json(self)
        # j.update({
        #     'event': 'PROP-SAVE',
        #     'datatype': str(self.datatype)
        # })
        j = {
            "name": self.name,
            "value": self.value if self.value else "",
            "type": self.type if self.type else "",
            "desc": self.desc if self.desc else ""
        }

        return j

class ElasticRunnable(ElasticNode): #number1
    label = 'runnables'

    celery_id = None
    name = None
    
    out = None
    error = None
    view = None
    
    script = None
    status = None
    duration = None
    provenance = False
    args = ""
    user_id = None
    workflow_id = None

    # modules = RelatedTo("ModuleInvocationItem", "MODULEINVOCATION", "id(b)")
    # users = RelatedFrom(UserItem, "USERRUN")
    # workflows = RelatedFrom(WorkflowItem, "WORKFLOWRUN")
    
    cpu_init = psutil.cpu_percent()
    memory_init = (psutil.virtual_memory()[2])/bytes_in_gb()
    cpu_run = 0.0
    memory_run = 0.0
    
    started_on = datetime.min

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.celery_id = kwargs.pop('celery_id', None)
        self.out = kwargs.pop('out', "")
        self.error = kwargs.pop('error', "")
        self.view = kwargs.pop('view', None)
        self.script = kwargs.pop('script', None)
        self.status = kwargs.pop('status', Status.RECEIVED)
        self.duration = kwargs.pop('duration', 0)
        self.provenance = kwargs.pop('provenance', False)
        self.args = kwargs.pop('args', "")
        self.user_id = kwargs.pop('user_id', None)
        self.workflow_id = kwargs.pop('workflow_id', None)
        self.cpu_init = kwargs.pop('cpu_init', 0.0)
        self.memory_init = kwargs.pop('memory_init', 0.0)
        self.cpu_run = kwargs.pop('cpu_run', 0.0)
        self.memory_run = kwargs.pop('memory_run', 0.0)
        self.started_on = convert_to_datetime(kwargs.pop('started_on', datetime.utcnow()))

        super(ElasticRunnable, self).__init__(**kwargs)
   
    # @property
    # def duration(self):
    #     if self.status == Status.STARTED:
    #         self.duration = utc_now() - self.started_on
    #         #graph().push(self)
    #     return self.duration    
            
    def update(self):
        ElasticManager.update(self)

    @property
    def modules(self):
        return ElasticModuleInvocation.get(runnable_id = self.id)

    @staticmethod
    def load(run_id = None, workflow_id = None):
        if run_id:
            return ElasticRunnable.first(id = run_id)
        elif workflow_id:
            return ElasticRunnable.get(workflow_id = workflow_id)
        else: # this will be very resource-intensive. never call it.
            return ElasticRunnable.get()
    
#     @staticmethod
#     def load_for_users(user_id):
#         user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
#         if not user:
#             return []
#         return [r for r in user.runs if not r.provenance]
    
    @staticmethod
    def load_for_users(user_id):        
        return ElasticRunnable.get(user_id = user_id)
        
    def invoke_module(self, name, package):
        if not name:
            raise ValueError("No function name for module")
        args = {'name': name}
        if package:
            args['package'] = package
        module = ElasticModule.first(**args)
        if not module:
            raise ValueError("No module {0} found.".format(name))

        invocation = ElasticManager.push(ElasticModuleInvocation(module_id=module.id))
        ElasticManager.push(ElasticInvokeRunnable(invoke_id = invocation.id, runnable_id = self.id))
        return invocation

    @staticmethod
    def create(user, workflow, script, provenance, args):
        item = ElasticRunnable(name=workflow.name, script=script, provenance=provenance, args=args, user_id = user.id, workflow_id = workflow.id)
        return ElasticManager.push(item)

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticRunnable, **kwargs)

    def update_cpu_memory(self):
        self.cpu_run = psutil.cpu_percent()
        self.memory_run = (psutil.virtual_memory()[2])/bytes_in_gb()
        
    def set_status(self, value, update = True):
        self.status = value
        
        if value == Status.STARTED:
            self.started_on = datetime.utcnow()
            self.update_cpu_memory()
    
        if value == Status.SUCCESS or value == Status.FAILURE or value == Status.REVOKED:
            self.duration = (datetime.utcnow() - self.started_on).total_seconds()
            self.update_cpu_memory()
        
        if update:
            self.update()
        
    @property        
    def completed(self):
        return self.status == Status.SUCCESS or self.status == Status.FAILURE or self.status == Status.REVOKED
    
    def json(self):
        j = ElasticNode.json(self)
        j.update({
            'user_id': self.user_id,
            'workflow_id': self.workflow_id,
            'celery_id': self.celery_id if self.celery_id is not None else 0,
            'memory': self.memory_run,
            'cpu': self.cpu_run,
            'out': self.out,
            'error': self.error,
            'view': self.view,
#            'script': self.script,
            'status': self.status,
            'duration': self.duration, #"{0:.3f}".format(neotime_duration_to_s(self.duration)),
            'args': str(self.args),
            'name': self.name
            })
        return j
           
    def to_json_tooltip(self):
        j = ElasticNode.json(self)
        j.update({
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'error': self.error,
            'duration': self.duration, #"{0:.3f}".format(neotime_duration_to_s(self.duration)),
        })
        return j
        
    def to_json_log(self):
        log = []
        
        for module in self.modules:
            log.append(module.to_json_log())

        j = ElasticNode.json(self)
        j.update({
            'id': self.id,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'err': self.error,
            'duration': self.duration, #"{0:.3f}".format(neotime_duration_to_s(self.duration)),
            'log': log
        })
        return j
        
    def to_json_info(self):
        j = ElasticNode.json(self)
        j.update({
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'status': self.status
        })
        return j


class ElasticInvokeInput(ElasticNode):
    label = 'invokeinputs'

    invoke_id = None
    data_id = None

    def __init__(self, **kwargs):
        self.invoke_id = kwargs.pop('invoke_id', None)
        self.data_id = kwargs.pop('data_id', None)
        super(ElasticInvokeInput, self).__init__(**kwargs)
    
    @staticmethod
    def add(invoke_id, data_id):
        access = ElasticInvokeInput(workflow_id = invoke_id, data_id = data_id)
        return ElasticManager.push(access)
    
    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticInvokeInput, **kwargs)


class ElasticInvokeOutput(ElasticInvokeInput):
    label = 'invokeoutputs'

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticInvokeOutput, **kwargs)

class ElasticInvokeRunnable(ElasticNode):
    label = 'invokerunnables'

    invoke_id = None
    runnable_id = None

    def __init__(self, **kwargs):
        self.invoke_id = kwargs.pop('invoke_id', None)
        self.runnable_id = kwargs.pop('runnable_id', None)
        super(ElasticInvokeRunnable, self).__init__(**kwargs)
    
    @staticmethod
    def add(invoke_id, runnable_id):
        access = ElasticInvokeInput(workflow_id = invoke_id, runnable_id = runnable_id)
        return ElasticManager.push(access)
    
    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticInvokeRunnable, **kwargs)


class ElasticModuleInvocation(ElasticNode):   
    label = 'moduleinvocations'

    module_id = None
    status = Status.RECEIVED
    
    cpu_init = psutil.cpu_percent()
    memory_init = (psutil.virtual_memory()[2])/bytes_in_gb()
    
    cpu_run = 0
    memory_run = 0
    
    started_on = datetime.min
    duration = 0
    
    def __init__(self, **kwargs):
        self.module_id = kwargs.pop("module_id", None)
        self.status = kwargs.pop("status", Status.RECEIVED)
        self.cpu_init = kwargs.pop("cpu_init", None)
        self.memory_init = kwargs.pop("memory_init", None)
        self.cpu_run = kwargs.pop("cpu_run", None)
        self.memory_run = kwargs.pop("memory_run", None)
        self.started_on = convert_to_datetime(kwargs.pop("started_on", datetime.now()))
        self.duration = kwargs.pop("duration", datetime.now())

        super(ElasticModuleInvocation, self).__init__(**kwargs)
    
    def json(self):
        j = ElasticNode.json(self)
        j.update({
            'name':self.name,
            'memory': str(self.memory_run),
            'cpu': str(self.cpu_run),
            'status': self.status           
        })
        
        return j 

    @staticmethod
    def get(**kwargs):
        return ElasticManager.and_query(ElasticModuleInvocation, **kwargs)

    @property
    def name(self):
        return ElasticModule.first(id = self.module_id).first()
        
    @property
    def run_id(self):
        runs = list(self.runs)
        return runs.id if runs else 0
           
    # @property
    # def duration(self):
    #     if self.status == Status.STARTED:
    #         self.duration = neotime.DateTime.utc_now() - self.started_on
    #         #graph().push(self)
            
    #     return self.duration  
    
    # @duration.setter
    # def duration(self, value):
    #     self.duration = value
    
    @staticmethod
    def load(module_id, name = None, package = None):
        if not module_id and name:
            if package:
                module = ElasticModule.first(name = name, package = package)
                if module:
                    module_id = module.id
            else:
                pkg_func = name.split(".")
                if len(pkg_func) > 1:
                    name = pkg_func[-1]
                    package = ".".join(pkg_func[0:-1])
                else:
                    module = ElasticModule.first(name = name)
                    if module:
                        module_id = module.id

        if module_id:
            return ElasticModuleInvocation.first(module_id = module_id)
        
    def start(self):
        self.status = Status.STARTED
        self.started_on = datetime.utcnow()
        
        self.duration = 0
        self.memory_run = (psutil.virtual_memory()[2])/bytes_in_gb()
        self.cpu_run = psutil.cpu_percent()
                    
        self.add_log(Status.STARTED, LogType.INFO)
        ElasticManager.update(self)
    
    def succeeded(self):
        self.status = Status.SUCCESS
        self.add_log(Status.SUCCESS, LogType.INFO)
        self.modified_on = datetime.utcnow()
        self.duration = (datetime.utcnow() - self.started_on).total_seconds()
        
        ElasticManager.update(self)
    
    def failed(self, log = "Task Failed."):
        self.status = Status.FAILURE
        self.add_log(log, LogType.INFO)
        self.modified_on = datetime.utcnow()
        self.duration = (datetime.utcnow() - self.started_on).total_seconds()

        ElasticManager.update(self)
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        return ElasticManager.push(ElasticInvocationLog(text = log, type=logtype, module_id = self.id))
    
    # def add_arg(self, datatype, value):
    #     if isinstance(value, ElasticValue):
    #         self.inputs.add(value)
    #     else:
    #         for data in self.inputs:
    #             if data.datatype == datatype and data.value == value:
    #                 value = data
    #                 break
    #         if not value:    
    #             value = ElasticValue.get_by_type_value(datatype, value)
    #             if not value:
    #                 data = ElasticValue(value, datatype)
    #                 graph().push(data)
    #             self.inputs.add(data)

    #     graph().push(self)
        
    #     return value
    
    @property
    def inputs(self):
        return ElasticInvokeInput.get(invoke_id = self.id)

    @property
    def outputs(self):
        return ElasticInvokeOutput.get(invoke_id = self.id)
    
    @property
    def runs(self):
        invokerunnables = ElasticInvokeRunnable.get(invoke_id = self.id)
        return UserList([ElasticRunnable.get(id = ir.runnable_id).first() for ir in invokerunnables])

    def add_input(self, user_id, datatype, value, rights, **kwargs):
        for data in self.inputs:
            if data.datatype == datatype and data.value == value:
                return data.allocate_for_user(user_id, rights)
                      
        data = ElasticValue.get_by_type_value(datatype, value)
        if not data:
            kwargs.update({'value': value, 'type': datatype})
            data = ElasticManager.push(ElasticValue(**kwargs)) #  data = ValueItem(str(value), datatype)
        
        ElasticManager.push(ElasticInvokeInput(invoke_id = self.id, data_id = data.id))
        data.allocate_for_user(user_id, rights)

        return data

    def add_outputs(self, dataAndType):
        runitem = self.runs[0]
        
        result = ()        
        for d in dataAndType:
            data = None
            if not isinstance(d[1], ElasticValue):
                data = ElasticValue.get_by_type_value(d[0], d[1])
                if not data:
                    data = ElasticValue(name=d[2] if len(d) > 2 else '', value=str(d[1]), type=d[0], task_id = self.id, job_id = runitem.id, workflow_id = runitem.workflow_id)
                    data = ElasticManager.push(data)
                    data.allocate_for_user(runitem.user_id, AccessRights.Owner)                    
                else:
                    data.allocate_for_user(runitem.user_id, AccessRights.Write)
                
            result += (d[1],)
               
        return result
    
    def to_json_log(self):
        
        data = [{ "datatype": data.type, "data": data.value} for data in self.outputs]
            
        return { 
            'name': self.name if self.name else "", 
            'status': self.status,
            'data': data
        }
        
class ElasticInvocationLog(ElasticNode):
    label = 'logs'
    type = None
    text = None
    module_id = None
        
    def __init__(self, **kwargs):
        self.module_id = kwargs.pop("module_id", None)
        self.type = kwargs.pop("type", LogType.ERROR)
        self.text = kwargs.pop("text", "")

        super(ElasticInvocationLog, self).__init__(**kwargs)
       
    def json(self):
        j = ElasticNode.json(self)
        j.update({
            'type': self.type,
            'log': self.text
            })
        
        return j
    
    @staticmethod
    def load(module_id):
        return ElasticInvocationLog.first(module_id = module_id)
    
    def updateTime(self):
        self.modified_on = datetime.utcnow()
        ElasticManager.update_fields(label=self.__class__.label, id = self.id, modified_on = self.modified_on)