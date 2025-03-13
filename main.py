import cv2
import pickle
import numpy as np

windowName = "Video"
windowNameBlur = f"{windowName}Blur"
windowNameThres = f"{windowName}Thres"
windowNameMedian = f"{windowName}Median"
cap = cv2.VideoCapture('carPark.mp4')
width, height = 107, 48
roxo = (255, 0, 255)
verde = (15, 255, 0)

try:
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
except (FileNotFoundError, pickle.UnpicklingError):
    posList = []


def check_parking_space():
    for pos in posList:
        x, y = pos
        img_crop = img[y:y+height, x:x+width]
        cv2.imshow(str(x*y), img_crop)


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, interations=1)

    check_parking_space()

    for posi in posList:
        cv2.rectangle(img, posi, (posi[0] + width, posi[1] + height), verde, 2)

    cv2.imshow(windowName, img)
    cv2.imshow(windowNameBlur, imgBlur)
    cv2.imshow(windowNameThres, imgThreshold)
    cv2.imshow(windowNameMedian, imgMedian)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# cv2.destroyAllWindows()
