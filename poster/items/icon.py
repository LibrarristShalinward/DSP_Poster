from PIL import Image
from matplotlib.axes import Axes
from numpy.typing import NDArray
from typing import Optional
import colorsys
import matplotlib.pyplot as plt
import numpy as np


# 该类用于处理图标的加载和绘制
class Icon:
    def __init__(self, path: str) -> None:
        """
        初始化Icon类

        参数:
        path (str): 图标的路径
        """
        self.path: str = path
        self.image: Image.Image = Image.open(path).convert("RGBA")
        self._main_color: Optional[NDArray[np.float64]] = None
        self._bg_color: Optional[NDArray[np.float64]] = None

    @property
    def main_color(self) -> NDArray[np.float64]:
        """
        返回以透明度加权的图片RGB颜色均值

        返回:
        NDArray[np.float64]: 以透明度加权的RGB颜色均值
        """
        if self._main_color is None:
            data = np.array(self.image)
            alpha = data[:, :, 3] / 255.0
            rgb = data[:, :, :3]
            weighted_rgb = rgb * alpha[:, :, None]
            total_alpha = np.sum(alpha)
            self._main_color = np.sum(weighted_rgb, axis = (0, 1)) / total_alpha
        return self._main_color

    @property
    def bg_color(self) -> NDArray[np.float64]:
        """
        返回通过HSV映射后的背景颜色

        返回:
        NDArray[np.float64]: 背景颜色的RGB值
        """
        if self._bg_color is None:
            hsv = colorsys.rgb_to_hsv(*(self.main_color / 255.0))
            scaled_s = hsv[1] * .6 + .3  # 缩放饱和度
            scaled_v = hsv[2] * .5 + .5  # 缩放亮度
            new_rgb = colorsys.hsv_to_rgb(hsv[0], scaled_s, scaled_v)
            self._bg_color = np.array(new_rgb) * 255
        return self._bg_color

    def draw(self, x: float, y: float, a: float) -> None:
        """
        使用Matplotlib绘制图标

        参数:
        x (float): 图标中心的x坐标
        y (float): 图标中心的y坐标
        a (float): 图标的边长
        """
        # 绘制背景正方形
        square_x = [x - a / 2, x + a / 2, x + a / 2, x - a / 2]
        square_y = [y - a / 2, y - a / 2, y + a / 2, y + a / 2]
        plt.fill(square_x, square_y, color = self.bg_color / 255.0, linewidth = 0, zorder = -1)
        # 绘制图标
        img_extent = [x - a / 2, x + a / 2, y - a / 2, y + a / 2]
        plt.imshow(self.image, extent = img_extent, zorder = 0)