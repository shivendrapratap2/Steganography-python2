from PIL import Image
import cv2
import numpy as np
import math
        
class Node():

    def __init__(self, char, freq, left_node, right_node):
        self.char = char
        self.freq = freq
        self.left = left_node
        self.right = right_node


    
#Traversal.............................
    
def walk_tree(node, prefix="", code={}):
    if isinstance(node.left, Node):
        walk_tree(node.left, prefix+"0", code)
    else:
        code[node.char] = prefix
    if isinstance(node.right, Node):
        walk_tree(node.right, prefix+"1", code)
    else:
        code[node.char]=prefix
    return(code)
        
 
#Creating BMP file......................

image = cv2.imread("test_image.jpg", cv2.IMREAD_GRAYSCALE)
h, w = image.shape[0], image.shape[1]

height = h
width = w
h = np.float32(h) 
w = np.float32(w) 

nbh = math.ceil(h/8)
nbh = np.int32(nbh)

nbw = math.ceil(w/8)
nbw = np.int32(nbw)

H =  8 * nbh

W =  8 * nbw

padded_img = np.zeros((H,W))

padded_img[0:height,0:width] = image[0:height,0:width]

cv2.imwrite('uncompressed.bmp', np.uint8(padded_img))
image = cv2.imread("uncompressed.bmp")

# creating frequency fie...............................

pix_freq = [0]*256
for i in range(h):
    for j in range(image.shape[1]):
        pix_freq[image[i,j,0]] += 1

#creating haffmann tree................................
        
ls = []
for i in range(0,256):
    if pix_freq[i] != 0:
        ls.append(Node(i, pix_freq[i], None, None))
ls = sorted(ls, key=lambda x: (x.freq))

size = len(ls)
for i in range(0, 2*(size-1), 2):
    ls.append(Node("IN", ls[i].freq + ls[i+1].freq, ls[i], ls[i+1]))
    ls = sorted(ls, key=lambda x: (x.freq))
        
root = ls[len(ls)-1]


code = walk_tree(root, "", {})

# string of hufmann codes for respective pixel values....

encoded_msg = ""
f = open("compressed.txt", "wb+")
for i in range(h):
    for j in range(w):
        encoded_msg += code[image[i,j,0]]

# writing into file......................................

l = len(encoded_msg)/8
print(l)
s = bytearray(0)
for i in range(0, l+1):
    if i == l:
        num = int(encoded_msg[i*8:], 2)
        s.insert(i, num)
    else:
        num = int(encoded_msg[i*8:(i+1)*8], 2)
        s.insert(i, num)
        
f.write(s)
f.close()

# Decoding.............................................

# Pending
    
