"""Search YouTube from the terminal and print real video titles, channels and links.

Used to build each week's videos.md with verified links.

Usage:
    python3 tools/yt_search.py "Gaurav Sen consistent hashing" "Engineering Digest caching"
"""

import json
import re
import sys
import urllib.parse
import urllib.request


def search(query, limit=8):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
    html = urllib.request.urlopen(request, timeout=20).read().decode("utf-8", "ignore")
    match = re.search(r"var ytInitialData = (\{.*?\});</script>", html)
    if not match:
        return []

    videos = []

    def walk(node):
        if isinstance(node, dict):
            if "videoRenderer" in node:
                v = node["videoRenderer"]
                title = "".join(run.get("text", "") for run in v.get("title", {}).get("runs", []))
                channel = "".join(run.get("text", "") for run in v.get("ownerText", {}).get("runs", []))
                length = v.get("lengthText", {}).get("simpleText", "")
                videos.append((channel, title, v.get("videoId"), length))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(json.loads(match.group(1)))
    return videos[:limit]


if __name__ == "__main__":
    for query in sys.argv[1:]:
        print(f"\n### {query}")
        try:
            for channel, title, video_id, length in search(query):
                print(f"  [{channel}] {title} ({length}) https://www.youtube.com/watch?v={video_id}")
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR: {e}")
