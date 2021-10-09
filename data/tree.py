import warnings
import numpy as np
from PIL import Image
from anytree import NodeMixin, PostOrderIter, PreOrderIter

H_MIN = 0.5
H_MAX = 2.0


class BaseElement(NodeMixin):
    def __init__(self, d):
        self.name = d.name.split('/')[-1]
        self.image = Image.fromarray(d[:])
        self.attrs = dict(d.attrs)
        self.__H, self.__x, self.__y = [None] * 3

    def _normalize(self):
        M = self.root.base_size
        x0, y0, x1, y1 = self.attrs['box']
        x0, x1 = x0 / M, x1 / M
        y0, y1 = y0 / M, y1 / M
        self.attrs['nbox'] = [x0, y0, x1, y1]
        self.attrs['H'], self.attrs['W'] = y1 - y0, x1 - x0
        self.aspect_ratio = (x1 - x0) / (y1 - y0)

    @property
    def H(self):
        if self.__H is None:
            if np.isnan(self.l_H):
                self.__H = self.parent.H
            else:
                H_ub = min(self.parent.H, self.parent.W / self.aspect_ratio,
                           self.attrs['H'] * H_MAX)
                self.__H = self.l_H * (H_ub - self.H_lb) + self.H_lb
        return self.__H

    @property
    def x(self):
        if self.__x is None:
            if np.isnan(self.l_x):
                self.__x = self.parent.x
            else:
                x_ub = self.parent.x + self.parent.W - self.W
                self.__x = self.l_x * (x_ub - self.parent.x) + self.parent.x
        return self.__x

    @property
    def y(self):
        if self.__y is None:
            if np.isnan(self.l_y):
                self.__y = self.parent.y
            else:
                y_ub = self.parent.y + self.parent.H - self.H
                self.__y = self.l_y * (y_ub - self.parent.y) + self.parent.y
        return self.__y

    @property
    def W(self):
        return self.H * self.aspect_ratio


class RootElement(BaseElement):
    def __init__(self, d):
        super().__init__(d)
        x0, y0, x1, y1 = d.attrs['box']
        self.base_size = float(max(y1 - y0, x1 - x0))
        self._normalize()

    @property
    def H(self):
        return self.attrs['H']

    @property
    def x(self):
        return self.attrs['nbox'][0]

    @property
    def y(self):
        return self.attrs['nbox'][1]

    def _pre_attach(self, parent):
        raise RuntimeError('Cannot set parent to RootElement')


class Element(BaseElement):
    def set_H_lb(self):
        _, y0, _, y1 = self.attrs['nbox']
        H_lb = (y1 - y0) * H_MIN
        for d in self.descendants:
            H_lb = max(d.H_lb, d.W_lb / self.aspect_ratio, H_lb)
        self.H_lb = H_lb
        self.W_lb = H_lb * self.aspect_ratio


class WebPageLayout():
    def __init__(self, g):
        self.root = RootElement(g['root'])
        self.elements = [Element(g[str(i)])
                         for i in range(len(g) - 1)]

        # tree construction
        for e in self.elements:
            if e.attrs['parent'] == 'root':
                e.parent = self.root
            else:
                e.parent = self.elements[e.attrs['parent']]

        def not_root(e):
            return not e.is_root

        # set H lower bound
        for e in PostOrderIter(self.root, filter_=not_root):
            e._normalize()
            e.set_H_lb()

        # set parameters
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            for e in PreOrderIter(self.root, filter_=not_root):
                x0, y0, _, y1 = e.attrs['nbox']
                H_ub = min(e.parent.H, e.parent.W / e.aspect_ratio,
                           (y1 - y0) * H_MAX)
                e.l_H = (y1 - y0 - e.H_lb) / (H_ub - e.H_lb)
                e.l_x = (x0 - e.parent.x) / (e.parent.W - e.W)
                e.l_y = (y0 - e.parent.y) / (e.parent.H - e.H)
