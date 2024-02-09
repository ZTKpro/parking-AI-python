import cv2
import cvzone
import numpy as np
import pickle

cap = cv2.VideoCapture("carPark.mp4")

with open("positions", "rb") as file:
    pos_list = pickle.load(file)

width, height = 107, 48


def check_parking_space(img_processed):
    available_places = 0

    for pos in pos_list:
        x, y = pos
        img_crop = img_processed[y : y + height, x : x + width]

        count = cv2.countNonZero(img_crop)
        cvzone.putTextRect(
            frame,
            str(count),
            (x, y + height - 3),
            scale=1,
            colorR=(255, 0, 0),
            offset=5,
        )

        if count < 750:
            available_places += 1
            color = (0, 255, 0)
            thickness = 3
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(
            frame,
            pt1=(x, y),
            pt2=(x + width, y + height),
            color=color,
            thickness=thickness,
        )
        cvzone.putTextRect(
            frame,
            f"Free {str(available_places)} / {len(pos_list)}",
            (400, 50),
            scale=3,
            colorR=(0, 255, 0),
            offset=5,
        )


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 1)
    threshold = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16
    )
    median = cv2.medianBlur(threshold, 7)
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(median, kernel, iterations=1)

    check_parking_space(dilation)

    cv2.imshow("Car Parking Counter", frame)

    key = cv2.waitKey(10)
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()