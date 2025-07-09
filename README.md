# SCHNEIDER-ATV320-MODBUS-RTU-GUI
Schneider ATV320 Inverter Open Source AC Motor Control GUI

## 8E1 MODBUS RTU ID:1

![image](https://github.com/user-attachments/assets/83716db9-f8e3-40b6-8a78-2f26a25bafb8)


Firstly This GUI was used with Schneider ATV320 inverter controller. AC asynchronous motor is driven by the driver. An AC asynchronous motor was driven by a driver. The logic control algorithm was implemented using the Somove application using Modbus RTU communication between the motor driver and the computer. The motor speed was adjusted based on the analog input signal from the potentiometer. The digital output was designed to act as the motor's emergency stop button.

![image](https://github.com/user-attachments/assets/4eb3963a-60af-4b7a-92d9-963405e1b7c5)





| Function | Address | Type |
|---------|:--------:|:--------:|
| AI1     |5242   | Volt     |
| RCC  | 3202  | Hz  |
| DEC  | 9002  | Sec.  |
| ACC  | 9001  | Sec.  |
| ULN  | 3207  | Volt  |
| LCR | 3204  | Ampere  |




For checking the addresses: https://github.com/sanny32/OpenModScan 



![image](https://github.com/user-attachments/assets/aecc4ff6-186e-47a9-87df-9786e36399dd)


