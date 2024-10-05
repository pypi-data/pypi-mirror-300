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
import sys
import logging
import tarfile
import io
import os
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack111ll11l11_opy_, bstack111ll111ll_opy_
import tempfile
import json
bstack1lllll1lll1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡥࡧࡥࡹ࡬࠴࡬ࡰࡩࠪᓬ"))
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11ll1l_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᓭ"),
      datefmt=bstack11ll1l_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᓮ"),
      stream=sys.stdout
    )
  return logger
def bstack1lllll1l1l1_opy_():
  global bstack1lllll1lll1_opy_
  if os.path.exists(bstack1lllll1lll1_opy_):
    os.remove(bstack1lllll1lll1_opy_)
def bstack11l1ll1l1_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack11l1l1l1ll_opy_(config, log_level):
  bstack1lllll11l11_opy_ = log_level
  if bstack11ll1l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᓯ") in config and config[bstack11ll1l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᓰ")] in bstack111ll11l11_opy_:
    bstack1lllll11l11_opy_ = bstack111ll11l11_opy_[config[bstack11ll1l_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᓱ")]]
  if config.get(bstack11ll1l_opy_ (u"ࠧࡥ࡫ࡶࡥࡧࡲࡥࡂࡷࡷࡳࡈࡧࡰࡵࡷࡵࡩࡑࡵࡧࡴࠩᓲ"), False):
    logging.getLogger().setLevel(bstack1lllll11l11_opy_)
    return bstack1lllll11l11_opy_
  global bstack1lllll1lll1_opy_
  bstack11l1ll1l1_opy_()
  bstack1lllll1llll_opy_ = logging.Formatter(
    fmt=bstack11ll1l_opy_ (u"ࠨ࡞ࡱࠩ࠭ࡧࡳࡤࡶ࡬ࡱࡪ࠯ࡳࠡ࡝ࠨࠬࡳࡧ࡭ࡦࠫࡶࡡࡠࠫࠨ࡭ࡧࡹࡩࡱࡴࡡ࡮ࡧࠬࡷࡢࠦ࠭ࠡࠧࠫࡱࡪࡹࡳࡢࡩࡨ࠭ࡸ࠭ᓳ"),
    datefmt=bstack11ll1l_opy_ (u"ࠩࠨࡌ࠿ࠫࡍ࠻ࠧࡖࠫᓴ")
  )
  bstack1lllll11l1l_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack1lllll1lll1_opy_)
  file_handler.setFormatter(bstack1lllll1llll_opy_)
  bstack1lllll11l1l_opy_.setFormatter(bstack1lllll1llll_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack1lllll11l1l_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11ll1l_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲ࠯ࡴࡨࡱࡴࡺࡥ࠯ࡴࡨࡱࡴࡺࡥࡠࡥࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲࠬᓵ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack1lllll11l1l_opy_.setLevel(bstack1lllll11l11_opy_)
  logging.getLogger().addHandler(bstack1lllll11l1l_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack1lllll11l11_opy_
def bstack1lllll111ll_opy_(config):
  try:
    bstack1lllll1ll1l_opy_ = set(bstack111ll111ll_opy_)
    bstack1lllll1ll11_opy_ = bstack11ll1l_opy_ (u"ࠫࠬᓶ")
    with open(bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᓷ")) as bstack1lllll11lll_opy_:
      bstack1lllll1l1ll_opy_ = bstack1lllll11lll_opy_.read()
      bstack1lllll1ll11_opy_ = re.sub(bstack11ll1l_opy_ (u"ࡸࠧ࡟ࠪ࡟ࡷ࠰࠯࠿ࠤ࠰࠭ࠨࡡࡴࠧᓸ"), bstack11ll1l_opy_ (u"ࠧࠨᓹ"), bstack1lllll1l1ll_opy_, flags=re.M)
      bstack1lllll1ll11_opy_ = re.sub(
        bstack11ll1l_opy_ (u"ࡳࠩࡡࠬࡡࡹࠫࠪࡁࠫࠫᓺ") + bstack11ll1l_opy_ (u"ࠩࡿࠫᓻ").join(bstack1lllll1ll1l_opy_) + bstack11ll1l_opy_ (u"ࠪ࠭࠳࠰ࠤࠨᓼ"),
        bstack11ll1l_opy_ (u"ࡶࠬࡢ࠲࠻ࠢ࡞ࡖࡊࡊࡁࡄࡖࡈࡈࡢ࠭ᓽ"),
        bstack1lllll1ll11_opy_, flags=re.M | re.I
      )
    def bstack1llllll1111_opy_(dic):
      bstack1lllll1l111_opy_ = {}
      for key, value in dic.items():
        if key in bstack1lllll1ll1l_opy_:
          bstack1lllll1l111_opy_[key] = bstack11ll1l_opy_ (u"ࠬࡡࡒࡆࡆࡄࡇ࡙ࡋࡄ࡞ࠩᓾ")
        else:
          if isinstance(value, dict):
            bstack1lllll1l111_opy_[key] = bstack1llllll1111_opy_(value)
          else:
            bstack1lllll1l111_opy_[key] = value
      return bstack1lllll1l111_opy_
    bstack1lllll1l111_opy_ = bstack1llllll1111_opy_(config)
    return {
      bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩᓿ"): bstack1lllll1ll11_opy_,
      bstack11ll1l_opy_ (u"ࠧࡧ࡫ࡱࡥࡱࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᔀ"): json.dumps(bstack1lllll1l111_opy_)
    }
  except Exception as e:
    return {}
def bstack1ll11l11_opy_(config):
  global bstack1lllll1lll1_opy_
  try:
    if config.get(bstack11ll1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᔁ"), False):
      return
    uuid = os.getenv(bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᔂ"))
    if not uuid or uuid == bstack11ll1l_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᔃ"):
      return
    bstack1lllll11ll1_opy_ = [bstack11ll1l_opy_ (u"ࠫࡷ࡫ࡱࡶ࡫ࡵࡩࡲ࡫࡮ࡵࡵ࠱ࡸࡽࡺࠧᔄ"), bstack11ll1l_opy_ (u"ࠬࡖࡩࡱࡨ࡬ࡰࡪ࠭ᔅ"), bstack11ll1l_opy_ (u"࠭ࡰࡺࡲࡵࡳ࡯࡫ࡣࡵ࠰ࡷࡳࡲࡲࠧᔆ"), bstack1lllll1lll1_opy_]
    bstack11l1ll1l1_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠭࡭ࡱࡪࡷ࠲࠭ᔇ") + uuid + bstack11ll1l_opy_ (u"ࠨ࠰ࡷࡥࡷ࠴ࡧࡻࠩᔈ"))
    with tarfile.open(output_file, bstack11ll1l_opy_ (u"ࠤࡺ࠾࡬ࢀࠢᔉ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack1lllll11ll1_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack1lllll111ll_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack1lllll1l11l_opy_ = data.encode()
        tarinfo.size = len(bstack1lllll1l11l_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack1lllll1l11l_opy_))
    bstack1111111l1_opy_ = MultipartEncoder(
      fields= {
        bstack11ll1l_opy_ (u"ࠪࡨࡦࡺࡡࠨᔊ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11ll1l_opy_ (u"ࠫࡷࡨࠧᔋ")), bstack11ll1l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࠲࡭ࡺࡪࡲࠪᔌ")),
        bstack11ll1l_opy_ (u"࠭ࡣ࡭࡫ࡨࡲࡹࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᔍ"): uuid
      }
    )
    response = requests.post(
      bstack11ll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࡷࡳࡰࡴࡧࡤ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡨࡲࡩࡦࡰࡷ࠱ࡱࡵࡧࡴ࠱ࡸࡴࡱࡵࡡࡥࠤᔎ"),
      data=bstack1111111l1_opy_,
      headers={bstack11ll1l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᔏ"): bstack1111111l1_opy_.content_type},
      auth=(config[bstack11ll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫᔐ")], config[bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ᔑ")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11ll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡹࡵࡲ࡯ࡢࡦࠣࡰࡴ࡭ࡳ࠻ࠢࠪᔒ") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫࡮ࡥ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵ࠽ࠫᔓ") + str(e))
  finally:
    try:
      bstack1lllll1l1l1_opy_()
    except:
      pass