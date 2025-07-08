
import serial
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import time

def read_modbus_register(adrr):
    try:
        # Modbus RTU Serial bağlantısı
        client = ModbusSerialClient(
            port='COM12',  # Seri port adını değiştirin (örn: COM3, /dev/ttyUSB0)
            baudrate=19200,  # Baud rate'i cihazınıza göre ayarlayın
            timeout=1,
            parity='E',  # Parity: N(None), E(Even), O(Odd)
            stopbits=1,
            bytesize=8
        )
        
        # Bağlantıyı aç
        if client.connect():
            print("Modbus bağlantısı başarılı!")
            
            # 49001 adresindeki değeri oku
            # Modbus adresleri genellikle 1-based, ancak pymodbus 0-based kullanır
            # 49001 -> 49000 (0-based)
            device_id = 1  # Slave ID (cihaz ID'si)
            #register_address = 5242  # 49001 - 1 = 49000
            
            # Holding register'ı oku
            result = client.read_holding_registers(
                address=adrr,
                count=1,
            )
            
            if not result.isError():
                value = result.registers[0]
                print(f"Adres 49001'deki değer: {value}")
                return value
            else:
                print(f"Hata: {result}")
                return None
                
        else:
            print("Modbus bağlantısı kurulamadı!")
            return None
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None
        
    finally:
        # Bağlantıyı kapat
        if 'client' in locals():
            client.close()
            print("Bağlantı kapatıldı.")

# Sürekli okuma için fonksiyon
def continuous_read(interval=5):
    """
    Belirli aralıklarla sürekli okuma yapar
    interval: saniye cinsinden okuma aralığı
    """
    print(f"Sürekli okuma başlatılıyor... ({interval} saniye aralıkla)")
    
    while True:
        try:
            value = read_modbus_register()
            if value is not None:
                print(f"Okunan değer: {value}")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nOkuma durduruldu.")
            break

if __name__ == "__main__":
    # Tek seferlik okuma
    read_modbus_register(9001)
    