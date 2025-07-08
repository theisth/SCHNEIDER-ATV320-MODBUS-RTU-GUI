import serial
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import time

def read_modbus_register(addr):
    """
    Belirtilen adresten Modbus register değerini okur
    """
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
            
            device_id = 1  # Slave ID (cihaz ID'si)
            
            # Holding register'ı oku
            result = client.read_holding_registers(
                address=addr,
                count=1,
                slave=device_id
            )
            
            if not result.isError():
                value = result.registers[0]
                print(f"Adres {addr}'deki değer: {value}")
                return value
            else:
                print(f"Okuma hatası: {result}")
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

def write_modbus_register(addr, value):
    """
    Belirtilen adrese Modbus register değerini yazar
    """
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
            
            device_id = 1  # Slave ID (cihaz ID'si)
            
            # Holding register'a yaz
            result = client.write_register(
                address=addr,
                value=value,
                slave=device_id
            )
            
            if not result.isError():
                print(f"Adres {addr}'e değer {value} başarıyla yazıldı!")
                return True
            else:
                print(f"Yazma hatası: {result}")
                return False
                
        else:
            print("Modbus bağlantısı kurulamadı!")
            return False
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False
        
    finally:
        # Bağlantıyı kapat
        if 'client' in locals():
            client.close()
            print("Bağlantı kapatıldı.")

def write_multiple_registers(addr, values):
    """
    Birden fazla register'a aynı anda yazar
    values: yazılacak değerlerin listesi
    """
    try:
        client = ModbusSerialClient(
            port='COM12',
            baudrate=19200,
            timeout=1,
            parity='E',
            stopbits=1,
            bytesize=8
        )
        
        if client.connect():
            print("Modbus bağlantısı başarılı!")
            
            device_id = 1
            
            # Birden fazla register'a yaz
            result = client.write_registers(
                address=addr,
                values=values,
                slave=device_id
            )
            
            if not result.isError():
                print(f"Adres {addr}'den itibaren {len(values)} register'a başarıyla yazıldı!")
                return True
            else:
                print(f"Yazma hatası: {result}")
                return False
                
        else:
            print("Modbus bağlantısı kurulamadı!")
            return False
            
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False
        
    finally:
        if 'client' in locals():
            client.close()
            print("Bağlantı kapatıldı.")

def read_write_test(addr, new_value):
    """
    Önce okuma, sonra yazma, tekrar okuma işlemi yapar
    """
    print("=== Okuma/Yazma Test İşlemi ===")
    
    # Önce mevcut değeri oku
    print("1. Mevcut değer okunuyor...")
    old_value = read_modbus_register(addr)
    
    if old_value is not None:
        print(f"Mevcut değer: {old_value}")
        
        # Yeni değeri yaz
        print(f"2. Yeni değer ({new_value}) yazılıyor...")
        write_success = write_modbus_register(addr, new_value)
        
        if write_success:
            # Yazma işleminden sonra tekrar oku
            print("3. Yazma işlemi sonrası kontrol ediliyor...")
            time.sleep(0.5)  # Kısa bir bekleme
            final_value = read_modbus_register(addr)
            
            if final_value == new_value:
                print("✓ Yazma işlemi başarılı! Değer doğru şekilde değiştirildi.")
            else:
                print("✗ Yazma işlemi başarısız! Değer beklendiği gibi değişmedi.")
        else:
            print("✗ Yazma işlemi başarısız!")
    else:
        print("✗ Okuma işlemi başarısız!")

# Sürekli okuma için fonksiyon
def continuous_read(addr, interval=5):
    """
    Belirli aralıklarla sürekli okuma yapar
    interval: saniye cinsinden okuma aralığı
    """
    print(f"Sürekli okuma başlatılıyor... ({interval} saniye aralıkla)")
    
    while True:
        try:
            value = read_modbus_register(addr)
            if value is not None:
                print(f"Okunan değer: {value}")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nOkuma durduruldu.")
            break

if __name__ == "__main__":
    # Test senaryoları
    
    # 1. Tek seferlik okuma
    print("=== Tek Seferlik Okuma ===")
    read_modbus_register(9001)
    
    # 2. Tek seferlik yazma
    print("\n=== Tek Seferlik Yazma ===")
    write_modbus_register(9001, 10)  # 9001 adresine 1234 değerini yaz
    
    print("=== Degistirmis Degeri Oku ===")
    read_modbus_register(9001)