# from multiprocessing import JoinableQueue, process
from process_cmd import ProcessCmd
import multiprocessing as mp
from cmd_provider import CmdProvider


# class KafkaConsumerEmulator:
#     def __init__(self, queue: mp.JoinableQueue):
#         self._queue = queue

#     def consume(self):
#         current_process = mp.current_process()
#         process_id = current_process.pid
#         print("KafkaConsumerEmulator", "consume()", f"process: {process_id}")
#         for message in range(10):
#             # todo: push cmds...
#             # self._queue.put(f"Command {message}")
#             self._queue.put(ProcessCmd())


class KafkaConsumerEmulator(CmdProvider):
    def provide(self) -> [ProcessCmd]:
        return [ProcessCmd() for _ in range(10)]
