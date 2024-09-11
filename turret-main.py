import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

port = input("Select device port for Arduino #: ")


serialInst.baudrate = 9600
serialInst.port = port
serialInst.open()

while True:
    command = input("Arduino Command (ON/OFF/exit): ")
    serialInst.write(command.encode('utf-8'))

    if command == 'exit':
        serialInst.close()
        exit()