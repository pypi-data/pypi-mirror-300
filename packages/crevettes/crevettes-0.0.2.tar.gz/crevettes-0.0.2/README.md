# crevettes

A Python utility to capture a thread and commends for a given Reddit thread. This utility came out of a research need for the [Digital Feminist Network](https://digfemnet.org/).

## Requirements

* [praw](https://github.com/praw-dev/praw)
* [python-dotenv](https://github.com/theskumar/python-dotenv)

## Usage

```
crevettes thread_id
```

## Example

```
crevettes 1bq51lp
```

You will need a `.env` file populated with the following:

```
REDDIT_CLIENT_ID=YOUR_CLIENT_ID
REDDIT_CLIENT_SECRET=YOUR_CLIENT_SECRET
REDDIT_USER_AGENT=YOUR_USER_AGENT
```

## License

The Unlicense
