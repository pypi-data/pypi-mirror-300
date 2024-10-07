from raft.collection import Collection
from .subscription_tasks import subscriptions
from .resource_group_tasks import resource_groups
from .resource_group_tasks import providers
from .ldap_tasks import update_ldaps_cert
from .application_tasks import apps, register_app
from .group_tasks import groups
from .sharepoint_tasks import grant_access_to_site
from .whoami import whoami


azure_tasks = Collection()
azure_tasks.add_task(subscriptions)
azure_tasks.add_task(resource_groups)
azure_tasks.add_task(providers)
azure_tasks.add_task(update_ldaps_cert)
azure_tasks.add_task(apps)
azure_tasks.add_task(groups)
azure_tasks.add_task(grant_access_to_site)
azure_tasks.add_task(whoami)
azure_tasks.add_task(register_app)
