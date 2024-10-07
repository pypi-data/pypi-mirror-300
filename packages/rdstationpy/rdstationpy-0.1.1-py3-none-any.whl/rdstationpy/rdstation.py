from rdstationpy.api_client import ApiClient
from rdstationpy.services.activities import ActivitiesService
from rdstationpy.services.campaigns import CampaignsService
from rdstationpy.services.contacts import ContactsService
from rdstationpy.services.custom_fields import CustomFieldsService
from rdstationpy.services.deal_lost_reasons import DealLostReasonsService
from rdstationpy.services.deal_pipelines import DealPipelines
from rdstationpy.services.deal_sources import DealSourcesService
from rdstationpy.services.deals import DealsService
from rdstationpy.services.organizations import OrganizationsService
from rdstationpy.services.products import ProductsService
from rdstationpy.services.tasks import TasksService
from rdstationpy.services.teams import TeamsService
from rdstationpy.services.users import UsersService
from rdstationpy.services.webhooks import WebhooksService


class RDStation:
    def __init__(self, api_key, url="https://crm.rdstation.com/api/v1", config=None):
        self.api_client = ApiClient(api_key, url, config)

        self.activities = ActivitiesService(self.api_client)
        self.campaigns = CampaignsService(self.api_client)
        self.contacts = ContactsService(self.api_client)
        self.custom_fields = CustomFieldsService(self.api_client)
        self.deal_lost_reasons = DealLostReasonsService(self.api_client)
        self.deal_pipelines = DealPipelines(self.api_client)
        self.deal_sources = DealSourcesService(self.api_client)
        self.deals = DealsService(self.api_client)
        self.organizations = OrganizationsService(self.api_client)
        self.products = ProductsService(self.api_client)
        self.tasks = TasksService(self.api_client)
        self.teams = TeamsService(self.api_client)
        self.users = UsersService(self.api_client)
        self.webhooks = WebhooksService(self.api_client)
