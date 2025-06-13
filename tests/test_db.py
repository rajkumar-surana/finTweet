import os
from datetime import datetime

from sqlalchemy.orm import sessionmaker

from fin_tweet.database import Base, Tweet, User, get_engine

TEST_DB_URL = "sqlite:///test_fin_tweet.db"


def setup_module(module):
    if os.path.exists("test_fin_tweet.db"):
        os.remove("test_fin_tweet.db")
    engine = get_engine(TEST_DB_URL)
    Base.metadata.create_all(bind=engine)
    module.Session = sessionmaker(bind=engine)


def teardown_module(module):
    if os.path.exists("test_fin_tweet.db"):
        os.remove("test_fin_tweet.db")


def test_insert_user_and_tweet():
    session = Session()
    user = User(user_id="123", name="Test", handle="test")
    session.add(user)
    session.commit()

    tweet = Tweet(tweet_id="abc", user=user, text="hello", tweet_created_at=datetime.utcnow())
    session.add(tweet)
    session.commit()

    assert session.query(User).count() == 1
    assert session.query(Tweet).count() == 1
    session.close()
