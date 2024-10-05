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
import builtins
import logging
class bstack1l1l1111_opy_:
    def __init__(self, handler):
        self._111ll1l1l1_opy_ = builtins.print
        self.handler = handler
        self._started = False
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self._111ll1l111_opy_ = {
            level: getattr(self.logger, level)
            for level in [bstack11ll1l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ပ"), bstack11ll1l_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨဖ"), bstack11ll1l_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫဗ"), bstack11ll1l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪဘ")]
        }
    def start(self):
        if self._started:
            return
        self._started = True
        builtins.print = self._111ll1ll11_opy_
        self._111ll1l1ll_opy_()
    def _111ll1ll11_opy_(self, *args, **kwargs):
        self._111ll1l1l1_opy_(*args, **kwargs)
        message = bstack11ll1l_opy_ (u"ࠬࠦࠧမ").join(map(str, args)) + bstack11ll1l_opy_ (u"࠭࡜࡯ࠩယ")
        self._log_message(bstack11ll1l_opy_ (u"ࠧࡊࡐࡉࡓࠬရ"), message)
    def _log_message(self, level, msg, *args, **kwargs):
        if self.handler:
            self.handler({bstack11ll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧလ"): level, bstack11ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪဝ"): msg})
    def _111ll1l1ll_opy_(self):
        for level, bstack111ll1l11l_opy_ in self._111ll1l111_opy_.items():
            setattr(logging, level, self._111ll11lll_opy_(level, bstack111ll1l11l_opy_))
    def _111ll11lll_opy_(self, level, bstack111ll1l11l_opy_):
        def wrapper(msg, *args, **kwargs):
            bstack111ll1l11l_opy_(msg, *args, **kwargs)
            self._log_message(level.upper(), msg)
        return wrapper
    def reset(self):
        if not self._started:
            return
        self._started = False
        builtins.print = self._111ll1l1l1_opy_
        for level, bstack111ll1l11l_opy_ in self._111ll1l111_opy_.items():
            setattr(logging, level, bstack111ll1l11l_opy_)