import numpy as np
import cv2
import sys

class HistogramColorClassifier:
    

    def __init__(self, channels=[0, 1, 2], hist_size=[128, 128, 128], hist_range=[0, 255, 0, 255, 0, 255], hist_type='BGR'):

        self.channels = channels
        self.hist_size = hist_size
        self.hist_range = hist_range
        self.hist_type = hist_type
        self.model_list = list()
        self.name_list = list()

    def addModelHistogram(self, model_frame, name=''):
        
        if(self.hist_type=='HSV'): model_frame = cv2.cvtColor(model_frame, cv2.COLOR_BGR2HSV)
        elif(self.hist_type=='GRAY'): model_frame = cv2.cvtColor(model_frame, cv2.COLOR_BGR2GRAY)
        elif(self.hist_type=='RGB'): model_frame = cv2.cvtColor(model_frame, cv2.COLOR_BGR2RGB)
        hist = cv2.calcHist([model_frame], self.channels, None, self.hist_size, self.hist_range)
        hist = cv2.normalize(hist, hist).flatten()
        if name == '': name = str(len(self.model_list))
        if name not in self.name_list:
            self.model_list.append(hist)
            self.name_list.append(name)
        else:
            for i in range(len(self.name_list)):
                if self.name_list[i] == name:
                    self.model_list[i] = hist
                    break


    def returnHistogramComparison(self, hist_1, hist_2, method='intersection'):
        if cv2.__version__.split(".")[0] == '3':
            if(method=="intersection"):
                comparison = cv2.compareHist(hist_1, hist_2, cv2.HISTCMP_INTERSECT)
            elif(method=="correlation"):
                comparison = cv2.compareHist(hist_1, hist_2, cv2.HISTCMP_CORREL)
            elif(method=="chisqr"):
                comparison = cv2.compareHist(hist_1, hist_2, cv2.HISTCMP_CHISQR)
            elif(method=="bhattacharyya"):
                comparison = cv2.compareHist(hist_1, hist_2, cv2.HISTCMP_BHATTACHARYYA)
            else:
                raise ValueError('[DEEPGAZE] color_classification.py: the method specified ' + str(method) + ' is not supported.')
        else:
            if(method=="intersection"):
                comparison = cv2.compareHist(hist_1, hist_2, cv2.cv.CV_COMP_INTERSECT)
            elif(method=="correlation"):
                comparison = cv2.compareHist(hist_1, hist_2, cv2.cv.CV_COMP_CORREL)
            elif(method=="chisqr"):
                comparison = cv2.compareHist(hist_1, hist_2, cv2.cv.CV_COMP_CHISQR)
            elif(method=="bhattacharyya"):
                comparison = cv2.compareHist(hist_1, hist_2, cv2.cv.CV_COMP_BHATTACHARYYA)
            else:
                raise ValueError('[DEEPGAZE] color_classification.py: the method specified ' + str(method) + ' is not supported.')
        return comparison/np.sum(hist_2)

    def returnHistogramComparisonArray(self, image, method='intersection'):
        
        if(self.hist_type=='HSV'): image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        elif(self.hist_type=='GRAY'): image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif(self.hist_type=='RGB'): image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        comparison_array = np.zeros(len(self.model_list))
        image_hist = cv2.calcHist([image], self.channels, None, self.hist_size, self.hist_range)
        image_hist = cv2.normalize(image_hist, image_hist).flatten()        
        counter = 0
        for model_hist in self.model_list:
            comparison_array[counter] = self.returnHistogramComparison(image_hist, model_hist, method=method)
            counter += 1
        return comparison_array


