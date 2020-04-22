import cv2
import numpy as np
import math
class Imaging:
    def image_resize(self,image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

    def undesired_objects (self, image):
        image = image.astype('uint8')
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(image, connectivity=8)
        sizes = stats[:, -1]

        max_label = 1
        max_size = sizes[1]

        print(nb_components)

        for i in range(2, nb_components):
            if sizes[i] > max_size:
                max_label = i
                max_size = sizes[i]

        img2 = np.zeros(output.shape)
        img2[output == max_label] = 255
        # cv2.imshow("Biggest component", img2)
        # cv2.waitKey()
        return img2


    def isolate(self, img):

        # cv2.imshow('def', img)
        # cv2.waitKey(0)

        kernel = np.ones((3,3), np.uint8)
        # norm_img = np.zeros(img.shape)
        # final_img = cv2.normalize(gray, norm_img, 0, 255, cv2.NORM_MINMAX)
        final_img = cv2.dilate(img,kernel,iterations = 1)
        # final_img = cv2.equalizeHist(final_img)

        # cv2.imshow('norm', final_img)
        # cv2.waitKey(0)

        # edges = cv2.Canny(img,100,200)
        # cv2.imshow('edges', edges)
        # cv2.waitKey(0)

        ret,thresh1 = cv2.threshold(final_img,100,255,cv2.THRESH_BINARY)
        thresh1 = (255-thresh1)

        # cv2.imshow('threshold', thresh1)
        # cv2.waitKey(0)


        thresh1 = self.undesired_objects(thresh1)

        # cv2.imshow('threshold', thresh1)
        # cv2.waitKey(0)

        kernel = np.ones((20,20),np.uint8)

        closing = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
        kernel = np.ones((10,10),np.uint8)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)


        # cv2.imshow('open', opening)
        # cv2.waitKey(0)

        # cv2.imshow('close', closing)
        # cv2.waitKey(0)

        final = self.undesired_objects(closing)

        # cv2.imshow('final', final)
        # cv2.waitKey(0)
        return final

    def getHeight(self, img):
        
        l = []
        for i in range(len(img)):
            l.append(self.hasAtRow(img, i))

        start  = -1
        stop = -1
        for x in range(len(l)):
            if l[x]:
                start = x
                break

        for x in range(len(l)):
            if l[-x]:
                stop = len(l) - x
                break
        
        return (stop - start, start, stop)

    def getWidthAt(self, img, i):
        count = 0

        for j in range(len(img[i])):
            if img[i][j] > 0:
                count += 1
        
        return count

    def removeToes(self, img):

        noToes = img.copy()

        height, startHeight, stopHeight = self.getHeight(img)

        offset = int(.2 * height)
        checkpoint = stopHeight - offset

        
        # minWidth = self.getWidthAt(img, checkpoint)
        minWidth = 0
        dist = math.floor((stopHeight - startHeight)/2)
        print(noToes[0][0])
        for i in range (dist):
            if self.getWidthAt(noToes,(startHeight + dist + i)) > minWidth:
                minWidth = self.getWidthAt(noToes, (startHeight + dist + i))

        print('minWidth',minWidth)

        count = 0
        prev = noToes[startHeight][0]

        for i in range(int(.2 * height)):
            for j in range(len(noToes[0])):
                if prev == noToes[startHeight+i][j]:
                    count += 1
                else:
                    if count < minWidth:
                        for k in range(count):
                            noToes[startHeight+i][j-k-1] = 0
                    count = 1

        return noToes


    def hasAtRow(self, img, j):
        for i in range(len(img[0])):
            if img[j][i] > 0:
                return True
        return False


    def calculateIndex(self, img):
        height, start, stop = self.getHeight(img)

        step = height/3

        a = 0
        b = 0
        c = 0

        for i in range(height):

            if i < step:
                a += self.getWidthAt(img, i+start)
            elif i < step*2:
                b += self.getWidthAt(img, i+start)
            else:
                c += self.getWidthAt(img, i+start)

        
        return (b / (a+b+c))

    def getIndex(self,path):
        img = cv2.imread(path)


        img = self.image_resize( img, height = 512)
        cv2.imshow('orig', img)
        cv2.waitKey(0)

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        # gray = cv2.GaussianBlur(gray, (15, 15), 1)
        # gray = cv2.medianBlur(gray,5)

        img = gray

        img = self.isolate(img)
        cv2.imshow('iso', img)
        cv2.waitKey(0)

        print (self.getHeight(img))

        toeless = self.removeToes(img)
        toeless = self.undesired_objects(toeless)
        cv2.imshow('toeless', toeless)
        cv2.waitKey(0)


        index = self.calculateIndex(toeless)
        print(index)

        newImg = path + 'processed.jpg'
        


        return index


imageOp = Imaging()
imageOp.getIndex('jeff.jpg')

# # High arch (AI≤0.21)
# Normal arch (AI between 0.21 and 0.26) and
# Low arch (AI≥0.26)