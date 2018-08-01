import cv2
import numpy as np

 
#binary encoder
text = raw_input("enter text: ")
ascii = ""
for i in range (0,len(text)):
    if(ord(text[i]) <= 63):
        ascii = ascii + "00" + bin(ord(text[i]))[2:]
    else:
        ascii = ascii  + "0" + bin(ord(text[i]))[2:]
print(ascii)



#pixel value
image = cv2.imread("C:\Users\User\Desktop\download.jpg")
size = image.shape
print(size)

# creating a blank image
enc_image = np.zeros((size[0], size[1], 3), np.uint8)
 
L = 0
for i in range(0,size[0]):
    for j in range(0,size[1]):
        if L < len(ascii)   :
            #print(bin(image[i,j,0]))
            red_bin = (bin(image[i,j,0])[2:])
            red_bin = red_bin[0:len(red_bin)-1] + ascii[L]
            enc_image[i,j,0] = int(red_bin, 2)
            enc_image[i,j,1] = image[i,j,1]
            enc_image[i,j,2] = image[i,j,2]
            L = L+1
        else:
            enc_image[i,j] = image[i,j]

cv2.imwrite('encoded_image1.png', enc_image)


dec_img = cv2.imread("encoded_image1.png")
size = dec_img.shape

message = ""
cur_char = ""
var2 = ""
flag = 1

for i in range(0, size[0]):
    for j in range(0, size[1]):
        if (cur_char != "!") :
            var1 = bin(dec_img[i,j,0])
            var2 = var2 + var1[len(var1)-1:]
            if(len(var2) == 8):
                #print(j,var2)
                cur_char = chr(int(var2, 2))
                message = message + cur_char
                var2 = ""
               
print(message)




                


            
