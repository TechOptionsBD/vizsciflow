from collections import namedtuple
import logging
import sys
import os
import json

from flask_login.mixins import UserMixin

import psutil
from datetime import datetime

from .ogmex import Model, Property, RelatedTo, RelatedFrom
from py2neo import NodeMatcher
from py2neo import Graph
import neotime

from .common import Status, LogType, AccessRights, Permission
from dsl.fileop import FolderItem
from dsl.datatype import DataType

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app, request, url_for
import hashlib

from .managers.sessionmgr import SessionManager

bytes_in_gb = 1024 * 1024
def neotime_duration_to_ms(duration):
    return duration[0] * 2629800000 + duration[1] * 86400000 + duration[2] * 1000 + duration[3]/1000000

def neotime_duration_to_s(duration):
    return neotime_duration_to_ms(duration)/1000

def neotime2StrfTime(date):
    if isinstance(date, neotime.DateTime):
        date = datetime(date.year, date.month, date.day,
                                 date.hour, date.minute, int(date.second),
                                 int(date.second * 1000000 % 1000000),
                                 tzinfo=date.tzinfo)
    return date.strftime("%d-%m-%Y %H:%M:%S")

def graph():
    return SessionManager.session()

#inspect.getmembers(cls_, lambda a:not(inspect.isroutine(a)))
class NodeItem(Model):
    __primarykey__ = "__id__"
    created_on = Property("created_on")
    modified_on = Property("modified_on")
    properties = []
    
    def __init__(self, **kwargs):
        self.created_on = kwargs.pop('created_on', neotime.DateTime.utc_now())
        self.modified_on = kwargs.pop('modified_on', neotime.DateTime.utc_now())
        
        # other properties
        for k, v in kwargs.items():
            #self.add_new_prooperty(k, v)
            self.properties.append(Property(k, v))
                
    def add_new_property(self, name, value):
        self.__class__ = type(
            type(self).__name__, (self.__class__,), {name: Property()}
        )
        setattr(self, name, value)
    
    @staticmethod
    def get_with_and(cls_, **kwargs):
        # return items with id directly
        id = kwargs.pop('id', None)
        if id:
            return cls_.match(graph(), int(id))
        #query with other attributes
        query = ""
        for k in kwargs:
            if query:
                query += " AND"
            if isinstance(kwargs[k], str):
                query += " _.{0}='{1}'".format(k, kwargs[k])
            else:
                query += " _.{0}={1}".format(k, kwargs[k])

        return cls_.match(graph()).where(query) if query else cls_.match(graph())
    
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
        return cls_.match(graph()).where(query) if query else cls_.match(graph())

    @property
    def label(self):
        return self.__primarylabel__

    @label.setter
    def label(self, l):
        self.__primarylabel__ = l
            
    @property
    def id(self):
        return self.__primaryvalue__
    
    @staticmethod
    def OrderBy(self, items, key):
        pass

    @staticmethod
    def push(node):
        graph().push(node)
    
    @property
    def created_on_formatted(self):
        return self.created_on.to_native()

    @created_on_formatted.setter
    def created_on_formatted(self, value):
        self.created_on = neotime.DateTime(value.year, value.month, value.day, value.hour, value.minute, value.second, value.tzinfo)
#     
    @property
    def modified_on_formatted(self):
        return self.modified_on.to_native()
    @modified_on_formatted.setter
    def modified_on_formatted(self, value):        
        self.modified_on = neotime.DateTime(value.year, value.month, value.day, value.hour, value.minute, value.second, value.tzinfo)
        
    def json(self):
        
        j = {
            'created_on': str(self.created_on),
            'modified_on': str(self.modified_on),
        }
        for property in self.properties:
            j.update({property.key: property})
        return j
    
    @staticmethod
    def load(id):
        registry = {'UserItem':UserItem, 'WorkflowItem':WorkflowItem, 'ModuleInvocationItem':ModuleInvocationItem, 'ValueItem':ValueItem, 'RunnableItem': RunnableItem}
        
        cypher = "MATCH(n) WHERE ID(n)={0} RETURN n".format(id)
        c = graph().run(cypher)
        node = next(iter(c))['n']
        label = list(node.labels)[0]
        if  label in registry:
            return registry[label].wrap(node)

    @staticmethod
    def matchItems(cypher, **parameters):
        registry = {'UserItem':UserItem, 'WorkflowItem':WorkflowItem, 'ModuleInvocationItem':ModuleInvocationItem, 'ValueItem':ValueItem, 'RunnableItem': RunnableItem}
        
        c = graph().run(cypher, parameters)
        for node in iter(c):
            graphnode = node['n']
            label = list(graphnode.labels)[0]
            if  label in registry:
                yield registry[label].wrap(graphnode)

    @staticmethod
    def run(cypher, **parameters):
        return graph().run(cypher, parameters)

class DataSourceItem(NodeItem):
    name = Property("name")
    type = Property("type")
    url = Property("url")
    root = Property("root")
    public = Property("public", True)
    prefix = Property("prefix")
    active = Property("active")
    temp = Property("temp", False)
    #user name and password if authentication is needed for the data source (e.g. hdfs, ftp)
    user = Property("user")
    password = Property("password")
    
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.type = kwargs.pop('type', None)
        self.url = kwargs.pop('url', None)
        self.public = kwargs.pop('public', True)
        self.user = kwargs.pop('user', None)
        self.password = kwargs.pop('password', None)
        self.prefix = kwargs.pop('prefix', None)
        self.active = kwargs.pop('active', True)
        self.temp = kwargs.pop('temp', False)

        super(DataSourceItem, self).__init__(**kwargs)

    @staticmethod
    def insert_datasources():
        try:
            datasrc = DataSourceItem(name='HDFS', type='hdfs', url='hdfs://206.12.102.75:54310/', root='/user', user='hadoop', password='spark#2018', public='/public', prefix='HDFS')
            graph().push(datasrc)
            datasrc = DataSourceItem(name='LocalFS', type='posix', url='/home/phenodoop/phenoproc/storage/', root='/', public='/public')
            graph().push(datasrc)
            datasrc = DataSourceItem(name='GalaxyFS', type='gfs', url='http://sr-p2irc-big8.usask.ca:8080', root='/', password='7483fa940d53add053903042c39f853a', prefix='GalaxyFS')
            graph().push(datasrc)
            datasrc = DataSourceItem(name='HDFS-BIG', type='hdfs', url='http://sr-p2irc-big1.usask.ca:50070', root='/user', user='hdfs', public='/public', prefix='HDFS-BIG')
            graph().push(datasrc)
        except Exception as e:
            logging.error("Error creating data sources: " + str(e))
            raise

    def __repr__(self):
        return '<DataSourceItem %r>' % self.name

    @staticmethod
    def get(**kwargs):
        return NodeItem.get_with_and(DataSourceItem, **kwargs)
    
    @staticmethod
    def has_access_rights(user_id, path, checkRights):
        defaultRights = AccessRights.NotSet
        
        if path == os.sep:
            defaultRights = AccessRights.Read # we are giving read access to our root folder to all logged in user

        prefixedDataSources = DataSourceItem.match(graph()).where("_.prefix='{0}' OR _.url = '{1}'".format(path, path))
        if list(prefixedDataSources):
            defaultRights = AccessRights.Read

        #cypher = "MATCH(u:UserItem)-[:USERACCESS]->(v:ValueItem) WHERE ID(u)={0} AND v.value= RETURN v"

        return True
    
#     @staticmethod
#     def add(user_id, datasource_id, url, rights):
#         return DataSourceItem.add(user_id, datasource_id, url, rights)
    
#     @staticmethod
#     def add(user_id, ds_id, url, rights):
#         try:
#             data = DataSourceAllocation.query.filter(and_(DataSourceAllocation.datasource_id == ds_id, DataSourceAllocation.url == url)).first()
#             if not data:
#                 data = DataSourceAllocation()
#                 data.datasource_id = ds_id
#                 data.url = url
#                 db.session.add(data)
#                 db.session.commit()
            
#             DataPermission.add(user_id, data.id, rights)
#             return data
#         except SQLAlchemyError:
#             db.session.rollback()
#             raise


# class DataSourceAllocation(NodeItem):
#     datasources = RelatedTo("DataSourceItem", "ALLOCATIONDATASOURCE")
#     url = Property("url")


class RoleItem(NodeItem):
    name = Property("name")
    default = Property("default", False)
    permissions = Property("permissions")

    users = RelatedTo("UserItem", "ROLEUSER")

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.default = kwargs.pop('default', False)
        self.permissions = kwargs.pop('permissions', 0x00)
        super(RoleItem, self).__init__(**kwargs)

    @staticmethod
    def get(**kwargs):
        return NodeItem.get_with_and(RoleItem, **kwargs)

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
                role = RoleItem.get(name=r).first()
                if role is None:
                    role = RoleItem(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                graph().push(role)            
        except:
            logging.error("Error creating default roles")
            raise

    def __repr__(self):
        return '<Role %r>' % self.name

class UserItem(NodeItem, UserMixin):    
    email = Property("email")
    username = Property("username")    
    password_hash = Property("password_hash")
    confirmed = Property("confirmed", True)
    name = Property("name")
    location = Property("location")
    about_me = Property("about_me")
    member_since = Property("member_since")
    last_seen = Property("last_seen")
    avatar_hash = Property("avatar_hash")
    oid = Property("oid")
    
    runs = RelatedTo("RunnableItem", "USERRUN")
    workflows = RelatedTo("WorkflowItem", "OWNERWORKFLOW")
    datasets = RelatedTo("ValueItem", "USERACCESS")
    modules = RelatedTo("ModuleItem", "USERMODULE")
    roles = RelatedFrom("RoleItem", "ROLEUSER")
    moduleaccesses = RelatedTo("ModuleItem", "MODULEACCESS")
    workflowaccesses = RelatedTo("WorkflowItem", "WORKFLOWACCESS")

    def __init__(self, **kwargs):
        self.email = kwargs.pop('email', None)
        self.username = kwargs.pop('username', None)
        self.confirmed = kwargs.pop('confirmed', True)
        self.location = kwargs.pop('location', None)
        self.about_me = kwargs.pop('about_me', None)
        self.member_since = kwargs.pop('member_since', neotime.DateTime.utc_now())
        self.last_seen = kwargs.pop('last_seen', neotime.DateTime.utc_now())
        self.avatar_hash = kwargs.pop('avatar_hash', None)
        self.oid = kwargs.pop('oid', 0)

        self.password_hash = kwargs.pop('password_hash', None)
        if not self.password_hash:
            self.password = kwargs.pop('password', None)

        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

        super(UserItem, self).__init__(**kwargs)

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
        return list(self.roles)[0]

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
        graph.push(self)
        return True

    @staticmethod
    def get(**kwargs):
        return NodeItem.get_with_and(UserItem, **kwargs).first()

    @staticmethod
    def load(user_id):
        if user_id:
            return UserItem.get(id=user_id)
        else: # this will be very resource-intensive. never call it.
            return list(UserItem.match(graph()).limit(sys.maxsize))

    # @staticmethod
    # def Create(user_id):
    #     user = UserItem(User.query.get(user_id).username)
    #     user.user_id = user_id
    #     return user
    
    @staticmethod
    def Create(**kwargs):
        user = UserItem(**kwargs)
        
        graph().push(user)
        
        role = None
        if user.email == current_app.config['PHENOPROC_ADMIN']:
            role = RoleItem.get(permissions=0xff).first()
            role.users.add(user)
        if role is None:
            role = RoleItem.get(default=True).first()
            role.users.add(user)
        if role:
            user.roles.add(role)
            
        if user.email is not None and user.avatar_hash is None:
            user.avatar_hash = hashlib.md5(user.email.encode('utf-8')).hexdigest()

        graph().push(role)
        
        return user
            
    @property
    def Runs(self):
        return list(self.runs)
    
    @property
    def Workflows(self):
        return list(self.workflows)
    
    def ping(self):
        self.last_seen = neotime.DateTime.utc_now()
        graph().push(self)
    
    def can(self, permissions):
        return self.role is not None and \
            self.role.permissions is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
    
    def add_module(self, module_id, access):
        module = ModuleItem.get(id=module_id).first()
        self.modules.add(module)
    
    def add_modules_access(self, function, package, access):
        modules = ModuleItem.get(name=function, package=package)
        for module in modules:
            self.modules.add(module)

    @staticmethod
    def get_other_users_with_entities(id, *args):
        argstr = ",.".join(args)
        users = graph().run("MATCH(u:UserItem) WHERE ID(u)!={0} RETURN u{.{1}}".format(id, argstr))
        nodes = []
        for node in iter(users):
            #yield node['n']
            nodes.append(node['n'])

class ModuleItem(NodeItem):
    org = Property("org")
    name = Property("name")
    package = Property("package")
    public = Property("public", False)
    active = Property("active", True)
    group = Property("group")
    example = Property("example")
    desc = Property("desc")
    href = Property("href")
    internal = Property("internal")
    module = Property("module")

    owners = RelatedFrom("UserItem", "USERMODULE")
    users = RelatedFrom("UserItem", "MODULEACCESS")

    params = RelatedTo("DataPropertyItem", "PARAM", "id(b)")
    returns = RelatedTo("DataPropertyItem", "RETURN", "id(b)")

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

        super(ModuleItem, self).__init__(**kwargs)
        
    @staticmethod
    def add_user_access(id, users, access):
        module = ModuleItem.get(id=id)
        users = users.split(',')
        for user in users:
            module.users.add(user)
            user.moduleaccesses.add(module)
        graph().push(module)

    def add_owner(self, user_id, access):
        user = UserItem.get(id=user_id)
        user.modules.add(self)
        graph().push(user)

    @staticmethod
    def get(**kwargs):
        return NodeItem.get_with_and(ModuleItem, **kwargs)
    
    @staticmethod
    def add(owner_id, value, access, users):
        module = ModuleItem(**value)

        graph().push(module)

        if owner_id is not None:
            owner = UserItem.get(id=owner_id)
            module.owners.add(owner)
            owner.modules.add(module)
            graph().push(owner)

        if users:
            if owner_id in users:
                users.remove(owner_id)
            for user_id in users:
                user = UserItem.get(id=user_id)
                if user:
                    module.users.add(user)
                    user.moduleaccesses.add(module)
                    graph().push(user)

        return module 

    def json(self):
        params = [p.json() for p in self.params]
        returns = [r.json() for r in self.returns]
        return {
            'id': self.id,
            #'user': self.user.username,
            'org': self.org if self.org else "",
            'name': self.name,
            'internal': self.internal if self.internal else "",
            'package': self.package  if self.package else "",
            'public': self.public,
            'module': self.module,
            'group': self.group if self.group else "",
            'desc': self.desc if self.desc else "",
            'href': self.href if self.href else "",
            'example': self.example if self.example else "",
            'is_owner': False,
            'params': params,
            'returns': returns
        }

    @staticmethod
    def insert_modules(url):
        funcs = ModuleItem.load_funcs_recursive(url)
        funclist = []
        for f in funcs.values():
            funclist.extend(f)

        modules = []
        for f in funclist:
            #module = ModuleItem(org=f["org"], name=f["name"], package=f["package"], internal=f["internal"], module=f["module"], example=f["example"], desc=f["desc"], group=f["group"], href=f["href"])
            module = ModuleItem(**f)
            for p in f["params"]:
                dp = DataPropertyItem(**p)
                graph().push(dp)
                module.params.add(dp)
            
            for p in f["returns"]:
                dp = DataPropertyItem(**p)
                graph().push(dp)
                module.returns.add(dp)
            
            modules.append(module)
            graph().push(module)
            
        return modules

    
    @staticmethod
    def load_funcs_recursive(library_def_file):
        if os.path.isfile(library_def_file):
            return ModuleItem.load_funcs(library_def_file)
        
        all_funcs = {}
        for f in os.listdir(library_def_file):
            funcs = ModuleItem.load_funcs_recursive(os.path.join(library_def_file, f))
            for k,v in funcs.items():
                if k in all_funcs:
                    all_funcs[k].extend(v)
                else:
                    all_funcs[k] = v if isinstance(v, list) else [v]
        return all_funcs
       
    @staticmethod
    def load_funcs(library_def_file):
        funcs = {}
        try:
            if not os.path.isfile(library_def_file) or not library_def_file.endswith(".json"):
                return funcs
            
            with open(library_def_file, 'r') as json_data:
                d = json.load(json_data)
                libraries = d["functions"]
                libraries = sorted(libraries, key = lambda k : k['package'].lower())
                for f in libraries:
                    org = f["org"] if f.get("org") else ""
                    name = f["name"] if f.get("name") else f["internal"]
                    internal = f["internal"] if f.get("internal") else f["name"]
                    module = f["module"] if f.get("module") else None
                    package = f["package"] if f.get("package") else ""
                    example = f["example"] if f.get("example") else ""
                    desc = f["desc"] if f.get("desc") else ""
                    #runmode = f["runmode"] if f.get("runmode") else ""
                    #level = int(f["level"]) if f.get("level") else 0
                    group = f["group"] if f.get("group") else ""
                    href = f["href"] if f.get("href") else ""
                    public = bool(f["public"]) if f.get("public") else True

                    params = []
                    if f.get("params"):
                        for p in f["params"]:
                            pname = p["name"] if p.get("name") else ""
                            pvalue = p["value"] if p.get("value") else ""
                            ptype = p["type"] if p.get("type") else ""
                            pdesc = p["desc"] if p.get("desc") else ""
                            params.append({"name": pname, "value": pvalue, "desc": pdesc, "type": ptype})
                            
                    returns = []
                    if f.get("returns"):
                        rs = f["returns"]
                        if not isinstance(rs, list):
                            rs = [rs]

                        for p in rs:
                            pname = p["name"] if p.get("name") else ""
                            ptype = p["type"] if p.get("type") else ""
                            pdesc = p["desc"] if p.get("desc") else ""
                            returns.append({"name": pname, "desc": pdesc, "type": ptype})

                    func = {
                        "org": org,
                        "name": name, 
                        "internal": internal,
                        "package":package, 
                        "module": module,
                        "params": params, 
                        "example": example,
                        "desc": desc,
                        #"runmode": runmode,
                        #"level": level, 
                        "group": group,
                        "returns": returns,
                        "public": public
                        }
                    if name.lower() in funcs:
                        funcs[name.lower()].extend([func])
                    else:
                        funcs[name.lower()] = [func]
        finally:
            return funcs
    
    def func_to_internal_name(self, funcname):
        for f in self.funcs:
            if f.get("name") and self.iequal(f["name"], funcname):
                return f["internal"]

    @staticmethod
    def get_module_by_name_package_for_user_access(user_id, name, package = None):
        service = ModuleItem.get(name=name, package=package).first()
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

class WorkflowItem(NodeItem):
    name = Property("name")
    desc = Property("desc")
    script = Property("script")
    public = Property("public", True)
    temp = Property("temp", False)
    derived = Property("derived", 0)
    
    owners = RelatedFrom("UserItem", "OWNERWORKFLOW")
    #users = RelatedFrom("UserItem", "WORKFLOWACCESS")
    runs = RelatedTo("RunnableItem", "WORKFLOWRUN")
    symbols = RelatedTo("ValueItem", "SYMBOL")
    modules = RelatedTo("ModuleInvocationItem", "MODULEINVOCATION")
    params = RelatedTo("DataPropertyItem", "PARAM", "id(b)")
    
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.desc = kwargs.pop('desc', "")
        self.script = kwargs.pop('script', None)
        self.public = kwargs.pop('public', True)
        self.temp = kwargs.pop('temp', False)
        self.derived = kwargs.pop('derived', 0)

        args = kwargs.pop('params', None)
        super(WorkflowItem, self).__init__(**kwargs)

        if args:
            for arg in args:
                param = DataPropertyItem(arg)
                graph().push(param)
                self.params.add(param)
    
    def add_module(self, **kwargs):
        module = NodeItem.get_with_and(ModuleItem, **kwargs).first()
        if module:
            self.modules.add(module)
            graph().push(self)
            return module

    def update_script(self, script):
        if self.script == script:
            return True                       
        try:
            self.script = script
            self.modified_on = neotime.DateTime.utc_now()
            graph().push(self)
            try:
                #self.git_write(script)
                pass
            except Exception as e:
                logging.error("Git error while updating workflow: " + e.message)
        except:
            raise

    @staticmethod
    def Create(**kwargs):
        owner_id = kwargs.pop('user_id', None)
        users =  kwargs.pop('users', None)
        workflow = WorkflowItem(**kwargs)
        graph().push(workflow)

        if owner_id is not None:
            owner = UserItem.get(id=owner_id)
            workflow.owners.add(owner)
            owner.workflows.add(workflow)
            graph().push(owner)
        if users:
            users = users.split(",")
            for username in users:
                user = UserItem.get(username=username)
                workflow.users.add(user)
                user.workflowaccesses.add(workflow)
                graph().push(user)
        return workflow
            
    @property
    def Runs(self):
        return list(self.runs)
    
    @property
    def user_id(self):
        return list(self.owners)[0].id


    @property
    def user(self):
        return list(self.owners)[0]

    @property
    def accesses(self):
        rights = []
        for user in list.users:
            v = {'user_id': id, 'rights': AccessRights.Write}
            rights.append(namedtuple("WorkflowAccess", v.keys())(*v.values()))

        return rights

    def to_json_info(self):
        return {
            'id': self.id,
            #'user': self.user.username,
            'name': self.name
        }

    def to_json(self):
        params = [param.json() for param in self.params]
        return {
            'id': self.id,
            'user': list(self.owners)[0].username if self.owners else '',#self.user.username,
            'name': self.name,
            'desc': self.desc,
            'script': self.script,
            'args': params
        }

    @staticmethod
    def get_workflows_as_list(access, user_id, *args):
        user = UserItem.get(id=user_id)
        workflows = [ownedwf for ownedwf in user.workflows]
        workflows.extend([accesswf for accesswf in user.workflowaccesses])
        return workflows
    
    @staticmethod
    def get(**kwargs):
        return NodeItem.get_with_and(WorkflowItem, **kwargs).first()

class DataItem(NodeItem):
    name = Property("name", "")
    value = Property("value", "")

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', "")
        self.value = DataItem.to_primitive(kwargs.pop('value', ""))

        super(DataItem, self).__init__(**kwargs)   
   
    @staticmethod
    def create(**kwargs):
        item = DataItem(*kwargs)
        graph().push(item)
        return item
    
    def json(self):
        j = NodeItem.json(self)
        j['value'] = self.value
        return j

    @staticmethod
    def to_primitive(value):
        return value if isinstance(value, (int, float, bool, str)) else str(value)

class ValueItem(DataItem):
    datatype = Property("datatype")
    type = Property("type")
    
    inputs = RelatedTo("ModuleInvocationItem", "INPUT")
    outputs = RelatedFrom("ModuleInvocationItem", "OUTPUT")
    
    #allocations = RelatedTo("DataAllocationItem", "ALLOCATION")
    users = RelatedFrom(UserItem, 'ACCESS')
    
    def __init__(self, **kwargs):
        self.type = kwargs.pop('type', DataType.Value) # if type else str(DataType.Value) #str(type(self.value))
        super(ValueItem, self).__init__(**kwargs)
        self.datatype =  str(type(self.value)) #str(self.__class__.__name__) #val_type#
    
    def set_name(self, value):
        self.name = value
    
    @staticmethod
    def Create(**kwargs):
        item = ValueItem(**kwargs)
        item.name = "value"
        graph().push(item)
        return item
    
    def get_allocation_for_user(self, user_id):
        return next((a for a in self.allocations if a.user_id == user_id), None)

    def allocate_for_user(self, user_id, rights):
        for a in self.users:
            if a.id == user_id:
                if rights > a.datasets.get(self, "rights"):
                    a.datasets.remove(self)
                    a.datasets.add(self, rights=rights)
                    graph().push(a)
                return self
            
        user = UserItem.get(id=user_id)
        user.datasets.add(self, rights=rights)
        graph().push(user)
        return self

    def __add__(self, other):
        if self.type == "value":
            return self.value + other.value
        elif self.type == DataType.File or self.type == DataType.Folder:
            FolderItem(self.value) + other.value
        else:
            raise NotImplementedError
    
    def __sub__(self, other):
        if self.type == "value":
            return self.value - other.value
        elif self.type == DataType.File or self.type == DataType.Folder:
            FolderItem(self.value) - other.value
        else:
            raise NotImplementedError
    
    def __mul__(self, other):
        if self.type == "value":
            return self.value * other.value
        else:
            raise NotImplementedError
    
    def __truediv__(self, other):
        if self.type == "value":
            return self.value / other.value
        else:
            raise NotImplementedError
                    
    def json(self):
        j = DataItem.json(self)
        j.update({
            'event': 'VAL-SAVE',
            'datatype': str(self.datatype),
            'type': self.type,
            'memory': (psutil.virtual_memory()[2])/bytes_in_gb,
            'cpu': (psutil.cpu_percent()),
            'name': self.name
        })
        return j
            
    @staticmethod
    def get_by_type_value(type, value):
        return ValueItem.match(graph()).where("_.type={0} AND _.value='{1}'".format(type, value)).first()
    
    @staticmethod
    def load(id = None, path = None):
        if id:
            return ValueItem.match(graph(), id).first()
        else:
            return ValueItem.match(graph()).where("_.value='{0}'".format(path)).first()
    
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
       
class DataPropertyItem(NodeItem):
    name = Property("name")
    value = Property("value")
    type = Property("type")
    desc = Property("desc")

    #data = RelatedFrom(ValueItem, "ALLOCATION")
    
    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.value = kwargs.pop('value', None)
        self.desc = kwargs.pop('desc', None)
        self.type = kwargs.pop('type', None)

        super(DataPropertyItem, self).__init__(**kwargs)
    
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
        
class RunnableItem(NodeItem): #number1
    celery_id = Property("celery_id", 0)
    name = Property("name")
    
    out = Property("out", "")
    error = Property("error", "")
    view = Property("view", "")
    
    script = Property("script", "")
    status = Property("status", Status.RECEIVED)
    duration = Property("duration", neotime.Duration())
    provenance = Property("provenance", False)
    args = Property("args", "")
    
    modules = RelatedTo("ModuleInvocationItem", "MODULEINVOCATION", "id(b)")
    users = RelatedFrom(UserItem, "USERRUN")
    workflows = RelatedFrom(WorkflowItem, "WORKFLOWRUN")
    
    cpu_init = Property("cpu_init", psutil.cpu_percent())
    memory_init = Property("memory_init", (psutil.virtual_memory()[2])/bytes_in_gb)
    cpu_run = Property("cpu_run", 0.0)
    memory_run = Property("memory_run", 0.0)
    
    started_on = Property("started_on", neotime.DateTime.min)

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', None)
        self.celery_id = kwargs.pop('celery_id', None)
        self.out = kwargs.pop('out', "")
        self.error = kwargs.pop('error', "")
        self.view = kwargs.pop('view', None)
        self.script = kwargs.pop('script', None)
        self.status = kwargs.pop('status', Status.RECEIVED)
        #self.duration = kwargs.pop('duration', neotime.Duration())
        self.provenance = kwargs.pop('provenance', False)
        self.args = kwargs.pop('args', "")
        
        super(RunnableItem, self).__init__(**kwargs)
                    
    @property
    def user_id(self):
        return list(self.users)[0].id
    
    @property
    def workflow_id(self):
        return list(self.workflows)[0].id
    
    # @property
    # def duration(self):
    #     if self.status == Status.STARTED:
    #         self.duration = neotime.DateTime.utc_now() - self.started_on
    #         #graph().push(self)
    #     return self.duration    
            
    def update(self):
        graph().push(self)
            
    @staticmethod
    def load_runnables_from_cypher(cypher):
        
        runs = []
        c = graph().run(cypher).data()
        for i in c:
            for _,v in i.items():
                runs.append(RunnableItem.load(v.identity))
        return runs
                
    @staticmethod
    def load(run_id = None, workflow_id = None):
        if run_id:
            return RunnableItem.match(graph(), run_id).first()
        elif workflow_id:
            return RunnableItem.match(graph()).where("_.workflow_id = {0}".format(workflow_id)).limit(sys.maxsize)
        else: # this will be very resource-intensive. never call it.
            return list(RunnableItem.match(graph()).limit(sys.maxsize))
    
#     @staticmethod
#     def load_for_users(user_id):
#         user = UserItem.match(graph()).where("_.user_id = {0}".format(user_id)).first()
#         if not user:
#             return []
#         return [r for r in user.runs if not r.provenance]
    
    @staticmethod
    def load_for_users(user_id):        
        cypher = "MATCH (n:RunnableItem)<-[:USERRUN]-(u:UserItem) WHERE ID(u) = $id AND n.provenance = FALSE RETURN n"
        return NodeItem.matchItems(cypher, id=user_id)
        
    def invoke_module(self, name, package):
        if not name:
            raise ValueError("No function name for module")
        module = ModuleItem(name=name, package=package)
        graph().push(module)

        item = ModuleInvocationItem(module=module)
        graph().push(item)
        item.runs.add(self)
        self.modules.add(item)

        graph().push(self)
        return item
    
    @staticmethod
    def create(user, workflow, script, provenance, args):
        item = RunnableItem(name=workflow.name, script=script, provenance=provenance, args=args)
        graph().push(item)

        user.runs.add(item)
        graph().push(user)
        workflow.runs.add(item)
        graph().push(workflow)

        graph().pull(item)
        return item

    @staticmethod
    def get(**kwargs):
        return NodeItem.get_with_and(RunnableItem, **kwargs)

    @staticmethod
    def load_if(condition = None):
        pass
    
    def update_cpu_memory(self):
        self.cpu_run = psutil.cpu_percent()
        self.memory_run = (psutil.virtual_memory()[2])/bytes_in_gb
        
    def set_status(self, value, update = True):
        self.status = value
        
        if value == Status.STARTED:
            self.started_on = neotime.DateTime.utc_now()
            self.update_cpu_memory()
    
        if value == Status.SUCCESS or value == Status.FAILURE or value == Status.REVOKED:
            self.duration = neotime.DateTime.utc_now() - self.started_on
            self.update_cpu_memory()
        
        if update:
            self.update()
        
    @property        
    def completed(self):
        return self.status == Status.SUCCESS or self.status == Status.FAILURE or self.status == Status.REVOKED
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'user_id': self.user_id,
            'workflow_id': self.workflow_id,
            'celery_id': self.celery_id,
            'memory': self.memory_run,
            'cpu': self.cpu_run,
            'out': self.out,
            'error': self.error,
            'view': self.view,
#            'script': self.script,
            'status': self.status,
            'duration': "{0:.3f}".format(neotime_duration_to_s(self.duration)),
            'args': str(self.args),
            'name': self.name
            })
        return j
       
    def nodes_by_property(self, key = None, value = None, order_by = None):
        moduleItems = []
        cypher = ''
        if not key:
            if not value:
                cypher = "MATCH(n) WHERE ID(n)={0} AND t.name = {1} return t".format(self._id, key) if key else "MATCH(n)-[:MODULEINVOCATION]->(t) WHERE ID(n)={0} return t".format(self._id)
        c = graph().run(cypher)
        for i in c:
            for _, v in i.items():
                moduleItems.append(ModuleInvocationItem.load_from_node(v))
        return moduleItems
    
    def to_json_tooltip(self):
        error = ""
        if error:
            error = (self._error[:60] + '...') if len(self.error) > 60 else self.error
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status,
            'err': error,
            'duration': "{0:.3f}".format(neotime_duration_to_s(self.duration)),
            'created_on': neotime2StrfTime(self.created_on),
            'modified_on': neotime2StrfTime(self.modified_on)
        }
        
    def to_json_log(self):
        log = []
        
        for module in self.modules:
            log.append(module.to_json_log())

        return {
            'id': self.id,
            'script': self.script,
            'status': self.status,
            'out': self.out,
            'err': self.error,
            'duration': "{0:.3f}".format(neotime_duration_to_s(self.duration)),
            'log': log
        }
        
    def to_json_info(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'modified_on': neotime2StrfTime(self.modified_on),
            'status': self.status
        }
        
class ModuleInvocationItem(NodeItem):
    runs = RelatedFrom(RunnableItem, "RUN2INVOC")
    inputs = RelatedFrom(ValueItem, "INPUT")
    outputs = RelatedTo(ValueItem, "OUTPUT")
    logs = RelatedTo("TaskLogItem", "INVOCLOG", "id(b)")
    modules = RelatedFrom(ModuleItem, "MODULE2INVOC")
    
    status = Property("status", Status.RECEIVED)
    
    cpu_init = Property("cpu_init", psutil.cpu_percent())
    memory_init = Property("memory_init", (psutil.virtual_memory()[2])/bytes_in_gb)
    
    cpu_run = Property("cpu_run", 0)
    memory_run = Property("memory_run", 0)
    
    started_on = Property("started_on", neotime.DateTime.min)
    duration = Property("duration", neotime.Duration())
    
    def __init__(self, **kwargs):
        module = kwargs.pop("module", None)
        super(ModuleInvocationItem, self).__init__(**kwargs)
        if module:
            self.modules.add(module)
    
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'RUN-CREATE',
            'name':self.name,
            'memory': str(self.memory_run),
            'cpu': str(self.cpu_run),
            'status': self.status           
        })
        
        return j 

    @property
    def name(self):
        modules = list(self.modules)
        return modules[0].name if modules else ""
        
    def prop_from_node(self, node):
        NodeItem.prop_from_node(self, node, "name", "status")
        self.status = node["status"]
        return self
    
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
        if module_id:
            return ModuleInvocationItem.match(graph(), module_id).first()
        elif name:
            if not package:
                pkg_func = name.split(".")
                if len(pkg_func) > 1:
                    name = pkg_func[-1]
                    package = ".".join(pkg_func[0:-1])
                else:
                    return ModuleInvocationItem.match(graph()).where("_.name='{0}'".format(name)).first()
            
            return ModuleInvocationItem.match(graph()).where("_.name='{0}' AND _.package='{1}'".format(name, package)).first()
        
    def start(self):
        self.status = Status.STARTED
        self.started_on = neotime.DateTime.utc_now()
        
        self.duration = neotime.Duration()
        self.memory_run = (psutil.virtual_memory()[2])/bytes_in_gb
        self.cpu_run = psutil.cpu_percent()
                    
        self.add_log(Status.STARTED, LogType.INFO)
        graph().push(self)
    
    def succeeded(self):
        self.status = Status.SUCCESS
        self.add_log(Status.SUCCESS, LogType.INFO)
        self.modified_on = neotime.DateTime.utc_now()
        self.duration = neotime.DateTime.utc_now() - self.started_on
        
        graph().push(self)
    
    def failed(self, log = "Task Failed."):
        self.status = Status.FAILURE
        self.add_log(log, LogType.INFO)
        self.modified_on = datetime.utcnow()
        self.duration = neotime.DateTime.utc_now() - self.started_on
        
        graph().push(self)
                    
    def add_log(self, log, logtype =  LogType.ERROR):
        item = TaskLogItem(text = log, type=logtype)
        graph().push(item)
        self.logs.add(item)
        return item
    
    def graph(self):
        pass
    
    def add_arg(self, datatype, value):
        if isinstance(value, ValueItem):
            self.inputs.add(value)
        else:
            for data in self.inputs:
                if data.datatype == datatype and data.value == value:
                    value = data
                    break
            if not value:    
                value = ValueItem.get_by_type_value(datatype, value)
                if not value:
                    data = ValueItem(value, datatype)
                    graph().push(data)
                self.inputs.add(data)

        graph().push(self)
        
        return value
    
    def add_input(self, user_id, datatype, value, rights, **kwargs):
        for data in self.inputs:
            if data.datatype == datatype and data.value == value:
                return data.allocate_for_user(user_id, rights)
                            
        data = ValueItem.get_by_type_value(datatype, value)
        if not data:
            kwargs.update({'value': value, 'type': datatype})
            data = ValueItem(**kwargs) #  data = ValueItem(str(value), datatype)
            graph().push(data)
        
        data.allocate_for_user(user_id, rights)
        
        self.inputs.add(data)
        graph().push(self)
        
        return data
    
    def add_outputs(self, dataAndType):
        runitem = list(self.runs)[0]
        
        result = ()        
        for d in dataAndType:
            data = None
            if not isinstance(d[1], ValueItem):
                data = ValueItem.get_by_type_value(d[0], d[1])
                if not data:
                    data = ValueItem(name=d[2] if len(d) > 2 else '', value=str(d[1]), type=d[0], task_id = self.id, job_id = runitem.id, workflow_id = runitem.workflow_id)
                    data.allocate_for_user(runitem.user_id, AccessRights.Owner)                    
                    graph().push(data)
                else:
                    data.allocate_for_user(runitem.user_id, AccessRights.Write)
                
            self.outputs.add(data)
            result += (d[1],)
        
        graph().push(self)
        
        return result
    
    def to_json_log(self):
        
        data = [{ "datatype": data.type, "data": data.value} for data in self.outputs]
            
        return { 
            'name': self.name if self.name else "", 
            'status': self.status,
            'data': data
        }
        
class TaskLogItem(NodeItem):
    type = Property("type")
    text = Property("text")
    
    log = RelatedFrom(ModuleInvocationItem)
    
    def __init__(self, **kwargs):
        self.type = kwargs.pop("type", LogType.ERROR)
        self.text = kwargs.pop("text", "")

        super(TaskLogItem, self).__init__(**kwargs)
       
    def json(self):
        j = NodeItem.json(self)
        j.update({
            'event': 'LOG-CREATE',
            'type': self.type,
            'log': self.text
            })
        
        return j
    
    @staticmethod
    def load(task_id):
        return TaskLogItem.match(graph(), task_id).first()
    
    def updateTime(self):
        self.modified_on = datetime.utcnow()
        graph().push(self)