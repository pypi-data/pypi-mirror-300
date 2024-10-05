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
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l11l111l_opy_ as bstack11l11111ll_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack11ll1ll1l_opy_
from bstack_utils.helper import bstack1lll11l1_opy_, bstack11llll1l_opy_, bstack1lllll1l1l_opy_, bstack11l111l1l1_opy_, bstack11l1111111_opy_, bstack11ll111ll_opy_, get_host_info, bstack111llll1ll_opy_, bstack1ll1lll1l1_opy_, bstack11lll11l_opy_
from browserstack_sdk._version import __version__
logger = logging.getLogger(__name__)
@bstack11lll11l_opy_(class_method=False)
def _11l1111l1l_opy_(driver, bstack111lll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11ll1l_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪཋ"): caps.get(bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩཌ"), None),
        bstack11ll1l_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨཌྷ"): bstack111lll11_opy_.get(bstack11ll1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨཎ"), None),
        bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬཏ"): caps.get(bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬཐ"), None),
        bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪད"): caps.get(bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪདྷ"), None)
    }
  except Exception as error:
    logger.debug(bstack11ll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧན") + str(error))
  return response
def on():
    if os.environ.get(bstack11ll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩཔ"), None) is None or os.environ[bstack11ll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪཕ")] == bstack11ll1l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦབ"):
        return False
    return True
def bstack11l111l11l_opy_(config):
  return config.get(bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧབྷ"), False) or any([p.get(bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨམ"), False) == True for p in config.get(bstack11ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬཙ"), [])])
def bstack1lll1lllll_opy_(config, bstack111llll1l_opy_):
  try:
    if not bstack1lllll1l1l_opy_(config):
      return False
    bstack11l11l11l1_opy_ = config.get(bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪཚ"), False)
    if int(bstack111llll1l_opy_) < len(config.get(bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧཛ"), [])) and config[bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨཛྷ")][bstack111llll1l_opy_]:
      bstack11l1111l11_opy_ = config[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩཝ")][bstack111llll1l_opy_].get(bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧཞ"), None)
    else:
      bstack11l1111l11_opy_ = config.get(bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨཟ"), None)
    if bstack11l1111l11_opy_ != None:
      bstack11l11l11l1_opy_ = bstack11l1111l11_opy_
    bstack111lll1lll_opy_ = os.getenv(bstack11ll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧའ")) is not None and len(os.getenv(bstack11ll1l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨཡ"))) > 0 and os.getenv(bstack11ll1l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩར")) != bstack11ll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪལ")
    return bstack11l11l11l1_opy_ and bstack111lll1lll_opy_
  except Exception as error:
    logger.debug(bstack11ll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ཤ") + str(error))
  return False
def bstack1ll1l1l1l_opy_(test_tags):
  bstack11l111111l_opy_ = os.getenv(bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨཥ"))
  if bstack11l111111l_opy_ is None:
    return True
  bstack11l111111l_opy_ = json.loads(bstack11l111111l_opy_)
  try:
    include_tags = bstack11l111111l_opy_[bstack11ll1l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ས")] if bstack11ll1l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧཧ") in bstack11l111111l_opy_ and isinstance(bstack11l111111l_opy_[bstack11ll1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨཨ")], list) else []
    exclude_tags = bstack11l111111l_opy_[bstack11ll1l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩཀྵ")] if bstack11ll1l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪཪ") in bstack11l111111l_opy_ and isinstance(bstack11l111111l_opy_[bstack11ll1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫཫ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11ll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢཬ") + str(error))
  return False
def bstack11l111l1ll_opy_(config, bstack11l11111l1_opy_, bstack111llll11l_opy_, bstack111llll111_opy_):
  bstack11l111llll_opy_ = bstack11l111l1l1_opy_(config)
  bstack111lll1l1l_opy_ = bstack11l1111111_opy_(config)
  if bstack11l111llll_opy_ is None or bstack111lll1l1l_opy_ is None:
    logger.error(bstack11ll1l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ཭"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ཮"), bstack11ll1l_opy_ (u"ࠪࡿࢂ࠭཯")))
    data = {
        bstack11ll1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ཰"): config[bstack11ll1l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧཱࠪ")],
        bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦིࠩ"): config.get(bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧཱིࠪ"), os.path.basename(os.getcwd())),
        bstack11ll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨུࠫ"): bstack1lll11l1_opy_(),
        bstack11ll1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴཱུࠧ"): config.get(bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ྲྀ"), bstack11ll1l_opy_ (u"ࠫࠬཷ")),
        bstack11ll1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬླྀ"): {
            bstack11ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ཹ"): bstack11l11111l1_opy_,
            bstack11ll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰེࠪ"): bstack111llll11l_opy_,
            bstack11ll1l_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲཻࠬ"): __version__,
            bstack11ll1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨོࠫ"): bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰཽࠪ"),
            bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫཾ"): bstack11ll1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧཿ"),
            bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳྀ࠭"): bstack111llll111_opy_
        },
        bstack11ll1l_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴཱྀࠩ"): settings,
        bstack11ll1l_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩྂ"): bstack111llll1ll_opy_(),
        bstack11ll1l_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩྃ"): bstack11ll111ll_opy_(),
        bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳ྄ࠬ"): get_host_info(),
        bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭྅"): bstack1lllll1l1l_opy_(config)
    }
    headers = {
        bstack11ll1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ྆"): bstack11ll1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ྇"),
    }
    config = {
        bstack11ll1l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬྈ"): (bstack11l111llll_opy_, bstack111lll1l1l_opy_),
        bstack11ll1l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩྉ"): headers
    }
    response = bstack1ll1lll1l1_opy_(bstack11ll1l_opy_ (u"ࠩࡓࡓࡘ࡚ࠧྊ"), bstack11l11111ll_opy_ + bstack11ll1l_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪྋ"), data, config)
    bstack111lllll1l_opy_ = response.json()
    if bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬྌ")]:
      parsed = json.loads(os.getenv(bstack11ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ྍ"), bstack11ll1l_opy_ (u"࠭ࡻࡾࠩྎ")))
      parsed[bstack11ll1l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨྏ")] = bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ྐ")][bstack11ll1l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪྑ")]
      os.environ[bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫྒ")] = json.dumps(parsed)
      bstack11ll1ll1l_opy_.bstack111lllll11_opy_(bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩྒྷ")][bstack11ll1l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ྔ")])
      bstack11ll1ll1l_opy_.bstack11l11l1111_opy_(bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"࠭ࡤࡢࡶࡤࠫྕ")][bstack11ll1l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩྖ")])
      bstack11ll1ll1l_opy_.store()
      return bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ྗ")][bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ྘")], bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨྙ")][bstack11ll1l_opy_ (u"ࠫ࡮ࡪࠧྚ")]
    else:
      logger.error(bstack11ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭ྛ") + bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧྜ")])
      if bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྜྷ")] == bstack11ll1l_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪྞ"):
        for bstack111lllllll_opy_ in bstack111lllll1l_opy_[bstack11ll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩྟ")]:
          logger.error(bstack111lllllll_opy_[bstack11ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫྠ")])
      return None, None
  except Exception as error:
    logger.error(bstack11ll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧྡ") +  str(error))
    return None, None
def bstack111llllll1_opy_():
  if os.getenv(bstack11ll1l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪྡྷ")) is None:
    return {
        bstack11ll1l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ྣ"): bstack11ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ྤ"),
        bstack11ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩྥ"): bstack11ll1l_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨྦ")
    }
  data = {bstack11ll1l_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫྦྷ"): bstack1lll11l1_opy_()}
  headers = {
      bstack11ll1l_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫྨ"): bstack11ll1l_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ྩ") + os.getenv(bstack11ll1l_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦྪ")),
      bstack11ll1l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ྫ"): bstack11ll1l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫྫྷ")
  }
  response = bstack1ll1lll1l1_opy_(bstack11ll1l_opy_ (u"ࠩࡓ࡙࡙࠭ྭ"), bstack11l11111ll_opy_ + bstack11ll1l_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬྮ"), data, { bstack11ll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬྯ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11ll1l_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨྰ") + bstack11llll1l_opy_().isoformat() + bstack11ll1l_opy_ (u"࡚࠭ࠨྱ"))
      return {bstack11ll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧྲ"): bstack11ll1l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩླ"), bstack11ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪྴ"): bstack11ll1l_opy_ (u"ࠪࠫྵ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11ll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢྶ") + str(error))
    return {
        bstack11ll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬྷ"): bstack11ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬྸ"),
        bstack11ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨྐྵ"): str(error)
    }
def bstack1l11ll11l_opy_(caps, options, desired_capabilities={}):
  try:
    bstack111lll11ll_opy_ = caps.get(bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩྺ"), {}).get(bstack11ll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ྻ"), caps.get(bstack11ll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪྼ"), bstack11ll1l_opy_ (u"ࠫࠬ྽")))
    if bstack111lll11ll_opy_:
      logger.warn(bstack11ll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ྾"))
      return False
    if options:
      bstack111lll1ll1_opy_ = options.to_capabilities()
    elif desired_capabilities:
      bstack111lll1ll1_opy_ = desired_capabilities
    else:
      bstack111lll1ll1_opy_ = {}
    browser = caps.get(bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ྿"), bstack11ll1l_opy_ (u"ࠧࠨ࿀")).lower() or bstack111lll1ll1_opy_.get(bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭࿁"), bstack11ll1l_opy_ (u"ࠩࠪ࿂")).lower()
    if browser != bstack11ll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ࿃"):
      logger.warn(bstack11ll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ࿄"))
      return False
    browser_version = caps.get(bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿅")) or caps.get(bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ࿆")) or bstack111lll1ll1_opy_.get(bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࿇")) or bstack111lll1ll1_opy_.get(bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ࿈"), {}).get(bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ࿉")) or bstack111lll1ll1_opy_.get(bstack11ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ࿊"), {}).get(bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭࿋"))
    if browser_version and browser_version != bstack11ll1l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬ࿌") and int(browser_version.split(bstack11ll1l_opy_ (u"࠭࠮ࠨ࿍"))[0]) <= 98:
      logger.warn(bstack11ll1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡ࠻࠻࠲ࠧ࿎"))
      return False
    if not options:
      bstack11l1111lll_opy_ = caps.get(bstack11ll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭࿏")) or bstack111lll1ll1_opy_.get(bstack11ll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ࿐"), {})
      if bstack11ll1l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ࿑") in bstack11l1111lll_opy_.get(bstack11ll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩ࿒"), []):
        logger.warn(bstack11ll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢ࿓"))
        return False
    return True
  except Exception as error:
    logger.debug(bstack11ll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣ࿔") + str(error))
    return False
def set_capabilities(caps, config):
  try:
    bstack11l111ll11_opy_ = config.get(bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ࿕"), {})
    bstack11l111ll11_opy_[bstack11ll1l_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ࿖")] = os.getenv(bstack11ll1l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ࿗"))
    bstack11l111l111_opy_ = json.loads(os.getenv(bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ࿘"), bstack11ll1l_opy_ (u"ࠫࢀࢃࠧ࿙"))).get(bstack11ll1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿚"))
    caps[bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭࿛")] = True
    if bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ࿜") in caps:
      caps[bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ࿝")][bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ࿞")] = bstack11l111ll11_opy_
      caps[bstack11ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ࿟")][bstack11ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ࿠")][bstack11ll1l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭࿡")] = bstack11l111l111_opy_
    else:
      caps[bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ࿢")] = bstack11l111ll11_opy_
      caps[bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭࿣")][bstack11ll1l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ࿤")] = bstack11l111l111_opy_
  except Exception as error:
    logger.debug(bstack11ll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥ࿥") +  str(error))
def bstack1l11111lll_opy_(driver, bstack11l111ll1l_opy_):
  try:
    setattr(driver, bstack11ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ࿦"), True)
    session = driver.session_id
    if session:
      bstack11l111lll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l111lll1_opy_ = False
      bstack11l111lll1_opy_ = url.scheme in [bstack11ll1l_opy_ (u"ࠦ࡭ࡺࡴࡱࠤ࿧"), bstack11ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ࿨")]
      if bstack11l111lll1_opy_:
        if bstack11l111ll1l_opy_:
          logger.info(bstack11ll1l_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨ࿩"))
      return bstack11l111ll1l_opy_
  except Exception as e:
    logger.error(bstack11ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥ࿪") + str(e))
    return False
def bstack11l11ll1_opy_(driver, name, path):
  try:
    bstack111llll1l1_opy_ = {
        bstack11ll1l_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨ࿫"): threading.current_thread().current_test_uuid,
        bstack11ll1l_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ࿬"): os.environ.get(bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ࿭"), bstack11ll1l_opy_ (u"ࠫࠬ࿮")),
        bstack11ll1l_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩ࿯"): os.environ.get(bstack11ll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ࿰"), bstack11ll1l_opy_ (u"ࠧࠨ࿱"))
    }
    logger.debug(bstack11ll1l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ࿲"))
    logger.debug(driver.execute_async_script(bstack11ll1ll1l_opy_.perform_scan, {bstack11ll1l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤ࿳"): name}))
    logger.debug(driver.execute_async_script(bstack11ll1ll1l_opy_.bstack11l1111ll1_opy_, bstack111llll1l1_opy_))
    logger.info(bstack11ll1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨ࿴"))
  except Exception as bstack111lll1l11_opy_:
    logger.error(bstack11ll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨ࿵") + str(path) + bstack11ll1l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢ࿶") + str(bstack111lll1l11_opy_))