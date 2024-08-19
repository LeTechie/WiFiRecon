"""
@author: Sandip Jana
"""
import time
from get_BSSID import *

FLAG_LOCATION= str(input("Enter Location(e.g. Room No.): "))

try:
    Fresh_Test = get_BSSID()
    RESULT_WiFi_Scan= []
    for i in range(0,10):
        time.sleep(0.5)
        Last_Test = Fresh_Test
        Fresh_Test = get_BSSID()
        print("Scan #"+str(i))
        if Last_Test == Fresh_Test:
            RESULT_WiFi_Scan= Fresh_Test
            
    if not RESULT_WiFi_Scan:
        print("Keep your system at a fixed position and run the script again")
    else:
        print("Scan COMPLETE!")
        
    ####### SAVE the result with Location #########################################
    FILE_NAME= str(FLAG_LOCATION)+ ".txt"
    with open(FILE_NAME, "w") as file:
        file.write("LOCATION, AP_MAC_ID, SSID, CENTER_FREQ_MHz, RSSI_dBm\n")
        for key, value in RESULT_WiFi_Scan.items():
            file.write(f"{FLAG_LOCATION}, {key}, {value[0]}, {value[1]}, {value[2]}\n")
    print("File Saved Successfully!")

except:
    print("Scan FAILED!!")
    print("Check your WiFi Adapter settings/ Keep it ON during the scan")
        







