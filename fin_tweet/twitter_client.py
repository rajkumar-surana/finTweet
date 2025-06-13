from __future__ import annotations

import json
from datetime import datetime
from typing import Dict, List, Optional

import requests

from .config import load_config


class TwitterClient:
    """Simple wrapper around Twitter APIs used in this project."""

    def __init__(self, config: Optional[Dict[str, str]] = None):
        if config is None:
            config = load_config()
        self.bearer_token = config.get("bearer_token", "")
        self.csrf_token = config.get("csrf_token", "")
        self.cookies = config.get("cookies", "")
        self.user_id = config.get("user_id", "")
        self.session = requests.Session()

    def _auth_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.bearer_token}",
            "x-csrf-token": self.csrf_token,
            "content-type": "application/json",
            "user-agent": "finTweetBot/1.0",
            "cookie": self.cookies,
        }

    def get_following(self, count: int = 20, cursor: Optional[str] = None) -> Dict:
        url = "https://x.com/i/api/graphql/UEMg7scHEoC_FsYmXhkRkQ/Following"
        variables = {"userId": self.user_id, "count": count, "includePromotedContent": False}
        if cursor:
            variables["cursor"] = cursor
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps({"responsive_web_graphql_skip_user_profile_image_extensions_enabled": False}),
        }
        response = self.session.get(url, headers=self._auth_headers(), params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_user_tweets(self, target_user_id: str, count: int = 20) -> Dict:
        url = "https://x.com/i/api/graphql/2ItQrd86P8C0pDU6td3Z7Q/UserTweets"
        variables = {
            "userId": target_user_id,
            "count": count,
            "includePromotedContent": True,
            "withVoice": True,
        }
        params = {
            "variables": json.dumps(variables),
            "features": json.dumps({"responsive_web_graphql_skip_user_profile_image_extensions_enabled": False}),
            "fieldToggles": json.dumps({"withArticlePlainText": False}),
        }
        response = self.session.get(url, headers=self._auth_headers(), params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_tweets(data: Dict) -> List[Dict]:
        tweets: List[Dict] = []
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
                    content = (
                        entry.get("content", {})
                        .get("itemContent", {})
                        .get("tweet_results", {})
                        .get("result", {})
                    )
                    legacy = content.get("legacy", {})
                    tweet_text = legacy.get("full_text")
                    if tweet_text:
                        tweets.append(
                            {
                                "tweet_id": content.get("rest_id", ""),
                                "text": tweet_text,
                                "created_at": legacy.get("created_at"),
                            }
                        )
        return tweets

    @staticmethod
    def parse_users(data: Dict) -> List[Dict]:
        users: List[Dict] = []
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
                    content = (
                        entry.get("content", {})
                        .get("itemContent", {})
                        .get("user_results", {})
                        .get("result", {})
                    )
                    core = content.get("core", {})
                    legacy = content.get("legacy", {})
                    if not content.get("rest_id"):
                        continue
                    users.append(
                        {
                            "user_id": content.get("rest_id"),
                            "name": core.get("name"),
                            "handle": core.get("screen_name"),
                            "description": legacy.get("description", ""),
                            "created_at": legacy.get("created_at"),
                        }
                    )
        return users
