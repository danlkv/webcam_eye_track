import cv2, os, time

folder = './data/'
img_folder = folder + 'img/'
data_file = folder + 'labels.csv'

def _folder_check(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def save(eyes,face,label):
    """
    Saves the data and label (monitor index)

    eyes: list[np.array]
    face: np.array
    label: str

    """
    ts = str(time.time()).replace('.','-')
    for i, eye in enumerate(eyes):
        _save_img(eye,
                '%s_eye_%d.png'%(ts, i)
                )

    _save_img(face, '%s_face.png'%ts)

    _save_data(ts+','+label)

def _save_data(data):
    with open(data_file, 'a+') as f:
        print("appending data %s"%data)
        f.write( data+'\n')


def _save_img(img,name):
    print("saving image %s"%name)
    filename= img_folder + name
    _folder_check(filename)
    cv2.imwrite(filename,img)


