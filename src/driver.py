from cmd_provider import CmdProviderManager
from kafka_consumer_emulator import KafkaConsumerEmulator
from cmd_processor_emulator import CmdProcessorEmulator
from multiprocessing import JoinableQueue
from cmd_processor_manager import CmdProcessorManager
from process_configuration import ProcessConfiguration
from process_manager import ProcessManager


def main():
    NUM_CONSUMERS = 2

    config = ProcessConfiguration(
        num_worker_processes=NUM_CONSUMERS, num_cmd_provider_processes=NUM_CONSUMERS
    )
    queue = JoinableQueue()
    cmd_processor = CmdProcessorEmulator()
    cmd_provider = KafkaConsumerEmulator()

    cmd_provider_manager = CmdProviderManager(cmd_provider, queue)
    cmd_processor_manager = CmdProcessorManager(cmd_processor, queue)

    process_manager = ProcessManager(
        config, cmd_processor_manager, cmd_provider_manager
    )

    process_manager.manage()


if __name__ == "__main__":
    main()
