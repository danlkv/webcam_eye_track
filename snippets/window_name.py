import sys
import os
import subprocess
import re

def get_active_window_title():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        return match.group("name").strip(b'"')

    return None

def get_connected_monitors_info():
    """
    uses xrandr to detect monitor parameters
    returns: list[dict]
    """
    root = subprocess.Popen(['xrandr'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()
    # Example: HDMI-1-1 connected 1920x1200+0+0 
    m = re.findall(b'(?P<name>.+) connected.+?(?P<width>[0-9]+)x(?P<height>[0-9]+)\+(?P<x>[0-9]+)\+(?P<y>[0-9]+)', stdout)
    if m != None:
        monitors = [
                {
                    'name':str(m_[0].decode('utf-8')),
                    'width':str(m_[1].decode('utf-8')),
                    'height':str(m_[2].decode('utf-8')),
                    'x':str(m_[3].decode('utf-8')),
                    'y':str(m_[4].decode('utf-8')),
                        }
                for m_ in m]

        return monitors
    return []

if __name__ == "__main__":
    print(get_connected_monitors_info())
    print(get_active_window_title())
