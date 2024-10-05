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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l111l111_opy_ = {}
        bstack11l1l111ll_opy_ = os.environ.get(bstack11ll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬຐ"), bstack11ll1l_opy_ (u"ࠬ࠭ຑ"))
        if not bstack11l1l111ll_opy_:
            return bstack1l111l111_opy_
        try:
            bstack11l1l111l1_opy_ = json.loads(bstack11l1l111ll_opy_)
            if bstack11ll1l_opy_ (u"ࠨ࡯ࡴࠤຒ") in bstack11l1l111l1_opy_:
                bstack1l111l111_opy_[bstack11ll1l_opy_ (u"ࠢࡰࡵࠥຓ")] = bstack11l1l111l1_opy_[bstack11ll1l_opy_ (u"ࠣࡱࡶࠦດ")]
            if bstack11ll1l_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨຕ") in bstack11l1l111l1_opy_ or bstack11ll1l_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨຖ") in bstack11l1l111l1_opy_:
                bstack1l111l111_opy_[bstack11ll1l_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢທ")] = bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠧࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠤຘ"), bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠨ࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠤນ")))
            if bstack11ll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣບ") in bstack11l1l111l1_opy_ or bstack11ll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨປ") in bstack11l1l111l1_opy_:
                bstack1l111l111_opy_[bstack11ll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢຜ")] = bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࠦຝ"), bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤພ")))
            if bstack11ll1l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢຟ") in bstack11l1l111l1_opy_ or bstack11ll1l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢຠ") in bstack11l1l111l1_opy_:
                bstack1l111l111_opy_[bstack11ll1l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣມ")] = bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠥຢ"), bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠥຣ")))
            if bstack11ll1l_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧࠥ຤") in bstack11l1l111l1_opy_ or bstack11ll1l_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠣລ") in bstack11l1l111l1_opy_:
                bstack1l111l111_opy_[bstack11ll1l_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤ຦")] = bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࠨວ"), bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠦຨ")))
            if bstack11ll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥຩ") in bstack11l1l111l1_opy_ or bstack11ll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣສ") in bstack11l1l111l1_opy_:
                bstack1l111l111_opy_[bstack11ll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤຫ")] = bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࠨຬ"), bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦອ")))
            if bstack11ll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤຮ") in bstack11l1l111l1_opy_ or bstack11ll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤຯ") in bstack11l1l111l1_opy_:
                bstack1l111l111_opy_[bstack11ll1l_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥະ")] = bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧັ"), bstack11l1l111l1_opy_.get(bstack11ll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧາ")))
            if bstack11ll1l_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸࠨຳ") in bstack11l1l111l1_opy_:
                bstack1l111l111_opy_[bstack11ll1l_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢິ")] = bstack11l1l111l1_opy_[bstack11ll1l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣີ")]
        except Exception as error:
            logger.error(bstack11ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡧࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡢࡶࡤ࠾ࠥࠨຶ") +  str(error))
        return bstack1l111l111_opy_