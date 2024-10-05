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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack111l111lll_opy_
from browserstack_sdk.bstack11l1ll11_opy_ import bstack11l1l111_opy_
def _1lllllll111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack1lllllllll1_opy_:
    def __init__(self, handler):
        self._1lllllll1ll_opy_ = {}
        self._1llllll1l1l_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack11l1l111_opy_.version()
        if bstack111l111lll_opy_(pytest_version, bstack11ll1l_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨᓁ")) >= 0:
            self._1lllllll1ll_opy_[bstack11ll1l_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓂ")] = Module._register_setup_function_fixture
            self._1lllllll1ll_opy_[bstack11ll1l_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᓃ")] = Module._register_setup_module_fixture
            self._1lllllll1ll_opy_[bstack11ll1l_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᓄ")] = Class._register_setup_class_fixture
            self._1lllllll1ll_opy_[bstack11ll1l_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓅ")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack1lllllll1l1_opy_(bstack11ll1l_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᓆ"))
            Module._register_setup_module_fixture = self.bstack1lllllll1l1_opy_(bstack11ll1l_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᓇ"))
            Class._register_setup_class_fixture = self.bstack1lllllll1l1_opy_(bstack11ll1l_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᓈ"))
            Class._register_setup_method_fixture = self.bstack1lllllll1l1_opy_(bstack11ll1l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᓉ"))
        else:
            self._1lllllll1ll_opy_[bstack11ll1l_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᓊ")] = Module._inject_setup_function_fixture
            self._1lllllll1ll_opy_[bstack11ll1l_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓋ")] = Module._inject_setup_module_fixture
            self._1lllllll1ll_opy_[bstack11ll1l_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᓌ")] = Class._inject_setup_class_fixture
            self._1lllllll1ll_opy_[bstack11ll1l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᓍ")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack1lllllll1l1_opy_(bstack11ll1l_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᓎ"))
            Module._inject_setup_module_fixture = self.bstack1lllllll1l1_opy_(bstack11ll1l_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᓏ"))
            Class._inject_setup_class_fixture = self.bstack1lllllll1l1_opy_(bstack11ll1l_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᓐ"))
            Class._inject_setup_method_fixture = self.bstack1lllllll1l1_opy_(bstack11ll1l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᓑ"))
    def bstack1llllllllll_opy_(self, bstack1llllll1l11_opy_, hook_type):
        meth = getattr(bstack1llllll1l11_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._1llllll1l1l_opy_[hook_type] = meth
            setattr(bstack1llllll1l11_opy_, hook_type, self.bstack1lllllll11l_opy_(hook_type))
    def bstack1llllll11l1_opy_(self, instance, bstack1llllll1lll_opy_):
        if bstack1llllll1lll_opy_ == bstack11ll1l_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᓒ"):
            self.bstack1llllllllll_opy_(instance.obj, bstack11ll1l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᓓ"))
            self.bstack1llllllllll_opy_(instance.obj, bstack11ll1l_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᓔ"))
        if bstack1llllll1lll_opy_ == bstack11ll1l_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᓕ"):
            self.bstack1llllllllll_opy_(instance.obj, bstack11ll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨᓖ"))
            self.bstack1llllllllll_opy_(instance.obj, bstack11ll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥᓗ"))
        if bstack1llllll1lll_opy_ == bstack11ll1l_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᓘ"):
            self.bstack1llllllllll_opy_(instance.obj, bstack11ll1l_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᓙ"))
            self.bstack1llllllllll_opy_(instance.obj, bstack11ll1l_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᓚ"))
        if bstack1llllll1lll_opy_ == bstack11ll1l_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᓛ"):
            self.bstack1llllllllll_opy_(instance.obj, bstack11ll1l_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᓜ"))
            self.bstack1llllllllll_opy_(instance.obj, bstack11ll1l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᓝ"))
    @staticmethod
    def bstack1llllllll1l_opy_(hook_type, func, args):
        if hook_type in [bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᓞ"), bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᓟ")]:
            _1lllllll111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack1lllllll11l_opy_(self, hook_type):
        def bstack1llllll111l_opy_(arg=None):
            self.handler(hook_type, bstack11ll1l_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᓠ"))
            result = None
            exception = None
            try:
                self.bstack1llllllll1l_opy_(hook_type, self._1llllll1l1l_opy_[hook_type], (arg,))
                result = Result(result=bstack11ll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᓡ"))
            except Exception as e:
                result = Result(result=bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᓢ"), exception=e)
                self.handler(hook_type, bstack11ll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᓣ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᓤ"), result)
        def bstack1llllllll11_opy_(this, arg=None):
            self.handler(hook_type, bstack11ll1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᓥ"))
            result = None
            exception = None
            try:
                self.bstack1llllllll1l_opy_(hook_type, self._1llllll1l1l_opy_[hook_type], (this, arg))
                result = Result(result=bstack11ll1l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᓦ"))
            except Exception as e:
                result = Result(result=bstack11ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᓧ"), exception=e)
                self.handler(hook_type, bstack11ll1l_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᓨ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack11ll1l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᓩ"), result)
        if hook_type in [bstack11ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᓪ"), bstack11ll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᓫ")]:
            return bstack1llllllll11_opy_
        return bstack1llllll111l_opy_
    def bstack1lllllll1l1_opy_(self, bstack1llllll1lll_opy_):
        def bstack1llllll1ll1_opy_(this, *args, **kwargs):
            self.bstack1llllll11l1_opy_(this, bstack1llllll1lll_opy_)
            self._1lllllll1ll_opy_[bstack1llllll1lll_opy_](this, *args, **kwargs)
        return bstack1llllll1ll1_opy_