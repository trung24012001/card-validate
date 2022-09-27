import subprocess
import platform
import urllib.request
import threading
import time


class WifiConfig:
    def __init__(self):
        thread = threading.Thread(target=self.check_connection)
        thread.start()

    def create_connection(self, ssid, key):
        if platform.system() != "Linux":
            return False
        try:
            command = "systemctl start NetworkManager " + "&& sleep 5 " + \
                "&& nmcli dev wifi connect '" + ssid + "' password '" + key + "'"
            subprocess.run(command, shell=True, check=True)
            return True
        except Exception as e:
            print(e)
            self.reverse_host()
            return False

    def reverse_host(self):
        try:
            command = "systemctl stop NetworkManager " + "&& systemctl restart hostapd " + \
                "&& systemctl restart dhcpcd " + "&& systemctl restart dnsmasq"
            subprocess.run(command, shell=True, check=True)
        except Exception as e:
            print(e)
            # self.reboot()
            print("Error!!!!")

    def reboot(self):
        try:
            subprocess.run("reboot", shell=True, check=True)
        except Exception as e:
            print(e)
            print("Error!!!!")

    def is_connected(self, host='http://google.com'):
        try:
            urllib.request.urlopen(host)  # Python 3.x
            return True
        except:
            return False

    def check_connection(self):
        try:
            while True:
                if not self.is_connected():
                    print("reverst")
                    self.reverse_host()
                    return

                time.sleep(60)
        except:
            return
