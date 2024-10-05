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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11111l1ll1_opy_, bstack1l1l11l1ll_opy_, bstack1ll11111_opy_, bstack1l11l111l_opy_, \
    bstack1111ll1ll1_opy_
def bstack1l11l1l11l_opy_(bstack1ll1lll1ll1_opy_):
    for driver in bstack1ll1lll1ll1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1lll111_opy_(driver, status, reason=bstack11ll1l_opy_ (u"ࠪࠫᗣ")):
    bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
    if bstack11l111ll_opy_.bstack111llll1_opy_():
        return
    bstack1ll11l1ll1_opy_ = bstack11l1llll11_opy_(bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗤ"), bstack11ll1l_opy_ (u"ࠬ࠭ᗥ"), status, reason, bstack11ll1l_opy_ (u"࠭ࠧᗦ"), bstack11ll1l_opy_ (u"ࠧࠨᗧ"))
    driver.execute_script(bstack1ll11l1ll1_opy_)
def bstack1llllll11l_opy_(page, status, reason=bstack11ll1l_opy_ (u"ࠨࠩᗨ")):
    try:
        if page is None:
            return
        bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
        if bstack11l111ll_opy_.bstack111llll1_opy_():
            return
        bstack1ll11l1ll1_opy_ = bstack11l1llll11_opy_(bstack11ll1l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᗩ"), bstack11ll1l_opy_ (u"ࠪࠫᗪ"), status, reason, bstack11ll1l_opy_ (u"ࠫࠬᗫ"), bstack11ll1l_opy_ (u"ࠬ࠭ᗬ"))
        page.evaluate(bstack11ll1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢᗭ"), bstack1ll11l1ll1_opy_)
    except Exception as e:
        print(bstack11ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡾࢁࠧᗮ"), e)
def bstack11l1llll11_opy_(type, name, status, reason, bstack1lll11l1l_opy_, bstack11l1ll11l_opy_):
    bstack1lll1111l_opy_ = {
        bstack11ll1l_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨᗯ"): type,
        bstack11ll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗰ"): {}
    }
    if type == bstack11ll1l_opy_ (u"ࠪࡥࡳࡴ࡯ࡵࡣࡷࡩࠬᗱ"):
        bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗲ")][bstack11ll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᗳ")] = bstack1lll11l1l_opy_
        bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᗴ")][bstack11ll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬᗵ")] = json.dumps(str(bstack11l1ll11l_opy_))
    if type == bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᗶ"):
        bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗷ")][bstack11ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᗸ")] = name
    if type == bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗹ"):
        bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᗺ")][bstack11ll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᗻ")] = status
        if status == bstack11ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᗼ") and str(reason) != bstack11ll1l_opy_ (u"ࠣࠤᗽ"):
            bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᗾ")][bstack11ll1l_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᗿ")] = json.dumps(str(reason))
    bstack11l1l11ll1_opy_ = bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩᘀ").format(json.dumps(bstack1lll1111l_opy_))
    return bstack11l1l11ll1_opy_
def bstack1lll1l1l1l_opy_(url, config, logger, bstack111111lll_opy_=False):
    hostname = bstack1l1l11l1ll_opy_(url)
    is_private = bstack1l11l111l_opy_(hostname)
    try:
        if is_private or bstack111111lll_opy_:
            file_path = bstack11111l1ll1_opy_(bstack11ll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᘁ"), bstack11ll1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᘂ"), logger)
            if os.environ.get(bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡔࡏࡕࡡࡖࡉ࡙ࡥࡅࡓࡔࡒࡖࠬᘃ")) and eval(
                    os.environ.get(bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᘄ"))):
                return
            if (bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᘅ") in config and not config[bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᘆ")]):
                os.environ[bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᘇ")] = str(True)
                bstack1ll1llll11l_opy_ = {bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧᘈ"): hostname}
                bstack1111ll1ll1_opy_(bstack11ll1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬᘉ"), bstack11ll1l_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬᘊ"), bstack1ll1llll11l_opy_, logger)
    except Exception as e:
        pass
def bstack1l1lll1l1_opy_(caps, bstack1ll1lll1lll_opy_):
    if bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘋ") in caps:
        caps[bstack11ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᘌ")][bstack11ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࠩᘍ")] = True
        if bstack1ll1lll1lll_opy_:
            caps[bstack11ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘎ")][bstack11ll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᘏ")] = bstack1ll1lll1lll_opy_
    else:
        caps[bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࠫᘐ")] = True
        if bstack1ll1lll1lll_opy_:
            caps[bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᘑ")] = bstack1ll1lll1lll_opy_
def bstack1lll11l1l1l_opy_(bstack1l11l1l1_opy_):
    bstack1ll1llll111_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹ࡙ࡴࡢࡶࡸࡷࠬᘒ"), bstack11ll1l_opy_ (u"ࠩࠪᘓ"))
    if bstack1ll1llll111_opy_ == bstack11ll1l_opy_ (u"ࠪࠫᘔ") or bstack1ll1llll111_opy_ == bstack11ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᘕ"):
        threading.current_thread().testStatus = bstack1l11l1l1_opy_
    else:
        if bstack1l11l1l1_opy_ == bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᘖ"):
            threading.current_thread().testStatus = bstack1l11l1l1_opy_