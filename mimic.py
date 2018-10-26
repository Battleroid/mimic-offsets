import sys
import textwrap
from argparse import ArgumentParser
from functools import partial

from kafka import KafkaConsumer, OffsetAndMetadata, TopicPartition


def main(topic, from_group, to_group, brokers, dry_run):
    """
    Mimic offsets for consumer group under topic to another consumer group.
    """

    def get_cons_offsets(topic, cons):
        """
        Get current committed consumer group offsets for topic.
        """
        partitions_for_topic = cons.partitions_for_topic(topic)
        partitions = [TopicPartition(topic, i) for i in partitions_for_topic]
        committed_offsets = {
            partition: OffsetAndMetadata(cons.committed(partition), None)
            for partition in partitions
        }
        return committed_offsets

    def report_offsets(offsets, group):
        """
        Pretty print our table of offsets.
        """
        indent = partial(textwrap.indent, prefix=' ' * 4)
        print(f'Topic status for "{topic}:{group}", with {len(offsets)} partitions:')
        print()
        print('       #  Current offset')
        for partition, offset in offsets.items():
            print(indent(f'{partition.partition:>4}: {offset.offset:<10}'))
        print()

    # Create consumer for originating group, get its offsets
    from_cons = KafkaConsumer(
        group_id=from_group,
        bootstrap_servers=brokers,
        enable_auto_commit=False
    )

    # What's going to happen?
    committed_offsets = get_cons_offsets(topic, from_cons)
    del from_cons
    report_offsets(committed_offsets, from_group)

    if dry_run:
        print('Dry run mode, exiting')
        sys.exit()

    # Setup the new consumer group with the right offsets, demonstrate changes
    to_cons = KafkaConsumer(
        group_id=to_group,
        bootstrap_servers=brokers,
        enable_auto_commit=False
    )
    to_cons.commit(committed_offsets)
    set_offsets = get_cons_offsets(topic, to_cons)
    del to_cons

    print('\nAfter offset mimic:\n')

    report_offsets(set_offsets, to_group)


if __name__ == '__main__':
    parser = ArgumentParser(description=main.__doc__)
    parser.add_argument('TOPIC', help='topic to inspect')
    parser.add_argument('FROM_GROUP', help='consumer group to get offsets from')
    parser.add_argument('TO_GROUP', help='consumer group to copy offsets to')
    parser.add_argument('--for-real', default=True, action='store_false', help='really mimic the offsets')
    parser.add_argument('-b', '--brokers', help='kafka brokers')
    args = parser.parse_args()
    topic, from_group, to_group = args.TOPIC, args.FROM_GROUP, args.TO_GROUP
    brokers = args.brokers
    dry_run = args.for_real
    main(topic, from_group, to_group, brokers, dry_run)
