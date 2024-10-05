from contextlib import contextmanager
from dagster import AssetExecutionContext, ConfigurableResource
from dagster_shell import execute_shell_command
from pydantic import Field
from enum import Enum
import tempfile

class CloudqueryCommand(Enum):
    SYNC = "sync"
    MIGRATE = "migrate"


class CloudqueryResource(ConfigurableResource):
    """Resource for interacting with the Cloudquery CLI."""

    path_to_cloudquery_binary: str = Field(
        description=(
            "Path to the Cloudquery binary. Defaults to 'cloudquery' if not set."
        ),
        default="cloudquery",
    )

    @classmethod
    def _is_dagster_maintained(cls) -> bool:
        return False

    def migrate(self, context: AssetExecutionContext, *, spec_path: str = "", spec_blob: str = ""):
        self._run(CloudqueryCommand.MIGRATE, context, spec_path=spec_path, spec_blob=spec_blob)

    def sync(self, context: AssetExecutionContext, *, spec_path: str = "", spec_blob: str = ""):
        self._run(CloudqueryCommand.SYNC, context, spec_path=spec_path, spec_blob=spec_blob)

    def _resolve_cloudquery_path(self) -> str:
        return self.path_to_cloudquery_binary

    def _resolve_spec(self, *, spec_path: str = "", spec_blob: str = "") -> str:
        if spec_path and spec_blob:
            raise ValueError("Supply either `spec_path` or `spec_blob`, not both.")
        if not spec_path and not spec_blob:
            raise ValueError("You must supply either `spec_path` or `spec_blob`.")
        if spec_path:
            with open(spec_path, "r") as file:
                return file.read()
        if spec_blob:
            return spec_blob

    @contextmanager
    def _make_spec_file(self, *, spec_path: str = "", spec_blob: str = ""):
        spec = self._resolve_spec(spec_path=spec_path, spec_blob=spec_blob)
        with tempfile.NamedTemporaryFile(mode='w+t') as temp_file:
            temp_file.write(spec)
            temp_file.flush()
            yield temp_file.name

    def _run(self, command: CloudqueryCommand, context: AssetExecutionContext, *, spec_path: str = "", spec_blob: str = ""):
        cloudquery_path = self._resolve_cloudquery_path()

        with self._make_spec_file(spec_path=spec_path, spec_blob=spec_blob) as spec_file:
            ret = execute_shell_command(f"{cloudquery_path} {command.value} --log-console {spec_file}", output_logging="STREAM", log=context.log)
            if ret[1] != 0:
                raise Exception(f"cloudquery command failed with: {ret}")
