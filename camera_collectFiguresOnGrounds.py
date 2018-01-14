from picamera.array import PiRGBArray
from picamera import PiCamera
import picamera
import matplotlib.pyplot as plt
import time
import cv2
import io
from lane_lines import annotate_image_array
import sys
import numpy as np      
from detectImage import *
from lane_lines import *
def binLane(img):
    src = np.array([[26,96], [53,60], [96,60], [140,96]]).astype(np.float32) 
    dst = np.array([[21,95], [21,-20],[116,-20],[116,95]]).astype(np.float32) 
    M    = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    #img2 = (img[:,:,2]>120).astype(np.uint8)
    #ii = cv2.Canny(img[:,:,2], 150, 200)
    #ii2 = cv2.GaussianBlur(ii, (3, 3), 0)
    #ii2[np.arange(0,15),:] = 0
    
    img_t = cv2.warpPerspective(img[:,:,1], M, (128, 96), cv2.WARP_INVERSE_MAP)
    return img_t

refPos = [50,200]
initParams = [
        np.linspace(0.001, 0.02, 10),
        np.array(list(np.linspace(1.5, 10, 10)) + list(np.linspace(-30, -1.5, 10))),
        np.arange( 23, 28, 2),
        np.arange(-25, 25, 3)
]

def camera_main2(share_obj, obj_b):
    print('AAsAA')
    with picamera.PiCamera() as camera:
        #camera.start_preview()
        camera.resolution = (640, 480)
        # time.sleep(0.5)
        idx = 0
        paramSearch = None
        seedParams = []
        l_errors = []
        paramSearch = initParams
        print('AAAA')
        with picamera.array.PiRGBArray(camera) as stream:
            print("BBB")
            while 1:
                #print(idx)
                camera.capture(stream, format='bgr')
                # At this point the image is available as stream.array
                img = stream.array
                img = cv2.resize(img, (128,96))
                img = img[:,:,::-1]
                output_file = "./testFigures4/output_image.%d.%d.jpg" % ( int(time.time()), idx)
                idx += 1
                
                img[np.arange(0,30),:,:] = 0
                img[np.arange(40,96),:,:] = 0
                img[:,np.arange(0,50),:] = 0
                img[:,np.arange(120,128),:] = 0
                # plt.imsave(output_file, img)
    
                idx_red = (img[:,:,0]>200)*(img[:,:,1]<130)*(img[:,:,2]<130)
                idx_yellow = (img[:,:,0]>200)*(img[:,:,1]>120)*(img[:,:,2]<100)
                sum_redIdx = np.sum(idx_red)
                sum_yellowIdx = np.sum(idx_yellow)
                if sum_redIdx > 10:
                    sum_redIdx = 0

                if sum_yellowIdx > 10:
                    sum_yellowIdx = 0

                share_obj.value = sum_redIdx# + sum_yellowIdx
                print('result:', sum_redIdx, sum_yellowIdx, share_obj.value)
                #print('result:', sum_redIdx, sum_yellowIdx, share_obj.value)
                # plt.imsave(output_file + ".yellow.png", img_yellow)
                
                
                
                
                '''
                img_cvt = binLane(image)
                kernel = np.ones([5,5])
                img_cvt_high = cv2.dilate(
                    ((cv2.resize(img_cvt, (100,200))>150)*255).astype(np.uint8), kernel,iterations = 1
                )
                img3 = np.zeros([200,100,3])
                img3[:,:,0] = img_cvt_high
                img3[:,:,1] = img_cvt_high
                img3[:,:,2] = img_cvt_high
                img_lane = annotate_image_array(img3.astype(np.uint8), median_shift_obj)
                plt.imsave(output_file, img_lane)
                
                if len(seedParams) == 0:
                    paramSearch = initParams
                else:
                    lla = np.linspace(seedParams[0]-(initParams[0][1]-initParams[0][0])*15,
                                    seedParams[0]+(initParams[0][1]-initParams[0][0])*15, 5)
                    llb = np.linspace(seedParams[1]-(initParams[1][1]-initParams[1][0]),
                                    seedParams[1]+(initParams[1][1]-initParams[1][0]), 3)
                    llc = [seedParams[2]-2, seedParams[2]+2, seedParams[2]]
                    lld = [seedParams[3]-2, seedParams[3]+2, seedParams[3]]
                    paramSearch = [lla, llb, llc, lld]
        
                coords,params = getBestParams(img_cvt_high, paramSearch, refPos)
                score = params[4]
                if score < 25:
                    seedParams = []
                    prevVal = 0
                    if len(l_errors)>0:
                        prevVal = l_errors[-1]
                    l_errors.append(prevVal)

                else:
                    d = params[3]
                    seedParams = params
                    d = PrevFilter(d, l_errors)
                    l_errors.append(d)
        
                print(l_errors[-1])
                '''
                stream.truncate(0)


                #forward_left = int(sys.argv[1])
                #forward_right = int(sys.argv[2])
                #car.set_speed(forward_left, forward_right)
                                        
    #except KeyboardInterrupt:
    #    car.__del__()

if __name__ == '__main__':
    camera_main2()
