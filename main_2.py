import cv2
from button_gui import Buttons

#OpenCV DNN
net = cv2.dnn.readNet("deepFaceDetection/openCV_detection/dnn_model/yolov4-tiny.cfg", "deepFaceDetection/openCV_detection/dnn_model/yolov4-tiny.weights")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(412,412), scale=1/255)

#load class list
classes = []
with open("deepFaceDetection/openCV_detection/dnn_model/classes.txt","r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

#initialize buttons
button = Buttons()
button.add_button(20,20)
colors = button.colors

#initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


#mouse click to detect
def click_button(event, x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDOWN:
        button.button_click(x,y)

cv2.namedWindow("Window")
cv2.setMouseCallback("Window", click_button)


while True:
    success, frame = cap.read()
    frame = cv2.flip(frame,1) #flipping the frame

    # if frame is read correctly ret is True
    if not success:
        print("You know? This is not sucessful!")
        break

    #get active button
    # active_buttons = button.active_buttons_list()

    #object detection
    if button.get_detection_status():
        (class_id, scores, bboxes) = model.detect(frame)
        for class_id,scores, bboxes in zip(class_id, scores, bboxes):
            (x,y,w,h) = bboxes
            class_name = classes[class_id]
            # print(x,y,w,h)
            cv2.putText(frame, class_name, (x,y -10), cv2.FONT_HERSHEY_PLAIN, 2,(0,150,200),3)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,150,200),2)

    # print("class_id:", class_id)
    # print("scores:", scores)
    # print("bboxes:", bboxes)

    button.display_buttons(frame)

    cv2.imshow("Window", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()