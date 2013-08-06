__version__ = '0.0.1'

def version():
    return __version__

def version_context_processor():
    return dict(version=__version__)
