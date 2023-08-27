import multiprocessing
import queue


class CommandProcessor:
    def process_command(self, command):
        # Process the command
        print(f"Processing command: {command}")


class KafkaConsumerManager:
    def __init__(self, queue):
        self.queue = queue

    def consume(self):
        # Simulate Kafka message consumption
        for message in range(10):
            self.queue.put(f"Command {message}")


def message_worker(queue, command_processor):
    while True:
        message = queue.get()
        if message is None:
            break
        command_processor.process_command(message)
        queue.task_done()


def main():
    num_consumers = 2

    queue = multiprocessing.JoinableQueue()
    command_processor = CommandProcessor()
    kafka_consumer_manager = KafkaConsumerManager(queue)

    consumers = []
    for _ in range(num_consumers):
        consumer = multiprocessing.Process(target=kafka_consumer_manager.consume)
        consumers.append(consumer)
        consumer.start()

    workers = []
    for _ in range(num_consumers):
        worker = multiprocessing.Process(
            target=message_worker, args=(queue, command_processor)
        )
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
