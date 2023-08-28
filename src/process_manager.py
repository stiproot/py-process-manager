from cmd_processor import CmdProcessor
from process_cmd import ProcessCmd
from cmd_provider import CmdProvider, CmdProviderManager
from kafka_consumer_emulator import KafkaConsumerEmulator
from multiprocessing import JoinableQueue, Process
from process_metadata_service import ProcessMetadataService


class ProcessManager:
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


# def message_worker(queue, cmd_processor: CmdProcessor):
#     while True:
#         msg = queue.get()
#         if msg is None:
#             break

#         print(f"Processing message {msg.idempotency_id}")
#         cmd_processor.process(msg)
#         queue.task_done()


def main():
    num_consumers = 2

    queue = JoinableQueue()
    cmd_processor = CmdProcessor()
    cmd_provider = KafkaConsumerEmulator()
    cmd_provider_manager = CmdProviderManager(cmd_provider, queue)
    process_manager = ProcessManager(cmd_processor, queue)

    providers = []

    for _ in range(num_consumers):
        provider = Process(target=cmd_provider_manager.manage)
        providers.append(provider)
        provider.start()

    workers = []

    for _ in range(num_consumers):
        # worker = Process(target=message_worker, args=(queue, cmd_processor))
        worker = Process(target=process_manager.manage)
        workers.append(worker)
        worker.start()

    for provider in providers:
        provider.join()

    for _ in range(num_consumers):
        queue.put(None)  # Signal workers to exit

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()
