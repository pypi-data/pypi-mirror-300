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
import logging
import os
import threading
from bstack_utils.helper import bstack1l11lll111_opy_
from bstack_utils.constants import bstack111l1lll11_opy_
logger = logging.getLogger(__name__)
class bstack1lll11ll_opy_:
    bstack1ll1llllll1_opy_ = None
    @classmethod
    def bstack1ll11l11l_opy_(cls):
        if cls.on():
            logger.info(
                bstack11ll1l_opy_ (u"࡙ࠩ࡭ࡸ࡯ࡴࠡࡪࡷࡸࡵࡹ࠺࠰࠱ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡴࡴࡸࡴ࠭ࠢ࡬ࡲࡸ࡯ࡧࡩࡶࡶ࠰ࠥࡧ࡮ࡥࠢࡰࡥࡳࡿࠠ࡮ࡱࡵࡩࠥࡪࡥࡣࡷࡪ࡫࡮ࡴࡧࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡡ࡭࡮ࠣࡥࡹࠦ࡯࡯ࡧࠣࡴࡱࡧࡣࡦࠣ࡟ࡲࠬ᝸").format(os.environ[bstack11ll1l_opy_ (u"ࠥࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠤ᝹")]))
    @classmethod
    def on(cls):
        if os.environ.get(bstack11ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬ᝺"), None) is None or os.environ[bstack11ll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡍ࡛࡙࠭᝻")] == bstack11ll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ᝼"):
            return False
        return True
    @classmethod
    def bstack1ll1l111111_opy_(cls, bs_config, framework=bstack11ll1l_opy_ (u"ࠢࠣ᝽")):
        if framework == bstack11ll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ᝾"):
            return bstack1l11lll111_opy_(bs_config.get(bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭᝿")))
        bstack1ll11ll11ll_opy_ = framework in bstack111l1lll11_opy_
        return bstack1l11lll111_opy_(bs_config.get(bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧក"), bstack1ll11ll11ll_opy_))
    @classmethod
    def bstack1ll11ll1lll_opy_(cls, framework):
        return framework in bstack111l1lll11_opy_
    @classmethod
    def bstack1ll1l1l11ll_opy_(cls, bs_config, framework):
        return cls.bstack1ll1l111111_opy_(bs_config, framework) is True and cls.bstack1ll11ll1lll_opy_(framework)
    @staticmethod
    def current_hook_uuid():
        return getattr(threading.current_thread(), bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨខ"), None)
    @staticmethod
    def bstack1ll111l1_opy_():
        if getattr(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩគ"), None):
            return {
                bstack11ll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫឃ"): bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬង"),
                bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨច"): getattr(threading.current_thread(), bstack11ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ឆ"), None)
            }
        if getattr(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧជ"), None):
            return {
                bstack11ll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩឈ"): bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪញ"),
                bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ដ"): getattr(threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫឋ"), None)
            }
        return None
    @staticmethod
    def bstack1ll11ll1l11_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1lll11ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def bstack11ll1ll1_opy_(test, hook_name=None):
        bstack1ll11lll111_opy_ = test.parent
        if hook_name in [bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭ឌ"), bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪឍ"), bstack11ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࠩណ"), bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡰࡦࡸࡰࡪ࠭ត")]:
            bstack1ll11lll111_opy_ = test
        scope = []
        while bstack1ll11lll111_opy_ is not None:
            scope.append(bstack1ll11lll111_opy_.name)
            bstack1ll11lll111_opy_ = bstack1ll11lll111_opy_.parent
        scope.reverse()
        return scope[2:]
    @staticmethod
    def bstack1ll11ll1l1l_opy_(hook_type):
        if hook_type == bstack11ll1l_opy_ (u"ࠧࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠥថ"):
            return bstack11ll1l_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡮࡯ࡰ࡭ࠥទ")
        elif hook_type == bstack11ll1l_opy_ (u"ࠢࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠦធ"):
            return bstack11ll1l_opy_ (u"ࠣࡖࡨࡥࡷࡪ࡯ࡸࡰࠣ࡬ࡴࡵ࡫ࠣន")
    @staticmethod
    def bstack1ll11ll1ll1_opy_(bstack111l1lll_opy_):
        try:
            if not bstack1lll11ll_opy_.on():
                return bstack111l1lll_opy_
            if os.environ.get(bstack11ll1l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠢប"), None) == bstack11ll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣផ"):
                tests = os.environ.get(bstack11ll1l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠣព"), None)
                if tests is None or tests == bstack11ll1l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥភ"):
                    return bstack111l1lll_opy_
                bstack111l1lll_opy_ = tests.split(bstack11ll1l_opy_ (u"࠭ࠬࠨម"))
                return bstack111l1lll_opy_
        except Exception as exc:
            print(bstack11ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡲࡦࡴࡸࡲࠥ࡮ࡡ࡯ࡦ࡯ࡩࡷࡀࠠࠣយ"), str(exc))
        return bstack111l1lll_opy_