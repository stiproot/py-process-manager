from cmd_processor import CmdProcessor
from process_cmd import ProcessCmd
from cmd_provider import CmdProvider
from kafka_consumer_emulator import KafkaConsumerEmulator
from multiprocessing import JoinableQueue, Process
from process_metadata_service import ProcessMetadataService


def message_worker(queue, cmd_processor: CmdProcessor):
    while True:
        pid = ProcessMetadataService().pid()
        print(f"message_worker() / pid:{pid}")
        message = queue.get()
        print(f"Processing message {message}")
        if message is None:
            break
        cmd = ProcessCmd()
        cmd_processor.process(cmd)
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
