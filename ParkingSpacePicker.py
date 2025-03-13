import cv2
import pickle


# cv2.rectangle(img, (x1, y1), (x2, y2), (b, g, r), bitola da borda)
# x1 canto superior esquerdo
# y1 linha vertical
# x2 canto inferior direito
# x2 linha vertical
windowName = "Imagem"
width, height = 107, 48
posList = []

azul = (255, 16, 15)

try:
    with open('carParkPos', 'rb') as f:
        posList = pickle.load(f)
except (FileNotFoundError, pickle.UnpicklingError):
    posList = []


def mouse_click(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, posi in enumerate(posList):
            x1, y1 = posi
            if x1 < x < x1+width and y1 < y < y1+height:
                posList.pop(i)

    with open('carParkPos', 'wb') as arquivo:
        pickle.dump(posList, arquivo)


while True:
    img = cv2.imread('carParkImg.png')
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0]+width, pos[1] + height), azul, 2)
        # cv2.rectangle(img, (50, 192), (157, 240), (255, 16, 15), 2)

    cv2.imshow(windowName, img)
    cv2.setMouseCallback(windowName, mouse_click)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
