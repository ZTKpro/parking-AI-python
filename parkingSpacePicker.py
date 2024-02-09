import cv2
import pickle

try:
    with open("positions", "rb") as file:
        pos_list = pickle.load(file)
except:
    pos_list = []

width, height = 107, 48


def mouse_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        pos_list.append((x, y))

    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(pos_list):
            if pos[0] < x < pos[0] + width and pos[1] < y < pos[1] + height:
                pos_list.pop(i)


# Load saved positions from a file if it exists
try:
    with open("positions.pkl", "rb") as file:
        pos_list = pickle.load(file)
except FileNotFoundError:
    pass

while True:
    img = cv2.imread("example_image.png")

    for pos in pos_list:
        cv2.rectangle(
            img,
            pt1=pos,
            pt2=(pos[0] + width, pos[1] + height),
            color=(0, 255, 0),
            thickness=2,
        )

    cv2.imshow("Car Park", img)
    cv2.setMouseCallback("Car Park", mouse_click)
    key = cv2.waitKey(1)

    with open("positions", "wb") as file:
        pickle.dump(pos_list, file)

    # Break the loop when 'q' key is pressed
    if key == ord("q"):
        break

cv2.destroyAllWindows()