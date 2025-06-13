from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from typing import List

from .config import load_config
from .database import SessionLocal, Tweet, User, init_db
from .twitter_client import TwitterClient


def save_users(db_session, users: List[dict]) -> None:
    for user_data in users:
        user = db_session.query(User).filter_by(user_id=user_data["user_id"]).first()
        if not user:
            user = User(
                user_id=user_data["user_id"],
                name=user_data["name"],
                handle=user_data["handle"],
                description=user_data.get("description"),
                created_at=datetime.strptime(user_data["created_at"], "%a %b %d %H:%M:%S %z %Y")
                if user_data.get("created_at")
                else None,
            )
            db_session.add(user)
    db_session.commit()


def save_tweets(db_session, user: User, tweets: List[dict]) -> None:
    for tweet_data in tweets:
        if db_session.query(Tweet).filter_by(tweet_id=tweet_data["tweet_id"]).first():
            continue
        created_at = datetime.strptime(tweet_data["created_at"], "%a %b %d %H:%M:%S %z %Y")
        tweet = Tweet(
            tweet_id=tweet_data["tweet_id"],
            user=user,
            text=tweet_data["text"],
            tweet_created_at=created_at,
        )
        db_session.add(tweet)
    user.last_checked_at = datetime.utcnow()
    db_session.commit()


def fetch_following(client: TwitterClient) -> None:
    init_db()
    session = SessionLocal()
    cursor = None
    while True:
        data = client.get_following(count=20, cursor=cursor)
        users = TwitterClient.parse_users(data)
        save_users(session, users)
        cursor = None
        instructions = (
            data.get("data", {})
            .get("user", {})
            .get("result", {})
            .get("timeline", {})
            .get("timeline", {})
            .get("instructions", [])
        )
        for instruction in instructions:
            if instruction.get("type") == "TimelineAddEntries":
                for entry in instruction.get("entries", []):
                    if (
                        entry.get("content", {}).get("entryType") == "TimelineTimelineCursor"
                        and entry.get("content", {}).get("cursorType") == "Bottom"
                    ):
                        cursor = entry.get("content", {}).get("value")
        if not cursor:
            break


def fetch_recent_tweets(client: TwitterClient) -> None:
    init_db()
    session = SessionLocal()
    one_month_ago = datetime.utcnow() - timedelta(days=30)
    users = session.query(User).all()
    for user in users:
        if user.last_checked_at and user.last_checked_at > datetime.utcnow() - timedelta(days=1):
            continue
        data = client.get_user_tweets(target_user_id=user.user_id, count=100)
        tweets = client.parse_tweets(data)
        tweets_filtered = [
            t for t in tweets if datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S %z %Y") > one_month_ago
        ]
        save_tweets(session, user, tweets_filtered)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="finTweet data collector")
    parser.add_argument("--follow", action="store_true", help="Fetch following list")
    parser.add_argument("--tweets", action="store_true", help="Fetch recent tweets")
    args = parser.parse_args()

    cfg = load_config()
    client = TwitterClient(cfg)

    if args.follow:
        fetch_following(client)
    if args.tweets:
        fetch_recent_tweets(client)
