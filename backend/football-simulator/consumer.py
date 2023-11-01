"""Consumes stream for printing all messages to the console.
"""

from argparse import ArgumentParser, FileType
from configparser import ConfigParser
import json
import sys
from confluent_kafka import Consumer, KafkaError, KafkaException


def msg_process(msg):
    # Print the current time and the message.
    val = msg.value()
    game_time = msg.key()
    dval = json.loads(val)
    print(game_time, dval)


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('topic', type=str,
                        help='Name of the Kafka topic to stream.')
    args = parser.parse_args()
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    consumer = Consumer(config)

    running = True

    try:
        while running:
            consumer.subscribe([args.topic])

            msg = consumer.poll(1)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error().code() == KafkaError.UNKNOWN_TOPIC_OR_PART:
                    sys.stderr.write('Topic unknown, creating %s topic\n' %
                                     (args.topic))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


if __name__ == "__main__":
    main()