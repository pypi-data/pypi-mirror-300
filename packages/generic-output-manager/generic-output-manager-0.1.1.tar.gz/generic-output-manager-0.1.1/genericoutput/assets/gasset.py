from datetime import datetime
from ..storages.storage import Storage
from ..notifier import Notifier
import os
import uuid

class GAsset():

    storage = Storage()
    notifier = Notifier()

    def __init__(self, name, messageType, title=None, description=None, var=None, show=True) -> None:
        self.name = name
        self.key = name.lower().replace(" ", "-")
        self.messageType = messageType
        self.title = title
        self.description = description
        self.var = var
        self.created = datetime.now()
        self.modified = self.created
        self.show = show
        self.uuid = str(uuid.uuid4())

    def to_json(self):

        result = {
            "name": self.name,
            "key": self.key,
            "uuid": self.uuid,
            "messageType": self.messageType,
            "title": self.title,
            "description": self.description,
            "var": self.var,
            "created": str(self.created),
            "modified": str(datetime.now()),
            "show": self.show
        }

        if "BDA_ID" in os.environ:
            result['bdaId'] = os.environ.get('BDA_ID')

        if "SERVICE_ID" in os.environ:
            result['serviceId'] = os.environ.get('SERVICE_ID')

        if "ORGANIZATION_ID" in os.environ:
            result['organizationId'] = os.environ.get('ORGANIZATION_ID')
        
        if "OWNER_ID" in os.environ:
            result['ownerId'] = os.environ.get('OWNER_ID')

        if "EXECUTION_ID" in os.environ:
            result['executionId'] = os.environ.get('EXECUTION_ID')

        if "ACCESS_LEVEL" in os.environ:
            result['accessLevel'] = os.environ.get('ACCESS_LEVEL')

        if "EXECUTOR_ID" in os.environ:
            result['executorId'] = os.environ.get('EXECUTOR_ID')
        
        if "EXECUTOR_NAME" in os.environ:
            result['executorName'] = os.environ.get('EXECUTOR_NAME')
        
        if "EXECUTOR_ORG_ID" in os.environ:
            result['executorOrgId'] = os.environ.get('EXECUTOR_ORG_ID')
        
        if "EXECUTOR_ORG_NAME" in os.environ:
            result['executorOrgName'] = os.environ.get('EXECUTOR_ORG_NAME')

        return result
    
    def get_path(self):
        return None
    
    def send(self):
        self.path = self.storage.save(path=self.get_path(), metadata=self.to_json())
        self.notifier.something_has_changed(self.to_json())
