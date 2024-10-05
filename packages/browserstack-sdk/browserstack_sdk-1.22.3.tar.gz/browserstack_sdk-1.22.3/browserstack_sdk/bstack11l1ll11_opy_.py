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
import multiprocessing
import os
import json
from time import sleep
import bstack_utils.bstack11l11111_opy_ as bstack111lll1l_opy_
from browserstack_sdk.bstack11ll11ll_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1ll1l_opy_
class bstack11l1l111_opy_:
    def __init__(self, args, logger, bstack11l1llll_opy_, bstack111l11ll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1llll_opy_ = bstack11l1llll_opy_
        self.bstack111l11ll_opy_ = bstack111l11ll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack111l1lll_opy_ = []
        self.bstack111l1l11_opy_ = None
        self.bstack11l1l1l1_opy_ = []
        self.bstack111l111l_opy_ = self.bstack11l1l1ll_opy_()
        self.bstack11l11l1l_opy_ = -1
    def bstack111l1111_opy_(self, bstack111l1l1l_opy_):
        self.parse_args()
        self.bstack11ll111l_opy_()
        self.bstack111lllll_opy_(bstack111l1l1l_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    @staticmethod
    def bstack11l111l1_opy_():
        import importlib
        if getattr(importlib, bstack11ll1l_opy_ (u"ࠫ࡫࡯࡮ࡥࡡ࡯ࡳࡦࡪࡥࡳࠩू"), False):
            bstack11ll11l1_opy_ = importlib.find_loader(bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧृ"))
        else:
            bstack11ll11l1_opy_ = importlib.util.find_spec(bstack11ll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡥࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨॄ"))
    def bstack111ll1l1_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack11l11l1l_opy_ = -1
        if self.bstack111l11ll_opy_ and bstack11ll1l_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧॅ") in self.bstack11l1llll_opy_:
            self.bstack11l11l1l_opy_ = int(self.bstack11l1llll_opy_[bstack11ll1l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨॆ")])
        try:
            bstack111ll111_opy_ = [bstack11ll1l_opy_ (u"ࠩ࠰࠱ࡩࡸࡩࡷࡧࡵࠫे"), bstack11ll1l_opy_ (u"ࠪ࠱࠲ࡶ࡬ࡶࡩ࡬ࡲࡸ࠭ै"), bstack11ll1l_opy_ (u"ࠫ࠲ࡶࠧॉ")]
            if self.bstack11l11l1l_opy_ >= 0:
                bstack111ll111_opy_.extend([bstack11ll1l_opy_ (u"ࠬ࠳࠭࡯ࡷࡰࡴࡷࡵࡣࡦࡵࡶࡩࡸ࠭ॊ"), bstack11ll1l_opy_ (u"࠭࠭࡯ࠩो")])
            for arg in bstack111ll111_opy_:
                self.bstack111ll1l1_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11ll111l_opy_(self):
        bstack111l1l11_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack111l1l11_opy_ = bstack111l1l11_opy_
        return bstack111l1l11_opy_
    def bstack11l11l11_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            self.bstack11l111l1_opy_()
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack11l1ll1l_opy_)
    def bstack111lllll_opy_(self, bstack111l1l1l_opy_):
        bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
        if bstack111l1l1l_opy_:
            self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"ࠧ࠮࠯ࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫौ"))
            self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"ࠨࡖࡵࡹࡪ्࠭"))
        if bstack11l111ll_opy_.bstack111llll1_opy_():
            self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"ࠩ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠨॎ"))
            self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"ࠪࡘࡷࡻࡥࠨॏ"))
        self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"ࠫ࠲ࡶࠧॐ"))
        self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠪ॑"))
        self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"࠭࠭࠮ࡦࡵ࡭ࡻ࡫ࡲࠨ॒"))
        self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"))
        if self.bstack11l11l1l_opy_ > 1:
            self.bstack111l1l11_opy_.append(bstack11ll1l_opy_ (u"ࠨ࠯ࡱࠫ॔"))
            self.bstack111l1l11_opy_.append(str(self.bstack11l11l1l_opy_))
    def bstack11l1111l_opy_(self):
        bstack11l1l1l1_opy_ = []
        for spec in self.bstack111l1lll_opy_:
            bstack1111llll_opy_ = [spec]
            bstack1111llll_opy_ += self.bstack111l1l11_opy_
            bstack11l1l1l1_opy_.append(bstack1111llll_opy_)
        self.bstack11l1l1l1_opy_ = bstack11l1l1l1_opy_
        return bstack11l1l1l1_opy_
    def bstack11l1l1ll_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack111l111l_opy_ = True
            return True
        except Exception as e:
            self.bstack111l111l_opy_ = False
        return self.bstack111l111l_opy_
    def bstack111ll11l_opy_(self, bstack11l1l11l_opy_, bstack111l1111_opy_):
        bstack111l1111_opy_[bstack11ll1l_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩॕ")] = self.bstack11l1llll_opy_
        multiprocessing.set_start_method(bstack11ll1l_opy_ (u"ࠪࡷࡵࡧࡷ࡯ࠩॖ"))
        bstack11ll1111_opy_ = []
        manager = multiprocessing.Manager()
        bstack11l11lll_opy_ = manager.list()
        if bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧॗ") in self.bstack11l1llll_opy_:
            for index, platform in enumerate(self.bstack11l1llll_opy_[bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨक़")]):
                bstack11ll1111_opy_.append(multiprocessing.Process(name=str(index),
                                                            target=bstack11l1l11l_opy_,
                                                            args=(self.bstack111l1l11_opy_, bstack111l1111_opy_, bstack11l11lll_opy_)))
            bstack111ll1ll_opy_ = len(self.bstack11l1llll_opy_[bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩख़")])
        else:
            bstack11ll1111_opy_.append(multiprocessing.Process(name=str(0),
                                                        target=bstack11l1l11l_opy_,
                                                        args=(self.bstack111l1l11_opy_, bstack111l1111_opy_, bstack11l11lll_opy_)))
            bstack111ll1ll_opy_ = 1
        i = 0
        for t in bstack11ll1111_opy_:
            os.environ[bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧग़")] = str(i)
            if bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫज़") in self.bstack11l1llll_opy_:
                os.environ[bstack11ll1l_opy_ (u"ࠩࡆ࡙ࡗࡘࡅࡏࡖࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡊࡁࡕࡃࠪड़")] = json.dumps(self.bstack11l1llll_opy_[bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ढ़")][i % bstack111ll1ll_opy_])
            i += 1
            t.start()
        for t in bstack11ll1111_opy_:
            t.join()
        return list(bstack11l11lll_opy_)
    @staticmethod
    def bstack111l11l1_opy_(driver, bstack111lll11_opy_, logger, item=None, wait=False):
        item = item or getattr(threading.current_thread(), bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨफ़"), None)
        if item and getattr(item, bstack11ll1l_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡹ࡫ࡳࡵࡡࡦࡥࡸ࡫ࠧय़"), None) and not getattr(item, bstack11ll1l_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡰࡲࡢࡨࡴࡴࡥࠨॠ"), False):
            logger.info(
                bstack11ll1l_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠥࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡪࡵࠣࡹࡳࡪࡥࡳࡹࡤࡽ࠳ࠨॡ"))
            bstack11l1lll1_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack111lll1l_opy_.bstack11l11ll1_opy_(driver, item.name, item.path)
            item._a11y_stop_done = True
            if wait:
                sleep(2)