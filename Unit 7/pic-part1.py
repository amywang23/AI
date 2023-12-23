#27-color naïve quantization: Take each pixel in turn. For R, G, and B individually, if the value is less than
#255 // 3, make it 0. If it’s greater than 255 * 2 // 3, make it 255. Otherwise, make it 127.
#• 8-color naïve quantization: Take each pixel in turn. For R, G, and B individually, if the value is less than 128,
#make it 0. If it’s greater or equal, make it 255

from PIL import Image



def  vector_quantization(img, pix, method):
    for i in range (img.size[0]):
        for j in range (img.size[1]):
            color = pix[i,j]
            newcolor = [-1,-1,-1]
            if (method == 27):
                for ii in range(3):
                    if (color[ii] < 255/ 3):
                        newcolor[ii] = 0
                    elif (color[ii] > 255*2/3):
                        newcolor[ii] = 255
                    else:
                        newcolor[ii] = 127
            if (method == 8):
                for ii in range(3):
                    if (color[ii] < 128):
                        newcolor[ii] = 0
                    else:
                        newcolor[ii] = 255
            pix[i,j] = (newcolor[0],newcolor[1],newcolor[2])
            
    return img

img = Image.open("beach.jpeg") 
img.show() 

# print(img.size) # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
# print(pix[2,5]) # Access the color at a specific location; note [x, y] NOT [row, column].
# pix[2,5] = (255, 255, 255) # Set the pixel to white. Note this is called on “pix”, but it modifies “img”.


img = vector_quantization(img, pix, 8)
img.show() # Now, you should see a single white pixel near the upper left corner
img.save("part1-8.png") # Save the resulting image. Alter your filename as necessary.
