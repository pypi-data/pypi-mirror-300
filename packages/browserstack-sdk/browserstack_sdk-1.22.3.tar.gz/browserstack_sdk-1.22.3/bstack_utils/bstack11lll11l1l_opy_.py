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
import threading
import logging
import bstack_utils.bstack11l11111_opy_ as bstack111lll1l_opy_
from bstack_utils.helper import bstack1ll11111_opy_
logger = logging.getLogger(__name__)
def bstack111l1ll1l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack11l1111ll_opy_(context, *args):
    tags = getattr(args[0], bstack11ll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫဌ"), [])
    bstack1ll11lllll_opy_ = bstack111lll1l_opy_.bstack1ll1l1l1l_opy_(tags)
    threading.current_thread().isA11yTest = bstack1ll11lllll_opy_
    try:
      bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1ll1l_opy_(bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ဍ")) else context.browser
      if bstack1lll11lll_opy_ and bstack1lll11lll_opy_.session_id and bstack1ll11lllll_opy_ and bstack1ll11111_opy_(
              threading.current_thread(), bstack11ll1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧဎ"), None):
          threading.current_thread().isA11yTest = bstack111lll1l_opy_.bstack1l11111lll_opy_(bstack1lll11lll_opy_, bstack1ll11lllll_opy_)
    except Exception as e:
       logger.debug(bstack11ll1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡴࡢࡴࡷࠤࡦ࠷࠱ࡺࠢ࡬ࡲࠥࡨࡥࡩࡣࡹࡩ࠿ࠦࡻࡾࠩဏ").format(str(e)))
def bstack1l1l11lll1_opy_(bstack1lll11lll_opy_):
    if bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧတ"), None) and bstack1ll11111_opy_(
      threading.current_thread(), bstack11ll1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪထ"), None) and not bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡢࡷࡹࡵࡰࠨဒ"), False):
      threading.current_thread().a11y_stop = True
      bstack111lll1l_opy_.bstack11l11ll1_opy_(bstack1lll11lll_opy_, name=bstack11ll1l_opy_ (u"ࠨࠢဓ"), path=bstack11ll1l_opy_ (u"ࠢࠣန"))