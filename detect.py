import json
import re

class DetectionHandler:
    def __init__(self, social_platforms_file):
        with open(social_platforms_file, 'r') as file:
            self.social_patterns = json.load(file)

    def enhanced_detection(self, page_content, query, types_keywords):
        detection_result = {type_key: False for type_key in types_keywords}
        query_mentions = 0

        for type_key, keywords in types_keywords.items():
            if any(keyword.lower() in page_content.lower() for keyword in keywords):
                detection_result[type_key] = True

        query_mentions = page_content.lower().count(query.lower())

        social_platforms_detected = []
        for platform, pattern in self.social_patterns.items():
            if re.search(pattern, page_content):
                social_platforms_detected.append(platform)

        return {
            "is_forum": detection_result.get("forum", False),
            "is_news": detection_result.get("news", False),
            "query_mentions": query_mentions,
            "social_platforms_detected": social_platforms_detected
        }