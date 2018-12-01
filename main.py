import argparse
from camera.face import Camera, getAvailableCameraIds
from window import *
import data

# This is where xml cascade files stored
face_cascade_path = '/home/danlkv/Junction/payhere/ml_data/haarcascade_frontalface_default.xml'
eye_cascade_path = '/home/danlkv/Junction/payhere/ml_data/haarcascade_eye.xml'

def init_face_cam():
    ids = getAvailableCameraIds(3)
    print(ids)

    cam = Camera( 1,
            faces=face_cascade_path,
            eyes=eye_cascade_path,
            )
    return cam

def _check_if_window_inside(window_pos,monitor):
    dx = int(window_pos[0]) -int( monitor['x'])
    dy = int(window_pos[1]) - int(monitor['y'])
    if dx>0 and dy>0:
        if dx<int(monitor['width']) and dy<int(monitor['height']):
            return True

    return False

def get_active_monitor(monitors):
    for m in monitors:
        window_pos = get_active_window_position()
        if len(window_pos)>0:
            if _check_if_window_inside(window_pos,m):
                return m
        else:
            print('no window found')

def main():
    cam = init_face_cam()
    monitors = get_connected_monitors_info()
    while True:
        img = cam.read()
        f,e = cam.detect(img)
        f_img, e_img = cam.get_imgs(img,f,e)

        if len(f)>0:
            print("face")
        else:
            print("no face")
            continue

        act_mon = get_active_monitor(monitors)
        if act_mon:
            mon_name = act_mon['name']
            print('active mon',mon_name)
            if len(f)>0:
                face = f[0]

                data.save(e_img,f_img[0],mon_name)

        img = cam.draw_rects(img,f,e)
        cam.show(img)
        time.sleep(0.05)

    pass

if __name__=="__main__":
    main()
    parser = argparse.ArgumentParser(description='GUI?')
    parser.add_argument('--gui', action="store_true",default=False)
    parser.add_argument('--smiles', action="store_true",default=False)
    args = parser.parse_args()

    main()
