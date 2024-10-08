import importlib.metadata

def get_version(package_name):
    try:
        version = importlib.metadata.version(package_name)
        return version
    except importlib.metadata.PackageNotFoundError:
        return "develop"
