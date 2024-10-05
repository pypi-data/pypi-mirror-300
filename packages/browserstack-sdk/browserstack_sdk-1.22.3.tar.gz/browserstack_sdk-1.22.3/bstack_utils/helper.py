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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111l1ll1l1_opy_, bstack1l11l11111_opy_, bstack1lll11ll11_opy_, bstack11ll1l1l1_opy_,
                                    bstack111l1l1lll_opy_, bstack111l1l1l1l_opy_, bstack111ll111ll_opy_, bstack111ll1111l_opy_)
from bstack_utils.messages import bstack1l1111111_opy_, bstack11lll1l1l_opy_
from bstack_utils.proxy import bstack111ll1l11_opy_, bstack1lll1l1lll_opy_
bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
logger = logging.getLogger(__name__)
def bstack11l111l1l1_opy_(config):
    return config[bstack11ll1l_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨዹ")]
def bstack11l1111111_opy_(config):
    return config[bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪዺ")]
def bstack1ll1ll1l1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack1111ll1l11_opy_(obj):
    values = []
    bstack111l1l11l1_opy_ = re.compile(bstack11ll1l_opy_ (u"ࡳࠤࡡࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࡝ࡦ࠮ࠨࠧዻ"), re.I)
    for key in obj.keys():
        if bstack111l1l11l1_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111llll11_opy_(config):
    tags = []
    tags.extend(bstack1111ll1l11_opy_(os.environ))
    tags.extend(bstack1111ll1l11_opy_(config))
    return tags
def bstack1111111lll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111llll1l_opy_(bstack111l1l1l11_opy_):
    if not bstack111l1l1l11_opy_:
        return bstack11ll1l_opy_ (u"ࠩࠪዼ")
    return bstack11ll1l_opy_ (u"ࠥࡿࢂࠦࠨࡼࡿࠬࠦዽ").format(bstack111l1l1l11_opy_.name, bstack111l1l1l11_opy_.email)
def bstack111llll1ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11111l1111_opy_ = repo.common_dir
        info = {
            bstack11ll1l_opy_ (u"ࠦࡸ࡮ࡡࠣዾ"): repo.head.commit.hexsha,
            bstack11ll1l_opy_ (u"ࠧࡹࡨࡰࡴࡷࡣࡸ࡮ࡡࠣዿ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11ll1l_opy_ (u"ࠨࡢࡳࡣࡱࡧ࡭ࠨጀ"): repo.active_branch.name,
            bstack11ll1l_opy_ (u"ࠢࡵࡣࡪࠦጁ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11ll1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࠦጂ"): bstack1111llll1l_opy_(repo.head.commit.committer),
            bstack11ll1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࡤࡪࡡࡵࡧࠥጃ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11ll1l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࠥጄ"): bstack1111llll1l_opy_(repo.head.commit.author),
            bstack11ll1l_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࡣࡩࡧࡴࡦࠤጅ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11ll1l_opy_ (u"ࠧࡩ࡯࡮࡯࡬ࡸࡤࡳࡥࡴࡵࡤ࡫ࡪࠨጆ"): repo.head.commit.message,
            bstack11ll1l_opy_ (u"ࠨࡲࡰࡱࡷࠦጇ"): repo.git.rev_parse(bstack11ll1l_opy_ (u"ࠢ࠮࠯ࡶ࡬ࡴࡽ࠭ࡵࡱࡳࡰࡪࡼࡥ࡭ࠤገ")),
            bstack11ll1l_opy_ (u"ࠣࡥࡲࡱࡲࡵ࡮ࡠࡩ࡬ࡸࡤࡪࡩࡳࠤጉ"): bstack11111l1111_opy_,
            bstack11ll1l_opy_ (u"ࠤࡺࡳࡷࡱࡴࡳࡧࡨࡣ࡬࡯ࡴࡠࡦ࡬ࡶࠧጊ"): subprocess.check_output([bstack11ll1l_opy_ (u"ࠥ࡫࡮ࡺࠢጋ"), bstack11ll1l_opy_ (u"ࠦࡷ࡫ࡶ࠮ࡲࡤࡶࡸ࡫ࠢጌ"), bstack11ll1l_opy_ (u"ࠧ࠳࠭ࡨ࡫ࡷ࠱ࡨࡵ࡭࡮ࡱࡱ࠱ࡩ࡯ࡲࠣግ")]).strip().decode(
                bstack11ll1l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬጎ")),
            bstack11ll1l_opy_ (u"ࠢ࡭ࡣࡶࡸࡤࡺࡡࡨࠤጏ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11ll1l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡴࡡࡶ࡭ࡳࡩࡥࡠ࡮ࡤࡷࡹࡥࡴࡢࡩࠥጐ"): repo.git.rev_list(
                bstack11ll1l_opy_ (u"ࠤࡾࢁ࠳࠴ࡻࡾࠤ጑").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11111ll1ll_opy_ = []
        for remote in remotes:
            bstack111l11l11l_opy_ = {
                bstack11ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣጒ"): remote.name,
                bstack11ll1l_opy_ (u"ࠦࡺࡸ࡬ࠣጓ"): remote.url,
            }
            bstack11111ll1ll_opy_.append(bstack111l11l11l_opy_)
        bstack11111111ll_opy_ = {
            bstack11ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥጔ"): bstack11ll1l_opy_ (u"ࠨࡧࡪࡶࠥጕ"),
            **info,
            bstack11ll1l_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫ࡳࠣ጖"): bstack11111ll1ll_opy_
        }
        bstack11111111ll_opy_ = bstack111l11l111_opy_(bstack11111111ll_opy_)
        return bstack11111111ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11ll1l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡱࡳࡹࡱࡧࡴࡪࡰࡪࠤࡌ࡯ࡴࠡ࡯ࡨࡸࡦࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࢀࠦ጗").format(err))
        return {}
def bstack111l11l111_opy_(bstack11111111ll_opy_):
    bstack1111l11lll_opy_ = bstack1111l11l11_opy_(bstack11111111ll_opy_)
    if bstack1111l11lll_opy_ and bstack1111l11lll_opy_ > bstack111l1l1lll_opy_:
        bstack111111l1l1_opy_ = bstack1111l11lll_opy_ - bstack111l1l1lll_opy_
        bstack111111ll1l_opy_ = bstack111l11llll_opy_(bstack11111111ll_opy_[bstack11ll1l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥጘ")], bstack111111l1l1_opy_)
        bstack11111111ll_opy_[bstack11ll1l_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦጙ")] = bstack111111ll1l_opy_
        logger.info(bstack11ll1l_opy_ (u"࡙ࠦ࡮ࡥࠡࡥࡲࡱࡲ࡯ࡴࠡࡪࡤࡷࠥࡨࡥࡦࡰࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩ࠴ࠠࡔ࡫ࡽࡩࠥࡵࡦࠡࡥࡲࡱࡲ࡯ࡴࠡࡣࡩࡸࡪࡸࠠࡵࡴࡸࡲࡨࡧࡴࡪࡱࡱࠤ࡮ࡹࠠࡼࡿࠣࡏࡇࠨጚ")
                    .format(bstack1111l11l11_opy_(bstack11111111ll_opy_) / 1024))
    return bstack11111111ll_opy_
def bstack1111l11l11_opy_(bstack1l111lllll_opy_):
    try:
        if bstack1l111lllll_opy_:
            bstack1111l1ll11_opy_ = json.dumps(bstack1l111lllll_opy_)
            bstack111l111l11_opy_ = sys.getsizeof(bstack1111l1ll11_opy_)
            return bstack111l111l11_opy_
    except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"࡙ࠧ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡨࡪ࡮ࡨࠤࡨࡧ࡬ࡤࡷ࡯ࡥࡹ࡯࡮ࡨࠢࡶ࡭ࡿ࡫ࠠࡰࡨࠣࡎࡘࡕࡎࠡࡱࡥ࡮ࡪࡩࡴ࠻ࠢࡾࢁࠧጛ").format(e))
    return -1
def bstack111l11llll_opy_(field, bstack1111ll1l1l_opy_):
    try:
        bstack11111l1lll_opy_ = len(bytes(bstack111l1l1l1l_opy_, bstack11ll1l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬጜ")))
        bstack11111ll1l1_opy_ = bytes(field, bstack11ll1l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ጝ"))
        bstack111l111ll1_opy_ = len(bstack11111ll1l1_opy_)
        bstack1111l11111_opy_ = ceil(bstack111l111ll1_opy_ - bstack1111ll1l1l_opy_ - bstack11111l1lll_opy_)
        if bstack1111l11111_opy_ > 0:
            bstack1111111l1l_opy_ = bstack11111ll1l1_opy_[:bstack1111l11111_opy_].decode(bstack11ll1l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧጞ"), errors=bstack11ll1l_opy_ (u"ࠩ࡬࡫ࡳࡵࡲࡦࠩጟ")) + bstack111l1l1l1l_opy_
            return bstack1111111l1l_opy_
    except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡱ࡫ࠥ࡬ࡩࡦ࡮ࡧ࠰ࠥࡴ࡯ࡵࡪ࡬ࡲ࡬ࠦࡷࡢࡵࠣࡸࡷࡻ࡮ࡤࡣࡷࡩࡩࠦࡨࡦࡴࡨ࠾ࠥࢁࡽࠣጠ").format(e))
    return field
def bstack11ll111ll_opy_():
    env = os.environ
    if (bstack11ll1l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤጡ") in env and len(env[bstack11ll1l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥጢ")]) > 0) or (
            bstack11ll1l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧጣ") in env and len(env[bstack11ll1l_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨጤ")]) > 0):
        return {
            bstack11ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨጥ"): bstack11ll1l_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥጦ"),
            bstack11ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨጧ"): env.get(bstack11ll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢጨ")),
            bstack11ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢጩ"): env.get(bstack11ll1l_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣጪ")),
            bstack11ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨጫ"): env.get(bstack11ll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢጬ"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠤࡆࡍࠧጭ")) == bstack11ll1l_opy_ (u"ࠥࡸࡷࡻࡥࠣጮ") and bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨጯ"))):
        return {
            bstack11ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥጰ"): bstack11ll1l_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣጱ"),
            bstack11ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥጲ"): env.get(bstack11ll1l_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦጳ")),
            bstack11ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦጴ"): env.get(bstack11ll1l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢጵ")),
            bstack11ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥጶ"): env.get(bstack11ll1l_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣጷ"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠨࡃࡊࠤጸ")) == bstack11ll1l_opy_ (u"ࠢࡵࡴࡸࡩࠧጹ") and bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣጺ"))):
        return {
            bstack11ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጻ"): bstack11ll1l_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨጼ"),
            bstack11ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢጽ"): env.get(bstack11ll1l_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧጾ")),
            bstack11ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣጿ"): env.get(bstack11ll1l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤፀ")),
            bstack11ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢፁ"): env.get(bstack11ll1l_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣፂ"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠥࡇࡎࠨፃ")) == bstack11ll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤፄ") and env.get(bstack11ll1l_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨፅ")) == bstack11ll1l_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣፆ"):
        return {
            bstack11ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧፇ"): bstack11ll1l_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥፈ"),
            bstack11ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧፉ"): None,
            bstack11ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧፊ"): None,
            bstack11ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥፋ"): None
        }
    if env.get(bstack11ll1l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣፌ")) and env.get(bstack11ll1l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤፍ")):
        return {
            bstack11ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧፎ"): bstack11ll1l_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦፏ"),
            bstack11ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧፐ"): env.get(bstack11ll1l_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣፑ")),
            bstack11ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨፒ"): None,
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦፓ"): env.get(bstack11ll1l_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣፔ"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠢࡄࡋࠥፕ")) == bstack11ll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨፖ") and bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣፗ"))):
        return {
            bstack11ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣፘ"): bstack11ll1l_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥፙ"),
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣፚ"): env.get(bstack11ll1l_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤ፛")),
            bstack11ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፜"): None,
            bstack11ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢ፝"): env.get(bstack11ll1l_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ፞"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠥࡇࡎࠨ፟")) == bstack11ll1l_opy_ (u"ࠦࡹࡸࡵࡦࠤ፠") and bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣ፡"))):
        return {
            bstack11ll1l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ።"): bstack11ll1l_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥ፣"),
            bstack11ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ፤"): env.get(bstack11ll1l_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣ፥")),
            bstack11ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ፦"): env.get(bstack11ll1l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤ፧")),
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦ፨"): env.get(bstack11ll1l_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤ፩"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠢࡄࡋࠥ፪")) == bstack11ll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨ፫") and bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧ፬"))):
        return {
            bstack11ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣ፭"): bstack11ll1l_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦ፮"),
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፯"): env.get(bstack11ll1l_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥ፰")),
            bstack11ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፱"): env.get(bstack11ll1l_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ፲")),
            bstack11ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ፳"): env.get(bstack11ll1l_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨ፴"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠦࡈࡏࠢ፵")) == bstack11ll1l_opy_ (u"ࠧࡺࡲࡶࡧࠥ፶") and bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤ፷"))):
        return {
            bstack11ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ፸"): bstack11ll1l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦ፹"),
            bstack11ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ፺"): env.get(bstack11ll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤ፻")),
            bstack11ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ፼"): env.get(bstack11ll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢ፽")) or env.get(bstack11ll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤ፾")),
            bstack11ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፿"): env.get(bstack11ll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᎀ"))
        }
    if bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᎁ"))):
        return {
            bstack11ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᎂ"): bstack11ll1l_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᎃ"),
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎄ"): bstack11ll1l_opy_ (u"ࠨࡻࡾࡽࢀࠦᎅ").format(env.get(bstack11ll1l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᎆ")), env.get(bstack11ll1l_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᎇ"))),
            bstack11ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᎈ"): env.get(bstack11ll1l_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤᎉ")),
            bstack11ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎊ"): env.get(bstack11ll1l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᎋ"))
        }
    if bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᎌ"))):
        return {
            bstack11ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᎍ"): bstack11ll1l_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᎎ"),
            bstack11ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᎏ"): bstack11ll1l_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤ᎐").format(env.get(bstack11ll1l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪ᎑")), env.get(bstack11ll1l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭᎒")), env.get(bstack11ll1l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧ᎓")), env.get(bstack11ll1l_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫ᎔"))),
            bstack11ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᎕"): env.get(bstack11ll1l_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᎖")),
            bstack11ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᎗"): env.get(bstack11ll1l_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧ᎘"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨ᎙")) and env.get(bstack11ll1l_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣ᎚")):
        return {
            bstack11ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᎛"): bstack11ll1l_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥ᎜"),
            bstack11ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᎝"): bstack11ll1l_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨ᎞").format(env.get(bstack11ll1l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧ᎟")), env.get(bstack11ll1l_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᎠ")), env.get(bstack11ll1l_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭Ꭱ"))),
            bstack11ll1l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎢ"): env.get(bstack11ll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᎣ")),
            bstack11ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᎤ"): env.get(bstack11ll1l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᎥ"))
        }
    if any([env.get(bstack11ll1l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᎦ")), env.get(bstack11ll1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᎧ")), env.get(bstack11ll1l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᎨ"))]):
        return {
            bstack11ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᎩ"): bstack11ll1l_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᎪ"),
            bstack11ll1l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᎫ"): env.get(bstack11ll1l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᎬ")),
            bstack11ll1l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᎭ"): env.get(bstack11ll1l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᎮ")),
            bstack11ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᎯ"): env.get(bstack11ll1l_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᎰ"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᎱ")):
        return {
            bstack11ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᎲ"): bstack11ll1l_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥᎳ"),
            bstack11ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᎴ"): env.get(bstack11ll1l_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢᎵ")),
            bstack11ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᎶ"): env.get(bstack11ll1l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨᎷ")),
            bstack11ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎸ"): env.get(bstack11ll1l_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᎹ"))
        }
    if env.get(bstack11ll1l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦᎺ")) or env.get(bstack11ll1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᎻ")):
        return {
            bstack11ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᎼ"): bstack11ll1l_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢᎽ"),
            bstack11ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᎾ"): env.get(bstack11ll1l_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᎿ")),
            bstack11ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏀ"): bstack11ll1l_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥᏁ") if env.get(bstack11ll1l_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᏂ")) else None,
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏃ"): env.get(bstack11ll1l_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦᏄ"))
        }
    if any([env.get(bstack11ll1l_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧᏅ")), env.get(bstack11ll1l_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᏆ")), env.get(bstack11ll1l_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᏇ"))]):
        return {
            bstack11ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏈ"): bstack11ll1l_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥᏉ"),
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏊ"): None,
            bstack11ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᏋ"): env.get(bstack11ll1l_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦᏌ")),
            bstack11ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᏍ"): env.get(bstack11ll1l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᏎ"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨᏏ")):
        return {
            bstack11ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᏐ"): bstack11ll1l_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣᏑ"),
            bstack11ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᏒ"): env.get(bstack11ll1l_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᏓ")),
            bstack11ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᏔ"): bstack11ll1l_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥᏕ").format(env.get(bstack11ll1l_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭Ꮦ"))) if env.get(bstack11ll1l_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᏗ")) else None,
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏘ"): env.get(bstack11ll1l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᏙ"))
        }
    if bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣᏚ"))):
        return {
            bstack11ll1l_opy_ (u"ࠣࡰࡤࡱࡪࠨᏛ"): bstack11ll1l_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥᏜ"),
            bstack11ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᏝ"): env.get(bstack11ll1l_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣᏞ")),
            bstack11ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᏟ"): env.get(bstack11ll1l_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤᏠ")),
            bstack11ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᏡ"): env.get(bstack11ll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᏢ"))
        }
    if bstack1l11lll111_opy_(env.get(bstack11ll1l_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥᏣ"))):
        return {
            bstack11ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᏤ"): bstack11ll1l_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧᏥ"),
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᏦ"): bstack11ll1l_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢᏧ").format(env.get(bstack11ll1l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫᏨ")), env.get(bstack11ll1l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬᏩ")), env.get(bstack11ll1l_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩᏪ"))),
            bstack11ll1l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᏫ"): env.get(bstack11ll1l_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨᏬ")),
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᏭ"): env.get(bstack11ll1l_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨᏮ"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠢࡄࡋࠥᏯ")) == bstack11ll1l_opy_ (u"ࠣࡶࡵࡹࡪࠨᏰ") and env.get(bstack11ll1l_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤᏱ")) == bstack11ll1l_opy_ (u"ࠥ࠵ࠧᏲ"):
        return {
            bstack11ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᏳ"): bstack11ll1l_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧᏴ"),
            bstack11ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᏵ"): bstack11ll1l_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥ᏶").format(env.get(bstack11ll1l_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬ᏷"))),
            bstack11ll1l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏸ"): None,
            bstack11ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᏹ"): None,
        }
    if env.get(bstack11ll1l_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢᏺ")):
        return {
            bstack11ll1l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏻ"): bstack11ll1l_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣᏼ"),
            bstack11ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏽ"): None,
            bstack11ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᏾"): env.get(bstack11ll1l_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥ᏿")),
            bstack11ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᐀"): env.get(bstack11ll1l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᐁ"))
        }
    if any([env.get(bstack11ll1l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣᐂ")), env.get(bstack11ll1l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨᐃ")), env.get(bstack11ll1l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧᐄ")), env.get(bstack11ll1l_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤᐅ"))]):
        return {
            bstack11ll1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᐆ"): bstack11ll1l_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨᐇ"),
            bstack11ll1l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᐈ"): None,
            bstack11ll1l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᐉ"): env.get(bstack11ll1l_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᐊ")) or None,
            bstack11ll1l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᐋ"): env.get(bstack11ll1l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᐌ"), 0)
        }
    if env.get(bstack11ll1l_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢᐍ")):
        return {
            bstack11ll1l_opy_ (u"ࠥࡲࡦࡳࡥࠣᐎ"): bstack11ll1l_opy_ (u"ࠦࡌࡵࡃࡅࠤᐏ"),
            bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᐐ"): None,
            bstack11ll1l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᐑ"): env.get(bstack11ll1l_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᐒ")),
            bstack11ll1l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᐓ"): env.get(bstack11ll1l_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣᐔ"))
        }
    if env.get(bstack11ll1l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣᐕ")):
        return {
            bstack11ll1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᐖ"): bstack11ll1l_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣᐗ"),
            bstack11ll1l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᐘ"): env.get(bstack11ll1l_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᐙ")),
            bstack11ll1l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᐚ"): env.get(bstack11ll1l_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧᐛ")),
            bstack11ll1l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᐜ"): env.get(bstack11ll1l_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᐝ"))
        }
    return {bstack11ll1l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᐞ"): None}
def get_host_info():
    return {
        bstack11ll1l_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣᐟ"): platform.node(),
        bstack11ll1l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤᐠ"): platform.system(),
        bstack11ll1l_opy_ (u"ࠣࡶࡼࡴࡪࠨᐡ"): platform.machine(),
        bstack11ll1l_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥᐢ"): platform.version(),
        bstack11ll1l_opy_ (u"ࠥࡥࡷࡩࡨࠣᐣ"): platform.architecture()[0]
    }
def bstack1l1l111ll1_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack111l111111_opy_():
    if bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬᐤ")):
        return bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫᐥ")
    return bstack11ll1l_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬᐦ")
def bstack1111ll1lll_opy_(driver):
    info = {
        bstack11ll1l_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᐧ"): driver.capabilities,
        bstack11ll1l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬᐨ"): driver.session_id,
        bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᐩ"): driver.capabilities.get(bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᐪ"), None),
        bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᐫ"): driver.capabilities.get(bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᐬ"), None),
        bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨᐭ"): driver.capabilities.get(bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᐮ"), None),
    }
    if bstack111l111111_opy_() == bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᐯ"):
        info[bstack11ll1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪᐰ")] = bstack11ll1l_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩᐱ") if bstack1ll1l1l1ll_opy_() else bstack11ll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᐲ")
    return info
def bstack1ll1l1l1ll_opy_():
    if bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᐳ")):
        return True
    if bstack1l11lll111_opy_(os.environ.get(bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧᐴ"), None)):
        return True
    return False
def bstack1ll1lll1l1_opy_(bstack1111l1l11l_opy_, url, data, config):
    headers = config.get(bstack11ll1l_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᐵ"), None)
    proxies = bstack111ll1l11_opy_(config, url)
    auth = config.get(bstack11ll1l_opy_ (u"ࠨࡣࡸࡸ࡭࠭ᐶ"), None)
    response = requests.request(
            bstack1111l1l11l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll111111l_opy_(bstack1l11lllll_opy_, size):
    bstack11lllllll1_opy_ = []
    while len(bstack1l11lllll_opy_) > size:
        bstack1lll111111_opy_ = bstack1l11lllll_opy_[:size]
        bstack11lllllll1_opy_.append(bstack1lll111111_opy_)
        bstack1l11lllll_opy_ = bstack1l11lllll_opy_[size:]
    bstack11lllllll1_opy_.append(bstack1l11lllll_opy_)
    return bstack11lllllll1_opy_
def bstack1111l1111l_opy_(message, bstack11111ll111_opy_=False):
    os.write(1, bytes(message, bstack11ll1l_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᐷ")))
    os.write(1, bytes(bstack11ll1l_opy_ (u"ࠪࡠࡳ࠭ᐸ"), bstack11ll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᐹ")))
    if bstack11111ll111_opy_:
        with open(bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫᐺ") + os.environ[bstack11ll1l_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬᐻ")] + bstack11ll1l_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬᐼ"), bstack11ll1l_opy_ (u"ࠨࡣࠪᐽ")) as f:
            f.write(message + bstack11ll1l_opy_ (u"ࠩ࡟ࡲࠬᐾ"))
def bstack11111l1l1l_opy_():
    return os.environ[bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᐿ")].lower() == bstack11ll1l_opy_ (u"ࠫࡹࡸࡵࡦࠩᑀ")
def bstack1l1l1l111l_opy_(bstack1111l1l111_opy_):
    return bstack11ll1l_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫᑁ").format(bstack111l1ll1l1_opy_, bstack1111l1l111_opy_)
def bstack1lll11l1_opy_():
    return bstack11llll1l_opy_().replace(tzinfo=None).isoformat() + bstack11ll1l_opy_ (u"࡚࠭ࠨᑂ")
def bstack1111111ll1_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11ll1l_opy_ (u"࡛ࠧࠩᑃ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11ll1l_opy_ (u"ࠨ࡜ࠪᑄ")))).total_seconds() * 1000
def bstack111l1l111l_opy_(timestamp):
    return bstack1111111l11_opy_(timestamp).isoformat() + bstack11ll1l_opy_ (u"ࠩ࡝ࠫᑅ")
def bstack1111l1l1ll_opy_(bstack11111llll1_opy_):
    date_format = bstack11ll1l_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨᑆ")
    bstack11111l111l_opy_ = datetime.datetime.strptime(bstack11111llll1_opy_, date_format)
    return bstack11111l111l_opy_.isoformat() + bstack11ll1l_opy_ (u"ࠫ࡟࠭ᑇ")
def bstack1111lll11l_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑈ")
    else:
        return bstack11ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᑉ")
def bstack1l11lll111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11ll1l_opy_ (u"ࠧࡵࡴࡸࡩࠬᑊ")
def bstack111111ll11_opy_(val):
    return val.__str__().lower() == bstack11ll1l_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᑋ")
def bstack11lll11l_opy_(bstack111l1111l1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l1111l1_opy_ as e:
                print(bstack11ll1l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᑌ").format(func.__name__, bstack111l1111l1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack111l11lll1_opy_(bstack111111llll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111111llll_opy_(cls, *args, **kwargs)
            except bstack111l1111l1_opy_ as e:
                print(bstack11ll1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᑍ").format(bstack111111llll_opy_.__name__, bstack111l1111l1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack111l11lll1_opy_
    else:
        return decorator
def bstack1lllll1l1l_opy_(bstack11l1llll_opy_):
    if bstack11ll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᑎ") in bstack11l1llll_opy_ and bstack111111ll11_opy_(bstack11l1llll_opy_[bstack11ll1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᑏ")]):
        return False
    if bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᑐ") in bstack11l1llll_opy_ and bstack111111ll11_opy_(bstack11l1llll_opy_[bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᑑ")]):
        return False
    return True
def bstack1ll11l11ll_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1llll111l_opy_(hub_url):
    if bstack11l111lll_opy_() <= version.parse(bstack11ll1l_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨᑒ")):
        if hub_url != bstack11ll1l_opy_ (u"ࠩࠪᑓ"):
            return bstack11ll1l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᑔ") + hub_url + bstack11ll1l_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣᑕ")
        return bstack1lll11ll11_opy_
    if hub_url != bstack11ll1l_opy_ (u"ࠬ࠭ᑖ"):
        return bstack11ll1l_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᑗ") + hub_url + bstack11ll1l_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣᑘ")
    return bstack11ll1l1l1_opy_
def bstack1111111111_opy_():
    return isinstance(os.getenv(bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧᑙ")), str)
def bstack1l1l11l1ll_opy_(url):
    return urlparse(url).hostname
def bstack1l11l111l_opy_(hostname):
    for bstack1ll1lllll_opy_ in bstack1l11l11111_opy_:
        regex = re.compile(bstack1ll1lllll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11111l1ll1_opy_(bstack11111lll11_opy_, file_name, logger):
    bstack11l1l1lll_opy_ = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠩࢁࠫᑚ")), bstack11111lll11_opy_)
    try:
        if not os.path.exists(bstack11l1l1lll_opy_):
            os.makedirs(bstack11l1l1lll_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠪࢂࠬᑛ")), bstack11111lll11_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11ll1l_opy_ (u"ࠫࡼ࠭ᑜ")):
                pass
            with open(file_path, bstack11ll1l_opy_ (u"ࠧࡽࠫࠣᑝ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1111111_opy_.format(str(e)))
def bstack1111ll1ll1_opy_(file_name, key, value, logger):
    file_path = bstack11111l1ll1_opy_(bstack11ll1l_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ᑞ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1llll1_opy_ = json.load(open(file_path, bstack11ll1l_opy_ (u"ࠧࡳࡤࠪᑟ")))
        else:
            bstack1ll1llll1_opy_ = {}
        bstack1ll1llll1_opy_[key] = value
        with open(file_path, bstack11ll1l_opy_ (u"ࠣࡹ࠮ࠦᑠ")) as outfile:
            json.dump(bstack1ll1llll1_opy_, outfile)
def bstack1llll1llll_opy_(file_name, logger):
    file_path = bstack11111l1ll1_opy_(bstack11ll1l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᑡ"), file_name, logger)
    bstack1ll1llll1_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11ll1l_opy_ (u"ࠪࡶࠬᑢ")) as bstack11ll11l11_opy_:
            bstack1ll1llll1_opy_ = json.load(bstack11ll11l11_opy_)
    return bstack1ll1llll1_opy_
def bstack111l1l1l1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨᑣ") + file_path + bstack11ll1l_opy_ (u"ࠬࠦࠧᑤ") + str(e))
def bstack11l111lll_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11ll1l_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣᑥ")
def bstack1l1111l11_opy_(config):
    if bstack11ll1l_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᑦ") in config:
        del (config[bstack11ll1l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᑧ")])
        return False
    if bstack11l111lll_opy_() < version.parse(bstack11ll1l_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨᑨ")):
        return False
    if bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩᑩ")):
        return True
    if bstack11ll1l_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫᑪ") in config and config[bstack11ll1l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᑫ")] is False:
        return False
    else:
        return True
def bstack111lllll1_opy_(args_list, bstack11111111l1_opy_):
    index = -1
    for value in bstack11111111l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1ll1llll_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1ll1llll_opy_ = bstack1ll1llll_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᑬ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11ll1l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᑭ"), exception=exception)
    def bstack1111lll1_opy_(self):
        if self.result != bstack11ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᑮ"):
            return None
        if isinstance(self.exception_type, str) and bstack11ll1l_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧᑯ") in self.exception_type:
            return bstack11ll1l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦᑰ")
        return bstack11ll1l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᑱ")
    def bstack111l111l1l_opy_(self):
        if self.result != bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᑲ"):
            return None
        if self.bstack1ll1llll_opy_:
            return self.bstack1ll1llll_opy_
        return bstack11111lllll_opy_(self.exception)
def bstack11111lllll_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack1111l111l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1ll11111_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1111l1111_opy_(config, logger):
    try:
        import playwright
        bstack1111l1l1l1_opy_ = playwright.__file__
        bstack11111lll1l_opy_ = os.path.split(bstack1111l1l1l1_opy_)
        bstack11111l11l1_opy_ = bstack11111lll1l_opy_[0] + bstack11ll1l_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩᑳ")
        os.environ[bstack11ll1l_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪᑴ")] = bstack1lll1l1lll_opy_(config)
        with open(bstack11111l11l1_opy_, bstack11ll1l_opy_ (u"ࠨࡴࠪᑵ")) as f:
            bstack11llll1lll_opy_ = f.read()
            bstack1111l11l1l_opy_ = bstack11ll1l_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨᑶ")
            bstack111l1l1111_opy_ = bstack11llll1lll_opy_.find(bstack1111l11l1l_opy_)
            if bstack111l1l1111_opy_ == -1:
              process = subprocess.Popen(bstack11ll1l_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢᑷ"), shell=True, cwd=bstack11111lll1l_opy_[0])
              process.wait()
              bstack111111l111_opy_ = bstack11ll1l_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫᑸ")
              bstack111111111l_opy_ = bstack11ll1l_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤᑹ")
              bstack1111l111ll_opy_ = bstack11llll1lll_opy_.replace(bstack111111l111_opy_, bstack111111111l_opy_)
              with open(bstack11111l11l1_opy_, bstack11ll1l_opy_ (u"࠭ࡷࠨᑺ")) as f:
                f.write(bstack1111l111ll_opy_)
    except Exception as e:
        logger.error(bstack11lll1l1l_opy_.format(str(e)))
def bstack1l1l111ll_opy_():
  try:
    bstack111l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧᑻ"))
    bstack11111l11ll_opy_ = []
    if os.path.exists(bstack111l11l1l1_opy_):
      with open(bstack111l11l1l1_opy_) as f:
        bstack11111l11ll_opy_ = json.load(f)
      os.remove(bstack111l11l1l1_opy_)
    return bstack11111l11ll_opy_
  except:
    pass
  return []
def bstack1ll1ll1111_opy_(bstack1lllll1ll_opy_):
  try:
    bstack11111l11ll_opy_ = []
    bstack111l11l1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᑼ"))
    if os.path.exists(bstack111l11l1l1_opy_):
      with open(bstack111l11l1l1_opy_) as f:
        bstack11111l11ll_opy_ = json.load(f)
    bstack11111l11ll_opy_.append(bstack1lllll1ll_opy_)
    with open(bstack111l11l1l1_opy_, bstack11ll1l_opy_ (u"ࠩࡺࠫᑽ")) as f:
        json.dump(bstack11111l11ll_opy_, f)
  except:
    pass
def bstack111ll1l1l_opy_(logger, bstack11111l1l11_opy_ = False):
  try:
    test_name = os.environ.get(bstack11ll1l_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ᑾ"), bstack11ll1l_opy_ (u"ࠫࠬᑿ"))
    if test_name == bstack11ll1l_opy_ (u"ࠬ࠭ᒀ"):
        test_name = threading.current_thread().__dict__.get(bstack11ll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬᒁ"), bstack11ll1l_opy_ (u"ࠧࠨᒂ"))
    bstack1111ll11l1_opy_ = bstack11ll1l_opy_ (u"ࠨ࠮ࠣࠫᒃ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11111l1l11_opy_:
        bstack111llll1l_opy_ = os.environ.get(bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᒄ"), bstack11ll1l_opy_ (u"ࠪ࠴ࠬᒅ"))
        bstack1l1lllllll_opy_ = {bstack11ll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᒆ"): test_name, bstack11ll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᒇ"): bstack1111ll11l1_opy_, bstack11ll1l_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬᒈ"): bstack111llll1l_opy_}
        bstack1111lll1l1_opy_ = []
        bstack1111ll11ll_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ᒉ"))
        if os.path.exists(bstack1111ll11ll_opy_):
            with open(bstack1111ll11ll_opy_) as f:
                bstack1111lll1l1_opy_ = json.load(f)
        bstack1111lll1l1_opy_.append(bstack1l1lllllll_opy_)
        with open(bstack1111ll11ll_opy_, bstack11ll1l_opy_ (u"ࠨࡹࠪᒊ")) as f:
            json.dump(bstack1111lll1l1_opy_, f)
    else:
        bstack1l1lllllll_opy_ = {bstack11ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᒋ"): test_name, bstack11ll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᒌ"): bstack1111ll11l1_opy_, bstack11ll1l_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᒍ"): str(multiprocessing.current_process().name)}
        if bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩᒎ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1lllllll_opy_)
  except Exception as e:
      logger.warn(bstack11ll1l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥᒏ").format(e))
def bstack1llll11l1l_opy_(error_message, test_name, index, logger):
  try:
    bstack111l11l1ll_opy_ = []
    bstack1l1lllllll_opy_ = {bstack11ll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᒐ"): test_name, bstack11ll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᒑ"): error_message, bstack11ll1l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᒒ"): index}
    bstack1111ll1111_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫᒓ"))
    if os.path.exists(bstack1111ll1111_opy_):
        with open(bstack1111ll1111_opy_) as f:
            bstack111l11l1ll_opy_ = json.load(f)
    bstack111l11l1ll_opy_.append(bstack1l1lllllll_opy_)
    with open(bstack1111ll1111_opy_, bstack11ll1l_opy_ (u"ࠫࡼ࠭ᒔ")) as f:
        json.dump(bstack111l11l1ll_opy_, f)
  except Exception as e:
    logger.warn(bstack11ll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣᒕ").format(e))
def bstack11ll11lll1_opy_(bstack11111lll1_opy_, name, logger):
  try:
    bstack1l1lllllll_opy_ = {bstack11ll1l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᒖ"): name, bstack11ll1l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᒗ"): bstack11111lll1_opy_, bstack11ll1l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᒘ"): str(threading.current_thread()._name)}
    return bstack1l1lllllll_opy_
  except Exception as e:
    logger.warn(bstack11ll1l_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨᒙ").format(e))
  return
def bstack1111ll111l_opy_():
    return platform.system() == bstack11ll1l_opy_ (u"࡛ࠪ࡮ࡴࡤࡰࡹࡶࠫᒚ")
def bstack11ll11ll1_opy_(bstack1111lll111_opy_, config, logger):
    bstack111l11ll11_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111lll111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫࡯ࡸࡪࡸࠠࡤࡱࡱࡪ࡮࡭ࠠ࡬ࡧࡼࡷࠥࡨࡹࠡࡴࡨ࡫ࡪࡾࠠ࡮ࡣࡷࡧ࡭ࡀࠠࡼࡿࠥᒛ").format(e))
    return bstack111l11ll11_opy_
def bstack111l111lll_opy_(bstack1111l1llll_opy_, bstack1111l11ll1_opy_):
    bstack111l11ll1l_opy_ = version.parse(bstack1111l1llll_opy_)
    bstack111111lll1_opy_ = version.parse(bstack1111l11ll1_opy_)
    if bstack111l11ll1l_opy_ > bstack111111lll1_opy_:
        return 1
    elif bstack111l11ll1l_opy_ < bstack111111lll1_opy_:
        return -1
    else:
        return 0
def bstack11llll1l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack1111111l11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack1111l1ll1l_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack11lllll11_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack11ll1l_opy_ (u"ࠬ࡭ࡥࡵࠩᒜ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1ll1lll11_opy_ = caps.get(bstack11ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᒝ"))
    bstack111111l11l_opy_ = True
    if bstack111111ll11_opy_(caps.get(bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡵࡴࡧ࡚࠷ࡈ࠭ᒞ"))) or bstack111111ll11_opy_(caps.get(bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨᒟ"))):
        bstack111111l11l_opy_ = False
    if bstack1l1111l11_opy_({bstack11ll1l_opy_ (u"ࠤࡸࡷࡪ࡝࠳ࡄࠤᒠ"): bstack111111l11l_opy_}):
        bstack1ll1lll11_opy_ = bstack1ll1lll11_opy_ or {}
        bstack1ll1lll11_opy_[bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᒡ")] = bstack1111l1ll1l_opy_(framework)
        bstack1ll1lll11_opy_[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᒢ")] = bstack11111l1l1l_opy_()
        if getattr(options, bstack11ll1l_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭ᒣ"), None):
            options.set_capability(bstack11ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᒤ"), bstack1ll1lll11_opy_)
        else:
            options[bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒥ")] = bstack1ll1lll11_opy_
    else:
        if getattr(options, bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡺࠩᒦ"), None):
            options.set_capability(bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪᒧ"), bstack1111l1ll1l_opy_(framework))
            options.set_capability(bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᒨ"), bstack11111l1l1l_opy_())
        else:
            options[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᒩ")] = bstack1111l1ll1l_opy_(framework)
            options[bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᒪ")] = bstack11111l1l1l_opy_()
    return options
def bstack1111llllll_opy_(bstack1111lll1ll_opy_, framework):
    if bstack1111lll1ll_opy_ and len(bstack1111lll1ll_opy_.split(bstack11ll1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᒫ"))) > 1:
        ws_url = bstack1111lll1ll_opy_.split(bstack11ll1l_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᒬ"))[0]
        if bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫᒭ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack1111l1lll1_opy_ = json.loads(urllib.parse.unquote(bstack1111lll1ll_opy_.split(bstack11ll1l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨᒮ"))[1]))
            bstack1111l1lll1_opy_ = bstack1111l1lll1_opy_ or {}
            bstack1111l1lll1_opy_[bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᒯ")] = str(framework) + str(__version__)
            bstack1111l1lll1_opy_[bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᒰ")] = bstack11111l1l1l_opy_()
            bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_.split(bstack11ll1l_opy_ (u"ࠬࡩࡡࡱࡵࡀࠫᒱ"))[0] + bstack11ll1l_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᒲ") + urllib.parse.quote(json.dumps(bstack1111l1lll1_opy_))
    return bstack1111lll1ll_opy_
def bstack11llll1l1l_opy_():
    global bstack1l1l1111l1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1l1l1111l1_opy_ = BrowserType.connect
    return bstack1l1l1111l1_opy_
def bstack1llll11lll_opy_(framework_name):
    global bstack11l11l11l_opy_
    bstack11l11l11l_opy_ = framework_name
    return framework_name
def bstack1l11l1l1l1_opy_(self, *args, **kwargs):
    global bstack1l1l1111l1_opy_
    try:
        global bstack11l11l11l_opy_
        if bstack11ll1l_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᒳ") in kwargs:
            kwargs[bstack11ll1l_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᒴ")] = bstack1111llllll_opy_(
                kwargs.get(bstack11ll1l_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᒵ"), None),
                bstack11l11l11l_opy_
            )
    except Exception as e:
        logger.error(bstack11ll1l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡘࡊࡋࠡࡥࡤࡴࡸࡀࠠࡼࡿࠥᒶ").format(str(e)))
    return bstack1l1l1111l1_opy_(self, *args, **kwargs)
def bstack111111l1ll_opy_(bstack1111lllll1_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111ll1l11_opy_(bstack1111lllll1_opy_, bstack11ll1l_opy_ (u"ࠦࠧᒷ"))
        if proxies and proxies.get(bstack11ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦᒸ")):
            parsed_url = urlparse(proxies.get(bstack11ll1l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᒹ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11ll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᒺ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11ll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᒻ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11ll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡖࡵࡨࡶࠬᒼ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11ll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᒽ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1111111ll_opy_(bstack1111lllll1_opy_):
    bstack111l11111l_opy_ = {
        bstack111ll1111l_opy_[bstack11111ll11l_opy_]: bstack1111lllll1_opy_[bstack11111ll11l_opy_]
        for bstack11111ll11l_opy_ in bstack1111lllll1_opy_
        if bstack11111ll11l_opy_ in bstack111ll1111l_opy_
    }
    bstack111l11111l_opy_[bstack11ll1l_opy_ (u"ࠦࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠦᒾ")] = bstack111111l1ll_opy_(bstack1111lllll1_opy_, bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᒿ")))
    bstack111l1l11ll_opy_ = [element.lower() for element in bstack111ll111ll_opy_]
    bstack111l1111ll_opy_(bstack111l11111l_opy_, bstack111l1l11ll_opy_)
    return bstack111l11111l_opy_
def bstack111l1111ll_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11ll1l_opy_ (u"ࠨࠪࠫࠬ࠭ࠦᓀ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l1111ll_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l1111ll_opy_(item, keys)