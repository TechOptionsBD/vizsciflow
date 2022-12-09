import json
from app.managers.mgrutil import ManagerUtility
from app.objectmodel.common import AccessType

class WorkflowManager():
    def __init__(self):
        self.persistance = ManagerUtility.Manage('workflow')

    def create(self, **kwargs):
        return self.persistance.create(**kwargs)

    def update(self, **kwargs):
        return self.persistance.update(**kwargs)
    
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
        
        return samples

    @staticmethod
    def get_a_workflow_details(workflow, props):
        json = {}
        for name in props:
            data = getattr(workflow, name)
            json.update({name:data})
        return json
        
    @staticmethod
    def get_workflow_details(workflows, props):
        return [WorkflowManager.get_a_workflow_details(w, props) for w in workflows]

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

    def get_returns_json(self, workflow_id):
        return self.persistance.get_returns_json(workflow_id)        

workflowmanager = WorkflowManager()
