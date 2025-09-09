import serial
import serial.tools.list_ports
import time

def find_arduino_port():
    """Auto-detect Arduino port."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if 'Arduino' in port.description or 'USB-SERIAL' in port.description:
            print(f"Arduino found on port: {port.device}")
            return port.device
    print("No Arduino found.")
    return None

def Data_Send_To_Arduino(user_input):
    # Send a message to Arduino
    arduino.write((user_input + '\n').encode('utf-8'))  

def Data_Received_From_Arduino_Wait():
    while True:
        # Receive data from Arduino
        if arduino.in_waiting > 0:
            received_data = arduino.readline().decode('utf-8').strip()
            #print(f"Received from Arduino: {received_data}")
            return received_data
    
# Get the port for Arduino
arduino_port = find_arduino_port()

if arduino_port:
    try:
        # Establish a serial connection
        arduino = serial.Serial(arduino_port, baudrate=9600, timeout=1)
        print("Connected to Arduino!")

        # Wait for the connection to stabilize
        time.sleep(2)  # Wait 2 seconds for Arduino to reset

        # Send data to Arduino
        Data_Send_To_Arduino('CONNECTED')
        

    except Exception as e:
        print(f"Error: {e}")
    '''finally:
        if arduino.is_open:
            arduino.close()
            print("Connection closed.")'''
