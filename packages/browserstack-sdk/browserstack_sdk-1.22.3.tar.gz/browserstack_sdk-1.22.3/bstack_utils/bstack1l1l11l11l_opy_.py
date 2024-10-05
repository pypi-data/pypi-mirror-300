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
from browserstack_sdk.bstack11l1ll11_opy_ import bstack11l1l111_opy_
from browserstack_sdk.bstack1l11l111_opy_ import RobotHandler
def bstack1l1l11l1l1_opy_(framework):
    if framework.lower() == bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩድ"):
        return bstack11l1l111_opy_.version()
    elif framework.lower() == bstack11ll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩዶ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11ll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫዷ"):
        import behave
        return behave.__version__
    else:
        return bstack11ll1l_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳ࠭ዸ")