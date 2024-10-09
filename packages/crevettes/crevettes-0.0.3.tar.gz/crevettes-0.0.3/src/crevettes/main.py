import sys

from crevettes import harvester


def main():
    if len(sys.argv) != 2:
        print("Usage: crevettes thread_id")
        sys.exit(1)

    # Get thread ID from command-line argument.
    thread_id = sys.argv[1]

    # Fetch thread and comments.
    submission, comments = harvester.fetch_reddit_thread(thread_id)

    # Write thread metadata data to csv.
    harvester.write_to_csv(submission, comments, thread_id)


if __name__ == "__main__":
    main()
