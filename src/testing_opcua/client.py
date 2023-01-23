from time import sleep

import numpy as np
from opcua import Client, Node

from shared import Params
from testing_opcua.shared import get_ip


def connect_and_get_values():
    try:
        client = Client(url="opc.tcp://" + get_ip() + ":4841")
        client.connect()
        time: Node = client.get_node("ns=2;i=3").get_value()
        temp: Node = client.get_node("ns=2;i=2").get_value()
        humidity: Node = client.get_node("ns=2;i=4").get_value()
    except OSError:
        time = 0
        temp = np.random.random_integers(22, 24)
        humidity = 0
        print("Could not connect :(")

    return time, temp, humidity
