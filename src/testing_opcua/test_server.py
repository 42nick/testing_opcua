import datetime
import pdb
from time import sleep

import numpy as np
from opcua import Node, Server

from shared import get_ip

server = Server()

# url = "opc.tcp://127.0.0.1:4841"


url = f"opc.tcp://{get_ip()}:4841"
server.set_endpoint(url=url)


name = "TEST_SERVER"
addspace = server.register_namespace(name)

node: Node = server.get_objects_node()

paramspace: Node = node.add_object(addspace, "params")


print(type(paramspace))
temp: Node = paramspace.add_variable(addspace, "temp", 0)
time: Node = paramspace.add_variable(addspace, "time", 0)
humidity: Node = paramspace.add_variable(addspace, "humidity", 0)

# print(type(temp))
temp.set_writable()
time.set_writable()
humidity.set_writable()

server.start()

while True:

    temp.set_value(np.random.random_sample())
    humidity.set_value(int(np.random.randint(22, 25)))
    time.set_value(datetime.datetime.now())

    sleep(1)
