from pkg_resources import resource_filename

def get_resource_path(resource_name):
    return resource_filename(__name__, 'resources/{}'.format(resource_name))