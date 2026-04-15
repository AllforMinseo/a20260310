import requests

from config.settings import settings
from ai.stt_client import request_stt

url = settings.stt_server_url

print("STT_SERVER_URL =", url)
print("Calling stt_client.request_stt(...)")

text = request_stt(
    file_path="4분 26초.mp3",
    upload_timeout=60,
    result_timeout=900,
    poll_interval=2.0,
)

print("\n=== STT RESULT (first 500 chars) ===")
print(text[:500])