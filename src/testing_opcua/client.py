from time import sleep
from opcua import Client, Node

from shared import Params

client = Client(url=Params.URL)

client.connect()

while True:

    time: Node = client.get_node("ns=2;i=3")
    temp: Node = client.get_node("ns=2;i=2")
    txt: Node = client.get_node("ns=2;i=4")

    print(time.get_value(), temp.get_value(), txt.get_value())
    sleep(0.5)
