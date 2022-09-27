import subprocess
import platform
import urllib.request
import threading
import time


class WifiConfig:
    def __init__(self):
        thread = threading.Thread(target=self.check_network)
        thread.start()

    def test_command(self, ssid, key):
        try:
            self.connect_wifi(ssid, key)
            self.back_hostpot()
            return True
        except Exception as e:
            print(e)
            return False

    def create_connection(self, ssid, key):
        if platform.system() != "Linux":
            return False
        if self.test_command(ssid, key):
            thread = threading.Thread(
                target=self.connect_wifi,
                args=(
                    ssid,
                    key,
                ),
            )
            thread.start()
            return True
        else:
            self.back_hostpot()
            return False

    def connect_wifi(self, ssid, key):
        try:
            command = (
                "systemctl start NetworkManager "
                + "&& sleep 5 "
                + "&& nmcli dev wifi connect '"
                + ssid
                + "' password '"
                + key
                + "'"
            )
            subprocess.run(command, shell=True, check=True)
            return True
        except Exception as e:
            print(e)
            return False

    def back_hostpot(self):
        try:
            command = (
                "systemctl stop NetworkManager "
                + "&& systemctl restart hostapd "
                + "&& systemctl restart dhcpcd "
                + "&& systemctl restart dnsmasq"
            )
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

    def is_connected(self, host="http://google.com"):
        try:
            urllib.request.urlopen(host)  # Python 3.x
            return True
        except:
            return False

    def check_network(self):
        try:
            while True:
                if not self.is_connected():
                    self.back_hostpot()
                    return
                time.sleep(60)
        except:
            return
