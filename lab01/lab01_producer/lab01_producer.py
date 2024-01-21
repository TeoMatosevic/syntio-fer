import requests
import json
from azure.eventhub import EventHubProducerClient, EventData
import asyncio

connection_str = (
    "Endpoint=sb://tm-ehns-tpiuo.servicebus.windows.net/"
    ";SharedAccessKeyName=RootManageSharedAccessKey;"
    "SharedAccessKey=BpXgI4gaS9suZ9+KaqzW8If9TGTaQwOEM+AEhIiQiWI="
)
eventhub_name = "tm-eh-tpiuo"
url = "https://oauth.reddit.com/r/dataengineering/top.json?limit=10&t=all"
redit_id = "Mpv44m4AX0UpydVDvowJDw"
redit_secret = "w16rCZuCHXiLSBIUdgOTFfDLYIQOaQ"
auth = requests.auth.HTTPBasicAuth(redit_id, redit_secret)
data = {
    "grant_type": "password",
    "username": "Ancient_League_1716",
    "password": "ijhweubvceuirzv",
}

user_agent = "windows:producer_app:v1.0 (by /u/Ancient_League_1716)"
reddit_headers = {"User-agent": user_agent}

token_response = requests.post(
    "https://www.reddit.com/api/v1/access_token",
    auth=auth,
    data=data,
    headers=reddit_headers,
)
token = token_response.json()["access_token"]
reddit_headers["Authorization"] = f"bearer {token}"


def fetch(data_batch, after):
    parameters = {"after": after, "limit": 10}

    response = requests.get(url, headers=reddit_headers, params=parameters)

    print(response)

    if response.ok:
        data = response.json()

        for post in data["data"]["children"]:
            data_batch.add(EventData(json.dumps(post).encode("utf-8")))
        after = data["data"]["after"]
        return after
    else:
        return None


async def run():
    after = None

    producer = EventHubProducerClient.from_connection_string(
        conn_str=connection_str, eventhub_name=eventhub_name
    )

    for _ in range(100):
        data_batch = producer.create_batch()

        after = fetch(data_batch, after)

        if not after:
            break

        await producer.send_batch(data_batch)

        await asyncio.sleep(10)
    pass


def main():
    asyncio.run(run())

    while True:
        continue


main()
