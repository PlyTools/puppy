import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import pickle
import settings


# 棋盘图信息
n_row = 6    # 棋盘图角点的行数
n_col = 9    # 棋盘图角点的列数

# 校正图片所在文件
images_path = "calibrate_images"


def calibrate(filename, silent = True):

    objp = np.zeros((n_row * n_col, 3), np.float32)
    objp[:, :2] = np.mgrid[0:n_col, 0:n_row].T.reshape(-1, 2)

    '''
        初始化棋盘图的角点的对象坐标，如
        (0, 0), (0, 1), ... ,(0, n_col-1), 
        (1, 0), (1, 1), ... ,(1, n_col-1) , 
        (2, 0), (2, 1), ... ,(2, n_col-1),
        ..., 
        (n_row-1, 0), (n_row-1, 1), ... ,(n_row-1, n_col-1)

    '''
    object_points = []
    '''
        初始化棋盘图的角点的像素坐标，各个坐标为具体像素点位置
    '''
    image_points = []

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # 通过循环遍历所有校正图像
    for image_file in os.listdir(images_path):
        if image_file.endswith("jpg"):
            # turn images to grayscale and find chessboard corners
            img = cv2.imread(os.path.join(images_path, image_file))
            img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            found, corners = cv2.findChessboardCorners(img_gray, (n_col, n_row))
            print("%s to find all corners in %s" % ("Success" if found else "Fail", image_file))
            if found:
                # 在将角点像素坐标加入列表前，微调以获取更精确的像素坐标位置
                cv2.drawChessboardCorners(img, (n_col, n_row), corners, found)
                corners2 = cv2.cornerSubPix(img_gray, corners, (11, 11), (-1, -1), criteria)
                image_points.append(corners2)
                object_points.append(objp)

                if not silent:
                    plt.imshow(img)
                    plt.show()

    '''
        根据检测到的所有对象点坐标和相应像素点坐标执行校正
        mtx: 相机内参，即教学中的K矩阵
        dist: 畸变系数，即D矩阵
        rvecs: 每个棋盘图模型的外参数矩阵R的列表
        tvecs: 每个棋盘图模型的转移矩阵T的列表
    '''
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, img_gray.shape[::-1], None, None)
    img_size = img.shape

    # 压缩保存摄像头参数
    calib_data = {'cam_matrix':mtx, 'dist_coeffs':dist, 'img_size':img_size}
    print(calib_data)
    with open(filename, 'wb') as f:
        pickle.dump(calib_data, f)

    if not silent:
        for image_file in os.listdir(images_path):
            if image_file.endswith("jpg"):
                # 显示校正后图像
                img = cv2.imread(os.path.join(images_path, image_file))
                plt.imshow(cv2.undistort(img, mtx, dist))
                plt.show()

    return mtx, dist


if __name__ == '__main__':
    calibrate(settings.CALIB_FILE_NAME, True)








