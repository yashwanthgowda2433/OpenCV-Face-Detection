import cv2
print("package imported")

# img = cv2.imread("resources/image.png")
# cv2.imshow("Output", img)
# cv2.waitKey(0)

# cap = cv2.VideoCapture("resources/test.mp4")
# while True:
#     success, img = cap.read()
#     cv2.imshow("Video", img)
#     if cv2.waitKey(1) & 0xFF ==ord('q'):
#         break


cap = cv2.VideoCapture(0)
cap.set(3,640)#width
cap.set(4,480)#height
cap.set(10,100)#brightness
while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break