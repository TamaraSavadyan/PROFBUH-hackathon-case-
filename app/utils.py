import re
from urllib.parse import urlparse, parse_qs


def extract_link_from_message(text):
    url_pattern = re.compile(r'https?://\S+')

    match = re.search(url_pattern, text)

    if match:
        link = match.group(0)
        return link

    return None

def get_video_id(video_link):
    parsed_url = urlparse(video_link)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get('v', [''])[0]
    return video_id

