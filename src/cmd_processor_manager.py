from cmd_processor import CmdProcessor
from multiprocessing import JoinableQueue


class CmdProcessorManager:
    def __init__(self, cmd_processor: CmdProcessor, queue: JoinableQueue):
        self._cmd_processor = cmd_processor
        self._queue = queue

    def manage(self):
        while True:
            msg = self._queue.get()
            if msg is None:
                break

            print(f"Processing message {msg.idempotency_id}")
            self._cmd_processor.process(msg)
            self._queue.task_done()
