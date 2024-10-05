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
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack11lll111l_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11ll11ll11_opy_ import bstack1ll1lll1l_opy_
import time
import requests
def bstack11l1l1llll_opy_():
  global CONFIG
  headers = {
        bstack11ll1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬ१"): bstack11ll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ२"),
      }
  proxies = bstack111ll1l11_opy_(CONFIG, bstack1ll1111l1l_opy_)
  try:
    response = requests.get(bstack1ll1111l1l_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1l11111l1_opy_ = response.json()[bstack11ll1l_opy_ (u"ࠨࡪࡸࡦࡸ࠭३")]
      logger.debug(bstack1l1llllll_opy_.format(response.json()))
      return bstack1l11111l1_opy_
    else:
      logger.debug(bstack11l11lll1_opy_.format(bstack11ll1l_opy_ (u"ࠤࡕࡩࡸࡶ࡯࡯ࡵࡨࠤࡏ࡙ࡏࡏࠢࡳࡥࡷࡹࡥࠡࡧࡵࡶࡴࡸࠠࠣ४")))
  except Exception as e:
    logger.debug(bstack11l11lll1_opy_.format(e))
def bstack1l1llll1ll_opy_(hub_url):
  global CONFIG
  url = bstack11ll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ५")+  hub_url + bstack11ll1l_opy_ (u"ࠦ࠴ࡩࡨࡦࡥ࡮ࠦ६")
  headers = {
        bstack11ll1l_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡴࡺࡲࡨࠫ७"): bstack11ll1l_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ८"),
      }
  proxies = bstack111ll1l11_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack11lll1ll1_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1ll1lllll1_opy_.format(hub_url, e))
def bstack1l1l1llll_opy_():
  try:
    global bstack1l1ll1l1ll_opy_
    bstack1l11111l1_opy_ = bstack11l1l1llll_opy_()
    bstack1llll1111l_opy_ = []
    results = []
    for bstack11l11l111_opy_ in bstack1l11111l1_opy_:
      bstack1llll1111l_opy_.append(bstack11ll1l11_opy_(target=bstack1l1llll1ll_opy_,args=(bstack11l11l111_opy_,)))
    for t in bstack1llll1111l_opy_:
      t.start()
    for t in bstack1llll1111l_opy_:
      results.append(t.join())
    bstack1l1l1l1l11_opy_ = {}
    for item in results:
      hub_url = item[bstack11ll1l_opy_ (u"ࠧࡩࡷࡥࡣࡺࡸ࡬ࠨ९")]
      latency = item[bstack11ll1l_opy_ (u"ࠨ࡮ࡤࡸࡪࡴࡣࡺࠩ॰")]
      bstack1l1l1l1l11_opy_[hub_url] = latency
    bstack1ll1l1lll_opy_ = min(bstack1l1l1l1l11_opy_, key= lambda x: bstack1l1l1l1l11_opy_[x])
    bstack1l1ll1l1ll_opy_ = bstack1ll1l1lll_opy_
    logger.debug(bstack11lll1111l_opy_.format(bstack1ll1l1lll_opy_))
  except Exception as e:
    logger.debug(bstack11lll1ll11_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1l1ll1ll11_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack11ll11ll1_opy_, bstack1ll1lll1l1_opy_, bstack1l1l1l111l_opy_, bstack1ll11111_opy_, bstack1lllll1l1l_opy_, \
  Notset, bstack1l1111l11_opy_, \
  bstack1llll1llll_opy_, bstack111l1l1l1_opy_, bstack111lllll1_opy_, bstack11ll111ll_opy_, bstack1ll11l11ll_opy_, bstack1l1l111ll1_opy_, \
  bstack1ll1ll1l1l_opy_, \
  bstack1111l1111_opy_, bstack1l1l111ll_opy_, bstack1ll1ll1111_opy_, bstack11ll11lll1_opy_, \
  bstack111ll1l1l_opy_, bstack1llll11l1l_opy_, bstack1l11lll111_opy_, bstack1111111ll_opy_
from bstack_utils.bstack1l1l11l11l_opy_ import bstack1l1l11l1l1_opy_
from bstack_utils.bstack1ll11ll1l_opy_ import bstack1l11l11ll1_opy_
from bstack_utils.bstack1l1111lll1_opy_ import bstack1ll1lll111_opy_, bstack1llllll11l_opy_
from bstack_utils.bstack1l1l111l_opy_ import bstack1l1llll1_opy_
from bstack_utils.bstack1ll1l1ll_opy_ import bstack1lll11ll_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack11ll1ll1l_opy_
from bstack_utils.proxy import bstack11l1lll11l_opy_, bstack111ll1l11_opy_, bstack1lll1l1lll_opy_, bstack1lll1ll1ll_opy_
import bstack_utils.bstack11l11111_opy_ as bstack111lll1l_opy_
from browserstack_sdk.bstack11l1ll11_opy_ import *
from browserstack_sdk.bstack11ll11ll_opy_ import *
from bstack_utils.bstack1ll1111111_opy_ import bstack1lll1ll1l1_opy_
from browserstack_sdk.bstack1l11111ll_opy_ import *
import bstack_utils.bstack1l1l111111_opy_ as bstack1ll11ll1ll_opy_
import bstack_utils.bstack11lll11l1l_opy_ as bstack1l1111l1l1_opy_
bstack1lllll1l11_opy_ = bstack11ll1l_opy_ (u"ࠩࠣࠤ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠢࠣ࡭࡫࠮ࡰࡢࡩࡨࠤࡂࡃ࠽ࠡࡸࡲ࡭ࡩࠦ࠰ࠪࠢࡾࡠࡳࠦࠠࠡࡶࡵࡽࢀࡢ࡮ࠡࡥࡲࡲࡸࡺࠠࡧࡵࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮࡜ࠨࡨࡶࡠࠬ࠯࠻࡝ࡰࠣࠤࠥࠦࠠࡧࡵ࠱ࡥࡵࡶࡥ࡯ࡦࡉ࡭ࡱ࡫ࡓࡺࡰࡦࠬࡧࡹࡴࡢࡥ࡮ࡣࡵࡧࡴࡩ࠮ࠣࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡵࡥࡩ࡯ࡦࡨࡼ࠮ࠦࠫࠡࠤ࠽ࠦࠥ࠱ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭࠮ࡡࡸࡣ࡬ࡸࠥࡴࡥࡸࡒࡤ࡫ࡪ࠸࠮ࡦࡸࡤࡰࡺࡧࡴࡦࠪࠥࠬ࠮ࠦ࠽࠿ࠢࡾࢁࠧ࠲ࠠ࡝ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡪࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡥࡵࡣ࡬ࡰࡸࠨࡽ࡝ࠩࠬ࠭࠮ࡡࠢࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠥࡡ࠮ࠦࠫࠡࠤ࠯ࡠࡡࡴࠢࠪ࡞ࡱࠤࠥࠦࠠࡾࡥࡤࡸࡨ࡮ࠨࡦࡺࠬࡿࡡࡴࠠࠡࠢࠣࢁࡡࡴࠠࠡࡿ࡟ࡲࠥࠦ࠯ࠫࠢࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࠦࠪ࠰ࠩॱ")
bstack11lll11l11_opy_ = bstack11ll1l_opy_ (u"ࠪࡠࡳ࠵ࠪࠡ࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࠥ࠰࠯࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭ࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠵ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡧࡹࡴࡢࡥ࡮ࡣࡨࡧࡰࡴࠢࡀࠤࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࡞ࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࠰࡯ࡩࡳ࡭ࡴࡩࠢ࠰ࠤ࠶ࡣ࡜࡯ࡥࡲࡲࡸࡺࠠࡱࡡ࡬ࡲࡩ࡫ࡸࠡ࠿ࠣࡴࡷࡵࡣࡦࡵࡶ࠲ࡦࡸࡧࡷ࡝ࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠶ࡢࡢ࡮ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࠮ࡴ࡮࡬ࡧࡪ࠮࠰࠭ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࡥࡷ࡭ࡶ࠯࡮ࡨࡲ࡬ࡺࡨࠡ࠯ࠣ࠷࠮ࡢ࡮ࡤࡱࡱࡷࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮ࠤࡂࠦࡲࡦࡳࡸ࡭ࡷ࡫ࠨࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧ࠯࠻࡝ࡰ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰࡯ࡥࡺࡴࡣࡩࠢࡀࠤࡦࡹࡹ࡯ࡥࠣࠬࡱࡧࡵ࡯ࡥ࡫ࡓࡵࡺࡩࡰࡰࡶ࠭ࠥࡃ࠾ࠡࡽ࡟ࡲࡱ࡫ࡴࠡࡥࡤࡴࡸࡁ࡜࡯ࡶࡵࡽࠥࢁ࡜࡯ࡥࡤࡴࡸࠦ࠽ࠡࡌࡖࡓࡓ࠴ࡰࡢࡴࡶࡩ࠭ࡨࡳࡵࡣࡦ࡯ࡤࡩࡡࡱࡵࠬࡠࡳࠦࠠࡾࠢࡦࡥࡹࡩࡨࠩࡧࡻ࠭ࠥࢁ࡜࡯ࠢࠣࠤࠥࢃ࡜࡯ࠢࠣࡶࡪࡺࡵࡳࡰࠣࡥࡼࡧࡩࡵࠢ࡬ࡱࡵࡵࡲࡵࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠺࡟ࡣࡵࡷࡥࡨࡱ࠮ࡤࡪࡵࡳࡲ࡯ࡵ࡮࠰ࡦࡳࡳࡴࡥࡤࡶࠫࡿࡡࡴࠠࠡࠢࠣࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺ࠺ࠡࡢࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠨࢀ࡫࡮ࡤࡱࡧࡩ࡚ࡘࡉࡄࡱࡰࡴࡴࡴࡥ࡯ࡶࠫࡎࡘࡕࡎ࠯ࡵࡷࡶ࡮ࡴࡧࡪࡨࡼࠬࡨࡧࡰࡴࠫࠬࢁࡥ࠲࡜࡯ࠢࠣࠤࠥ࠴࠮࠯࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳ࡝ࡰࠣࠤࢂ࠯࡜࡯ࡿ࡟ࡲ࠴࠰ࠠ࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࠤ࠯࠵࡜࡯ࠩॲ")
from ._version import __version__
bstack1l111ll1ll_opy_ = None
CONFIG = {}
bstack11ll1ll11l_opy_ = {}
bstack1ll1l11ll1_opy_ = {}
bstack1llll1l11l_opy_ = None
bstack11l1lll1l_opy_ = None
bstack1111l1ll1_opy_ = None
bstack1l1lllll1_opy_ = -1
bstack1l1llll111_opy_ = 0
bstack1lll11l1l1_opy_ = bstack11l1l11l1l_opy_
bstack1ll1ll111_opy_ = 1
bstack1l1l1l1l1l_opy_ = False
bstack11l1ll1l1l_opy_ = False
bstack11l11l11l_opy_ = bstack11ll1l_opy_ (u"ࠫࠬॳ")
bstack1ll1llll11_opy_ = bstack11ll1l_opy_ (u"ࠬ࠭ॴ")
bstack1llll1l1ll_opy_ = False
bstack1ll1l1lll1_opy_ = True
bstack111ll11ll_opy_ = bstack11ll1l_opy_ (u"࠭ࠧॵ")
bstack11l1l1l1l1_opy_ = []
bstack1l1ll1l1ll_opy_ = bstack11ll1l_opy_ (u"ࠧࠨॶ")
bstack11ll11111l_opy_ = False
bstack1l1ll1ll1l_opy_ = None
bstack11lll11111_opy_ = None
bstack1l1ll11lll_opy_ = None
bstack111llll11_opy_ = -1
bstack1l11ll1ll1_opy_ = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠨࢀࠪॷ")), bstack11ll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩॸ"), bstack11ll1l_opy_ (u"ࠪ࠲ࡷࡵࡢࡰࡶ࠰ࡶࡪࡶ࡯ࡳࡶ࠰࡬ࡪࡲࡰࡦࡴ࠱࡮ࡸࡵ࡮ࠨॹ"))
bstack1ll111lll1_opy_ = 0
bstack1l11111l1l_opy_ = 0
bstack1ll1l1l11_opy_ = []
bstack11ll11l11l_opy_ = []
bstack11ll1l1111_opy_ = []
bstack1ll111111_opy_ = []
bstack1ll11ll111_opy_ = bstack11ll1l_opy_ (u"ࠫࠬॺ")
bstack1l1l1l11ll_opy_ = bstack11ll1l_opy_ (u"ࠬ࠭ॻ")
bstack11llll11ll_opy_ = False
bstack1l11ll1l11_opy_ = False
bstack1l1111ll11_opy_ = {}
bstack11llllllll_opy_ = None
bstack11111111l_opy_ = None
bstack11111l11_opy_ = None
bstack1llll1ll11_opy_ = None
bstack1ll11lll1_opy_ = None
bstack1lll1l11ll_opy_ = None
bstack1111l1l1l_opy_ = None
bstack11ll11llll_opy_ = None
bstack11lll1lll_opy_ = None
bstack1ll11lll1l_opy_ = None
bstack1ll1l11l1l_opy_ = None
bstack111ll11l1_opy_ = None
bstack11l1llll1l_opy_ = None
bstack1l1llllll1_opy_ = None
bstack1lll1l1111_opy_ = None
bstack1ll1llll1l_opy_ = None
bstack111l1111l_opy_ = None
bstack1ll1l1l111_opy_ = None
bstack1ll111llll_opy_ = None
bstack11l1l11l11_opy_ = None
bstack1l1ll11ll_opy_ = None
bstack1l1l1111l1_opy_ = None
bstack11ll111lll_opy_ = False
bstack1lll1l1l1_opy_ = bstack11ll1l_opy_ (u"ࠨࠢॼ")
logger = bstack1l1ll1ll11_opy_.get_logger(__name__, bstack1lll11l1l1_opy_)
bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
percy = bstack1l1111l11l_opy_()
bstack1lllllll1_opy_ = bstack1ll1lll1l_opy_()
bstack1ll11111ll_opy_ = bstack1l11111ll_opy_()
def bstack11l1ll1111_opy_():
  global CONFIG
  global bstack11llll11ll_opy_
  global bstack11l111ll_opy_
  bstack1llll1l1l_opy_ = bstack1l11lll11_opy_(CONFIG)
  if bstack1lllll1l1l_opy_(CONFIG):
    if (bstack11ll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩॽ") in bstack1llll1l1l_opy_ and str(bstack1llll1l1l_opy_[bstack11ll1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪॾ")]).lower() == bstack11ll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧॿ")):
      bstack11llll11ll_opy_ = True
    bstack11l111ll_opy_.bstack111l11lll_opy_(bstack1llll1l1l_opy_.get(bstack11ll1l_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧঀ"), False))
  else:
    bstack11llll11ll_opy_ = True
    bstack11l111ll_opy_.bstack111l11lll_opy_(True)
def bstack11l1l11ll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack11l111lll_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack1l1111l111_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack11ll1l_opy_ (u"ࠦ࠲࠳ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡨࡵ࡮ࡧ࡫ࡪࡪ࡮ࡲࡥࠣঁ") == args[i].lower() or bstack11ll1l_opy_ (u"ࠧ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰࡰࡩ࡭࡬ࠨং") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack111ll11ll_opy_
      bstack111ll11ll_opy_ += bstack11ll1l_opy_ (u"࠭࠭࠮ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡃࡰࡰࡩ࡭࡬ࡌࡩ࡭ࡧࠣࠫঃ") + path
      return path
  return None
bstack1l11l1l111_opy_ = re.compile(bstack11ll1l_opy_ (u"ࡲࠣ࠰࠭ࡃࡡࠪࡻࠩ࠰࠭ࡃ࠮ࢃ࠮ࠫࡁࠥ঄"))
def bstack1ll1ll1lll_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack1l11l1l111_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack11ll1l_opy_ (u"ࠣࠦࡾࠦঅ") + group + bstack11ll1l_opy_ (u"ࠤࢀࠦআ"), os.environ.get(group))
  return value
def bstack11111ll1_opy_():
  bstack11l1ll111_opy_ = bstack1l1111l111_opy_()
  if bstack11l1ll111_opy_ and os.path.exists(os.path.abspath(bstack11l1ll111_opy_)):
    fileName = bstack11l1ll111_opy_
  if bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋࠧই") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡔࡔࡆࡊࡉࡢࡊࡎࡒࡅࠨঈ")])) and not bstack11ll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡑࡥࡲ࡫ࠧউ") in locals():
    fileName = os.environ[bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࡤࡌࡉࡍࡇࠪঊ")]
  if bstack11ll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡓࡧ࡭ࡦࠩঋ") in locals():
    bstack1_opy_ = os.path.abspath(fileName)
  else:
    bstack1_opy_ = bstack11ll1l_opy_ (u"ࠨࠩঌ")
  bstack11l11l1ll_opy_ = os.getcwd()
  bstack1l1lll1l11_opy_ = bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡻࡰࡰࠬ঍")
  bstack1lll11l111_opy_ = bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡼࡥࡲࡲࠧ঎")
  while (not os.path.exists(bstack1_opy_)) and bstack11l11l1ll_opy_ != bstack11ll1l_opy_ (u"ࠦࠧএ"):
    bstack1_opy_ = os.path.join(bstack11l11l1ll_opy_, bstack1l1lll1l11_opy_)
    if not os.path.exists(bstack1_opy_):
      bstack1_opy_ = os.path.join(bstack11l11l1ll_opy_, bstack1lll11l111_opy_)
    if bstack11l11l1ll_opy_ != os.path.dirname(bstack11l11l1ll_opy_):
      bstack11l11l1ll_opy_ = os.path.dirname(bstack11l11l1ll_opy_)
    else:
      bstack11l11l1ll_opy_ = bstack11ll1l_opy_ (u"ࠧࠨঐ")
  if not os.path.exists(bstack1_opy_):
    bstack11l1l1ll11_opy_(
      bstack11llll1ll1_opy_.format(os.getcwd()))
  try:
    with open(bstack1_opy_, bstack11ll1l_opy_ (u"࠭ࡲࠨ঑")) as stream:
      yaml.add_implicit_resolver(bstack11ll1l_opy_ (u"ࠢࠢࡲࡤࡸ࡭࡫ࡸࠣ঒"), bstack1l11l1l111_opy_)
      yaml.add_constructor(bstack11ll1l_opy_ (u"ࠣࠣࡳࡥࡹ࡮ࡥࡹࠤও"), bstack1ll1ll1lll_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack1_opy_, bstack11ll1l_opy_ (u"ࠩࡵࠫঔ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack11l1l1ll11_opy_(bstack1l1l111l1_opy_.format(str(exc)))
def bstack1l1ll1lll1_opy_(config):
  bstack1ll11lll11_opy_ = bstack1lllllllll_opy_(config)
  for option in list(bstack1ll11lll11_opy_):
    if option.lower() in bstack1l1l1ll111_opy_ and option != bstack1l1l1ll111_opy_[option.lower()]:
      bstack1ll11lll11_opy_[bstack1l1l1ll111_opy_[option.lower()]] = bstack1ll11lll11_opy_[option]
      del bstack1ll11lll11_opy_[option]
  return config
def bstack11ll11l111_opy_():
  global bstack1ll1l11ll1_opy_
  for key, bstack1l1l11l11_opy_ in bstack1ll111lll_opy_.items():
    if isinstance(bstack1l1l11l11_opy_, list):
      for var in bstack1l1l11l11_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll1l11ll1_opy_[key] = os.environ[var]
          break
    elif bstack1l1l11l11_opy_ in os.environ and os.environ[bstack1l1l11l11_opy_] and str(os.environ[bstack1l1l11l11_opy_]).strip():
      bstack1ll1l11ll1_opy_[key] = os.environ[bstack1l1l11l11_opy_]
  if bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬক") in os.environ:
    bstack1ll1l11ll1_opy_[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨখ")] = {}
    bstack1ll1l11ll1_opy_[bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩগ")][bstack11ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨঘ")] = os.environ[bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩঙ")]
def bstack1llllllll1_opy_():
  global bstack11ll1ll11l_opy_
  global bstack111ll11ll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack11ll1l_opy_ (u"ࠨ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫচ").lower() == val.lower():
      bstack11ll1ll11l_opy_[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ছ")] = {}
      bstack11ll1ll11l_opy_[bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧজ")][bstack11ll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঝ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack11ll1111l1_opy_ in bstack11lll1ll1l_opy_.items():
    if isinstance(bstack11ll1111l1_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack11ll1111l1_opy_:
          if idx < len(sys.argv) and bstack11ll1l_opy_ (u"ࠬ࠳࠭ࠨঞ") + var.lower() == val.lower() and not key in bstack11ll1ll11l_opy_:
            bstack11ll1ll11l_opy_[key] = sys.argv[idx + 1]
            bstack111ll11ll_opy_ += bstack11ll1l_opy_ (u"࠭ࠠ࠮࠯ࠪট") + var + bstack11ll1l_opy_ (u"ࠧࠡࠩঠ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack11ll1l_opy_ (u"ࠨ࠯࠰ࠫড") + bstack11ll1111l1_opy_.lower() == val.lower() and not key in bstack11ll1ll11l_opy_:
          bstack11ll1ll11l_opy_[key] = sys.argv[idx + 1]
          bstack111ll11ll_opy_ += bstack11ll1l_opy_ (u"ࠩࠣ࠱࠲࠭ঢ") + bstack11ll1111l1_opy_ + bstack11ll1l_opy_ (u"ࠪࠤࠬণ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack11l1l1lll1_opy_(config):
  bstack1l111l11ll_opy_ = config.keys()
  for bstack1l1lll1111_opy_, bstack1l11ll1ll_opy_ in bstack1lll1l1l11_opy_.items():
    if bstack1l11ll1ll_opy_ in bstack1l111l11ll_opy_:
      config[bstack1l1lll1111_opy_] = config[bstack1l11ll1ll_opy_]
      del config[bstack1l11ll1ll_opy_]
  for bstack1l1lll1111_opy_, bstack1l11ll1ll_opy_ in bstack1l111l1lll_opy_.items():
    if isinstance(bstack1l11ll1ll_opy_, list):
      for bstack1llll11l1_opy_ in bstack1l11ll1ll_opy_:
        if bstack1llll11l1_opy_ in bstack1l111l11ll_opy_:
          config[bstack1l1lll1111_opy_] = config[bstack1llll11l1_opy_]
          del config[bstack1llll11l1_opy_]
          break
    elif bstack1l11ll1ll_opy_ in bstack1l111l11ll_opy_:
      config[bstack1l1lll1111_opy_] = config[bstack1l11ll1ll_opy_]
      del config[bstack1l11ll1ll_opy_]
  for bstack1llll11l1_opy_ in list(config):
    for bstack1l1lllll11_opy_ in bstack1l1l1lll1_opy_:
      if bstack1llll11l1_opy_.lower() == bstack1l1lllll11_opy_.lower() and bstack1llll11l1_opy_ != bstack1l1lllll11_opy_:
        config[bstack1l1lllll11_opy_] = config[bstack1llll11l1_opy_]
        del config[bstack1llll11l1_opy_]
  bstack11llll11l1_opy_ = [{}]
  if not config.get(bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧত")):
    config[bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨথ")] = [{}]
  bstack11llll11l1_opy_ = config[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩদ")]
  for platform in bstack11llll11l1_opy_:
    for bstack1llll11l1_opy_ in list(platform):
      for bstack1l1lllll11_opy_ in bstack1l1l1lll1_opy_:
        if bstack1llll11l1_opy_.lower() == bstack1l1lllll11_opy_.lower() and bstack1llll11l1_opy_ != bstack1l1lllll11_opy_:
          platform[bstack1l1lllll11_opy_] = platform[bstack1llll11l1_opy_]
          del platform[bstack1llll11l1_opy_]
  for bstack1l1lll1111_opy_, bstack1l11ll1ll_opy_ in bstack1l111l1lll_opy_.items():
    for platform in bstack11llll11l1_opy_:
      if isinstance(bstack1l11ll1ll_opy_, list):
        for bstack1llll11l1_opy_ in bstack1l11ll1ll_opy_:
          if bstack1llll11l1_opy_ in platform:
            platform[bstack1l1lll1111_opy_] = platform[bstack1llll11l1_opy_]
            del platform[bstack1llll11l1_opy_]
            break
      elif bstack1l11ll1ll_opy_ in platform:
        platform[bstack1l1lll1111_opy_] = platform[bstack1l11ll1ll_opy_]
        del platform[bstack1l11ll1ll_opy_]
  for bstack1l1ll11ll1_opy_ in bstack11lll11ll1_opy_:
    if bstack1l1ll11ll1_opy_ in config:
      if not bstack11lll11ll1_opy_[bstack1l1ll11ll1_opy_] in config:
        config[bstack11lll11ll1_opy_[bstack1l1ll11ll1_opy_]] = {}
      config[bstack11lll11ll1_opy_[bstack1l1ll11ll1_opy_]].update(config[bstack1l1ll11ll1_opy_])
      del config[bstack1l1ll11ll1_opy_]
  for platform in bstack11llll11l1_opy_:
    for bstack1l1ll11ll1_opy_ in bstack11lll11ll1_opy_:
      if bstack1l1ll11ll1_opy_ in list(platform):
        if not bstack11lll11ll1_opy_[bstack1l1ll11ll1_opy_] in platform:
          platform[bstack11lll11ll1_opy_[bstack1l1ll11ll1_opy_]] = {}
        platform[bstack11lll11ll1_opy_[bstack1l1ll11ll1_opy_]].update(platform[bstack1l1ll11ll1_opy_])
        del platform[bstack1l1ll11ll1_opy_]
  config = bstack1l1ll1lll1_opy_(config)
  return config
def bstack11l1ll1l11_opy_(config):
  global bstack1ll1llll11_opy_
  if bstack1lllll1l1l_opy_(config) and bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫধ") in config and str(config[bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬন")]).lower() != bstack11ll1l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ঩"):
    if not bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧপ") in config:
      config[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨফ")] = {}
    if not config[bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩব")].get(bstack11ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡆ࡮ࡴࡡࡳࡻࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡷࡦࡺࡩࡰࡰࠪভ")) and not bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩম") in config[bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬয")]:
      bstack1lll11l1_opy_ = datetime.datetime.now()
      bstack1lll11111l_opy_ = bstack1lll11l1_opy_.strftime(bstack11ll1l_opy_ (u"ࠩࠨࡨࡤࠫࡢࡠࠧࡋࠩࡒ࠭র"))
      hostname = socket.gethostname()
      bstack1llll1l111_opy_ = bstack11ll1l_opy_ (u"ࠪࠫ঱").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack11ll1l_opy_ (u"ࠫࢀࢃ࡟ࡼࡿࡢࡿࢂ࠭ল").format(bstack1lll11111l_opy_, hostname, bstack1llll1l111_opy_)
      config[bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ঳")][bstack11ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ঴")] = identifier
    bstack1ll1llll11_opy_ = config[bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ঵")].get(bstack11ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪশ"))
  return config
def bstack11lllll1l1_opy_():
  bstack11111lll_opy_ =  bstack11ll111ll_opy_()[bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠨষ")]
  return bstack11111lll_opy_ if bstack11111lll_opy_ else -1
def bstack1l1lll1ll_opy_(bstack11111lll_opy_):
  global CONFIG
  if not bstack11ll1l_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬস") in CONFIG[bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭হ")]:
    return
  CONFIG[bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ঺")] = CONFIG[bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ঻")].replace(
    bstack11ll1l_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾ়ࠩ"),
    str(bstack11111lll_opy_)
  )
def bstack1l1ll111ll_opy_():
  global CONFIG
  if not bstack11ll1l_opy_ (u"ࠨࠦࡾࡈࡆ࡚ࡅࡠࡖࡌࡑࡊࢃࠧঽ") in CONFIG[bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫা")]:
    return
  bstack1lll11l1_opy_ = datetime.datetime.now()
  bstack1lll11111l_opy_ = bstack1lll11l1_opy_.strftime(bstack11ll1l_opy_ (u"ࠪࠩࡩ࠳ࠥࡣ࠯ࠨࡌ࠿ࠫࡍࠨি"))
  CONFIG[bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ী")] = CONFIG[bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧু")].replace(
    bstack11ll1l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬূ"),
    bstack1lll11111l_opy_
  )
def bstack1llll1l11_opy_():
  global CONFIG
  if bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩৃ") in CONFIG and not bool(CONFIG[bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৄ")]):
    del CONFIG[bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ৅")]
    return
  if not bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৆") in CONFIG:
    CONFIG[bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ে")] = bstack11ll1l_opy_ (u"ࠬࠩࠤࡼࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࡽࠨৈ")
  if bstack11ll1l_opy_ (u"࠭ࠤࡼࡆࡄࡘࡊࡥࡔࡊࡏࡈࢁࠬ৉") in CONFIG[bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ৊")]:
    bstack1l1ll111ll_opy_()
    os.environ[bstack11ll1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡠࡅࡒࡑࡇࡏࡎࡆࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬো")] = CONFIG[bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫৌ")]
  if not bstack11ll1l_opy_ (u"ࠪࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁ্ࠬ") in CONFIG[bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ৎ")]:
    return
  bstack11111lll_opy_ = bstack11ll1l_opy_ (u"ࠬ࠭৏")
  bstack1l1l11ll1_opy_ = bstack11lllll1l1_opy_()
  if bstack1l1l11ll1_opy_ != -1:
    bstack11111lll_opy_ = bstack11ll1l_opy_ (u"࠭ࡃࡊࠢࠪ৐") + str(bstack1l1l11ll1_opy_)
  if bstack11111lll_opy_ == bstack11ll1l_opy_ (u"ࠧࠨ৑"):
    bstack1ll1111ll1_opy_ = bstack1llllll1l1_opy_(CONFIG[bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ৒")])
    if bstack1ll1111ll1_opy_ != -1:
      bstack11111lll_opy_ = str(bstack1ll1111ll1_opy_)
  if bstack11111lll_opy_:
    bstack1l1lll1ll_opy_(bstack11111lll_opy_)
    os.environ[bstack11ll1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭৓")] = CONFIG[bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ৔")]
def bstack1l1111ll1_opy_(bstack1ll111ll1l_opy_, bstack11ll1l1l1l_opy_, path):
  bstack1l111lllll_opy_ = {
    bstack11ll1l_opy_ (u"ࠫ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ৕"): bstack11ll1l1l1l_opy_
  }
  if os.path.exists(path):
    bstack1ll1llll1_opy_ = json.load(open(path, bstack11ll1l_opy_ (u"ࠬࡸࡢࠨ৖")))
  else:
    bstack1ll1llll1_opy_ = {}
  bstack1ll1llll1_opy_[bstack1ll111ll1l_opy_] = bstack1l111lllll_opy_
  with open(path, bstack11ll1l_opy_ (u"ࠨࡷࠬࠤৗ")) as outfile:
    json.dump(bstack1ll1llll1_opy_, outfile)
def bstack1llllll1l1_opy_(bstack1ll111ll1l_opy_):
  bstack1ll111ll1l_opy_ = str(bstack1ll111ll1l_opy_)
  bstack11l1l1lll_opy_ = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠧࡿࠩ৘")), bstack11ll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ৙"))
  try:
    if not os.path.exists(bstack11l1l1lll_opy_):
      os.makedirs(bstack11l1l1lll_opy_)
    file_path = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠩࢁࠫ৚")), bstack11ll1l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ৛"), bstack11ll1l_opy_ (u"ࠫ࠳ࡨࡵࡪ࡮ࡧ࠱ࡳࡧ࡭ࡦ࠯ࡦࡥࡨ࡮ࡥ࠯࡬ࡶࡳࡳ࠭ড়"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack11ll1l_opy_ (u"ࠬࡽࠧঢ়")):
        pass
      with open(file_path, bstack11ll1l_opy_ (u"ࠨࡷࠬࠤ৞")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack11ll1l_opy_ (u"ࠧࡳࠩয়")) as bstack11ll11l11_opy_:
      bstack1l111l11l1_opy_ = json.load(bstack11ll11l11_opy_)
    if bstack1ll111ll1l_opy_ in bstack1l111l11l1_opy_:
      bstack1lll1l1ll1_opy_ = bstack1l111l11l1_opy_[bstack1ll111ll1l_opy_][bstack11ll1l_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬৠ")]
      bstack111ll111l_opy_ = int(bstack1lll1l1ll1_opy_) + 1
      bstack1l1111ll1_opy_(bstack1ll111ll1l_opy_, bstack111ll111l_opy_, file_path)
      return bstack111ll111l_opy_
    else:
      bstack1l1111ll1_opy_(bstack1ll111ll1l_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1111111_opy_.format(str(e)))
    return -1
def bstack1111l1l1_opy_(config):
  if not config[bstack11ll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫৡ")] or not config[bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ৢ")]:
    return True
  else:
    return False
def bstack1ll1l111l_opy_(config, index=0):
  global bstack1llll1l1ll_opy_
  bstack1ll1lll11_opy_ = {}
  caps = bstack1ll1l1ll1l_opy_ + bstack1ll111l1ll_opy_
  if bstack1llll1l1ll_opy_:
    caps += bstack111lll1ll_opy_
  for key in config:
    if key in caps + [bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৣ")]:
      continue
    bstack1ll1lll11_opy_[key] = config[key]
  if bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৤") in config:
    for bstack1l1lllll1l_opy_ in config[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৥")][index]:
      if bstack1l1lllll1l_opy_ in caps:
        continue
      bstack1ll1lll11_opy_[bstack1l1lllll1l_opy_] = config[bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ০")][index][bstack1l1lllll1l_opy_]
  bstack1ll1lll11_opy_[bstack11ll1l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪ১")] = socket.gethostname()
  if bstack11ll1l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪ২") in bstack1ll1lll11_opy_:
    del (bstack1ll1lll11_opy_[bstack11ll1l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫ৩")])
  return bstack1ll1lll11_opy_
def bstack11l1lll1ll_opy_(config):
  global bstack1llll1l1ll_opy_
  bstack1lll11lll1_opy_ = {}
  caps = bstack1ll111l1ll_opy_
  if bstack1llll1l1ll_opy_:
    caps += bstack111lll1ll_opy_
  for key in caps:
    if key in config:
      bstack1lll11lll1_opy_[key] = config[key]
  return bstack1lll11lll1_opy_
def bstack11l1lll1l1_opy_(bstack1ll1lll11_opy_, bstack1lll11lll1_opy_):
  bstack1ll111l11l_opy_ = {}
  for key in bstack1ll1lll11_opy_.keys():
    if key in bstack1lll1l1l11_opy_:
      bstack1ll111l11l_opy_[bstack1lll1l1l11_opy_[key]] = bstack1ll1lll11_opy_[key]
    else:
      bstack1ll111l11l_opy_[key] = bstack1ll1lll11_opy_[key]
  for key in bstack1lll11lll1_opy_:
    if key in bstack1lll1l1l11_opy_:
      bstack1ll111l11l_opy_[bstack1lll1l1l11_opy_[key]] = bstack1lll11lll1_opy_[key]
    else:
      bstack1ll111l11l_opy_[key] = bstack1lll11lll1_opy_[key]
  return bstack1ll111l11l_opy_
def bstack11ll11ll1l_opy_(config, index=0):
  global bstack1llll1l1ll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack11ll11l1ll_opy_ = bstack11ll11ll1_opy_(bstack11l1lllll1_opy_, config, logger)
  bstack1lll11lll1_opy_ = bstack11l1lll1ll_opy_(config)
  bstack1lll11l11l_opy_ = bstack1ll111l1ll_opy_
  bstack1lll11l11l_opy_ += bstack11lllll11l_opy_
  bstack1lll11lll1_opy_ = update(bstack1lll11lll1_opy_, bstack11ll11l1ll_opy_)
  if bstack1llll1l1ll_opy_:
    bstack1lll11l11l_opy_ += bstack111lll1ll_opy_
  if bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৪") in config:
    if bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ৫") in config[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৬")][index]:
      caps[bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ৭")] = config[bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৮")][index][bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ৯")]
    if bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫৰ") in config[bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৱ")][index]:
      caps[bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭৲")] = str(config[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৳")][index][bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ৴")])
    bstack1l111lll1l_opy_ = bstack11ll11ll1_opy_(bstack11l1lllll1_opy_, config[bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ৵")][index], logger)
    bstack1lll11l11l_opy_ += list(bstack1l111lll1l_opy_.keys())
    for bstack11ll1ll111_opy_ in bstack1lll11l11l_opy_:
      if bstack11ll1ll111_opy_ in config[bstack11ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ৶")][index]:
        if bstack11ll1ll111_opy_ == bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ৷"):
          try:
            bstack1l111lll1l_opy_[bstack11ll1ll111_opy_] = str(config[bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ৸")][index][bstack11ll1ll111_opy_] * 1.0)
          except:
            bstack1l111lll1l_opy_[bstack11ll1ll111_opy_] = str(config[bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৹")][index][bstack11ll1ll111_opy_])
        else:
          bstack1l111lll1l_opy_[bstack11ll1ll111_opy_] = config[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ৺")][index][bstack11ll1ll111_opy_]
        del (config[bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৻")][index][bstack11ll1ll111_opy_])
    bstack1lll11lll1_opy_ = update(bstack1lll11lll1_opy_, bstack1l111lll1l_opy_)
  bstack1ll1lll11_opy_ = bstack1ll1l111l_opy_(config, index)
  for bstack1llll11l1_opy_ in bstack1ll111l1ll_opy_ + list(bstack11ll11l1ll_opy_.keys()):
    if bstack1llll11l1_opy_ in bstack1ll1lll11_opy_:
      bstack1lll11lll1_opy_[bstack1llll11l1_opy_] = bstack1ll1lll11_opy_[bstack1llll11l1_opy_]
      del (bstack1ll1lll11_opy_[bstack1llll11l1_opy_])
  if bstack1l1111l11_opy_(config):
    bstack1ll1lll11_opy_[bstack11ll1l_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨৼ")] = True
    caps.update(bstack1lll11lll1_opy_)
    caps[bstack11ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ৽")] = bstack1ll1lll11_opy_
  else:
    bstack1ll1lll11_opy_[bstack11ll1l_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ৾")] = False
    caps.update(bstack11l1lll1l1_opy_(bstack1ll1lll11_opy_, bstack1lll11lll1_opy_))
    if bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ৿") in caps:
      caps[bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭਀")] = caps[bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫਁ")]
      del (caps[bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬਂ")])
    if bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩਃ") in caps:
      caps[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ਄")] = caps[bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫਅ")]
      del (caps[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬਆ")])
  return caps
def bstack1llll111l_opy_():
  global bstack1l1ll1l1ll_opy_
  if bstack11l111lll_opy_() <= version.parse(bstack11ll1l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬਇ")):
    if bstack1l1ll1l1ll_opy_ != bstack11ll1l_opy_ (u"࠭ࠧਈ"):
      return bstack11ll1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣਉ") + bstack1l1ll1l1ll_opy_ + bstack11ll1l_opy_ (u"ࠣ࠼࠻࠴࠴ࡽࡤ࠰ࡪࡸࡦࠧਊ")
    return bstack1lll11ll11_opy_
  if bstack1l1ll1l1ll_opy_ != bstack11ll1l_opy_ (u"ࠩࠪ਋"):
    return bstack11ll1l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ਌") + bstack1l1ll1l1ll_opy_ + bstack11ll1l_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧ਍")
  return bstack11ll1l1l1_opy_
def bstack111111111_opy_(options):
  return hasattr(options, bstack11ll1l_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭਎"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack1l1l1l1111_opy_(options, bstack1111ll11l_opy_):
  for bstack1l1ll1l111_opy_ in bstack1111ll11l_opy_:
    if bstack1l1ll1l111_opy_ in [bstack11ll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫਏ"), bstack11ll1l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫਐ")]:
      continue
    if bstack1l1ll1l111_opy_ in options._experimental_options:
      options._experimental_options[bstack1l1ll1l111_opy_] = update(options._experimental_options[bstack1l1ll1l111_opy_],
                                                         bstack1111ll11l_opy_[bstack1l1ll1l111_opy_])
    else:
      options.add_experimental_option(bstack1l1ll1l111_opy_, bstack1111ll11l_opy_[bstack1l1ll1l111_opy_])
  if bstack11ll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭਑") in bstack1111ll11l_opy_:
    for arg in bstack1111ll11l_opy_[bstack11ll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ਒")]:
      options.add_argument(arg)
    del (bstack1111ll11l_opy_[bstack11ll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨਓ")])
  if bstack11ll1l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨਔ") in bstack1111ll11l_opy_:
    for ext in bstack1111ll11l_opy_[bstack11ll1l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩਕ")]:
      options.add_extension(ext)
    del (bstack1111ll11l_opy_[bstack11ll1l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪਖ")])
def bstack1l1111111l_opy_(options, bstack11111l11l_opy_):
  if bstack11ll1l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ਗ") in bstack11111l11l_opy_:
    for bstack1lllll111_opy_ in bstack11111l11l_opy_[bstack11ll1l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧਘ")]:
      if bstack1lllll111_opy_ in options._preferences:
        options._preferences[bstack1lllll111_opy_] = update(options._preferences[bstack1lllll111_opy_], bstack11111l11l_opy_[bstack11ll1l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨਙ")][bstack1lllll111_opy_])
      else:
        options.set_preference(bstack1lllll111_opy_, bstack11111l11l_opy_[bstack11ll1l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩਚ")][bstack1lllll111_opy_])
  if bstack11ll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩਛ") in bstack11111l11l_opy_:
    for arg in bstack11111l11l_opy_[bstack11ll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪਜ")]:
      options.add_argument(arg)
def bstack1l1ll1l11_opy_(options, bstack1ll111l1l_opy_):
  if bstack11ll1l_opy_ (u"࠭ࡷࡦࡤࡹ࡭ࡪࡽࠧਝ") in bstack1ll111l1l_opy_:
    options.use_webview(bool(bstack1ll111l1l_opy_[bstack11ll1l_opy_ (u"ࠧࡸࡧࡥࡺ࡮࡫ࡷࠨਞ")]))
  bstack1l1l1l1111_opy_(options, bstack1ll111l1l_opy_)
def bstack11lll1l111_opy_(options, bstack11l1ll1ll_opy_):
  for bstack1l1l1ll1l1_opy_ in bstack11l1ll1ll_opy_:
    if bstack1l1l1ll1l1_opy_ in [bstack11ll1l_opy_ (u"ࠨࡶࡨࡧ࡭ࡴ࡯࡭ࡱࡪࡽࡕࡸࡥࡷ࡫ࡨࡻࠬਟ"), bstack11ll1l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧਠ")]:
      continue
    options.set_capability(bstack1l1l1ll1l1_opy_, bstack11l1ll1ll_opy_[bstack1l1l1ll1l1_opy_])
  if bstack11ll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨਡ") in bstack11l1ll1ll_opy_:
    for arg in bstack11l1ll1ll_opy_[bstack11ll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩਢ")]:
      options.add_argument(arg)
  if bstack11ll1l_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩਣ") in bstack11l1ll1ll_opy_:
    options.bstack1lll1lll1l_opy_(bool(bstack11l1ll1ll_opy_[bstack11ll1l_opy_ (u"࠭ࡴࡦࡥ࡫ࡲࡴࡲ࡯ࡨࡻࡓࡶࡪࡼࡩࡦࡹࠪਤ")]))
def bstack1ll111l11_opy_(options, bstack1l1l1l1ll1_opy_):
  for bstack1l1ll111l1_opy_ in bstack1l1l1l1ll1_opy_:
    if bstack1l1ll111l1_opy_ in [bstack11ll1l_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫਥ"), bstack11ll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ਦ")]:
      continue
    options._options[bstack1l1ll111l1_opy_] = bstack1l1l1l1ll1_opy_[bstack1l1ll111l1_opy_]
  if bstack11ll1l_opy_ (u"ࠩࡤࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ਧ") in bstack1l1l1l1ll1_opy_:
    for bstack11lll1l11_opy_ in bstack1l1l1l1ll1_opy_[bstack11ll1l_opy_ (u"ࠪࡥࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧਨ")]:
      options.bstack1l1ll1111l_opy_(
        bstack11lll1l11_opy_, bstack1l1l1l1ll1_opy_[bstack11ll1l_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ਩")][bstack11lll1l11_opy_])
  if bstack11ll1l_opy_ (u"ࠬࡧࡲࡨࡵࠪਪ") in bstack1l1l1l1ll1_opy_:
    for arg in bstack1l1l1l1ll1_opy_[bstack11ll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫਫ")]:
      options.add_argument(arg)
def bstack11ll1l1l11_opy_(options, caps):
  if not hasattr(options, bstack11ll1l_opy_ (u"ࠧࡌࡇ࡜ࠫਬ")):
    return
  if options.KEY == bstack11ll1l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ਭ") and options.KEY in caps:
    bstack1l1l1l1111_opy_(options, caps[bstack11ll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧਮ")])
  elif options.KEY == bstack11ll1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨਯ") and options.KEY in caps:
    bstack1l1111111l_opy_(options, caps[bstack11ll1l_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩਰ")])
  elif options.KEY == bstack11ll1l_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭࠳ࡵࡰࡵ࡫ࡲࡲࡸ࠭਱") and options.KEY in caps:
    bstack11lll1l111_opy_(options, caps[bstack11ll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧਲ")])
  elif options.KEY == bstack11ll1l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨਲ਼") and options.KEY in caps:
    bstack1l1ll1l11_opy_(options, caps[bstack11ll1l_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ਴")])
  elif options.KEY == bstack11ll1l_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨਵ") and options.KEY in caps:
    bstack1ll111l11_opy_(options, caps[bstack11ll1l_opy_ (u"ࠪࡷࡪࡀࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩਸ਼")])
def bstack1l111ll111_opy_(caps):
  global bstack1llll1l1ll_opy_
  if isinstance(os.environ.get(bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ਷")), str):
    bstack1llll1l1ll_opy_ = eval(os.getenv(bstack11ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭ਸ")))
  if bstack1llll1l1ll_opy_:
    if bstack11l1l11ll_opy_() < version.parse(bstack11ll1l_opy_ (u"࠭࠲࠯࠵࠱࠴ࠬਹ")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack11ll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ਺")
    if bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭਻") in caps:
      browser = caps[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫਼ࠧ")]
    elif bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ਽") in caps:
      browser = caps[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬਾ")]
    browser = str(browser).lower()
    if browser == bstack11ll1l_opy_ (u"ࠬ࡯ࡰࡩࡱࡱࡩࠬਿ") or browser == bstack11ll1l_opy_ (u"࠭ࡩࡱࡣࡧࠫੀ"):
      browser = bstack11ll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࠧੁ")
    if browser == bstack11ll1l_opy_ (u"ࠨࡵࡤࡱࡸࡻ࡮ࡨࠩੂ"):
      browser = bstack11ll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ੃")
    if browser not in [bstack11ll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ੄"), bstack11ll1l_opy_ (u"ࠫࡪࡪࡧࡦࠩ੅"), bstack11ll1l_opy_ (u"ࠬ࡯ࡥࠨ੆"), bstack11ll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠭ੇ"), bstack11ll1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨੈ")]:
      return None
    try:
      package = bstack11ll1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷ࠴ࡻࡾ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ੉").format(browser)
      name = bstack11ll1l_opy_ (u"ࠩࡒࡴࡹ࡯࡯࡯ࡵࠪ੊")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack111111111_opy_(options):
        return None
      for bstack1llll11l1_opy_ in caps.keys():
        options.set_capability(bstack1llll11l1_opy_, caps[bstack1llll11l1_opy_])
      bstack11ll1l1l11_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l111111l1_opy_(options, bstack1ll11l1lll_opy_):
  if not bstack111111111_opy_(options):
    return
  for bstack1llll11l1_opy_ in bstack1ll11l1lll_opy_.keys():
    if bstack1llll11l1_opy_ in bstack11lllll11l_opy_:
      continue
    if bstack1llll11l1_opy_ in options._caps and type(options._caps[bstack1llll11l1_opy_]) in [dict, list]:
      options._caps[bstack1llll11l1_opy_] = update(options._caps[bstack1llll11l1_opy_], bstack1ll11l1lll_opy_[bstack1llll11l1_opy_])
    else:
      options.set_capability(bstack1llll11l1_opy_, bstack1ll11l1lll_opy_[bstack1llll11l1_opy_])
  bstack11ll1l1l11_opy_(options, bstack1ll11l1lll_opy_)
  if bstack11ll1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡥࡧࡥࡹ࡬࡭ࡥࡳࡃࡧࡨࡷ࡫ࡳࡴࠩੋ") in options._caps:
    if options._caps[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩੌ")] and options._caps[bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧ੍ࠪ")].lower() != bstack11ll1l_opy_ (u"࠭ࡦࡪࡴࡨࡪࡴࡾࠧ੎"):
      del options._caps[bstack11ll1l_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭੏")]
def bstack1111ll1ll_opy_(proxy_config):
  if bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ੐") in proxy_config:
    proxy_config[bstack11ll1l_opy_ (u"ࠩࡶࡷࡱࡖࡲࡰࡺࡼࠫੑ")] = proxy_config[bstack11ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ੒")]
    del (proxy_config[bstack11ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨ੓")])
  if bstack11ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ੔") in proxy_config and proxy_config[bstack11ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡙ࡿࡰࡦࠩ੕")].lower() != bstack11ll1l_opy_ (u"ࠧࡥ࡫ࡵࡩࡨࡺࠧ੖"):
    proxy_config[bstack11ll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ੗")] = bstack11ll1l_opy_ (u"ࠩࡰࡥࡳࡻࡡ࡭ࠩ੘")
  if bstack11ll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡃࡸࡸࡴࡩ࡯࡯ࡨ࡬࡫࡚ࡸ࡬ࠨਖ਼") in proxy_config:
    proxy_config[bstack11ll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡗࡽࡵ࡫ࠧਗ਼")] = bstack11ll1l_opy_ (u"ࠬࡶࡡࡤࠩਜ਼")
  return proxy_config
def bstack11ll11l1l1_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack11ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬੜ") in config:
    return proxy
  config[bstack11ll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭੝")] = bstack1111ll1ll_opy_(config[bstack11ll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧਫ਼")])
  if proxy == None:
    proxy = Proxy(config[bstack11ll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࠨ੟")])
  return proxy
def bstack11l11ll11_opy_(self):
  global CONFIG
  global bstack111ll11l1_opy_
  try:
    proxy = bstack1lll1l1lll_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack11ll1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨ੠")):
        proxies = bstack11l1lll11l_opy_(proxy, bstack1llll111l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1ll111l_opy_ = proxies.popitem()
          if bstack11ll1l_opy_ (u"ࠦ࠿࠵࠯ࠣ੡") in bstack1l1ll111l_opy_:
            return bstack1l1ll111l_opy_
          else:
            return bstack11ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ੢") + bstack1l1ll111l_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack11ll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥ੣").format(str(e)))
  return bstack111ll11l1_opy_(self)
def bstack11ll1l11l_opy_():
  global CONFIG
  return bstack1lll1ll1ll_opy_(CONFIG) and bstack1l1l111ll1_opy_() and bstack11l111lll_opy_() >= version.parse(bstack1l1lll11l1_opy_)
def bstack1lll1111l1_opy_():
  global CONFIG
  return (bstack11ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ੤") in CONFIG or bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ੥") in CONFIG) and bstack1ll1ll1l1l_opy_()
def bstack1lllllllll_opy_(config):
  bstack1ll11lll11_opy_ = {}
  if bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭੦") in config:
    bstack1ll11lll11_opy_ = config[bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ੧")]
  if bstack11ll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ੨") in config:
    bstack1ll11lll11_opy_ = config[bstack11ll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ੩")]
  proxy = bstack1lll1l1lll_opy_(config)
  if proxy:
    if proxy.endswith(bstack11ll1l_opy_ (u"࠭࠮ࡱࡣࡦࠫ੪")) and os.path.isfile(proxy):
      bstack1ll11lll11_opy_[bstack11ll1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪ੫")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack11ll1l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭੬")):
        proxies = bstack111ll1l11_opy_(config, bstack1llll111l_opy_())
        if len(proxies) > 0:
          protocol, bstack1l1ll111l_opy_ = proxies.popitem()
          if bstack11ll1l_opy_ (u"ࠤ࠽࠳࠴ࠨ੭") in bstack1l1ll111l_opy_:
            parsed_url = urlparse(bstack1l1ll111l_opy_)
          else:
            parsed_url = urlparse(protocol + bstack11ll1l_opy_ (u"ࠥ࠾࠴࠵ࠢ੮") + bstack1l1ll111l_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll11lll11_opy_[bstack11ll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡋࡳࡸࡺࠧ੯")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll11lll11_opy_[bstack11ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡴࡸࡴࠨੰ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll11lll11_opy_[bstack11ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩੱ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll11lll11_opy_[bstack11ll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪੲ")] = str(parsed_url.password)
  return bstack1ll11lll11_opy_
def bstack1l11lll11_opy_(config):
  if bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡉ࡯࡯ࡶࡨࡼࡹࡕࡰࡵ࡫ࡲࡲࡸ࠭ੳ") in config:
    return config[bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺࡃࡰࡰࡷࡩࡽࡺࡏࡱࡶ࡬ࡳࡳࡹࠧੴ")]
  return {}
def bstack1l1lll1l1_opy_(caps):
  global bstack1ll1llll11_opy_
  if bstack11ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫੵ") in caps:
    caps[bstack11ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ੶")][bstack11ll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫ੷")] = True
    if bstack1ll1llll11_opy_:
      caps[bstack11ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ੸")][bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ੹")] = bstack1ll1llll11_opy_
  else:
    caps[bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭੺")] = True
    if bstack1ll1llll11_opy_:
      caps[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ੻")] = bstack1ll1llll11_opy_
def bstack111lll1l1_opy_():
  global CONFIG
  if not bstack1lllll1l1l_opy_(CONFIG):
    return
  if bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ੼") in CONFIG and bstack1l11lll111_opy_(CONFIG[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ੽")]):
    if (
      bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ੾") in CONFIG
      and bstack1l11lll111_opy_(CONFIG[bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ੿")].get(bstack11ll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡇ࡯࡮ࡢࡴࡼࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡸࡧࡴࡪࡱࡱࠫ઀")))
    ):
      logger.debug(bstack11ll1l_opy_ (u"ࠣࡎࡲࡧࡦࡲࠠࡣ࡫ࡱࡥࡷࡿࠠ࡯ࡱࡷࠤࡸࡺࡡࡳࡶࡨࡨࠥࡧࡳࠡࡵ࡮࡭ࡵࡈࡩ࡯ࡣࡵࡽࡎࡴࡩࡵ࡫ࡤࡰ࡮ࡹࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡧࡱࡥࡧࡲࡥࡥࠤઁ"))
      return
    bstack1ll11lll11_opy_ = bstack1lllllllll_opy_(CONFIG)
    bstack11ll111111_opy_(CONFIG[bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬં")], bstack1ll11lll11_opy_)
def bstack11ll111111_opy_(key, bstack1ll11lll11_opy_):
  global bstack1l111ll1ll_opy_
  logger.info(bstack1ll1lll1ll_opy_)
  try:
    bstack1l111ll1ll_opy_ = Local()
    bstack1ll11111l_opy_ = {bstack11ll1l_opy_ (u"ࠪ࡯ࡪࡿࠧઃ"): key}
    bstack1ll11111l_opy_.update(bstack1ll11lll11_opy_)
    logger.debug(bstack1ll11llll_opy_.format(str(bstack1ll11111l_opy_)))
    bstack1l111ll1ll_opy_.start(**bstack1ll11111l_opy_)
    if bstack1l111ll1ll_opy_.isRunning():
      logger.info(bstack1ll1l11l11_opy_)
  except Exception as e:
    bstack11l1l1ll11_opy_(bstack1l1ll11111_opy_.format(str(e)))
def bstack1llll1ll1l_opy_():
  global bstack1l111ll1ll_opy_
  if bstack1l111ll1ll_opy_.isRunning():
    logger.info(bstack1ll1l111l1_opy_)
    bstack1l111ll1ll_opy_.stop()
  bstack1l111ll1ll_opy_ = None
def bstack1lll111lll_opy_(bstack1ll1111l1_opy_=[]):
  global CONFIG
  bstack11111ll11_opy_ = []
  bstack1lll1l11l_opy_ = [bstack11ll1l_opy_ (u"ࠫࡴࡹࠧ઄"), bstack11ll1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઅ"), bstack11ll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪઆ"), bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩઇ"), bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ઈ"), bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪઉ")]
  try:
    for err in bstack1ll1111l1_opy_:
      bstack1l11lll11l_opy_ = {}
      for k in bstack1lll1l11l_opy_:
        val = CONFIG[bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ઊ")][int(err[bstack11ll1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪઋ")])].get(k)
        if val:
          bstack1l11lll11l_opy_[k] = val
      if(err[bstack11ll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫઌ")] != bstack11ll1l_opy_ (u"࠭ࠧઍ")):
        bstack1l11lll11l_opy_[bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡸ࠭઎")] = {
          err[bstack11ll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭એ")]: err[bstack11ll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨઐ")]
        }
        bstack11111ll11_opy_.append(bstack1l11lll11l_opy_)
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡬࡯ࡳ࡯ࡤࡸࡹ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶ࠽ࠤࠬઑ") + str(e))
  finally:
    return bstack11111ll11_opy_
def bstack11llll1111_opy_(file_name):
  bstack1l1l11ll11_opy_ = []
  try:
    bstack1l111l11l_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1l111l11l_opy_):
      with open(bstack1l111l11l_opy_) as f:
        bstack1111lll1l_opy_ = json.load(f)
        bstack1l1l11ll11_opy_ = bstack1111lll1l_opy_
      os.remove(bstack1l111l11l_opy_)
    return bstack1l1l11ll11_opy_
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡦࡪࡰࡧ࡭ࡳ࡭ࠠࡦࡴࡵࡳࡷࠦ࡬ࡪࡵࡷ࠾ࠥ࠭઒") + str(e))
    return bstack1l1l11ll11_opy_
def bstack1l11l1l11l_opy_():
  global bstack1lll1l1l1_opy_
  global bstack11l1l1l1l1_opy_
  global bstack1ll1l1l11_opy_
  global bstack11ll11l11l_opy_
  global bstack11ll1l1111_opy_
  global bstack1l1l1l11ll_opy_
  global CONFIG
  bstack1ll1ll1ll1_opy_ = os.environ.get(bstack11ll1l_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭ઓ"))
  if bstack1ll1ll1ll1_opy_ in [bstack11ll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬઔ"), bstack11ll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ક")]:
    bstack1111lllll_opy_()
  percy.shutdown()
  if bstack1lll1l1l1_opy_:
    logger.warning(bstack11llll1l11_opy_.format(str(bstack1lll1l1l1_opy_)))
  else:
    try:
      bstack1ll1llll1_opy_ = bstack1llll1llll_opy_(bstack11ll1l_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧખ"), logger)
      if bstack1ll1llll1_opy_.get(bstack11ll1l_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧગ")) and bstack1ll1llll1_opy_.get(bstack11ll1l_opy_ (u"ࠪࡲࡺࡪࡧࡦࡡ࡯ࡳࡨࡧ࡬ࠨઘ")).get(bstack11ll1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡰࡤࡱࡪ࠭ઙ")):
        logger.warning(bstack11llll1l11_opy_.format(str(bstack1ll1llll1_opy_[bstack11ll1l_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪચ")][bstack11ll1l_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨછ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack11lllll1ll_opy_)
  global bstack1l111ll1ll_opy_
  if bstack1l111ll1ll_opy_:
    bstack1llll1ll1l_opy_()
  try:
    for driver in bstack11l1l1l1l1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack1ll111ll1_opy_)
  if bstack1l1l1l11ll_opy_ == bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭જ"):
    bstack11ll1l1111_opy_ = bstack11llll1111_opy_(bstack11ll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩઝ"))
  if bstack1l1l1l11ll_opy_ == bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩઞ") and len(bstack11ll11l11l_opy_) == 0:
    bstack11ll11l11l_opy_ = bstack11llll1111_opy_(bstack11ll1l_opy_ (u"ࠪࡴࡼࡥࡰࡺࡶࡨࡷࡹࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶ࠱࡮ࡸࡵ࡮ࠨટ"))
    if len(bstack11ll11l11l_opy_) == 0:
      bstack11ll11l11l_opy_ = bstack11llll1111_opy_(bstack11ll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡵࡶࡰࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪઠ"))
  bstack11ll1lll1l_opy_ = bstack11ll1l_opy_ (u"ࠬ࠭ડ")
  if len(bstack1ll1l1l11_opy_) > 0:
    bstack11ll1lll1l_opy_ = bstack1lll111lll_opy_(bstack1ll1l1l11_opy_)
  elif len(bstack11ll11l11l_opy_) > 0:
    bstack11ll1lll1l_opy_ = bstack1lll111lll_opy_(bstack11ll11l11l_opy_)
  elif len(bstack11ll1l1111_opy_) > 0:
    bstack11ll1lll1l_opy_ = bstack1lll111lll_opy_(bstack11ll1l1111_opy_)
  elif len(bstack1ll111111_opy_) > 0:
    bstack11ll1lll1l_opy_ = bstack1lll111lll_opy_(bstack1ll111111_opy_)
  if bool(bstack11ll1lll1l_opy_):
    bstack1lllll1111_opy_(bstack11ll1lll1l_opy_)
  else:
    bstack1lllll1111_opy_()
  bstack111l1l1l1_opy_(bstack11llllll1l_opy_, logger)
  bstack1l1ll1ll11_opy_.bstack1ll11l11_opy_(CONFIG)
  if len(bstack11ll1l1111_opy_) > 0:
    sys.exit(len(bstack11ll1l1111_opy_))
def bstack11ll1l111_opy_(bstack111111ll1_opy_, frame):
  global bstack11l111ll_opy_
  logger.error(bstack1l111llll_opy_)
  bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡎࡰࠩઢ"), bstack111111ll1_opy_)
  if hasattr(signal, bstack11ll1l_opy_ (u"ࠧࡔ࡫ࡪࡲࡦࡲࡳࠨણ")):
    bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨત"), signal.Signals(bstack111111ll1_opy_).name)
  else:
    bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩથ"), bstack11ll1l_opy_ (u"ࠪࡗࡎࡍࡕࡏࡍࡑࡓ࡜ࡔࠧદ"))
  bstack1ll1ll1ll1_opy_ = os.environ.get(bstack11ll1l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬધ"))
  if bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬન"):
    bstack1l1llll1_opy_.stop(bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭઩")))
  bstack1l11l1l11l_opy_()
  sys.exit(1)
def bstack11l1l1ll11_opy_(err):
  logger.critical(bstack11l1ll11ll_opy_.format(str(err)))
  bstack1lllll1111_opy_(bstack11l1ll11ll_opy_.format(str(err)), True)
  atexit.unregister(bstack1l11l1l11l_opy_)
  bstack1111lllll_opy_()
  sys.exit(1)
def bstack11llllll1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1lllll1111_opy_(message, True)
  atexit.unregister(bstack1l11l1l11l_opy_)
  bstack1111lllll_opy_()
  sys.exit(1)
def bstack1llll1l1l1_opy_():
  global CONFIG
  global bstack11ll1ll11l_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1ll1l1lll1_opy_
  CONFIG = bstack11111ll1_opy_()
  load_dotenv(CONFIG.get(bstack11ll1l_opy_ (u"ࠧࡦࡰࡹࡊ࡮ࡲࡥࠨપ")))
  bstack11ll11l111_opy_()
  bstack1llllllll1_opy_()
  CONFIG = bstack11l1l1lll1_opy_(CONFIG)
  update(CONFIG, bstack1ll1l11ll1_opy_)
  update(CONFIG, bstack11ll1ll11l_opy_)
  CONFIG = bstack11l1ll1l11_opy_(CONFIG)
  bstack1ll1l1lll1_opy_ = bstack1lllll1l1l_opy_(CONFIG)
  os.environ[bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫફ")] = bstack1ll1l1lll1_opy_.__str__()
  bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪબ"), bstack1ll1l1lll1_opy_)
  if (bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ભ") in CONFIG and bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧમ") in bstack11ll1ll11l_opy_) or (
          bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨય") in CONFIG and bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩર") not in bstack1ll1l11ll1_opy_):
    if os.getenv(bstack11ll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑ࡟ࡄࡑࡐࡆࡎࡔࡅࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ઱")):
      CONFIG[bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪલ")] = os.getenv(bstack11ll1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡡࡆࡓࡒࡈࡉࡏࡇࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉ࠭ળ"))
    else:
      bstack1llll1l11_opy_()
  elif (bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭઴") not in CONFIG and bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭વ") in CONFIG) or (
          bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨશ") in bstack1ll1l11ll1_opy_ and bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩષ") not in bstack11ll1ll11l_opy_):
    del (CONFIG[bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩસ")])
  if bstack1111l1l1_opy_(CONFIG):
    bstack11l1l1ll11_opy_(bstack1ll1l11111_opy_)
  bstack11ll1l1lll_opy_()
  bstack1l1l1l11l_opy_()
  if bstack1llll1l1ll_opy_:
    CONFIG[bstack11ll1l_opy_ (u"ࠨࡣࡳࡴࠬહ")] = bstack1ll1l1llll_opy_(CONFIG)
    logger.info(bstack1l1l111l11_opy_.format(CONFIG[bstack11ll1l_opy_ (u"ࠩࡤࡴࡵ࠭઺")]))
  if not bstack1ll1l1lll1_opy_:
    CONFIG[bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭઻")] = [{}]
def bstack11l1llllll_opy_(config, bstack1ll1l1l1ll_opy_):
  global CONFIG
  global bstack1llll1l1ll_opy_
  CONFIG = config
  bstack1llll1l1ll_opy_ = bstack1ll1l1l1ll_opy_
def bstack1l1l1l11l_opy_():
  global CONFIG
  global bstack1llll1l1ll_opy_
  if bstack11ll1l_opy_ (u"ࠫࡦࡶࡰࠨ઼") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11llllll1_opy_(e, bstack11lll1llll_opy_)
    bstack1llll1l1ll_opy_ = True
    bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫઽ"), True)
def bstack1ll1l1llll_opy_(config):
  bstack1l11lll1l1_opy_ = bstack11ll1l_opy_ (u"࠭ࠧા")
  app = config[bstack11ll1l_opy_ (u"ࠧࡢࡲࡳࠫિ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1l1111lll_opy_:
      if os.path.exists(app):
        bstack1l11lll1l1_opy_ = bstack11ll1ll1l1_opy_(config, app)
      elif bstack1l1ll1llll_opy_(app):
        bstack1l11lll1l1_opy_ = app
      else:
        bstack11l1l1ll11_opy_(bstack11l1l1l11l_opy_.format(app))
    else:
      if bstack1l1ll1llll_opy_(app):
        bstack1l11lll1l1_opy_ = app
      elif os.path.exists(app):
        bstack1l11lll1l1_opy_ = bstack11ll1ll1l1_opy_(app)
      else:
        bstack11l1l1ll11_opy_(bstack1l111lll1_opy_)
  else:
    if len(app) > 2:
      bstack11l1l1ll11_opy_(bstack1ll1l1111l_opy_)
    elif len(app) == 2:
      if bstack11ll1l_opy_ (u"ࠨࡲࡤࡸ࡭࠭ી") in app and bstack11ll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬુ") in app:
        if os.path.exists(app[bstack11ll1l_opy_ (u"ࠪࡴࡦࡺࡨࠨૂ")]):
          bstack1l11lll1l1_opy_ = bstack11ll1ll1l1_opy_(config, app[bstack11ll1l_opy_ (u"ࠫࡵࡧࡴࡩࠩૃ")], app[bstack11ll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨૄ")])
        else:
          bstack11l1l1ll11_opy_(bstack11l1l1l11l_opy_.format(app))
      else:
        bstack11l1l1ll11_opy_(bstack1ll1l1111l_opy_)
    else:
      for key in app:
        if key in bstack1l1l1l1lll_opy_:
          if key == bstack11ll1l_opy_ (u"࠭ࡰࡢࡶ࡫ࠫૅ"):
            if os.path.exists(app[key]):
              bstack1l11lll1l1_opy_ = bstack11ll1ll1l1_opy_(config, app[key])
            else:
              bstack11l1l1ll11_opy_(bstack11l1l1l11l_opy_.format(app))
          else:
            bstack1l11lll1l1_opy_ = app[key]
        else:
          bstack11l1l1ll11_opy_(bstack1l1ll1l1l1_opy_)
  return bstack1l11lll1l1_opy_
def bstack1l1ll1llll_opy_(bstack1l11lll1l1_opy_):
  import re
  bstack1ll1l111ll_opy_ = re.compile(bstack11ll1l_opy_ (u"ࡲࠣࡠ࡞ࡥ࠲ࢀࡁ࠮࡜࠳࠱࠾ࡢ࡟࠯࡞࠰ࡡ࠯ࠪࠢ૆"))
  bstack1l11l11l1_opy_ = re.compile(bstack11ll1l_opy_ (u"ࡳࠤࡡ࡟ࡦ࠳ࡺࡂ࠯࡝࠴࠲࠿࡜ࡠ࠰࡟࠱ࡢ࠰࠯࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭ࠨࠧે"))
  if bstack11ll1l_opy_ (u"ࠩࡥࡷ࠿࠵࠯ࠨૈ") in bstack1l11lll1l1_opy_ or re.fullmatch(bstack1ll1l111ll_opy_, bstack1l11lll1l1_opy_) or re.fullmatch(bstack1l11l11l1_opy_, bstack1l11lll1l1_opy_):
    return True
  else:
    return False
def bstack11ll1ll1l1_opy_(config, path, bstack11ll111l1l_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack11ll1l_opy_ (u"ࠪࡶࡧ࠭ૉ")).read()).hexdigest()
  bstack1l11ll111_opy_ = bstack11ll1ll11_opy_(md5_hash)
  bstack1l11lll1l1_opy_ = None
  if bstack1l11ll111_opy_:
    logger.info(bstack111ll1111_opy_.format(bstack1l11ll111_opy_, md5_hash))
    return bstack1l11ll111_opy_
  bstack1111111l1_opy_ = MultipartEncoder(
    fields={
      bstack11ll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࠩ૊"): (os.path.basename(path), open(os.path.abspath(path), bstack11ll1l_opy_ (u"ࠬࡸࡢࠨો")), bstack11ll1l_opy_ (u"࠭ࡴࡦࡺࡷ࠳ࡵࡲࡡࡪࡰࠪૌ")),
      bstack11ll1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟ࡪࡦ્ࠪ"): bstack11ll111l1l_opy_
    }
  )
  response = requests.post(bstack1lllll1ll1_opy_, data=bstack1111111l1_opy_,
                           headers={bstack11ll1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ૎"): bstack1111111l1_opy_.content_type},
                           auth=(config[bstack11ll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ૏")], config[bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ૐ")]))
  try:
    res = json.loads(response.text)
    bstack1l11lll1l1_opy_ = res[bstack11ll1l_opy_ (u"ࠫࡦࡶࡰࡠࡷࡵࡰࠬ૑")]
    logger.info(bstack1l1l1ll1ll_opy_.format(bstack1l11lll1l1_opy_))
    bstack1111lll11_opy_(md5_hash, bstack1l11lll1l1_opy_)
  except ValueError as err:
    bstack11l1l1ll11_opy_(bstack11llll1l1_opy_.format(str(err)))
  return bstack1l11lll1l1_opy_
def bstack11ll1l1lll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack1ll1ll111_opy_
  bstack1l111l111_opy_ = 1
  bstack1ll11l1ll_opy_ = 1
  if bstack11ll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ૒") in CONFIG:
    bstack1ll11l1ll_opy_ = CONFIG[bstack11ll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭૓")]
  else:
    bstack1ll11l1ll_opy_ = bstack11ll1ll1ll_opy_(framework_name, args) or 1
  if bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૔") in CONFIG:
    bstack1l111l111_opy_ = len(CONFIG[bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ૕")])
  bstack1ll1ll111_opy_ = int(bstack1ll11l1ll_opy_) * int(bstack1l111l111_opy_)
def bstack11ll1ll1ll_opy_(framework_name, args):
  if framework_name == bstack1l1l1ll11l_opy_ and args and bstack11ll1l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ૖") in args:
      bstack1ll1l11l1_opy_ = args.index(bstack11ll1l_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ૗"))
      return int(args[bstack1ll1l11l1_opy_ + 1]) or 1
  return 1
def bstack11ll1ll11_opy_(md5_hash):
  bstack1ll11llll1_opy_ = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠫࢃ࠭૘")), bstack11ll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ૙"), bstack11ll1l_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ૚"))
  if os.path.exists(bstack1ll11llll1_opy_):
    bstack1ll1111lll_opy_ = json.load(open(bstack1ll11llll1_opy_, bstack11ll1l_opy_ (u"ࠧࡳࡤࠪ૛")))
    if md5_hash in bstack1ll1111lll_opy_:
      bstack1l11l1lll_opy_ = bstack1ll1111lll_opy_[md5_hash]
      bstack1lll1l11l1_opy_ = datetime.datetime.now()
      bstack11111l1ll_opy_ = datetime.datetime.strptime(bstack1l11l1lll_opy_[bstack11ll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ૜")], bstack11ll1l_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭૝"))
      if (bstack1lll1l11l1_opy_ - bstack11111l1ll_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l11l1lll_opy_[bstack11ll1l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ૞")]):
        return None
      return bstack1l11l1lll_opy_[bstack11ll1l_opy_ (u"ࠫ࡮ࡪࠧ૟")]
  else:
    return None
def bstack1111lll11_opy_(md5_hash, bstack1l11lll1l1_opy_):
  bstack11l1l1lll_opy_ = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠬࢄࠧૠ")), bstack11ll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ૡ"))
  if not os.path.exists(bstack11l1l1lll_opy_):
    os.makedirs(bstack11l1l1lll_opy_)
  bstack1ll11llll1_opy_ = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠧࡿࠩૢ")), bstack11ll1l_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨૣ"), bstack11ll1l_opy_ (u"ࠩࡤࡴࡵ࡛ࡰ࡭ࡱࡤࡨࡒࡊ࠵ࡉࡣࡶ࡬࠳ࡰࡳࡰࡰࠪ૤"))
  bstack1lll111ll1_opy_ = {
    bstack11ll1l_opy_ (u"ࠪ࡭ࡩ࠭૥"): bstack1l11lll1l1_opy_,
    bstack11ll1l_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ૦"): datetime.datetime.strftime(datetime.datetime.now(), bstack11ll1l_opy_ (u"ࠬࠫࡤ࠰ࠧࡰ࠳ࠪ࡟ࠠࠦࡊ࠽ࠩࡒࡀࠥࡔࠩ૧")),
    bstack11ll1l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ૨"): str(__version__)
  }
  if os.path.exists(bstack1ll11llll1_opy_):
    bstack1ll1111lll_opy_ = json.load(open(bstack1ll11llll1_opy_, bstack11ll1l_opy_ (u"ࠧࡳࡤࠪ૩")))
  else:
    bstack1ll1111lll_opy_ = {}
  bstack1ll1111lll_opy_[md5_hash] = bstack1lll111ll1_opy_
  with open(bstack1ll11llll1_opy_, bstack11ll1l_opy_ (u"ࠣࡹ࠮ࠦ૪")) as outfile:
    json.dump(bstack1ll1111lll_opy_, outfile)
def bstack1l111l111l_opy_(self):
  return
def bstack1l1lll111_opy_(self):
  return
def bstack11l1lll11_opy_(self):
  global bstack11l1llll1l_opy_
  bstack11l1llll1l_opy_(self)
def bstack1l1l111l1l_opy_():
  global bstack1l1ll11lll_opy_
  bstack1l1ll11lll_opy_ = True
def bstack1ll1ll1ll_opy_(self):
  global bstack11l11l11l_opy_
  global bstack1llll1l11l_opy_
  global bstack11111111l_opy_
  try:
    if bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ૫") in bstack11l11l11l_opy_ and self.session_id != None and bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧ૬"), bstack11ll1l_opy_ (u"ࠫࠬ૭")) != bstack11ll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭૮"):
      bstack1lll1ll11_opy_ = bstack11ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭૯") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ૰")
      if bstack1lll1ll11_opy_ == bstack11ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ૱"):
        bstack111ll1l1l_opy_(logger)
      if self != None:
        bstack1ll1lll111_opy_(self, bstack1lll1ll11_opy_, bstack11ll1l_opy_ (u"ࠩ࠯ࠤࠬ૲").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack11ll1l_opy_ (u"ࠪࠫ૳")
    if bstack11ll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ૴") in bstack11l11l11l_opy_ and getattr(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ૵"), None):
      bstack11l1l111_opy_.bstack111l11l1_opy_(self, bstack1l1111ll11_opy_, logger, wait=True)
    if bstack11ll1l_opy_ (u"࠭ࡢࡦࡪࡤࡺࡪ࠭૶") in bstack11l11l11l_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1ll1lll111_opy_(self, bstack11ll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ૷"))
      bstack1l1111l1l1_opy_.bstack1l1l11lll1_opy_(self)
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤ૸") + str(e))
  bstack11111111l_opy_(self)
  self.session_id = None
def bstack11llll111_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack11lllll11_opy_
    global bstack11l11l11l_opy_
    command_executor = kwargs.get(bstack11ll1l_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶࠬૹ"), bstack11ll1l_opy_ (u"ࠪࠫૺ"))
    bstack11l1l1ll1l_opy_ = False
    if type(command_executor) == str and bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧૻ") in command_executor:
      bstack11l1l1ll1l_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨૼ") in str(getattr(command_executor, bstack11ll1l_opy_ (u"࠭࡟ࡶࡴ࡯ࠫ૽"), bstack11ll1l_opy_ (u"ࠧࠨ૾"))):
      bstack11l1l1ll1l_opy_ = True
    else:
      return bstack11llllllll_opy_(self, *args, **kwargs)
    if bstack11l1l1ll1l_opy_:
      if kwargs.get(bstack11ll1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ૿")):
        kwargs[bstack11ll1l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ଀")] = bstack11lllll11_opy_(kwargs[bstack11ll1l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫଁ")], bstack11l11l11l_opy_)
      elif kwargs.get(bstack11ll1l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫଂ")):
        kwargs[bstack11ll1l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬଃ")] = bstack11lllll11_opy_(kwargs[bstack11ll1l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭଄")], bstack11l11l11l_opy_)
  except Exception as e:
    logger.error(bstack11ll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡕࡇࡏࠥࡩࡡࡱࡵ࠽ࠤࢀࢃࠢଅ").format(str(e)))
  return bstack11llllllll_opy_(self, *args, **kwargs)
def bstack111111l1_opy_(self, command_executor=bstack11ll1l_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰࠳࠵࠻࠳࠶࠮࠱࠰࠴࠾࠹࠺࠴࠵ࠤଆ"), *args, **kwargs):
  bstack1l1lll11l_opy_ = bstack11llll111_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1lll11ll_opy_.on():
    return bstack1l1lll11l_opy_
  try:
    logger.debug(bstack11ll1l_opy_ (u"ࠩࡆࡳࡲࡳࡡ࡯ࡦࠣࡉࡽ࡫ࡣࡶࡶࡲࡶࠥࡽࡨࡦࡰࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡩࡴࠢࡩࡥࡱࡹࡥࠡ࠯ࠣࡿࢂ࠭ଇ").format(str(command_executor)))
    logger.debug(bstack11ll1l_opy_ (u"ࠪࡌࡺࡨࠠࡖࡔࡏࠤ࡮ࡹࠠ࠮ࠢࡾࢁࠬଈ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧଉ") in command_executor._url:
      bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭ଊ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩଋ") in command_executor):
    bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࠨଌ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1llll1_opy_.bstack1ll1l1l11l_opy_(self)
  return bstack1l1lll11l_opy_
def bstack1ll1ll11ll_opy_(args):
  return bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩ଍") in str(args)
def bstack1l1lll1lll_opy_(self, driver_command, *args, **kwargs):
  global bstack11l1l11l11_opy_
  global bstack11ll111lll_opy_
  bstack1lll11ll1l_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠩ࡬ࡷࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭଎"), None) and bstack1ll11111_opy_(
          threading.current_thread(), bstack11ll1l_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩଏ"), None)
  bstack11l11l1l1_opy_ = getattr(self, bstack11ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫଐ"), None) != None and getattr(self, bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬ଑"), None) == True
  if not bstack11ll111lll_opy_ and bstack1ll1l1lll1_opy_ and bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭଒") in CONFIG and CONFIG[bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧଓ")] == True and bstack11ll1ll1l_opy_.bstack1l11l1lll1_opy_(driver_command) and (bstack11l11l1l1_opy_ or bstack1lll11ll1l_opy_) and not bstack1ll1ll11ll_opy_(args):
    try:
      bstack11ll111lll_opy_ = True
      logger.debug(bstack11ll1l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡼࡿࠪଔ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack11ll1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡶࡥࡳࡨࡲࡶࡲࠦࡳࡤࡣࡱࠤࢀࢃࠧକ").format(str(err)))
    bstack11ll111lll_opy_ = False
  response = bstack11l1l11l11_opy_(self, driver_command, *args, **kwargs)
  if (bstack11ll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩଖ") in str(bstack11l11l11l_opy_).lower() or bstack11ll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫଗ") in str(bstack11l11l11l_opy_).lower()) and bstack1lll11ll_opy_.on():
    try:
      if driver_command == bstack11ll1l_opy_ (u"ࠬࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠩଘ"):
        bstack1l1llll1_opy_.bstack1l11ll11ll_opy_({
            bstack11ll1l_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬଙ"): response[bstack11ll1l_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ଚ")],
            bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨଛ"): bstack1l1llll1_opy_.current_test_uuid() if bstack1l1llll1_opy_.current_test_uuid() else bstack1lll11ll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack1lllllll1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack1llll1l11l_opy_
  global bstack1l1lllll1_opy_
  global bstack1111l1ll1_opy_
  global bstack1l1l1l1l1l_opy_
  global bstack11l1ll1l1l_opy_
  global bstack11l11l11l_opy_
  global bstack11llllllll_opy_
  global bstack11l1l1l1l1_opy_
  global bstack111llll11_opy_
  global bstack1l1111ll11_opy_
  CONFIG[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫଜ")] = str(bstack11l11l11l_opy_) + str(__version__)
  command_executor = bstack1llll111l_opy_()
  logger.debug(bstack1l11ll11l1_opy_.format(command_executor))
  proxy = bstack11ll11l1l1_opy_(CONFIG, proxy)
  bstack111llll1l_opy_ = 0 if bstack1l1lllll1_opy_ < 0 else bstack1l1lllll1_opy_
  try:
    if bstack1l1l1l1l1l_opy_ is True:
      bstack111llll1l_opy_ = int(multiprocessing.current_process().name)
    elif bstack11l1ll1l1l_opy_ is True:
      bstack111llll1l_opy_ = int(threading.current_thread().name)
  except:
    bstack111llll1l_opy_ = 0
  bstack1ll11l1lll_opy_ = bstack11ll11ll1l_opy_(CONFIG, bstack111llll1l_opy_)
  logger.debug(bstack11lll11l1_opy_.format(str(bstack1ll11l1lll_opy_)))
  if bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧଝ") in CONFIG and bstack1l11lll111_opy_(CONFIG[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨଞ")]):
    bstack1l1lll1l1_opy_(bstack1ll11l1lll_opy_)
  if bstack111lll1l_opy_.bstack1lll1lllll_opy_(CONFIG, bstack111llll1l_opy_) and bstack111lll1l_opy_.bstack1l11ll11l_opy_(bstack1ll11l1lll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack111lll1l_opy_.set_capabilities(bstack1ll11l1lll_opy_, CONFIG)
  if desired_capabilities:
    bstack11l1l1l11_opy_ = bstack11l1l1lll1_opy_(desired_capabilities)
    bstack11l1l1l11_opy_[bstack11ll1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬଟ")] = bstack1l1111l11_opy_(CONFIG)
    bstack11l1l1l111_opy_ = bstack11ll11ll1l_opy_(bstack11l1l1l11_opy_)
    if bstack11l1l1l111_opy_:
      bstack1ll11l1lll_opy_ = update(bstack11l1l1l111_opy_, bstack1ll11l1lll_opy_)
    desired_capabilities = None
  if options:
    bstack1l111111l1_opy_(options, bstack1ll11l1lll_opy_)
  if not options:
    options = bstack1l111ll111_opy_(bstack1ll11l1lll_opy_)
  bstack1l1111ll11_opy_ = CONFIG.get(bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଠ"))[bstack111llll1l_opy_]
  if proxy and bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧଡ")):
    options.proxy(proxy)
  if options and bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧଢ")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack11l111lll_opy_() < version.parse(bstack11ll1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨଣ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack1ll11l1lll_opy_)
  logger.info(bstack11lll11ll_opy_)
  if bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠪ࠸࠳࠷࠰࠯࠲ࠪତ")):
    bstack11llllllll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠫ࠸࠴࠸࠯࠲ࠪଥ")):
    bstack11llllllll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠬ࠸࠮࠶࠵࠱࠴ࠬଦ")):
    bstack11llllllll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11llllllll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1lllll1ll_opy_ = bstack11ll1l_opy_ (u"࠭ࠧଧ")
    if bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠧ࠵࠰࠳࠲࠵ࡨ࠱ࠨନ")):
      bstack1lllll1ll_opy_ = self.caps.get(bstack11ll1l_opy_ (u"ࠣࡱࡳࡸ࡮ࡳࡡ࡭ࡊࡸࡦ࡚ࡸ࡬ࠣ଩"))
    else:
      bstack1lllll1ll_opy_ = self.capabilities.get(bstack11ll1l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤପ"))
    if bstack1lllll1ll_opy_:
      bstack1ll1ll1111_opy_(bstack1lllll1ll_opy_)
      if bstack11l111lll_opy_() <= version.parse(bstack11ll1l_opy_ (u"ࠪ࠷࠳࠷࠳࠯࠲ࠪଫ")):
        self.command_executor._url = bstack11ll1l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧବ") + bstack1l1ll1l1ll_opy_ + bstack11ll1l_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤଭ")
      else:
        self.command_executor._url = bstack11ll1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣମ") + bstack1lllll1ll_opy_ + bstack11ll1l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣଯ")
      logger.debug(bstack1l1lll111l_opy_.format(bstack1lllll1ll_opy_))
    else:
      logger.debug(bstack11lll111l1_opy_.format(bstack11ll1l_opy_ (u"ࠣࡑࡳࡸ࡮ࡳࡡ࡭ࠢࡋࡹࡧࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤର")))
  except Exception as e:
    logger.debug(bstack11lll111l1_opy_.format(e))
  if bstack11ll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ଱") in bstack11l11l11l_opy_:
    bstack1ll11111l1_opy_(bstack1l1lllll1_opy_, bstack111llll11_opy_)
  bstack1llll1l11l_opy_ = self.session_id
  if bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪଲ") in bstack11l11l11l_opy_ or bstack11ll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫଳ") in bstack11l11l11l_opy_ or bstack11ll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ଴") in bstack11l11l11l_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l1llll1_opy_.bstack1ll1l1l11l_opy_(self)
  bstack11l1l1l1l1_opy_.append(self)
  if bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩଵ") in CONFIG and bstack11ll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬଶ") in CONFIG[bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫଷ")][bstack111llll1l_opy_]:
    bstack1111l1ll1_opy_ = CONFIG[bstack11ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬସ")][bstack111llll1l_opy_][bstack11ll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨହ")]
  logger.debug(bstack1l1llll1l_opy_.format(bstack1llll1l11l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll1ll11l_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack11ll11111l_opy_
      if(bstack11ll1l_opy_ (u"ࠦ࡮ࡴࡤࡦࡺ࠱࡮ࡸࠨ଺") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠬࢄࠧ଻")), bstack11ll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ଼࠭"), bstack11ll1l_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩଽ")), bstack11ll1l_opy_ (u"ࠨࡹࠪା")) as fp:
          fp.write(bstack11ll1l_opy_ (u"ࠤࠥି"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack11ll1l_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧୀ")))):
          with open(args[1], bstack11ll1l_opy_ (u"ࠫࡷ࠭ୁ")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack11ll1l_opy_ (u"ࠬࡧࡳࡺࡰࡦࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦ࡟࡯ࡧࡺࡔࡦ࡭ࡥࠩࡥࡲࡲࡹ࡫ࡸࡵ࠮ࠣࡴࡦ࡭ࡥࠡ࠿ࠣࡺࡴ࡯ࡤࠡ࠲ࠬࠫୂ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack1lllll1l11_opy_)
            lines.insert(1, bstack11lll11l11_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack11ll1l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣୃ")), bstack11ll1l_opy_ (u"ࠧࡸࠩୄ")) as bstack11l1l11lll_opy_:
              bstack11l1l11lll_opy_.writelines(lines)
        CONFIG[bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ୅")] = str(bstack11l11l11l_opy_) + str(__version__)
        bstack111llll1l_opy_ = 0 if bstack1l1lllll1_opy_ < 0 else bstack1l1lllll1_opy_
        try:
          if bstack1l1l1l1l1l_opy_ is True:
            bstack111llll1l_opy_ = int(multiprocessing.current_process().name)
          elif bstack11l1ll1l1l_opy_ is True:
            bstack111llll1l_opy_ = int(threading.current_thread().name)
        except:
          bstack111llll1l_opy_ = 0
        CONFIG[bstack11ll1l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤ୆")] = False
        CONFIG[bstack11ll1l_opy_ (u"ࠥ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤେ")] = True
        bstack1ll11l1lll_opy_ = bstack11ll11ll1l_opy_(CONFIG, bstack111llll1l_opy_)
        logger.debug(bstack11lll11l1_opy_.format(str(bstack1ll11l1lll_opy_)))
        if CONFIG.get(bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨୈ")):
          bstack1l1lll1l1_opy_(bstack1ll11l1lll_opy_)
        if bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ୉") in CONFIG and bstack11ll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ୊") in CONFIG[bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪୋ")][bstack111llll1l_opy_]:
          bstack1111l1ll1_opy_ = CONFIG[bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫୌ")][bstack111llll1l_opy_][bstack11ll1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫୍ࠧ")]
        args.append(os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠪࢂࠬ୎")), bstack11ll1l_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ୏"), bstack11ll1l_opy_ (u"ࠬ࠴ࡳࡦࡵࡶ࡭ࡴࡴࡩࡥࡵ࠱ࡸࡽࡺࠧ୐")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack1ll11l1lll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack11ll1l_opy_ (u"ࠨࡩ࡯ࡦࡨࡼࡤࡨࡳࡵࡣࡦ࡯࠳ࡰࡳࠣ୑"))
      bstack11ll11111l_opy_ = True
      return bstack1lll1l1111_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1111ll111_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack1l1lllll1_opy_
    global bstack1111l1ll1_opy_
    global bstack1l1l1l1l1l_opy_
    global bstack11l1ll1l1l_opy_
    global bstack11l11l11l_opy_
    CONFIG[bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩ୒")] = str(bstack11l11l11l_opy_) + str(__version__)
    bstack111llll1l_opy_ = 0 if bstack1l1lllll1_opy_ < 0 else bstack1l1lllll1_opy_
    try:
      if bstack1l1l1l1l1l_opy_ is True:
        bstack111llll1l_opy_ = int(multiprocessing.current_process().name)
      elif bstack11l1ll1l1l_opy_ is True:
        bstack111llll1l_opy_ = int(threading.current_thread().name)
    except:
      bstack111llll1l_opy_ = 0
    CONFIG[bstack11ll1l_opy_ (u"ࠣ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢ୓")] = True
    bstack1ll11l1lll_opy_ = bstack11ll11ll1l_opy_(CONFIG, bstack111llll1l_opy_)
    logger.debug(bstack11lll11l1_opy_.format(str(bstack1ll11l1lll_opy_)))
    if CONFIG.get(bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭୔")):
      bstack1l1lll1l1_opy_(bstack1ll11l1lll_opy_)
    if bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭୕") in CONFIG and bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩୖ") in CONFIG[bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨୗ")][bstack111llll1l_opy_]:
      bstack1111l1ll1_opy_ = CONFIG[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ୘")][bstack111llll1l_opy_][bstack11ll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ୙")]
    import urllib
    import json
    bstack11lll11lll_opy_ = bstack11ll1l_opy_ (u"ࠨࡹࡶࡷ࠿࠵࠯ࡤࡦࡳ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࡃࡨࡧࡰࡴ࠿ࠪ୚") + urllib.parse.quote(json.dumps(bstack1ll11l1lll_opy_))
    browser = self.connect(bstack11lll11lll_opy_)
    return browser
except Exception as e:
    pass
def bstack1lllll1lll_opy_():
    global bstack11ll11111l_opy_
    global bstack11l11l11l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11l1l1l1_opy_
        if not bstack1ll1l1lll1_opy_:
          global bstack1l1l1111l1_opy_
          if not bstack1l1l1111l1_opy_:
            from bstack_utils.helper import bstack11llll1l1l_opy_, bstack1llll11lll_opy_
            bstack1l1l1111l1_opy_ = bstack11llll1l1l_opy_()
            bstack1llll11lll_opy_(bstack11l11l11l_opy_)
          BrowserType.connect = bstack1l11l1l1l1_opy_
          return
        BrowserType.launch = bstack1111ll111_opy_
        bstack11ll11111l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll1ll11l_opy_
      bstack11ll11111l_opy_ = True
    except Exception as e:
      pass
def bstack1ll1l1ll11_opy_(context, bstack1ll11l111_opy_):
  try:
    context.page.evaluate(bstack11ll1l_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥ୛"), bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧଡ଼")+ json.dumps(bstack1ll11l111_opy_) + bstack11ll1l_opy_ (u"ࠦࢂࢃࠢଢ଼"))
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥ୞"), e)
def bstack11ll1111l_opy_(context, message, level):
  try:
    context.page.evaluate(bstack11ll1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢୟ"), bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬୠ") + json.dumps(message) + bstack11ll1l_opy_ (u"ࠨ࠮ࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠫୡ") + json.dumps(level) + bstack11ll1l_opy_ (u"ࠩࢀࢁࠬୢ"))
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡡ࡯ࡰࡲࡸࡦࡺࡩࡰࡰࠣࡿࢂࠨୣ"), e)
def bstack1l1l11l111_opy_(self, url):
  global bstack1l1llllll1_opy_
  try:
    bstack1lll1l1l1l_opy_(url)
  except Exception as err:
    logger.debug(bstack1l1llll11_opy_.format(str(err)))
  try:
    bstack1l1llllll1_opy_(self, url)
  except Exception as e:
    try:
      bstack1111l111_opy_ = str(e)
      if any(err_msg in bstack1111l111_opy_ for err_msg in bstack1111111l_opy_):
        bstack1lll1l1l1l_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1l1llll11_opy_.format(str(err)))
    raise e
def bstack11l1l111l_opy_(self):
  global bstack11lll11111_opy_
  bstack11lll11111_opy_ = self
  return
def bstack1ll11l1l11_opy_(self):
  global bstack1l1ll1ll1l_opy_
  bstack1l1ll1ll1l_opy_ = self
  return
def bstack1l11ll1lll_opy_(test_name, bstack1lll1lll1_opy_):
  global CONFIG
  if percy.bstack1l111ll11_opy_() == bstack11ll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤ୤"):
    bstack11ll1llll_opy_ = os.path.relpath(bstack1lll1lll1_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack11ll1llll_opy_)
    bstack11llll111l_opy_ = suite_name + bstack11ll1l_opy_ (u"ࠧ࠳ࠢ୥") + test_name
    threading.current_thread().percySessionName = bstack11llll111l_opy_
def bstack1l111l1111_opy_(self, test, *args, **kwargs):
  global bstack11111l11_opy_
  test_name = None
  bstack1lll1lll1_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1lll1lll1_opy_ = str(test.source)
  bstack1l11ll1lll_opy_(test_name, bstack1lll1lll1_opy_)
  bstack11111l11_opy_(self, test, *args, **kwargs)
def bstack111l111ll_opy_(driver, bstack11llll111l_opy_):
  if not bstack11llll11ll_opy_ and bstack11llll111l_opy_:
      bstack1lll1111l_opy_ = {
          bstack11ll1l_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭୦"): bstack11ll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ୧"),
          bstack11ll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ୨"): {
              bstack11ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ୩"): bstack11llll111l_opy_
          }
      }
      bstack11l1l11ll1_opy_ = bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠨ୪").format(json.dumps(bstack1lll1111l_opy_))
      driver.execute_script(bstack11l1l11ll1_opy_)
  if bstack11l1lll1l_opy_:
      bstack111l1l11l_opy_ = {
          bstack11ll1l_opy_ (u"ࠫࡦࡩࡴࡪࡱࡱࠫ୫"): bstack11ll1l_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧ୬"),
          bstack11ll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ୭"): {
              bstack11ll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬ୮"): bstack11llll111l_opy_ + bstack11ll1l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪ୯"),
              bstack11ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ୰"): bstack11ll1l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨୱ")
          }
      }
      if bstack11l1lll1l_opy_.status == bstack11ll1l_opy_ (u"ࠫࡕࡇࡓࡔࠩ୲"):
          bstack1l11lll1ll_opy_ = bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ୳").format(json.dumps(bstack111l1l11l_opy_))
          driver.execute_script(bstack1l11lll1ll_opy_)
          bstack1ll1lll111_opy_(driver, bstack11ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭୴"))
      elif bstack11l1lll1l_opy_.status == bstack11ll1l_opy_ (u"ࠧࡇࡃࡌࡐࠬ୵"):
          reason = bstack11ll1l_opy_ (u"ࠣࠤ୶")
          bstack1l1l1l11l1_opy_ = bstack11llll111l_opy_ + bstack11ll1l_opy_ (u"ࠩࠣࡪࡦ࡯࡬ࡦࡦࠪ୷")
          if bstack11l1lll1l_opy_.message:
              reason = str(bstack11l1lll1l_opy_.message)
              bstack1l1l1l11l1_opy_ = bstack1l1l1l11l1_opy_ + bstack11ll1l_opy_ (u"ࠪࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࠪ୸") + reason
          bstack111l1l11l_opy_[bstack11ll1l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ୹")] = {
              bstack11ll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ୺"): bstack11ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ୻"),
              bstack11ll1l_opy_ (u"ࠧࡥࡣࡷࡥࠬ୼"): bstack1l1l1l11l1_opy_
          }
          bstack1l11lll1ll_opy_ = bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭୽").format(json.dumps(bstack111l1l11l_opy_))
          driver.execute_script(bstack1l11lll1ll_opy_)
          bstack1ll1lll111_opy_(driver, bstack11ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ୾"), reason)
          bstack1llll11l1l_opy_(reason, str(bstack11l1lll1l_opy_), str(bstack1l1lllll1_opy_), logger)
def bstack1l1ll11l11_opy_(driver, test):
  if percy.bstack1l111ll11_opy_() == bstack11ll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣ୿") and percy.bstack11ll1lllll_opy_() == bstack11ll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ஀"):
      bstack1l11l1ll1_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ஁"), None)
      bstack1llll1lll1_opy_(driver, bstack1l11l1ll1_opy_, test)
  if bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪஂ"), None) and bstack1ll11111_opy_(
          threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ஃ"), None):
      logger.info(bstack11ll1l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠦࡐࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡ࡫ࡶࠤࡺࡴࡤࡦࡴࡺࡥࡾ࠴ࠠࠣ஄"))
      bstack111lll1l_opy_.bstack11l11ll1_opy_(driver, name=test.name, path=test.source)
def bstack11l1llll1_opy_(test, bstack11llll111l_opy_):
    try:
      data = {}
      if test:
        data[bstack11ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧஅ")] = bstack11llll111l_opy_
      if bstack11l1lll1l_opy_:
        if bstack11l1lll1l_opy_.status == bstack11ll1l_opy_ (u"ࠪࡔࡆ࡙ࡓࠨஆ"):
          data[bstack11ll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫஇ")] = bstack11ll1l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬஈ")
        elif bstack11l1lll1l_opy_.status == bstack11ll1l_opy_ (u"࠭ࡆࡂࡋࡏࠫஉ"):
          data[bstack11ll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧஊ")] = bstack11ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ஋")
          if bstack11l1lll1l_opy_.message:
            data[bstack11ll1l_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩ஌")] = str(bstack11l1lll1l_opy_.message)
      user = CONFIG[bstack11ll1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ஍")]
      key = CONFIG[bstack11ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧஎ")]
      url = bstack11ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡻࡾ࠼ࡾࢁࡅࡧࡰࡪ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡵࡵࡱࡰࡥࡹ࡫࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠱ࡾࢁ࠳ࡰࡳࡰࡰࠪஏ").format(user, key, bstack1llll1l11l_opy_)
      headers = {
        bstack11ll1l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡵࡻࡳࡩࠬஐ"): bstack11ll1l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ஑"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack11l1ll1ll1_opy_.format(str(e)))
def bstack1lllll11ll_opy_(test, bstack11llll111l_opy_):
  global CONFIG
  global bstack1l1ll1ll1l_opy_
  global bstack11lll11111_opy_
  global bstack1llll1l11l_opy_
  global bstack11l1lll1l_opy_
  global bstack1111l1ll1_opy_
  global bstack1llll1ll11_opy_
  global bstack1ll11lll1_opy_
  global bstack1lll1l11ll_opy_
  global bstack1l1ll11ll_opy_
  global bstack11l1l1l1l1_opy_
  global bstack1l1111ll11_opy_
  try:
    if not bstack1llll1l11l_opy_:
      with open(os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠨࢀࠪஒ")), bstack11ll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩஓ"), bstack11ll1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬஔ"))) as f:
        bstack11l11llll_opy_ = json.loads(bstack11ll1l_opy_ (u"ࠦࢀࠨக") + f.read().strip() + bstack11ll1l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ஖") + bstack11ll1l_opy_ (u"ࠨࡽࠣ஗"))
        bstack1llll1l11l_opy_ = bstack11l11llll_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11l1l1l1l1_opy_:
    for driver in bstack11l1l1l1l1_opy_:
      if bstack1llll1l11l_opy_ == driver.session_id:
        if test:
          bstack1l1ll11l11_opy_(driver, test)
        bstack111l111ll_opy_(driver, bstack11llll111l_opy_)
  elif bstack1llll1l11l_opy_:
    bstack11l1llll1_opy_(test, bstack11llll111l_opy_)
  if bstack1l1ll1ll1l_opy_:
    bstack1ll11lll1_opy_(bstack1l1ll1ll1l_opy_)
  if bstack11lll11111_opy_:
    bstack1lll1l11ll_opy_(bstack11lll11111_opy_)
  if bstack1l1ll11lll_opy_:
    bstack1l1ll11ll_opy_()
def bstack1lllll1l1_opy_(self, test, *args, **kwargs):
  bstack11llll111l_opy_ = None
  if test:
    bstack11llll111l_opy_ = str(test.name)
  bstack1lllll11ll_opy_(test, bstack11llll111l_opy_)
  bstack1llll1ll11_opy_(self, test, *args, **kwargs)
def bstack11ll11lll_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1111l1l1l_opy_
  global CONFIG
  global bstack11l1l1l1l1_opy_
  global bstack1llll1l11l_opy_
  bstack1lll11lll_opy_ = None
  try:
    if bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭஘"), None):
      try:
        if not bstack1llll1l11l_opy_:
          with open(os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠨࢀࠪங")), bstack11ll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩச"), bstack11ll1l_opy_ (u"ࠪ࠲ࡸ࡫ࡳࡴ࡫ࡲࡲ࡮ࡪࡳ࠯ࡶࡻࡸࠬ஛"))) as f:
            bstack11l11llll_opy_ = json.loads(bstack11ll1l_opy_ (u"ࠦࢀࠨஜ") + f.read().strip() + bstack11ll1l_opy_ (u"ࠬࠨࡸࠣ࠼ࠣࠦࡾࠨࠧ஝") + bstack11ll1l_opy_ (u"ࠨࡽࠣஞ"))
            bstack1llll1l11l_opy_ = bstack11l11llll_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11l1l1l1l1_opy_:
        for driver in bstack11l1l1l1l1_opy_:
          if bstack1llll1l11l_opy_ == driver.session_id:
            bstack1lll11lll_opy_ = driver
    bstack1ll11lllll_opy_ = bstack111lll1l_opy_.bstack1ll1l1l1l_opy_(test.tags)
    if bstack1lll11lll_opy_:
      threading.current_thread().isA11yTest = bstack111lll1l_opy_.bstack1l11111lll_opy_(bstack1lll11lll_opy_, bstack1ll11lllll_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1ll11lllll_opy_
  except:
    pass
  bstack1111l1l1l_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack11l1lll1l_opy_
  bstack11l1lll1l_opy_ = self._test
def bstack1l1lll1ll1_opy_():
  global bstack1l11ll1ll1_opy_
  try:
    if os.path.exists(bstack1l11ll1ll1_opy_):
      os.remove(bstack1l11ll1ll1_opy_)
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡧࡩࡱ࡫ࡴࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪட") + str(e))
def bstack1lllllll11_opy_():
  global bstack1l11ll1ll1_opy_
  bstack1ll1llll1_opy_ = {}
  try:
    if not os.path.isfile(bstack1l11ll1ll1_opy_):
      with open(bstack1l11ll1ll1_opy_, bstack11ll1l_opy_ (u"ࠨࡹࠪ஠")):
        pass
      with open(bstack1l11ll1ll1_opy_, bstack11ll1l_opy_ (u"ࠤࡺ࠯ࠧ஡")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l11ll1ll1_opy_):
      bstack1ll1llll1_opy_ = json.load(open(bstack1l11ll1ll1_opy_, bstack11ll1l_opy_ (u"ࠪࡶࡧ࠭஢")))
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡲࡦࡣࡧ࡭ࡳ࡭ࠠࡳࡱࡥࡳࡹࠦࡲࡦࡲࡲࡶࡹࠦࡦࡪ࡮ࡨ࠾ࠥ࠭ண") + str(e))
  finally:
    return bstack1ll1llll1_opy_
def bstack1ll11111l1_opy_(platform_index, item_index):
  global bstack1l11ll1ll1_opy_
  try:
    bstack1ll1llll1_opy_ = bstack1lllllll11_opy_()
    bstack1ll1llll1_opy_[item_index] = platform_index
    with open(bstack1l11ll1ll1_opy_, bstack11ll1l_opy_ (u"ࠧࡽࠫࠣத")) as outfile:
      json.dump(bstack1ll1llll1_opy_, outfile)
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡹࡵ࡭ࡹ࡯࡮ࡨࠢࡷࡳࠥࡸ࡯ࡣࡱࡷࠤࡷ࡫ࡰࡰࡴࡷࠤ࡫࡯࡬ࡦ࠼ࠣࠫ஥") + str(e))
def bstack1l111ll1l_opy_(bstack111lll11l_opy_):
  global CONFIG
  bstack1ll111ll11_opy_ = bstack11ll1l_opy_ (u"ࠧࠨ஦")
  if not bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ஧") in CONFIG:
    logger.info(bstack11ll1l_opy_ (u"ࠩࡑࡳࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠡࡲࡤࡷࡸ࡫ࡤࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡲࡦࡲࡲࡶࡹࠦࡦࡰࡴࠣࡖࡴࡨ࡯ࡵࠢࡵࡹࡳ࠭ந"))
  try:
    platform = CONFIG[bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ன")][bstack111lll11l_opy_]
    if bstack11ll1l_opy_ (u"ࠫࡴࡹࠧப") in platform:
      bstack1ll111ll11_opy_ += str(platform[bstack11ll1l_opy_ (u"ࠬࡵࡳࠨ஫")]) + bstack11ll1l_opy_ (u"࠭ࠬࠡࠩ஬")
    if bstack11ll1l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ஭") in platform:
      bstack1ll111ll11_opy_ += str(platform[bstack11ll1l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫம")]) + bstack11ll1l_opy_ (u"ࠩ࠯ࠤࠬய")
    if bstack11ll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧர") in platform:
      bstack1ll111ll11_opy_ += str(platform[bstack11ll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨற")]) + bstack11ll1l_opy_ (u"ࠬ࠲ࠠࠨல")
    if bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨள") in platform:
      bstack1ll111ll11_opy_ += str(platform[bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩழ")]) + bstack11ll1l_opy_ (u"ࠨ࠮ࠣࠫவ")
    if bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧஶ") in platform:
      bstack1ll111ll11_opy_ += str(platform[bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨஷ")]) + bstack11ll1l_opy_ (u"ࠫ࠱ࠦࠧஸ")
    if bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ஹ") in platform:
      bstack1ll111ll11_opy_ += str(platform[bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ஺")]) + bstack11ll1l_opy_ (u"ࠧ࠭ࠢࠪ஻")
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠨࡕࡲࡱࡪࠦࡥࡳࡴࡲࡶࠥ࡯࡮ࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡷ࡫ࡰࡰࡴࡷࠤ࡬࡫࡮ࡦࡴࡤࡸ࡮ࡵ࡮ࠨ஼") + str(e))
  finally:
    if bstack1ll111ll11_opy_[len(bstack1ll111ll11_opy_) - 2:] == bstack11ll1l_opy_ (u"ࠩ࠯ࠤࠬ஽"):
      bstack1ll111ll11_opy_ = bstack1ll111ll11_opy_[:-2]
    return bstack1ll111ll11_opy_
def bstack11lll1111_opy_(path, bstack1ll111ll11_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack1l1ll11l1l_opy_ = ET.parse(path)
    bstack111llllll_opy_ = bstack1l1ll11l1l_opy_.getroot()
    bstack1l11l111l1_opy_ = None
    for suite in bstack111llllll_opy_.iter(bstack11ll1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩா")):
      if bstack11ll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫி") in suite.attrib:
        suite.attrib[bstack11ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪீ")] += bstack11ll1l_opy_ (u"࠭ࠠࠨு") + bstack1ll111ll11_opy_
        bstack1l11l111l1_opy_ = suite
    bstack1lll11l11_opy_ = None
    for robot in bstack111llllll_opy_.iter(bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ூ")):
      bstack1lll11l11_opy_ = robot
    bstack1ll11ll11l_opy_ = len(bstack1lll11l11_opy_.findall(bstack11ll1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧ௃")))
    if bstack1ll11ll11l_opy_ == 1:
      bstack1lll11l11_opy_.remove(bstack1lll11l11_opy_.findall(bstack11ll1l_opy_ (u"ࠩࡶࡹ࡮ࡺࡥࠨ௄"))[0])
      bstack11lll1lll1_opy_ = ET.Element(bstack11ll1l_opy_ (u"ࠪࡷࡺ࡯ࡴࡦࠩ௅"), attrib={bstack11ll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩெ"): bstack11ll1l_opy_ (u"࡙ࠬࡵࡪࡶࡨࡷࠬே"), bstack11ll1l_opy_ (u"࠭ࡩࡥࠩை"): bstack11ll1l_opy_ (u"ࠧࡴ࠲ࠪ௉")})
      bstack1lll11l11_opy_.insert(1, bstack11lll1lll1_opy_)
      bstack1l11ll1l1l_opy_ = None
      for suite in bstack1lll11l11_opy_.iter(bstack11ll1l_opy_ (u"ࠨࡵࡸ࡭ࡹ࡫ࠧொ")):
        bstack1l11ll1l1l_opy_ = suite
      bstack1l11ll1l1l_opy_.append(bstack1l11l111l1_opy_)
      bstack1lll1llll1_opy_ = None
      for status in bstack1l11l111l1_opy_.iter(bstack11ll1l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩோ")):
        bstack1lll1llll1_opy_ = status
      bstack1l11ll1l1l_opy_.append(bstack1lll1llll1_opy_)
    bstack1l1ll11l1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡶࡡࡳࡵ࡬ࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠨௌ") + str(e))
def bstack1l11llll1l_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll1l1l111_opy_
  global CONFIG
  if bstack11ll1l_opy_ (u"ࠦࡵࡿࡴࡩࡱࡱࡴࡦࡺࡨ்ࠣ") in options:
    del options[bstack11ll1l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲࡵࡧࡴࡩࠤ௎")]
  bstack1l111lllll_opy_ = bstack1lllllll11_opy_()
  for bstack1llllll1l_opy_ in bstack1l111lllll_opy_.keys():
    path = os.path.join(os.getcwd(), bstack11ll1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࡤࡸࡥࡴࡷ࡯ࡸࡸ࠭௏"), str(bstack1llllll1l_opy_), bstack11ll1l_opy_ (u"ࠧࡰࡷࡷࡴࡺࡺ࠮ࡹ࡯࡯ࠫௐ"))
    bstack11lll1111_opy_(path, bstack1l111ll1l_opy_(bstack1l111lllll_opy_[bstack1llllll1l_opy_]))
  bstack1l1lll1ll1_opy_()
  return bstack1ll1l1l111_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack111l11l11_opy_(self, ff_profile_dir):
  global bstack11ll11llll_opy_
  if not ff_profile_dir:
    return None
  return bstack11ll11llll_opy_(self, ff_profile_dir)
def bstack111l111l1_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll1llll11_opy_
  bstack1l1llll11l_opy_ = []
  if bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ௑") in CONFIG:
    bstack1l1llll11l_opy_ = CONFIG[bstack11ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ௒")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack11ll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦ௓")],
      pabot_args[bstack11ll1l_opy_ (u"ࠦࡻ࡫ࡲࡣࡱࡶࡩࠧ௔")],
      argfile,
      pabot_args.get(bstack11ll1l_opy_ (u"ࠧ࡮ࡩࡷࡧࠥ௕")),
      pabot_args[bstack11ll1l_opy_ (u"ࠨࡰࡳࡱࡦࡩࡸࡹࡥࡴࠤ௖")],
      platform[0],
      bstack1ll1llll11_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack11ll1l_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡨ࡬ࡰࡪࡹࠢௗ")] or [(bstack11ll1l_opy_ (u"ࠣࠤ௘"), None)]
    for platform in enumerate(bstack1l1llll11l_opy_)
  ]
def bstack1ll1l1l1l1_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll11l1l1_opy_=bstack11ll1l_opy_ (u"ࠩࠪ௙")):
  global bstack1ll11lll1l_opy_
  self.platform_index = platform_index
  self.bstack1l1ll11l1_opy_ = bstack1ll11l1l1_opy_
  bstack1ll11lll1l_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l11l1l11_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1ll1l11l1l_opy_
  global bstack111ll11ll_opy_
  bstack11ll1l11ll_opy_ = copy.deepcopy(item)
  if not bstack11ll1l_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ௚") in item.options:
    bstack11ll1l11ll_opy_.options[bstack11ll1l_opy_ (u"ࠫࡻࡧࡲࡪࡣࡥࡰࡪ࠭௛")] = []
  bstack1lll1l1ll_opy_ = bstack11ll1l11ll_opy_.options[bstack11ll1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௜")].copy()
  for v in bstack11ll1l11ll_opy_.options[bstack11ll1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௝")]:
    if bstack11ll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝࠭௞") in v:
      bstack1lll1l1ll_opy_.remove(v)
    if bstack11ll1l_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ௟") in v:
      bstack1lll1l1ll_opy_.remove(v)
    if bstack11ll1l_opy_ (u"ࠩࡅࡗ࡙ࡇࡃࡌࡆࡈࡊࡑࡕࡃࡂࡎࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭௠") in v:
      bstack1lll1l1ll_opy_.remove(v)
  bstack1lll1l1ll_opy_.insert(0, bstack11ll1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙࠼ࡾࢁࠬ௡").format(bstack11ll1l11ll_opy_.platform_index))
  bstack1lll1l1ll_opy_.insert(0, bstack11ll1l_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡈࡊࡌࡌࡐࡅࡄࡐࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒ࠻ࡽࢀࠫ௢").format(bstack11ll1l11ll_opy_.bstack1l1ll11l1_opy_))
  bstack11ll1l11ll_opy_.options[bstack11ll1l_opy_ (u"ࠬࡼࡡࡳ࡫ࡤࡦࡱ࡫ࠧ௣")] = bstack1lll1l1ll_opy_
  if bstack111ll11ll_opy_:
    bstack11ll1l11ll_opy_.options[bstack11ll1l_opy_ (u"࠭ࡶࡢࡴ࡬ࡥࡧࡲࡥࠨ௤")].insert(0, bstack11ll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙࠺ࡼࡿࠪ௥").format(bstack111ll11ll_opy_))
  return bstack1ll1l11l1l_opy_(caller_id, datasources, is_last, bstack11ll1l11ll_opy_, outs_dir)
def bstack11ll1lll1_opy_(command, item_index):
  if bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡵࡨࡷࡸ࡯࡯࡯ࠩ௦")):
    os.environ[bstack11ll1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪ௧")] = json.dumps(CONFIG[bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭௨")][item_index % bstack1l1llll111_opy_])
  global bstack111ll11ll_opy_
  if bstack111ll11ll_opy_:
    command[0] = command[0].replace(bstack11ll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ௩"), bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩ௪") + str(
      item_index) + bstack11ll1l_opy_ (u"࠭ࠠࠨ௫") + bstack111ll11ll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭௬"),
                                    bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠭ࡴࡦ࡮ࠤࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠥ࠳࠭ࡣࡵࡷࡥࡨࡱ࡟ࡪࡶࡨࡱࡤ࡯࡮ࡥࡧࡻࠤࠬ௭") + str(item_index), 1)
def bstack1lll11111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11lll1lll_opy_
  bstack11ll1lll1_opy_(command, item_index)
  return bstack11lll1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack1l1l1lll1l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11lll1lll_opy_
  bstack11ll1lll1_opy_(command, item_index)
  return bstack11lll1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l1ll1ll1_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11lll1lll_opy_
  bstack11ll1lll1_opy_(command, item_index)
  return bstack11lll1lll_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1l1ll1l1l_opy_(self, runner, quiet=False, capture=True):
  global bstack1l11l11ll_opy_
  bstack1llll11111_opy_ = bstack1l11l11ll_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack11ll1l_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࡤࡧࡲࡳࠩ௮")):
      runner.exception_arr = []
    if not hasattr(runner, bstack11ll1l_opy_ (u"ࠪࡩࡽࡩ࡟ࡵࡴࡤࡧࡪࡨࡡࡤ࡭ࡢࡥࡷࡸࠧ௯")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1llll11111_opy_
def bstack1111l11l1_opy_(runner, hook_name, context, element, bstack11llllll11_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack1ll11111ll_opy_.bstack11llll11l_opy_(hook_name, element)
    bstack11llllll11_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack1ll11111ll_opy_.bstack1111llll1_opy_(element)
      if hook_name not in [bstack11ll1l_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠨ௰"), bstack11ll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨ௱")] and args and hasattr(args[0], bstack11ll1l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡤࡳࡥࡴࡵࡤ࡫ࡪ࠭௲")):
        args[0].error_message = bstack11ll1l_opy_ (u"ࠧࠨ௳")
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡭ࡧ࡮ࡥ࡮ࡨࠤ࡭ࡵ࡯࡬ࡵࠣ࡭ࡳࠦࡢࡦࡪࡤࡺࡪࡀࠠࡼࡿࠪ௴").format(str(e)))
def bstack11ll11l1l_opy_(runner, name, context, bstack11llllll11_opy_, *args):
    if runner.hooks.get(bstack11ll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ௵")).__name__ != bstack11ll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲ࡟ࡥࡧࡩࡥࡺࡲࡴࡠࡪࡲࡳࡰࠨ௶"):
      bstack1111l11l1_opy_(runner, name, context, runner, bstack11llllll11_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack111l1ll1l_opy_(bstack11ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ௷")) else context.browser
      runner.driver_initialised = bstack11ll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤ௸")
    except Exception as e:
      logger.debug(bstack11ll1l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡤࡳ࡫ࡹࡩࡷࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࠣࡥࡹࡺࡲࡪࡤࡸࡸࡪࡀࠠࡼࡿࠪ௹").format(str(e)))
def bstack1l111lll11_opy_(runner, name, context, bstack11llllll11_opy_, *args):
    bstack1111l11l1_opy_(runner, name, context, context.feature, bstack11llllll11_opy_, *args)
    try:
      if not bstack11llll11ll_opy_:
        bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1ll1l_opy_(bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭௺")) else context.browser
        if is_driver_active(bstack1lll11lll_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack11ll1l_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠤ௻")
          bstack1ll11l111_opy_ = str(runner.feature.name)
          bstack1ll1l1ll11_opy_(context, bstack1ll11l111_opy_)
          bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧ௼") + json.dumps(bstack1ll11l111_opy_) + bstack11ll1l_opy_ (u"ࠪࢁࢂ࠭௽"))
    except Exception as e:
      logger.debug(bstack11ll1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠣ࡭ࡳࠦࡢࡦࡨࡲࡶࡪࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ௾").format(str(e)))
def bstack1l11l1l1ll_opy_(runner, name, context, bstack11llllll11_opy_, *args):
    if hasattr(context, bstack11ll1l_opy_ (u"ࠬࡹࡣࡦࡰࡤࡶ࡮ࡵࠧ௿")):
        bstack1ll11111ll_opy_.start_test(context)
    target = context.scenario if hasattr(context, bstack11ll1l_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨఀ")) else context.feature
    bstack1111l11l1_opy_(runner, name, context, target, bstack11llllll11_opy_, *args)
def bstack1l1l1llll1_opy_(runner, name, context, bstack11llllll11_opy_, *args):
    if len(context.scenario.tags) == 0: bstack1ll11111ll_opy_.start_test(context)
    bstack1111l11l1_opy_(runner, name, context, context.scenario, bstack11llllll11_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1l1111l1l1_opy_.bstack11l1111ll_opy_(context, *args)
    try:
      bstack1lll11lll_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ఁ"), context.browser)
      if is_driver_active(bstack1lll11lll_opy_):
        bstack1l1llll1_opy_.bstack1ll1l1l11l_opy_(bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧం"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack11ll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠦః")
        if (not bstack11llll11ll_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll11l111_opy_ = str(runner.feature.name)
          bstack1ll11l111_opy_ = feature_name + bstack11ll1l_opy_ (u"ࠪࠤ࠲ࠦࠧఄ") + scenario_name
          if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨఅ"):
            bstack1ll1l1ll11_opy_(context, bstack1ll11l111_opy_)
            bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪఆ") + json.dumps(bstack1ll11l111_opy_) + bstack11ll1l_opy_ (u"࠭ࡽࡾࠩఇ"))
    except Exception as e:
      logger.debug(bstack11ll1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲ࠾ࠥࢁࡽࠨఈ").format(str(e)))
def bstack1l1l111lll_opy_(runner, name, context, bstack11llllll11_opy_, *args):
    bstack1111l11l1_opy_(runner, name, context, args[0], bstack11llllll11_opy_, *args)
    try:
      bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1ll1l_opy_(bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧఉ")) else context.browser
      if is_driver_active(bstack1lll11lll_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack11ll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢఊ")
        bstack1ll11111ll_opy_.bstack1llll1lll_opy_(args[0])
        if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣఋ"):
          feature_name = bstack1ll11l111_opy_ = str(runner.feature.name)
          bstack1ll11l111_opy_ = feature_name + bstack11ll1l_opy_ (u"ࠫࠥ࠳ࠠࠨఌ") + context.scenario.name
          bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪ఍") + json.dumps(bstack1ll11l111_opy_) + bstack11ll1l_opy_ (u"࠭ࡽࡾࠩఎ"))
    except Exception as e:
      logger.debug(bstack11ll1l_opy_ (u"ࠧࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠦࡩ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡸࡪࡶ࠺ࠡࡽࢀࠫఏ").format(str(e)))
def bstack1l1lll11ll_opy_(runner, name, context, bstack11llllll11_opy_, *args):
  bstack1ll11111ll_opy_.bstack1l111ll11l_opy_(args[0])
  try:
    bstack1l11llllll_opy_ = args[0].status.name
    bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧఐ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1lll11lll_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack11ll1l_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ఑")
        feature_name = bstack1ll11l111_opy_ = str(runner.feature.name)
        bstack1ll11l111_opy_ = feature_name + bstack11ll1l_opy_ (u"ࠪࠤ࠲ࠦࠧఒ") + context.scenario.name
        bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩఓ") + json.dumps(bstack1ll11l111_opy_) + bstack11ll1l_opy_ (u"ࠬࢃࡽࠨఔ"))
    if str(bstack1l11llllll_opy_).lower() == bstack11ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭క"):
      bstack11lllll111_opy_ = bstack11ll1l_opy_ (u"ࠧࠨఖ")
      bstack111111l1l_opy_ = bstack11ll1l_opy_ (u"ࠨࠩగ")
      bstack1l11l11lll_opy_ = bstack11ll1l_opy_ (u"ࠩࠪఘ")
      try:
        import traceback
        bstack11lllll111_opy_ = runner.exception.__class__.__name__
        bstack1l1l1l111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111111l1l_opy_ = bstack11ll1l_opy_ (u"ࠪࠤࠬఙ").join(bstack1l1l1l111_opy_)
        bstack1l11l11lll_opy_ = bstack1l1l1l111_opy_[-1]
      except Exception as e:
        logger.debug(bstack111ll1lll_opy_.format(str(e)))
      bstack11lllll111_opy_ += bstack1l11l11lll_opy_
      bstack11ll1111l_opy_(context, json.dumps(str(args[0].name) + bstack11ll1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥచ") + str(bstack111111l1l_opy_)),
                          bstack11ll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦఛ"))
      if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡵࡧࡳࠦజ"):
        bstack1llllll11l_opy_(getattr(context, bstack11ll1l_opy_ (u"ࠧࡱࡣࡪࡩࠬఝ"), None), bstack11ll1l_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣఞ"), bstack11lllll111_opy_)
        bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧట") + json.dumps(str(args[0].name) + bstack11ll1l_opy_ (u"ࠥࠤ࠲ࠦࡆࡢ࡫࡯ࡩࡩࠧ࡜࡯ࠤఠ") + str(bstack111111l1l_opy_)) + bstack11ll1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤࡨࡶࡷࡵࡲࠣࡿࢀࠫడ"))
      if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥఢ"):
        bstack1ll1lll111_opy_(bstack1lll11lll_opy_, bstack11ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ణ"), bstack11ll1l_opy_ (u"ࠢࡔࡥࡨࡲࡦࡸࡩࡰࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦత") + str(bstack11lllll111_opy_))
    else:
      bstack11ll1111l_opy_(context, bstack11ll1l_opy_ (u"ࠣࡒࡤࡷࡸ࡫ࡤࠢࠤథ"), bstack11ll1l_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢద"))
      if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠣధ"):
        bstack1llllll11l_opy_(getattr(context, bstack11ll1l_opy_ (u"ࠫࡵࡧࡧࡦࠩన"), None), bstack11ll1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ఩"))
      bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡩࡧࡴࡢࠤ࠽ࠫప") + json.dumps(str(args[0].name) + bstack11ll1l_opy_ (u"ࠢࠡ࠯ࠣࡔࡦࡹࡳࡦࡦࠤࠦఫ")) + bstack11ll1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧబ"))
      if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡶࡸࡪࡶࠢభ"):
        bstack1ll1lll111_opy_(bstack1lll11lll_opy_, bstack11ll1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥమ"))
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠫࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡮ࡣࡵ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡩ࡯ࠢࡤࡪࡹ࡫ࡲࠡࡵࡷࡩࡵࡀࠠࡼࡿࠪయ").format(str(e)))
  bstack1111l11l1_opy_(runner, name, context, args[0], bstack11llllll11_opy_, *args)
def bstack1ll11l1l1l_opy_(runner, name, context, bstack11llllll11_opy_, *args):
  bstack1ll11111ll_opy_.end_test(args[0])
  try:
    bstack11lllll1l_opy_ = args[0].status.name
    bstack1lll11lll_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫర"), context.browser)
    bstack1l1111l1l1_opy_.bstack1l1l11lll1_opy_(bstack1lll11lll_opy_)
    if str(bstack11lllll1l_opy_).lower() == bstack11ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ఱ"):
      bstack11lllll111_opy_ = bstack11ll1l_opy_ (u"ࠧࠨల")
      bstack111111l1l_opy_ = bstack11ll1l_opy_ (u"ࠨࠩళ")
      bstack1l11l11lll_opy_ = bstack11ll1l_opy_ (u"ࠩࠪఴ")
      try:
        import traceback
        bstack11lllll111_opy_ = runner.exception.__class__.__name__
        bstack1l1l1l111_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack111111l1l_opy_ = bstack11ll1l_opy_ (u"ࠪࠤࠬవ").join(bstack1l1l1l111_opy_)
        bstack1l11l11lll_opy_ = bstack1l1l1l111_opy_[-1]
      except Exception as e:
        logger.debug(bstack111ll1lll_opy_.format(str(e)))
      bstack11lllll111_opy_ += bstack1l11l11lll_opy_
      bstack11ll1111l_opy_(context, json.dumps(str(args[0].name) + bstack11ll1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥశ") + str(bstack111111l1l_opy_)),
                          bstack11ll1l_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦష"))
      if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣస") or runner.driver_initialised == bstack11ll1l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧహ"):
        bstack1llllll11l_opy_(getattr(context, bstack11ll1l_opy_ (u"ࠨࡲࡤ࡫ࡪ࠭఺"), None), bstack11ll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ఻"), bstack11lllll111_opy_)
        bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡦࡤࡸࡦࠨ࠺ࠨ఼") + json.dumps(str(args[0].name) + bstack11ll1l_opy_ (u"ࠦࠥ࠳ࠠࡇࡣ࡬ࡰࡪࡪࠡ࡝ࡰࠥఽ") + str(bstack111111l1l_opy_)) + bstack11ll1l_opy_ (u"ࠬ࠲ࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥࡩࡷࡸ࡯ࡳࠤࢀࢁࠬా"))
      if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣి") or runner.driver_initialised == bstack11ll1l_opy_ (u"ࠧࡪࡰࡶࡸࡪࡶࠧీ"):
        bstack1ll1lll111_opy_(bstack1lll11lll_opy_, bstack11ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨు"), bstack11ll1l_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨూ") + str(bstack11lllll111_opy_))
    else:
      bstack11ll1111l_opy_(context, bstack11ll1l_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦృ"), bstack11ll1l_opy_ (u"ࠦ࡮ࡴࡦࡰࠤౄ"))
      if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢ౅") or runner.driver_initialised == bstack11ll1l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ࠭ె"):
        bstack1llllll11l_opy_(getattr(context, bstack11ll1l_opy_ (u"ࠧࡱࡣࡪࡩࠬే"), None), bstack11ll1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣై"))
      bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢࡥࡣࡷࡥࠧࡀࠧ౉") + json.dumps(str(args[0].name) + bstack11ll1l_opy_ (u"ࠥࠤ࠲ࠦࡐࡢࡵࡶࡩࡩࠧࠢొ")) + bstack11ll1l_opy_ (u"ࠫ࠱ࠦࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠡࠤ࡬ࡲ࡫ࡵࠢࡾࡿࠪో"))
      if runner.driver_initialised == bstack11ll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢౌ") or runner.driver_initialised == bstack11ll1l_opy_ (u"࠭ࡩ࡯ࡵࡷࡩࡵ్࠭"):
        bstack1ll1lll111_opy_(bstack1lll11lll_opy_, bstack11ll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ౎"))
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡲࡧࡲ࡬ࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡳࠦࡡࡧࡶࡨࡶࠥ࡬ࡥࡢࡶࡸࡶࡪࡀࠠࡼࡿࠪ౏").format(str(e)))
  bstack1111l11l1_opy_(runner, name, context, context.scenario, bstack11llllll11_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack11111l1l_opy_(runner, name, context, bstack11llllll11_opy_, *args):
    target = context.scenario if hasattr(context, bstack11ll1l_opy_ (u"ࠩࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౐")) else context.feature
    bstack1111l11l1_opy_(runner, name, context, target, bstack11llllll11_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1l11lllll1_opy_(runner, name, context, bstack11llllll11_opy_, *args):
    try:
      bstack1lll11lll_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ౑"), context.browser)
      if context.failed is True:
        bstack1l1lll1l1l_opy_ = []
        bstack1llll111l1_opy_ = []
        bstack1l11l1llll_opy_ = []
        bstack11111lll1_opy_ = bstack11ll1l_opy_ (u"ࠫࠬ౒")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack1l1lll1l1l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l1l1l111_opy_ = traceback.format_tb(exc_tb)
            bstack1l11lll1l_opy_ = bstack11ll1l_opy_ (u"ࠬࠦࠧ౓").join(bstack1l1l1l111_opy_)
            bstack1llll111l1_opy_.append(bstack1l11lll1l_opy_)
            bstack1l11l1llll_opy_.append(bstack1l1l1l111_opy_[-1])
        except Exception as e:
          logger.debug(bstack111ll1lll_opy_.format(str(e)))
        bstack11lllll111_opy_ = bstack11ll1l_opy_ (u"࠭ࠧ౔")
        for i in range(len(bstack1l1lll1l1l_opy_)):
          bstack11lllll111_opy_ += bstack1l1lll1l1l_opy_[i] + bstack1l11l1llll_opy_[i] + bstack11ll1l_opy_ (u"ࠧ࡝ࡰౕࠪ")
        bstack11111lll1_opy_ = bstack11ll1l_opy_ (u"ࠨౖࠢࠪ").join(bstack1llll111l1_opy_)
        if runner.driver_initialised in [bstack11ll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ౗"), bstack11ll1l_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡥࡱࡲࠢౘ")]:
          bstack11ll1111l_opy_(context, bstack11111lll1_opy_, bstack11ll1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥౙ"))
          bstack1llllll11l_opy_(getattr(context, bstack11ll1l_opy_ (u"ࠬࡶࡡࡨࡧࠪౚ"), None), bstack11ll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ౛"), bstack11lllll111_opy_)
          bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡪࡡࡵࡣࠥ࠾ࠬ౜") + json.dumps(bstack11111lll1_opy_) + bstack11ll1l_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧࢃࡽࠨౝ"))
          bstack1ll1lll111_opy_(bstack1lll11lll_opy_, bstack11ll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ౞"), bstack11ll1l_opy_ (u"ࠥࡗࡴࡳࡥࠡࡵࡦࡩࡳࡧࡲࡪࡱࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡢ࡮ࠣ౟") + str(bstack11lllll111_opy_))
          bstack1l1lllllll_opy_ = bstack11ll11lll1_opy_(bstack11111lll1_opy_, runner.feature.name, logger)
          if (bstack1l1lllllll_opy_ != None):
            bstack1ll111111_opy_.append(bstack1l1lllllll_opy_)
      else:
        if runner.driver_initialised in [bstack11ll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣ࡫࡫ࡡࡵࡷࡵࡩࠧౠ"), bstack11ll1l_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠤౡ")]:
          bstack11ll1111l_opy_(context, bstack11ll1l_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤౢ") + str(runner.feature.name) + bstack11ll1l_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤౣ"), bstack11ll1l_opy_ (u"ࠣ࡫ࡱࡪࡴࠨ౤"))
          bstack1llllll11l_opy_(getattr(context, bstack11ll1l_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ౥"), None), bstack11ll1l_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ౦"))
          bstack1lll11lll_opy_.execute_script(bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ౧") + json.dumps(bstack11ll1l_opy_ (u"ࠧࡌࡥࡢࡶࡸࡶࡪࡀࠠࠣ౨") + str(runner.feature.name) + bstack11ll1l_opy_ (u"ࠨࠠࡱࡣࡶࡷࡪࡪࠡࠣ౩")) + bstack11ll1l_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡯࡮ࡧࡱࠥࢁࢂ࠭౪"))
          bstack1ll1lll111_opy_(bstack1lll11lll_opy_, bstack11ll1l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ౫"))
          bstack1l1lllllll_opy_ = bstack11ll11lll1_opy_(bstack11111lll1_opy_, runner.feature.name, logger)
          if (bstack1l1lllllll_opy_ != None):
            bstack1ll111111_opy_.append(bstack1l1lllllll_opy_)
    except Exception as e:
      logger.debug(bstack11ll1l_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶࠤ࡮ࡴࠠࡢࡨࡷࡩࡷࠦࡦࡦࡣࡷࡹࡷ࡫࠺ࠡࡽࢀࠫ౬").format(str(e)))
    bstack1111l11l1_opy_(runner, name, context, context.feature, bstack11llllll11_opy_, *args)
def bstack1l11111l11_opy_(runner, name, context, bstack11llllll11_opy_, *args):
    bstack1111l11l1_opy_(runner, name, context, runner, bstack11llllll11_opy_, *args)
def bstack1l11l1111_opy_(self, name, context, *args):
  if bstack1ll1l1lll1_opy_:
    platform_index = int(threading.current_thread()._name) % bstack1l1llll111_opy_
    bstack1ll1ll1l11_opy_ = CONFIG[bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౭")][platform_index]
    os.environ[bstack11ll1l_opy_ (u"ࠫࡈ࡛ࡒࡓࡇࡑࡘࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡅࡃࡗࡅࠬ౮")] = json.dumps(bstack1ll1ll1l11_opy_)
  global bstack11llllll11_opy_
  if not hasattr(self, bstack11ll1l_opy_ (u"ࠬࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡳࡦࡦࠪ౯")):
    self.driver_initialised = None
  bstack11111ll1l_opy_ = {
      bstack11ll1l_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠪ౰"): bstack11ll11l1l_opy_,
      bstack11ll1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡧࡧࡤࡸࡺࡸࡥࠨ౱"): bstack1l111lll11_opy_,
      bstack11ll1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡶࡤ࡫ࠬ౲"): bstack1l11l1l1ll_opy_,
      bstack11ll1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౳"): bstack1l1l1llll1_opy_,
      bstack11ll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡹ࡫ࡰࠨ౴"): bstack1l1l111lll_opy_,
      bstack11ll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡹ࡫ࡰࠨ౵"): bstack1l1lll11ll_opy_,
      bstack11ll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭౶"): bstack1ll11l1l1l_opy_,
      bstack11ll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡺࡡࡨࠩ౷"): bstack11111l1l_opy_,
      bstack11ll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠧ౸"): bstack1l11lllll1_opy_,
      bstack11ll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠫ౹"): bstack1l11111l11_opy_
  }
  handler = bstack11111ll1l_opy_.get(name, bstack11llllll11_opy_)
  handler(self, name, context, bstack11llllll11_opy_, *args)
  if name in [bstack11ll1l_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ౺"), bstack11ll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫ౻"), bstack11ll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡥࡱࡲࠧ౼")]:
    try:
      bstack1lll11lll_opy_ = threading.current_thread().bstackSessionDriver if bstack111l1ll1l_opy_(bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ౽")) else context.browser
      bstack1l111l1ll1_opy_ = (
        (name == bstack11ll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡧ࡬࡭ࠩ౾") and self.driver_initialised == bstack11ll1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ౿")) or
        (name == bstack11ll1l_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨಀ") and self.driver_initialised == bstack11ll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥಁ")) or
        (name == bstack11ll1l_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡶࡧࡪࡴࡡࡳ࡫ࡲࠫಂ") and self.driver_initialised in [bstack11ll1l_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨಃ"), bstack11ll1l_opy_ (u"ࠧ࡯࡮ࡴࡶࡨࡴࠧ಄")]) or
        (name == bstack11ll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡴࡦࡲࠪಅ") and self.driver_initialised == bstack11ll1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧಆ"))
      )
      if bstack1l111l1ll1_opy_:
        self.driver_initialised = None
        bstack1lll11lll_opy_.quit()
    except Exception:
      pass
def bstack11l111l11_opy_(config, startdir):
  return bstack11ll1l_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲ࠻ࠢࡾ࠴ࢂࠨಇ").format(bstack11ll1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣಈ"))
notset = Notset()
def bstack11ll1lll11_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack1ll1llll1l_opy_
  if str(name).lower() == bstack11ll1l_opy_ (u"ࠪࡨࡷ࡯ࡶࡦࡴࠪಉ"):
    return bstack11ll1l_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠥಊ")
  else:
    return bstack1ll1llll1l_opy_(self, name, default, skip)
def bstack1llll1ll1_opy_(item, when):
  global bstack111l1111l_opy_
  try:
    bstack111l1111l_opy_(item, when)
  except Exception as e:
    pass
def bstack1111l1lll_opy_():
  return
def bstack11l1llll11_opy_(type, name, status, reason, bstack1lll11l1l_opy_, bstack11l1ll11l_opy_):
  bstack1lll1111l_opy_ = {
    bstack11ll1l_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬಋ"): type,
    bstack11ll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಌ"): {}
  }
  if type == bstack11ll1l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩ಍"):
    bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫಎ")][bstack11ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨಏ")] = bstack1lll11l1l_opy_
    bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ಐ")][bstack11ll1l_opy_ (u"ࠫࡩࡧࡴࡢࠩ಑")] = json.dumps(str(bstack11l1ll11l_opy_))
  if type == bstack11ll1l_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ಒ"):
    bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩಓ")][bstack11ll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬಔ")] = name
  if type == bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫಕ"):
    bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬಖ")][bstack11ll1l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪಗ")] = status
    if status == bstack11ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫಘ"):
      bstack1lll1111l_opy_[bstack11ll1l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨಙ")][bstack11ll1l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ಚ")] = json.dumps(str(reason))
  bstack11l1l11ll1_opy_ = bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬಛ").format(json.dumps(bstack1lll1111l_opy_))
  return bstack11l1l11ll1_opy_
def bstack1l1llll1l1_opy_(driver_command, response):
    if driver_command == bstack11ll1l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬಜ"):
        bstack1l1llll1_opy_.bstack1l11ll11ll_opy_({
            bstack11ll1l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨಝ"): response[bstack11ll1l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩಞ")],
            bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫಟ"): bstack1l1llll1_opy_.current_test_uuid()
        })
def bstack11l1l1ll1_opy_(item, call, rep):
  global bstack1ll111llll_opy_
  global bstack11l1l1l1l1_opy_
  global bstack11llll11ll_opy_
  name = bstack11ll1l_opy_ (u"ࠬ࠭ಠ")
  try:
    if rep.when == bstack11ll1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫಡ"):
      bstack1llll1l11l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack11llll11ll_opy_:
          name = str(rep.nodeid)
          bstack1ll11l1ll1_opy_ = bstack11l1llll11_opy_(bstack11ll1l_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨಢ"), name, bstack11ll1l_opy_ (u"ࠨࠩಣ"), bstack11ll1l_opy_ (u"ࠩࠪತ"), bstack11ll1l_opy_ (u"ࠪࠫಥ"), bstack11ll1l_opy_ (u"ࠫࠬದ"))
          threading.current_thread().bstack11l11ll1l_opy_ = name
          for driver in bstack11l1l1l1l1_opy_:
            if bstack1llll1l11l_opy_ == driver.session_id:
              driver.execute_script(bstack1ll11l1ll1_opy_)
      except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬಧ").format(str(e)))
      try:
        bstack1lll1ll1l1_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack11ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧನ"):
          status = bstack11ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ಩") if rep.outcome.lower() == bstack11ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨಪ") else bstack11ll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩಫ")
          reason = bstack11ll1l_opy_ (u"ࠪࠫಬ")
          if status == bstack11ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫಭ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack11ll1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪಮ") if status == bstack11ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ಯ") else bstack11ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ರ")
          data = name + bstack11ll1l_opy_ (u"ࠨࠢࡳࡥࡸࡹࡥࡥࠣࠪಱ") if status == bstack11ll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩಲ") else name + bstack11ll1l_opy_ (u"ࠪࠤ࡫ࡧࡩ࡭ࡧࡧࠥࠥ࠭ಳ") + reason
          bstack11ll1l1ll1_opy_ = bstack11l1llll11_opy_(bstack11ll1l_opy_ (u"ࠫࡦࡴ࡮ࡰࡶࡤࡸࡪ࠭಴"), bstack11ll1l_opy_ (u"ࠬ࠭ವ"), bstack11ll1l_opy_ (u"࠭ࠧಶ"), bstack11ll1l_opy_ (u"ࠧࠨಷ"), level, data)
          for driver in bstack11l1l1l1l1_opy_:
            if bstack1llll1l11l_opy_ == driver.session_id:
              driver.execute_script(bstack11ll1l1ll1_opy_)
      except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡩ࡯࡯ࡶࡨࡼࡹࠦࡦࡰࡴࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡴࡧࡶࡷ࡮ࡵ࡮࠻ࠢࡾࢁࠬಸ").format(str(e)))
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡴࡢࡶࡨࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠤࡹ࡫ࡳࡵࠢࡶࡸࡦࡺࡵࡴ࠼ࠣࡿࢂ࠭ಹ").format(str(e)))
  bstack1ll111llll_opy_(item, call, rep)
def bstack1llll1lll1_opy_(driver, bstack1llll11ll1_opy_, test=None):
  global bstack1l1lllll1_opy_
  if test != None:
    bstack1l1l1l1l1_opy_ = getattr(test, bstack11ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨ಺"), None)
    bstack1111l111l_opy_ = getattr(test, bstack11ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩ಻"), None)
    PercySDK.screenshot(driver, bstack1llll11ll1_opy_, bstack1l1l1l1l1_opy_=bstack1l1l1l1l1_opy_, bstack1111l111l_opy_=bstack1111l111l_opy_, bstack111111l11_opy_=bstack1l1lllll1_opy_)
  else:
    PercySDK.screenshot(driver, bstack1llll11ll1_opy_)
def bstack111lll111_opy_(driver):
  if bstack1lllllll1_opy_.bstack1l11ll1l1_opy_() is True or bstack1lllllll1_opy_.capturing() is True:
    return
  bstack1lllllll1_opy_.bstack11l111l1l_opy_()
  while not bstack1lllllll1_opy_.bstack1l11ll1l1_opy_():
    bstack1l1l11111l_opy_ = bstack1lllllll1_opy_.bstack1ll1ll111l_opy_()
    bstack1llll1lll1_opy_(driver, bstack1l1l11111l_opy_)
  bstack1lllllll1_opy_.bstack1ll1111l11_opy_()
def bstack1lll111l1_opy_(sequence, driver_command, response = None, bstack11ll111ll1_opy_ = None, args = None):
    try:
      if sequence != bstack11ll1l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩ಼ࠬ"):
        return
      if percy.bstack1l111ll11_opy_() == bstack11ll1l_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧಽ"):
        return
      bstack1l1l11111l_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪಾ"), None)
      for command in bstack11111llll_opy_:
        if command == driver_command:
          for driver in bstack11l1l1l1l1_opy_:
            bstack111lll111_opy_(driver)
      bstack11111l111_opy_ = percy.bstack11ll1lllll_opy_()
      if driver_command in bstack11111111_opy_[bstack11111l111_opy_]:
        bstack1lllllll1_opy_.bstack1l1l1ll11_opy_(bstack1l1l11111l_opy_, driver_command)
    except Exception as e:
      pass
def bstack11lll1l1l1_opy_(framework_name):
  if bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠ࡯ࡲࡨࡤࡩࡡ࡭࡮ࡨࡨࠬಿ")):
      return
  bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ೀ"), True)
  global bstack11l11l11l_opy_
  global bstack11ll11111l_opy_
  global bstack1l11ll1l11_opy_
  bstack11l11l11l_opy_ = framework_name
  logger.info(bstack1ll1llllll_opy_.format(bstack11l11l11l_opy_.split(bstack11ll1l_opy_ (u"ࠪ࠱ࠬು"))[0]))
  bstack11l1ll1111_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1ll1l1lll1_opy_:
      Service.start = bstack1l111l111l_opy_
      Service.stop = bstack1l1lll111_opy_
      webdriver.Remote.get = bstack1l1l11l111_opy_
      WebDriver.close = bstack11l1lll11_opy_
      WebDriver.quit = bstack1ll1ll1ll_opy_
      webdriver.Remote.__init__ = bstack1lllllll1l_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1ll1l1lll1_opy_:
        webdriver.Remote.__init__ = bstack111111l1_opy_
    WebDriver.execute = bstack1l1lll1lll_opy_
    bstack11ll11111l_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1ll1l1lll1_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l1l111l1l_opy_
  except Exception as e:
    pass
  bstack1lllll1lll_opy_()
  if not bstack11ll11111l_opy_:
    bstack11llllll1_opy_(bstack11ll1l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨೂ"), bstack1lll11ll1_opy_)
  if bstack11ll1l11l_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack11l11ll11_opy_
    except Exception as e:
      logger.error(bstack11lll1l1l_opy_.format(str(e)))
  if bstack1lll1111l1_opy_():
    bstack1111l1111_opy_(CONFIG, logger)
  if (bstack11ll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫೃ") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack1l111ll11_opy_() == bstack11ll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦೄ"):
          bstack1l11l11ll1_opy_(bstack1lll111l1_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack111l11l11_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1ll11l1l11_opy_
      except Exception as e:
        logger.warn(bstack1ll11l111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack11l1l111l_opy_
      except Exception as e:
        logger.debug(bstack1lll111ll_opy_ + str(e))
    except Exception as e:
      bstack11llllll1_opy_(e, bstack1ll11l111l_opy_)
    Output.start_test = bstack1l111l1111_opy_
    Output.end_test = bstack1lllll1l1_opy_
    TestStatus.__init__ = bstack11ll11lll_opy_
    QueueItem.__init__ = bstack1ll1l1l1l1_opy_
    pabot._create_items = bstack111l111l1_opy_
    try:
      from pabot import __version__ as bstack1llllll11_opy_
      if version.parse(bstack1llllll11_opy_) >= version.parse(bstack11ll1l_opy_ (u"ࠧ࠳࠰࠴࠹࠳࠶ࠧ೅")):
        pabot._run = bstack1l1ll1ll1_opy_
      elif version.parse(bstack1llllll11_opy_) >= version.parse(bstack11ll1l_opy_ (u"ࠨ࠴࠱࠵࠸࠴࠰ࠨೆ")):
        pabot._run = bstack1l1l1lll1l_opy_
      else:
        pabot._run = bstack1lll11111_opy_
    except Exception as e:
      pabot._run = bstack1lll11111_opy_
    pabot._create_command_for_execution = bstack1l11l1l11_opy_
    pabot._report_results = bstack1l11llll1l_opy_
  if bstack11ll1l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩೇ") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11llllll1_opy_(e, bstack1ll1l1111_opy_)
    Runner.run_hook = bstack1l11l1111_opy_
    Step.run = bstack1l1ll1l1l_opy_
  if bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪೈ") in str(framework_name).lower():
    if not bstack1ll1l1lll1_opy_:
      return
    try:
      if percy.bstack1l111ll11_opy_() == bstack11ll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤ೉"):
          bstack1l11l11ll1_opy_(bstack1lll111l1_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack11l111l11_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1111l1lll_opy_
      Config.getoption = bstack11ll1lll11_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack11l1l1ll1_opy_
    except Exception as e:
      pass
def bstack1l1l11l1l_opy_():
  global CONFIG
  if bstack11ll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬೊ") in CONFIG and int(CONFIG[bstack11ll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ೋ")]) > 1:
    logger.warn(bstack1lll1111ll_opy_)
def bstack1lll1llll_opy_(arg, bstack111l1111_opy_, bstack1l1l11ll11_opy_=None):
  global CONFIG
  global bstack1l1ll1l1ll_opy_
  global bstack1llll1l1ll_opy_
  global bstack1ll1l1lll1_opy_
  global bstack11l111ll_opy_
  bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧೌ")
  if bstack111l1111_opy_ and isinstance(bstack111l1111_opy_, str):
    bstack111l1111_opy_ = eval(bstack111l1111_opy_)
  CONFIG = bstack111l1111_opy_[bstack11ll1l_opy_ (u"ࠨࡅࡒࡒࡋࡏࡇࠨ್")]
  bstack1l1ll1l1ll_opy_ = bstack111l1111_opy_[bstack11ll1l_opy_ (u"ࠩࡋ࡙ࡇࡥࡕࡓࡎࠪ೎")]
  bstack1llll1l1ll_opy_ = bstack111l1111_opy_[bstack11ll1l_opy_ (u"ࠪࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬ೏")]
  bstack1ll1l1lll1_opy_ = bstack111l1111_opy_[bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ೐")]
  bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭೑"), bstack1ll1l1lll1_opy_)
  os.environ[bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨ೒")] = bstack1ll1ll1ll1_opy_
  os.environ[bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌ࠭೓")] = json.dumps(CONFIG)
  os.environ[bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨ೔")] = bstack1l1ll1l1ll_opy_
  os.environ[bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪೕ")] = str(bstack1llll1l1ll_opy_)
  os.environ[bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓ࡝࡙ࡋࡓࡕࡡࡓࡐ࡚ࡍࡉࡏࠩೖ")] = str(True)
  if bstack111lllll1_opy_(arg, [bstack11ll1l_opy_ (u"ࠫ࠲ࡴࠧ೗"), bstack11ll1l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭೘")]) != -1:
    os.environ[bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧ೙")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1ll11ll1l1_opy_)
    return
  bstack1l111ll1l1_opy_()
  global bstack1ll1ll111_opy_
  global bstack1l1lllll1_opy_
  global bstack1ll1llll11_opy_
  global bstack111ll11ll_opy_
  global bstack11ll11l11l_opy_
  global bstack1l11ll1l11_opy_
  global bstack1l1l1l1l1l_opy_
  arg.append(bstack11ll1l_opy_ (u"ࠢ࠮࡙ࠥ೚"))
  arg.append(bstack11ll1l_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥ࠻ࡏࡲࡨࡺࡲࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡱࡵࡵࡲࡵࡧࡧ࠾ࡵࡿࡴࡦࡵࡷ࠲ࡕࡿࡴࡦࡵࡷ࡛ࡦࡸ࡮ࡪࡰࡪࠦ೛"))
  arg.append(bstack11ll1l_opy_ (u"ࠤ࠰࡛ࠧ೜"))
  arg.append(bstack11ll1l_opy_ (u"ࠥ࡭࡬ࡴ࡯ࡳࡧ࠽ࡘ࡭࡫ࠠࡩࡱࡲ࡯࡮ࡳࡰ࡭ࠤೝ"))
  global bstack11llllllll_opy_
  global bstack11111111l_opy_
  global bstack11l1l11l11_opy_
  global bstack1111l1l1l_opy_
  global bstack11ll11llll_opy_
  global bstack1ll11lll1l_opy_
  global bstack1ll1l11l1l_opy_
  global bstack11l1llll1l_opy_
  global bstack1l1llllll1_opy_
  global bstack111ll11l1_opy_
  global bstack1ll1llll1l_opy_
  global bstack111l1111l_opy_
  global bstack1ll111llll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11llllllll_opy_ = webdriver.Remote.__init__
    bstack11111111l_opy_ = WebDriver.quit
    bstack11l1llll1l_opy_ = WebDriver.close
    bstack1l1llllll1_opy_ = WebDriver.get
    bstack11l1l11l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1lll1ll1ll_opy_(CONFIG) and bstack1l1l111ll1_opy_():
    if bstack11l111lll_opy_() < version.parse(bstack1l1lll11l1_opy_):
      logger.error(bstack1lll111l1l_opy_.format(bstack11l111lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111ll11l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11lll1l1l_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack1ll1llll1l_opy_ = Config.getoption
    from _pytest import runner
    bstack111l1111l_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack11l1ll1l_opy_)
  try:
    from pytest_bdd import reporting
    bstack1ll111llll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack11ll1l_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬೞ"))
  bstack1ll1llll11_opy_ = CONFIG.get(bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩ೟"), {}).get(bstack11ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨೠ"))
  bstack1l1l1l1l1l_opy_ = True
  bstack11lll1l1l1_opy_(bstack11l1ll1lll_opy_)
  os.environ[bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨೡ")] = CONFIG[bstack11ll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪೢ")]
  os.environ[bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬೣ")] = CONFIG[bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭೤")]
  os.environ[bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧ೥")] = bstack1ll1l1lll1_opy_.__str__()
  from _pytest.config import main as bstack1ll111l1l1_opy_
  bstack11ll1l111l_opy_ = []
  try:
    bstack1l11l1111l_opy_ = bstack1ll111l1l1_opy_(arg)
    if bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ೦") in multiprocessing.current_process().__dict__.keys():
      for bstack111l1l1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack11ll1l111l_opy_.append(bstack111l1l1ll_opy_)
    try:
      bstack1l111l1l1_opy_ = (bstack11ll1l111l_opy_, int(bstack1l11l1111l_opy_))
      bstack1l1l11ll11_opy_.append(bstack1l111l1l1_opy_)
    except:
      bstack1l1l11ll11_opy_.append((bstack11ll1l111l_opy_, bstack1l11l1111l_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack11ll1l111l_opy_.append({bstack11ll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ೧"): bstack11ll1l_opy_ (u"ࠧࡑࡴࡲࡧࡪࡹࡳࠡࠩ೨") + os.environ.get(bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ೩")), bstack11ll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ೪"): traceback.format_exc(), bstack11ll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ೫"): int(os.environ.get(bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ೬")))})
    bstack1l1l11ll11_opy_.append((bstack11ll1l111l_opy_, 1))
def bstack111l11111_opy_(arg):
  global bstack1l11111l1l_opy_
  bstack11lll1l1l1_opy_(bstack1l1l11ll1l_opy_)
  os.environ[bstack11ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭೭")] = str(bstack1llll1l1ll_opy_)
  from behave.__main__ import main as bstack1l11l11l11_opy_
  status_code = bstack1l11l11l11_opy_(arg)
  if status_code != 0:
    bstack1l11111l1l_opy_ = status_code
def bstack11l1lllll_opy_():
  logger.info(bstack1lll111l11_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack11ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ೮"), help=bstack11ll1l_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡥࡲࡲ࡫࡯ࡧࠨ೯"))
  parser.add_argument(bstack11ll1l_opy_ (u"ࠨ࠯ࡸࠫ೰"), bstack11ll1l_opy_ (u"ࠩ࠰࠱ࡺࡹࡥࡳࡰࡤࡱࡪ࠭ೱ"), help=bstack11ll1l_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡶࡵࡨࡶࡳࡧ࡭ࡦࠩೲ"))
  parser.add_argument(bstack11ll1l_opy_ (u"ࠫ࠲ࡱࠧೳ"), bstack11ll1l_opy_ (u"ࠬ࠳࠭࡬ࡧࡼࠫ೴"), help=bstack11ll1l_opy_ (u"࡙࠭ࡰࡷࡵࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡥࡨࡩࡥࡴࡵࠣ࡯ࡪࡿࠧ೵"))
  parser.add_argument(bstack11ll1l_opy_ (u"ࠧ࠮ࡨࠪ೶"), bstack11ll1l_opy_ (u"ࠨ࠯࠰ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭೷"), help=bstack11ll1l_opy_ (u"ࠩ࡜ࡳࡺࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ೸"))
  bstack1111l11ll_opy_ = parser.parse_args()
  try:
    bstack11ll1llll1_opy_ = bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡳ࡫ࡲࡪࡥ࠱ࡽࡲࡲ࠮ࡴࡣࡰࡴࡱ࡫ࠧ೹")
    if bstack1111l11ll_opy_.framework and bstack1111l11ll_opy_.framework not in (bstack11ll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ೺"), bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭೻")):
      bstack11ll1llll1_opy_ = bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࡻࡰࡰ࠳ࡹࡡ࡮ࡲ࡯ࡩࠬ೼")
    bstack1l111l1l1l_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll1llll1_opy_)
    bstack11l1ll111l_opy_ = open(bstack1l111l1l1l_opy_, bstack11ll1l_opy_ (u"ࠧࡳࠩ೽"))
    bstack1l1ll1l11l_opy_ = bstack11l1ll111l_opy_.read()
    bstack11l1ll111l_opy_.close()
    if bstack1111l11ll_opy_.username:
      bstack1l1ll1l11l_opy_ = bstack1l1ll1l11l_opy_.replace(bstack11ll1l_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡕࡔࡇࡕࡒࡆࡓࡅࠨ೾"), bstack1111l11ll_opy_.username)
    if bstack1111l11ll_opy_.key:
      bstack1l1ll1l11l_opy_ = bstack1l1ll1l11l_opy_.replace(bstack11ll1l_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡂࡅࡆࡉࡘ࡙࡟ࡌࡇ࡜ࠫ೿"), bstack1111l11ll_opy_.key)
    if bstack1111l11ll_opy_.framework:
      bstack1l1ll1l11l_opy_ = bstack1l1ll1l11l_opy_.replace(bstack11ll1l_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫഀ"), bstack1111l11ll_opy_.framework)
    file_name = bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧഁ")
    file_path = os.path.abspath(file_name)
    bstack111ll1ll1_opy_ = open(file_path, bstack11ll1l_opy_ (u"ࠬࡽࠧം"))
    bstack111ll1ll1_opy_.write(bstack1l1ll1l11l_opy_)
    bstack111ll1ll1_opy_.close()
    logger.info(bstack1l1l1111l_opy_)
    try:
      os.environ[bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨഃ")] = bstack1111l11ll_opy_.framework if bstack1111l11ll_opy_.framework != None else bstack11ll1l_opy_ (u"ࠢࠣഄ")
      config = yaml.safe_load(bstack1l1ll1l11l_opy_)
      config[bstack11ll1l_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨഅ")] = bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡶࡩࡹࡻࡰࠨആ")
      bstack11111l1l1_opy_(bstack1llllll1ll_opy_, config)
    except Exception as e:
      logger.debug(bstack1l1111ll1l_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lllll11l1_opy_.format(str(e)))
def bstack11111l1l1_opy_(bstack1l1ll1lll_opy_, config, bstack1l11l111ll_opy_={}):
  global bstack1ll1l1lll1_opy_
  global bstack1l1l1l11ll_opy_
  global bstack11l111ll_opy_
  if not config:
    return
  bstack11llll1ll_opy_ = bstack1ll1lll11l_opy_ if not bstack1ll1l1lll1_opy_ else (
    bstack11ll111l1_opy_ if bstack11ll1l_opy_ (u"ࠪࡥࡵࡶࠧഇ") in config else bstack1l11l1ll11_opy_)
  bstack111l11l1l_opy_ = False
  bstack1l1l1lll11_opy_ = False
  if bstack1ll1l1lll1_opy_ is True:
      if bstack11ll1l_opy_ (u"ࠫࡦࡶࡰࠨഈ") in config:
          bstack111l11l1l_opy_ = True
      else:
          bstack1l1l1lll11_opy_ = True
  bstack1l1l1111ll_opy_ = bstack1ll11ll1ll_opy_.bstack1lll1ll1l_opy_(config, bstack1l1l1l11ll_opy_)
  data = {
    bstack11ll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧഉ"): config[bstack11ll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨഊ")],
    bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪഋ"): config[bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫഌ")],
    bstack11ll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭഍"): bstack1l1ll1lll_opy_,
    bstack11ll1l_opy_ (u"ࠪࡨࡪࡺࡥࡤࡶࡨࡨࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧഎ"): os.environ.get(bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡊࡗࡇࡍࡆ࡙ࡒࡖࡐ࠭ഏ"), bstack1l1l1l11ll_opy_),
    bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧഐ"): bstack1ll11ll111_opy_,
    bstack11ll1l_opy_ (u"࠭࡯ࡱࡶ࡬ࡱࡦࡲ࡟ࡩࡷࡥࡣࡺࡸ࡬ࠨ഑"): bstack1l1l111ll_opy_(),
    bstack11ll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵࠪഒ"): {
      bstack11ll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ഓ"): str(config[bstack11ll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩഔ")]) if bstack11ll1l_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪക") in config else bstack11ll1l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧഖ"),
      bstack11ll1l_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࡖࡦࡴࡶ࡭ࡴࡴࠧഗ"): sys.version,
      bstack11ll1l_opy_ (u"࠭ࡲࡦࡨࡨࡶࡷ࡫ࡲࠨഘ"): bstack1ll11l11l1_opy_(os.getenv(bstack11ll1l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤങ"), bstack11ll1l_opy_ (u"ࠣࠤച"))),
      bstack11ll1l_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫഛ"): bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪജ"),
      bstack11ll1l_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࠬഝ"): bstack11llll1ll_opy_,
      bstack11ll1l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪഞ"): bstack1l1l1111ll_opy_,
      bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡶࡷ࡬ࡨࠬട"): os.environ[bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬഠ")],
      bstack11ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫഡ"): bstack1l1l11l1l1_opy_(os.environ.get(bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡈࡕࡅࡒࡋࡗࡐࡔࡎࠫഢ"), bstack1l1l1l11ll_opy_)),
      bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ണ"): config[bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧത")] if config[bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨഥ")] else bstack11ll1l_opy_ (u"ࠨࡵ࡯࡭ࡱࡳࡼࡴࠢദ"),
      bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩധ"): str(config[bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪന")]) if bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫഩ") in config else bstack11ll1l_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࠦപ"),
      bstack11ll1l_opy_ (u"ࠫࡴࡹࠧഫ"): sys.platform,
      bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠧബ"): socket.gethostname(),
      bstack11ll1l_opy_ (u"࠭ࡳࡥ࡭ࡕࡹࡳࡏࡤࠨഭ"): bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩമ"))
    }
  }
  if not bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨയ")) is None:
    data[bstack11ll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬര")][bstack11ll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡒ࡫ࡴࡢࡦࡤࡸࡦ࠭റ")] = {
      bstack11ll1l_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫല"): bstack11ll1l_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪള"),
      bstack11ll1l_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭ഴ"): bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠧࡴࡦ࡮ࡏ࡮ࡲ࡬ࡔ࡫ࡪࡲࡦࡲࠧവ")),
      bstack11ll1l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࡏࡷࡰࡦࡪࡸࠧശ"): bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡑࡳࠬഷ"))
    }
  if bstack1l1ll1lll_opy_ == bstack1l1l11llll_opy_:
    data[bstack11ll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭സ")][bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡆࡳࡳ࡬ࡩࡨࠩഹ")] = bstack1111111ll_opy_(config)
    data[bstack11ll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡵࡸ࡯ࡱࡧࡵࡸ࡮࡫ࡳࠨഺ")][bstack11ll1l_opy_ (u"࠭ࡩࡴࡒࡨࡶࡨࡿࡁࡶࡶࡲࡉࡳࡧࡢ࡭ࡧࡧ഻ࠫ")] = percy.bstack1111l1l11_opy_
    data[bstack11ll1l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵ഼ࠪ")][bstack11ll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡂࡶ࡫࡯ࡨࡎࡪࠧഽ")] = percy.bstack1l111111ll_opy_
  update(data[bstack11ll1l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠬാ")], bstack1l11l111ll_opy_)
  try:
    response = bstack1ll1lll1l1_opy_(bstack11ll1l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨി"), bstack1l1l1l111l_opy_(bstack111l1l111_opy_), data, {
      bstack11ll1l_opy_ (u"ࠫࡦࡻࡴࡩࠩീ"): (config[bstack11ll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧു")], config[bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩൂ")])
    })
    if response:
      logger.debug(bstack11l1l1111_opy_.format(bstack1l1ll1lll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1l1l1ll1l_opy_.format(str(e)))
def bstack1ll11l11l1_opy_(framework):
  return bstack11ll1l_opy_ (u"ࠢࡼࡿ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࡽࢀࠦൃ").format(str(framework), __version__) if framework else bstack11ll1l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࡻࡾࠤൄ").format(
    __version__)
def bstack1l111ll1l1_opy_():
  global CONFIG
  global bstack1lll11l1l1_opy_
  if bool(CONFIG):
    return
  try:
    bstack1llll1l1l1_opy_()
    logger.debug(bstack11l111111_opy_.format(str(CONFIG)))
    bstack1lll11l1l1_opy_ = bstack1l1ll1ll11_opy_.bstack11l1l1l1ll_opy_(CONFIG, bstack1lll11l1l1_opy_)
    bstack11l1ll1111_opy_()
  except Exception as e:
    logger.error(bstack11ll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࡷࡳ࠰ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࠨ൅") + str(e))
    sys.exit(1)
  sys.excepthook = bstack11lllllll_opy_
  atexit.register(bstack1l11l1l11l_opy_)
  signal.signal(signal.SIGINT, bstack11ll1l111_opy_)
  signal.signal(signal.SIGTERM, bstack11ll1l111_opy_)
def bstack11lllllll_opy_(exctype, value, traceback):
  global bstack11l1l1l1l1_opy_
  try:
    for driver in bstack11l1l1l1l1_opy_:
      bstack1ll1lll111_opy_(driver, bstack11ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪെ"), bstack11ll1l_opy_ (u"ࠦࡘ࡫ࡳࡴ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡽࡩࡵࡪ࠽ࠤࡡࡴࠢേ") + str(value))
  except Exception:
    pass
  bstack1lllll1111_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1lllll1111_opy_(message=bstack11ll1l_opy_ (u"ࠬ࠭ൈ"), bstack1ll1l1ll1_opy_ = False):
  global CONFIG
  bstack1llll11ll_opy_ = bstack11ll1l_opy_ (u"࠭ࡧ࡭ࡱࡥࡥࡱࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠨ൉") if bstack1ll1l1ll1_opy_ else bstack11ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ൊ")
  try:
    if message:
      bstack1l11l111ll_opy_ = {
        bstack1llll11ll_opy_ : str(message)
      }
      bstack11111l1l1_opy_(bstack1l1l11llll_opy_, CONFIG, bstack1l11l111ll_opy_)
    else:
      bstack11111l1l1_opy_(bstack1l1l11llll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack11ll1l1ll_opy_.format(str(e)))
def bstack1ll111111l_opy_(bstack1l11lllll_opy_, size):
  bstack11lllllll1_opy_ = []
  while len(bstack1l11lllll_opy_) > size:
    bstack1lll111111_opy_ = bstack1l11lllll_opy_[:size]
    bstack11lllllll1_opy_.append(bstack1lll111111_opy_)
    bstack1l11lllll_opy_ = bstack1l11lllll_opy_[size:]
  bstack11lllllll1_opy_.append(bstack1l11lllll_opy_)
  return bstack11lllllll1_opy_
def bstack11l1lll111_opy_(args):
  if bstack11ll1l_opy_ (u"ࠨ࠯ࡰࠫോ") in args and bstack11ll1l_opy_ (u"ࠩࡳࡨࡧ࠭ൌ") in args:
    return True
  return False
def run_on_browserstack(bstack1llll111ll_opy_=None, bstack1l1l11ll11_opy_=None, bstack1lll11l1ll_opy_=False):
  global CONFIG
  global bstack1l1ll1l1ll_opy_
  global bstack1llll1l1ll_opy_
  global bstack1l1l1l11ll_opy_
  global bstack11l111ll_opy_
  bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"്ࠪࠫ")
  bstack111l1l1l1_opy_(bstack11llllll1l_opy_, logger)
  if bstack1llll111ll_opy_ and isinstance(bstack1llll111ll_opy_, str):
    bstack1llll111ll_opy_ = eval(bstack1llll111ll_opy_)
  if bstack1llll111ll_opy_:
    CONFIG = bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠫࡈࡕࡎࡇࡋࡊࠫൎ")]
    bstack1l1ll1l1ll_opy_ = bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠬࡎࡕࡃࡡࡘࡖࡑ࠭൏")]
    bstack1llll1l1ll_opy_ = bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"࠭ࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨ൐")]
    bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ൑"), bstack1llll1l1ll_opy_)
    bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ൒")
  bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠩࡶࡨࡰࡘࡵ࡯ࡋࡧࠫ൓"), uuid4().__str__())
  logger.debug(bstack11ll1l_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࡂ࠭ൔ") + bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩ࠭ൕ")))
  if not bstack1lll11l1ll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1ll11ll1l1_opy_)
      return
    if sys.argv[1] == bstack11ll1l_opy_ (u"ࠬ࠳࠭ࡷࡧࡵࡷ࡮ࡵ࡮ࠨൖ") or sys.argv[1] == bstack11ll1l_opy_ (u"࠭࠭ࡷࠩൗ"):
      logger.info(bstack11ll1l_opy_ (u"ࠧࡃࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡐࡺࡶ࡫ࡳࡳࠦࡓࡅࡍࠣࡺࢀࢃࠧ൘").format(__version__))
      return
    if sys.argv[1] == bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ൙"):
      bstack11l1lllll_opy_()
      return
  args = sys.argv
  bstack1l111ll1l1_opy_()
  global bstack1ll1ll111_opy_
  global bstack1l1llll111_opy_
  global bstack1l1l1l1l1l_opy_
  global bstack11l1ll1l1l_opy_
  global bstack1l1lllll1_opy_
  global bstack1ll1llll11_opy_
  global bstack111ll11ll_opy_
  global bstack1ll1l1l11_opy_
  global bstack11ll11l11l_opy_
  global bstack1l11ll1l11_opy_
  global bstack1ll111lll1_opy_
  bstack1l1llll111_opy_ = len(CONFIG.get(bstack11ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ൚"), []))
  if not bstack1ll1ll1ll1_opy_:
    if args[1] == bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ൛") or args[1] == bstack11ll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠷ࠬ൜"):
      bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ൝")
      args = args[2:]
    elif args[1] == bstack11ll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ൞"):
      bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ൟ")
      args = args[2:]
    elif args[1] == bstack11ll1l_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧൠ"):
      bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨൡ")
      args = args[2:]
    elif args[1] == bstack11ll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫൢ"):
      bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬൣ")
      args = args[2:]
    elif args[1] == bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ൤"):
      bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭൥")
      args = args[2:]
    elif args[1] == bstack11ll1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧ൦"):
      bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ൧")
      args = args[2:]
    else:
      if not bstack11ll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൨") in CONFIG or str(CONFIG[bstack11ll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൩")]).lower() in [bstack11ll1l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ൪"), bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭൫")]:
        bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭൬")
        args = args[1:]
      elif str(CONFIG[bstack11ll1l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ൭")]).lower() == bstack11ll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ൮"):
        bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ൯")
        args = args[1:]
      elif str(CONFIG[bstack11ll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭൰")]).lower() == bstack11ll1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪ൱"):
        bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ൲")
        args = args[1:]
      elif str(CONFIG[bstack11ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ൳")]).lower() == bstack11ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ൴"):
        bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ൵")
        args = args[1:]
      elif str(CONFIG[bstack11ll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ൶")]).lower() == bstack11ll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ൷"):
        bstack1ll1ll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫ൸")
        args = args[1:]
      else:
        os.environ[bstack11ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧ൹")] = bstack1ll1ll1ll1_opy_
        bstack11l1l1ll11_opy_(bstack1l111l1ll_opy_)
  os.environ[bstack11ll1l_opy_ (u"࠭ࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࡡࡘࡗࡊࡊࠧൺ")] = bstack1ll1ll1ll1_opy_
  bstack1l1l1l11ll_opy_ = bstack1ll1ll1ll1_opy_
  global bstack1lll1l1111_opy_
  global bstack1l1l1111l1_opy_
  if bstack1llll111ll_opy_:
    try:
      os.environ[bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩൻ")] = bstack1ll1ll1ll1_opy_
      bstack11111l1l1_opy_(bstack1lll1l111l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1llllll111_opy_.format(str(e)))
  global bstack11llllllll_opy_
  global bstack11111111l_opy_
  global bstack11111l11_opy_
  global bstack1llll1ll11_opy_
  global bstack1lll1l11ll_opy_
  global bstack1ll11lll1_opy_
  global bstack1111l1l1l_opy_
  global bstack11ll11llll_opy_
  global bstack11lll1lll_opy_
  global bstack1ll11lll1l_opy_
  global bstack1ll1l11l1l_opy_
  global bstack11l1llll1l_opy_
  global bstack11llllll11_opy_
  global bstack1l11l11ll_opy_
  global bstack1l1llllll1_opy_
  global bstack111ll11l1_opy_
  global bstack1ll1llll1l_opy_
  global bstack111l1111l_opy_
  global bstack1ll1l1l111_opy_
  global bstack1ll111llll_opy_
  global bstack11l1l11l11_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11llllllll_opy_ = webdriver.Remote.__init__
    bstack11111111l_opy_ = WebDriver.quit
    bstack11l1llll1l_opy_ = WebDriver.close
    bstack1l1llllll1_opy_ = WebDriver.get
    bstack11l1l11l11_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1lll1l1111_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack11llll1l1l_opy_
    bstack1l1l1111l1_opy_ = bstack11llll1l1l_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1ll11ll_opy_
    from QWeb.keywords import browser
    bstack1l1ll11ll_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1lll1ll1ll_opy_(CONFIG) and bstack1l1l111ll1_opy_():
    if bstack11l111lll_opy_() < version.parse(bstack1l1lll11l1_opy_):
      logger.error(bstack1lll111l1l_opy_.format(bstack11l111lll_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack111ll11l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack11lll1l1l_opy_.format(str(e)))
  if not CONFIG.get(bstack11ll1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪർ"), False) and not bstack1llll111ll_opy_:
    logger.info(bstack1ll1ll1l1_opy_)
  if bstack1ll1ll1ll1_opy_ != bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩൽ") or (bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪൾ") and not bstack1llll111ll_opy_):
    bstack1l1l1llll_opy_()
  if (bstack1ll1ll1ll1_opy_ in [bstack11ll1l_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪൿ"), bstack11ll1l_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫ඀"), bstack11ll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸ࠲࡯࡮ࡵࡧࡵࡲࡦࡲࠧඁ")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack111l11l11_opy_
        bstack1ll11lll1_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1ll11l111l_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1lll1l11ll_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1lll111ll_opy_ + str(e))
    except Exception as e:
      bstack11llllll1_opy_(e, bstack1ll11l111l_opy_)
    if bstack1ll1ll1ll1_opy_ != bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨං"):
      bstack1l1lll1ll1_opy_()
    bstack11111l11_opy_ = Output.start_test
    bstack1llll1ll11_opy_ = Output.end_test
    bstack1111l1l1l_opy_ = TestStatus.__init__
    bstack11lll1lll_opy_ = pabot._run
    bstack1ll11lll1l_opy_ = QueueItem.__init__
    bstack1ll1l11l1l_opy_ = pabot._create_command_for_execution
    bstack1ll1l1l111_opy_ = pabot._report_results
  if bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨඃ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11llllll1_opy_(e, bstack1ll1l1111_opy_)
    bstack11llllll11_opy_ = Runner.run_hook
    bstack1l11l11ll_opy_ = Step.run
  if bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩ඄"):
    try:
      from _pytest.config import Config
      bstack1ll1llll1l_opy_ = Config.getoption
      from _pytest import runner
      bstack111l1111l_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack11l1ll1l_opy_)
    try:
      from pytest_bdd import reporting
      bstack1ll111llll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack11ll1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫඅ"))
  try:
    framework_name = bstack11ll1l_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪආ") if bstack1ll1ll1ll1_opy_ in [bstack11ll1l_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫඇ"), bstack11ll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬඈ"), bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඉ")] else bstack1ll1ll11l1_opy_(bstack1ll1ll1ll1_opy_)
    bstack11ll1l11l1_opy_ = {
      bstack11ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩඊ"): bstack11ll1l_opy_ (u"ࠩࡾ࠴ࢂ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨඋ").format(framework_name) if bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪඌ") and bstack1ll11l11ll_opy_() else framework_name,
      bstack11ll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨඍ"): bstack1l1l11l1l1_opy_(framework_name),
      bstack11ll1l_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪඎ"): __version__,
      bstack11ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧඏ"): bstack1ll1ll1ll1_opy_
    }
    if bstack1ll1ll1ll1_opy_ in bstack1l111llll1_opy_:
      if bstack1ll1l1lll1_opy_ and bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧඐ") in CONFIG and CONFIG[bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨඑ")] == True:
        if bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩඒ") in CONFIG:
          os.environ[bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫඓ")] = os.getenv(bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬඔ"), json.dumps(CONFIG[bstack11ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬඕ")]))
          CONFIG[bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ඖ")].pop(bstack11ll1l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ඗"), None)
          CONFIG[bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ඘")].pop(bstack11ll1l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ඙"), None)
        bstack11ll1l11l1_opy_[bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪක")] = {
          bstack11ll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩඛ"): bstack11ll1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧග"),
          bstack11ll1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧඝ"): str(bstack11l111lll_opy_())
        }
    if bstack1ll1ll1ll1_opy_ not in [bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨඞ")]:
      bstack111111ll_opy_ = bstack1l1llll1_opy_.launch(CONFIG, bstack11ll1l11l1_opy_)
  except Exception as e:
    logger.debug(bstack1llll1111_opy_.format(bstack11ll1l_opy_ (u"ࠨࡖࡨࡷࡹࡎࡵࡣࠩඟ"), str(e)))
  if bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩච"):
    bstack1l1l1l1l1l_opy_ = True
    if bstack1llll111ll_opy_ and bstack1lll11l1ll_opy_:
      bstack1ll1llll11_opy_ = CONFIG.get(bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧඡ"), {}).get(bstack11ll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ජ"))
      bstack11lll1l1l1_opy_(bstack1ll11ll11_opy_)
    elif bstack1llll111ll_opy_:
      bstack1ll1llll11_opy_ = CONFIG.get(bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩඣ"), {}).get(bstack11ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨඤ"))
      global bstack11l1l1l1l1_opy_
      try:
        if bstack11l1lll111_opy_(bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඥ")]) and multiprocessing.current_process().name == bstack11ll1l_opy_ (u"ࠨ࠲ࠪඦ"):
          bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬට")].remove(bstack11ll1l_opy_ (u"ࠪ࠱ࡲ࠭ඨ"))
          bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧඩ")].remove(bstack11ll1l_opy_ (u"ࠬࡶࡤࡣࠩඪ"))
          bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩණ")] = bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪඬ")][0]
          with open(bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫත")], bstack11ll1l_opy_ (u"ࠩࡵࠫථ")) as f:
            bstack11llll1lll_opy_ = f.read()
          bstack1l111111l_opy_ = bstack11ll1l_opy_ (u"ࠥࠦࠧ࡬ࡲࡰ࡯ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡶࡨࡰࠦࡩ࡮ࡲࡲࡶࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦ࠽ࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡ࡬ࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪ࠮ࡻࡾࠫ࠾ࠤ࡫ࡸ࡯࡮ࠢࡳࡨࡧࠦࡩ࡮ࡲࡲࡶࡹࠦࡐࡥࡤ࠾ࠤࡴ࡭࡟ࡥࡤࠣࡁࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮࠿ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦࡨࡪࠥࡳ࡯ࡥࡡࡥࡶࡪࡧ࡫ࠩࡵࡨࡰ࡫࠲ࠠࡢࡴࡪ࠰ࠥࡺࡥ࡮ࡲࡲࡶࡦࡸࡹࠡ࠿ࠣ࠴࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡲࡺ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡷ࡭ࠠ࠾ࠢࡶࡸࡷ࠮ࡩ࡯ࡶࠫࡥࡷ࡭ࠩࠬ࠳࠳࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡩࡽࡩࡥࡱࡶࠣࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡡࡴࠢࡨ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡴࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡱࡪࡣࡩࡨࠨࡴࡧ࡯ࡪ࠱ࡧࡲࡨ࠮ࡷࡩࡲࡶ࡯ࡳࡣࡵࡽ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡨࡧ࠴ࡤࡰࡡࡥࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣ࠰ࡧࡳࡤࡨࡲࡦࡣ࡮ࠤࡂࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡖࡤࡣࠪࠬ࠲ࡸ࡫ࡴࡠࡶࡵࡥࡨ࡫ࠨࠪ࡞ࡱࠦࠧࠨද").format(str(bstack1llll111ll_opy_))
          bstack1ll111l111_opy_ = bstack1l111111l_opy_ + bstack11llll1lll_opy_
          bstack111l1ll11_opy_ = bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧධ")] + bstack11ll1l_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡴࡦ࡯ࡳ࠲ࡵࡿࠧන")
          with open(bstack111l1ll11_opy_, bstack11ll1l_opy_ (u"࠭ࡷࠨ඲")):
            pass
          with open(bstack111l1ll11_opy_, bstack11ll1l_opy_ (u"ࠢࡸ࠭ࠥඳ")) as f:
            f.write(bstack1ll111l111_opy_)
          import subprocess
          bstack1l1ll1111_opy_ = subprocess.run([bstack11ll1l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࠣප"), bstack111l1ll11_opy_])
          if os.path.exists(bstack111l1ll11_opy_):
            os.unlink(bstack111l1ll11_opy_)
          os._exit(bstack1l1ll1111_opy_.returncode)
        else:
          if bstack11l1lll111_opy_(bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬඵ")]):
            bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭බ")].remove(bstack11ll1l_opy_ (u"ࠫ࠲ࡳࠧභ"))
            bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨම")].remove(bstack11ll1l_opy_ (u"࠭ࡰࡥࡤࠪඹ"))
            bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪය")] = bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫර")][0]
          bstack11lll1l1l1_opy_(bstack1ll11ll11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ඼")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack11ll1l_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬල")] = bstack11ll1l_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭඾")
          mod_globals[bstack11ll1l_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧ඿")] = os.path.abspath(bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩව")])
          exec(open(bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪශ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack11ll1l_opy_ (u"ࠨࡅࡤࡹ࡬࡮ࡴࠡࡇࡻࡧࡪࡶࡴࡪࡱࡱ࠾ࠥࢁࡽࠨෂ").format(str(e)))
          for driver in bstack11l1l1l1l1_opy_:
            bstack1l1l11ll11_opy_.append({
              bstack11ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧස"): bstack1llll111ll_opy_[bstack11ll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭හ")],
              bstack11ll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪළ"): str(e),
              bstack11ll1l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫෆ"): multiprocessing.current_process().name
            })
            bstack1ll1lll111_opy_(driver, bstack11ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭෇"), bstack11ll1l_opy_ (u"ࠢࡔࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡹ࡬ࡸ࡭ࡀࠠ࡝ࡰࠥ෈") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l1l1l1l1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack1llll1l1ll_opy_, CONFIG, logger)
      bstack111lll1l1_opy_()
      bstack1l1l11l1l_opy_()
      bstack111l1111_opy_ = {
        bstack11ll1l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ෉"): args[0],
        bstack11ll1l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈ්ࠩ"): CONFIG,
        bstack11ll1l_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ෋"): bstack1l1ll1l1ll_opy_,
        bstack11ll1l_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭෌"): bstack1llll1l1ll_opy_
      }
      percy.bstack1ll11l1111_opy_()
      if bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ෍") in CONFIG:
        bstack11ll1111_opy_ = []
        manager = multiprocessing.Manager()
        bstack11l11lll_opy_ = manager.list()
        if bstack11l1lll111_opy_(args):
          for index, platform in enumerate(CONFIG[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෎")]):
            if index == 0:
              bstack111l1111_opy_[bstack11ll1l_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪා")] = args
            bstack11ll1111_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack111l1111_opy_, bstack11l11lll_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫැ")]):
            bstack11ll1111_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack111l1111_opy_, bstack11l11lll_opy_)))
        for t in bstack11ll1111_opy_:
          t.start()
        for t in bstack11ll1111_opy_:
          t.join()
        bstack1ll1l1l11_opy_ = list(bstack11l11lll_opy_)
      else:
        if bstack11l1lll111_opy_(args):
          bstack111l1111_opy_[bstack11ll1l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬෑ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack111l1111_opy_,))
          test.start()
          test.join()
        else:
          bstack11lll1l1l1_opy_(bstack1ll11ll11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack11ll1l_opy_ (u"ࠪࡣࡤࡴࡡ࡮ࡧࡢࡣࠬි")] = bstack11ll1l_opy_ (u"ࠫࡤࡥ࡭ࡢ࡫ࡱࡣࡤ࠭ී")
          mod_globals[bstack11ll1l_opy_ (u"ࠬࡥ࡟ࡧ࡫࡯ࡩࡤࡥࠧු")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ෕") or bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ූ"):
    percy.init(bstack1llll1l1ll_opy_, CONFIG, logger)
    percy.bstack1ll11l1111_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11llllll1_opy_(e, bstack1ll11l111l_opy_)
    bstack111lll1l1_opy_()
    bstack11lll1l1l1_opy_(bstack1l1l1ll11l_opy_)
    if bstack1ll1l1lll1_opy_:
      bstack11ll1l1lll_opy_(bstack1l1l1ll11l_opy_, args)
      if bstack11ll1l_opy_ (u"ࠨ࠯࠰ࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭෗") in args:
        i = args.index(bstack11ll1l_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧෘ"))
        args.pop(i)
        args.pop(i)
      if bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ෙ") not in CONFIG:
        CONFIG[bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧේ")] = [{}]
        bstack1l1llll111_opy_ = 1
      if bstack1ll1ll111_opy_ == 0:
        bstack1ll1ll111_opy_ = 1
      args.insert(0, str(bstack1ll1ll111_opy_))
      args.insert(0, str(bstack11ll1l_opy_ (u"ࠬ࠳࠭ࡱࡴࡲࡧࡪࡹࡳࡦࡵࠪෛ")))
    if bstack1l1llll1_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1l11llll1_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack11lll1l11l_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack11ll1l_opy_ (u"ࠨࡒࡐࡄࡒࡘࡤࡕࡐࡕࡋࡒࡒࡘࠨො"),
        ).parse_args(bstack1l11llll1_opy_)
        bstack1l11111111_opy_ = args.index(bstack1l11llll1_opy_[0]) if len(bstack1l11llll1_opy_) > 0 else len(args)
        args.insert(bstack1l11111111_opy_, str(bstack11ll1l_opy_ (u"ࠧ࠮࠯࡯࡭ࡸࡺࡥ࡯ࡧࡵࠫෝ")))
        args.insert(bstack1l11111111_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡠࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳ࠰ࡳࡽࠬෞ"))))
        if bstack1l11lll111_opy_(os.environ.get(bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧෟ"))) and str(os.environ.get(bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࡠࡖࡈࡗ࡙࡙ࠧ෠"), bstack11ll1l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ෡"))) != bstack11ll1l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ෢"):
          for bstack1l11llll11_opy_ in bstack11lll1l11l_opy_:
            args.remove(bstack1l11llll11_opy_)
          bstack11ll111l11_opy_ = os.environ.get(bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࡣ࡙ࡋࡓࡕࡕࠪ෣")).split(bstack11ll1l_opy_ (u"ࠧ࠭ࠩ෤"))
          for bstack1l11ll111l_opy_ in bstack11ll111l11_opy_:
            args.append(bstack1l11ll111l_opy_)
      except Exception as e:
        logger.error(bstack11ll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡵࡶࡤࡧ࡭࡯࡮ࡨࠢ࡯࡭ࡸࡺࡥ࡯ࡧࡵࠤ࡫ࡵࡲࠡࡑࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࠢࡈࡶࡷࡵࡲࠡ࠯ࠣࠦ෥").format(e))
    pabot.main(args)
  elif bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴ࠮࡫ࡱࡸࡪࡸ࡮ࡢ࡮ࠪ෦"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11llllll1_opy_(e, bstack1ll11l111l_opy_)
    for a in args:
      if bstack11ll1l_opy_ (u"ࠪࡆࡘ࡚ࡁࡄࡍࡓࡐࡆ࡚ࡆࡐࡔࡐࡍࡓࡊࡅ࡙ࠩ෧") in a:
        bstack1l1lllll1_opy_ = int(a.split(bstack11ll1l_opy_ (u"ࠫ࠿࠭෨"))[1])
      if bstack11ll1l_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡉࡋࡆࡍࡑࡆࡅࡑࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ෩") in a:
        bstack1ll1llll11_opy_ = str(a.split(bstack11ll1l_opy_ (u"࠭࠺ࠨ෪"))[1])
      if bstack11ll1l_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡃࡍࡋࡄࡖࡌ࡙ࠧ෫") in a:
        bstack111ll11ll_opy_ = str(a.split(bstack11ll1l_opy_ (u"ࠨ࠼ࠪ෬"))[1])
    bstack1111ll1l1_opy_ = None
    if bstack11ll1l_opy_ (u"ࠩ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠨ෭") in args:
      i = args.index(bstack11ll1l_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ෮"))
      args.pop(i)
      bstack1111ll1l1_opy_ = args.pop(i)
    if bstack1111ll1l1_opy_ is not None:
      global bstack111llll11_opy_
      bstack111llll11_opy_ = bstack1111ll1l1_opy_
    bstack11lll1l1l1_opy_(bstack1l1l1ll11l_opy_)
    run_cli(args)
    if bstack11ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴࠨ෯") in multiprocessing.current_process().__dict__.keys():
      for bstack111l1l1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1l1l11ll11_opy_.append(bstack111l1l1ll_opy_)
  elif bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ෰"):
    percy.init(bstack1llll1l1ll_opy_, CONFIG, logger)
    percy.bstack1ll11l1111_opy_()
    bstack1l1l11lll_opy_ = bstack11l1l111_opy_(args, logger, CONFIG, bstack1ll1l1lll1_opy_)
    bstack1l1l11lll_opy_.bstack11l11l11_opy_()
    bstack111lll1l1_opy_()
    bstack11l1ll1l1l_opy_ = True
    bstack1l11ll1l11_opy_ = bstack1l1l11lll_opy_.bstack11l1l1ll_opy_()
    bstack1l1l11lll_opy_.bstack111l1111_opy_(bstack11llll11ll_opy_)
    bstack1l11111ll1_opy_ = bstack1l1l11lll_opy_.bstack111ll11l_opy_(bstack1lll1llll_opy_, {
      bstack11ll1l_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ෱"): bstack1l1ll1l1ll_opy_,
      bstack11ll1l_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩෲ"): bstack1llll1l1ll_opy_,
      bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡗࡗࡓࡒࡇࡔࡊࡑࡑࠫෳ"): bstack1ll1l1lll1_opy_
    })
    try:
      bstack11ll1l111l_opy_, bstack1l1111llll_opy_ = map(list, zip(*bstack1l11111ll1_opy_))
      bstack11ll11l11l_opy_ = bstack11ll1l111l_opy_[0]
      for status_code in bstack1l1111llll_opy_:
        if status_code != 0:
          bstack1ll111lll1_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack11ll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡡࡷࡧࠣࡩࡷࡸ࡯ࡳࡵࠣࡥࡳࡪࠠࡴࡶࡤࡸࡺࡹࠠࡤࡱࡧࡩ࠳ࠦࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࠽ࠤࢀࢃࠢ෴").format(str(e)))
  elif bstack1ll1ll1ll1_opy_ == bstack11ll1l_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ෵"):
    try:
      from behave.__main__ import main as bstack1l11l11l11_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11llllll1_opy_(e, bstack1ll1l1111_opy_)
    bstack111lll1l1_opy_()
    bstack11l1ll1l1l_opy_ = True
    bstack11l11l1l_opy_ = 1
    if bstack11ll1l_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෶") in CONFIG:
      bstack11l11l1l_opy_ = CONFIG[bstack11ll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ෷")]
    if bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෸") in CONFIG:
      bstack1ll1111ll_opy_ = int(bstack11l11l1l_opy_) * int(len(CONFIG[bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ෹")]))
    else:
      bstack1ll1111ll_opy_ = int(bstack11l11l1l_opy_)
    config = Configuration(args)
    bstack1l1l1l1ll_opy_ = config.paths
    if len(bstack1l1l1l1ll_opy_) == 0:
      import glob
      pattern = bstack11ll1l_opy_ (u"ࠨࠬ࠭࠳࠯࠴ࡦࡦࡣࡷࡹࡷ࡫ࠧ෺")
      bstack11l1111l1_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11l1111l1_opy_)
      config = Configuration(args)
      bstack1l1l1l1ll_opy_ = config.paths
    bstack111l1lll_opy_ = [os.path.normpath(item) for item in bstack1l1l1l1ll_opy_]
    bstack1lllll11l_opy_ = [os.path.normpath(item) for item in args]
    bstack1lll1lll11_opy_ = [item for item in bstack1lllll11l_opy_ if item not in bstack111l1lll_opy_]
    import platform as pf
    if pf.system().lower() == bstack11ll1l_opy_ (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪ෻"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack111l1lll_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l11ll1111_opy_)))
                    for bstack1l11ll1111_opy_ in bstack111l1lll_opy_]
    bstack11l1l1l1_opy_ = []
    for spec in bstack111l1lll_opy_:
      bstack1111llll_opy_ = []
      bstack1111llll_opy_ += bstack1lll1lll11_opy_
      bstack1111llll_opy_.append(spec)
      bstack11l1l1l1_opy_.append(bstack1111llll_opy_)
    execution_items = []
    for bstack1111llll_opy_ in bstack11l1l1l1_opy_:
      if bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෼") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ෽")]):
          item = {}
          item[bstack11ll1l_opy_ (u"ࠬࡧࡲࡨࠩ෾")] = bstack11ll1l_opy_ (u"࠭ࠠࠨ෿").join(bstack1111llll_opy_)
          item[bstack11ll1l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭฀")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack11ll1l_opy_ (u"ࠨࡣࡵ࡫ࠬก")] = bstack11ll1l_opy_ (u"ࠩࠣࠫข").join(bstack1111llll_opy_)
        item[bstack11ll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩฃ")] = 0
        execution_items.append(item)
    bstack1ll1l11lll_opy_ = bstack1ll111111l_opy_(execution_items, bstack1ll1111ll_opy_)
    for execution_item in bstack1ll1l11lll_opy_:
      bstack11ll1111_opy_ = []
      for item in execution_item:
        bstack11ll1111_opy_.append(bstack11ll1l11_opy_(name=str(item[bstack11ll1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪค")]),
                                             target=bstack111l11111_opy_,
                                             args=(item[bstack11ll1l_opy_ (u"ࠬࡧࡲࡨࠩฅ")],)))
      for t in bstack11ll1111_opy_:
        t.start()
      for t in bstack11ll1111_opy_:
        t.join()
  else:
    bstack11l1l1ll11_opy_(bstack1l111l1ll_opy_)
  if not bstack1llll111ll_opy_:
    bstack1111lllll_opy_()
  bstack1l1ll1ll11_opy_.bstack11l1ll1l1_opy_()
def browserstack_initialize(bstack1lll1ll11l_opy_=None):
  run_on_browserstack(bstack1lll1ll11l_opy_, None, True)
def bstack1111lllll_opy_():
  global CONFIG
  global bstack1l1l1l11ll_opy_
  global bstack1ll111lll1_opy_
  global bstack1l11111l1l_opy_
  global bstack11l111ll_opy_
  bstack1l1llll1_opy_.stop()
  bstack1lll11ll_opy_.bstack1ll11l11l_opy_()
  [bstack1lll1ll111_opy_, bstack1l111l1l11_opy_] = get_build_link()
  if bstack1lll1ll111_opy_ is not None and bstack11lllll1l1_opy_() != -1:
    sessions = bstack11l1l1l1l_opy_(bstack1lll1ll111_opy_)
    bstack1lllll111l_opy_(sessions, bstack1l111l1l11_opy_)
  if bstack1l1l1l11ll_opy_ == bstack11ll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ฆ") and bstack1ll111lll1_opy_ != 0:
    sys.exit(bstack1ll111lll1_opy_)
  if bstack1l1l1l11ll_opy_ == bstack11ll1l_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧง") and bstack1l11111l1l_opy_ != 0:
    sys.exit(bstack1l11111l1l_opy_)
def bstack1ll1ll11l1_opy_(bstack1l11l1ll1l_opy_):
  if bstack1l11l1ll1l_opy_:
    return bstack1l11l1ll1l_opy_.capitalize()
  else:
    return bstack11ll1l_opy_ (u"ࠨࠩจ")
def bstack1llllllll_opy_(bstack111l11ll1_opy_):
  if bstack11ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧฉ") in bstack111l11ll1_opy_ and bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨช")] != bstack11ll1l_opy_ (u"ࠫࠬซ"):
    return bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪฌ")]
  else:
    bstack11llll111l_opy_ = bstack11ll1l_opy_ (u"ࠨࠢญ")
    if bstack11ll1l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧฎ") in bstack111l11ll1_opy_ and bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨฏ")] != None:
      bstack11llll111l_opy_ += bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩฐ")] + bstack11ll1l_opy_ (u"ࠥ࠰ࠥࠨฑ")
      if bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠫࡴࡹࠧฒ")] == bstack11ll1l_opy_ (u"ࠧ࡯࡯ࡴࠤณ"):
        bstack11llll111l_opy_ += bstack11ll1l_opy_ (u"ࠨࡩࡐࡕࠣࠦด")
      bstack11llll111l_opy_ += (bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫต")] or bstack11ll1l_opy_ (u"ࠨࠩถ"))
      return bstack11llll111l_opy_
    else:
      bstack11llll111l_opy_ += bstack1ll1ll11l1_opy_(bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪท")]) + bstack11ll1l_opy_ (u"ࠥࠤࠧธ") + (
              bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭น")] or bstack11ll1l_opy_ (u"ࠬ࠭บ")) + bstack11ll1l_opy_ (u"ࠨࠬࠡࠤป")
      if bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠧࡰࡵࠪผ")] == bstack11ll1l_opy_ (u"࡙ࠣ࡬ࡲࡩࡵࡷࡴࠤฝ"):
        bstack11llll111l_opy_ += bstack11ll1l_opy_ (u"ࠤ࡚࡭ࡳࠦࠢพ")
      bstack11llll111l_opy_ += bstack111l11ll1_opy_[bstack11ll1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧฟ")] or bstack11ll1l_opy_ (u"ࠫࠬภ")
      return bstack11llll111l_opy_
def bstack1lll1l111_opy_(bstack11lll1l1ll_opy_):
  if bstack11lll1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠧࡪ࡯࡯ࡧࠥม"):
    return bstack11ll1l_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡩࡵࡩࡪࡴ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡩࡵࡩࡪࡴࠢ࠿ࡅࡲࡱࡵࡲࡥࡵࡧࡧࡀ࠴࡬࡯࡯ࡶࡁࡀ࠴ࡺࡤ࠿ࠩย")
  elif bstack11lll1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢร"):
    return bstack11ll1l_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࡶࡪࡪ࠻ࠣࡀ࠿ࡪࡴࡴࡴࠡࡥࡲࡰࡴࡸ࠽ࠣࡴࡨࡨࠧࡄࡆࡢ࡫࡯ࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫฤ")
  elif bstack11lll1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤล"):
    return bstack11ll1l_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿࡭ࡲࡦࡧࡱ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧ࡭ࡲࡦࡧࡱࠦࡃࡖࡡࡴࡵࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪฦ")
  elif bstack11lll1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠦࡪࡸࡲࡰࡴࠥว"):
    return bstack11ll1l_opy_ (u"ࠬࡂࡴࡥࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡳࡧࡧ࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡸࡥࡥࠤࡁࡉࡷࡸ࡯ࡳ࠾࠲ࡪࡴࡴࡴ࠿࠾࠲ࡸࡩࡄࠧศ")
  elif bstack11lll1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠨࡴࡪ࡯ࡨࡳࡺࡺࠢษ"):
    return bstack11ll1l_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡩࡪࡧ࠳࠳࠸࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࠨ࡫ࡥࡢ࠵࠵࠺ࠧࡄࡔࡪ࡯ࡨࡳࡺࡺ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬส")
  elif bstack11lll1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠤห"):
    return bstack11ll1l_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡧࡲࡡࡤ࡭࠾ࠦࡃࡂࡦࡰࡰࡷࠤࡨࡵ࡬ࡰࡴࡀࠦࡧࡲࡡࡤ࡭ࠥࡂࡗࡻ࡮࡯࡫ࡱ࡫ࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪฬ")
  else:
    return bstack11ll1l_opy_ (u"ࠪࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡢ࡭ࡣࡦ࡯ࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡢ࡭ࡣࡦ࡯ࠧࡄࠧอ") + bstack1ll1ll11l1_opy_(
      bstack11lll1l1ll_opy_) + bstack11ll1l_opy_ (u"ࠫࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪฮ")
def bstack1l1111l1l_opy_(session):
  return bstack11ll1l_opy_ (u"ࠬࡂࡴࡳࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡵࡳࡼࠨ࠾࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠢࡶࡩࡸࡹࡩࡰࡰ࠰ࡲࡦࡳࡥࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦࢀࢃࠢࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࡁࡿࢂࡂ࠯ࡢࡀ࠿࠳ࡹࡪ࠾ࡼࡿࡾࢁࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢ࠿ࡽࢀࡀ࠴ࡺࡤ࠿࠾ࡷࡨࠥࡧ࡬ࡪࡩࡱࡁࠧࡩࡥ࡯ࡶࡨࡶࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࡃࢁࡽ࠽࠱ࡷࡨࡃࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼࠰ࡶࡵࡂࠬฯ").format(
    session[bstack11ll1l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪะ")], bstack1llllllll_opy_(session), bstack1lll1l111_opy_(session[bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡳࡵࡣࡷࡹࡸ࠭ั")]),
    bstack1lll1l111_opy_(session[bstack11ll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨา")]),
    bstack1ll1ll11l1_opy_(session[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪำ")] or session[bstack11ll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪิ")] or bstack11ll1l_opy_ (u"ࠫࠬี")) + bstack11ll1l_opy_ (u"ࠧࠦࠢึ") + (session[bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨื")] or bstack11ll1l_opy_ (u"ࠧࠨุ")),
    session[bstack11ll1l_opy_ (u"ࠨࡱࡶูࠫ")] + bstack11ll1l_opy_ (u"ࠤฺࠣࠦ") + session[bstack11ll1l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ฻")], session[bstack11ll1l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭฼")] or bstack11ll1l_opy_ (u"ࠬ࠭฽"),
    session[bstack11ll1l_opy_ (u"࠭ࡣࡳࡧࡤࡸࡪࡪ࡟ࡢࡶࠪ฾")] if session[bstack11ll1l_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫ฿")] else bstack11ll1l_opy_ (u"ࠨࠩเ"))
def bstack1lllll111l_opy_(sessions, bstack1l111l1l11_opy_):
  try:
    bstack11lll111ll_opy_ = bstack11ll1l_opy_ (u"ࠤࠥแ")
    if not os.path.exists(bstack111l1lll1_opy_):
      os.mkdir(bstack111l1lll1_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11ll1l_opy_ (u"ࠪࡥࡸࡹࡥࡵࡵ࠲ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨโ")), bstack11ll1l_opy_ (u"ࠫࡷ࠭ใ")) as f:
      bstack11lll111ll_opy_ = f.read()
    bstack11lll111ll_opy_ = bstack11lll111ll_opy_.replace(bstack11ll1l_opy_ (u"ࠬࢁࠥࡓࡇࡖ࡙ࡑ࡚ࡓࡠࡅࡒ࡙ࡓ࡚ࠥࡾࠩไ"), str(len(sessions)))
    bstack11lll111ll_opy_ = bstack11lll111ll_opy_.replace(bstack11ll1l_opy_ (u"࠭ࡻࠦࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠩࢂ࠭ๅ"), bstack1l111l1l11_opy_)
    bstack11lll111ll_opy_ = bstack11lll111ll_opy_.replace(bstack11ll1l_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡐࡄࡑࡊࠫࡽࠨๆ"),
                                              sessions[0].get(bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟࡯ࡣࡰࡩࠬ็")) if sessions[0] else bstack11ll1l_opy_ (u"่ࠩࠪ"))
    with open(os.path.join(bstack111l1lll1_opy_, bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠯ࡵࡩࡵࡵࡲࡵ࠰࡫ࡸࡲࡲ้ࠧ")), bstack11ll1l_opy_ (u"ࠫࡼ๊࠭")) as stream:
      stream.write(bstack11lll111ll_opy_.split(bstack11ll1l_opy_ (u"ࠬࢁࠥࡔࡇࡖࡗࡎࡕࡎࡔࡡࡇࡅ࡙ࡇࠥࡾ๋ࠩ"))[0])
      for session in sessions:
        stream.write(bstack1l1111l1l_opy_(session))
      stream.write(bstack11lll111ll_opy_.split(bstack11ll1l_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪ์"))[1])
    logger.info(bstack11ll1l_opy_ (u"ࠧࡈࡧࡱࡩࡷࡧࡴࡦࡦࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡥࡹ࡮ࡲࡤࠡࡣࡵࡸ࡮࡬ࡡࡤࡶࡶࠤࡦࡺࠠࡼࡿࠪํ").format(bstack111l1lll1_opy_));
  except Exception as e:
    logger.debug(bstack1lll11llll_opy_.format(str(e)))
def bstack11l1l1l1l_opy_(bstack1lll1ll111_opy_):
  global CONFIG
  try:
    host = bstack11ll1l_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫ๎") if bstack11ll1l_opy_ (u"ࠩࡤࡴࡵ࠭๏") in CONFIG else bstack11ll1l_opy_ (u"ࠪࡥࡵ࡯ࠧ๐")
    user = CONFIG[bstack11ll1l_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭๑")]
    key = CONFIG[bstack11ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ๒")]
    bstack11l1ll11l1_opy_ = bstack11ll1l_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ๓") if bstack11ll1l_opy_ (u"ࠧࡢࡲࡳࠫ๔") in CONFIG else bstack11ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ๕")
    url = bstack11ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡧࡶࡷ࡮ࡵ࡮ࡴ࠰࡭ࡷࡴࡴࠧ๖").format(user, key, host, bstack11l1ll11l1_opy_,
                                                                                bstack1lll1ll111_opy_)
    headers = {
      bstack11ll1l_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ๗"): bstack11ll1l_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ๘"),
    }
    proxies = bstack111ll1l11_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack11ll1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡶࡩࡸࡹࡩࡰࡰࠪ๙")], response.json()))
  except Exception as e:
    logger.debug(bstack1l11l1l1l_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack1ll11ll111_opy_
  try:
    if bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๚") in CONFIG:
      host = bstack11ll1l_opy_ (u"ࠧࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦࠪ๛") if bstack11ll1l_opy_ (u"ࠨࡣࡳࡴࠬ๜") in CONFIG else bstack11ll1l_opy_ (u"ࠩࡤࡴ࡮࠭๝")
      user = CONFIG[bstack11ll1l_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬ๞")]
      key = CONFIG[bstack11ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ๟")]
      bstack11l1ll11l1_opy_ = bstack11ll1l_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ๠") if bstack11ll1l_opy_ (u"࠭ࡡࡱࡲࠪ๡") in CONFIG else bstack11ll1l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ๢")
      url = bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡾࢁ࠿ࢁࡽࡁࡽࢀ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡼࡿ࠲ࡦࡺ࡯࡬ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ๣").format(user, key, host, bstack11l1ll11l1_opy_)
      headers = {
        bstack11ll1l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨ๤"): bstack11ll1l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭๥"),
      }
      if bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๦") in CONFIG:
        params = {bstack11ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ๧"): CONFIG[bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ๨")], bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๩"): CONFIG[bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ๪")]}
      else:
        params = {bstack11ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ๫"): CONFIG[bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭๬")]}
      proxies = bstack111ll1l11_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1111l11l_opy_ = response.json()[0][bstack11ll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡤࡸ࡭ࡱࡪࠧ๭")]
        if bstack1111l11l_opy_:
          bstack1l111l1l11_opy_ = bstack1111l11l_opy_[bstack11ll1l_opy_ (u"ࠬࡶࡵࡣ࡮࡬ࡧࡤࡻࡲ࡭ࠩ๮")].split(bstack11ll1l_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨ࠳ࡢࡶ࡫࡯ࡨࠬ๯"))[0] + bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡹ࠯ࠨ๰") + bstack1111l11l_opy_[
            bstack11ll1l_opy_ (u"ࠨࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ๱")]
          logger.info(bstack1l11l11l1l_opy_.format(bstack1l111l1l11_opy_))
          bstack1ll11ll111_opy_ = bstack1111l11l_opy_[bstack11ll1l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๲")]
          bstack11l1l11l1_opy_ = CONFIG[bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭๳")]
          if bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭๴") in CONFIG:
            bstack11l1l11l1_opy_ += bstack11ll1l_opy_ (u"ࠬࠦࠧ๵") + CONFIG[bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ๶")]
          if bstack11l1l11l1_opy_ != bstack1111l11l_opy_[bstack11ll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ๷")]:
            logger.debug(bstack11ll11111_opy_.format(bstack1111l11l_opy_[bstack11ll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭๸")], bstack11l1l11l1_opy_))
          return [bstack1111l11l_opy_[bstack11ll1l_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ๹")], bstack1l111l1l11_opy_]
    else:
      logger.warn(bstack1l1111l1ll_opy_)
  except Exception as e:
    logger.debug(bstack111l1llll_opy_.format(str(e)))
  return [None, None]
def bstack1lll1l1l1l_opy_(url, bstack111111lll_opy_=False):
  global CONFIG
  global bstack1lll1l1l1_opy_
  if not bstack1lll1l1l1_opy_:
    hostname = bstack1l1l11l1ll_opy_(url)
    is_private = bstack1l11l111l_opy_(hostname)
    if (bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧ๺") in CONFIG and not bstack1l11lll111_opy_(CONFIG[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨ๻")])) and (is_private or bstack111111lll_opy_):
      bstack1lll1l1l1_opy_ = hostname
def bstack1l1l11l1ll_opy_(url):
  return urlparse(url).hostname
def bstack1l11l111l_opy_(hostname):
  for bstack1ll1lllll_opy_ in bstack1l11l11111_opy_:
    regex = re.compile(bstack1ll1lllll_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack111l1ll1l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack1l1lllll1_opy_
  bstack1llll11l11_opy_ = not (bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ๼"), None) and bstack1ll11111_opy_(
          threading.current_thread(), bstack11ll1l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ๽"), None))
  bstack1l1l11111_opy_ = getattr(driver, bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ๾"), None) != True
  if not bstack111lll1l_opy_.bstack1lll1lllll_opy_(CONFIG, bstack1l1lllll1_opy_) or (bstack1l1l11111_opy_ and bstack1llll11l11_opy_):
    logger.warning(bstack11ll1l_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵ࠱ࠦ๿"))
    return {}
  try:
    logger.debug(bstack11ll1l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭຀"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack11ll1ll1l_opy_.bstack1l1l1lllll_opy_)
    return results
  except Exception:
    logger.error(bstack11ll1l_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡸࡧࡵࡩࠥ࡬࡯ࡶࡰࡧ࠲ࠧກ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack1l1lllll1_opy_
  bstack1llll11l11_opy_ = not (bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨຂ"), None) and bstack1ll11111_opy_(
          threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ຃"), None))
  bstack1l1l11111_opy_ = getattr(driver, bstack11ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ຄ"), None) != True
  if not bstack111lll1l_opy_.bstack1lll1lllll_opy_(CONFIG, bstack1l1lllll1_opy_) or (bstack1l1l11111_opy_ and bstack1llll11l11_opy_):
    logger.warning(bstack11ll1l_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡶࡹࡲࡳࡡࡳࡻ࠱ࠦ຅"))
    return {}
  try:
    logger.debug(bstack11ll1l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡹࡵ࡮࡯ࡤࡶࡾ࠭ຆ"))
    logger.debug(perform_scan(driver))
    bstack11ll1111ll_opy_ = driver.execute_async_script(bstack11ll1ll1l_opy_.bstack1ll1l11ll_opy_)
    return bstack11ll1111ll_opy_
  except Exception:
    logger.error(bstack11ll1l_opy_ (u"ࠤࡑࡳࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡵ࡮࡯ࡤࡶࡾࠦࡷࡢࡵࠣࡪࡴࡻ࡮ࡥ࠰ࠥງ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack1l1lllll1_opy_
  bstack1llll11l11_opy_ = not (bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧຈ"), None) and bstack1ll11111_opy_(
          threading.current_thread(), bstack11ll1l_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪຉ"), None))
  bstack1l1l11111_opy_ = getattr(driver, bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬຊ"), None) != True
  if not bstack111lll1l_opy_.bstack1lll1lllll_opy_(CONFIG, bstack1l1lllll1_opy_) or (bstack1l1l11111_opy_ and bstack1llll11l11_opy_):
    logger.warning(bstack11ll1l_opy_ (u"ࠨࡎࡰࡶࠣࡥࡳࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡩࡡ࡯ࡰࡲࡸࠥࡸࡵ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࠮ࠣ຋"))
    return {}
  try:
    bstack11l111ll1_opy_ = driver.execute_async_script(bstack11ll1ll1l_opy_.perform_scan, {bstack11ll1l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧຌ"): kwargs.get(bstack11ll1l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡲࡱࡲࡧ࡮ࡥࠩຍ"), None) or bstack11ll1l_opy_ (u"ࠩࠪຎ")})
    return bstack11l111ll1_opy_
  except Exception:
    logger.error(bstack11ll1l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤຏ"))
    return {}