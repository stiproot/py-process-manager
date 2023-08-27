# from multiprocessing import JoinableQueue, process
import multiprocessing as mp


class KafkaConsumerEmulator:
    def __init__(self, queue: mp.JoinableQueue):
        self._queue = queue

    def consume(self):
        current_process = mp.current_process()
        process_id = current_process.pid
        print("KafkaConsumerEmulator", "consume()", f"process: {process_id}")
        for message in range(10):
            self._queue.put(f"Command {message}")
