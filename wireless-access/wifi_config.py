import subprocess
import platform
import urllib.request
import threading
import time


class WifiConfig:
    def __init__(self):
        pass

    def start(self):
        # thread = threading.Thread(target=self.check_network)
        # thread.start()
        pass

    def test_command(self, ssid, key):
        if self.connect_wifi(ssid, key):
            self.back_hostpot()
            return True
        else:
            return False

    def create_connection(self, ssid, key):
        if platform.system() != "Linux":
            return False
        if self.connect_wifi(ssid, key):
            return True
        else:
            self.back_hostpot()
            return False
        # if self.test_command(ssid, key) is True:

        #     def run_thread():
        #         time.sleep(5)
        #         self.connect_wifi(ssid, key)

        #     thread = threading.Thread(target=run_thread)
        #     thread.start()
        #     return True
        # else:
        #     self.back_hostpot()
        #     return False

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

    def retry(self):
        try:
            command = "systemctl start NetworkManager && sleep 5"
            subprocess.run(command, shell=True, check=True)
            if self.is_connected():
                return True
            else:
                self.back_hostpot()
                return False
        except Exception as e:
            print(e)
            self.back_hostpot()
            return False

    def check_network(self):
        try:
            while True:
                if not self.is_connected():
                    self.retry()
                time.sleep(30)
        except:
            return
