import numpy as np
import cv2

# outputs list textreg_list (a list of text regions)
# each item has format (x,y,w,h) which represent column, row, width, height
def localizeText(_base_img):
    bgr_img = _base_img.copy()
    base_img = cv2.cvtColor(_base_img, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    grad = cv2.morphologyEx(base_img, cv2.MORPH_GRADIENT, kernel) 
    ret, thres = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,1))
    connect = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)
    ret, contours, hier = cv2.findContours(connect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask = np.zeros(thres.shape, dtype=np.uint8)
    
    # apply opening -> erosion followed by dilation
    #kernel = np.ones((5,5), np.uint8)
    ##denoise = cv2.morphologyEx(base_img, cv2.MORPH_OPEN, kernel)

    #ret, thresh = cv2.threshold(base_img, 127, 255, 0)
    ##gauss_thresh = cv2.adaptiveThreshold(base_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    #dilate = cv2.dilate(thresh, kernel, iterations=1)
    #dilate = cv2.blur(dilate, (3,3))
    #c_img, contours, hier = cv2.findContours(dilate, 0, 1)

    ##cv2.drawContours(base_img, contours, -1, (255,255,255), 3)
    textreg_list = []
    idx = 0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)

        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, idx, (255,255,255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)

        if r > 0.45 and w > 8 and h > 8:
            cv2.rectangle(bgr_img, (x,y),(x+w-1,y+h-1), (0,125,0), 2)
            textreg_list.append((x,y,w,h))

        #if x == 0 & y == 0:
        #    continue
        #cv2.rectangle(bgr_img, (x,y),(x+w,y+h), (0,125,0), 2)
        #textreg_list.append((x,y,w,h))
        idx += 1

    #base_img = cv2.GaussianBlur(base_img, (5,5), 0)
    #edges = cv2.Canny(base_img, 100, 200)

    cv2.imshow('clr', bgr_img)
    #cv2.imshow('base', connect)
    #cv2.imshow('img', thres)
    #cv2.imshow('dil', dilate)

    return textreg_list

def extractBackgnd(_regionsList, _img):
    regions = _regionsList
    img = _img.copy()


    #ret, thres = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #ret, contours, hier = cv2.findContours(thres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for reg in regions:
        x = reg[0]
        y = reg[1]
        w = reg[2]
        h = reg[3]
        # kernel size can be adjusted

        b_avg = 0
        g_avg = 0
        r_avg = 0
        for b,g,r in img[y:y+h-1, x+w]:
            b_avg += b
            g_avg += g
            r_avg += r
        b_avg /= h
        g_avg /= h
        r_avg /= h

        img[y:y+h-1, x:x+w-1] = (b_avg, g_avg, r_avg)
        img[y:y+h-1, x:x+w-1] = cv2.medianBlur(img[y:y+h-1, x:x+w-1], 45)
        

    return img

#testimg = cv2.imread('testfiles/menu5.jpg')
testimg = cv2.imread('testfiles/menu4.png')

rect = localizeText(testimg)
print(*rect, sep='\n')

cv2.imshow('bkgd', extractBackgnd(rect, testimg))
cv2.waitKey()