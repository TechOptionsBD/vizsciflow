import os
import sys

from config import Config
from flask import g

import psutil
from datetime import datetime

from .models import Status, Workflow, LogType, AccessRights, DataType, User
from dsl.fileop import FolderItem

from elasticsearch import Elasticsearch
es = Elasticsearch()

class ElasticManager():
    
    @staticmethod
    def close():
        pass

    @staticmethod
    def clear():
        final_indices = es.indices.get_alias().keys()
        
        for _index in final_indices:
            try:
                if "." not in _index: # avoid deleting indexes like `.kibana`
                    # if _index == 'datasets':# delete index as needed
                    es.indices.delete(index=_index)
                    print ("Successfully deleted:", _index)
            except Exception as error:
                print ('indices.delete error:', error, 'for index:', _index)

    # @staticmethod
    # def create_user_index():
    #     index = 'users'
    #     es.indices.create(index)
    
    @staticmethod
    def update_doc(index, runnable):
        es.update(index=index, id=runnable['id'], body = {"doc": runnable})

    @staticmethod
    def add_json_to_es_index(index, runnable):
        es.index(index=index, id=runnable["id"], body=runnable)

    @staticmethod
    def add_to_es_index(index, run_id, runnable):
        payload = {}

        for attr, value in runnable.__dict__.items():
            payload[attr] = value
        es.index(index=index, id=run_id, body=payload)
        return True

    @staticmethod
    def runnable_query_index_by_workflow_id(index, workflow_id):
        run_items = []
        search = es.search(index = index, body = {'query': {'match': {'_workflow_id': workflow_id}}})
        for hit in search['hits']['hits']:
            if int(hit['_id']) not in run_items:
                run_items.append(int(hit['_id']))
        return run_items

    @staticmethod
    def runnable_query_index_by_user_id(index, user_id):
        run_items = []
        search = es.search(index = index, body = {'query': {'match': {'user_id': user_id}}})
        for hit in search['hits']['hits']:
            if int(hit['_id']) not in run_items:
                run_items.append(int(hit['_id']))
        return run_items

    @staticmethod
    def runnable_query_index_by_fields(index, **kwargs):

        match = {}
        for k,v in kwargs:
            match[k] = v
        run_items = []
        search = es.search(index = index, body = {'query': {'match': match}})
        for hit in search['hits']['hits']:
            if int(hit['_id']) not in run_items:
                run_items.append(int(hit['_id']))
        return run_items

    @staticmethod
    def runnable_query_index(index, id):
        run_items = []
        search = es.search(index = index, body = {"query":{ "ids":{ "values": [id] } } })
        for hit in search['hits']['hits']:
            run_items.append(hit)

        if run_items:
            return run_items[0]['_source']

# class ElasticNode():
#     id = None
#     created_on = datetime.utcnow()
#     modified_on = datetime.utcnow()
#     properties = {}
    
#     def __init__(self, **kwargs):
#         self.created_on = kwargs.pop('created_on', datetime.utcnow())
#         self.modified_on = kwargs.pop('modified_on', datetime.utcnow())
        
#         # other properties
#         for k, v in kwargs.items():
#             self.properties[k] = v
                    
#     @staticmethod
#     def get_with_and(cls_, **kwargs):
#         # return items with id directly
#         id = kwargs.pop('id', None)
#         if id:
#             return cls_.match(graph(), int(id))
#         #query with other attributes
#         query = ""
#         for k in kwargs:
#             if query:
#                 query += " AND"
#             if isinstance(kwargs[k], str):
#                 query += " _.{0}='{1}'".format(k, kwargs[k])
#             else:
#                 query += " _.{0}={1}".format(k, kwargs[k])

#         return cls_.match(graph()).where(query) if query else cls_.match(graph())
    
#     @staticmethod
#     def get_with_or(cls_, **kwargs):
#         # return items with id directly
#         id = kwargs.pop('id', None)
#         #query with other attributes
#         query = ""
#         for k in kwargs:
#             if query:
#                 query += " OR"
#             if isinstance(kwargs[k], str):
#                 query += " _.{0}='{1}'".format(k, kwargs[k])
#             else:
#                 query += " _.{0}={1}".format(k, kwargs[k])

#         if id:
#             if query:
#                 query += " OR "
#             query += "ID(id)={0}".format(id)
#         return cls_.match(graph()).where(query) if query else cls_.match(graph())

#     @staticmethod
#     def OrderBy(self, items, key):
#         pass
    
#     @staticmethod
#     def push(node):
#         graph().push(node)
    
#     def json(self):
        
#         j = {
#             'id': self.id,
#             'created_on': str(self.created_on),
#             'modified_on': str(self.modified_on),
#         }
#         for k, v in self.properties.item():
#             j.update({k: v})
#         return j

# class ElasticDataSource(ElasticNode):
#     name = None
#     type = None
#     url = None
#     root = None
#     public = True
#     prefix = None
#     active = True
#     temp = False

#     #user name and password if authentication is needed for the data source (e.g. hdfs, ftp)
#     user = None
#     password = None
    
#     def __init__(self, **kwargs):
#         self.name = kwargs.pop('name', None)
#         self.type = kwargs.pop('type', None)
#         self.url = kwargs.pop('url', None)
#         self.public = kwargs.pop('public', True)
#         self.user = kwargs.pop('user', None)
#         self.password = kwargs.pop('password', None)
#         self.prefix = kwargs.pop('prefix', None)
#         self.active = kwargs.pop('active', True)
#         self.temp = kwargs.pop('temp', False)

#         super(ElasticDataSource, self).__init__(**kwargs)

#     @staticmethod
#     def insert_datasources():
#         try:
#             datasrc = ElasticDataSource(name='HDFS', type='hdfs', url='hdfs://206.12.102.75:54310/', root='/user', user='hadoop', password='spark#2018', public='/public', prefix='HDFS')
#             graph().push(datasrc)
#             basedir = os.path.dirname(os.path.abspath(__file__))
#             storagedir = os.path.abspath(os.path.join(basedir, '../storage'))
#             datasrc = ElasticDataSource(name='LocalFS', type='posix', url=storagedir, root='/', public='/public')
#             graph().push(datasrc)
#             datasrc = ElasticDataSource(name='GalaxyFS', type='gfs', url='http://sr-p2irc-big8.usask.ca:8080', root='/', password='7483fa940d53add053903042c39f853a', prefix='GalaxyFS')
#             graph().push(datasrc)
#             datasrc = ElasticDataSource(name='HDFS-BIG', type='hdfs', url='http://sr-p2irc-big1.usask.ca:50070', root='/user', user='hdfs', public='/public', prefix='HDFS-BIG')
#             graph().push(datasrc)
#         except Exception as e:
#             logging.error("Error creating data sources: " + str(e))
#             raise

#     def __repr__(self):
#         return '<DataSourceItem %r>' % self.name

#     @staticmethod
#     def get(**kwargs):
#         return NodeItem.get_with_and(DataSourceItem, **kwargs)
    
#     @staticmethod
#     def has_access_rights(user_id, path, checkRights):
#         defaultRights = AccessRights.NotSet
        
#         if path == os.sep:
#             defaultRights = AccessRights.Read # we are giving read access to our root folder to all logged in user

#         prefixedDataSources = DataSourceItem.match(graph()).where("_.prefix='{0}' OR _.url = '{1}'".format(path, path))
#         if list(prefixedDataSources):
#             defaultRights = AccessRights.Read

#         #cypher = "MATCH(u:UserItem)-[:USERACCESS]->(v:ValueItem) WHERE ID(u)={0} AND v.value= RETURN v"

#         return True


# class RoleItem(NodeItem):
#     name = Property("name")
#     default = Property("default", False)
#     permissions = Property("permissions")

#     users = RelatedTo("UserItem", "ROLEUSER")

#     def __init__(self, **kwargs):
#         self.name = kwargs.pop('name', None)
#         self.default = kwargs.pop('default', False)
#         self.permissions = kwargs.pop('permissions', 0x00)
#         super(RoleItem, self).__init__(**kwargs)

#     @staticmethod
#     def get(**kwargs):
#         return NodeItem.get_with_and(RoleItem, **kwargs)

#     @staticmethod
#     def insert_roles():
#         roles = {
#             'User': (Permission.FOLLOW |
#                      Permission.COMMENT |
#                      Permission.WRITE_ARTICLES |
#                      Permission.WRITE_WORKFLOWS, True),
#             'Moderator': (Permission.FOLLOW |
#                           Permission.COMMENT |
#                           Permission.WRITE_ARTICLES |
#                           Permission.WRITE_WORKFLOWS |
#                           Permission.MODERATE_COMMENTS |
#                           Permission.MODERATE_WORKFLOWS, False),
#             'Administrator': (0xff, False)
#         }
#         try:
#             for r in roles:
#                 role = RoleItem.get(name=r).first()
#                 if role is None:
#                     role = RoleItem(name=r)
#                 role.permissions = roles[r][0]
#                 role.default = roles[r][1]
#                 graph().push(role)            
#         except:
#             logging.error("Error creating default roles")
#             raise

#     def __repr__(self):
#         return '<Role %r>' % self.name

# class UserItem(NodeItem, UserMixin):    
#     email = Property("email")
#     username = Property("username")    
#     password_hash = Property("password_hash")
#     confirmed = Property("confirmed", True)
#     name = Property("name")
#     location = Property("location")
#     about_me = Property("about_me")
#     member_since = Property("member_since")
#     last_seen = Property("last_seen")
#     avatar_hash = Property("avatar_hash")
#     oid = Property("oid")
    
#     runs = RelatedTo("RunnableItem", "USERRUN")
#     workflows = RelatedTo("WorkflowItem", "OWNERWORKFLOW")
#     datasets = RelatedTo("ValueItem", "USERACCESS")
#     modules = RelatedTo("ModuleItem", "USERMODULE")
#     roles = RelatedFrom("RoleItem", "ROLEUSER")
#     moduleaccesses = RelatedTo("ModuleItem", "MODULEACCESS")
#     workflowaccesses = RelatedTo("WorkflowItem", "WORKFLOWACCESS")

#     def __init__(self, **kwargs):
#         self.email = kwargs.pop('email', None)
#         self.username = kwargs.pop('username', None)
#         self.confirmed = kwargs.pop('confirmed', True)
#         self.location = kwargs.pop('location', None)
#         self.about_me = kwargs.pop('about_me', None)
#         self.member_since = kwargs.pop('member_since', neotime.DateTime.utc_now())
#         self.last_seen = kwargs.pop('last_seen', neotime.DateTime.utc_now())
#         self.avatar_hash = kwargs.pop('avatar_hash', None)
#         self.oid = kwargs.pop('oid', 0)

#         self.password_hash = kwargs.pop('password_hash', None)
#         if not self.password_hash:
#             self.password = kwargs.pop('password', None)

#         if self.email is not None and self.avatar_hash is None:
#             self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

#         super(UserItem, self).__init__(**kwargs)

#     def gravatar(self, size=100, default='identicon', rating='g'):
#         if request.is_secure:
#             url = 'https://secure.gravatar.com/avatar'
#         else:
#             url = 'http://www.gravatar.com/avatar'
        
#         hash = None
#         if self.email:
#             hash = self.avatar_hash or hashlib.md5(
#                 self.email.encode('utf-8')).hexdigest()

#         return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
#             url=url, hash=hash, size=size, default=default, rating=rating)

#     @property
#     def role(self):
#         return list(self.roles)[0]

#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')

#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password) if password else None

#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)

#     def verify_and_update_password(self, oldpassword, password):
#         if not check_password_hash(self.password_hash, oldpassword):
#             return False
#         self.password = password
#         graph.push(self)
#         return True

#     @staticmethod
#     def first(**kwargs):
#         return UserItem.get(**kwargs).first()

#     @staticmethod
#     def get(**kwargs):
#         return NodeItem.get_with_and(UserItem, **kwargs)

#     @staticmethod
#     def load(user_id):
#         if user_id:
#             return UserItem.first(id=user_id)
#         else: # this will be very resource-intensive. never call it.
#             return list(UserItem.match(graph()).limit(sys.maxsize))

#     # @staticmethod
#     # def Create(user_id):
#     #     user = UserItem(User.query.get(user_id).username)
#     #     user.user_id = user_id
#     #     return user
    
#     @staticmethod
#     def Create(**kwargs):
#         user = UserItem(**kwargs)
        
#         graph().push(user)
        
#         role = None
#         if user.email == current_app.config['PHENOPROC_ADMIN']:
#             role = RoleItem.get(permissions=0xff).first()
#             role.users.add(user)
#         if role is None:
#             role = RoleItem.get(default=True).first()
#             role.users.add(user)
#         if role:
#             user.roles.add(role)
            
#         if user.email is not None and user.avatar_hash is None:
#             user.avatar_hash = hashlib.md5(user.email.encode('utf-8')).hexdigest()

#         graph().push(role)
        
#         return user
            
#     @property
#     def Runs(self):
#         return list(self.runs)
    
#     @property
#     def Workflows(self):
#         return list(self.workflows)
    
#     def ping(self):
#         self.last_seen = neotime.DateTime.utc_now()
#         graph().push(self)
    
#     def can(self, permissions):
#         return self.role is not None and \
#             self.role.permissions is not None and \
#             (self.role.permissions & permissions) == permissions

#     def is_administrator(self):
#         return self.can(Permission.ADMINISTER)
    
#     def add_module(self, module_id, access):
#         module = ModuleItem.get(id=module_id).first()
#         self.modules.add(module)
    
#     def add_modules_access(self, function, package, access):
#         modules = ModuleItem.get(name=function, package=package)
#         for module in modules:
#             self.modules.add(module)

#     @staticmethod
#     def get_other_users_with_entities(id, *args):
#         argstr = ",.".join(args)
#         users = graph().run("MATCH(u:UserItem) WHERE ID(u)!={0} RETURN u{.{1}}".format(id, argstr))
#         nodes = []
#         for node in iter(users):
#             #yield node['n']
#             nodes.append(node['n'])



# class ElasticRunnable(ElasticNode): #number
#     _name = "name"
    
#     # out = Property("out", "")
#     # error = Property("error", "")
#     # view = Property("view", "")
    
#     # script = Property("script", "")
#     _status = Status.RECEIVED
#     _duration = 0
#     _provenance = False
#     _error = ""
#     # _modules = RelatedTo("ElasticModule", "MODULE", "id(b)")
#     # users = RelatedFrom(UserItem, "USERRUN")
#     # workflows = RelatedFrom(WorkflowItem, "WORKFLOWRUN")
    
#     # cpu_init = Property("cpu_init", psutil.cpu_percent())
#     # memory_init = Property("memory_init", (psutil.virtual_memory()[2])/bytes_in_gb)
    
#     # cpu_run = Property("cpu_run", 0.0)
#     # memory_run = Property("memory_run", 0.0)
    
#     _started_on = datetime.min
#     _user_id = 0
#     _workflow_id = 0
#     _celery_id = 0

#     def __init__(self, name, **kwargs):
#         super().__init__(**kwargs)
#         self._name = name
                    
#     @property
#     def user_id(self):
#         return self._user_id
    
#     @property
#     def workflow_id(self):
#         return self._workflow_id
    
#     @property
#     def duration(self):
#         if self._status == Status.STARTED:
#             delta = datetime.utcnow() - self._started_on
#             self._duration = delta.total_seconds()

#         return self._duration    
    
#     @property
#     def name(self):
#         return self._name

#     @property
#     def error(self):
#         return self._error
    
#     @error.setter
#     def error(self, value):
#         self._error = value

#     @property
#     def celery_id(self):
#         return self._celery_id
    
#     @celery_id.setter
#     def celery_id(self, value):
#         self._celery_id = value

#     @property
#     def status(self):
#         return self._status
    
#     @property
#     def provenance(self):
#         return self._provenance

#     @property
#     def started_on(self):
#         return self._started_on

#     def load_from_es(self, item):
#         self._provenance = item['provenance']
#         self._workflow_id = item['workflow_id']
#         self._user_id = item['user_id']
#         self._status = item['status']
#         self._duration = int(item['duration'])
#         self._status = item['status']
#         self._started_on =  datetime.strptime(item['started_on'], "%m/%d/%y, %H:%M:%S")
#         return super().load_from_es(item)

#     @staticmethod
#     def load(run_id = None, workflow_id = None):
#         if run_id:
#             item = ElasticManager.runnable_query_index('runnable', run_id)
#             if item:
#                 runnable = ElasticRunnable(item['name'])
#                 runnable._id = run_id
#                 return runnable.load_from_es(item)
#         elif workflow_id:
#             #get all items with workflow_id matched
#             runnables = ElasticManager.runnable_query_index_by_workflow_id('runnable', workflow_id)
#             return [ElasticRunnable.load(r) for r in runnables]
#         # else: # this will be very resource-intensive. never call it.
#         #     return list(ElasticRunnable.match(graph()).limit(sys.maxsize))
    
# #     @staticmethod
# #     def load_for_users(user_id):
# #         user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
# #         if not user:
# #             return []
# #         return [r for r in user.runs if not r.provenance]
    
#     @staticmethod
#     def load_for_users(user_id):        
#         runnables = ElasticManager.runnable_query_index_by_user_id('runnable', user_id)
#         return [ElasticRunnable.load(r) for r in runnables]
        
#     def add_module(self, function_name, package):
#         item = ElasticModule(function_name, package)
#         self._modules.add(item)
#         return item
    
#     @staticmethod
#     def create(run_id, user_id, workflow_id, script, provenance, args):
        
#         dbWorkflow = Workflow.query.get(workflow_id)
#         item = ElasticRunnable(dbWorkflow.name)
#         item._id = run_id
#         item._provenance = provenance
#         item._user_id = user_id
#         item._workflow_id = workflow_id

#         # add to es db
#         ElasticManager.add_json_to_es_index('runnable', item.json())
#         return item
        
#     @staticmethod
#     def load_if(condition = None):
#         pass
    
#     @property        
#     def completed(self):
#         return self.status == Status.SUCCESS or self.status == Status.FAILURE or self.status == Status.REVOKED
    
#     def set_status(self, value, update = True):
#         self._status = value
        
#         if value == Status.STARTED:
#             self._started_on = datetime.utcnow()
    
#         if value == Status.SUCCESS or value == Status.FAILURE or value == Status.REVOKED:
#             self._duration = datetime.utcnow() - self.started_on
        
#         if update:
#             self.update()

#     def update(self):
#         ElasticManager.update_doc('runnable', self.json())

#     def json(self):
#         j = ElasticNode.json(self)
#         j.update({
#             'user_id': self.user_id,
#             'workflow_id': self.workflow_id,
#             'error': self.error,
#             'status': self.status,
#             'duration': self.duration,
#             'name': self.name,
#             'provenance': self.provenance,
#             'started_on': self.started_on.strftime("%m/%d/%y, %H:%M:%S")
#             })
#         return j
           
#     def to_json_tooltip(self):
#         error = ""
#         if error:
#             error = (self.error[:60] + '...') if len(self.error) > 60 else self.error
#         return {
#             'id': self.id,
#             'name': self.name,
#             'status': self.status,
#             'err': error,
#             'duration': self.duration,
#             'created_on': self.created_on.strftime("%m/%d/%y, %H:%M:%S"),
#             'modified_on': self.modified_on.strftime("%m/%d/%y, %H:%M:%S")
#         }
        
#     def to_json_log(self):
#         log = []
        
#         # for module in self._modules:
#         #     log.append(module.to_json_log())

#         return {
#             'id': self.id,
#             'status': self.status,
#             'err': self.error,
#             'duration': self.duration,
#             'log': log
#         }
        
#     def to_json_info(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'name': self.name,
#             'modified_on': self.modified_on.strftime("%m/%d/%y, %H:%M:%S"),
#             'status': self.status
#         }
        
# class ElasticModule(ElasticNode):
#     _inputs = []
#     _outputs = []
#     _logs = []

    
#     _name = "name"
#     _package = "package"
#     _status = Status.RECEIVED
    
#     _started_on = datetime.min
#     _duration = 0
    
#     def __init__(self, name, package = None, **kwargs):
#         super().__init__(**kwargs)
#         self._name = name
#         self._package = package
    
#     def json(self):
#         j = ElasticNode.json(self)
#         j.update({
#             'event': 'RUN-CREATE',
#             'name':self._name,
#             'status': self.status           
#         })
        
#         return j 

#     def name(self):
#         return self._name
        
#     def inputs(self):
#         return self._inputs
    
#     def outputs(self):
#         return self._outputs
    
#     def prop_from_node(self, node):
#         ElasticNode.prop_from_node(self, node, "name", "status")
#         self.status = node["status"]
#         return self
    
#     @property
#     def run_id(self):
#         return list(self.runs)[0].id
           
#     @property
#     def duration(self):
#         if self._status == Status.STARTED:
#             self._duration = datetime.utcnow() - self._started_on
#             #graph().push(self)
            
#         return self._duration  
    
#     @duration.setter
#     def duration(self, value):
#         self._duration = value
        
#     @staticmethod
#     def load(module_id, name = None, package = None):
#         # adjust for es db
#         if module_id:
#             pass
#             #
#         elif name:
#             if not package:
#                 pkg_func = name.split(".")
#                 if len(pkg_func) > 1:
#                     name = pkg_func[-1]
#                     package = ".".join(pkg_func[0:-1])
#                 else:
#                     return ElasticModule.match(graph()).where("_.name='{0}'".format(name)).first()
            
#             return ElasticModule.match(graph()).where("_.name='{0}' AND _.package='{1}'".format(name, package)).first()
        
#     def start(self):
#         self._status = Status.STARTED
#         self._started_on = datetime.utcnow()        
#         self._duration = 0
#         self.update()
    
#     def succeeded(self):
#         self._status = Status.SUCCESS
#         self._modified_on = datetime.utcnow()
#         self._duration = datetime.utcnow() - self._started_on
#         self.update()
    
#     def failed(self, log = "Task Failed."):
#         self._status = Status.FAILURE
#         self._modified_on = datetime.utcnow()()
#         self._duration = datetime.utcnow()() - self._started_on
#         self.update()
        
#     def to_json_log(self):
        
#         #data = [{ "datatype": data.valuetype, "data": data._value} for data in self._outputs]
            
#         return { 
#             'name': self._name if self._name else "", 
#             'status': self.status
#          #   'data': data
#         }

