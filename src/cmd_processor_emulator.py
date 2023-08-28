import time
from process_cmd import ProcessCmd
from process_metadata_service import ProcessMetadataService
from cmd_processor import CmdProcessor


class CmdProcessorEmulator(CmdProcessor):
    def process(self, cmd: ProcessCmd) -> None:
        print(
            "process()",
            "start",
            f"pid:{ProcessMetadataService().pid()}",
            f"cmd:{cmd.idempotency_id}",
        )

        time.sleep(2)

        print(
            "process()",
            "end",
            f"pid:{ProcessMetadataService().pid()}",
            f"cmd:{cmd.idempotency_id}",
        )
