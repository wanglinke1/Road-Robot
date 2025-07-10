"""
提供摄像头初始化、开启与释放的模块

主要功能包括:
- 摄像头资源的调度
"""

import cv2
from Config import my_logger


class Camera:
    """
    用于摄像头初始化与图像识别的类

    这个类提供了初始化及释放摄像头，对各种物体与颜色进行识别的功能

    方法:
        __init__: 进行摄像头初始化
        open: 打开摄像头
        release: 释放摄像头资源
    """

    def __init__(self, device: int = 0) -> None:
        """
        初始化摄像头

        Args:
            device(int): 摄像头序号

        Returns:
            None
        """
        self.center_y = None
        self.center_x = None

        self.location_y = None
        self.location_x = None

        self.frame_height = None
        self.frame_width = None

        my_logger.info(f'开始初始化摄像头')
        self.device_id = device
        self.cap = None
        self._debug = False

        my_logger.info(f'初始化摄像头成功！')

    @property
    def debug(self) -> bool:
        return self._debug

    @debug.setter
    def debug(self, value) -> None:
        if isinstance(value, bool):
            self._debug = value
        else:
            raise TypeError

    def open(self) -> None:
        """
        打开摄像头，类在初始化后不会自动打开摄像头，需要手动调用该方法打开摄像头

        Returns:
            None
        """
        if self.cap is None:
            my_logger.info(f"开启摄像头中......")
            self.cap = cv2.VideoCapture(self.device_id)
            if not self.cap.isOpened():
                raise RuntimeError("摄像头打开失败")
            my_logger.info(f"摄像头成功打开")
        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.center_x = self.frame_width // 2
        self.center_y = self.frame_height // 2

    def release(self) -> None:
        """
        关闭摄像头，在程序结束时需要调用该方法释放摄像头

        Returns:
            None
        """
        my_logger.info(f'正在关闭摄像头')
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            my_logger.info(f'摄像头已关闭')
        else:
            my_logger.warning('摄像头未打开，不需释放')

    def show_frame(self) -> None:
        """
        显示摄像头画面

        Returns:
            None
        """
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("摄像头未打开，无法显示画面")

        my_logger.info("开始显示摄像头画面，按 'q' 键退出")
        while True:
            ret, frame = self.cap.read()
            if not ret:
                my_logger.error("无法读取摄像头画面")
                break

            # 显示画面
            cv2.imshow("Camera Frame", frame)

            # 按 'q' 键退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 关闭窗口
        cv2.destroyAllWindows()

if __name__ == '__main__':
    camera = Camera(device=0)
    camera.debug = True
    camera.open()

    try:
        camera.show_frame()
    finally:
        camera.release()