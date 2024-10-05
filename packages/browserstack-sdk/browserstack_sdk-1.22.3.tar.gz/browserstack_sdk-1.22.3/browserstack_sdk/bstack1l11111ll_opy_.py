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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack1ll11l1l_opy_ import bstack1ll1ll1l_opy_, bstack1l1lll1l_opy_
from bstack_utils.bstack1ll1l1ll_opy_ import bstack1lll11ll_opy_
from bstack_utils.helper import bstack1ll11111_opy_, bstack1lll11l1_opy_, Result
from bstack_utils.bstack1l1l111l_opy_ import bstack1l1llll1_opy_
from bstack_utils.capture import bstack1l1l1111_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack1l11111ll_opy_:
    def __init__(self):
        self.bstack1lll1ll1_opy_ = bstack1l1l1111_opy_(self.bstack11lll111_opy_)
        self.tests = {}
    @staticmethod
    def bstack11lll111_opy_(log):
        if not (log[bstack11ll1l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩື")] and log[bstack11ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧຸࠪ")].strip()):
            return
        active = bstack1lll11ll_opy_.bstack1ll111l1_opy_()
        log = {
            bstack11ll1l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ູࠩ"): log[bstack11ll1l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮຺ࠪ")],
            bstack11ll1l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨົ"): bstack1lll11l1_opy_(),
            bstack11ll1l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧຼ"): log[bstack11ll1l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨຽ")],
        }
        if active:
            if active[bstack11ll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭຾")] == bstack11ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ຿"):
                log[bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪເ")] = active[bstack11ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫແ")]
            elif active[bstack11ll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪໂ")] == bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷࠫໃ"):
                log[bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧໄ")] = active[bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ໅")]
        bstack1l1llll1_opy_.bstack1ll11l11_opy_([log])
    def start_test(self, attrs):
        bstack11l1l1111l_opy_ = uuid4().__str__()
        self.tests[bstack11l1l1111l_opy_] = {}
        self.bstack1lll1ll1_opy_.start()
        driver = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨໆ"), None)
        bstack1ll11l1l_opy_ = bstack1l1lll1l_opy_(
            name=attrs.scenario.name,
            uuid=bstack11l1l1111l_opy_,
            bstack1l111111_opy_=bstack1lll11l1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack11ll1l_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ໇"),
            framework=bstack11ll1l_opy_ (u"ࠫࡇ࡫ࡨࡢࡸࡨ່ࠫ"),
            scope=[attrs.feature.name],
            bstack1l1lllll_opy_=bstack1l1llll1_opy_.bstack11llllll_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[bstack11l1l1111l_opy_][bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ້")] = bstack1ll11l1l_opy_
        threading.current_thread().current_test_uuid = bstack11l1l1111l_opy_
        bstack1l1llll1_opy_.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪ໊ࠧ"), bstack1ll11l1l_opy_)
    def end_test(self, attrs):
        bstack11l11llll1_opy_ = {
            bstack11ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩ໋ࠧ"): attrs.feature.name,
            bstack11ll1l_opy_ (u"ࠣࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࠨ໌"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack1ll11l1l_opy_ = self.tests[current_test_uuid][bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬໍ")]
        meta = {
            bstack11ll1l_opy_ (u"ࠥࡪࡪࡧࡴࡶࡴࡨࠦ໎"): bstack11l11llll1_opy_,
            bstack11ll1l_opy_ (u"ࠦࡸࡺࡥࡱࡵࠥ໏"): bstack1ll11l1l_opy_.meta.get(bstack11ll1l_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ໐"), []),
            bstack11ll1l_opy_ (u"ࠨࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ໑"): {
                bstack11ll1l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ໒"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack1ll11l1l_opy_.bstack11l1l11111_opy_(meta)
        bstack1ll11l1l_opy_.bstack11l11lllll_opy_(bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸ࠭໓"), []))
        bstack11l11lll11_opy_, exception = self._11l11ll11l_opy_(attrs)
        bstack1l1l1l1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack1ll1llll_opy_=[bstack11l11lll11_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack11ll1l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໔")].stop(time=bstack1lll11l1_opy_(), duration=int(attrs.duration)*1000, result=bstack1l1l1l1l_opy_)
        bstack1l1llll1_opy_.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ໕"), self.tests[threading.current_thread().current_test_uuid][bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໖")])
    def bstack1llll1lll_opy_(self, attrs):
        bstack1llll1ll_opy_ = {
            bstack11ll1l_opy_ (u"ࠬ࡯ࡤࠨ໗"): uuid4().__str__(),
            bstack11ll1l_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧ໘"): attrs.keyword,
            bstack11ll1l_opy_ (u"ࠧࡴࡶࡨࡴࡤࡧࡲࡨࡷࡰࡩࡳࡺࠧ໙"): [],
            bstack11ll1l_opy_ (u"ࠨࡶࡨࡼࡹ࠭໚"): attrs.name,
            bstack11ll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭໛"): bstack1lll11l1_opy_(),
            bstack11ll1l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪໜ"): bstack11ll1l_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬໝ"),
            bstack11ll1l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪໞ"): bstack11ll1l_opy_ (u"࠭ࠧໟ")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ໠")].add_step(bstack1llll1ll_opy_)
        threading.current_thread().current_step_uuid = bstack1llll1ll_opy_[bstack11ll1l_opy_ (u"ࠨ࡫ࡧࠫ໡")]
    def bstack1l111ll11l_opy_(self, attrs):
        current_test_id = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭໢"), None)
        current_step_uuid = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡸࡺࡥࡱࡡࡸࡹ࡮ࡪࠧ໣"), None)
        bstack11l11lll11_opy_, exception = self._11l11ll11l_opy_(attrs)
        bstack1l1l1l1l_opy_ = Result(result=attrs.status.name, exception=exception, bstack1ll1llll_opy_=[bstack11l11lll11_opy_])
        self.tests[current_test_id][bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໤")].bstack1l11l1ll_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack1l1l1l1l_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11llll11l_opy_(self, name, attrs):
        try:
            bstack11l11ll1ll_opy_ = uuid4().__str__()
            self.tests[bstack11l11ll1ll_opy_] = {}
            self.bstack1lll1ll1_opy_.start()
            scopes = []
            driver = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫ໥"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡶࠫ໦")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack11l11ll1ll_opy_)
            if name in [bstack11ll1l_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠦ໧"), bstack11ll1l_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦ໨")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack11ll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡩࡩࡦࡺࡵࡳࡧࠥ໩"), bstack11ll1l_opy_ (u"ࠥࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠥ໪")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack11ll1l_opy_ (u"ࠫ࡫࡫ࡡࡵࡷࡵࡩࠬ໫")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack1ll1ll1l_opy_(
                name=name,
                uuid=bstack11l11ll1ll_opy_,
                bstack1l111111_opy_=bstack1lll11l1_opy_(),
                file_path=file_path,
                framework=bstack11ll1l_opy_ (u"ࠧࡈࡥࡩࡣࡹࡩࠧ໬"),
                bstack1l1lllll_opy_=bstack1l1llll1_opy_.bstack11llllll_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack11ll1l_opy_ (u"ࠨࡰࡦࡰࡧ࡭ࡳ࡭ࠢ໭"),
                hook_type=name
            )
            self.tests[bstack11l11ll1ll_opy_][bstack11ll1l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡡࡵࡣࠥ໮")] = hook_data
            current_test_id = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠣࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠧ໯"), None)
            if current_test_id:
                hook_data.bstack11l11ll1l1_opy_(current_test_id)
            if name == bstack11ll1l_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨ໰"):
                threading.current_thread().before_all_hook_uuid = bstack11l11ll1ll_opy_
            threading.current_thread().current_hook_uuid = bstack11l11ll1ll_opy_
            bstack1l1llll1_opy_.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"ࠥࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠦ໱"), hook_data)
        except Exception as e:
            logger.debug(bstack11ll1l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࠠࡩࡱࡲ࡯ࠥ࡫ࡶࡦࡰࡷࡷ࠱ࠦࡨࡰࡱ࡮ࠤࡳࡧ࡭ࡦ࠼ࠣࠩࡸ࠲ࠠࡦࡴࡵࡳࡷࡀࠠࠦࡵࠥ໲"), name, e)
    def bstack1111llll1_opy_(self, attrs):
        bstack1l111l11_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ໳"), None)
        hook_data = self.tests[bstack1l111l11_opy_][bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ໴")]
        status = bstack11ll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ໵")
        exception = None
        bstack11l11lll11_opy_ = None
        if hook_data.name == bstack11ll1l_opy_ (u"ࠣࡣࡩࡸࡪࡸ࡟ࡢ࡮࡯ࠦ໶"):
            self.bstack1lll1ll1_opy_.reset()
            bstack11l11lll1l_opy_ = self.tests[bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ໷"), None)][bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭໸")].result.result
            if bstack11l11lll1l_opy_ == bstack11ll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ໹"):
                if attrs.hook_failures == 1:
                    status = bstack11ll1l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ໺")
                elif attrs.hook_failures == 2:
                    status = bstack11ll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ໻")
            elif attrs.bstack11l11ll111_opy_:
                status = bstack11ll1l_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ໼")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack11ll1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ໽") and attrs.hook_failures == 1:
                status = bstack11ll1l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤ໾")
            elif hasattr(attrs, bstack11ll1l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪ໿")) and attrs.error_message:
                status = bstack11ll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦༀ")
            bstack11l11lll11_opy_, exception = self._11l11ll11l_opy_(attrs)
        bstack1l1l1l1l_opy_ = Result(result=status, exception=exception, bstack1ll1llll_opy_=[bstack11l11lll11_opy_])
        hook_data.stop(time=bstack1lll11l1_opy_(), duration=0, result=bstack1l1l1l1l_opy_)
        bstack1l1llll1_opy_.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ༁"), self.tests[bstack1l111l11_opy_][bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ༂")])
        threading.current_thread().current_hook_uuid = None
    def _11l11ll11l_opy_(self, attrs):
        try:
            import traceback
            bstack1l1l1l111_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l11lll11_opy_ = bstack1l1l1l111_opy_[-1] if bstack1l1l1l111_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack11ll1l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦ࡯ࡤࡥࡸࡶࡷ࡫ࡤࠡࡹ࡫࡭ࡱ࡫ࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡵࡥࡨ࡫ࡢࡢࡥ࡮ࠦ༃"))
            bstack11l11lll11_opy_ = None
            exception = None
        return bstack11l11lll11_opy_, exception