import datetime
from time import sleep

import numpy as np
from opcua import Node, Server

server = Server()

url = "opc.tcp://127.0.0.1:4841"
server.set_endpoint(url=url)


name = "TEST_SERVER"
addspace = server.register_namespace(name)

node: Node = server.get_objects_node()

paramspace: Node = node.add_object(addspace, "params")


print(type(paramspace))
temp: Node = paramspace.add_variable(addspace, "temp", 0)
time: Node = paramspace.add_variable(addspace, "time", 0)
txt: Node = paramspace.add_variable(addspace, "txt", 0)

# print(type(temp))
temp.set_writable()
time.set_writable()
txt.set_writable()

server.start()

while True:

    temp.set_value(np.random.random_sample())
    time.set_value(datetime.datetime.now())
    txt.set_value(f"Moin: {np.random.randint(0, 100)}")

    sleep(1)
