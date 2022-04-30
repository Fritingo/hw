import cv2 as cv
import numpy as np

def homography(input,projeced):
    # homography matrix
    matrix = []
    for i in range(4):
        matrix.append([-input[i][0],-input[i][1],-1,0,0,0,projeced[i][0]*input[i][0],projeced[i][0]*input[i][1],projeced[i][0]])
        matrix.append([0,0,0,-input[i][0],-input[i][1],-1,projeced[i][1]*input[i][0],projeced[i][1]*input[i][1],projeced[i][1]])
    # print(' ------- testing ------- ')
    # print(matrix)
    # print(' ------- testing ------- ')
    _, _, H = np.linalg.svd(np.array(matrix))
    H = np.reshape(H[-1],(3,3))
    H /= H[-1][-1]
    return H
    # print('+++++++++')
    # print(H)
    # H = H
    


def mouse_action(event, x, y, flags, replace_coordinate_array):
    cv.imshow('collect coordinate', img_dest_copy)
    if event == cv.EVENT_LBUTTONUP:
       
        cv.circle(img_dest_copy, (x, y), 2, (0, 255, 255), -1)

       
        replace_coordinate_array.append([x, y])


if __name__ == '__main__':
    
    img_src = cv.imread('puppy.jpg', cv.IMREAD_COLOR)
    h, w, c = img_src.shape
    
    img_src_coordinate = np.array([[x, y] for x in (0, w - 1) for y in (0, h - 1)])
   

  

   
    img_dest = cv.imread('background.png', cv.IMREAD_COLOR)
   
    img_dest_copy = np.tile(img_dest, 1)

   
    replace_coordinate = []
    cv.namedWindow('collect coordinate')
    cv.setMouseCallback('collect coordinate', mouse_action, replace_coordinate)
    while True:
        
        if cv.waitKey(20) == 27:
            break

    print(replace_coordinate)

    replace_coordinate = np.array(replace_coordinate)


    matrix = homography(img_src_coordinate, replace_coordinate)
    perspective_img = cv.warpPerspective(img_src, matrix, (img_dest.shape[1], img_dest.shape[0]))
    cv.imshow('img', perspective_img)

   
    retval, threshold_img = cv.threshold(perspective_img, 0, 255, cv.THRESH_BINARY)
  
    cv.copyTo(src=threshold_img, mask=np.tile(threshold_img, 1), dst=img_dest)
    cv.copyTo(src=perspective_img, mask=np.tile(perspective_img, 1), dst=img_dest)
    cv.imshow('result', img_dest)
    cv.imwrite('310832007.jpg',img_dest)
    cv.waitKey()
    cv.destroyAllWindows()