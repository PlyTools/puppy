from lane import settings
import pickle


def read_camera_params():
    """
    从settings.CALIB_FILE_NAME中读取保存的摄像头内参和畸变系数
    """
    with open(settings.CALIB_FILE_NAME, 'rb') as f:
        calib_data = pickle.load(f)
        cam_matrix = calib_data["cam_matrix"]
        dist_coeffs = calib_data["dist_coeffs"]
        img_size = calib_data["img_size"]
        return cam_matrix, dist_coeffs, img_size


def read_perspective_params():
    """
        从settings.PERSPECTIVE_FILE_NAME中读取透视变换矩阵
    """
    with open(settings.PERSPECTIVE_FILE_NAME, 'rb') as f:
        perspective_data = pickle.load(f)
        perspective_transform = perspective_data["perspective_transform"]
        pixels_per_meter = perspective_data['pixels_per_meter']
        orig_points = perspective_data["orig_points"]
        return perspective_transform, pixels_per_meter, orig_points

