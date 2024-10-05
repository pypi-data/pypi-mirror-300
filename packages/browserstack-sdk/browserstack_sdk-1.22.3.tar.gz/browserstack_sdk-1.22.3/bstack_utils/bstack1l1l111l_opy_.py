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
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack11l111l1l1_opy_, bstack11l1111111_opy_, bstack1ll1lll1l1_opy_, bstack11lll11l_opy_, bstack111l111111_opy_, bstack1111ll1lll_opy_, bstack1111l1111l_opy_, bstack1lll11l1_opy_
from bstack_utils.bstack1ll1llllll1_opy_ import bstack1ll1lllllll_opy_
import bstack_utils.bstack1l1l111111_opy_ as bstack1ll11ll1ll_opy_
from bstack_utils.bstack1ll1l1ll_opy_ import bstack1lll11ll_opy_
import bstack_utils.bstack11l11111_opy_ as bstack111lll1l_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack11ll1ll1l_opy_
from bstack_utils.bstack1ll11l1l_opy_ import bstack1l1l1l11_opy_
bstack1ll1ll11111_opy_ = bstack11ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᙖ")
logger = logging.getLogger(__name__)
class bstack1l1llll1_opy_:
    bstack1ll1llllll1_opy_ = None
    bs_config = None
    bstack11ll1l11l1_opy_ = None
    @classmethod
    @bstack11lll11l_opy_(class_method=True)
    def launch(cls, bs_config, bstack11ll1l11l1_opy_):
        cls.bs_config = bs_config
        cls.bstack11ll1l11l1_opy_ = bstack11ll1l11l1_opy_
        try:
            cls.bstack1ll1l1ll1l1_opy_()
            bstack11l111llll_opy_ = bstack11l111l1l1_opy_(bs_config)
            bstack111lll1l1l_opy_ = bstack11l1111111_opy_(bs_config)
            data = bstack1ll11ll1ll_opy_.bstack1ll1l1l11l1_opy_(bs_config, bstack11ll1l11l1_opy_)
            config = {
                bstack11ll1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᙗ"): (bstack11l111llll_opy_, bstack111lll1l1l_opy_),
                bstack11ll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᙘ"): cls.default_headers()
            }
            response = bstack1ll1lll1l1_opy_(bstack11ll1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᙙ"), cls.request_url(bstack11ll1l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪᙚ")), data, config)
            if response.status_code != 200:
                bstack1ll1ll1111l_opy_ = response.json()
                if bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᙛ")] == False:
                    cls.bstack1ll1l11l1l1_opy_(bstack1ll1ll1111l_opy_)
                    return
                cls.bstack1ll1l11l1ll_opy_(bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᙜ")])
                cls.bstack1ll1l11lll1_opy_(bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᙝ")])
                return None
            bstack1ll1l1lll1l_opy_ = cls.bstack1ll1l11llll_opy_(response)
            return bstack1ll1l1lll1l_opy_
        except Exception as error:
            logger.error(bstack11ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧᙞ").format(str(error)))
            return None
    @classmethod
    @bstack11lll11l_opy_(class_method=True)
    def stop(cls, bstack1ll1l1llll1_opy_=None):
        if not bstack1lll11ll_opy_.on() and not bstack111lll1l_opy_.on():
            return
        if os.environ.get(bstack11ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᙟ")) == bstack11ll1l_opy_ (u"ࠤࡱࡹࡱࡲࠢᙠ") or os.environ.get(bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᙡ")) == bstack11ll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᙢ"):
            logger.error(bstack11ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᙣ"))
            return {
                bstack11ll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᙤ"): bstack11ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᙥ"),
                bstack11ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᙦ"): bstack11ll1l_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᙧ")
            }
        try:
            cls.bstack1ll1llllll1_opy_.shutdown()
            data = {
                bstack11ll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᙨ"): bstack1lll11l1_opy_()
            }
            if not bstack1ll1l1llll1_opy_ is None:
                data[bstack11ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨᙩ")] = [{
                    bstack11ll1l_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᙪ"): bstack11ll1l_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫᙫ"),
                    bstack11ll1l_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧᙬ"): bstack1ll1l1llll1_opy_
                }]
            config = {
                bstack11ll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ᙭"): cls.default_headers()
            }
            bstack1111l1l111_opy_ = bstack11ll1l_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪ᙮").format(os.environ[bstack11ll1l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣᙯ")])
            bstack1ll1l1lllll_opy_ = cls.request_url(bstack1111l1l111_opy_)
            response = bstack1ll1lll1l1_opy_(bstack11ll1l_opy_ (u"ࠫࡕ࡛ࡔࠨᙰ"), bstack1ll1l1lllll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11ll1l_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦᙱ"))
        except Exception as error:
            logger.error(bstack11ll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥᙲ") + str(error))
            return {
                bstack11ll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᙳ"): bstack11ll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᙴ"),
                bstack11ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙵ"): str(error)
            }
    @classmethod
    @bstack11lll11l_opy_(class_method=True)
    def bstack1ll1l11llll_opy_(cls, response):
        bstack1ll1ll1111l_opy_ = response.json()
        bstack1ll1l1lll1l_opy_ = {}
        if bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠪ࡮ࡼࡺࠧᙶ")) is None:
            os.environ[bstack11ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᙷ")] = bstack11ll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᙸ")
        else:
            os.environ[bstack11ll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᙹ")] = bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠧ࡫ࡹࡷࠫᙺ"), bstack11ll1l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᙻ"))
        os.environ[bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᙼ")] = bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᙽ"), bstack11ll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᙾ"))
        if bstack1lll11ll_opy_.bstack1ll1l1l11ll_opy_(cls.bs_config, cls.bstack11ll1l11l1_opy_.get(bstack11ll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭ᙿ"), bstack11ll1l_opy_ (u"࠭ࠧ "))) is True:
            bstack1ll1l111l1l_opy_, bstack1ll1l1l1111_opy_, bstack1ll1l1l1lll_opy_ = cls.bstack1ll1l111lll_opy_(bstack1ll1ll1111l_opy_)
            if bstack1ll1l111l1l_opy_ != None and bstack1ll1l1l1111_opy_ != None:
                bstack1ll1l1lll1l_opy_[bstack11ll1l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᚁ")] = {
                    bstack11ll1l_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫᚂ"): bstack1ll1l111l1l_opy_,
                    bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚃ"): bstack1ll1l1l1111_opy_,
                    bstack11ll1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧᚄ"): bstack1ll1l1l1lll_opy_
                }
            else:
                bstack1ll1l1lll1l_opy_[bstack11ll1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚅ")] = {}
        else:
            bstack1ll1l1lll1l_opy_[bstack11ll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚆ")] = {}
        if bstack111lll1l_opy_.bstack11l111l11l_opy_(cls.bs_config) is True:
            bstack1ll1l1l1ll1_opy_, bstack1ll1l1l1111_opy_ = cls.bstack1ll1l1ll111_opy_(bstack1ll1ll1111l_opy_)
            if bstack1ll1l1l1ll1_opy_ != None and bstack1ll1l1l1111_opy_ != None:
                bstack1ll1l1lll1l_opy_[bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚇ")] = {
                    bstack11ll1l_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫᚈ"): bstack1ll1l1l1ll1_opy_,
                    bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᚉ"): bstack1ll1l1l1111_opy_,
                }
            else:
                bstack1ll1l1lll1l_opy_[bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚊ")] = {}
        else:
            bstack1ll1l1lll1l_opy_[bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚋ")] = {}
        if bstack1ll1l1lll1l_opy_[bstack11ll1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚌ")].get(bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᚍ")) != None or bstack1ll1l1lll1l_opy_[bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚎ")].get(bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᚏ")) != None:
            cls.bstack1ll1l1l1l11_opy_(bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠨ࡬ࡺࡸࠬᚐ")), bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚑ")))
        return bstack1ll1l1lll1l_opy_
    @classmethod
    def bstack1ll1l111lll_opy_(cls, bstack1ll1ll1111l_opy_):
        if bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᚒ")) == None:
            cls.bstack1ll1l11l1ll_opy_()
            return [None, None, None]
        if bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚓ")][bstack11ll1l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᚔ")] != True:
            cls.bstack1ll1l11l1ll_opy_(bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᚕ")])
            return [None, None, None]
        logger.debug(bstack11ll1l_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᚖ"))
        os.environ[bstack11ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᚗ")] = bstack11ll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᚘ")
        if bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠪ࡮ࡼࡺࠧᚙ")):
            os.environ[bstack11ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡌ࡚ࡘࠬᚚ")] = bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠬࡰࡷࡵࠩ᚛")]
            os.environ[bstack11ll1l_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ᚜")] = json.dumps({
                bstack11ll1l_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ᚝"): bstack11l111l1l1_opy_(cls.bs_config),
                bstack11ll1l_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ᚞"): bstack11l1111111_opy_(cls.bs_config)
            })
        if bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ᚟")):
            os.environ[bstack11ll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᚠ")] = bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᚡ")]
        if bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚢ")].get(bstack11ll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚣ"), {}).get(bstack11ll1l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᚤ")):
            os.environ[bstack11ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩᚥ")] = str(bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᚦ")][bstack11ll1l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᚧ")][bstack11ll1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨᚨ")])
        return [bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠬࡰࡷࡵࠩᚩ")], bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᚪ")], os.environ[bstack11ll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᚫ")]]
    @classmethod
    def bstack1ll1l1ll111_opy_(cls, bstack1ll1ll1111l_opy_):
        if bstack1ll1ll1111l_opy_.get(bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚬ")) == None:
            cls.bstack1ll1l11lll1_opy_()
            return [None, None]
        if bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚭ")][bstack11ll1l_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᚮ")] != True:
            cls.bstack1ll1l11lll1_opy_(bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚯ")])
            return [None, None]
        if bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚰ")].get(bstack11ll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚱ")):
            logger.debug(bstack11ll1l_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᚲ"))
            parsed = json.loads(os.getenv(bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᚳ"), bstack11ll1l_opy_ (u"ࠩࡾࢁࠬᚴ")))
            capabilities = bstack1ll11ll1ll_opy_.bstack1ll1l11ll1l_opy_(bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚵ")][bstack11ll1l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᚶ")][bstack11ll1l_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᚷ")], bstack11ll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᚸ"), bstack11ll1l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᚹ"))
            bstack1ll1l1l1ll1_opy_ = capabilities[bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᚺ")]
            os.environ[bstack11ll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᚻ")] = bstack1ll1l1l1ll1_opy_
            parsed[bstack11ll1l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚼ")] = capabilities[bstack11ll1l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚽ")]
            os.environ[bstack11ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᚾ")] = json.dumps(parsed)
            scripts = bstack1ll11ll1ll_opy_.bstack1ll1l11ll1l_opy_(bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚿ")][bstack11ll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᛀ")][bstack11ll1l_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᛁ")], bstack11ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᛂ"), bstack11ll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫᛃ"))
            bstack11ll1ll1l_opy_.bstack111lllll11_opy_(scripts)
            commands = bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᛄ")][bstack11ll1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛅ")][bstack11ll1l_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧᛆ")].get(bstack11ll1l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᛇ"))
            bstack11ll1ll1l_opy_.bstack11l11l1111_opy_(commands)
            bstack11ll1ll1l_opy_.store()
        return [bstack1ll1l1l1ll1_opy_, bstack1ll1ll1111l_opy_[bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪᛈ")]]
    @classmethod
    def bstack1ll1l11l1ll_opy_(cls, response=None):
        os.environ[bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᛉ")] = bstack11ll1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᛊ")
        os.environ[bstack11ll1l_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪᛋ")] = bstack11ll1l_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᛌ")
        os.environ[bstack11ll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᛍ")] = bstack11ll1l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᛎ")
        os.environ[bstack11ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩᛏ")] = bstack11ll1l_opy_ (u"ࠩࡱࡹࡱࡲࠧᛐ")
        os.environ[bstack11ll1l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩᛑ")] = bstack11ll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᛒ")
        os.environ[bstack11ll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ᛓ")] = bstack11ll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᛔ")
        cls.bstack1ll1l11l1l1_opy_(response, bstack11ll1l_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢᛕ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l11lll1_opy_(cls, response=None):
        os.environ[bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᛖ")] = bstack11ll1l_opy_ (u"ࠩࡱࡹࡱࡲࠧᛗ")
        os.environ[bstack11ll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᛘ")] = bstack11ll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᛙ")
        os.environ[bstack11ll1l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᛚ")] = bstack11ll1l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛛ")
        cls.bstack1ll1l11l1l1_opy_(response, bstack11ll1l_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᛜ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l1l1l11_opy_(cls, bstack1ll1l1l1l1l_opy_, bstack1ll1l1l1111_opy_):
        os.environ[bstack11ll1l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛝ")] = bstack1ll1l1l1l1l_opy_
        os.environ[bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᛞ")] = bstack1ll1l1l1111_opy_
    @classmethod
    def bstack1ll1l11l1l1_opy_(cls, response=None, product=bstack11ll1l_opy_ (u"ࠥࠦᛟ")):
        if response == None:
            logger.error(product + bstack11ll1l_opy_ (u"ࠦࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠨᛠ"))
        for error in response[bstack11ll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬᛡ")]:
            bstack111l1111l1_opy_ = error[bstack11ll1l_opy_ (u"࠭࡫ࡦࡻࠪᛢ")]
            error_message = error[bstack11ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛣ")]
            if error_message:
                if bstack111l1111l1_opy_ == bstack11ll1l_opy_ (u"ࠣࡇࡕࡖࡔࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡅࡇࡑࡍࡊࡊࠢᛤ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11ll1l_opy_ (u"ࠤࡇࡥࡹࡧࠠࡶࡲ࡯ࡳࡦࡪࠠࡵࡱࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࠥᛥ") + product + bstack11ll1l_opy_ (u"ࠥࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡩࡻࡥࠡࡶࡲࠤࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠣᛦ"))
    @classmethod
    def bstack1ll1l1ll1l1_opy_(cls):
        if cls.bstack1ll1llllll1_opy_ is not None:
            return
        cls.bstack1ll1llllll1_opy_ = bstack1ll1lllllll_opy_(cls.bstack1ll1ll111l1_opy_)
        cls.bstack1ll1llllll1_opy_.start()
    @classmethod
    def bstack11lllll1_opy_(cls):
        if cls.bstack1ll1llllll1_opy_ is None:
            return
        cls.bstack1ll1llllll1_opy_.shutdown()
    @classmethod
    @bstack11lll11l_opy_(class_method=True)
    def bstack1ll1ll111l1_opy_(cls, bstack1l1ll111_opy_, bstack1ll1l11l11l_opy_=bstack11ll1l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪᛧ")):
        config = {
            bstack11ll1l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᛨ"): cls.default_headers()
        }
        response = bstack1ll1lll1l1_opy_(bstack11ll1l_opy_ (u"࠭ࡐࡐࡕࡗࠫᛩ"), cls.request_url(bstack1ll1l11l11l_opy_), bstack1l1ll111_opy_, config)
        bstack111lllll1l_opy_ = response.json()
    @classmethod
    def bstack1l1l1lll_opy_(cls, bstack1l1ll111_opy_, bstack1ll1l11l11l_opy_=bstack11ll1l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᛪ")):
        if not bstack1ll11ll1ll_opy_.bstack1ll1l1ll1ll_opy_(bstack1l1ll111_opy_[bstack11ll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ᛫")]):
            return
        bstack1l1l1111ll_opy_ = bstack1ll11ll1ll_opy_.bstack1ll1l111l11_opy_(bstack1l1ll111_opy_[bstack11ll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᛬")], bstack1l1ll111_opy_.get(bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ᛭")))
        if bstack1l1l1111ll_opy_ != None:
            bstack1l1ll111_opy_[bstack11ll1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩᛮ")] = bstack1l1l1111ll_opy_
        if bstack1ll1l11l11l_opy_ == bstack11ll1l_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫᛯ"):
            cls.bstack1ll1l1ll1l1_opy_()
            cls.bstack1ll1llllll1_opy_.add(bstack1l1ll111_opy_)
        elif bstack1ll1l11l11l_opy_ == bstack11ll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᛰ"):
            cls.bstack1ll1ll111l1_opy_([bstack1l1ll111_opy_], bstack1ll1l11l11l_opy_)
    @classmethod
    @bstack11lll11l_opy_(class_method=True)
    def bstack1ll11l11_opy_(cls, bstack1llll11l_opy_):
        bstack1ll1l111ll1_opy_ = []
        for log in bstack1llll11l_opy_:
            bstack1ll1l11ll11_opy_ = {
                bstack11ll1l_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᛱ"): bstack11ll1l_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪᛲ"),
                bstack11ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᛳ"): log[bstack11ll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᛴ")],
                bstack11ll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᛵ"): log[bstack11ll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᛶ")],
                bstack11ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭ᛷ"): {},
                bstack11ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᛸ"): log[bstack11ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᛹")],
            }
            if bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ᛺") in log:
                bstack1ll1l11ll11_opy_[bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ᛻")] = log[bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ᛼")]
            elif bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ᛽") in log:
                bstack1ll1l11ll11_opy_[bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭᛾")] = log[bstack11ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᛿")]
            bstack1ll1l111ll1_opy_.append(bstack1ll1l11ll11_opy_)
        cls.bstack1l1l1lll_opy_({
            bstack11ll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᜀ"): bstack11ll1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᜁ"),
            bstack11ll1l_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᜂ"): bstack1ll1l111ll1_opy_
        })
    @classmethod
    @bstack11lll11l_opy_(class_method=True)
    def bstack1ll1l1ll11l_opy_(cls, steps):
        bstack1ll1l1l111l_opy_ = []
        for step in steps:
            bstack1ll1l1lll11_opy_ = {
                bstack11ll1l_opy_ (u"ࠫࡰ࡯࡮ࡥࠩᜃ"): bstack11ll1l_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨᜄ"),
                bstack11ll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬᜅ"): step[bstack11ll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᜆ")],
                bstack11ll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫᜇ"): step[bstack11ll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᜈ")],
                bstack11ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᜉ"): step[bstack11ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᜊ")],
                bstack11ll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᜋ"): step[bstack11ll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨᜌ")]
            }
            if bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜍ") in step:
                bstack1ll1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᜎ")] = step[bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜏ")]
            elif bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜐ") in step:
                bstack1ll1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᜑ")] = step[bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᜒ")]
            bstack1ll1l1l111l_opy_.append(bstack1ll1l1lll11_opy_)
        cls.bstack1l1l1lll_opy_({
            bstack11ll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᜓ"): bstack11ll1l_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧ᜔ࠫ"),
            bstack11ll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡸ᜕࠭"): bstack1ll1l1l111l_opy_
        })
    @classmethod
    @bstack11lll11l_opy_(class_method=True)
    def bstack1l11ll11ll_opy_(cls, screenshot):
        cls.bstack1l1l1lll_opy_({
            bstack11ll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᜖"): bstack11ll1l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ᜗"),
            bstack11ll1l_opy_ (u"ࠫࡱࡵࡧࡴࠩ᜘"): [{
                bstack11ll1l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ᜙"): bstack11ll1l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨ᜚"),
                bstack11ll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ᜛"): datetime.datetime.utcnow().isoformat() + bstack11ll1l_opy_ (u"ࠨ࡜ࠪ᜜"),
                bstack11ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᜝"): screenshot[bstack11ll1l_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ᜞")],
                bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᜟ"): screenshot[bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᜠ")]
            }]
        }, bstack1ll1l11l11l_opy_=bstack11ll1l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫᜡ"))
    @classmethod
    @bstack11lll11l_opy_(class_method=True)
    def bstack1ll1l1l11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1l1lll_opy_({
            bstack11ll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫᜢ"): bstack11ll1l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬᜣ"),
            bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫᜤ"): {
                bstack11ll1l_opy_ (u"ࠥࡹࡺ࡯ࡤࠣᜥ"): cls.current_test_uuid(),
                bstack11ll1l_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥᜦ"): cls.bstack11llllll_opy_(driver)
            }
        })
    @classmethod
    def bstack1l1111l1_opy_(cls, event: str, bstack1l1ll111_opy_: bstack1l1l1l11_opy_):
        bstack11lll1l1_opy_ = {
            bstack11ll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᜧ"): event,
            bstack1l1ll111_opy_.bstack1ll11ll1_opy_(): bstack1l1ll111_opy_.bstack1lllll11_opy_(event)
        }
        cls.bstack1l1l1lll_opy_(bstack11lll1l1_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11ll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᜨ"), None) is None or os.environ[bstack11ll1l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡏ࡝ࡔࠨᜩ")] == bstack11ll1l_opy_ (u"ࠣࡰࡸࡰࡱࠨᜪ")) and (os.environ.get(bstack11ll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᜫ"), None) is None or os.environ[bstack11ll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᜬ")] == bstack11ll1l_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᜭ")):
            return False
        return True
    @staticmethod
    def bstack1ll1l1111ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1llll1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11ll1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᜮ"): bstack11ll1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᜯ"),
            bstack11ll1l_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪᜰ"): bstack11ll1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᜱ")
        }
        if os.environ.get(bstack11ll1l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᜲ"), None):
            headers[bstack11ll1l_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᜳ")] = bstack11ll1l_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃ᜴ࠧ").format(os.environ[bstack11ll1l_opy_ (u"ࠧࡈࡓࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ࠨ᜵")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11ll1l_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ᜶").format(bstack1ll1ll11111_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ᜷"), None)
    @staticmethod
    def bstack11llllll_opy_(driver):
        return {
            bstack111l111111_opy_(): bstack1111ll1lll_opy_(driver)
        }
    @staticmethod
    def bstack1ll1l11l111_opy_(exception_info, report):
        return [{bstack11ll1l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ᜸"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111lll1_opy_(typename):
        if bstack11ll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ᜹") in typename:
            return bstack11ll1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ᜺")
        return bstack11ll1l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ᜻")