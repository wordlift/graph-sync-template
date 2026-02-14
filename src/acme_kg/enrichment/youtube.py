import json
import logging
import os
import urllib.request
import urllib.error
from typing import Optional, Dict


class YouTubeEnricher:
    """
    Enricher for YouTube video metadata using the YouTube Data API v3.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the YouTubeEnricher.

        Args:
            api_key: YouTube Data API key. If not provided, it will be loaded from the environment.
        """
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        self.logger = logging.getLogger(__name__)

    def enrich_video(self, video_id: str) -> Optional[Dict[str, str]]:
        """
        Fetch video metadata from YouTube Data API v3.

        Args:
            video_id: YouTube video ID

        Returns:
            Dictionary with title, description, thumbnailUrl, and publishedAt or None if API fails
        """
        if not self.api_key:
            self.logger.warning(
                "YOUTUBE_API_KEY is not configured. YouTube enrichment is skipped but graph sync will continue. "
                "Set YOUTUBE_API_KEY in local .env and in GitHub Actions secrets if you want metadata enrichment."
            )
            return None

        try:
            url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={self.api_key}"

            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())

            if "items" in data and len(data["items"]) > 0:
                snippet = data["items"][0]["snippet"]

                # Get highest quality thumbnail
                thumbnails = snippet.get("thumbnails", {})
                thumbnail_url = (
                    thumbnails.get("maxres", {}).get("url")
                    or thumbnails.get("standard", {}).get("url")
                    or thumbnails.get("high", {}).get("url")
                    or thumbnails.get("medium", {}).get("url")
                    or f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                )

                return {
                    "title": snippet.get("title", ""),
                    "description": snippet.get("description", ""),
                    "thumbnailUrl": thumbnail_url,
                    "publishedAt": snippet.get("publishedAt", ""),
                }
            else:
                self.logger.warning(f"No YouTube data found for video ID: {video_id}")
                return None

        except urllib.error.HTTPError as e:
            self.logger.error(
                f"YouTube API HTTP error for {video_id}: {e.code} - {e.reason}"
            )
            return None
        except Exception as e:
            self.logger.error(
                f"Error fetching YouTube metadata for {video_id}: {str(e)}"
            )
            return None
