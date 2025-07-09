# SCHNEIDER-ATV320-MODBUS-RTU-GUI
Schneider ATV320 Inverter Open Source AC Motor Control GUI

## 8E1 MODBUS RTU ID:1
### WARNING: You must Edit Serial COM in Python Code. (Ex. COM12 in this app.)
### Control your systems serial ports.

## Application Photo
![image](https://github.com/user-attachments/assets/83716db9-f8e3-40b6-8a78-2f26a25bafb8)

Firstly This GUI was used with Schneider ATV320 inverter controller. AC asynchronous motor is driven by the driver. An AC asynchronous motor was driven by a driver. The logic control algorithm was implemented using the Somove application using Modbus RTU communication between the motor driver and the computer. The motor speed was adjusted based on the analog input signal from the potentiometer. The digital output was designed to act as the motor's emergency stop button. 

## ATV Logic Diagram
![image](https://github.com/user-attachments/assets/4eb3963a-60af-4b7a-92d9-963405e1b7c5)

Once the system, programmed with ATV Logic, is started, the ID is defined. After defining the ID, the ATV320 sends a response to other devices via MODBUS. Unfortunately, the GUI does not work without defining the address; please specify the address in SoMove program for ATV320 or others that you have. After defining the address, MODBUS now prints all the addresses as a response. The addresses in the table below are read and written using Python.

## Addresses Diagram
| Function | Address | Type | Description |
|---------|:--------:|:--------:|:--------:|
| AI1     |5242   | Volt     | Analog Input 1 |
| RCC  | 3202  | Hz  |Motor Herthz  |
| DEC  | 9002  | Sec.  | Deceleration Ramp Time|
| ACC  | 9001  | Sec.  | Acceleration Ramp Time|
| ULN  | 3207  | Volt  | Main Line Voltage |
| LCR | 3204  | Ampere  | Motor Current  |

You can apply the addresses in this table using the programs in the link. The following image shows the sample application for addresses 9002 and 9001. For checking the MODBUS addresses: https://github.com/sanny32/OpenModScan 

![image](https://github.com/user-attachments/assets/122a51c9-fa2b-40e6-a3ef-acb31df6d011)


This Python project is a graphical user interface (GUI) application developed to directly control Schneider Electric's ATV320 series frequency converter from a computer, using the Modbus RTU protocol. Written in the Python programming language, the application primarily implements serial communication with the driver via the Modbus RTU protocol using the pymodbus library. This communication utilizes the pyserial infrastructure, enabling a direct RS485 or USB-to-RS485 converter. Users can initiate communication with the driver by entering connection parameters such as the port name (e.g., COM3) and baud rate in the GUI. The application's design, built with tkinter and ttk modules, offers a modern and user-friendly interface; window titles, dimensions, labels, input fields, and buttons are systematically placed. Users can initiate read or write operations by entering register addresses and values ​​in the GUI input boxes; the read results are displayed instantly on the screen.

Technically, the most striking aspect of the application is ensuring real-time data flow and the interface's ability to operate without freezing. For this purpose, Python's threading library is used to continuously read data in a separate thread. This ensures that the GUI's main loop is unaffected by the data reading process, and user interactions continue uninterrupted. In Modbus RTU communication, methods such as read_holding_registers are used to read data from the drive, while write_register or write_registers are used to write data. Any connection errors or drive unresponsiveness that may occur during these operations are captured by the pymodbus.exceptions.ModbusIOException class, and errors are presented to the user as readable messages on the GUI. This allows the user to quickly identify hardware or connection problems.

The interface design prioritizes simplicity and functionality. For example, read data is displayed directly on the labels, while error messages or connection status are also communicated to the user. The application provides not only basic read and write functions but also monitoring and continuous control of communication with the drive. This allows engineers, technicians, or maintenance personnel to easily modify the parameters of the Schneider ATV320 drive, monitor motor status in real-time, and perform fault diagnosis operations. The code architecture utilizes a class called ModbusGUI, which defines GUI components, manages connection operations, and includes read/write functions. This ensures a structured design for both readability and maintainability.

Ultimately, this project utilizes technologies from the Python ecosystem, such as serial communication (pyserial), industrial Modbus protocol (pymodbus), multi-threading (threading), and desktop application development (tkinter), enabling practical, reliable, and visual control of a frequently used drive from a computer. The application was developed by taking into account the dynamics of real-world Modbus RTU communication in both hardware and software, and its user-friendly design provides a tool that even non-technical users can easily use.

![image](https://github.com/user-attachments/assets/aecc4ff6-186e-47a9-87df-9786e36399dd)


