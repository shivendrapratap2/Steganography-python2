import cv2
import numpy as np
from matplotlib import pyplot as plt
from color_classification import HistogramColorClassifier

#Defining the classifier
my_classifier = HistogramColorClassifier(channels=[0,1,2], hist_size=[128,128,128], hist_range=[0, 256, 0, 256, 0, 256], hist_type='BGR')

model_1 = cv2.imread('histointersection sample\CoverT4.bmp')


my_classifier.addModelHistogram(model_1)



image = cv2.imread('histointersection sample\StegoT4.bmp')


comparison_array = my_classifier.returnHistogramComparisonArray(image, method="bhattacharyya")



print("Comparison Array:")
print(comparison_array)


total_objects = 1
label_objects = ('stego match')
font_size = 10
width = 0.5 
plt.barh(np.arange(total_objects), comparison_array, width, color='b')
plt.yticks(np.arange(total_objects) + width/2.,label_objects , rotation=0, size=font_size)
plt.xlim(0.0, 1.0)
plt.ylim(-0.5, 5.0)
plt.xlabel('Matching Probability', size=font_size)
figManager = plt.get_current_fig_manager()
#figManager.window.showMaximized()
plt.show()

