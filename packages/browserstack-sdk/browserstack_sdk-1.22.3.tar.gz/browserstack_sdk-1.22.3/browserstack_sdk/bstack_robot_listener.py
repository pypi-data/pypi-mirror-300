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
import threading
from uuid import uuid4
from itertools import zip_longest
from collections import OrderedDict
from robot.libraries.BuiltIn import BuiltIn
from browserstack_sdk.bstack1l11l111_opy_ import RobotHandler
from bstack_utils.capture import bstack1l1l1111_opy_
from bstack_utils.bstack1ll11l1l_opy_ import bstack1l1l1l11_opy_, bstack1ll1ll1l_opy_, bstack1l1lll1l_opy_
from bstack_utils.bstack1ll1l1ll_opy_ import bstack1lll11ll_opy_
from bstack_utils.bstack1l1l111l_opy_ import bstack1l1llll1_opy_
from bstack_utils.constants import *
from bstack_utils.helper import bstack1ll11111_opy_, bstack1lll11l1_opy_, Result, \
    bstack11lll11l_opy_, bstack11llll1l_opy_
class bstack_robot_listener:
    ROBOT_LISTENER_API_VERSION = 2
    store = {
        bstack11ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣ࡭ࡵ࡯࡬ࡡࡸࡹ࡮ࡪࠧࡶ"): [],
        bstack11ll1l_opy_ (u"ࠫ࡬ࡲ࡯ࡣࡣ࡯ࡣ࡭ࡵ࡯࡬ࡵࠪࡷ"): [],
        bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡴࠩࡸ"): []
    }
    bstack1l11ll1l_opy_ = []
    bstack11llll11_opy_ = []
    @staticmethod
    def bstack11lll111_opy_(log):
        if not (log[bstack11ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧࡹ")] and log[bstack11ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨࡺ")].strip()):
            return
        active = bstack1lll11ll_opy_.bstack1ll111l1_opy_()
        log = {
            bstack11ll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧࡻ"): log[bstack11ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨࡼ")],
            bstack11ll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ࡽ"): bstack11llll1l_opy_().isoformat() + bstack11ll1l_opy_ (u"ࠫ࡟࠭ࡾ"),
            bstack11ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ࡿ"): log[bstack11ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧࢀ")],
        }
        if active:
            if active[bstack11ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬࢁ")] == bstack11ll1l_opy_ (u"ࠨࡪࡲࡳࡰ࠭ࢂ"):
                log[bstack11ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩࢃ")] = active[bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪࢄ")]
            elif active[bstack11ll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩࢅ")] == bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࠪࢆ"):
                log[bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ࢇ")] = active[bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ࢈")]
        bstack1l1llll1_opy_.bstack1ll11l11_opy_([log])
    def __init__(self):
        self.messages = Messages()
        self._1lll1111_opy_ = None
        self._1lll1lll_opy_ = None
        self._1lll111l_opy_ = OrderedDict()
        self.bstack1lll1ll1_opy_ = bstack1l1l1111_opy_(self.bstack11lll111_opy_)
    @bstack11lll11l_opy_(class_method=True)
    def start_suite(self, name, attrs):
        self.messages.bstack1l111lll_opy_()
        if not self._1lll111l_opy_.get(attrs.get(bstack11ll1l_opy_ (u"ࠨ࡫ࡧࠫࢉ")), None):
            self._1lll111l_opy_[attrs.get(bstack11ll1l_opy_ (u"ࠩ࡬ࡨࠬࢊ"))] = {}
        bstack1l11lll1_opy_ = bstack1l1lll1l_opy_(
                bstack1ll1l1l1_opy_=attrs.get(bstack11ll1l_opy_ (u"ࠪ࡭ࡩ࠭ࢋ")),
                name=name,
                bstack1l111111_opy_=bstack1lll11l1_opy_(),
                file_path=os.path.relpath(attrs[bstack11ll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫࢌ")], start=os.getcwd()) if attrs.get(bstack11ll1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬࢍ")) != bstack11ll1l_opy_ (u"࠭ࠧࢎ") else bstack11ll1l_opy_ (u"ࠧࠨ࢏"),
                framework=bstack11ll1l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ࢐")
            )
        threading.current_thread().current_suite_id = attrs.get(bstack11ll1l_opy_ (u"ࠩ࡬ࡨࠬ࢑"), None)
        self._1lll111l_opy_[attrs.get(bstack11ll1l_opy_ (u"ࠪ࡭ࡩ࠭࢒"))][bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ࢓")] = bstack1l11lll1_opy_
    @bstack11lll11l_opy_(class_method=True)
    def end_suite(self, name, attrs):
        messages = self.messages.bstack1ll11lll_opy_()
        self._1l11ll11_opy_(messages)
        for bstack1ll1l11l_opy_ in self.bstack1l11ll1l_opy_:
            bstack1ll1l11l_opy_[bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ࢔")][bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ࢕")].extend(self.store[bstack11ll1l_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲ࡟ࡩࡱࡲ࡯ࡸ࠭࢖")])
            bstack1l1llll1_opy_.bstack1l1l1lll_opy_(bstack1ll1l11l_opy_)
        self.bstack1l11ll1l_opy_ = []
        self.store[bstack11ll1l_opy_ (u"ࠨࡩ࡯ࡳࡧࡧ࡬ࡠࡪࡲࡳࡰࡹࠧࢗ")] = []
    @bstack11lll11l_opy_(class_method=True)
    def start_test(self, name, attrs):
        self.bstack1lll1ll1_opy_.start()
        if not self._1lll111l_opy_.get(attrs.get(bstack11ll1l_opy_ (u"ࠩ࡬ࡨࠬ࢘")), None):
            self._1lll111l_opy_[attrs.get(bstack11ll1l_opy_ (u"ࠪ࡭ࡩ࢙࠭"))] = {}
        driver = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴ࢚ࠪ"), None)
        bstack1ll11l1l_opy_ = bstack1l1lll1l_opy_(
            bstack1ll1l1l1_opy_=attrs.get(bstack11ll1l_opy_ (u"ࠬ࡯ࡤࠨ࢛")),
            name=name,
            bstack1l111111_opy_=bstack1lll11l1_opy_(),
            file_path=os.path.relpath(attrs[bstack11ll1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭࢜")], start=os.getcwd()),
            scope=RobotHandler.bstack11ll1ll1_opy_(attrs.get(bstack11ll1l_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ࢝"), None)),
            framework=bstack11ll1l_opy_ (u"ࠨࡔࡲࡦࡴࡺࠧ࢞"),
            tags=attrs[bstack11ll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ࢟")],
            hooks=self.store[bstack11ll1l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮ࡢ࡬ࡴࡵ࡫ࡴࠩࢠ")],
            bstack1l1lllll_opy_=bstack1l1llll1_opy_.bstack11llllll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            code=bstack11ll1l_opy_ (u"ࠦࢀࢃࠠ࡝ࡰࠣࡿࢂࠨࢡ").format(bstack11ll1l_opy_ (u"ࠧࠦࠢࢢ").join(attrs[bstack11ll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫࢣ")]), name) if attrs[bstack11ll1l_opy_ (u"ࠧࡵࡣࡪࡷࠬࢤ")] else name
        )
        self._1lll111l_opy_[attrs.get(bstack11ll1l_opy_ (u"ࠨ࡫ࡧࠫࢥ"))][bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬࢦ")] = bstack1ll11l1l_opy_
        threading.current_thread().current_test_uuid = bstack1ll11l1l_opy_.bstack1l11l11l_opy_()
        threading.current_thread().current_test_id = attrs.get(bstack11ll1l_opy_ (u"ࠪ࡭ࡩ࠭ࢧ"), None)
        self.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬࢨ"), bstack1ll11l1l_opy_)
    @bstack11lll11l_opy_(class_method=True)
    def end_test(self, name, attrs):
        self.bstack1lll1ll1_opy_.reset()
        bstack1l11l1l1_opy_ = bstack1l1l11ll_opy_.get(attrs.get(bstack11ll1l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬࢩ")), bstack11ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧࢪ"))
        self._1lll111l_opy_[attrs.get(bstack11ll1l_opy_ (u"ࠧࡪࡦࠪࢫ"))][bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫࢬ")].stop(time=bstack1lll11l1_opy_(), duration=int(attrs.get(bstack11ll1l_opy_ (u"ࠩࡨࡰࡦࡶࡳࡦࡦࡷ࡭ࡲ࡫ࠧࢭ"), bstack11ll1l_opy_ (u"ࠪ࠴ࠬࢮ"))), result=Result(result=bstack1l11l1l1_opy_, exception=attrs.get(bstack11ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬࢯ")), bstack1ll1llll_opy_=[attrs.get(bstack11ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ࢰ"))]))
        self.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨࢱ"), self._1lll111l_opy_[attrs.get(bstack11ll1l_opy_ (u"ࠧࡪࡦࠪࢲ"))][bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫࢳ")], True)
        self.store[bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭ࢴ")] = []
        threading.current_thread().current_test_uuid = None
        threading.current_thread().current_test_id = None
    @bstack11lll11l_opy_(class_method=True)
    def start_keyword(self, name, attrs):
        self.messages.bstack1l111lll_opy_()
        current_test_id = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡨࠬࢵ"), None)
        bstack1llll1l1_opy_ = current_test_id if bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡩ࠭ࢶ"), None) else bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡳࡶ࡫ࡷࡩࡤ࡯ࡤࠨࢷ"), None)
        if attrs.get(bstack11ll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫࢸ"), bstack11ll1l_opy_ (u"ࠧࠨࢹ")).lower() in [bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧࢺ"), bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫࢻ")]:
            hook_type = bstack1l111ll1_opy_(attrs.get(bstack11ll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨࢼ")), bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨࢽ"), None))
            hook_name = bstack11ll1l_opy_ (u"ࠬࢁࡽࠨࢾ").format(attrs.get(bstack11ll1l_opy_ (u"࠭࡫ࡸࡰࡤࡱࡪ࠭ࢿ"), bstack11ll1l_opy_ (u"ࠧࠨࣀ")))
            if hook_type in [bstack11ll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡃࡏࡐࠬࣁ"), bstack11ll1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬࣂ")]:
                hook_name = bstack11ll1l_opy_ (u"ࠪ࡟ࢀࢃ࡝ࠡࡽࢀࠫࣃ").format(bstack1l1ll1ll_opy_.get(hook_type), attrs.get(bstack11ll1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫࣄ"), bstack11ll1l_opy_ (u"ࠬ࠭ࣅ")))
            bstack1l1lll11_opy_ = bstack1ll1ll1l_opy_(
                bstack1ll1l1l1_opy_=bstack1llll1l1_opy_ + bstack11ll1l_opy_ (u"࠭࠭ࠨࣆ") + attrs.get(bstack11ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬࣇ"), bstack11ll1l_opy_ (u"ࠨࠩࣈ")).lower(),
                name=hook_name,
                bstack1l111111_opy_=bstack1lll11l1_opy_(),
                file_path=os.path.relpath(attrs.get(bstack11ll1l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩࣉ")), start=os.getcwd()),
                framework=bstack11ll1l_opy_ (u"ࠪࡖࡴࡨ࡯ࡵࠩ࣊"),
                tags=attrs[bstack11ll1l_opy_ (u"ࠫࡹࡧࡧࡴࠩ࣋")],
                scope=RobotHandler.bstack11ll1ll1_opy_(attrs.get(bstack11ll1l_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬ࣌"), None)),
                hook_type=hook_type,
                meta={}
            )
            threading.current_thread().current_hook_uuid = bstack1l1lll11_opy_.bstack1l11l11l_opy_()
            threading.current_thread().current_hook_id = bstack1llll1l1_opy_ + bstack11ll1l_opy_ (u"࠭࠭ࠨ࣍") + attrs.get(bstack11ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬ࣎"), bstack11ll1l_opy_ (u"ࠨ࣏ࠩ")).lower()
            self.store[bstack11ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࣐࠭")] = [bstack1l1lll11_opy_.bstack1l11l11l_opy_()]
            if bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪ࣑ࠧ"), None):
                self.store[bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ࣒")].append(bstack1l1lll11_opy_.bstack1l11l11l_opy_())
            else:
                self.store[bstack11ll1l_opy_ (u"ࠬ࡭࡬ࡰࡤࡤࡰࡤ࡮࡯ࡰ࡭ࡶ࣓ࠫ")].append(bstack1l1lll11_opy_.bstack1l11l11l_opy_())
            if bstack1llll1l1_opy_:
                self._1lll111l_opy_[bstack1llll1l1_opy_ + bstack11ll1l_opy_ (u"࠭࠭ࠨࣔ") + attrs.get(bstack11ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬࣕ"), bstack11ll1l_opy_ (u"ࠨࠩࣖ")).lower()] = { bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬࣗ"): bstack1l1lll11_opy_ }
            bstack1l1llll1_opy_.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫࣘ"), bstack1l1lll11_opy_)
        else:
            bstack1llll1ll_opy_ = {
                bstack11ll1l_opy_ (u"ࠫ࡮ࡪࠧࣙ"): uuid4().__str__(),
                bstack11ll1l_opy_ (u"ࠬࡺࡥࡹࡶࠪࣚ"): bstack11ll1l_opy_ (u"࠭ࡻࡾࠢࡾࢁࠬࣛ").format(attrs.get(bstack11ll1l_opy_ (u"ࠧ࡬ࡹࡱࡥࡲ࡫ࠧࣜ")), attrs.get(bstack11ll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ࣝ"), bstack11ll1l_opy_ (u"ࠩࠪࣞ"))) if attrs.get(bstack11ll1l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨࣟ"), []) else attrs.get(bstack11ll1l_opy_ (u"ࠫࡰࡽ࡮ࡢ࡯ࡨࠫ࣠")),
                bstack11ll1l_opy_ (u"ࠬࡹࡴࡦࡲࡢࡥࡷ࡭ࡵ࡮ࡧࡱࡸࠬ࣡"): attrs.get(bstack11ll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫ࣢"), []),
                bstack11ll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࣣࠫ"): bstack1lll11l1_opy_(),
                bstack11ll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨࣤ"): bstack11ll1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪࣥ"),
                bstack11ll1l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨࣦ"): attrs.get(bstack11ll1l_opy_ (u"ࠫࡩࡵࡣࠨࣧ"), bstack11ll1l_opy_ (u"ࠬ࠭ࣨ"))
            }
            if attrs.get(bstack11ll1l_opy_ (u"࠭࡬ࡪࡤࡱࡥࡲ࡫ࣩࠧ"), bstack11ll1l_opy_ (u"ࠧࠨ࣪")) != bstack11ll1l_opy_ (u"ࠨࠩ࣫"):
                bstack1llll1ll_opy_[bstack11ll1l_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪ࣬")] = attrs.get(bstack11ll1l_opy_ (u"ࠪࡰ࡮ࡨ࡮ࡢ࡯ࡨ࣭ࠫ"))
            if not self.bstack11llll11_opy_:
                self._1lll111l_opy_[self._1llll111_opy_()][bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧ࣮ࠧ")].add_step(bstack1llll1ll_opy_)
                threading.current_thread().current_step_uuid = bstack1llll1ll_opy_[bstack11ll1l_opy_ (u"ࠬ࡯ࡤࠨ࣯")]
            self.bstack11llll11_opy_.append(bstack1llll1ll_opy_)
    @bstack11lll11l_opy_(class_method=True)
    def end_keyword(self, name, attrs):
        messages = self.messages.bstack1ll11lll_opy_()
        self._1l11ll11_opy_(messages)
        current_test_id = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡤࠨࣰ"), None)
        bstack1llll1l1_opy_ = current_test_id if current_test_id else bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡸ࡭ࡹ࡫࡟ࡪࡦࣱࠪ"), None)
        bstack1l1ll11l_opy_ = bstack1l1l11ll_opy_.get(attrs.get(bstack11ll1l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨࣲ")), bstack11ll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪࣳ"))
        bstack1lll1l11_opy_ = attrs.get(bstack11ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫࣴ"))
        if bstack1l1ll11l_opy_ != bstack11ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬࣵ") and not attrs.get(bstack11ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪࣶ࠭")) and self._1lll1111_opy_:
            bstack1lll1l11_opy_ = self._1lll1111_opy_
        bstack1l1l1l1l_opy_ = Result(result=bstack1l1ll11l_opy_, exception=bstack1lll1l11_opy_, bstack1ll1llll_opy_=[bstack1lll1l11_opy_])
        if attrs.get(bstack11ll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫࣷ"), bstack11ll1l_opy_ (u"ࠧࠨࣸ")).lower() in [bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶࣹࠧ"), bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࣺࠫ")]:
            bstack1llll1l1_opy_ = current_test_id if current_test_id else bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡻࡩࡵࡧࡢ࡭ࡩ࠭ࣻ"), None)
            if bstack1llll1l1_opy_:
                bstack1l111l11_opy_ = bstack1llll1l1_opy_ + bstack11ll1l_opy_ (u"ࠦ࠲ࠨࣼ") + attrs.get(bstack11ll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪࣽ"), bstack11ll1l_opy_ (u"࠭ࠧࣾ")).lower()
                self._1lll111l_opy_[bstack1l111l11_opy_][bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪࣿ")].stop(time=bstack1lll11l1_opy_(), duration=int(attrs.get(bstack11ll1l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭ऀ"), bstack11ll1l_opy_ (u"ࠩ࠳ࠫँ"))), result=bstack1l1l1l1l_opy_)
                bstack1l1llll1_opy_.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬं"), self._1lll111l_opy_[bstack1l111l11_opy_][bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧः")])
        else:
            bstack1llll1l1_opy_ = current_test_id if current_test_id else bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣ࡮ࡪࠧऄ"), None)
            if bstack1llll1l1_opy_ and len(self.bstack11llll11_opy_) == 1:
                current_step_uuid = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡴࡶࡨࡴࡤࡻࡵࡪࡦࠪअ"), None)
                self._1lll111l_opy_[bstack1llll1l1_opy_][bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪआ")].bstack1l11l1ll_opy_(current_step_uuid, duration=int(attrs.get(bstack11ll1l_opy_ (u"ࠨࡧ࡯ࡥࡵࡹࡥࡥࡶ࡬ࡱࡪ࠭इ"), bstack11ll1l_opy_ (u"ࠩ࠳ࠫई"))), result=bstack1l1l1l1l_opy_)
            else:
                self.bstack1lll1l1l_opy_(attrs)
            self.bstack11llll11_opy_.pop()
    def log_message(self, message):
        try:
            if message.get(bstack11ll1l_opy_ (u"ࠪ࡬ࡹࡳ࡬ࠨउ"), bstack11ll1l_opy_ (u"ࠫࡳࡵࠧऊ")) == bstack11ll1l_opy_ (u"ࠬࡿࡥࡴࠩऋ"):
                return
            self.messages.push(message)
            bstack1llll11l_opy_ = []
            if bstack1lll11ll_opy_.bstack1ll111l1_opy_():
                bstack1llll11l_opy_.append({
                    bstack11ll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩऌ"): bstack1lll11l1_opy_(),
                    bstack11ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨऍ"): message.get(bstack11ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩऎ")),
                    bstack11ll1l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨए"): message.get(bstack11ll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩऐ")),
                    **bstack1lll11ll_opy_.bstack1ll111l1_opy_()
                })
                if len(bstack1llll11l_opy_) > 0:
                    bstack1l1llll1_opy_.bstack1ll11l11_opy_(bstack1llll11l_opy_)
        except Exception as err:
            pass
    def close(self):
        bstack1l1llll1_opy_.bstack11lllll1_opy_()
    def bstack1lll1l1l_opy_(self, bstack1ll1ll11_opy_):
        if not bstack1lll11ll_opy_.bstack1ll111l1_opy_():
            return
        kwname = bstack11ll1l_opy_ (u"ࠫࢀࢃࠠࡼࡿࠪऑ").format(bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"ࠬࡱࡷ࡯ࡣࡰࡩࠬऒ")), bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"࠭ࡡࡳࡩࡶࠫओ"), bstack11ll1l_opy_ (u"ࠧࠨऔ"))) if bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭क"), []) else bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"ࠩ࡮ࡻࡳࡧ࡭ࡦࠩख"))
        error_message = bstack11ll1l_opy_ (u"ࠥ࡯ࡼࡴࡡ࡮ࡧ࠽ࠤࡡࠨࡻ࠱ࡿ࡟ࠦࠥࢂࠠࡴࡶࡤࡸࡺࡹ࠺ࠡ࡞ࠥࡿ࠶ࢃ࡜ࠣࠢࡿࠤࡪࡾࡣࡦࡲࡷ࡭ࡴࡴ࠺ࠡ࡞ࠥࡿ࠷ࢃ࡜ࠣࠤग").format(kwname, bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫघ")), str(bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ङ"))))
        bstack11lll1ll_opy_ = bstack11ll1l_opy_ (u"ࠨ࡫ࡸࡰࡤࡱࡪࡀࠠ࡝ࠤࡾ࠴ࢂࡢࠢࠡࡾࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࡡࠨࡻ࠲ࡿ࡟ࠦࠧच").format(kwname, bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧछ")))
        bstack1ll1lll1_opy_ = error_message if bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩज")) else bstack11lll1ll_opy_
        bstack11ll1l1l_opy_ = {
            bstack11ll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬझ"): self.bstack11llll11_opy_[-1].get(bstack11ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧञ"), bstack1lll11l1_opy_()),
            bstack11ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬट"): bstack1ll1lll1_opy_,
            bstack11ll1l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫठ"): bstack11ll1l_opy_ (u"࠭ࡅࡓࡔࡒࡖࠬड") if bstack1ll1ll11_opy_.get(bstack11ll1l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧढ")) == bstack11ll1l_opy_ (u"ࠨࡈࡄࡍࡑ࠭ण") else bstack11ll1l_opy_ (u"ࠩࡌࡒࡋࡕࠧत"),
            **bstack1lll11ll_opy_.bstack1ll111l1_opy_()
        }
        bstack1l1llll1_opy_.bstack1ll11l11_opy_([bstack11ll1l1l_opy_])
    def _1llll111_opy_(self):
        for bstack1ll1l1l1_opy_ in reversed(self._1lll111l_opy_):
            bstack1ll1111l_opy_ = bstack1ll1l1l1_opy_
            data = self._1lll111l_opy_[bstack1ll1l1l1_opy_][bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭थ")]
            if isinstance(data, bstack1ll1ll1l_opy_):
                if not bstack11ll1l_opy_ (u"ࠫࡊࡇࡃࡉࠩद") in data.bstack1ll111ll_opy_():
                    return bstack1ll1111l_opy_
            else:
                return bstack1ll1111l_opy_
    def _1l11ll11_opy_(self, messages):
        try:
            bstack11ll1lll_opy_ = BuiltIn().get_variable_value(bstack11ll1l_opy_ (u"ࠧࠪࡻࡍࡑࡊࠤࡑࡋࡖࡆࡎࢀࠦध")) in (bstack1l11111l_opy_.DEBUG, bstack1l11111l_opy_.TRACE)
            for message, bstack1l11llll_opy_ in zip_longest(messages, messages[1:]):
                name = message.get(bstack11ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧन"))
                level = message.get(bstack11ll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ऩ"))
                if level == bstack1l11111l_opy_.FAIL:
                    self._1lll1111_opy_ = name or self._1lll1111_opy_
                    self._1lll1lll_opy_ = bstack1l11llll_opy_.get(bstack11ll1l_opy_ (u"ࠣ࡯ࡨࡷࡸࡧࡧࡦࠤप")) if bstack11ll1lll_opy_ and bstack1l11llll_opy_ else self._1lll1lll_opy_
        except:
            pass
    @classmethod
    def bstack1l1111l1_opy_(self, event: str, bstack1l1ll111_opy_: bstack1l1l1l11_opy_, bstack1l1ll1l1_opy_=False):
        if event == bstack11ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫफ"):
            bstack1l1ll111_opy_.set(hooks=self.store[bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹࠧब")])
        if event == bstack11ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡱࡩࡱࡲࡨࡨࠬभ"):
            event = bstack11ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧम")
        if bstack1l1ll1l1_opy_:
            bstack11lll1l1_opy_ = {
                bstack11ll1l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪय"): event,
                bstack1l1ll111_opy_.bstack1ll11ll1_opy_(): bstack1l1ll111_opy_.bstack1lllll11_opy_(event)
            }
            self.bstack1l11ll1l_opy_.append(bstack11lll1l1_opy_)
        else:
            bstack1l1llll1_opy_.bstack1l1111l1_opy_(event, bstack1l1ll111_opy_)
class Messages:
    def __init__(self):
        self._1l1l11l1_opy_ = []
    def bstack1l111lll_opy_(self):
        self._1l1l11l1_opy_.append([])
    def bstack1ll11lll_opy_(self):
        return self._1l1l11l1_opy_.pop() if self._1l1l11l1_opy_ else list()
    def push(self, message):
        self._1l1l11l1_opy_[-1].append(message) if self._1l1l11l1_opy_ else self._1l1l11l1_opy_.append([message])
class bstack1l11111l_opy_:
    FAIL = bstack11ll1l_opy_ (u"ࠧࡇࡃࡌࡐࠬर")
    ERROR = bstack11ll1l_opy_ (u"ࠨࡇࡕࡖࡔࡘࠧऱ")
    WARNING = bstack11ll1l_opy_ (u"࡚ࠩࡅࡗࡔࠧल")
    bstack1l1111ll_opy_ = bstack11ll1l_opy_ (u"ࠪࡍࡓࡌࡏࠨळ")
    DEBUG = bstack11ll1l_opy_ (u"ࠫࡉࡋࡂࡖࡉࠪऴ")
    TRACE = bstack11ll1l_opy_ (u"࡚ࠬࡒࡂࡅࡈࠫव")
    bstack1l111l1l_opy_ = [FAIL, ERROR]
def bstack1l1l1ll1_opy_(bstack1ll1l111_opy_):
    if not bstack1ll1l111_opy_:
        return None
    if bstack1ll1l111_opy_.get(bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩश"), None):
        return getattr(bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪष")], bstack11ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭स"), None)
    return bstack1ll1l111_opy_.get(bstack11ll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧह"), None)
def bstack1l111ll1_opy_(hook_type, current_test_uuid):
    if hook_type.lower() not in [bstack11ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩऺ"), bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ऻ")]:
        return
    if hook_type.lower() == bstack11ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳ़ࠫ"):
        if current_test_uuid is None:
            return bstack11ll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪऽ")
        else:
            return bstack11ll1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬा")
    elif hook_type.lower() == bstack11ll1l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪि"):
        if current_test_uuid is None:
            return bstack11ll1l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬी")
        else:
            return bstack11ll1l_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧु")