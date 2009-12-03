import logging
import subprocess
import re

def getLogger(filename="log.txt"):
    logger = logging.getLogger(filename)
    fh = logging.FileHandler(filename,'w')
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)

    return logger

def get_ip():
    get_ip_command = ["ip", "-f", "inet", "addr"]
    result = subprocess.Popen(get_ip_command, stdout=subprocess.PIPE, close_fds=True).stdout.read()
    regexp = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    ip = re.findall(regexp, result)[1]
    return ip

def set_color(r,g,b):
    set_mode("direct")
    value = "%X:%X:%X" % (r,g,b)
    FILE = open("/sys/devices/platform/i2c_omap.2/i2c-0/0-0032/color","w")
    FILE.write(value)
    FILE.close()

def set_mode(mode):
    FILE = open("/sys/devices/platform/i2c_omap.2/i2c-0/0-0032/mode","w")
    FILE.write(mode)
    FILE.close()
