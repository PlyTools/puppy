import sys
import matplotlib.pyplot as plt
sys.path.append("../")
import os
from lane.perspective_transform import *


# 检测单一车道线
class LaneLine:
    def __init__(self, fit_poly=[0.0, 0.0, 0.0], warped_size=settings.UNWARPED_SIZE):
        # 二次函数的三个系数
        self.fit_poly = fit_poly
        self.warped_size = warped_size
        # 鸟瞰图图片大小
        self.ploty = np.array(self.warped_size[0], dtype=np.uint8)
        self.fitx = np.array(self.warped_size[1], dtype=np.uint8)
        self.line_points = np.ones((self.warped_size[1], self.warped_size[0]), dtype=np.uint8)

    def get_line_points(self, img_t):
        # 为拟合的多项式生成点，用以画图
        self.ploty = np.linspace(0, img_t.shape[0] - 1, img_t.shape[0])
        self.fitx = self.fit_poly[0] * self.ploty ** 2 + self.fit_poly[1] * self.ploty + self.fit_poly[2]
        self.line_points = np.stack((self.fitx, self.ploty), axis=-1)
        return self.line_points

# 车道检测
class LaneDetection:
    def __init__(self, img_size, warped_size, cam_matrix, dist_coeffs, transform_matrix, pixels_per_meter):
        self.found = False
        self.cam_matrix = cam_matrix
        self.dist_coeffs = dist_coeffs
        self.img_size = img_size
        self.warped_size = warped_size
        self.M = transform_matrix
        self.left_line = LaneLine()
        self.right_line = LaneLine()
        self.pixels_per_meter = pixels_per_meter

    def undistort(self, img):
        return cv2.undistort(img, self.cam_matrix, self.dist_coeffs)

    def warp(self, img):
        return cv2.warpPerspective(img, self.M, (self.warped_size[0], self.warped_size[1]))

    def unwarp(self, img):
        print(self.img_size)
        return cv2.warpPerspective(img, self.M, self.img_size, flags=cv2.WARP_FILL_OUTLIERS +
                                                                     cv2.INTER_CUBIC + cv2.WARP_INVERSE_MAP)

    def extract_lanes_pixels(self, binary_warped):
        # 获取二值化图像下半部分的像素直方图
        histogram = np.sum(binary_warped[binary_warped.shape[0]//2:, :], axis=0)
        plt.plot(histogram)
        plt.show()
        # 生成一幅三通道的图片以方便展示
        print(self.pixels_per_meter)
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))
        plt.imshow(out_img)
        plt.show()

        # 找到直方图中左边2/3车道宽度范围内和右边2/3车道宽度范围内各自顶点的x坐标leftx_base, rightx_base，分别作为左右车道线搜索的x起点
        midpoint = histogram.shape[0] // 2
        left_point = int(midpoint-settings.LANE_WIDTH*pixels_per_meter[0]*2//3) if int(midpoint-settings.LANE_WIDTH*pixels_per_meter[0]*2//3) > 0 else 0
        leftx_base = np.argmax(histogram[left_point:midpoint]) + left_point
        right_point = int(midpoint+settings.LANE_WIDTH*pixels_per_meter[0]*2//3) if int(midpoint+settings.LANE_WIDTH*pixels_per_meter[0]*2//3) < histogram.shape[0] else histogram.shape[0]
        rightx_base = np.argmax(histogram[midpoint:right_point]) + midpoint
        print(leftx_base, rightx_base)

        # 选择滑动窗口的数量
        nwindows = 9
        # 设置窗口高度
        window_height = binary_warped.shape[0] // nwindows
        # 识别图中所有非0值像素点的像素坐标x, y
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])
        # 使用上面的搜索起点leftx_base, rightx_base作为窗口的起始x值
        leftx_current = leftx_base
        rightx_current = rightx_base
        # 设置窗口宽度的余量(窗口宽度在+/- margin之间)为
        margin = 100
        # 设置找到重定位窗口的最小像素数
        minpix = 50
        # 创建空列表以接收左右车道像素索引
        left_lane_inds = []
        right_lane_inds = []

        # 一个接一个地穿过窗户
        for window in range(nwindows):
            # 识别x和y中的窗口边界
            win_y_low = binary_warped.shape[0] - (window + 1) * window_height
            win_y_high = binary_warped.shape[0] - window * window_height
            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin
            # 在图片中画出窗口
            cv2.rectangle(out_img, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high), (0, 255, 0), 2)
            cv2.rectangle(out_img, (win_xright_low, win_y_low), (win_xright_high, win_y_high), (0, 255, 0), 2)
            # 识别窗口内部非零像素在坐标数组中的索引
            good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) & (
                    nonzerox < win_xleft_high)).nonzero()[0]
            good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) & (
                    nonzerox < win_xright_high)).nonzero()[0]
            # 将窗口内部的非零像素的索引加入列表中
            left_lane_inds.append(good_left_inds)
            right_lane_inds.append(good_right_inds)
            # 如果发现的内部点数量多于minpix，那么将下一个窗口的位置设置为这些点的中央
            if len(good_left_inds) > minpix:
                leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
            if len(good_right_inds) > minpix:
                rightx_current = np.int(np.mean(nonzerox[good_right_inds]))
        # 拼接非零点的x坐标列表和y坐标列表
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
        # 获取左车道线和右车道线上点的x坐标列表，y坐标列表
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]
        return leftx, lefty, rightx, righty

    def get_center_shift(self):
        return (self.left_line.fitx[0] + self.right_line.fitx[0] - self.img_size[1]) // 2
        # return (left_points[0][0] + right_points[0][0] - self.img_size[1]) // 2 / self.pixels_per_meter
        # return np.polyval(coeffs, img_size[1] / pixels_per_meter[1]) - (img_size[0] // 2) / pixels_per_meter[0]

    def find_lane(self, img):
        # 去畸变
        img = self.undistort(img)

        # 通过透射变化获取鸟瞰图
        img_t = self.warp(img)
        plt.imshow(img_t)
        plt.show()

        # 二值化
        gray = cv2.cvtColor(img_t, cv2.COLOR_BGR2GRAY)
        retval, img_t = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        plt.imshow(img_t)
        plt.show()

        # 获取车道线像素点坐标并拟合
        leftx, lefty, rightx, righty = self.extract_lanes_pixels(img_t)
        self.left_line.fit_poly = np.polyfit(lefty, leftx, 2)
        self.right_line.fit_poly = np.polyfit(righty, rightx, 2)

        self.left_line.get_line_points(img_t)
        self.right_line.get_line_points(img_t)

        plt.imshow(img_t)
        plt.plot(self.left_line.fitx, self.left_line.ploty, color='yellow')
        plt.plot(self.right_line.fitx, self.right_line.ploty, color='yellow')
        plt.show()

    def draw_lane_weighted(self, img, alpha=1, beta=0.4, gamma=0):
        both_lines = np.concatenate((self.left_line.line_points, np.flipud(self.right_line.line_points)), axis=0)
        lanes = np.zeros((self.warped_size[1], self.warped_size[0], 3), dtype=np.uint8)

        cv2.polylines(lanes, [self.left_line.line_points.astype(np.int32)], False, (255, 0, 0), thickness=5)
        cv2.polylines(lanes, [self.right_line.line_points.astype(np.int32)], False, (0, 0, 255), thickness=5)
        cv2.fillPoly(lanes, [both_lines.astype(np.int32)], (0, 255, 0))

        lanes_unwarped = self.unwarp(lanes)
        return cv2.addWeighted(img, alpha, lanes_unwarped, beta, gamma)

    def process_image(self, img):
        self.find_lane(img)
        lane_img = self.draw_lane_weighted(img)
        shift = self.get_center_shift()

        plt.imshow(lane_img)
        plt.show()

        return shift


if __name__ == "__main__":
    cam_matrix, dist_coeffs, img_size = read_camera_params()
    perspective_transform, pixels_per_meter, orig_points = read_perspective_params()

    input_images = "test_images"
    output_images = "output_images"
    for image_file in os.listdir(input_images):
        if image_file.endswith(".jpg"):
            # turn images to grayscale and find chessboard corners
            img = cv2.imread(os.path.join(input_images, image_file))
            ld = LaneDetection(settings.ORIGINAL_SIZE, settings.UNWARPED_SIZE, cam_matrix, dist_coeffs,
                               perspective_transform, pixels_per_meter)
            img = ld.process_image(img)