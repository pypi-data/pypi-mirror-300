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
import datetime
import threading
from bstack_utils.helper import bstack111llll1ll_opy_, bstack11ll111ll_opy_, get_host_info, bstack1111llll11_opy_, \
 bstack1lllll1l1l_opy_, bstack1ll11111_opy_, bstack11lll11l_opy_, bstack1111l1111l_opy_, bstack1lll11l1_opy_
import bstack_utils.bstack11l11111_opy_ as bstack111lll1l_opy_
from bstack_utils.bstack1ll1l1ll_opy_ import bstack1lll11ll_opy_
from bstack_utils.percy import bstack1l1111l11l_opy_
from bstack_utils.config import Config
bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1111l11l_opy_()
@bstack11lll11l_opy_(class_method=False)
def bstack1ll1l1l11l1_opy_(bs_config, bstack11ll1l11l1_opy_):
  try:
    data = {
        bstack11ll1l_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬ᜼"): bstack11ll1l_opy_ (u"࠭ࡪࡴࡱࡱࠫ᜽"),
        bstack11ll1l_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭᜾"): bs_config.get(bstack11ll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᜿"), bstack11ll1l_opy_ (u"ࠩࠪᝀ")),
        bstack11ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨᝁ"): bs_config.get(bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᝂ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᝃ"): bs_config.get(bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨᝄ")),
        bstack11ll1l_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᝅ"): bs_config.get(bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᝆ"), bstack11ll1l_opy_ (u"ࠩࠪᝇ")),
        bstack11ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᝈ"): bstack1lll11l1_opy_(),
        bstack11ll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩᝉ"): bstack1111llll11_opy_(bs_config),
        bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨᝊ"): get_host_info(),
        bstack11ll1l_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧᝋ"): bstack11ll111ll_opy_(),
        bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᝌ"): os.environ.get(bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧᝍ")),
        bstack11ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧᝎ"): os.environ.get(bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨᝏ"), False),
        bstack11ll1l_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭ᝐ"): bstack111llll1ll_opy_(),
        bstack11ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᝑ"): bstack1ll11lll1l1_opy_(),
        bstack11ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪᝒ"): bstack1ll11llll11_opy_(bstack11ll1l11l1_opy_),
        bstack11ll1l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬᝓ"): bstack1lll1ll1l_opy_(bs_config, bstack11ll1l11l1_opy_.get(bstack11ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ᝔"), bstack11ll1l_opy_ (u"ࠩࠪ᝕"))),
        bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᝖"): bstack1lllll1l1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11ll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ᝗").format(str(error)))
    return None
def bstack1ll11llll11_opy_(framework):
  return {
    bstack11ll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ᝘"): framework.get(bstack11ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧ᝙"), bstack11ll1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ᝚")),
    bstack11ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ᝛"): framework.get(bstack11ll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᝜")),
    bstack11ll1l_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᝝"): framework.get(bstack11ll1l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᝞")),
    bstack11ll1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ᝟"): bstack11ll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᝠ"),
    bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᝡ"): framework.get(bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᝢ"))
  }
def bstack1lll1ll1l_opy_(bs_config, framework):
  bstack111l11l1l_opy_ = False
  bstack1l1l1lll11_opy_ = False
  if bstack11ll1l_opy_ (u"ࠩࡤࡴࡵ࠭ᝣ") in bs_config:
    bstack111l11l1l_opy_ = True
  else:
    bstack1l1l1lll11_opy_ = True
  bstack1l1l1111ll_opy_ = {
    bstack11ll1l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᝤ"): bstack1lll11ll_opy_.bstack1ll1l111111_opy_(bs_config, framework),
    bstack11ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᝥ"): bstack111lll1l_opy_.bstack11l111l11l_opy_(bs_config),
    bstack11ll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᝦ"): bs_config.get(bstack11ll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬᝧ"), False),
    bstack11ll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩᝨ"): bstack1l1l1lll11_opy_,
    bstack11ll1l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᝩ"): bstack111l11l1l_opy_
  }
  return bstack1l1l1111ll_opy_
@bstack11lll11l_opy_(class_method=False)
def bstack1ll11lll1l1_opy_():
  try:
    bstack1ll11llll1l_opy_ = json.loads(os.getenv(bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᝪ"), bstack11ll1l_opy_ (u"ࠪࡿࢂ࠭ᝫ")))
    return {
        bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᝬ"): bstack1ll11llll1l_opy_
    }
  except Exception as error:
    logger.error(bstack11ll1l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ᝭").format(str(error)))
    return {}
def bstack1ll1l11ll1l_opy_(array, bstack1ll1l11111l_opy_, bstack1ll1l1111l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l11111l_opy_]
    result[key] = o[bstack1ll1l1111l1_opy_]
  return result
def bstack1ll1l1ll1ll_opy_(bstack1l1ll1lll_opy_=bstack11ll1l_opy_ (u"࠭ࠧᝮ")):
  bstack1ll11lllll1_opy_ = bstack111lll1l_opy_.on()
  bstack1ll11lll1ll_opy_ = bstack1lll11ll_opy_.on()
  bstack1ll11lll11l_opy_ = percy.bstack1l111ll11_opy_()
  if bstack1ll11lll11l_opy_ and not bstack1ll11lll1ll_opy_ and not bstack1ll11lllll1_opy_:
    return bstack1l1ll1lll_opy_ not in [bstack11ll1l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫᝯ"), bstack11ll1l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬᝰ")]
  elif bstack1ll11lllll1_opy_ and not bstack1ll11lll1ll_opy_:
    return bstack1l1ll1lll_opy_ not in [bstack11ll1l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ᝱"), bstack11ll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᝲ"), bstack11ll1l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᝳ")]
  return bstack1ll11lllll1_opy_ or bstack1ll11lll1ll_opy_ or bstack1ll11lll11l_opy_
@bstack11lll11l_opy_(class_method=False)
def bstack1ll1l111l11_opy_(bstack1l1ll1lll_opy_, test=None):
  bstack1ll11llllll_opy_ = bstack111lll1l_opy_.on()
  if not bstack1ll11llllll_opy_ or bstack1l1ll1lll_opy_ not in [bstack11ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ᝴")] or test == None:
    return None
  return {
    bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᝵"): bstack1ll11llllll_opy_ and bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭᝶"), None) == True and bstack111lll1l_opy_.bstack1ll1l1l1l_opy_(test[bstack11ll1l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭᝷")])
  }