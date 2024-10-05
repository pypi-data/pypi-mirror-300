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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11l1llll_opy_, bstack111l11ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1llll_opy_ = bstack11l1llll_opy_
        self.bstack111l11ll_opy_ = bstack111l11ll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11ll1ll1_opy_(bstack1111l1ll_opy_):
        bstack1111ll11_opy_ = []
        if bstack1111l1ll_opy_:
            tokens = str(os.path.basename(bstack1111l1ll_opy_)).split(bstack11ll1l_opy_ (u"ࠣࡡࠥॢ"))
            camelcase_name = bstack11ll1l_opy_ (u"ࠤࠣࠦॣ").join(t.title() for t in tokens)
            suite_name, bstack1111ll1l_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll11_opy_.append(suite_name)
        return bstack1111ll11_opy_
    @staticmethod
    def bstack1111lll1_opy_(typename):
        if bstack11ll1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ।") in typename:
            return bstack11ll1l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ॥")
        return bstack11ll1l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ०")