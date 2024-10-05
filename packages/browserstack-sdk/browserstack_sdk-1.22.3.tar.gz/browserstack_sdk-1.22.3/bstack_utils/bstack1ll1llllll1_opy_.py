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
bstack1lll1111l11_opy_ = 1000
bstack1lll1111ll1_opy_ = 5
bstack1lll1111l1l_opy_ = 30
bstack1lll1111lll_opy_ = 2
class bstack1ll1lllllll_opy_:
    def __init__(self, handler, bstack1lll111l11l_opy_=bstack1lll1111l11_opy_, bstack1lll1111111_opy_=bstack1lll1111ll1_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1lll111l11l_opy_ = bstack1lll111l11l_opy_
        self.bstack1lll1111111_opy_ = bstack1lll1111111_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack1lll11111l1_opy_()
    def bstack1lll11111l1_opy_(self):
        self.timer = threading.Timer(self.bstack1lll1111111_opy_, self.bstack1lll11111ll_opy_)
        self.timer.start()
    def bstack1lll111l111_opy_(self):
        self.timer.cancel()
    def bstack1lll111111l_opy_(self):
        self.bstack1lll111l111_opy_()
        self.bstack1lll11111l1_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1lll111l11l_opy_:
                t = threading.Thread(target=self.bstack1lll11111ll_opy_)
                t.start()
                self.bstack1lll111111l_opy_()
    def bstack1lll11111ll_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1lll111l11l_opy_]
        del self.queue[:self.bstack1lll111l11l_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1lll111l111_opy_()
        while len(self.queue) > 0:
            self.bstack1lll11111ll_opy_()