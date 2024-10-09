import csv
import os
import re
from datetime import datetime

import praw
from dotenv import load_dotenv

# Load Reddit API environment variables.
load_dotenv()

# Initialize Reddit API using environment variables.
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
)


# Fetch a given Reddit thread by thread id.
def fetch_reddit_thread(thread_id):
    submission = reddit.submission(id=thread_id)
    submission.comments.replace_more(limit=None)
    comments = submission.comments.list()

    return submission, comments


# Clean titles for csv filenames.
def clean_thread_title(title):
    title = title.lower()
    title = re.sub(r"[^\w\s-]", "", title)
    title = re.sub(r"\s+", "-", title)

    return title


# Write thread metadata to csv.
def write_to_csv(submission, comments, thread_id):
    clean_title = clean_thread_title(submission.title)
    csv_filename = f"reddit-{thread_id}--{clean_title}.csv"

    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "timestamp",
                "thread_id",
                "thread_title",
                "thread_submitter",
                "thread_body",
                "thread_timestamp",
                "comment_id",
                "comment_username",
                "comment_body",
                "comment_reply_to_id",
            ]
        )

        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                submission.id,
                submission.title,
                (submission.author.name if submission.author else "Deleted"),
                submission.selftext,
                datetime.fromtimestamp(submission.created_utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "",
                "",
                "",
                "",
            ]
        )

        for comment in comments:
            writer.writerow(
                [
                    datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                    submission.id,
                    "",
                    "",
                    "",
                    "",
                    comment.id,
                    (comment.author.name if comment.author else "Deleted"),
                    comment.body,
                    (
                        comment.parent_id.split("_")[1]
                        if comment.parent_id != submission.id
                        else ""
                    ),
                ]
            )

    print(f"CSV saved as {csv_filename}")
