# SCHNEIDER-ATV320-MODBUS-RTU-GUI
Schneider ATV320 Inverter Open Source AC Motor Control GUI

## 8E1 MODBUS RTU ID:1

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


For checking the addresses: https://github.com/sanny32/OpenModScan 


![image](https://github.com/user-attachments/assets/aecc4ff6-186e-47a9-87df-9786e36399dd)


