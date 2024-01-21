import json

from azure.eventhub import EventHubConsumerClient
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime
from azure.core.exceptions import ResourceNotFoundError

connection_str = (
    "Endpoint=sb://tm-ehns-tpiuo.servicebus.windows.net/;"
    "SharedAccessKeyName=RootManageSharedAccessKey;"
    "SharedAccessKey=BpXgI4gaS9suZ9+KaqzW8If9TGTaQwOEM+AEhIiQiWI="
)
eventhub_name = "tm-eh-tpiuo"
consumer_group = "$Default"


storage_account_name = "tmsaferlab"
storage_container_name = "reddit-container"
storage_account_connection_str = (
    "DefaultEndpointsProtocol=https;AccountName=tmsaferlab;"
    "AccountKey=3wOeeGDh0XPajOpwTIryPBQNXSMG2B8Nvex5IZStoo"
    "CU0KNAI/KP8hYzqKmvhnS3ioHUu/"
    "YsUpEL+AStEAZT9g==;"
    "EndpointSuffix=core.windows.net"
)
service_client = DataLakeServiceClient.from_connection_string(
    conn_str=storage_account_connection_str
)
file_system_client = service_client.get_file_system_client(
    file_system=storage_container_name
)


def on_event_batch(partition_context, events):
    file_name = 0

    for event in events:
        post = json.loads(event.body_as_str(encoding="UTF-8"))
        creation = post["data"]["created_utc"]
        creation_datetime = datetime.utcfromtimestamp(creation)

        directory_client = file_system_client.get_directory_client(
            f"{str(creation_datetime.year)}/{str(creation_datetime.month)}/"
            f"{str(creation_datetime.day)}/{str(creation_datetime.hour)}/"
            f"{str(creation_datetime.minute)}"
        )

        try:
            directory_properties = directory_client.get_directory_properties()
            print("Old directory: " + str(directory_properties.name))
        except ResourceNotFoundError:
            directory_client.create_directory()
            new_directory_name = directory_client.get_directory_properties()
            print("New directory: " + str(new_directory_name.name))

        file_client = directory_client.get_file_client(str(file_name))
        file_client.create_file()
        event_bytes = str(event).encode("utf-8")

        length = len(event_bytes)
        file_client.append_data(data=event_bytes, offset=0, length=length)
        file_client.flush_data(len(event_bytes))

        file_name += 1


def main():
    consumer_client = EventHubConsumerClient.from_connection_string(
        connection_str, consumer_group, eventhub_name=eventhub_name
    )

    with consumer_client:
        consumer_client.receive_batch(
            on_event_batch=on_event_batch, starting_position="-1"
        )


main()
