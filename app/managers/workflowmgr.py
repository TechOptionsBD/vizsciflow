import json
from ..models import Workflow, WorkflowAccess, Service
from config import Config
from sqlalchemy import and_, or_
from ..common import AccessType
from ..graphutil import WorkflowItem
from .usermgr import usermanager

class GraphWorkflowManager():

    @staticmethod
    def first(**kwargs):
        return WorkflowItem.first(**kwargs)

    @staticmethod
    def get(**kwargs):
        return WorkflowItem.get(**kwargs)

    @staticmethod
    def get_workflows_as_list(access, user_id, *args):
        return WorkflowItem.get_workflows_as_list(access, user_id, *args)
    
    @staticmethod
    def create(**kwargs):
        return WorkflowItem.Create(**kwargs)

    @staticmethod
    def get_or_404(id):
        return WorkflowItem.first(id=id)

    @staticmethod
    def insert_workflows(path):
        return WorkflowItem.insert_workflows(path)

class DBWorkflowManager():
    @staticmethod
    def first(**kwargs):
        return Workflow.query.filter_by(**kwargs).first()

    @staticmethod
    def get(**kwargs):
        return Workflow.query.filter_by(**kwargs)
    
    @staticmethod
    def get_or_404(id):
        return Workflow.query.get(id)

    @staticmethod
    def create(**kwargs):
        return Workflow.create(**kwargs)

    @staticmethod
    def remove(user_id, workflow_id):
        Workflow.remove(user_id, workflow_id)

    @staticmethod
    def get_workflows_as_list(access, user_id, *args):
        terms = ["tag='{0}'".format(v) for v in args]
        if access == 0 or access == 3:
            return Workflow.query.filter(Workflow.public == True).filter(or_(*terms))
        if access == 1 or access == 3:
            return Workflow.query.filter(Workflow.public != True).filter(Workflow.accesses.any(and_(WorkflowAccess.user_id == user_id, Workflow.user_id != user_id))).filter(or_(*terms)) # TODO: Do we need or_ operator here? 
        if access == 2 or access == 3:
            return Workflow.query.filter(and_(Workflow.public != True, Workflow.user_id == user_id)).filter(or_(*terms))

class WorkflowManager():
    def __init__(self):
        if Config.DATA_MODE == 0:
            self.persistance = DBWorkflowManager()
        else:
            self.persistance = GraphWorkflowManager()
    
    def create(self, **kwargs):
        return self.persistance.create(**kwargs)

    def first(self, **kwargs):
        return self.persistance.first(**kwargs)
    
    def get(self, **kwargs):
        return self.persistance.get(**kwargs)
    
    def get_or_404(self, id):
        return self.persistance.get_or_404(id)
    
    def remove(self, user_id, workflow_id):
        self.persistance.remove(user_id, workflow_id)
    
    @staticmethod
    def get_workflows_info(workflows, access, username):
        workflow_list = []
        for workflow in workflows:
            json_info = workflow.to_json()
            json_info["access"] = access
            json_info["is_owner"] = json_info["user"] == username
            workflow_list.append(json_info)
        return workflow_list

    def get_workflows_as_list(self, access, user, *args):
        workflows = self.persistance.get_workflows_as_list(access, user.id, *args)
        samples = []
        if access == 0 or access == 3:
            samples = WorkflowManager.get_workflows_info(workflows, AccessType.PUBLIC, user.username)
        if access == 1 or access == 3:
            samples.extend(WorkflowManager.get_workflows_info(workflows, AccessType.SHARED, user.username))
        if access == 2 or access == 3:
            samples.extend(WorkflowManager.get_workflows_info(workflows, AccessType.PRIVATE, user.username))
        
        return json.dumps({'samples': samples})    

    @staticmethod
    def get_a_workflow_details(workflow, props):
        json = {}
        for name in props:
            data = getattr(workflow, name)
            json.update({name:data})
        return json
        
    @staticmethod
    def get_workflow_details(workflows, props):
        return [WorkflowManager.get_a_workflow_details(w) for w in workflows]

    #written_by: Moksedul Islam
    def get_workflow_list(self, user_id, props, access):
        workflows = self.persistance.get_workflows_as_list(access, user_id)
        workflow_list = []
        if access == 0 or access == 3:
            workflow_list.extend(WorkflowManager.get_workflow_details(workflows, props))
        if access == 1 or access == 3:
            workflow_list.extend(WorkflowManager.get_workflow_details(workflows, props))
        if access == 2 or access == 3:
            workflow_list.extend(WorkflowManager.get_workflow_details(workflows, props))
        
        return json.dumps(workflow_list)
    
    def insert_workflows(self, path):
        return self.persistance.insert_workflows(path)

        
workflowmanager = WorkflowManager()
