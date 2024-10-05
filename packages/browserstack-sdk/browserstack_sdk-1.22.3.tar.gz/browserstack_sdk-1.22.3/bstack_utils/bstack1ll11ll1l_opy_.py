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
class bstack1l11l11ll1_opy_:
    def __init__(self, handler):
        self._1ll1llll1ll_opy_ = None
        self.handler = handler
        self._1ll1llll1l1_opy_ = self.bstack1ll1lllll1l_opy_()
        self.patch()
    def patch(self):
        self._1ll1llll1ll_opy_ = self._1ll1llll1l1_opy_.execute
        self._1ll1llll1l1_opy_.execute = self.bstack1ll1lllll11_opy_()
    def bstack1ll1lllll11_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack11ll1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࠣᗡ"), driver_command, None, this, args)
            response = self._1ll1llll1ll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack11ll1l_opy_ (u"ࠤࡤࡪࡹ࡫ࡲࠣᗢ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1llll1l1_opy_.execute = self._1ll1llll1ll_opy_
    @staticmethod
    def bstack1ll1lllll1l_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver