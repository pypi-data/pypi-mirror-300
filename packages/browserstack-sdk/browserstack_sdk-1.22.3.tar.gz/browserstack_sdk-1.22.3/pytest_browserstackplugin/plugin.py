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
import datetime
import inspect
import logging
import os
import signal
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack11ll11ll1l_opy_, bstack11l1l1lll1_opy_, update, bstack1l111ll111_opy_,
                                       bstack11l111l11_opy_, bstack1111l1lll_opy_, bstack1l111l111l_opy_, bstack1l1lll111_opy_,
                                       bstack11l1lll11_opy_, bstack1l111111l1_opy_, bstack11llllll1_opy_, bstack11l1llllll_opy_,
                                       bstack11ll11l1l1_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1ll1ll11ll_opy_)
from browserstack_sdk.bstack11l1ll11_opy_ import bstack11l1l111_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack1l1ll1ll11_opy_
from bstack_utils.capture import bstack1l1l1111_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack11l1l11l1l_opy_, bstack1l1lll11l1_opy_, bstack1111111l_opy_, \
    bstack11l1ll1lll_opy_
from bstack_utils.helper import bstack1ll11111_opy_, bstack1111111l11_opy_, bstack11llll1l_opy_, bstack1l1l111ll1_opy_, bstack11111l1l1l_opy_, bstack1lll11l1_opy_, \
    bstack1111lll11l_opy_, \
    bstack1111111lll_opy_, bstack11l111lll_opy_, bstack1llll111l_opy_, bstack1111111111_opy_, bstack1ll11l11ll_opy_, Notset, \
    bstack1l1111l11_opy_, bstack1111111ll1_opy_, bstack11111lllll_opy_, Result, bstack111l1l111l_opy_, bstack1111l111l1_opy_, bstack11lll11l_opy_, \
    bstack1ll1ll1111_opy_, bstack111ll1l1l_opy_, bstack1l11lll111_opy_, bstack1111ll111l_opy_
from bstack_utils.bstack1llllll11ll_opy_ import bstack1lllllllll1_opy_
from bstack_utils.messages import bstack11lll111l1_opy_, bstack1l1lll111l_opy_, bstack11lll11ll_opy_, bstack1l11ll11l1_opy_, bstack11l1ll1l_opy_, \
    bstack11lll1l1l_opy_, bstack1lll111l1l_opy_, bstack11lll11l1_opy_, bstack1l1llll11_opy_, bstack1l1llll1l_opy_, \
    bstack1lll11ll1_opy_, bstack1ll1llllll_opy_
from bstack_utils.proxy import bstack1lll1l1lll_opy_, bstack11l1lll11l_opy_
from bstack_utils.bstack1ll1111111_opy_ import bstack1lll11l1l11_opy_, bstack1lll111lll1_opy_, bstack1lll111ll11_opy_, bstack1lll111ll1l_opy_, \
    bstack1lll111llll_opy_, bstack1lll111l1l1_opy_, bstack1lll11l1ll1_opy_, bstack1lll1ll1l1_opy_, bstack1lll11l11ll_opy_
from bstack_utils.bstack1ll11ll1l_opy_ import bstack1l11l11ll1_opy_
from bstack_utils.bstack1l1111lll1_opy_ import bstack11l1llll11_opy_, bstack1lll1l1l1l_opy_, bstack1l1lll1l1_opy_, \
    bstack1ll1lll111_opy_, bstack1llllll11l_opy_
from bstack_utils.bstack1ll11l1l_opy_ import bstack1l1lll1l_opy_
from bstack_utils.bstack1ll1l1ll_opy_ import bstack1lll11ll_opy_
import bstack_utils.bstack11l11111_opy_ as bstack111lll1l_opy_
from bstack_utils.bstack1l1l111l_opy_ import bstack1l1llll1_opy_
from bstack_utils.bstack11ll1ll1l_opy_ import bstack11ll1ll1l_opy_
bstack11llllllll_opy_ = None
bstack11111111l_opy_ = None
bstack1111l1l1l_opy_ = None
bstack11ll11llll_opy_ = None
bstack1ll11lll1l_opy_ = None
bstack1ll1l11l1l_opy_ = None
bstack111ll11l1_opy_ = None
bstack11l1llll1l_opy_ = None
bstack1l1llllll1_opy_ = None
bstack1lll1l1111_opy_ = None
bstack1ll1llll1l_opy_ = None
bstack111l1111l_opy_ = None
bstack1ll111llll_opy_ = None
bstack11l11l11l_opy_ = bstack11ll1l_opy_ (u"ࠨࠩរ")
CONFIG = {}
bstack1llll1l1ll_opy_ = False
bstack1l1ll1l1ll_opy_ = bstack11ll1l_opy_ (u"ࠩࠪល")
bstack1ll1llll11_opy_ = bstack11ll1l_opy_ (u"ࠪࠫវ")
bstack1l1l1l1l1l_opy_ = False
bstack11l1l1l1l1_opy_ = []
bstack1lll11l1l1_opy_ = bstack11l1l11l1l_opy_
bstack1ll11l1l1ll_opy_ = bstack11ll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫឝ")
bstack1ll111l1ll1_opy_ = False
bstack1l1111ll11_opy_ = {}
bstack11ll111lll_opy_ = False
logger = bstack1l1ll1ll11_opy_.get_logger(__name__, bstack1lll11l1l1_opy_)
store = {
    bstack11ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩឞ"): []
}
bstack1ll111ll1l1_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1lll111l_opy_ = {}
current_test_uuid = None
def bstack1ll1l1ll11_opy_(page, bstack1ll11l111_opy_):
    try:
        page.evaluate(bstack11ll1l_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢស"),
                      bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫហ") + json.dumps(
                          bstack1ll11l111_opy_) + bstack11ll1l_opy_ (u"ࠣࡿࢀࠦឡ"))
    except Exception as e:
        print(bstack11ll1l_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢអ"), e)
def bstack11ll1111l_opy_(page, message, level):
    try:
        page.evaluate(bstack11ll1l_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦឣ"), bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩឤ") + json.dumps(
            message) + bstack11ll1l_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨឥ") + json.dumps(level) + bstack11ll1l_opy_ (u"࠭ࡽࡾࠩឦ"))
    except Exception as e:
        print(bstack11ll1l_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥឧ"), e)
def pytest_configure(config):
    bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
    config.args = bstack1lll11ll_opy_.bstack1ll11ll1ll1_opy_(config.args)
    bstack11l111ll_opy_.bstack111l11lll_opy_(bstack1l11lll111_opy_(config.getoption(bstack11ll1l_opy_ (u"ࠨࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬឨ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1ll11ll11l1_opy_ = item.config.getoption(bstack11ll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫឩ"))
    plugins = item.config.getoption(bstack11ll1l_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰࡶࠦឪ"))
    report = outcome.get_result()
    bstack1ll111lll11_opy_(item, call, report)
    if bstack11ll1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷࡣࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡳࡰࡺ࡭ࡩ࡯ࠤឫ") not in plugins or bstack1ll11l11ll_opy_():
        return
    summary = []
    driver = getattr(item, bstack11ll1l_opy_ (u"ࠧࡥࡤࡳ࡫ࡹࡩࡷࠨឬ"), None)
    page = getattr(item, bstack11ll1l_opy_ (u"ࠨ࡟ࡱࡣࡪࡩࠧឭ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1ll11l1l11l_opy_(item, report, summary, bstack1ll11ll11l1_opy_)
    if (page is not None):
        bstack1ll11l11lll_opy_(item, report, summary, bstack1ll11ll11l1_opy_)
def bstack1ll11l1l11l_opy_(item, report, summary, bstack1ll11ll11l1_opy_):
    if report.when == bstack11ll1l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭ឮ") and report.skipped:
        bstack1lll11l11ll_opy_(report)
    if report.when in [bstack11ll1l_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢឯ"), bstack11ll1l_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦឰ")]:
        return
    if not bstack11111l1l1l_opy_():
        return
    try:
        if (str(bstack1ll11ll11l1_opy_).lower() != bstack11ll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨឱ")):
            item._driver.execute_script(
                bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠡࠩឲ") + json.dumps(
                    report.nodeid) + bstack11ll1l_opy_ (u"ࠬࢃࡽࠨឳ"))
        os.environ[bstack11ll1l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙ࡥࡔࡆࡕࡗࡣࡓࡇࡍࡆࠩ឴")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11ll1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡳࡡࡳ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦ࠼ࠣࡿ࠵ࢃࠢ឵").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll1l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥា")))
    bstack11lllll111_opy_ = bstack11ll1l_opy_ (u"ࠤࠥិ")
    bstack1lll11l11ll_opy_(report)
    if not passed:
        try:
            bstack11lllll111_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11ll1l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥី").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack11lllll111_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11ll1l_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨឹ")))
        bstack11lllll111_opy_ = bstack11ll1l_opy_ (u"ࠧࠨឺ")
        if not passed:
            try:
                bstack11lllll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll1l_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨុ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack11lllll111_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡤࡲࡳࡵࡴࡢࡶࡨࠦ࠱ࠦ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠢࠥ࡭ࡳ࡬࡯ࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡨࡦࡺࡡࠣ࠼ࠣࠫូ")
                    + json.dumps(bstack11ll1l_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠢࠤួ"))
                    + bstack11ll1l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧើ")
                )
            else:
                item._driver.execute_script(
                    bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡥࡳࡴࡲࡶࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡥࡣࡷࡥࠧࡀࠠࠨឿ")
                    + json.dumps(str(bstack11lllll111_opy_))
                    + bstack11ll1l_opy_ (u"ࠦࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࠢៀ")
                )
        except Exception as e:
            summary.append(bstack11ll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡥࡳࡴ࡯ࡵࡣࡷࡩ࠿ࠦࡻ࠱ࡿࠥេ").format(e))
def bstack1ll111llll1_opy_(test_name, error_message):
    try:
        bstack1ll11ll111l_opy_ = []
        bstack111llll1l_opy_ = os.environ.get(bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ែ"), bstack11ll1l_opy_ (u"ࠧ࠱ࠩៃ"))
        bstack1l1lllllll_opy_ = {bstack11ll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ោ"): test_name, bstack11ll1l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨៅ"): error_message, bstack11ll1l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩំ"): bstack111llll1l_opy_}
        bstack1ll111ll11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11ll1l_opy_ (u"ࠫࡵࡽ࡟ࡱࡻࡷࡩࡸࡺ࡟ࡦࡴࡵࡳࡷࡥ࡬ࡪࡵࡷ࠲࡯ࡹ࡯࡯ࠩះ"))
        if os.path.exists(bstack1ll111ll11l_opy_):
            with open(bstack1ll111ll11l_opy_) as f:
                bstack1ll11ll111l_opy_ = json.load(f)
        bstack1ll11ll111l_opy_.append(bstack1l1lllllll_opy_)
        with open(bstack1ll111ll11l_opy_, bstack11ll1l_opy_ (u"ࠬࡽࠧៈ")) as f:
            json.dump(bstack1ll11ll111l_opy_, f)
    except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡲࡨࡶࡸ࡯ࡳࡵ࡫ࡱ࡫ࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡳࡽࡹ࡫ࡳࡵࠢࡨࡶࡷࡵࡲࡴ࠼ࠣࠫ៉") + str(e))
def bstack1ll11l11lll_opy_(item, report, summary, bstack1ll11ll11l1_opy_):
    if report.when in [bstack11ll1l_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨ៊"), bstack11ll1l_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࠥ់")]:
        return
    if (str(bstack1ll11ll11l1_opy_).lower() != bstack11ll1l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ៌")):
        bstack1ll1l1ll11_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11ll1l_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧ៍")))
    bstack11lllll111_opy_ = bstack11ll1l_opy_ (u"ࠦࠧ៎")
    bstack1lll11l11ll_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack11lllll111_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11ll1l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡦࡢ࡫࡯ࡹࡷ࡫ࠠࡳࡧࡤࡷࡴࡴ࠺ࠡࡽ࠳ࢁࠧ៏").format(e)
                )
        try:
            if passed:
                bstack1llllll11l_opy_(getattr(item, bstack11ll1l_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬ័"), None), bstack11ll1l_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢ៑"))
            else:
                error_message = bstack11ll1l_opy_ (u"ࠨ្ࠩ")
                if bstack11lllll111_opy_:
                    bstack11ll1111l_opy_(item._page, str(bstack11lllll111_opy_), bstack11ll1l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠣ៓"))
                    bstack1llllll11l_opy_(getattr(item, bstack11ll1l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩ។"), None), bstack11ll1l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ៕"), str(bstack11lllll111_opy_))
                    error_message = str(bstack11lllll111_opy_)
                else:
                    bstack1llllll11l_opy_(getattr(item, bstack11ll1l_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫ៖"), None), bstack11ll1l_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨៗ"))
                bstack1ll111llll1_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11ll1l_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡻࡰࡥࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࡀࠠࡼ࠲ࢀࠦ៘").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack11ll1l_opy_ (u"ࠣ࠯࠰ࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ៙"), default=bstack11ll1l_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣ៚"), help=bstack11ll1l_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡨࠦࡳࡦࡶࠣࡷࡪࡹࡳࡪࡱࡱࠤࡳࡧ࡭ࡦࠤ៛"))
    parser.addoption(bstack11ll1l_opy_ (u"ࠦ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥៜ"), default=bstack11ll1l_opy_ (u"ࠧࡌࡡ࡭ࡵࡨࠦ៝"), help=bstack11ll1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡤࠢࡶࡩࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠧ៞"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11ll1l_opy_ (u"ࠢ࠮࠯ࡧࡶ࡮ࡼࡥࡳࠤ៟"), action=bstack11ll1l_opy_ (u"ࠣࡵࡷࡳࡷ࡫ࠢ០"), default=bstack11ll1l_opy_ (u"ࠤࡦ࡬ࡷࡵ࡭ࡦࠤ១"),
                         help=bstack11ll1l_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡸࡴࠦࡲࡶࡰࠣࡸࡪࡹࡴࡴࠤ២"))
def bstack11lll111_opy_(log):
    if not (log[bstack11ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ៣")] and log[bstack11ll1l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭៤")].strip()):
        return
    active = bstack1ll111l1_opy_()
    log = {
        bstack11ll1l_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ៥"): log[bstack11ll1l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭៦")],
        bstack11ll1l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ៧"): bstack11llll1l_opy_().isoformat() + bstack11ll1l_opy_ (u"ࠩ࡝ࠫ៨"),
        bstack11ll1l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ៩"): log[bstack11ll1l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ៪")],
    }
    if active:
        if active[bstack11ll1l_opy_ (u"ࠬࡺࡹࡱࡧࠪ៫")] == bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ៬"):
            log[bstack11ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ៭")] = active[bstack11ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ៮")]
        elif active[bstack11ll1l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ៯")] == bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࠨ៰"):
            log[bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ៱")] = active[bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ៲")]
    bstack1l1llll1_opy_.bstack1ll11l11_opy_([log])
def bstack1ll111l1_opy_():
    if len(store[bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪ៳")]) > 0 and store[bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫ៴")][-1]:
        return {
            bstack11ll1l_opy_ (u"ࠨࡶࡼࡴࡪ࠭៵"): bstack11ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ៶"),
            bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ៷"): store[bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ៸")][-1]
        }
    if store.get(bstack11ll1l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩ៹"), None):
        return {
            bstack11ll1l_opy_ (u"࠭ࡴࡺࡲࡨࠫ៺"): bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࠬ៻"),
            bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ៼"): store[bstack11ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭៽")]
        }
    return None
bstack1lll1ll1_opy_ = bstack1l1l1111_opy_(bstack11lll111_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1ll111l1ll1_opy_
        item._1ll111lllll_opy_ = True
        bstack1ll11lllll_opy_ = bstack111lll1l_opy_.bstack1ll1l1l1l_opy_(bstack1111111lll_opy_(item.own_markers))
        item._a11y_test_case = bstack1ll11lllll_opy_
        if bstack1ll111l1ll1_opy_:
            driver = getattr(item, bstack11ll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫ៾"), None)
            item._a11y_started = bstack111lll1l_opy_.bstack1l11111lll_opy_(driver, bstack1ll11lllll_opy_)
        if not bstack1l1llll1_opy_.on() or bstack1ll11l1l1ll_opy_ != bstack11ll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ៿"):
            return
        global current_test_uuid, bstack1lll1ll1_opy_
        bstack1lll1ll1_opy_.start()
        bstack1ll1l111_opy_ = {
            bstack11ll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ᠀"): uuid4().__str__(),
            bstack11ll1l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ᠁"): bstack11llll1l_opy_().isoformat() + bstack11ll1l_opy_ (u"࡛ࠧࠩ᠂")
        }
        current_test_uuid = bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᠃")]
        store[bstack11ll1l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭᠄")] = bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᠅")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1lll111l_opy_[item.nodeid] = {**_1lll111l_opy_[item.nodeid], **bstack1ll1l111_opy_}
        bstack1ll11l11111_opy_(item, _1lll111l_opy_[item.nodeid], bstack11ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ᠆"))
    except Exception as err:
        print(bstack11ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡩࡡ࡭࡮࠽ࠤࢀࢃࠧ᠇"), str(err))
def pytest_runtest_setup(item):
    global bstack1ll111ll1l1_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack1111111111_opy_():
        atexit.register(bstack1l11l1l11l_opy_)
        if not bstack1ll111ll1l1_opy_:
            try:
                bstack1ll11l11l1l_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack1111ll111l_opy_():
                    bstack1ll11l11l1l_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack1ll11l11l1l_opy_:
                    signal.signal(s, bstack1ll11l1ll11_opy_)
                bstack1ll111ll1l1_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11ll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡴࡨ࡫࡮ࡹࡴࡦࡴࠣࡷ࡮࡭࡮ࡢ࡮ࠣ࡬ࡦࡴࡤ࡭ࡧࡵࡷ࠿ࠦࠢ᠈") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1lll11l1l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11ll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᠉")
    try:
        if not bstack1l1llll1_opy_.on():
            return
        bstack1lll1ll1_opy_.start()
        uuid = uuid4().__str__()
        bstack1ll1l111_opy_ = {
            bstack11ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᠊"): uuid,
            bstack11ll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭᠋"): bstack11llll1l_opy_().isoformat() + bstack11ll1l_opy_ (u"ࠪ࡞ࠬ᠌"),
            bstack11ll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩ᠍"): bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪ᠎"),
            bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩ᠏"): bstack11ll1l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬ᠐"),
            bstack11ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫ᠑"): bstack11ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ᠒")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧ᠓")] = item
        store[bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨ᠔")] = [uuid]
        if not _1lll111l_opy_.get(item.nodeid, None):
            _1lll111l_opy_[item.nodeid] = {bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ᠕"): [], bstack11ll1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨ᠖"): []}
        _1lll111l_opy_[item.nodeid][bstack11ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭᠗")].append(bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭᠘")])
        _1lll111l_opy_[item.nodeid + bstack11ll1l_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩ᠙")] = bstack1ll1l111_opy_
        bstack1ll11l1l1l1_opy_(item, bstack1ll1l111_opy_, bstack11ll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ᠚"))
    except Exception as err:
        print(bstack11ll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧ᠛"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1111ll11_opy_
        bstack111llll1l_opy_ = 0
        if bstack1l1l1l1l1l_opy_ is True:
            bstack111llll1l_opy_ = int(os.environ.get(bstack11ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ᠜")))
        if bstack1l1111l11l_opy_.bstack1l111ll11_opy_() == bstack11ll1l_opy_ (u"ࠨࡴࡳࡷࡨࠦ᠝"):
            if bstack1l1111l11l_opy_.bstack11ll1lllll_opy_() == bstack11ll1l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᠞"):
                bstack1ll11l111l1_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᠟"), None)
                bstack1l11l1ll1_opy_ = bstack1ll11l111l1_opy_ + bstack11ll1l_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᠠ")
                driver = getattr(item, bstack11ll1l_opy_ (u"ࠪࡣࡩࡸࡩࡷࡧࡵࠫᠡ"), None)
                bstack1l1l1l1l1_opy_ = getattr(item, bstack11ll1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᠢ"), None)
                bstack1111l111l_opy_ = getattr(item, bstack11ll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᠣ"), None)
                PercySDK.screenshot(driver, bstack1l11l1ll1_opy_, bstack1l1l1l1l1_opy_=bstack1l1l1l1l1_opy_, bstack1111l111l_opy_=bstack1111l111l_opy_, bstack111111l11_opy_=bstack111llll1l_opy_)
        if getattr(item, bstack11ll1l_opy_ (u"࠭࡟ࡢ࠳࠴ࡽࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᠤ"), False):
            bstack11l1l111_opy_.bstack111l11l1_opy_(getattr(item, bstack11ll1l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᠥ"), None), bstack1l1111ll11_opy_, logger, item)
        if not bstack1l1llll1_opy_.on():
            return
        bstack1ll1l111_opy_ = {
            bstack11ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᠦ"): uuid4().__str__(),
            bstack11ll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᠧ"): bstack11llll1l_opy_().isoformat() + bstack11ll1l_opy_ (u"ࠪ࡞ࠬᠨ"),
            bstack11ll1l_opy_ (u"ࠫࡹࡿࡰࡦࠩᠩ"): bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᠪ"),
            bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᠫ"): bstack11ll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᠬ"),
            bstack11ll1l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᠭ"): bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᠮ")
        }
        _1lll111l_opy_[item.nodeid + bstack11ll1l_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᠯ")] = bstack1ll1l111_opy_
        bstack1ll11l1l1l1_opy_(item, bstack1ll1l111_opy_, bstack11ll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᠰ"))
    except Exception as err:
        print(bstack11ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫᠱ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1l1llll1_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1lll111ll1l_opy_(fixturedef.argname):
        store[bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᠲ")] = request.node
    elif bstack1lll111llll_opy_(fixturedef.argname):
        store[bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᠳ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack11ll1l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᠴ"): fixturedef.argname,
            bstack11ll1l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᠵ"): bstack1111lll11l_opy_(outcome),
            bstack11ll1l_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᠶ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᠷ")]
        if not _1lll111l_opy_.get(current_test_item.nodeid, None):
            _1lll111l_opy_[current_test_item.nodeid] = {bstack11ll1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᠸ"): []}
        _1lll111l_opy_[current_test_item.nodeid][bstack11ll1l_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᠹ")].append(fixture)
    except Exception as err:
        logger.debug(bstack11ll1l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᠺ"), str(err))
if bstack1ll11l11ll_opy_() and bstack1l1llll1_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1lll111l_opy_[request.node.nodeid][bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᠻ")].bstack1llll1lll_opy_(id(step))
        except Exception as err:
            print(bstack11ll1l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧᠼ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1lll111l_opy_[request.node.nodeid][bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᠽ")].bstack1l11l1ll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11ll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᠾ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1ll11l1l_opy_: bstack1l1lll1l_opy_ = _1lll111l_opy_[request.node.nodeid][bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᠿ")]
            bstack1ll11l1l_opy_.bstack1l11l1ll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11ll1l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᡀ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1ll11l1l1ll_opy_
        try:
            if not bstack1l1llll1_opy_.on() or bstack1ll11l1l1ll_opy_ != bstack11ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᡁ"):
                return
            global bstack1lll1ll1_opy_
            bstack1lll1ll1_opy_.start()
            driver = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧᡂ"), None)
            if not _1lll111l_opy_.get(request.node.nodeid, None):
                _1lll111l_opy_[request.node.nodeid] = {}
            bstack1ll11l1l_opy_ = bstack1l1lll1l_opy_.bstack1ll1ll11l11_opy_(
                scenario, feature, request.node,
                name=bstack1lll111l1l1_opy_(request.node, scenario),
                bstack1l111111_opy_=bstack1lll11l1_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11ll1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵ࠯ࡦࡹࡨࡻ࡭ࡣࡧࡵࠫᡃ"),
                tags=bstack1lll11l1ll1_opy_(feature, scenario),
                bstack1l1lllll_opy_=bstack1l1llll1_opy_.bstack11llllll_opy_(driver) if driver and driver.session_id else {}
            )
            _1lll111l_opy_[request.node.nodeid][bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᡄ")] = bstack1ll11l1l_opy_
            bstack1ll11l11l11_opy_(bstack1ll11l1l_opy_.uuid)
            bstack1l1llll1_opy_.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᡅ"), bstack1ll11l1l_opy_)
        except Exception as err:
            print(bstack11ll1l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡧࡪࡤࡠࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱ࠽ࠤࢀࢃࠧᡆ"), str(err))
def bstack1ll11l111ll_opy_(bstack11l11ll1ll_opy_):
    if bstack11l11ll1ll_opy_ in store[bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᡇ")]:
        store[bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᡈ")].remove(bstack11l11ll1ll_opy_)
def bstack1ll11l11l11_opy_(bstack11l1l1111l_opy_):
    store[bstack11ll1l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬᡉ")] = bstack11l1l1111l_opy_
    threading.current_thread().current_test_uuid = bstack11l1l1111l_opy_
@bstack1l1llll1_opy_.bstack1ll1l1111ll_opy_
def bstack1ll111lll11_opy_(item, call, report):
    global bstack1ll11l1l1ll_opy_
    bstack1lll1l11l1_opy_ = bstack1lll11l1_opy_()
    if hasattr(report, bstack11ll1l_opy_ (u"ࠩࡶࡸࡴࡶࠧᡊ")):
        bstack1lll1l11l1_opy_ = bstack111l1l111l_opy_(report.stop)
    elif hasattr(report, bstack11ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࠩᡋ")):
        bstack1lll1l11l1_opy_ = bstack111l1l111l_opy_(report.start)
    try:
        if getattr(report, bstack11ll1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᡌ"), bstack11ll1l_opy_ (u"ࠬ࠭ᡍ")) == bstack11ll1l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᡎ"):
            bstack1lll1ll1_opy_.reset()
        if getattr(report, bstack11ll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬᡏ"), bstack11ll1l_opy_ (u"ࠨࠩᡐ")) == bstack11ll1l_opy_ (u"ࠩࡦࡥࡱࡲࠧᡑ"):
            if bstack1ll11l1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᡒ"):
                _1lll111l_opy_[item.nodeid][bstack11ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᡓ")] = bstack1lll1l11l1_opy_
                bstack1ll11l11111_opy_(item, _1lll111l_opy_[item.nodeid], bstack11ll1l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᡔ"), report, call)
                store[bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᡕ")] = None
            elif bstack1ll11l1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᡖ"):
                bstack1ll11l1l_opy_ = _1lll111l_opy_[item.nodeid][bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᡗ")]
                bstack1ll11l1l_opy_.set(hooks=_1lll111l_opy_[item.nodeid].get(bstack11ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᡘ"), []))
                exception, bstack1ll1llll_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1ll1llll_opy_ = [call.excinfo.exconly(), getattr(report, bstack11ll1l_opy_ (u"ࠪࡰࡴࡴࡧࡳࡧࡳࡶࡹ࡫ࡸࡵࠩᡙ"), bstack11ll1l_opy_ (u"ࠫࠬᡚ"))]
                bstack1ll11l1l_opy_.stop(time=bstack1lll1l11l1_opy_, result=Result(result=getattr(report, bstack11ll1l_opy_ (u"ࠬࡵࡵࡵࡥࡲࡱࡪ࠭ᡛ"), bstack11ll1l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᡜ")), exception=exception, bstack1ll1llll_opy_=bstack1ll1llll_opy_))
                bstack1l1llll1_opy_.bstack1l1111l1_opy_(bstack11ll1l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᡝ"), _1lll111l_opy_[item.nodeid][bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᡞ")])
        elif getattr(report, bstack11ll1l_opy_ (u"ࠩࡺ࡬ࡪࡴࠧᡟ"), bstack11ll1l_opy_ (u"ࠪࠫᡠ")) in [bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᡡ"), bstack11ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᡢ")]:
            bstack1l111l11_opy_ = item.nodeid + bstack11ll1l_opy_ (u"࠭࠭ࠨᡣ") + getattr(report, bstack11ll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬᡤ"), bstack11ll1l_opy_ (u"ࠨࠩᡥ"))
            if getattr(report, bstack11ll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᡦ"), False):
                hook_type = bstack11ll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨᡧ") if getattr(report, bstack11ll1l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩᡨ"), bstack11ll1l_opy_ (u"ࠬ࠭ᡩ")) == bstack11ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬᡪ") else bstack11ll1l_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᡫ")
                _1lll111l_opy_[bstack1l111l11_opy_] = {
                    bstack11ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᡬ"): uuid4().__str__(),
                    bstack11ll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᡭ"): bstack1lll1l11l1_opy_,
                    bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᡮ"): hook_type
                }
            _1lll111l_opy_[bstack1l111l11_opy_][bstack11ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᡯ")] = bstack1lll1l11l1_opy_
            bstack1ll11l111ll_opy_(_1lll111l_opy_[bstack1l111l11_opy_][bstack11ll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪᡰ")])
            bstack1ll11l1l1l1_opy_(item, _1lll111l_opy_[bstack1l111l11_opy_], bstack11ll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨᡱ"), report, call)
            if getattr(report, bstack11ll1l_opy_ (u"ࠧࡸࡪࡨࡲࠬᡲ"), bstack11ll1l_opy_ (u"ࠨࠩᡳ")) == bstack11ll1l_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᡴ"):
                if getattr(report, bstack11ll1l_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨࠫᡵ"), bstack11ll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᡶ")) == bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᡷ"):
                    bstack1ll1l111_opy_ = {
                        bstack11ll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᡸ"): uuid4().__str__(),
                        bstack11ll1l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ᡹"): bstack1lll11l1_opy_(),
                        bstack11ll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᡺"): bstack1lll11l1_opy_()
                    }
                    _1lll111l_opy_[item.nodeid] = {**_1lll111l_opy_[item.nodeid], **bstack1ll1l111_opy_}
                    bstack1ll11l11111_opy_(item, _1lll111l_opy_[item.nodeid], bstack11ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ᡻"))
                    bstack1ll11l11111_opy_(item, _1lll111l_opy_[item.nodeid], bstack11ll1l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ᡼"), report, call)
    except Exception as err:
        print(bstack11ll1l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡻࡾࠩ᡽"), str(err))
def bstack1ll11l11ll1_opy_(test, bstack1ll1l111_opy_, result=None, call=None, bstack1l1ll1lll_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1ll11l1l_opy_ = {
        bstack11ll1l_opy_ (u"ࠬࡻࡵࡪࡦࠪ᡾"): bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᡿")],
        bstack11ll1l_opy_ (u"ࠧࡵࡻࡳࡩࠬᢀ"): bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᢁ"),
        bstack11ll1l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᢂ"): test.name,
        bstack11ll1l_opy_ (u"ࠪࡦࡴࡪࡹࠨᢃ"): {
            bstack11ll1l_opy_ (u"ࠫࡱࡧ࡮ࡨࠩᢄ"): bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᢅ"),
            bstack11ll1l_opy_ (u"࠭ࡣࡰࡦࡨࠫᢆ"): inspect.getsource(test.obj)
        },
        bstack11ll1l_opy_ (u"ࠧࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᢇ"): test.name,
        bstack11ll1l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࠧᢈ"): test.name,
        bstack11ll1l_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᢉ"): bstack1lll11ll_opy_.bstack11ll1ll1_opy_(test),
        bstack11ll1l_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᢊ"): file_path,
        bstack11ll1l_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᢋ"): file_path,
        bstack11ll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᢌ"): bstack11ll1l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧᢍ"),
        bstack11ll1l_opy_ (u"ࠧࡷࡥࡢࡪ࡮ࡲࡥࡱࡣࡷ࡬ࠬᢎ"): file_path,
        bstack11ll1l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᢏ"): bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᢐ")],
        bstack11ll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᢑ"): bstack11ll1l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫᢒ"),
        bstack11ll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᢓ"): {
            bstack11ll1l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᢔ"): test.nodeid
        },
        bstack11ll1l_opy_ (u"ࠧࡵࡣࡪࡷࠬᢕ"): bstack1111111lll_opy_(test.own_markers)
    }
    if bstack1l1ll1lll_opy_ in [bstack11ll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᢖ"), bstack11ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᢗ")]:
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠪࡱࡪࡺࡡࠨᢘ")] = {
            bstack11ll1l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭ᢙ"): bstack1ll1l111_opy_.get(bstack11ll1l_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᢚ"), [])
        }
    if bstack1l1ll1lll_opy_ == bstack11ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓ࡬࡫ࡳࡴࡪࡪࠧᢛ"):
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᢜ")] = bstack11ll1l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᢝ")
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᢞ")] = bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᢟ")]
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᢠ")] = bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᢡ")]
    if result:
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᢢ")] = result.outcome
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᢣ")] = result.duration * 1000
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᢤ")] = bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᢥ")]
        if result.failed:
            bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᢦ")] = bstack1l1llll1_opy_.bstack1111lll1_opy_(call.excinfo.typename)
            bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᢧ")] = bstack1l1llll1_opy_.bstack1ll1l11l111_opy_(call.excinfo, result)
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᢨ")] = bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷᢩࠬ")]
    if outcome:
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᢪ")] = bstack1111lll11l_opy_(outcome)
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ᢫")] = 0
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧ᢬")] = bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ᢭")]
        if bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᢮")] == bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᢯"):
            bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬᢰ")] = bstack11ll1l_opy_ (u"ࠧࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠨᢱ")  # bstack1ll11l1111l_opy_
            bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᢲ")] = [{bstack11ll1l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᢳ"): [bstack11ll1l_opy_ (u"ࠪࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠧᢴ")]}]
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᢵ")] = bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᢶ")]
    return bstack1ll11l1l_opy_
def bstack1ll11l1ll1l_opy_(test, bstack1l1lll11_opy_, bstack1l1ll1lll_opy_, result, call, outcome, bstack1ll111l1l1l_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᢷ")]
    hook_name = bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡴࡡ࡮ࡧࠪᢸ")]
    hook_data = {
        bstack11ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᢹ"): bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᢺ")],
        bstack11ll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᢻ"): bstack11ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᢼ"),
        bstack11ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᢽ"): bstack11ll1l_opy_ (u"࠭ࡻࡾࠩᢾ").format(bstack1lll111lll1_opy_(hook_name)),
        bstack11ll1l_opy_ (u"ࠧࡣࡱࡧࡽࠬᢿ"): {
            bstack11ll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬࠭ᣀ"): bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᣁ"),
            bstack11ll1l_opy_ (u"ࠪࡧࡴࡪࡥࠨᣂ"): None
        },
        bstack11ll1l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࠪᣃ"): test.name,
        bstack11ll1l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᣄ"): bstack1lll11ll_opy_.bstack11ll1ll1_opy_(test, hook_name),
        bstack11ll1l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩᣅ"): file_path,
        bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࠩᣆ"): file_path,
        bstack11ll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣇ"): bstack11ll1l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪᣈ"),
        bstack11ll1l_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᣉ"): file_path,
        bstack11ll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᣊ"): bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᣋ")],
        bstack11ll1l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᣌ"): bstack11ll1l_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩᣍ") if bstack1ll11l1l1ll_opy_ == bstack11ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᣎ") else bstack11ll1l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᣏ"),
        bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᣐ"): hook_type
    }
    bstack1ll1lll11ll_opy_ = bstack1l1l1ll1_opy_(_1lll111l_opy_.get(test.nodeid, None))
    if bstack1ll1lll11ll_opy_:
        hook_data[bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡩࡥࠩᣑ")] = bstack1ll1lll11ll_opy_
    if result:
        hook_data[bstack11ll1l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᣒ")] = result.outcome
        hook_data[bstack11ll1l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᣓ")] = result.duration * 1000
        hook_data[bstack11ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᣔ")] = bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᣕ")]
        if result.failed:
            hook_data[bstack11ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᣖ")] = bstack1l1llll1_opy_.bstack1111lll1_opy_(call.excinfo.typename)
            hook_data[bstack11ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᣗ")] = bstack1l1llll1_opy_.bstack1ll1l11l111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11ll1l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᣘ")] = bstack1111lll11l_opy_(outcome)
        hook_data[bstack11ll1l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭ᣙ")] = 100
        hook_data[bstack11ll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᣚ")] = bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᣛ")]
        if hook_data[bstack11ll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣜ")] == bstack11ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᣝ"):
            hook_data[bstack11ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᣞ")] = bstack11ll1l_opy_ (u"࡚ࠫࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠬᣟ")  # bstack1ll11l1111l_opy_
            hook_data[bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᣠ")] = [{bstack11ll1l_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᣡ"): [bstack11ll1l_opy_ (u"ࠧࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠫᣢ")]}]
    if bstack1ll111l1l1l_opy_:
        hook_data[bstack11ll1l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᣣ")] = bstack1ll111l1l1l_opy_.result
        hook_data[bstack11ll1l_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᣤ")] = bstack1111111ll1_opy_(bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᣥ")], bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᣦ")])
        hook_data[bstack11ll1l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᣧ")] = bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᣨ")]
        if hook_data[bstack11ll1l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᣩ")] == bstack11ll1l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᣪ"):
            hook_data[bstack11ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᣫ")] = bstack1l1llll1_opy_.bstack1111lll1_opy_(bstack1ll111l1l1l_opy_.exception_type)
            hook_data[bstack11ll1l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᣬ")] = [{bstack11ll1l_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᣭ"): bstack11111lllll_opy_(bstack1ll111l1l1l_opy_.exception)}]
    return hook_data
def bstack1ll11l11111_opy_(test, bstack1ll1l111_opy_, bstack1l1ll1lll_opy_, result=None, call=None, outcome=None):
    bstack1ll11l1l_opy_ = bstack1ll11l11ll1_opy_(test, bstack1ll1l111_opy_, result, call, bstack1l1ll1lll_opy_, outcome)
    driver = getattr(test, bstack11ll1l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ᣮ"), None)
    if bstack1l1ll1lll_opy_ == bstack11ll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᣯ") and driver:
        bstack1ll11l1l_opy_[bstack11ll1l_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᣰ")] = bstack1l1llll1_opy_.bstack11llllll_opy_(driver)
    if bstack1l1ll1lll_opy_ == bstack11ll1l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩᣱ"):
        bstack1l1ll1lll_opy_ = bstack11ll1l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᣲ")
    bstack11lll1l1_opy_ = {
        bstack11ll1l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᣳ"): bstack1l1ll1lll_opy_,
        bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭ᣴ"): bstack1ll11l1l_opy_
    }
    bstack1l1llll1_opy_.bstack1l1l1lll_opy_(bstack11lll1l1_opy_)
def bstack1ll11l1l1l1_opy_(test, bstack1ll1l111_opy_, bstack1l1ll1lll_opy_, result=None, call=None, outcome=None, bstack1ll111l1l1l_opy_=None):
    hook_data = bstack1ll11l1ll1l_opy_(test, bstack1ll1l111_opy_, bstack1l1ll1lll_opy_, result, call, outcome, bstack1ll111l1l1l_opy_)
    bstack11lll1l1_opy_ = {
        bstack11ll1l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩᣵ"): bstack1l1ll1lll_opy_,
        bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࠨ᣶"): hook_data
    }
    bstack1l1llll1_opy_.bstack1l1l1lll_opy_(bstack11lll1l1_opy_)
def bstack1l1l1ll1_opy_(bstack1ll1l111_opy_):
    if not bstack1ll1l111_opy_:
        return None
    if bstack1ll1l111_opy_.get(bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ᣷"), None):
        return getattr(bstack1ll1l111_opy_[bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ᣸")], bstack11ll1l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᣹"), None)
    return bstack1ll1l111_opy_.get(bstack11ll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᣺"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1l1llll1_opy_.on():
            return
        places = [bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪ᣻"), bstack11ll1l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ᣼"), bstack11ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ᣽")]
        bstack1llll11l_opy_ = []
        for bstack1ll111l1lll_opy_ in places:
            records = caplog.get_records(bstack1ll111l1lll_opy_)
            bstack1ll111ll1ll_opy_ = bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ᣾") if bstack1ll111l1lll_opy_ == bstack11ll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭᣿") else bstack11ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᤀ")
            bstack1ll111l11ll_opy_ = request.node.nodeid + (bstack11ll1l_opy_ (u"ࠪࠫᤁ") if bstack1ll111l1lll_opy_ == bstack11ll1l_opy_ (u"ࠫࡨࡧ࡬࡭ࠩᤂ") else bstack11ll1l_opy_ (u"ࠬ࠳ࠧᤃ") + bstack1ll111l1lll_opy_)
            bstack11l1l1111l_opy_ = bstack1l1l1ll1_opy_(_1lll111l_opy_.get(bstack1ll111l11ll_opy_, None))
            if not bstack11l1l1111l_opy_:
                continue
            for record in records:
                if bstack1111l111l1_opy_(record.message):
                    continue
                bstack1llll11l_opy_.append({
                    bstack11ll1l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᤄ"): bstack1111111l11_opy_(record.created).isoformat() + bstack11ll1l_opy_ (u"࡛ࠧࠩᤅ"),
                    bstack11ll1l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᤆ"): record.levelname,
                    bstack11ll1l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᤇ"): record.message,
                    bstack1ll111ll1ll_opy_: bstack11l1l1111l_opy_
                })
        if len(bstack1llll11l_opy_) > 0:
            bstack1l1llll1_opy_.bstack1ll11l11_opy_(bstack1llll11l_opy_)
    except Exception as err:
        print(bstack11ll1l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡩࡨࡵ࡮ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧ࠽ࠤࢀࢃࠧᤈ"), str(err))
def bstack1l1llll1l1_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack11ll111lll_opy_
    bstack1lll11ll1l_opy_ = bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᤉ"), None) and bstack1ll11111_opy_(
            threading.current_thread(), bstack11ll1l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᤊ"), None)
    bstack11l11l1l1_opy_ = getattr(driver, bstack11ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ᤋ"), None) != None and getattr(driver, bstack11ll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᤌ"), None) == True
    if sequence == bstack11ll1l_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᤍ") and driver != None:
      if not bstack11ll111lll_opy_ and bstack11111l1l1l_opy_() and bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᤎ") in CONFIG and CONFIG[bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᤏ")] == True and bstack11ll1ll1l_opy_.bstack1l11l1lll1_opy_(driver_command) and (bstack11l11l1l1_opy_ or bstack1lll11ll1l_opy_) and not bstack1ll1ll11ll_opy_(args):
        try:
          bstack11ll111lll_opy_ = True
          logger.debug(bstack11ll1l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡿࢂ࠭ᤐ").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11ll1l_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡲࡨࡶ࡫ࡵࡲ࡮ࠢࡶࡧࡦࡴࠠࡼࡿࠪᤑ").format(str(err)))
        bstack11ll111lll_opy_ = False
    if sequence == bstack11ll1l_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᤒ"):
        if driver_command == bstack11ll1l_opy_ (u"ࠧࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠫᤓ"):
            bstack1l1llll1_opy_.bstack1l11ll11ll_opy_({
                bstack11ll1l_opy_ (u"ࠨ࡫ࡰࡥ࡬࡫ࠧᤔ"): response[bstack11ll1l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨᤕ")],
                bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᤖ"): store[bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨᤗ")]
            })
def bstack1l11l1l11l_opy_():
    global bstack11l1l1l1l1_opy_
    bstack1l1ll1ll11_opy_.bstack11l1ll1l1_opy_()
    logging.shutdown()
    bstack1l1llll1_opy_.bstack11lllll1_opy_()
    for driver in bstack11l1l1l1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll11l1ll11_opy_(*args):
    global bstack11l1l1l1l1_opy_
    bstack1l1llll1_opy_.bstack11lllll1_opy_()
    for driver in bstack11l1l1l1l1_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack111111l1_opy_(self, *args, **kwargs):
    bstack1l1lll11l_opy_ = bstack11llllllll_opy_(self, *args, **kwargs)
    bstack1l1llll1_opy_.bstack1ll1l1l11l_opy_(self)
    return bstack1l1lll11l_opy_
def bstack11lll1l1l1_opy_(framework_name):
    from bstack_utils.config import Config
    bstack11l111ll_opy_ = Config.bstack111l1ll1_opy_()
    if bstack11l111ll_opy_.get_property(bstack11ll1l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡳ࡯ࡥࡡࡦࡥࡱࡲࡥࡥࠩᤘ")):
        return
    bstack11l111ll_opy_.bstack11l11111l_opy_(bstack11ll1l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥ࡭ࡰࡦࡢࡧࡦࡲ࡬ࡦࡦࠪᤙ"), True)
    global bstack11l11l11l_opy_
    global bstack11ll11111l_opy_
    bstack11l11l11l_opy_ = framework_name
    logger.info(bstack1ll1llllll_opy_.format(bstack11l11l11l_opy_.split(bstack11ll1l_opy_ (u"ࠧ࠮ࠩᤚ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11111l1l1l_opy_():
            Service.start = bstack1l111l111l_opy_
            Service.stop = bstack1l1lll111_opy_
            webdriver.Remote.__init__ = bstack1lllllll1l_opy_
            webdriver.Remote.get = bstack1l1l11l111_opy_
            if not isinstance(os.getenv(bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡃࡕࡅࡑࡒࡅࡍࠩᤛ")), str):
                return
            WebDriver.close = bstack11l1lll11_opy_
            WebDriver.quit = bstack1ll1ll1ll_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        if not bstack11111l1l1l_opy_() and bstack1l1llll1_opy_.on():
            webdriver.Remote.__init__ = bstack111111l1_opy_
        bstack11ll11111l_opy_ = True
    except Exception as e:
        pass
    bstack1lllll1lll_opy_()
    if os.environ.get(bstack11ll1l_opy_ (u"ࠩࡖࡉࡑࡋࡎࡊࡗࡐࡣࡔࡘ࡟ࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡎࡔࡓࡕࡃࡏࡐࡊࡊࠧᤜ")):
        bstack11ll11111l_opy_ = eval(os.environ.get(bstack11ll1l_opy_ (u"ࠪࡗࡊࡒࡅࡏࡋࡘࡑࡤࡕࡒࡠࡒࡏࡅ࡞࡝ࡒࡊࡉࡋࡘࡤࡏࡎࡔࡖࡄࡐࡑࡋࡄࠨᤝ")))
    if not bstack11ll11111l_opy_:
        bstack11llllll1_opy_(bstack11ll1l_opy_ (u"ࠦࡕࡧࡣ࡬ࡣࡪࡩࡸࠦ࡮ࡰࡶࠣ࡭ࡳࡹࡴࡢ࡮࡯ࡩࡩࠨᤞ"), bstack1lll11ll1_opy_)
    if bstack11ll1l11l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack11l11ll11_opy_
        except Exception as e:
            logger.error(bstack11lll1l1l_opy_.format(str(e)))
    if bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬ᤟") in str(framework_name).lower():
        if not bstack11111l1l1l_opy_():
            return
        try:
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
def bstack1ll1ll1ll_opy_(self):
    global bstack11l11l11l_opy_
    global bstack1llll1l11l_opy_
    global bstack11111111l_opy_
    try:
        if bstack11ll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᤠ") in bstack11l11l11l_opy_ and self.session_id != None and bstack1ll11111_opy_(threading.current_thread(), bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫᤡ"), bstack11ll1l_opy_ (u"ࠨࠩᤢ")) != bstack11ll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᤣ"):
            bstack1lll1ll11_opy_ = bstack11ll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᤤ") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11ll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᤥ")
            bstack111ll1l1l_opy_(logger, True)
            if self != None:
                bstack1ll1lll111_opy_(self, bstack1lll1ll11_opy_, bstack11ll1l_opy_ (u"ࠬ࠲ࠠࠨᤦ").join(threading.current_thread().bstackTestErrorMessages))
        item = store.get(bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪᤧ"), None)
        if item is not None and bstack1ll111l1ll1_opy_:
            bstack11l1l111_opy_.bstack111l11l1_opy_(self, bstack1l1111ll11_opy_, logger, item)
        threading.current_thread().testStatus = bstack11ll1l_opy_ (u"ࠧࠨᤨ")
    except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࠤᤩ") + str(e))
    bstack11111111l_opy_(self)
    self.session_id = None
def bstack1lllllll1l_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1llll1l11l_opy_
    global bstack1111l1ll1_opy_
    global bstack1l1l1l1l1l_opy_
    global bstack11l11l11l_opy_
    global bstack11llllllll_opy_
    global bstack11l1l1l1l1_opy_
    global bstack1l1ll1l1ll_opy_
    global bstack1ll1llll11_opy_
    global bstack1ll111l1ll1_opy_
    global bstack1l1111ll11_opy_
    CONFIG[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᤪ")] = str(bstack11l11l11l_opy_) + str(__version__)
    command_executor = bstack1llll111l_opy_(bstack1l1ll1l1ll_opy_)
    logger.debug(bstack1l11ll11l1_opy_.format(command_executor))
    proxy = bstack11ll11l1l1_opy_(CONFIG, proxy)
    bstack111llll1l_opy_ = 0
    try:
        if bstack1l1l1l1l1l_opy_ is True:
            bstack111llll1l_opy_ = int(os.environ.get(bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᤫ")))
    except:
        bstack111llll1l_opy_ = 0
    bstack1ll11l1lll_opy_ = bstack11ll11ll1l_opy_(CONFIG, bstack111llll1l_opy_)
    logger.debug(bstack11lll11l1_opy_.format(str(bstack1ll11l1lll_opy_)))
    bstack1l1111ll11_opy_ = CONFIG.get(bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᤬"))[bstack111llll1l_opy_]
    if bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ᤭") in CONFIG and CONFIG[bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ᤮")]:
        bstack1l1lll1l1_opy_(bstack1ll11l1lll_opy_, bstack1ll1llll11_opy_)
    if bstack111lll1l_opy_.bstack1lll1lllll_opy_(CONFIG, bstack111llll1l_opy_) and bstack111lll1l_opy_.bstack1l11ll11l_opy_(bstack1ll11l1lll_opy_, options, desired_capabilities):
        bstack1ll111l1ll1_opy_ = True
        bstack111lll1l_opy_.set_capabilities(bstack1ll11l1lll_opy_, CONFIG)
    if desired_capabilities:
        bstack11l1l1l11_opy_ = bstack11l1l1lll1_opy_(desired_capabilities)
        bstack11l1l1l11_opy_[bstack11ll1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧ᤯")] = bstack1l1111l11_opy_(CONFIG)
        bstack11l1l1l111_opy_ = bstack11ll11ll1l_opy_(bstack11l1l1l11_opy_)
        if bstack11l1l1l111_opy_:
            bstack1ll11l1lll_opy_ = update(bstack11l1l1l111_opy_, bstack1ll11l1lll_opy_)
        desired_capabilities = None
    if options:
        bstack1l111111l1_opy_(options, bstack1ll11l1lll_opy_)
    if not options:
        options = bstack1l111ll111_opy_(bstack1ll11l1lll_opy_)
    if proxy and bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠨ࠶࠱࠵࠵࠴࠰ࠨᤰ")):
        options.proxy(proxy)
    if options and bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨᤱ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack11l111lll_opy_() < version.parse(bstack11ll1l_opy_ (u"ࠪ࠷࠳࠾࠮࠱ࠩᤲ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1ll11l1lll_opy_)
    logger.info(bstack11lll11ll_opy_)
    if bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᤳ")):
        bstack11llllllll_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᤴ")):
        bstack11llllllll_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"࠭࠲࠯࠷࠶࠲࠵࠭ᤵ")):
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
        bstack1lllll1ll_opy_ = bstack11ll1l_opy_ (u"ࠧࠨᤶ")
        if bstack11l111lll_opy_() >= version.parse(bstack11ll1l_opy_ (u"ࠨ࠶࠱࠴࠳࠶ࡢ࠲ࠩᤷ")):
            bstack1lllll1ll_opy_ = self.caps.get(bstack11ll1l_opy_ (u"ࠤࡲࡴࡹ࡯࡭ࡢ࡮ࡋࡹࡧ࡛ࡲ࡭ࠤᤸ"))
        else:
            bstack1lllll1ll_opy_ = self.capabilities.get(bstack11ll1l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮᤹ࠥ"))
        if bstack1lllll1ll_opy_:
            bstack1ll1ll1111_opy_(bstack1lllll1ll_opy_)
            if bstack11l111lll_opy_() <= version.parse(bstack11ll1l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫ᤺")):
                self.command_executor._url = bstack11ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨ᤻") + bstack1l1ll1l1ll_opy_ + bstack11ll1l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥ᤼")
            else:
                self.command_executor._url = bstack11ll1l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤ᤽") + bstack1lllll1ll_opy_ + bstack11ll1l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤ᤾")
            logger.debug(bstack1l1lll111l_opy_.format(bstack1lllll1ll_opy_))
        else:
            logger.debug(bstack11lll111l1_opy_.format(bstack11ll1l_opy_ (u"ࠤࡒࡴࡹ࡯࡭ࡢ࡮ࠣࡌࡺࡨࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ᤿")))
    except Exception as e:
        logger.debug(bstack11lll111l1_opy_.format(e))
    bstack1llll1l11l_opy_ = self.session_id
    if bstack11ll1l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪ᥀") in bstack11l11l11l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11ll1l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ᥁"), None)
        if item:
            bstack1ll111ll111_opy_ = getattr(item, bstack11ll1l_opy_ (u"ࠬࡥࡴࡦࡵࡷࡣࡨࡧࡳࡦࡡࡶࡸࡦࡸࡴࡦࡦࠪ᥂"), False)
            if not getattr(item, bstack11ll1l_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧ᥃"), None) and bstack1ll111ll111_opy_:
                setattr(store[bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫ᥄")], bstack11ll1l_opy_ (u"ࠨࡡࡧࡶ࡮ࡼࡥࡳࠩ᥅"), self)
        bstack1l1llll1_opy_.bstack1ll1l1l11l_opy_(self)
    bstack11l1l1l1l1_opy_.append(self)
    if bstack11ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᥆") in CONFIG and bstack11ll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᥇") in CONFIG[bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᥈")][bstack111llll1l_opy_]:
        bstack1111l1ll1_opy_ = CONFIG[bstack11ll1l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᥉")][bstack111llll1l_opy_][bstack11ll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᥊")]
    logger.debug(bstack1l1llll1l_opy_.format(bstack1llll1l11l_opy_))
def bstack1l1l11l111_opy_(self, url):
    global bstack1l1llllll1_opy_
    global CONFIG
    try:
        bstack1lll1l1l1l_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1l1llll11_opy_.format(str(err)))
    try:
        bstack1l1llllll1_opy_(self, url)
    except Exception as e:
        try:
            bstack1111l111_opy_ = str(e)
            if any(err_msg in bstack1111l111_opy_ for err_msg in bstack1111111l_opy_):
                bstack1lll1l1l1l_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1l1llll11_opy_.format(str(err)))
        raise e
def bstack1llll1ll1_opy_(item, when):
    global bstack111l1111l_opy_
    try:
        bstack111l1111l_opy_(item, when)
    except Exception as e:
        pass
def bstack11l1l1ll1_opy_(item, call, rep):
    global bstack1ll111llll_opy_
    global bstack11l1l1l1l1_opy_
    name = bstack11ll1l_opy_ (u"ࠧࠨ᥋")
    try:
        if rep.when == bstack11ll1l_opy_ (u"ࠨࡥࡤࡰࡱ࠭᥌"):
            bstack1llll1l11l_opy_ = threading.current_thread().bstackSessionId
            bstack1ll11ll11l1_opy_ = item.config.getoption(bstack11ll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᥍"))
            try:
                if (str(bstack1ll11ll11l1_opy_).lower() != bstack11ll1l_opy_ (u"ࠪࡸࡷࡻࡥࠨ᥎")):
                    name = str(rep.nodeid)
                    bstack1ll11l1ll1_opy_ = bstack11l1llll11_opy_(bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᥏"), name, bstack11ll1l_opy_ (u"ࠬ࠭ᥐ"), bstack11ll1l_opy_ (u"࠭ࠧᥑ"), bstack11ll1l_opy_ (u"ࠧࠨᥒ"), bstack11ll1l_opy_ (u"ࠨࠩᥓ"))
                    os.environ[bstack11ll1l_opy_ (u"ࠩࡓ࡝࡙ࡋࡓࡕࡡࡗࡉࡘ࡚࡟ࡏࡃࡐࡉࠬᥔ")] = name
                    for driver in bstack11l1l1l1l1_opy_:
                        if bstack1llll1l11l_opy_ == driver.session_id:
                            driver.execute_script(bstack1ll11l1ll1_opy_)
            except Exception as e:
                logger.debug(bstack11ll1l_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᥕ").format(str(e)))
            try:
                bstack1lll1ll1l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11ll1l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᥖ"):
                    status = bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᥗ") if rep.outcome.lower() == bstack11ll1l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᥘ") else bstack11ll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᥙ")
                    reason = bstack11ll1l_opy_ (u"ࠨࠩᥚ")
                    if status == bstack11ll1l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᥛ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11ll1l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᥜ") if status == bstack11ll1l_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᥝ") else bstack11ll1l_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᥞ")
                    data = name + bstack11ll1l_opy_ (u"࠭ࠠࡱࡣࡶࡷࡪࡪࠡࠨᥟ") if status == bstack11ll1l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᥠ") else name + bstack11ll1l_opy_ (u"ࠨࠢࡩࡥ࡮ࡲࡥࡥࠣࠣࠫᥡ") + reason
                    bstack11ll1l1ll1_opy_ = bstack11l1llll11_opy_(bstack11ll1l_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫᥢ"), bstack11ll1l_opy_ (u"ࠪࠫᥣ"), bstack11ll1l_opy_ (u"ࠫࠬᥤ"), bstack11ll1l_opy_ (u"ࠬ࠭ᥥ"), level, data)
                    for driver in bstack11l1l1l1l1_opy_:
                        if bstack1llll1l11l_opy_ == driver.session_id:
                            driver.execute_script(bstack11ll1l1ll1_opy_)
            except Exception as e:
                logger.debug(bstack11ll1l_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡧࡴࡴࡴࡦࡺࡷࠤ࡫ࡵࡲࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡹࡥࡴࡵ࡬ࡳࡳࡀࠠࡼࡿࠪᥦ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡷࡹࡧࡴࡦࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡩࡸࡺࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽࢀࠫᥧ").format(str(e)))
    bstack1ll111llll_opy_(item, call, rep)
notset = Notset()
def bstack11ll1lll11_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll1llll1l_opy_
    if str(name).lower() == bstack11ll1l_opy_ (u"ࠨࡦࡵ࡭ࡻ࡫ࡲࠨᥨ"):
        return bstack11ll1l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠣᥩ")
    else:
        return bstack1ll1llll1l_opy_(self, name, default, skip)
def bstack11l11ll11_opy_(self):
    global CONFIG
    global bstack111ll11l1_opy_
    try:
        proxy = bstack1lll1l1lll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11ll1l_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᥪ")):
                proxies = bstack11l1lll11l_opy_(proxy, bstack1llll111l_opy_())
                if len(proxies) > 0:
                    protocol, bstack1l1ll111l_opy_ = proxies.popitem()
                    if bstack11ll1l_opy_ (u"ࠦ࠿࠵࠯ࠣᥫ") in bstack1l1ll111l_opy_:
                        return bstack1l1ll111l_opy_
                    else:
                        return bstack11ll1l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᥬ") + bstack1l1ll111l_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11ll1l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡳࡶࡴࡾࡹࠡࡷࡵࡰࠥࡀࠠࡼࡿࠥᥭ").format(str(e)))
    return bstack111ll11l1_opy_(self)
def bstack11ll1l11l_opy_():
    return (bstack11ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᥮") in CONFIG or bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬ᥯") in CONFIG) and bstack1l1l111ll1_opy_() and bstack11l111lll_opy_() >= version.parse(
        bstack1l1lll11l1_opy_)
def bstack1111ll111_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1111l1ll1_opy_
    global bstack1l1l1l1l1l_opy_
    global bstack11l11l11l_opy_
    CONFIG[bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᥰ")] = str(bstack11l11l11l_opy_) + str(__version__)
    bstack111llll1l_opy_ = 0
    try:
        if bstack1l1l1l1l1l_opy_ is True:
            bstack111llll1l_opy_ = int(os.environ.get(bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᥱ")))
    except:
        bstack111llll1l_opy_ = 0
    CONFIG[bstack11ll1l_opy_ (u"ࠦ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᥲ")] = True
    bstack1ll11l1lll_opy_ = bstack11ll11ll1l_opy_(CONFIG, bstack111llll1l_opy_)
    logger.debug(bstack11lll11l1_opy_.format(str(bstack1ll11l1lll_opy_)))
    if CONFIG.get(bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᥳ")):
        bstack1l1lll1l1_opy_(bstack1ll11l1lll_opy_, bstack1ll1llll11_opy_)
    if bstack11ll1l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᥴ") in CONFIG and bstack11ll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᥵") in CONFIG[bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᥶")][bstack111llll1l_opy_]:
        bstack1111l1ll1_opy_ = CONFIG[bstack11ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᥷")][bstack111llll1l_opy_][bstack11ll1l_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᥸")]
    import urllib
    import json
    bstack11lll11lll_opy_ = bstack11ll1l_opy_ (u"ࠫࡼࡹࡳ࠻࠱࠲ࡧࡩࡶ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯࠲ࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠿ࡤࡣࡳࡷࡂ࠭᥹") + urllib.parse.quote(json.dumps(bstack1ll11l1lll_opy_))
    browser = self.connect(bstack11lll11lll_opy_)
    return browser
def bstack1lllll1lll_opy_():
    global bstack11ll11111l_opy_
    global bstack11l11l11l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack1l11l1l1l1_opy_
        if not bstack11111l1l1l_opy_():
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
def bstack1ll11l1l111_opy_():
    global CONFIG
    global bstack1llll1l1ll_opy_
    global bstack1l1ll1l1ll_opy_
    global bstack1ll1llll11_opy_
    global bstack1l1l1l1l1l_opy_
    global bstack1lll11l1l1_opy_
    CONFIG = json.loads(os.environ.get(bstack11ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠫ᥺")))
    bstack1llll1l1ll_opy_ = eval(os.environ.get(bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ᥻")))
    bstack1l1ll1l1ll_opy_ = os.environ.get(bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡈࡖࡄࡢ࡙ࡗࡒࠧ᥼"))
    bstack11l1llllll_opy_(CONFIG, bstack1llll1l1ll_opy_)
    bstack1lll11l1l1_opy_ = bstack1l1ll1ll11_opy_.bstack11l1l1l1ll_opy_(CONFIG, bstack1lll11l1l1_opy_)
    global bstack11llllllll_opy_
    global bstack11111111l_opy_
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
    except Exception as e:
        pass
    if (bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ᥽") in CONFIG or bstack11ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭᥾") in CONFIG) and bstack1l1l111ll1_opy_():
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
        logger.debug(bstack11ll1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡶࡲࠤࡷࡻ࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࡶࠫ᥿"))
    bstack1ll1llll11_opy_ = CONFIG.get(bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨᦀ"), {}).get(bstack11ll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧᦁ"))
    bstack1l1l1l1l1l_opy_ = True
    bstack11lll1l1l1_opy_(bstack11l1ll1lll_opy_)
if (bstack1111111111_opy_()):
    bstack1ll11l1l111_opy_()
@bstack11lll11l_opy_(class_method=False)
def bstack1ll111l1l11_opy_(hook_name, event, bstack1ll11l1lll1_opy_=None):
    if hook_name not in [bstack11ll1l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᦂ"), bstack11ll1l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࠫᦃ"), bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᦄ"), bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᦅ"), bstack11ll1l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᦆ"), bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠬᦇ"), bstack11ll1l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣࡲ࡫ࡴࡩࡱࡧࠫᦈ"), bstack11ll1l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᦉ")]:
        return
    node = store[bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩࡵࡧࡰࠫᦊ")]
    if hook_name in [bstack11ll1l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᦋ"), bstack11ll1l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠫᦌ")]:
        node = store[bstack11ll1l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡲࡵࡤࡶ࡮ࡨࡣ࡮ࡺࡥ࡮ࠩᦍ")]
    elif hook_name in [bstack11ll1l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠩᦎ"), bstack11ll1l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸ࠭ᦏ")]:
        node = store[bstack11ll1l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡤ࡮ࡤࡷࡸࡥࡩࡵࡧࡰࠫᦐ")]
    if event == bstack11ll1l_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫ࠧᦑ"):
        hook_type = bstack1lll111ll11_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l1lll11_opy_ = {
            bstack11ll1l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᦒ"): uuid,
            bstack11ll1l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᦓ"): bstack1lll11l1_opy_(),
            bstack11ll1l_opy_ (u"ࠪࡸࡾࡶࡥࠨᦔ"): bstack11ll1l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᦕ"),
            bstack11ll1l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᦖ"): hook_type,
            bstack11ll1l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᦗ"): hook_name
        }
        store[bstack11ll1l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᦘ")].append(uuid)
        bstack1ll11ll1111_opy_ = node.nodeid
        if hook_type == bstack11ll1l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᦙ"):
            if not _1lll111l_opy_.get(bstack1ll11ll1111_opy_, None):
                _1lll111l_opy_[bstack1ll11ll1111_opy_] = {bstack11ll1l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᦚ"): []}
            _1lll111l_opy_[bstack1ll11ll1111_opy_][bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᦛ")].append(bstack1l1lll11_opy_[bstack11ll1l_opy_ (u"ࠫࡺࡻࡩࡥࠩᦜ")])
        _1lll111l_opy_[bstack1ll11ll1111_opy_ + bstack11ll1l_opy_ (u"ࠬ࠳ࠧᦝ") + hook_name] = bstack1l1lll11_opy_
        bstack1ll11l1l1l1_opy_(node, bstack1l1lll11_opy_, bstack11ll1l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧᦞ"))
    elif event == bstack11ll1l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᦟ"):
        bstack1l111l11_opy_ = node.nodeid + bstack11ll1l_opy_ (u"ࠨ࠯ࠪᦠ") + hook_name
        _1lll111l_opy_[bstack1l111l11_opy_][bstack11ll1l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᦡ")] = bstack1lll11l1_opy_()
        bstack1ll11l111ll_opy_(_1lll111l_opy_[bstack1l111l11_opy_][bstack11ll1l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᦢ")])
        bstack1ll11l1l1l1_opy_(node, _1lll111l_opy_[bstack1l111l11_opy_], bstack11ll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᦣ"), bstack1ll111l1l1l_opy_=bstack1ll11l1lll1_opy_)
def bstack1ll111lll1l_opy_():
    global bstack1ll11l1l1ll_opy_
    if bstack1ll11l11ll_opy_():
        bstack1ll11l1l1ll_opy_ = bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᦤ")
    else:
        bstack1ll11l1l1ll_opy_ = bstack11ll1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᦥ")
@bstack1l1llll1_opy_.bstack1ll1l1111ll_opy_
def bstack1ll11l1llll_opy_():
    bstack1ll111lll1l_opy_()
    if bstack1l1l111ll1_opy_():
        bstack1l11l11ll1_opy_(bstack1l1llll1l1_opy_)
    try:
        bstack1lllllllll1_opy_(bstack1ll111l1l11_opy_)
    except Exception as e:
        logger.debug(bstack11ll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡨࡰࡱ࡮ࡷࠥࡶࡡࡵࡥ࡫࠾ࠥࢁࡽࠣᦦ").format(e))
bstack1ll11l1llll_opy_()