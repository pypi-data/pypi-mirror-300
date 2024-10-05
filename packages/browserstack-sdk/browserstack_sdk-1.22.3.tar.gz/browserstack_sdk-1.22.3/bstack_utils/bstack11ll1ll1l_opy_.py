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
import json
class bstack111lll111l_opy_(object):
  bstack11l1l1lll_opy_ = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"࠭ࡾࠨ࿷")), bstack11ll1l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࿸"))
  bstack111ll1llll_opy_ = os.path.join(bstack11l1l1lll_opy_, bstack11ll1l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵ࠱࡮ࡸࡵ࡮ࠨ࿹"))
  bstack111lll1111_opy_ = None
  perform_scan = None
  bstack1l1l1lllll_opy_ = None
  bstack1ll1l11ll_opy_ = None
  bstack11l1111ll1_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack11ll1l_opy_ (u"ࠩ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠫ࿺")):
      cls.instance = super(bstack111lll111l_opy_, cls).__new__(cls)
      cls.instance.bstack111ll1ll1l_opy_()
    return cls.instance
  def bstack111ll1ll1l_opy_(self):
    try:
      with open(self.bstack111ll1llll_opy_, bstack11ll1l_opy_ (u"ࠪࡶࠬ࿻")) as bstack11ll11l11_opy_:
        bstack111lll11l1_opy_ = bstack11ll11l11_opy_.read()
        data = json.loads(bstack111lll11l1_opy_)
        if bstack11ll1l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭࿼") in data:
          self.bstack11l11l1111_opy_(data[bstack11ll1l_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ࿽")])
        if bstack11ll1l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ࿾") in data:
          self.bstack111lllll11_opy_(data[bstack11ll1l_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ࿿")])
    except:
      pass
  def bstack111lllll11_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack11ll1l_opy_ (u"ࠨࡵࡦࡥࡳ࠭က")]
      self.bstack1l1l1lllll_opy_ = scripts[bstack11ll1l_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ခ")]
      self.bstack1ll1l11ll_opy_ = scripts[bstack11ll1l_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧဂ")]
      self.bstack11l1111ll1_opy_ = scripts[bstack11ll1l_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩဃ")]
  def bstack11l11l1111_opy_(self, bstack111lll1111_opy_):
    if bstack111lll1111_opy_ != None and len(bstack111lll1111_opy_) != 0:
      self.bstack111lll1111_opy_ = bstack111lll1111_opy_
  def store(self):
    try:
      with open(self.bstack111ll1llll_opy_, bstack11ll1l_opy_ (u"ࠬࡽࠧင")) as file:
        json.dump({
          bstack11ll1l_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࡳࠣစ"): self.bstack111lll1111_opy_,
          bstack11ll1l_opy_ (u"ࠢࡴࡥࡵ࡭ࡵࡺࡳࠣဆ"): {
            bstack11ll1l_opy_ (u"ࠣࡵࡦࡥࡳࠨဇ"): self.perform_scan,
            bstack11ll1l_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨဈ"): self.bstack1l1l1lllll_opy_,
            bstack11ll1l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢဉ"): self.bstack1ll1l11ll_opy_,
            bstack11ll1l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤည"): self.bstack11l1111ll1_opy_
          }
        }, file)
    except:
      pass
  def bstack1l11l1lll1_opy_(self, bstack111ll1lll1_opy_):
    try:
      return any(command.get(bstack11ll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪဋ")) == bstack111ll1lll1_opy_ for command in self.bstack111lll1111_opy_)
    except:
      return False
bstack11ll1ll1l_opy_ = bstack111lll111l_opy_()