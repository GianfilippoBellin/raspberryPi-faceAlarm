import imutils
import numpy as np
import cv2 as cv
from imutils.object_detection import non_max_suppression


from Models.CallProvider import CallProvider
from Models.Connections import FramesConnection


class Detector:
    __classifier = None
    class_detection = ""
    n_frames = 20

    def getRects(self, frame):
        return []

    def showFrame(self, frame):
        frame = imutils.resize(frame)
        cv.imshow("Detector", frame)
        cv.waitKey(1)

    def find(__db_frames):

        # class which permit to save frames
        f = FramesConnection()

        # class which call directly the phones of clients in case of detection
        cp = CallProvider()

        # variable which
        one_shot = True

        # open the cam in read mode
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        # counter of consecutive faces detected in the frames
        i = 0

        while True:
            ret, frame = cap.read()

            # no frames stop
            if not ret:
                break

            # transformation from RGB to Gray chanel
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            rect = __db_frames.getRects(frame)

            for (x, y, w, h) in rect:
                # put the rectangles in the image
                cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # put the text in the frames
                cv.putText(frame, __db_frames.class_detection, (x, y - 10), cv.FONT_ITALIC, 0.9, (36, 255, 12), 2)

            # count the number of faces detected
            n_face = len(rect)
            i += 1

            # reset false positive face
            if n_face == 0:
                i = 0

            if i > __db_frames.n_frames:
                #cp.doCall()
                i = 0

            # check if there are faces
            is_face = (n_face > 0)

            # post the frames
            if is_face and one_shot:
                # TODO: find the correct format of frames for mongoDB
                f.post("face", is_face)
                one_shot = False

            __db_frames.showFrame(frame)


class DetectorFace(Detector):
    class_detection = "Face"
    path_mask = 'rsc/haarcascade_frontalface_default.xml'

    def __init__(self, scale_factor=1.1, min_neighbors=5):
        self.__classifier = cv.CascadeClassifier(self.path_mask)
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors

    def getRects(self, frame):
        return self.__classifier.detectMultiScale(frame, self.scale_factor, self.min_neighbors)


class DetectorPedestrian(Detector):
    class_detection = "Pedestrian"

    def __init__(self, win_stride=(4, 4), padding=(8, 8), scale=1.05, probs=None, overlap_thresholding=0.50):
        self.__classifier = cv.HOGDescriptor()
        self.__classifier.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
        self.win_stride = win_stride
        self.padding = padding
        self.scale = scale
        self.probs = probs
        self.overlap_trasholding = overlap_thresholding

    def getRects(self, frame):
        # detect people in the gray frame
        rects, _ = self.__classifier.detectMultiScale(frame, winStride=self.win_stride, padding=self.padding,
                                                      scale=self.scale)

        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=self.probs, overlapThresh=self.overlap_trasholding)
        return pick
