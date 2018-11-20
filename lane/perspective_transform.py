import sys
sys.path.append("..")
from lane.params_reader import *
from lane import settings
import numpy as np
import cv2
import pickle


def get_roi():
    """
    获取关注范围矩形的顶点像素坐标
    """
    roi_points = np.array([[0, settings.ORIGINAL_SIZE[1] - 50],
                           [settings.ORIGINAL_SIZE[0], settings.ORIGINAL_SIZE[1] - 50],
                           [settings.ORIGINAL_SIZE[0] // 2, settings.ORIGINAL_SIZE[1] // 2 + 50]], dtype=np.int32)
    roi = np.zeros((settings.ORIGINAL_SIZE[1], settings.ORIGINAL_SIZE[0]), dtype=np.uint8)
    cv2.fillPoly(roi, [roi_points], 1)
    return roi


def get_vanishing_point(img, cam_matrix, dist_coeffs, roi):
    """
    获取消失点(摄像头图像中车道线延长线的交点)
    """
    Lhs = np.zeros((2, 2), dtype=np.float32)
    Rhs = np.zeros((2, 1), dtype=np.float32)

    img = cv2.undistort(img, cam_matrix, dist_coeffs)
    img_hsl = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    edges = cv2.Canny(img_hsl[:, :, 1], 200, 100)
    lines = cv2.HoughLinesP(edges * roi, 0.5, np.pi / 180, 20, None, 180, 120)
    for line in lines:
        for x1, y1, x2, y2 in line:
            normal = np.array([[-(y2 - y1)], [x2 - x1]], dtype=np.float32)
            normal /= np.linalg.norm(normal)
            point = np.array([[x1], [y1]], dtype=np.float32)
            outer = np.matmul(normal, normal.T)
            Lhs += outer
            Rhs += np.matmul(outer, point)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), thickness=2)

    # 计算消失点坐标(vanishing point)
    vanishing_point = np.matmul(np.linalg.inv(Lhs), Rhs)
    return vanishing_point


def get_perspective_transform_points(vanishing_point):
    """
    :param vanishing_point: 消失点
    :return:
    """
    print(vanishing_point)
    # 选择图像上消失点偏下一点作为上部两个点的高度位置
    top = vanishing_point[1] + 60
    # 选择靠近图片底部的位置为下部两个点的高度位置
    bottom = settings.ORIGINAL_SIZE[1] - 35#- 35
    # 定义上部两个点在水平方向上的像素差
    width = settings.ORIGINAL_SIZE[0]//3

    def on_line(p1, p2, ycoord):
        return [p1[0] + (p2[0] - p1[0]) / float(p2[1] - p1[1]) * (ycoord - p1[1]), ycoord]

    # 定义透视变换的四个源点的像素坐标和目标点像素坐标
    p1 = [vanishing_point[0] - width / 2, top]
    p2 = [vanishing_point[0] + width / 2, top]
    p3 = on_line(p2, vanishing_point, bottom)
    p4 = on_line(p1, vanishing_point, bottom)
    src_points = np.array([p1, p2, p3, p4], dtype=np.float32)

    dst_points = np.array(
        [[0, 0], [settings.UNWARPED_SIZE[0], 0], [settings.UNWARPED_SIZE[0], settings.UNWARPED_SIZE[1]],
         [0, settings.UNWARPED_SIZE[1]]], dtype=np.float32)

    return src_points, dst_points


def get_pixel_per_meter_resolution(img, cam_matrix, dist_coeffs, M):
    """
    根据变换矩阵和摄像头内参，获取摄像头图像的像素/米分辨率
    :param M: 透视变换矩阵
    :return: x轴方向上像素/米分辨率，y轴方向上像素/米分辨率
    """
    min_wid = sys.maxsize

    img = cv2.undistort(img, cam_matrix, dist_coeffs)
    img = cv2.warpPerspective(img, M, settings.UNWARPED_SIZE)
    img_hsl = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    mask = img_hsl[:, :, 1] > 128
    mask[:, :50] = 0
    mask[:, -50:] = 0

    # 计算左边车道线像素的质心，取x坐标
    mom = cv2.moments(mask[:, :settings.UNWARPED_SIZE[0]//2].astype(np.uint8))
    x1 = mom["m10"] / mom["m00"]
    # 计算右边车道线像素的质心，取x坐标
    mom = cv2.moments(mask[:, settings.UNWARPED_SIZE[0]//2:].astype(np.uint8))
    x2 = settings.UNWARPED_SIZE[0] // 2 + mom["m10"] / mom["m00"]
    cv2.line(img, (int(x1), 0), (int(x1), settings.UNWARPED_SIZE[1]), (255, 0, 0), 3)
    cv2.line(img, (int(x2), 0), (int(x2), settings.UNWARPED_SIZE[1]), (0, 0, 255), 3)

    # 以质心的x坐标差作为车道线宽度的估计
    if (x2 - x1 < min_wid):
        min_wid = x2 - x1

    pix_per_meter_x = min_wid / (settings.LANE_WIDTH)   # 这里用车道大致宽度来对分辨率做预估
    Lh = np.linalg.inv(np.matmul(M, cam_matrix))
    pix_per_meter_y = pix_per_meter_x * np.linalg.norm(Lh[:, 0]) / np.linalg.norm(Lh[:, 1])
    print(pix_per_meter_x, pix_per_meter_y)

    # plt.imshow(img)
    # plt.show()
    return pix_per_meter_x, pix_per_meter_y


def get_homography_matrix(img):
    '''
    获取用于透视变换的单应性矩阵(homography matrix, 描述了射影几何中平面到平面的映射关系)
    :return:
    '''
    cam_matrix, dist_coeffs, _ = read_camera_params()
    roi = get_roi()
    vanishing_point = get_vanishing_point(img, cam_matrix, dist_coeffs, roi)
    src_points, dst_points = get_perspective_transform_points(vanishing_point)

    # 画出梯形
    cv2.polylines(img, [src_points.astype(np.int32)], True, (0, 0, 255), thickness=5)

    # 获得透视变化所需变换矩阵
    M = cv2.getPerspectiveTransform(src_points, dst_points)

    # 估计像素/距离分辨率
    pix_per_meter_x, pix_per_meter_y = get_pixel_per_meter_resolution(img, cam_matrix, dist_coeffs, M)

    # 保存数据
    perspective_data = {'perspective_transform': M,
                        'pixels_per_meter': (pix_per_meter_x, pix_per_meter_y),
                        'orig_points': src_points}
    with open(settings.PERSPECTIVE_FILE_NAME, 'wb') as f:
        pickle.dump(perspective_data, f)

    print(M)
    return M


if __name__=="__main__":
    straight_images = ["test_images/straight_lines1.jpg"]
    for img_path in straight_images:
        img = cv2.imread(img_path)
        get_homography_matrix(img)