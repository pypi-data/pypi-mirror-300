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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l11l1l11_opy_
bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
def bstack1lll11ll111_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll11lll11_opy_(bstack1lll11ll1l1_opy_, bstack1lll11ll11l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll11ll1l1_opy_):
        with open(bstack1lll11ll1l1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll11ll111_opy_(bstack1lll11ll1l1_opy_):
        pac = get_pac(url=bstack1lll11ll1l1_opy_)
    else:
        raise Exception(bstack11ll1l_opy_ (u"ࠪࡔࡦࡩࠠࡧ࡫࡯ࡩࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡀࠠࡼࡿࠪᖈ").format(bstack1lll11ll1l1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11ll1l_opy_ (u"ࠦ࠽࠴࠸࠯࠺࠱࠼ࠧᖉ"), 80))
        bstack1lll11llll1_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll11llll1_opy_ = bstack11ll1l_opy_ (u"ࠬ࠶࠮࠱࠰࠳࠲࠵࠭ᖊ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll11ll11l_opy_, bstack1lll11llll1_opy_)
    return proxy_url
def bstack1lll1ll1ll_opy_(config):
    return bstack11ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᖋ") in config or bstack11ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᖌ") in config
def bstack1lll1l1lll_opy_(config):
    if not bstack1lll1ll1ll_opy_(config):
        return
    if config.get(bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᖍ")):
        return config.get(bstack11ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᖎ"))
    if config.get(bstack11ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᖏ")):
        return config.get(bstack11ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨᖐ"))
def bstack111ll1l11_opy_(config, bstack1lll11ll11l_opy_):
    proxy = bstack1lll1l1lll_opy_(config)
    proxies = {}
    if config.get(bstack11ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᖑ")) or config.get(bstack11ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᖒ")):
        if proxy.endswith(bstack11ll1l_opy_ (u"ࠧ࠯ࡲࡤࡧࠬᖓ")):
            proxies = bstack11l1lll11l_opy_(proxy, bstack1lll11ll11l_opy_)
        else:
            proxies = {
                bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖔ"): proxy
            }
    bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠩᖕ"), proxies)
    return proxies
def bstack11l1lll11l_opy_(bstack1lll11ll1l1_opy_, bstack1lll11ll11l_opy_):
    proxies = {}
    global bstack1lll11ll1ll_opy_
    if bstack11ll1l_opy_ (u"ࠪࡔࡆࡉ࡟ࡑࡔࡒ࡜࡞࠭ᖖ") in globals():
        return bstack1lll11ll1ll_opy_
    try:
        proxy = bstack1lll11lll11_opy_(bstack1lll11ll1l1_opy_, bstack1lll11ll11l_opy_)
        if bstack11ll1l_opy_ (u"ࠦࡉࡏࡒࡆࡅࡗࠦᖗ") in proxy:
            proxies = {}
        elif bstack11ll1l_opy_ (u"ࠧࡎࡔࡕࡒࠥᖘ") in proxy or bstack11ll1l_opy_ (u"ࠨࡈࡕࡖࡓࡗࠧᖙ") in proxy or bstack11ll1l_opy_ (u"ࠢࡔࡑࡆࡏࡘࠨᖚ") in proxy:
            bstack1lll11lll1l_opy_ = proxy.split(bstack11ll1l_opy_ (u"ࠣࠢࠥᖛ"))
            if bstack11ll1l_opy_ (u"ࠤ࠽࠳࠴ࠨᖜ") in bstack11ll1l_opy_ (u"ࠥࠦᖝ").join(bstack1lll11lll1l_opy_[1:]):
                proxies = {
                    bstack11ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᖞ"): bstack11ll1l_opy_ (u"ࠧࠨᖟ").join(bstack1lll11lll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖠ"): str(bstack1lll11lll1l_opy_[0]).lower() + bstack11ll1l_opy_ (u"ࠢ࠻࠱࠲ࠦᖡ") + bstack11ll1l_opy_ (u"ࠣࠤᖢ").join(bstack1lll11lll1l_opy_[1:])
                }
        elif bstack11ll1l_opy_ (u"ࠤࡓࡖࡔ࡞࡙ࠣᖣ") in proxy:
            bstack1lll11lll1l_opy_ = proxy.split(bstack11ll1l_opy_ (u"ࠥࠤࠧᖤ"))
            if bstack11ll1l_opy_ (u"ࠦ࠿࠵࠯ࠣᖥ") in bstack11ll1l_opy_ (u"ࠧࠨᖦ").join(bstack1lll11lll1l_opy_[1:]):
                proxies = {
                    bstack11ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖧ"): bstack11ll1l_opy_ (u"ࠢࠣᖨ").join(bstack1lll11lll1l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖩ"): bstack11ll1l_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥᖪ") + bstack11ll1l_opy_ (u"ࠥࠦᖫ").join(bstack1lll11lll1l_opy_[1:])
                }
        else:
            proxies = {
                bstack11ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᖬ"): proxy
            }
    except Exception as e:
        print(bstack11ll1l_opy_ (u"ࠧࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤᖭ"), bstack11l11l1l11_opy_.format(bstack1lll11ll1l1_opy_, str(e)))
    bstack1lll11ll1ll_opy_ = proxies
    return proxies