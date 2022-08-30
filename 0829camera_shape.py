import cv2
import numpy as np
lower = np.array([30,40,200])   # 轉換成 NumPy 陣列，範圍稍微變小 ( 55->30, 70->40, 252->200 )
upper = np.array([90,100,255])  # 轉換成 NumPy 陣列，範圍稍微加大 ( 70->90, 80->100, 252->255 )
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Cannot receive frame")
        break
 
    img = cv2.resize(frame,(500,500),fx=0.7,fy=0.7)
    imgContour = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(img, 150, 200)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 4)
        area = cv2.contourArea(cnt)
        if area > 500:
            # print(cv2.arcLength(cnt, True))
            peri = cv2.arcLength(cnt, True)
            vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
            corners = len(vertices)#算有幾個頂點
            x, y, w, h = cv2.boundingRect(vertices)
            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 4)
            if corners == 3:
                cv2.putText(imgContour, 'triangle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif corners == 4:
                cv2.putText(imgContour, 'rectangle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif corners == 5:
                cv2.putText(imgContour, 'pentagon', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif corners >= 6:
                cv2.putText(imgContour, 'circle', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('imgContour', imgContour)

    if cv2.waitKey(1) == ord('q'):
        break       # 按下 q 鍵停止
cap.release()
cv2.destroyAllWindows()