import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

curr_directory = os.getcwd()
total_error=[]
db_path = os.path.join(curr_directory, "images", "bw")
count=[]
i=0

for filename in os.listdir(db_path):

    extension = os.path.splitext(filename)[1]
    mesh_name = os.path.splitext(filename)[0]

    image_original = cv2.imread(os.path.join(db_path, filename),0)
    image = cv2.bitwise_not(image_original)

    area_2 = cv2.countNonZero(image)


    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #for making image 3 channeled, optional
    disp = cv2.merge((image, image, image))

    disp = cv2.drawContours(disp, contours, -1, hierarchy=hierarchy, color=(0, 255, 0),thickness=5)



    cnt = contours[0]
    area_1 = cv2.contourArea(cnt)



    #area
    total_rows , total_cols = image.shape
    #countnonzero = white pixels

    error=abs(area_2-area_1)

    print(str(area_1) + "      " +str(area_2) + "        "+ str(i) + "       "+ str(error))


    cv2.imshow("disp",disp)
    cv2.waitKey(0)

    total_error.append(error)
    count.append(i)
    i+=1

plt.plot(count, total_error)
plt.title('error')
plt.xlabel('cnt')
plt.ylabel('error')
plt.show()