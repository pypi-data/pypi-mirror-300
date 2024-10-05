# coding: UTF-8
import sys
bstack1ll111l_opy_ = sys.version_info [0] == 2
bstack11ll1_opy_ = 2048
bstack111l11l_opy_ = 7
def bstack11ll1l_opy_ (bstack11111ll_opy_):
    global bstack111111l_opy_
    bstack1lll_opy_ = ord (bstack11111ll_opy_ [-1])
    bstack1l1l1ll_opy_ = bstack11111ll_opy_ [:-1]
    bstack1l11l1l_opy_ = bstack1lll_opy_ % len (bstack1l1l1ll_opy_)
    bstack1l1ll11_opy_ = bstack1l1l1ll_opy_ [:bstack1l11l1l_opy_] + bstack1l1l1ll_opy_ [bstack1l11l1l_opy_:]
    if bstack1ll111l_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1_opy_ - (bstack111_opy_ + bstack1lll_opy_) % bstack111l11l_opy_) for bstack111_opy_, char in enumerate (bstack1l1ll11_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack11ll1_opy_ - (bstack111_opy_ + bstack1lll_opy_) % bstack111l11l_opy_) for bstack111_opy_, char in enumerate (bstack1l1ll11_opy_)])
    return eval (bstack1llllll_opy_)
from collections import deque
from bstack_utils.constants import *
class bstack1ll1lll1l_opy_:
    def __init__(self):
        self._1lll1l1l111_opy_ = deque()
        self._1lll1l11lll_opy_ = {}
        self._1lll1l1l11l_opy_ = False
    def bstack1lll1l1ll1l_opy_(self, test_name, bstack1lll1l1111l_opy_):
        bstack1lll1l11l1l_opy_ = self._1lll1l11lll_opy_.get(test_name, {})
        return bstack1lll1l11l1l_opy_.get(bstack1lll1l1111l_opy_, 0)
    def bstack1lll1l11l11_opy_(self, test_name, bstack1lll1l1111l_opy_):
        bstack1lll1l1l1l1_opy_ = self.bstack1lll1l1ll1l_opy_(test_name, bstack1lll1l1111l_opy_)
        self.bstack1lll1l111l1_opy_(test_name, bstack1lll1l1111l_opy_)
        return bstack1lll1l1l1l1_opy_
    def bstack1lll1l111l1_opy_(self, test_name, bstack1lll1l1111l_opy_):
        if test_name not in self._1lll1l11lll_opy_:
            self._1lll1l11lll_opy_[test_name] = {}
        bstack1lll1l11l1l_opy_ = self._1lll1l11lll_opy_[test_name]
        bstack1lll1l1l1l1_opy_ = bstack1lll1l11l1l_opy_.get(bstack1lll1l1111l_opy_, 0)
        bstack1lll1l11l1l_opy_[bstack1lll1l1111l_opy_] = bstack1lll1l1l1l1_opy_ + 1
    def bstack1l1l1ll11_opy_(self, bstack1lll1l111ll_opy_, bstack1lll1l1l1ll_opy_):
        bstack1lll1l11ll1_opy_ = self.bstack1lll1l11l11_opy_(bstack1lll1l111ll_opy_, bstack1lll1l1l1ll_opy_)
        bstack1lll1l11111_opy_ = bstack111l1lll1l_opy_[bstack1lll1l1l1ll_opy_]
        bstack1lll1l1ll11_opy_ = bstack11ll1l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽ࠮ࡽࢀࠦᖇ").format(bstack1lll1l111ll_opy_, bstack1lll1l11111_opy_, bstack1lll1l11ll1_opy_)
        self._1lll1l1l111_opy_.append(bstack1lll1l1ll11_opy_)
    def bstack1l11ll1l1_opy_(self):
        return len(self._1lll1l1l111_opy_) == 0
    def bstack1ll1ll111l_opy_(self):
        bstack1lll11lllll_opy_ = self._1lll1l1l111_opy_.popleft()
        return bstack1lll11lllll_opy_
    def capturing(self):
        return self._1lll1l1l11l_opy_
    def bstack11l111l1l_opy_(self):
        self._1lll1l1l11l_opy_ = True
    def bstack1ll1111l11_opy_(self):
        self._1lll1l1l11l_opy_ = False