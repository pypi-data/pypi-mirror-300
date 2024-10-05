from dagster._core.libraries import DagsterLibraryRegistry
from .resource import CloudqueryResource as CloudqueryResource
from .version import __version__

DagsterLibraryRegistry.register("cloudquery", __version__)
