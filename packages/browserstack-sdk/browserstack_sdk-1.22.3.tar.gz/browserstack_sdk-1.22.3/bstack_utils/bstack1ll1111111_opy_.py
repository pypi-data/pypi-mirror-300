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
import re
from bstack_utils.bstack1l1111lll1_opy_ import bstack1lll11l1l1l_opy_
def bstack1lll11l111l_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᖮ")):
        return bstack11ll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᖯ")
    elif fixture_name.startswith(bstack11ll1l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᖰ")):
        return bstack11ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᖱ")
    elif fixture_name.startswith(bstack11ll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡸࡪࡧࡲࡥࡱࡺࡲࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᖲ")):
        return bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᖳ")
    elif fixture_name.startswith(bstack11ll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖴ")):
        return bstack11ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᖵ")
def bstack1lll111l1ll_opy_(fixture_name):
    return bool(re.match(bstack11ll1l_opy_ (u"ࠧ࡟ࡡࡻࡹࡳ࡯ࡴࡠࠪࡶࡩࡹࡻࡰࡽࡶࡨࡥࡷࡪ࡯ࡸࡰࠬࡣ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࡼ࡮ࡱࡧࡹࡱ࡫ࠩࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᖶ"), fixture_name))
def bstack1lll111ll1l_opy_(fixture_name):
    return bool(re.match(bstack11ll1l_opy_ (u"ࠨࡠࡢࡼࡺࡴࡩࡵࡡࠫࡷࡪࡺࡵࡱࡾࡷࡩࡦࡸࡤࡰࡹࡱ࠭ࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᖷ"), fixture_name))
def bstack1lll111llll_opy_(fixture_name):
    return bool(re.match(bstack11ll1l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࡣ࡭ࡣࡶࡷࡤ࡬ࡩࡹࡶࡸࡶࡪࡥ࠮ࠫࠩᖸ"), fixture_name))
def bstack1lll11l11l1_opy_(fixture_name):
    if fixture_name.startswith(bstack11ll1l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖹ")):
        return bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᖺ"), bstack11ll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᖻ")
    elif fixture_name.startswith(bstack11ll1l_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᖼ")):
        return bstack11ll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳࡭ࡰࡦࡸࡰࡪ࠭ᖽ"), bstack11ll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᖾ")
    elif fixture_name.startswith(bstack11ll1l_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖿ")):
        return bstack11ll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᗀ"), bstack11ll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᗁ")
    elif fixture_name.startswith(bstack11ll1l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᗂ")):
        return bstack11ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮࡯ࡲࡨࡺࡲࡥࠨᗃ"), bstack11ll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᗄ")
    return None, None
def bstack1lll111lll1_opy_(hook_name):
    if hook_name in [bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᗅ"), bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᗆ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll111ll11_opy_(hook_name):
    if hook_name in [bstack11ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᗇ"), bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡱࡪࡺࡨࡰࡦࠪᗈ")]:
        return bstack11ll1l_opy_ (u"ࠬࡈࡅࡇࡑࡕࡉࡤࡋࡁࡄࡊࠪᗉ")
    elif hook_name in [bstack11ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᗊ"), bstack11ll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥࡣ࡭ࡣࡶࡷࠬᗋ")]:
        return bstack11ll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬᗌ")
    elif hook_name in [bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᗍ"), bstack11ll1l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᗎ")]:
        return bstack11ll1l_opy_ (u"ࠫࡆࡌࡔࡆࡔࡢࡉࡆࡉࡈࠨᗏ")
    elif hook_name in [bstack11ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡱࡧࡹࡱ࡫ࠧᗐ"), bstack11ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡥ࡯ࡥࡸࡹࠧᗑ")]:
        return bstack11ll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡁࡍࡎࠪᗒ")
    return hook_name
def bstack1lll111l1l1_opy_(node, scenario):
    if hasattr(node, bstack11ll1l_opy_ (u"ࠨࡥࡤࡰࡱࡹࡰࡦࡥࠪᗓ")):
        parts = node.nodeid.rsplit(bstack11ll1l_opy_ (u"ࠤ࡞ࠦᗔ"))
        params = parts[-1]
        return bstack11ll1l_opy_ (u"ࠥࡿࢂ࡛ࠦࡼࡿࠥᗕ").format(scenario.name, params)
    return scenario.name
def bstack1lll11l1lll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11ll1l_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᗖ")):
            examples = list(node.callspec.params[bstack11ll1l_opy_ (u"ࠬࡥࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡩࡽࡧ࡭ࡱ࡮ࡨࠫᗗ")].values())
        return examples
    except:
        return []
def bstack1lll11l1ll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11l11ll_opy_(report):
    try:
        status = bstack11ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᗘ")
        if report.passed or (report.failed and hasattr(report, bstack11ll1l_opy_ (u"ࠢࡸࡣࡶࡼ࡫ࡧࡩ࡭ࠤᗙ"))):
            status = bstack11ll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᗚ")
        elif report.skipped:
            status = bstack11ll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᗛ")
        bstack1lll11l1l1l_opy_(status)
    except:
        pass
def bstack1lll1ll1l1_opy_(status):
    try:
        bstack1lll11l1111_opy_ = bstack11ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᗜ")
        if status == bstack11ll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᗝ"):
            bstack1lll11l1111_opy_ = bstack11ll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᗞ")
        elif status == bstack11ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᗟ"):
            bstack1lll11l1111_opy_ = bstack11ll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨᗠ")
        bstack1lll11l1l1l_opy_(bstack1lll11l1111_opy_)
    except:
        pass
def bstack1lll11l1l11_opy_(item=None, report=None, summary=None, extra=None):
    return