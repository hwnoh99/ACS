from pymodbus.client import ModbusTcpClient


class ModbusConn:
    def __init__(self):
        self.ip = '127.0.0.1'

    def read_regs(self):
        client = ModbusTcpClient(self.ip, 502)
        connection = client.connect()

        registers = []

        if connection:
            print("Connected Modbus server")

            res = client.read_holding_registers(0, 13, slave=1)
            print("Holding Regs :", res.registers)
            registers = res.registers
        else:
            print("Modbus server is unavailable")
        client.close()

        return registers
