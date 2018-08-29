import cv2
import sys
import math
import numpy as np

#####################################################################

keep_processing = True;
camera_to_use = 1; # 0 if you have one camera, 1 or > 1 otherwise

cnn_model_to_load = "MobileNetSSD_deploy";

#####################################################################

# define video capture object

cap = cv2.VideoCapture();

fourcc = cv2.VideoWriter_fourcc(*'XVID')
#fourcc = cv2.VideoWriter_fourcc(*'X264')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (720,720), True);

# define display window name

windowName = "Live Object Detection - CNN: " + cnn_model_to_load; # window name

# if command line arguments are provided try to read video_name
# otherwise default to capture from attached camera

if (((len(sys.argv) == 2) and (cap.open(str(sys.argv[1]))))
    or (cap.open(camera_to_use) or cap.open(camera_to_use - 1))):

    # create window by name (as resizable)

    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL);

    # init CNN model - here from Caffe

    net = cv2.dnn.readNetFromCaffe(cnn_model_to_load + ".prototxt", cnn_model_to_load + ".caffemodel");

    # provide mappings from class numbers to string labels

    classNames = {  0: 'background',
                    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
                    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
                    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
                    14: 'motorbike', 15: 'person', 16: 'pottedplant',
                    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' };

    while (keep_processing):

        # start a timer (to see how long processing and display takes)

        start_t = cv2.getTickCount();

        # if video file successfully open then read frame from video

        if (cap.isOpened):
            ret, frame = cap.read();

            #print(frame.shape)

            # when we reach the end of the video (file) exit cleanly

            if (ret == 0):
                keep_processing = False;
                continue;

        # transform the image into a network input "blob" (i.e. tensor)
        # by scaling the image to the input size of the network, in this case
        # not swapping the R and G channels (i.e. used when network trained on
        # RGB and not the BGR of OpenCV) and re-scaling the inputs from 0->255
        # to 0->1 by specifing the mean value for each channel

        swapRBchannels = False;             # do not swap channels
        meanChannelVal = 255.0 / 2.0;       # mean channel value

        inWidth = 300;     #300                 # network input width
        inHeight = 300;     #300                # network input height
        WHRatio = inWidth / float(inHeight);
        inScaleFactor = 0.007843;           # input scale factor


        cols = frame.shape[1]
        rows = frame.shape[0]


        if cols / float(rows) > WHRatio:
            cropSize = (int(rows * WHRatio), rows);
        else:
            cropSize = (cols, int(cols / WHRatio));

        y1 = int((rows - cropSize[1]) / 2);
        y2 = y1 + cropSize[1];
        x1 = int((cols - cropSize[0]) / 2);
        x2 = x1 + cropSize[0];
        frame = frame[y1:y2, x1:x2];

        blob = cv2.dnn.blobFromImage(frame, inScaleFactor, (inWidth, inHeight),
                (meanChannelVal, meanChannelVal, meanChannelVal), swapRBchannels);

        # set this transformed image -> tensor blob as the network input

        net.setInput(blob);

        # perform forward inference on the network

        detections = net.forward();

        # process the detections from the CNN to give bounding boxes

        # firstly recompute the frame size / crop based on the input send to the CNN

        cols = frame.shape[1]
        rows = frame.shape[0]

        # print("co, row :",cols, rows)

        # if cols / float(rows) > WHRatio:
        #     cropSize = (int(rows * WHRatio), rows);
        # else:
        #     cropSize = (cols, int(cols / WHRatio));

        # y1 = int((rows - cropSize[1]) / 2);
        # y2 = y1 + cropSize[1];
        # x1 = int((cols - cropSize[0]) / 2);
        # x2 = x1 + cropSize[0];
        # frame = frame[y1:y2, x1:x2];

        # for each detection returned from the network

        for i in range(detections.shape[2]):

            # extract the confidence of the detection

            confidence = detections[0, 0, i, 2];

            # provided that is above a threshold (0.2)

            if confidence > 0.8:

                # get the class number id and the bounding box

                class_id = int(detections[0, 0, i, 1]);

                xLeftBottom = int(detections[0, 0, i, 3] * cols);
                yLeftBottom = int(detections[0, 0, i, 4] * rows);
                xRightTop   = int(detections[0, 0, i, 5] * cols);
                yRightTop   = int(detections[0, 0, i, 6] * rows);

                # print(frame.shape)

                # draw the bounding box on the frame

                cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop),
                              (0, 255, 0));

                # look up the class name based on the class id and draw it on the frame also

                if class_id in classNames:
                    label = classNames[class_id] + ": " + str(confidence)
                    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1);

                    yLeftBottom = max(yLeftBottom, labelSize[1]);
                    cv2.rectangle(frame, (xLeftBottom, yLeftBottom - labelSize[1]),
                                         (xLeftBottom + labelSize[0], yLeftBottom + baseLine),
                                         (255, 255, 255), cv2.FILLED)
                    cv2.putText(frame, label, (xLeftBottom, yLeftBottom),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0));

        # display image
        out.write(frame);
        # print(frame.shape)
        cv2.imshow(windowName,frame);

        # stop the timer and convert to ms. (to see how long processing and display takes)

        stop_t = ((cv2.getTickCount() - start_t)/cv2.getTickFrequency()) * 1000;

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in milliseconds).
        # It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of multi-byte response)
        # here we use a wait time in ms. that takes account of processing time already used in the loop

        # wait 40ms or less depending on processing time taken (i.e. 1000ms / 25 fps = 40 ms)

        key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF;

        # It can also be set to detect specific key strokes by recording which key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False;

    # close all windows
    cap.release()
    out.release()
    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.");