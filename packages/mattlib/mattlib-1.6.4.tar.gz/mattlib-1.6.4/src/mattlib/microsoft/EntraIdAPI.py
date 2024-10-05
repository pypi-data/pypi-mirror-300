from .BaseMicrosoftAPI import BaseMicrosoftAPI
from datetime import datetime, timedelta

class EntraIdAPI(BaseMicrosoftAPI):
    def connect(self, tenant_ID, app_ID, secret_key):
       super().connect(tenant_ID, app_ID, secret_key,
                        'https://graph.microsoft.com/.default')
       self.subscriptions = None
       self.resource_groups = None
       self.servers = None

    def listAppsDisplayName(self):
        now = datetime.utcnow()
        set_end_date = now - timedelta(days=30)
        start_date = set_end_date.isoformat() + 'Z'
        end_date = now.isoformat() + 'Z'
        params = {
        '$filter': f"createdDateTime ge {start_date} and createdDateTime le {end_date}",
        '$select': 'appDisplayName,createdDateTime',
        '$orderby': 'appDisplayName'
        }
        url = 'https://graph.microsoft.com/v1.0/auditLogs/signIns'
        response = self.call_api(url,params,ignore=False)
        return response
    
    def listAuditLogsPerMonth(self):
        now = datetime.utcnow()
        set_end_date = now - timedelta(days=30)
        start_date = set_end_date.isoformat() + 'Z'
        end_date = now.isoformat() + 'Z'
        params = {
        '$filter': f"createdDateTime ge {start_date} and createdDateTime le {end_date}",
        }
        url = 'https://graph.microsoft.com/v1.0/auditLogs/signIns'
        response = self.call_api(url,params,ignore=False)
        return response
    
    def listAuditLogsPerDay(self):
        now = datetime.utcnow()
        set_end_date = now - timedelta(days=2)
        start_date = set_end_date.isoformat() + 'Z'
        end_date = now.isoformat() + 'Z'
        params = {
        '$filter': f"createdDateTime ge {start_date} and createdDateTime le {end_date}",
        }
        url = 'https://graph.microsoft.com/v1.0/auditLogs/signIns'
        response = self.call_api(url,params,ignore=True)
        return response

    def methods(self):
        methods = [
            {
                'method_name': 'listAppsDisplayName',
                'method': self.listAppsDisplayName,
                'format': 'json'
            },
            {
                'method_name': 'listAuditLogsPerMonth',
                'method': self.listAuditLogsPerMonth,
                'format': 'json'
            },
            {
                'method_name': 'listAuditLogsPerDay',
                'method': self.listAuditLogsPerDay,
                'format': 'json'
            }
        ]
        return methods
