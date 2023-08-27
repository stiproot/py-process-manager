from cmd_processor import CmdProcessor
from process_cmd import ProcessCmd
from cmd_provider import CmdProvider
from kafka_consumer_emulator import KafkaConsumerEmulator
from multiprocessing import JoinableQueue, Process
from process_metadata_service import ProcessMetadataService


class ProcessManager:
    def __init__(self, cmd_processor: CmdProcessor, cmd_provider: CmdProvider):
        self._queue = JoinableQueue()
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def join(self):
        pass


def message_worker(queue, cmd_processor: CmdProcessor):
    while True:
        pid = ProcessMetadataService().pid()
        print(f"message_worker() / pid:{pid}")
        msg = queue.get()
        if msg is None:
            break
        # cmd = ProcessCmd()
        print(f"Processing message {msg.idempotency_id}")
        cmd_processor.process(msg)
        queue.task_done()


def main():
    num_consumers = 2

    queue = JoinableQueue()
    cmd_processor = CmdProcessor()
    consumer_manager = KafkaConsumerEmulator(queue)

    consumers = []

    for _ in range(num_consumers):
        consumer = Process(target=consumer_manager.consume)
        consumers.append(consumer)
        consumer.start()

    workers = []

    for _ in range(num_consumers):
        worker = Process(target=message_worker, args=(queue, cmd_processor))
        workers.append(worker)
        worker.start()

    for consumer in consumers:
        consumer.join()

    for _ in range(num_consumers):
        queue.put(None)  # Signal workers to exit

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
