import serial
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
import time
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import math

class ModbusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ATV320 Modbus RTU Data Reader/Writer GUI")
        self.root.geometry("1500x900")
        
        # Blue theme setup
        self.setup_theme()
        
        # Modbus client
        self.client = None
        self.is_connected = False
        self.is_reading = False
        
        # Reading thread
        self.read_thread = None
        
        # Create GUI components
        self.create_widgets()
        
        # Initial connection
        self.connect_modbus()


    def setup_theme(self):
        """Blue theme setup"""
        self.root.configure(bg='#1e3a5f')
        
        # Style definitions
        style = ttk.Style()
        style.theme_use('clam')
        
        # Blue color scheme
        style.configure('TLabel', 
                       background='#1e3a5f', 
                       foreground='white',
                       font=('Arial', 10))
        
        style.configure('TLabelFrame', 
                       background='#1e3a5f',
                       foreground='white',
                       font=('Arial', 11, 'bold'))
        
        style.configure('TLabelFrame.Label', 
                       background='#1e3a5f',
                       foreground='white',
                       font=('Arial', 11, 'bold'))
        
        style.configure('TFrame', 
                       background='#1e3a5f')
        
        style.configure('TButton', 
                       background='#4682b4',
                       foreground='white',
                       font=('Arial', 10, 'bold'))
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = tk.Label(main_frame, text="ATV320 Modbus RTU Data Reader/Writer GUI", 
                              bg='#1e3a5f', fg='white', font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))

        # Designer
        title_designer = tk.Label(main_frame, text="@Ahmet Ali Tilkicioglu/Electronics Engineer", 
                              bg='#1e3a5f', fg='white', font=('Arial', 8, 'bold'))
        title_designer.grid(row=1, column=0, columnspan=4, pady=(0, 20))
        
        
        # Connection status
        self.status_label = tk.Label(main_frame, text="Connection Status: Connecting...", 
                                    bg='#1e3a5f', fg='white', font=('Arial', 12, 'bold'))
        self.status_label.grid(row=1, column=3, columnspan=4, pady=(0, 15))
        
        # Left panel - Data display and control
        left_frame = ttk.LabelFrame(main_frame, text="Data Monitoring and Control", padding="10")
        left_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                       padx=(0, 10), pady=(0, 10))
        
        # Analog Input 1 (mV) - Address 5242
        tk.Label(left_frame, text="Analog Input Voltage 1 (mV):", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.value_5242 = tk.Label(left_frame, text="0", bg='#87ceeb', fg='#000080', 
                                  font=('Arial', 12, 'bold'), relief='sunken', width=15)
        self.value_5242.grid(row=0, column=1, padx=(10, 0), sticky=tk.W)
        
        # Motor Hz - Address 3202
        tk.Label(left_frame, text="Motor Hz:", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=(15, 0))
        self.value_3202 = tk.Label(left_frame, text="0", bg='#87ceeb', fg='#000080', 
                                  font=('Arial', 12, 'bold'), relief='sunken', width=15)
        self.value_3202.grid(row=1, column=1, padx=(10, 0), sticky=tk.W, pady=(15, 0))
        
        # ACC - Address 9001 (Read)
        tk.Label(left_frame, text="ACC (Read):", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(15, 0))
        self.value_9001 = tk.Label(left_frame, text="0", bg='#87ceeb', fg='#000080', 
                                  font=('Arial', 12, 'bold'), relief='sunken', width=15)
        self.value_9001.grid(row=2, column=1, padx=(10, 0), sticky=tk.W, pady=(15, 0))
        
        # DEC - Address 9002 (Read)
        tk.Label(left_frame, text="DEC (Read):", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(15, 0))
        self.value_9002 = tk.Label(left_frame, text="0", bg='#87ceeb', fg='#000080', 
                                  font=('Arial', 12, 'bold'), relief='sunken', width=15)
        self.value_9002.grid(row=3, column=1, padx=(10, 0), sticky=tk.W, pady=(15, 0))


        # ULN - Address 3207 (Read)
        tk.Label(left_frame, text="ULN (Read):", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=(15, 0))
        self.value_3207 = tk.Label(left_frame, text="0", bg='#87ceeb', fg='#000080', 
                                  font=('Arial', 12, 'bold'), relief='sunken', width=15)
        self.value_3207.grid(row=4, column=1, padx=(10, 0), sticky=tk.W, pady=(15, 0))


        # LCR - Address 3204 (Read)
        tk.Label(left_frame, text="LCR (Read):", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=5, column=0, sticky=tk.W, pady=(15, 0))
        self.value_3204 = tk.Label(left_frame, text="0", bg='#87ceeb', fg='#000080', 
                                  font=('Arial', 12, 'bold'), relief='sunken', width=15)
        self.value_3204.grid(row=5, column=1, padx=(10, 0), sticky=tk.W, pady=(15, 0))



        # Write Control Frame
        write_frame = ttk.LabelFrame(left_frame, text="Write Control", padding="10")
        write_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))

        # ACC Write Control
        tk.Label(write_frame, text="New ACC Value:", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.acc_entry = tk.Entry(write_frame, width=10, font=('Arial', 12), bg='white', fg='black')
        self.acc_entry.grid(row=0, column=1, padx=(10, 0))
        
        self.write_acc_button = tk.Button(write_frame, text="Write ACC", 
                                         command=lambda: self.write_register_value(9001, self.acc_entry), 
                                         bg='#4682b4', fg='white', font=('Arial', 10, 'bold'))
        self.write_acc_button.grid(row=0, column=2, padx=(10, 0))
        
        # DEC Write Control
        tk.Label(write_frame, text="New DEC Value:", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky=tk.W)
        self.dec_entry = tk.Entry(write_frame, width=10, font=('Arial', 12), bg='white', fg='black')
        self.dec_entry.grid(row=1, column=1, padx=(10, 0))
        
        self.write_dec_button = tk.Button(write_frame, text="Write DEC", 
                                         command=lambda: self.write_register_value(9002, self.dec_entry), 
                                         bg='#4682b4', fg='white', font=('Arial', 10, 'bold'))
        self.write_dec_button.grid(row=1, column=2, padx=(10, 0))
        
        # Connection Settings Frame
        settings_frame = ttk.LabelFrame(left_frame, text="Connection Settings", padding="10")
        settings_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Slave ID setting
        tk.Label(settings_frame, text="Slave ID:", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.slave_id_var = tk.StringVar(value="1")
        self.slave_id_entry = tk.Entry(settings_frame, textvariable=self.slave_id_var, 
                                      width=5, font=('Arial', 12), bg='white', fg='black')
        self.slave_id_entry.grid(row=0, column=1, padx=(10, 0))
        
        # Test connection button
        self.test_button = tk.Button(settings_frame, text="Test Connection", 
                                    command=self.manual_test_connection, 
                                    bg='#4682b4', fg='white', font=('Arial', 10, 'bold'))
        self.test_button.grid(row=0, column=2, padx=(10, 0))
        
        # Control buttons
        button_frame = tk.Frame(left_frame, bg='#1e3a5f')
        button_frame.grid(row=9, column=0, columnspan=2, pady=(20, 0))
        
        self.start_button = tk.Button(button_frame, text="Start Reading", 
                                     command=self.start_reading, state="disabled", 
                                     bg='#4682b4', fg='white', font=('Arial', 10, 'bold'))
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = tk.Button(button_frame, text="Stop Reading", 
                                    command=self.stop_reading, state="disabled",
                                    bg='#4682b4', fg='white', font=('Arial', 10, 'bold'))
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.reconnect_button = tk.Button(button_frame, text="Reconnect", 
                                         command=self.reconnect, 
                                         bg='#4682b4', fg='white', font=('Arial', 10, 'bold'))
        self.reconnect_button.grid(row=0, column=2, padx=5)
        
        # Right panel - Gauges
        right_frame = ttk.LabelFrame(main_frame, text="Value Gauges", padding="10")
        right_frame.grid(row=2, column=2, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                        padx=(10, 0), pady=(0, 10))
        
        # Analog value gauge
        tk.Label(right_frame, text="Analog Input Voltage 1 (mV)", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=(0, 10))
        self.analog_canvas = tk.Canvas(right_frame, width=200, height=300, bg='#87ceeb')
        self.analog_canvas.grid(row=1, column=0, padx=10)
        
        # Hz value gauge
        tk.Label(right_frame, text="Hz Value Gauge", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=0, column=1, pady=(0, 10))
        self.hz_canvas = tk.Canvas(right_frame, width=200, height=300, bg='#87ceeb')
        self.hz_canvas.grid(row=1, column=1, padx=10)

        # Main Line Voltage value gauge
        tk.Label(right_frame, text="Main Line Voltage Value Gauge", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=0, column=2, pady=(0, 10))
        self.volt = tk.Canvas(right_frame, width=200, height=300, bg='#87ceeb')
        self.volt.grid(row=1, column=2, padx=10)        


        # Main Line Voltage value gauge
        tk.Label(right_frame, text="Motor Current", bg='#1e3a5f', fg='white', 
                font=('Arial', 12, 'bold')).grid(row=0, column=3, pady=(0, 10))
        self.amp = tk.Canvas(right_frame, width=200, height=300, bg='#87ceeb')
        self.amp.grid(row=1, column=3, padx=10)    


        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, height=8, width=70, bg='#f0f8ff', fg='#000080')
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.columnconfigure(3, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Initialize gauges
        self.draw_column_gauge(self.analog_canvas, 0, 0, 10000, "mV")
        self.draw_column_gauge(self.hz_canvas, 0, 0, 50, "Hz")
        self.draw_column_gauge(self.volt, 0, 0, 240, 'V')
        self.draw_column_gauge(self.amp, 0, 0, 50, 'A')

        
    def draw_column_gauge(self, canvas, value, min_val, max_val, title):
        """Draw column gauge with level-based colors"""
        canvas.delete("all")
        
        # Gauge parameters
        width = 190
        height = 280
        margin = 20
        gauge_width = 40
        gauge_height = height - 2 * margin - 40
        
        # Calculate position
        x_center = width // 2
        gauge_x = x_center - gauge_width // 2
        gauge_y = margin + 30
        
        # Calculate fill ratio
        if max_val > min_val:
            ratio = max(0, min(1, (value - min_val) / (max_val - min_val)))
        else:
            ratio = 0
        
        # Determine color based on level
        if ratio < 0.3:
            fill_color = '#00FF00'  # Green
        elif ratio < 0.6:
            fill_color = '#FFFF00'  # Yellow
        elif ratio < 0.8:
            fill_color = '#FF8000'  # Orange
        else:
            fill_color = '#FF0000'  # Red
        
        # Draw gauge background
        canvas.create_rectangle(gauge_x, gauge_y, gauge_x + gauge_width, 
                               gauge_y + gauge_height, fill='white', outline='black', width=2)
        
        # Draw fill
        fill_height = gauge_height * ratio
        if fill_height > 0:
            canvas.create_rectangle(gauge_x + 2, gauge_y + gauge_height - fill_height, 
                                   gauge_x + gauge_width - 2, gauge_y + gauge_height - 2, 
                                   fill=fill_color, outline='')
        
        # Draw scale markings
        for i in range(11):  # 0-10 scale
            scale_ratio = i / 10
            scale_y = gauge_y + gauge_height - (scale_ratio * gauge_height)
            
            # Scale line
            canvas.create_line(gauge_x + gauge_width, scale_y, 
                              gauge_x + gauge_width + 10, scale_y, 
                              fill='black', width=2)
            
            # Scale value
            scale_value = min_val + (scale_ratio * (max_val - min_val))
            canvas.create_text(gauge_x + gauge_width + 20, scale_y, 
                              text=f"{int(scale_value)}", anchor='w',
                              fill='black', font=('Arial', 8, 'bold'))
        
        # Draw title
        canvas.create_text(x_center, 15, text=title, 
                          fill='black', font=('Arial', 12, 'bold'))
        
        # Draw current value
        canvas.create_text(x_center, height - 15, text=f"{value:.1f}", 
                          fill='black', font=('Arial', 14, 'bold'))
        
        # Draw level indicator
        if ratio > 0:
            indicator_y = gauge_y + gauge_height - (ratio * gauge_height)
            canvas.create_polygon(gauge_x - 8, indicator_y, 
                                 gauge_x - 2, indicator_y - 6, 
                                 gauge_x - 2, indicator_y + 6, 
                                 fill='black')
        
    def log_message(self, message):
        """Add log message"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def connect_modbus(self):
        """Establish Modbus connection"""
        try:
            self.client = ModbusSerialClient(
                port='COM12',
                baudrate=19200,
                timeout=3,  # Increased timeout
                parity='E',
                stopbits=1,
                bytesize=8,
            )
            
            if self.client.connect():
                self.is_connected = True
                self.status_label.config(text="Connection Status: Connected", foreground="lightgreen")
                self.start_button.config(state="normal")
                self.write_acc_button.config(state="normal")
                self.write_dec_button.config(state="normal")
                self.log_message("Modbus connection successful!")
                
                # Test connection with a simple read
                self.test_connection()
            else:
                self.is_connected = False
                self.status_label.config(text="Connection Status: Connection Error", foreground="red")
                self.log_message("Modbus connection failed!")
                
        except Exception as e:
            self.is_connected = False
            self.status_label.config(text="Connection Status: Error", foreground="red")
            self.log_message(f"Connection error: {e}")
            
    def test_connection(self):
        """Test connection with a simple read"""
        try:
            # Try to read a common register (address 0) to test connection
            result = self.client.read_holding_registers(address=0, count=1)
            if result.isError():
                self.log_message("Connection test failed - device may not be responding")
                self.log_message("Check: Device ID, baud rate, parity, and wiring")
            else:
                self.log_message("Connection test successful!")
        except Exception as e:
            self.log_message(f"Connection test error: {e}")
            
    def read_modbus_register(self, address, slave_id=1):
        """Read Modbus register with improved error handling"""
        try:
            if not self.is_connected or not self.client:
                return None
                
            result = self.client.read_holding_registers(
                address=address,
                count=1,
                slave=slave_id  # Add slave ID parameter
            )
            
            if not result.isError():
                return result.registers[0]
            else:
                # More detailed error logging
                error_msg = str(result)
                if "No response" in error_msg:
                    self.log_message(f"Address {address}: No response from device (check slave ID: {slave_id})")
                elif "Illegal" in error_msg:
                    self.log_message(f"Address {address}: Illegal address or function")
                else:
                    self.log_message(f"Address {address} read error: {result}")
                return None
                
        except Exception as e:
            self.log_message(f"Address {address} read error: {e}")
            return None
            
    def write_modbus_register(self, address, value, slave_id=1):
        """Write Modbus register with improved error handling"""
        try:
            if not self.is_connected or not self.client:
                return False
                
            result = self.client.write_register(
                address=address,
                value=value,
                slave=slave_id  # Add slave ID parameter
            )
            
            if not result.isError():
                self.log_message(f"Value {value} successfully written to address {address}!")
                return True
            else:
                self.log_message(f"Address {address} write error: {result}")
                return False
                
        except Exception as e:
            self.log_message(f"Address {address} write error: {e}")
            return False
            
    def write_register_value(self, address, entry_widget):
        """Write register value from entry widget"""
        try:
            value = int(entry_widget.get())
            
            if self.write_modbus_register(address, value):
                messagebox.showinfo("Success", f"Value {value} written to address {address}!")
                entry_widget.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Could not write value to address {address}!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
        except Exception as e:
            messagebox.showerror("Error", f"Write error: {e}")
            
    def manual_test_connection(self):
        """Manual test connection with specific slave ID"""
        try:
            slave_id = int(self.slave_id_var.get())
            self.log_message(f"Testing connection with Slave ID: {slave_id}")
            
            # Test with multiple common addresses
            test_addresses = [0, 1, 2, 3, 4, 5, 100, 1000]
            success_count = 0
            
            for addr in test_addresses:
                result = self.client.read_holding_registers(address=addr, count=1, slave=slave_id)
                if not result.isError():
                    self.log_message(f"✓ Address {addr}: Success (Value: {result.registers[0]})")
                    success_count += 1
                else:
                    self.log_message(f"✗ Address {addr}: {result}")
            
            if success_count > 0:
                self.log_message(f"Connection test completed: {success_count}/{len(test_addresses)} addresses responded")
            else:
                self.log_message("No addresses responded. Check device settings.")
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid slave ID number!")
        except Exception as e:
            self.log_message(f"Test connection error: {e}")
            
    def update_values(self):
        """Update values with configurable slave ID"""
        slave_id = 1
        try:
            slave_id = int(self.slave_id_var.get())
        except:
            slave_id = 1
            
        while self.is_reading:
            try:
                # Read address 5242 (Analog Input)
                value_5242 = self.read_modbus_register(5242, slave_id)
                if value_5242 is not None:
                    self.value_5242.config(text=str(value_5242))
                    self.draw_column_gauge(self.analog_canvas, value_5242, 0, 10000, "mV")
                else:
                    self.value_5242.config(text="ERROR")
                
                # Read address 3202 (Motor Hz)
                value_3202 = self.read_modbus_register(3202, slave_id)
                if value_3202 is not None:
                    hz_value = value_3202 / 10.0
                    self.value_3202.config(text=f"{hz_value:.1f}")
                    self.draw_column_gauge(self.hz_canvas, hz_value, 0, 50, "Hz")
                else:
                    self.value_3202.config(text="ERROR")
                
                # Read address 9001 (ACC)
                value_9001 = self.read_modbus_register(9001, slave_id)
                if value_9001 is not None:
                    self.value_9001.config(text=str(value_9001))
                else:
                    self.value_9001.config(text="ERROR")

                # Read address 9002 (DEC)
                value_9002 = self.read_modbus_register(9002, slave_id)
                if value_9002 is not None:
                    self.value_9002.config(text=str(value_9002))
                else:
                    self.value_9002.config(text="ERROR")
                

                # Read address 3207 (ULN)
                value_3207 = self.read_modbus_register(3207, slave_id)
                if value_3207 is not None:
                    value_3207 = value_3207/10
                    self.value_3207.config(text=str(value_3207))
                    self.draw_column_gauge(self.volt, value_3207, 0, 240, "V")
                else:
                    self.value_3207.config(text="ERROR")


                # Read address 3204 (LCR)
                value_3204 = self.read_modbus_register(3204, slave_id)
                if value_3204 is not None:
                    self.value_3204.config(text=str(value_3204))
                    self.draw_column_gauge(self.amp, value_3204, 0, 50, "A")
                else:
                    self.value_3204.config(text="ERROR")


                time.sleep(0.001)  # Increased delay to reduce communication load
                
            except Exception as e:
                self.log_message(f"Data reading error: {e}")
                time.sleep(0.5)
                
    def start_reading(self):
        """Start reading"""
        if not self.is_connected:
            messagebox.showerror("Error", "No Modbus connection!")
            return
            
        self.is_reading = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start reading thread
        self.read_thread = threading.Thread(target=self.update_values)
        self.read_thread.daemon = True
        self.read_thread.start()
        
        self.log_message("Data reading started (0.2 second interval)")
        
    def stop_reading(self):
        """Stop reading"""
        self.is_reading = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log_message("Data reading stopped")
        
    def reconnect(self):
        """Reconnect"""
        if self.is_reading:
            self.stop_reading()
            
        if self.client:
            self.client.close()
            
        self.log_message("Reconnecting...")
        self.connect_modbus()
        
    def on_closing(self):
        """When application is closing"""
        self.is_reading = False
        if self.client:
            self.client.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModbusGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()