import json

from azure.eventhub import EventHubConsumerClient

# connection string information
connection_str = (
    "Endpoint=sb://tm-ehns-tpiuo.servicebus.windows.net/;"
    "SharedAccessKeyName=RootManageSharedAccessKey;"
    "SharedAccessKey=BpXgI4gaS9suZ9+KaqzW8If9TGTaQwOEM+AEhIiQiWI="
)
# eventhub name
eventhub_name = "tm-eh-tpiuo"
# consumer group name
consumer_group = "$Default"


def on_event(partition_context, event):
    json_data = json.loads(event.body_as_str())

    print(json_data)

    partition_context.update_checkpoint(event)


consumer = EventHubConsumerClient.from_connection_string(
    connection_str, consumer_group=consumer_group, eventhub_name=eventhub_name
)

with consumer:
    consumer.receive(on_event=on_event)
