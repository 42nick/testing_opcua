def get_ip()->str:
    with open("../../custom_configs/ip.txt") as file:
        ip = file.readline()
        return ip

class Params:
    URL = "opc.tcp://127.0.0.1:4841"

