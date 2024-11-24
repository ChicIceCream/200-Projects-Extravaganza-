import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

while True:
    success , img = cap.read()
    hands, img = detector.findHands(img)
    
    if hands:
        # Hand 1 code
        hand1 = hands[0]
        lmlist_hand1 = hand1["lmList"] # Gives a list of 21 landmark points
        bbox_hand1 = hand1["bbox"] # Info on bounding boxes 
        center_hand1 = hand1["center"] # gives the center of the hand
        
    
    cv2.imshow("Live Feed", img)
    cv2.waitKey(1)
    