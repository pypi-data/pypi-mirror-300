from raft.tasks import task
from .base import AzureTask
from ..base.utils import get_context_value
from ..base.utils import notice, notice_end


@task(help=dict(perms='read, write, or manage'), iterable=['perms'], klass=AzureTask)
def grant_access_to_site(ctx, site_name, app_name, perms=None, **kwargs):
    """
    grants the app with name app_name read and write permissions to the site_name sharepoint site

    this convocation is useful when you have created an azure application
    registration with api permission Sites.Selected and need to authorize
    the application to connect to a particular sharepoint site.
    """
    from affliction.graph_client import SynchronousGraphClient
    notice('tenant_name')
    perms = perms or [ 'read', 'write' ]
    creds = kwargs['creds']
    tenant_id = get_context_value(ctx, 'azure.tenant_id')
    api = SynchronousGraphClient(tenant_id, creds=creds)
    domains = api.initial_domain()
    initial_domain = domains['id']
    notice_end(initial_domain)
    notice('looking up application')
    hostname = initial_domain.replace('onmicrosoft', 'sharepoint')
    apps = api.search_apps(app_name)
    app_id = None
    app_name = app_name.lower()
    for x in apps:
        if x['displayName'].lower() == app_name:
            app_id = x['id']
            notice_end(f'{app_id}')
            break
    if not app_id:
        notice_end(False)
        notice('looking up service principal')
        result = api.search_service_principals(app_name)
        for x in result:
            if x['displayName'].lower() == app_name:
                app_id = x['appId']
                break
        if not app_id:
            notice_end(False)
            return
        notice_end(f'{app_id}')
    notice('site id')
    result = api.get_sharepoint_site(hostname, site_name)
    site_id = result['id']
    notice_end(site_id)
    notice('checking existing permissions')
    data = api.get_sharepoint_site_permissions(site_id)
    app_id_exists = False
    existing_permission_id = None
    existing_perms = []
    for x in data['value']:
        permission_id = x['id']
        data = api.get_sharepoint_site_permission(site_id, permission_id)
        roles = data['roles']
        identities = data['grantedToIdentitiesV2']
        for i in identities:
            app = i.get('application')
            if app and app['id'] == app_id:
                app_id_exists = True
                existing_permission_id = permission_id
                existing_perms = roles
                break
        if roles == perms and app_id_exists:
            notice_end('permission already granted')
            return
    notice_end(existing_permission_id is not None)
    if existing_permission_id:
        notice('updating existing permission')
        updated_perms = set(existing_perms)
        for perm in perms:
            updated_perms.add(perm)
        response = api.update_sharepoint_site_permission(
            site_id,
            existing_permission_id,
            roles=list(updated_perms),
            raw=True)
        notice_end(response.ok)
    else:
        notice('creating new permission')
        response = api.create_sharepoint_site_permission(
            site_id, app_id, app_name, perms, raw=True)
        notice_end(response.ok)
