import cv2


#######################################################
cap = cv2.VideoCapture("../Part1.mp4")

# object_detector_withoutShadow = cv2.bgsegm.createBackgroundSubtractorMOG()
object_detector_withShadow = cv2.createBackgroundSubtractorMOG2();
detections = []
# result = cv2.VideoWriter('objectDetectionTest.avi', 
#                          cv2.VideoWriter_fourcc(*'MJPG'),
#                          10, (960, 540))

while True:
    ret, frame = cap.read()

    #Extract Region of interest
    columns = 4
    rows = 2
    height, width, _ = frame.shape
    cellWidth = width/columns;
    cellHeight = height/rows;
  

    #object detection
    # grey = apply_brightness_contrast(frame, 50, 10)
    mask1 = object_detector_withShadow.apply(frame)
    # mask2 = object_detector_withoutShadow.apply(frame)

    _, mask1 = cv2.threshold(mask1, 254, 255, cv2.THRESH_BINARY)
    contours1, _ = cv2.findContours(mask1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours2, _ = cv2.findContours(mask2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours1:
        area = cv2.contourArea(cnt)
        if area > 3000:
            # cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # result.write(cv2.resize(frame, (960, 540)))
    # for cnt in contours2:
    #     area = cv2.contourArea(cnt)
    #     if area > 500:
    #         x, y, w, h = cv2.boundingRect(cnt)
    #         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    ############################################################################################


    imS = cv2.resize(frame, (960, 540))             # Resize image
    cv2.imshow("output", imS)                       # Show image
    # for y in range(0, rows):
    #     for x in range(0, columns):
    #       ROI = frame[int(x*cellWidth):int((x+1)*cellWidth), int(y*cellHeight):int((y+1)*cellHeight)];
    #       cv2.imshow("frame"+str(y)+str(x), ROI)


    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

#######################################################
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):
    
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf
