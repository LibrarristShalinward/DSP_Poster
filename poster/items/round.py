from abc import ABC, abstractmethod
import numpy as np



class Round(ABC):
    """
    折线段转角平滑抽象类
    """

    def __init__(self, r: float = .1, min_scale = .3, N: int = 11): 
        """
        Initialize the Round object.

        Parameters:
            r (float): Smooth radius.
            min_scale (float): Minimum scale factor for the remaining segment length after rounding.
            N (int): Number of points in the sequence.
        """
        self.r = r  # 平滑半径
        self.min_scale = min_scale  # 产生转角后剩余部分至少占原线段的长度比例
        self.N = N

    @abstractmethod
    def round(self, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
        """
        Abstract method to generate a sequence of points along a smooth curve.

        Parameters:
            a (np.ndarray): Point a, shape (..., 2,).
            b (np.ndarray): Point b, shape (..., 2,).
            c (np.ndarray): Point c, shape (..., 2,).

        Returns:
            np.ndarray: Sequence of points, shape (..., N, 2).
        """
        pass

    def __call__(self, x: np.ndarray) -> np.ndarray: 
        """
        用圆角平滑折线转角

        Args:
            x (np.ndarray): 折线点序列

        Returns:
            np.ndarray: 平滑后结果
        """
        # 确定保留的线段
        frags = np.stack([x[:-1], x[1:]], axis = 1)  # shape (L, 2, 2)
        lengths = np.linalg.norm(frags[:, 1] - frags[:, 0], axis = 1) # 计算每段线段的长度
        scale = (1 - self.r * 2. / lengths).clip(min = self.min_scale) # 计算保留线段的缩放比例
        frag_center = frags.mean(1, keepdims = True) # shape (L, 1, 2)
        leaved_frags = (frags - frag_center) * scale[:, np.newaxis, np.newaxis] + frag_center # shape (L, 2, 2)
        leaved_frags[0, 0], leaved_frags[-1, 1] = frags[0, 0], frags[-1, 1]  # 保留首尾点

        # 计算圆角
        rounds = self.round(leaved_frags[:-1, 1], frags[:-1, 1], leaved_frags[1:, 0]) # shape (L-1, N, 2)

        return np.concatenate([
            frags[0, 0][np.newaxis, :],  # 保留首点
            rounds.reshape(-1, 2),  # 圆角点
            frags[-1, 1][np.newaxis, :],  # 保留尾点
        ], axis = 0) # shape (L-1, N, 2) -> (L-1*N+2, 2)



class EllipseRound(Round):
    """
    Subclass of Round that generates points along an elliptical curve.
    """

    def round(self, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
        """
        Generate a sequence of points along the parametric elliptical curve.

        Parameters:
            a (np.ndarray): Point a, shape (..., 2,).
            b (np.ndarray): Point b, shape (..., 2,).
            c (np.ndarray): Point c, shape (..., 2,).

        Returns:
            np.ndarray: Sequence of points, shape (..., N, 2).
        """
        # Ensure a, b, c have the same shape
        a, b, c = np.broadcast_arrays(a, b, c)

        # Generate N equally spaced t values in [0, pi/2]
        t_values = np.linspace(0, np.pi / 2, self.N).reshape(*(1, ) * (len(a.shape) - 1), -1, 1)

        # Compute the parametric elliptical curve points
        curve_points = (
            (1 - np.sin(t_values)) * (a - b)[..., np.newaxis, :] +
            (1 - np.cos(t_values)) * (c - b)[..., np.newaxis, :] + b[..., np.newaxis, :]
        )
        return curve_points