import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.5, maxHands=2)

while True:
    success , img = cap.read()
    hands, img = detector.findHands(img)
    
    if hands:
        # Hand 1 code
        hand1 = hands[0]
        lmlist_hand1 = hand1["lmList"] # Gives a list of 21 landmark points
        bbox_hand1 = hand1["bbox"] # Info on bounding boxes (x and y coordinates + width & height)
        center_hand1 = hand1["center"] # gives the center of the hand
        hand1_type = hand1["type"] # left or right hand
        
        fingers_hand1 = detector.fingersUp(hand1)
        
        # length, info, img = detector.findDistance(lmlist_hand1[8][:2], lmlist_hand1[12][:2], img)
        

        # print(len(lmlist_hand1), lmlist_hand1)
        # print(len(bbox_hand1), bbox_hand1)
        # print(len(center_hand1), center_hand1)
        # print(hand1_type)
        # print(fingers_hand1)
        
        if len(hands) == 2:
            # Hand 2 code
            hand2 = hands[1]
            lmlist_hand2 = hand2["lmList"] # Gives a list of 21 landmark points
            bbox_hand2 = hand2["bbox"] # Info on bounding boxes (x and y coordinates + width & height)
            center_hand2 = hand2["center"] # gives the center of the hand
            hand2_type = hand2["type"] # left or right hand
            
            fingers_hand2 = detector.fingersUp(hand2)
            
            # length, info, img = detector.findDistance(lmlist_hand1[8][:2], lmlist_hand2[8][:2], img)
            
            
            # print(len(lmlist_hand2), lmlist_hand2)
            # print(len(bbox_hand2), bbox_hand2)
            # print(len(center_hand2), center_hand2)
            # print(hand1_type, hand2_type)
            # print(fingers_hand2)
    cv2.imshow("Live Feed", img)
    cv2.waitKey(1)
    