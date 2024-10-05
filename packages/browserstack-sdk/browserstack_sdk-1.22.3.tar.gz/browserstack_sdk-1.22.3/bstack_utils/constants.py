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
import re
bstack1lll1l1l11_opy_ = {
	bstack11ll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪဣ"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷ࠭ဤ"),
  bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ဥ"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡯ࡪࡿࠧဦ"),
  bstack11ll1l_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨဧ"): bstack11ll1l_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪဨ"),
  bstack11ll1l_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧဩ"): bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡣࡼ࠹ࡣࠨဪ"),
  bstack11ll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧါ"): bstack11ll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࠫာ"),
  bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧိ"): bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࠫီ"),
  bstack11ll1l_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫု"): bstack11ll1l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬူ"),
  bstack11ll1l_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧေ"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭ࠧဲ"),
  bstack11ll1l_opy_ (u"ࠪࡧࡴࡴࡳࡰ࡮ࡨࡐࡴ࡭ࡳࠨဳ"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡳࡰ࡮ࡨࠫဴ"),
  bstack11ll1l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪဵ"): bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡒ࡯ࡨࡵࠪံ"),
  bstack11ll1l_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶ့ࠫ"): bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳࡌࡰࡩࡶࠫး"),
  bstack11ll1l_opy_ (u"ࠩࡹ࡭ࡩ࡫࡯ࠨ္"): bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡹ࡭ࡩ࡫࡯ࠨ်"),
  bstack11ll1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪျ"): bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸ࡫࡬ࡦࡰ࡬ࡹࡲࡒ࡯ࡨࡵࠪြ"),
  bstack11ll1l_opy_ (u"࠭ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ွ"): bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡴࡦ࡮ࡨࡱࡪࡺࡲࡺࡎࡲ࡫ࡸ࠭ှ"),
  bstack11ll1l_opy_ (u"ࠨࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭ဿ"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡩࡨࡳࡑࡵࡣࡢࡶ࡬ࡳࡳ࠭၀"),
  bstack11ll1l_opy_ (u"ࠪࡸ࡮ࡳࡥࡻࡱࡱࡩࠬ၁"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡸ࡮ࡳࡥࡻࡱࡱࡩࠬ၂"),
  bstack11ll1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ၃"): bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ၄"),
  bstack11ll1l_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭၅"): bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡮ࡣࡶ࡯ࡈࡵ࡭࡮ࡣࡱࡨࡸ࠭၆"),
  bstack11ll1l_opy_ (u"ࠩ࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧ၇"): bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡬ࡨࡱ࡫ࡔࡪ࡯ࡨࡳࡺࡺࠧ၈"),
  bstack11ll1l_opy_ (u"ࠫࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫ၉"): bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡲࡧࡳ࡬ࡄࡤࡷ࡮ࡩࡁࡶࡶ࡫ࠫ၊"),
  bstack11ll1l_opy_ (u"࠭ࡳࡦࡰࡧࡏࡪࡿࡳࠨ။"): bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦࡰࡧࡏࡪࡿࡳࠨ၌"),
  bstack11ll1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡡࡪࡶࠪ၍"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡸࡸࡴ࡝ࡡࡪࡶࠪ၎"),
  bstack11ll1l_opy_ (u"ࠪ࡬ࡴࡹࡴࡴࠩ၏"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡬ࡴࡹࡴࡴࠩၐ"),
  bstack11ll1l_opy_ (u"ࠬࡨࡦࡤࡣࡦ࡬ࡪ࠭ၑ"): bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡦࡤࡣࡦ࡬ࡪ࠭ၒ"),
  bstack11ll1l_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨၓ"): bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨၔ"),
  bstack11ll1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬၕ"): bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬၖ"),
  bstack11ll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨၗ"): bstack11ll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬၘ"),
  bstack11ll1l_opy_ (u"࠭ࡲࡦࡣ࡯ࡑࡴࡨࡩ࡭ࡧࠪၙ"): bstack11ll1l_opy_ (u"ࠧࡳࡧࡤࡰࡤࡳ࡯ࡣ࡫࡯ࡩࠬၚ"),
  bstack11ll1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨၛ"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩၜ"),
  bstack11ll1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪၝ"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡺࡹࡴࡰ࡯ࡑࡩࡹࡽ࡯ࡳ࡭ࠪၞ"),
  bstack11ll1l_opy_ (u"ࠬࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ၟ"): bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡴࡥࡵࡹࡲࡶࡰࡖࡲࡰࡨ࡬ࡰࡪ࠭ၠ"),
  bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡵࡺࡉ࡯ࡵࡨࡧࡺࡸࡥࡄࡧࡵࡸࡸ࠭ၡ"): bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡔࡵ࡯ࡇࡪࡸࡴࡴࠩၢ"),
  bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫၣ"): bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫၤ"),
  bstack11ll1l_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫၥ"): bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡸࡵࡵࡳࡥࡨࠫၦ"),
  bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨၧ"): bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨၨ"),
  bstack11ll1l_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪၩ"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡪࡲࡷࡹࡔࡡ࡮ࡧࠪၪ"),
  bstack11ll1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ၫ"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡩࡳࡧࡢ࡭ࡧࡖ࡭ࡲ࠭ၬ"),
  bstack11ll1l_opy_ (u"ࠬࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩၭ"): bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩၮ"),
  bstack11ll1l_opy_ (u"ࠧࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬၯ"): bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡲ࡯ࡳࡦࡪࡍࡦࡦ࡬ࡥࠬၰ")
}
bstack111l1llll1_opy_ = [
  bstack11ll1l_opy_ (u"ࠩࡲࡷࠬၱ"),
  bstack11ll1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ၲ"),
  bstack11ll1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ၳ"),
  bstack11ll1l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪၴ"),
  bstack11ll1l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪၵ"),
  bstack11ll1l_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫၶ"),
  bstack11ll1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨၷ"),
]
bstack1ll111lll_opy_ = {
  bstack11ll1l_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫၸ"): [bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡘࡗࡊࡘࡎࡂࡏࡈࠫၹ"), bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡠࡐࡄࡑࡊ࠭ၺ")],
  bstack11ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨၻ"): bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩၼ"),
  bstack11ll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪၽ"): bstack11ll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡎࡂࡏࡈࠫၾ"),
  bstack11ll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧၿ"): bstack11ll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡖࡔࡐࡅࡄࡖࡢࡒࡆࡓࡅࠨႀ"),
  bstack11ll1l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ႁ"): bstack11ll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧႂ"),
  bstack11ll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ႃ"): bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡂࡔࡄࡐࡑࡋࡌࡔࡡࡓࡉࡗࡥࡐࡍࡃࡗࡊࡔࡘࡍࠨႄ"),
  bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬႅ"): bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒࠧႆ"),
  bstack11ll1l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧႇ"): bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨႈ"),
  bstack11ll1l_opy_ (u"ࠬࡧࡰࡱࠩႉ"): [bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡐࡑࡡࡌࡈࠬႊ"), bstack11ll1l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࠪႋ")],
  bstack11ll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪႌ"): bstack11ll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡕࡇࡏࡤࡒࡏࡈࡎࡈ࡚ࡊࡒႍࠧ"),
  bstack11ll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧႎ"): bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧႏ"),
  bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ႐"): bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡓࡇ࡙ࡅࡓࡘࡄࡆࡎࡒࡉࡕ࡛ࠪ႑")
}
bstack11lll1ll1l_opy_ = {
  bstack11ll1l_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩ႒"): [bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨࡶࡤࡴࡡ࡮ࡧࠪ႓"), bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡔࡡ࡮ࡧࠪ႔")],
  bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭႕"): [bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡢ࡯ࡪࡿࠧ႖"), bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ႗")],
  bstack11ll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ႘"): bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ႙"),
  bstack11ll1l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ႚ"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ႛ"),
  bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬႜ"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬႝ"),
  bstack11ll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ႞"): [bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡶࡰࡱࠩ႟"), bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭Ⴀ")],
  bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬႡ"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࠧႢ"),
  bstack11ll1l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧႣ"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧႤ"),
  bstack11ll1l_opy_ (u"ࠬࡧࡰࡱࠩႥ"): bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡰࡱࠩႦ"),
  bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩႧ"): bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡪࡐࡪࡼࡥ࡭ࠩႨ"),
  bstack11ll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ⴉ"): bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭Ⴊ")
}
bstack1l111l1lll_opy_ = {
  bstack11ll1l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧႫ"): bstack11ll1l_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩႬ"),
  bstack11ll1l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨႭ"): [bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩႮ"), bstack11ll1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠫႯ")],
  bstack11ll1l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧႰ"): bstack11ll1l_opy_ (u"ࠪࡲࡦࡳࡥࠨႱ"),
  bstack11ll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨႲ"): bstack11ll1l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬႳ"),
  bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫႴ"): [bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨႵ"), bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧႶ")],
  bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪႷ"): bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬႸ"),
  bstack11ll1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨႹ"): bstack11ll1l_opy_ (u"ࠬࡸࡥࡢ࡮ࡢࡱࡴࡨࡩ࡭ࡧࠪႺ"),
  bstack11ll1l_opy_ (u"࠭ࡡࡱࡲ࡬ࡹࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ⴛ"): [bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲ࡬ࡹࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠧႼ"), bstack11ll1l_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩႽ")],
  bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡋࡱࡷࡪࡩࡵࡳࡧࡆࡩࡷࡺࡳࠨႾ"): [bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡖࡷࡱࡉࡥࡳࡶࡶࠫႿ"), bstack11ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࠫჀ")]
}
bstack1ll111l1ll_opy_ = [
  bstack11ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡎࡴࡳࡦࡥࡸࡶࡪࡉࡥࡳࡶࡶࠫჁ"),
  bstack11ll1l_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩჂ"),
  bstack11ll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭Ⴣ"),
  bstack11ll1l_opy_ (u"ࠨࡵࡨࡸ࡜࡯࡮ࡥࡱࡺࡖࡪࡩࡴࠨჄ"),
  bstack11ll1l_opy_ (u"ࠩࡷ࡭ࡲ࡫࡯ࡶࡶࡶࠫჅ"),
  bstack11ll1l_opy_ (u"ࠪࡷࡹࡸࡩࡤࡶࡉ࡭ࡱ࡫ࡉ࡯ࡶࡨࡶࡦࡩࡴࡢࡤ࡬ࡰ࡮ࡺࡹࠨ჆"),
  bstack11ll1l_opy_ (u"ࠫࡺࡴࡨࡢࡰࡧࡰࡪࡪࡐࡳࡱࡰࡴࡹࡈࡥࡩࡣࡹ࡭ࡴࡸࠧჇ"),
  bstack11ll1l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ჈"),
  bstack11ll1l_opy_ (u"࠭࡭ࡰࡼ࠽ࡪ࡮ࡸࡥࡧࡱࡻࡓࡵࡺࡩࡰࡰࡶࠫ჉"),
  bstack11ll1l_opy_ (u"ࠧ࡮ࡵ࠽ࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ჊"),
  bstack11ll1l_opy_ (u"ࠨࡵࡨ࠾࡮࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ჋"),
  bstack11ll1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪ჌"),
]
bstack1ll1l1ll1l_opy_ = [
  bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧჍ"),
  bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ჎"),
  bstack11ll1l_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫ჏"),
  bstack11ll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ა"),
  bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪბ"),
  bstack11ll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪგ"),
  bstack11ll1l_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬდ"),
  bstack11ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧე"),
  bstack11ll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧვ"),
  bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪზ"),
  bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪთ"),
  bstack11ll1l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠩი"),
  bstack11ll1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡕࡣࡪࠫკ"),
  bstack11ll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ლ"),
  bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬმ"),
  bstack11ll1l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨნ"),
  bstack11ll1l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠴ࠫო"),
  bstack11ll1l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠶ࠬპ"),
  bstack11ll1l_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠸࠭ჟ"),
  bstack11ll1l_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠺ࠧრ"),
  bstack11ll1l_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠵ࠨს"),
  bstack11ll1l_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠷ࠩტ"),
  bstack11ll1l_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠹ࠪუ"),
  bstack11ll1l_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠻ࠫფ"),
  bstack11ll1l_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠽ࠬქ"),
  bstack11ll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ღ"),
  bstack11ll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡏࡱࡶ࡬ࡳࡳࡹࠧყ"),
  bstack11ll1l_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬშ"),
  bstack11ll1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬჩ")
]
bstack111ll11111_opy_ = [
  bstack11ll1l_opy_ (u"ࠫࡺࡶ࡬ࡰࡣࡧࡑࡪࡪࡩࡢࠩც"),
  bstack11ll1l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧძ"),
  bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩწ"),
  bstack11ll1l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬჭ"),
  bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡖࡲࡪࡱࡵ࡭ࡹࡿࠧხ"),
  bstack11ll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬჯ"),
  bstack11ll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡖࡤ࡫ࠬჰ"),
  bstack11ll1l_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩჱ"),
  bstack11ll1l_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧჲ"),
  bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫჳ"),
  bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨჴ"),
  bstack11ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧჵ"),
  bstack11ll1l_opy_ (u"ࠩࡲࡷࠬჶ"),
  bstack11ll1l_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ჷ"),
  bstack11ll1l_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪჸ"),
  bstack11ll1l_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡥ࡮ࡺࠧჹ"),
  bstack11ll1l_opy_ (u"࠭ࡲࡦࡩ࡬ࡳࡳ࠭ჺ"),
  bstack11ll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡿࡵ࡮ࡦࠩ჻"),
  bstack11ll1l_opy_ (u"ࠨ࡯ࡤࡧ࡭࡯࡮ࡦࠩჼ"),
  bstack11ll1l_opy_ (u"ࠩࡵࡩࡸࡵ࡬ࡶࡶ࡬ࡳࡳ࠭ჽ"),
  bstack11ll1l_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨჾ"),
  bstack11ll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨჿ"),
  bstack11ll1l_opy_ (u"ࠬࡼࡩࡥࡧࡲࠫᄀ"),
  bstack11ll1l_opy_ (u"࠭࡮ࡰࡒࡤ࡫ࡪࡒ࡯ࡢࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪᄁ"),
  bstack11ll1l_opy_ (u"ࠧࡣࡨࡦࡥࡨ࡮ࡥࠨᄂ"),
  bstack11ll1l_opy_ (u"ࠨࡦࡨࡦࡺ࡭ࠧᄃ"),
  bstack11ll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᄄ"),
  bstack11ll1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡩࡳࡪࡋࡦࡻࡶࠫᄅ"),
  bstack11ll1l_opy_ (u"ࠫࡷ࡫ࡡ࡭ࡏࡲࡦ࡮ࡲࡥࠨᄆ"),
  bstack11ll1l_opy_ (u"ࠬࡴ࡯ࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠩᄇ"),
  bstack11ll1l_opy_ (u"࠭ࡣࡩࡧࡦ࡯࡚ࡘࡌࠨᄈ"),
  bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᄉ"),
  bstack11ll1l_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡄࡱࡲ࡯࡮࡫ࡳࠨᄊ"),
  bstack11ll1l_opy_ (u"ࠩࡦࡥࡵࡺࡵࡳࡧࡆࡶࡦࡹࡨࠨᄋ"),
  bstack11ll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᄌ"),
  bstack11ll1l_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᄍ"),
  bstack11ll1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡘࡨࡶࡸ࡯࡯࡯ࠩᄎ"),
  bstack11ll1l_opy_ (u"࠭࡮ࡰࡄ࡯ࡥࡳࡱࡐࡰ࡮࡯࡭ࡳ࡭ࠧᄏ"),
  bstack11ll1l_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡘ࡫࡮ࡥࡍࡨࡽࡸ࠭ᄐ"),
  bstack11ll1l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡍࡱࡪࡷࠬᄑ"),
  bstack11ll1l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡋࡧࠫᄒ"),
  bstack11ll1l_opy_ (u"ࠪࡨࡪࡪࡩࡤࡣࡷࡩࡩࡊࡥࡷ࡫ࡦࡩࠬᄓ"),
  bstack11ll1l_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡔࡦࡸࡡ࡮ࡵࠪᄔ"),
  bstack11ll1l_opy_ (u"ࠬࡶࡨࡰࡰࡨࡒࡺࡳࡢࡦࡴࠪᄕ"),
  bstack11ll1l_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫᄖ"),
  bstack11ll1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࡔࡶࡴࡪࡱࡱࡷࠬᄗ"),
  bstack11ll1l_opy_ (u"ࠨࡥࡲࡲࡸࡵ࡬ࡦࡎࡲ࡫ࡸ࠭ᄘ"),
  bstack11ll1l_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩᄙ"),
  bstack11ll1l_opy_ (u"ࠪࡥࡵࡶࡩࡶ࡯ࡏࡳ࡬ࡹࠧᄚ"),
  bstack11ll1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡆ࡮ࡵ࡭ࡦࡶࡵ࡭ࡨ࠭ᄛ"),
  bstack11ll1l_opy_ (u"ࠬࡼࡩࡥࡧࡲ࡚࠷࠭ᄜ"),
  bstack11ll1l_opy_ (u"࠭࡭ࡪࡦࡖࡩࡸࡹࡩࡰࡰࡌࡲࡸࡺࡡ࡭࡮ࡄࡴࡵࡹࠧᄝ"),
  bstack11ll1l_opy_ (u"ࠧࡦࡵࡳࡶࡪࡹࡳࡰࡕࡨࡶࡻ࡫ࡲࠨᄞ"),
  bstack11ll1l_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࡏࡳ࡬ࡹࠧᄟ"),
  bstack11ll1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡇࡩࡶࠧᄠ"),
  bstack11ll1l_opy_ (u"ࠪࡸࡪࡲࡥ࡮ࡧࡷࡶࡾࡒ࡯ࡨࡵࠪᄡ"),
  bstack11ll1l_opy_ (u"ࠫࡸࡿ࡮ࡤࡖ࡬ࡱࡪ࡝ࡩࡵࡪࡑࡘࡕ࠭ᄢ"),
  bstack11ll1l_opy_ (u"ࠬ࡭ࡥࡰࡎࡲࡧࡦࡺࡩࡰࡰࠪᄣ"),
  bstack11ll1l_opy_ (u"࠭ࡧࡱࡵࡏࡳࡨࡧࡴࡪࡱࡱࠫᄤ"),
  bstack11ll1l_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡑࡴࡲࡪ࡮ࡲࡥࠨᄥ"),
  bstack11ll1l_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡏࡧࡷࡻࡴࡸ࡫ࠨᄦ"),
  bstack11ll1l_opy_ (u"ࠩࡩࡳࡷࡩࡥࡄࡪࡤࡲ࡬࡫ࡊࡢࡴࠪᄧ"),
  bstack11ll1l_opy_ (u"ࠪࡼࡲࡹࡊࡢࡴࠪᄨ"),
  bstack11ll1l_opy_ (u"ࠫࡽࡳࡸࡋࡣࡵࠫᄩ"),
  bstack11ll1l_opy_ (u"ࠬࡳࡡࡴ࡭ࡆࡳࡲࡳࡡ࡯ࡦࡶࠫᄪ"),
  bstack11ll1l_opy_ (u"࠭࡭ࡢࡵ࡮ࡆࡦࡹࡩࡤࡃࡸࡸ࡭࠭ᄫ"),
  bstack11ll1l_opy_ (u"ࠧࡸࡵࡏࡳࡨࡧ࡬ࡔࡷࡳࡴࡴࡸࡴࠨᄬ"),
  bstack11ll1l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡅࡲࡶࡸࡘࡥࡴࡶࡵ࡭ࡨࡺࡩࡰࡰࡶࠫᄭ"),
  bstack11ll1l_opy_ (u"ࠩࡤࡴࡵ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᄮ"),
  bstack11ll1l_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩᄯ"),
  bstack11ll1l_opy_ (u"ࠫࡷ࡫ࡳࡪࡩࡱࡅࡵࡶࠧᄰ"),
  bstack11ll1l_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮ࡴࠩᄱ"),
  bstack11ll1l_opy_ (u"࠭ࡣࡢࡰࡤࡶࡾ࠭ᄲ"),
  bstack11ll1l_opy_ (u"ࠧࡧ࡫ࡵࡩ࡫ࡵࡸࠨᄳ"),
  bstack11ll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᄴ"),
  bstack11ll1l_opy_ (u"ࠩ࡬ࡩࠬᄵ"),
  bstack11ll1l_opy_ (u"ࠪࡩࡩ࡭ࡥࠨᄶ"),
  bstack11ll1l_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫᄷ"),
  bstack11ll1l_opy_ (u"ࠬࡷࡵࡦࡷࡨࠫᄸ"),
  bstack11ll1l_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨᄹ"),
  bstack11ll1l_opy_ (u"ࠧࡢࡲࡳࡗࡹࡵࡲࡦࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠨᄺ"),
  bstack11ll1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡄࡣࡰࡩࡷࡧࡉ࡮ࡣࡪࡩࡎࡴࡪࡦࡥࡷ࡭ࡴࡴࠧᄻ"),
  bstack11ll1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡏࡳ࡬ࡹࡅࡹࡥ࡯ࡹࡩ࡫ࡈࡰࡵࡷࡷࠬᄼ"),
  bstack11ll1l_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡊࡰࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭ᄽ"),
  bstack11ll1l_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡅࡵࡶࡓࡦࡶࡷ࡭ࡳ࡭ࡳࠨᄾ"),
  bstack11ll1l_opy_ (u"ࠬࡸࡥࡴࡧࡵࡺࡪࡊࡥࡷ࡫ࡦࡩࠬᄿ"),
  bstack11ll1l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᅀ"),
  bstack11ll1l_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩᅁ"),
  bstack11ll1l_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡑࡣࡶࡷࡨࡵࡤࡦࠩᅂ"),
  bstack11ll1l_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡋࡲࡷࡉ࡫ࡶࡪࡥࡨࡗࡪࡺࡴࡪࡰࡪࡷࠬᅃ"),
  bstack11ll1l_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡄࡹࡩ࡯࡯ࡊࡰ࡭ࡩࡨࡺࡩࡰࡰࠪᅄ"),
  bstack11ll1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡵࡶ࡬ࡦࡒࡤࡽࠬᅅ"),
  bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭ᅆ"),
  bstack11ll1l_opy_ (u"࠭ࡷࡥ࡫ࡲࡗࡪࡸࡶࡪࡥࡨࠫᅇ"),
  bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᅈ"),
  bstack11ll1l_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵࡅࡵࡳࡸࡹࡓࡪࡶࡨࡘࡷࡧࡣ࡬࡫ࡱ࡫ࠬᅉ"),
  bstack11ll1l_opy_ (u"ࠩ࡫࡭࡬࡮ࡃࡰࡰࡷࡶࡦࡹࡴࠨᅊ"),
  bstack11ll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡓࡶࡪ࡬ࡥࡳࡧࡱࡧࡪࡹࠧᅋ"),
  bstack11ll1l_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧᅌ"),
  bstack11ll1l_opy_ (u"ࠬࡹࡩ࡮ࡑࡳࡸ࡮ࡵ࡮ࡴࠩᅍ"),
  bstack11ll1l_opy_ (u"࠭ࡲࡦ࡯ࡲࡺࡪࡏࡏࡔࡃࡳࡴࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࡒ࡯ࡤࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᅎ"),
  bstack11ll1l_opy_ (u"ࠧࡩࡱࡶࡸࡓࡧ࡭ࡦࠩᅏ"),
  bstack11ll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᅐ"),
  bstack11ll1l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࠫᅑ"),
  bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᅒ"),
  bstack11ll1l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᅓ"),
  bstack11ll1l_opy_ (u"ࠬࡶࡡࡨࡧࡏࡳࡦࡪࡓࡵࡴࡤࡸࡪ࡭ࡹࠨᅔ"),
  bstack11ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬᅕ"),
  bstack11ll1l_opy_ (u"ࠧࡵ࡫ࡰࡩࡴࡻࡴࡴࠩᅖ"),
  bstack11ll1l_opy_ (u"ࠨࡷࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡔࡷࡵ࡭ࡱࡶࡅࡩ࡭ࡧࡶࡪࡱࡵࠫᅗ")
]
bstack1l1l1ll111_opy_ = {
  bstack11ll1l_opy_ (u"ࠩࡹࠫᅘ"): bstack11ll1l_opy_ (u"ࠪࡺࠬᅙ"),
  bstack11ll1l_opy_ (u"ࠫ࡫࠭ᅚ"): bstack11ll1l_opy_ (u"ࠬ࡬ࠧᅛ"),
  bstack11ll1l_opy_ (u"࠭ࡦࡰࡴࡦࡩࠬᅜ"): bstack11ll1l_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭ᅝ"),
  bstack11ll1l_opy_ (u"ࠨࡱࡱࡰࡾࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᅞ"): bstack11ll1l_opy_ (u"ࠩࡲࡲࡱࡿࡁࡶࡶࡲࡱࡦࡺࡥࠨᅟ"),
  bstack11ll1l_opy_ (u"ࠪࡪࡴࡸࡣࡦ࡮ࡲࡧࡦࡲࠧᅠ"): bstack11ll1l_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨᅡ"),
  bstack11ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨᅢ"): bstack11ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡍࡵࡳࡵࠩᅣ"),
  bstack11ll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪᅤ"): bstack11ll1l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡰࡴࡷࠫᅥ"),
  bstack11ll1l_opy_ (u"ࠩࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᅦ"): bstack11ll1l_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᅧ"),
  bstack11ll1l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡳࡥࡸࡹࠧᅨ"): bstack11ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡔࡦࡹࡳࠨᅩ"),
  bstack11ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻ࡫ࡳࡸࡺࠧᅪ"): bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼࡌࡴࡹࡴࠨᅫ"),
  bstack11ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡵࡲࡵࠩᅬ"): bstack11ll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖ࡯ࡳࡶࠪᅭ"),
  bstack11ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡵࡴࡧࡵࠫᅮ"): bstack11ll1l_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᅯ"),
  bstack11ll1l_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡵࡸ࡯ࡹࡻࡸࡷࡪࡸࠧᅰ"): bstack11ll1l_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡖࡲࡰࡺࡼ࡙ࡸ࡫ࡲࠨᅱ"),
  bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᅲ"): bstack11ll1l_opy_ (u"ࠨ࠯࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪᅳ"),
  bstack11ll1l_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡲࡵࡳࡽࡿࡰࡢࡵࡶࠫᅴ"): bstack11ll1l_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡓࡶࡴࡾࡹࡑࡣࡶࡷࠬᅵ"),
  bstack11ll1l_opy_ (u"ࠫࡧ࡯࡮ࡢࡴࡼࡴࡦࡺࡨࠨᅶ"): bstack11ll1l_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩᅷ"),
  bstack11ll1l_opy_ (u"࠭ࡰࡢࡥࡩ࡭ࡱ࡫ࠧᅸ"): bstack11ll1l_opy_ (u"ࠧ࠮ࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᅹ"),
  bstack11ll1l_opy_ (u"ࠨࡲࡤࡧ࠲࡬ࡩ࡭ࡧࠪᅺ"): bstack11ll1l_opy_ (u"ࠩ࠰ࡴࡦࡩ࠭ࡧ࡫࡯ࡩࠬᅻ"),
  bstack11ll1l_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᅼ"): bstack11ll1l_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᅽ"),
  bstack11ll1l_opy_ (u"ࠬࡲ࡯ࡨࡨ࡬ࡰࡪ࠭ᅾ"): bstack11ll1l_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧᅿ"),
  bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᆀ"): bstack11ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᆁ"),
}
bstack111l1l1ll1_opy_ = bstack11ll1l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳ࠻࠱࠲࡫࡮ࡺࡨࡶࡤ࠱ࡧࡴࡳ࠯ࡱࡧࡵࡧࡾ࠵ࡣ࡭࡫࠲ࡶࡪࡲࡥࡢࡵࡨࡷ࠴ࡲࡡࡵࡧࡶࡸ࠴ࡪ࡯ࡸࡰ࡯ࡳࡦࡪࠢᆂ")
bstack111l1ll111_opy_ = bstack11ll1l_opy_ (u"ࠥ࠳ࡵ࡫ࡲࡤࡻ࠲࡬ࡪࡧ࡬ࡵࡪࡦ࡬ࡪࡩ࡫ࠣᆃ")
bstack11ll1l1l1_opy_ = bstack11ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡽࡤ࠰ࡪࡸࡦࠬᆄ")
bstack1lll11ll11_opy_ = bstack11ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡮ࡵࡣ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠨᆅ")
bstack1ll1111l1l_opy_ = bstack11ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡩࡷࡥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯࡯ࡧࡻࡸࡤ࡮ࡵࡣࡵࠪᆆ")
bstack111ll11l11_opy_ = {
  bstack11ll1l_opy_ (u"ࠧࡤࡴ࡬ࡸ࡮ࡩࡡ࡭ࠩᆇ"): 50,
  bstack11ll1l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᆈ"): 40,
  bstack11ll1l_opy_ (u"ࠩࡺࡥࡷࡴࡩ࡯ࡩࠪᆉ"): 30,
  bstack11ll1l_opy_ (u"ࠪ࡭ࡳ࡬࡯ࠨᆊ"): 20,
  bstack11ll1l_opy_ (u"ࠫࡩ࡫ࡢࡶࡩࠪᆋ"): 10
}
bstack11l1l11l1l_opy_ = bstack111ll11l11_opy_[bstack11ll1l_opy_ (u"ࠬ࡯࡮ࡧࡱࠪᆌ")]
bstack1ll11ll11_opy_ = bstack11ll1l_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᆍ")
bstack1l1l1ll11l_opy_ = bstack11ll1l_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡰࡺࡶ࡫ࡳࡳࡧࡧࡦࡰࡷ࠳ࠬᆎ")
bstack1l1l11ll1l_opy_ = bstack11ll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥ࠮ࡲࡼࡸ࡭ࡵ࡮ࡢࡩࡨࡲࡹ࠵ࠧᆏ")
bstack11l1ll1lll_opy_ = bstack11ll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᆐ")
bstack11l1ll1l_opy_ = bstack11ll1l_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡵࡿࡴࡦࡵࡷࠤࡦࡴࡤࠡࡲࡼࡸࡪࡹࡴ࠮ࡵࡨࡰࡪࡴࡩࡶ࡯ࠣࡴࡦࡩ࡫ࡢࡩࡨࡷ࠳ࠦࡠࡱ࡫ࡳࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡶࡹࡵࡧࡶࡸ࠲ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡠࠨᆑ")
bstack111ll111l1_opy_ = [bstack11ll1l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᆒ"), bstack11ll1l_opy_ (u"ࠬ࡟ࡏࡖࡔࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬᆓ")]
bstack111l1ll11l_opy_ = [bstack11ll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᆔ"), bstack11ll1l_opy_ (u"࡚ࠧࡑࡘࡖࡤࡇࡃࡄࡇࡖࡗࡤࡑࡅ࡚ࠩᆕ")]
bstack11l1lllll1_opy_ = re.compile(bstack11ll1l_opy_ (u"ࠨࡠ࡞ࡠࡡࡽ࠭࡞࠭࠽࠲࠯ࠪࠧᆖ"))
bstack111lll1ll_opy_ = [
  bstack11ll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡔࡡ࡮ࡧࠪᆗ"),
  bstack11ll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᆘ"),
  bstack11ll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᆙ"),
  bstack11ll1l_opy_ (u"ࠬࡴࡥࡸࡅࡲࡱࡲࡧ࡮ࡥࡖ࡬ࡱࡪࡵࡵࡵࠩᆚ"),
  bstack11ll1l_opy_ (u"࠭ࡡࡱࡲࠪᆛ"),
  bstack11ll1l_opy_ (u"ࠧࡶࡦ࡬ࡨࠬᆜ"),
  bstack11ll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᆝ"),
  bstack11ll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡦࠩᆞ"),
  bstack11ll1l_opy_ (u"ࠪࡳࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᆟ"),
  bstack11ll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡙ࡨࡦࡻ࡯ࡥࡸࠩᆠ"),
  bstack11ll1l_opy_ (u"ࠬࡴ࡯ࡓࡧࡶࡩࡹ࠭ᆡ"), bstack11ll1l_opy_ (u"࠭ࡦࡶ࡮࡯ࡖࡪࡹࡥࡵࠩᆢ"),
  bstack11ll1l_opy_ (u"ࠧࡤ࡮ࡨࡥࡷ࡙ࡹࡴࡶࡨࡱࡋ࡯࡬ࡦࡵࠪᆣ"),
  bstack11ll1l_opy_ (u"ࠨࡧࡹࡩࡳࡺࡔࡪ࡯࡬ࡲ࡬ࡹࠧᆤ"),
  bstack11ll1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡨࡶ࡫ࡵࡲ࡮ࡣࡱࡧࡪࡒ࡯ࡨࡩ࡬ࡲ࡬࠭ᆥ"),
  bstack11ll1l_opy_ (u"ࠪࡳࡹ࡮ࡥࡳࡃࡳࡴࡸ࠭ᆦ"),
  bstack11ll1l_opy_ (u"ࠫࡵࡸࡩ࡯ࡶࡓࡥ࡬࡫ࡓࡰࡷࡵࡧࡪࡕ࡮ࡇ࡫ࡱࡨࡋࡧࡩ࡭ࡷࡵࡩࠬᆧ"),
  bstack11ll1l_opy_ (u"ࠬࡧࡰࡱࡃࡦࡸ࡮ࡼࡩࡵࡻࠪᆨ"), bstack11ll1l_opy_ (u"࠭ࡡࡱࡲࡓࡥࡨࡱࡡࡨࡧࠪᆩ"), bstack11ll1l_opy_ (u"ࠧࡢࡲࡳ࡛ࡦ࡯ࡴࡂࡥࡷ࡭ࡻ࡯ࡴࡺࠩᆪ"), bstack11ll1l_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡒࡤࡧࡰࡧࡧࡦࠩᆫ"), bstack11ll1l_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡇࡹࡷࡧࡴࡪࡱࡱࠫᆬ"),
  bstack11ll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡕࡩࡦࡪࡹࡕ࡫ࡰࡩࡴࡻࡴࠨᆭ"),
  bstack11ll1l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡗࡩࡸࡺࡐࡢࡥ࡮ࡥ࡬࡫ࡳࠨᆮ"),
  bstack11ll1l_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡉ࡯ࡷࡧࡵࡥ࡬࡫ࠧᆯ"), bstack11ll1l_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࡆࡰࡧࡍࡳࡺࡥ࡯ࡶࠪᆰ"),
  bstack11ll1l_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡅࡧࡹ࡭ࡨ࡫ࡒࡦࡣࡧࡽ࡙࡯࡭ࡦࡱࡸࡸࠬᆱ"),
  bstack11ll1l_opy_ (u"ࠨࡣࡧࡦࡕࡵࡲࡵࠩᆲ"),
  bstack11ll1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡇࡩࡻ࡯ࡣࡦࡕࡲࡧࡰ࡫ࡴࠨᆳ"),
  bstack11ll1l_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡍࡳࡹࡴࡢ࡮࡯ࡘ࡮ࡳࡥࡰࡷࡷࠫᆴ"),
  bstack11ll1l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰࡕࡧࡴࡩࠩᆵ"),
  bstack11ll1l_opy_ (u"ࠬࡧࡶࡥࠩᆶ"), bstack11ll1l_opy_ (u"࠭ࡡࡷࡦࡏࡥࡺࡴࡣࡩࡖ࡬ࡱࡪࡵࡵࡵࠩᆷ"), bstack11ll1l_opy_ (u"ࠧࡢࡸࡧࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᆸ"), bstack11ll1l_opy_ (u"ࠨࡣࡹࡨࡆࡸࡧࡴࠩᆹ"),
  bstack11ll1l_opy_ (u"ࠩࡸࡷࡪࡑࡥࡺࡵࡷࡳࡷ࡫ࠧᆺ"), bstack11ll1l_opy_ (u"ࠪ࡯ࡪࡿࡳࡵࡱࡵࡩࡕࡧࡴࡩࠩᆻ"), bstack11ll1l_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡴࡵࡺࡳࡷࡪࠧᆼ"),
  bstack11ll1l_opy_ (u"ࠬࡱࡥࡺࡃ࡯࡭ࡦࡹࠧᆽ"), bstack11ll1l_opy_ (u"࠭࡫ࡦࡻࡓࡥࡸࡹࡷࡰࡴࡧࠫᆾ"),
  bstack11ll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩᆿ"), bstack11ll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡁࡳࡩࡶࠫᇀ"), bstack11ll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡆࡺࡨࡧࡺࡺࡡࡣ࡮ࡨࡈ࡮ࡸࠧᇁ"), bstack11ll1l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡅ࡫ࡶࡴࡳࡥࡎࡣࡳࡴ࡮ࡴࡧࡇ࡫࡯ࡩࠬᇂ"), bstack11ll1l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡘࡷࡪ࡙ࡹࡴࡶࡨࡱࡊࡾࡥࡤࡷࡷࡥࡧࡲࡥࠨᇃ"),
  bstack11ll1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵࡔࡴࡸࡴࠨᇄ"), bstack11ll1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࡵࠪᇅ"),
  bstack11ll1l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡊࡩࡴࡣࡥࡰࡪࡈࡵࡪ࡮ࡧࡇ࡭࡫ࡣ࡬ࠩᇆ"),
  bstack11ll1l_opy_ (u"ࠨࡣࡸࡸࡴ࡝ࡥࡣࡸ࡬ࡩࡼ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᇇ"),
  bstack11ll1l_opy_ (u"ࠩ࡬ࡲࡹ࡫࡮ࡵࡃࡦࡸ࡮ࡵ࡮ࠨᇈ"), bstack11ll1l_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡆࡥࡹ࡫ࡧࡰࡴࡼࠫᇉ"), bstack11ll1l_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡊࡱࡧࡧࡴࠩᇊ"), bstack11ll1l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡦࡲࡉ࡯ࡶࡨࡲࡹࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨᇋ"),
  bstack11ll1l_opy_ (u"࠭ࡤࡰࡰࡷࡗࡹࡵࡰࡂࡲࡳࡓࡳࡘࡥࡴࡧࡷࠫᇌ"),
  bstack11ll1l_opy_ (u"ࠧࡶࡰ࡬ࡧࡴࡪࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩᇍ"), bstack11ll1l_opy_ (u"ࠨࡴࡨࡷࡪࡺࡋࡦࡻࡥࡳࡦࡸࡤࠨᇎ"),
  bstack11ll1l_opy_ (u"ࠩࡱࡳࡘ࡯ࡧ࡯ࠩᇏ"),
  bstack11ll1l_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࡘࡲ࡮ࡳࡰࡰࡴࡷࡥࡳࡺࡖࡪࡧࡺࡷࠬᇐ"),
  bstack11ll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡴࡤࡳࡱ࡬ࡨ࡜ࡧࡴࡤࡪࡨࡶࡸ࠭ᇑ"),
  bstack11ll1l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᇒ"),
  bstack11ll1l_opy_ (u"࠭ࡲࡦࡥࡵࡩࡦࡺࡥࡄࡪࡵࡳࡲ࡫ࡄࡳ࡫ࡹࡩࡷ࡙ࡥࡴࡵ࡬ࡳࡳࡹࠧᇓ"),
  bstack11ll1l_opy_ (u"ࠧ࡯ࡣࡷ࡭ࡻ࡫ࡗࡦࡤࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ᇔ"),
  bstack11ll1l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡕࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡕࡧࡴࡩࠩᇕ"),
  bstack11ll1l_opy_ (u"ࠩࡱࡩࡹࡽ࡯ࡳ࡭ࡖࡴࡪ࡫ࡤࠨᇖ"),
  bstack11ll1l_opy_ (u"ࠪ࡫ࡵࡹࡅ࡯ࡣࡥࡰࡪࡪࠧᇗ"),
  bstack11ll1l_opy_ (u"ࠫ࡮ࡹࡈࡦࡣࡧࡰࡪࡹࡳࠨᇘ"),
  bstack11ll1l_opy_ (u"ࠬࡧࡤࡣࡇࡻࡩࡨ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᇙ"),
  bstack11ll1l_opy_ (u"࠭࡬ࡰࡥࡤࡰࡪ࡙ࡣࡳ࡫ࡳࡸࠬᇚ"),
  bstack11ll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡉ࡫ࡶࡪࡥࡨࡍࡳ࡯ࡴࡪࡣ࡯࡭ࡿࡧࡴࡪࡱࡱࠫᇛ"),
  bstack11ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡍࡲࡢࡰࡷࡔࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠨᇜ"),
  bstack11ll1l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡑࡥࡹࡻࡲࡢ࡮ࡒࡶ࡮࡫࡮ࡵࡣࡷ࡭ࡴࡴࠧᇝ"),
  bstack11ll1l_opy_ (u"ࠪࡷࡾࡹࡴࡦ࡯ࡓࡳࡷࡺࠧᇞ"),
  bstack11ll1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡩࡨࡈࡰࡵࡷࠫᇟ"),
  bstack11ll1l_opy_ (u"ࠬࡹ࡫ࡪࡲࡘࡲࡱࡵࡣ࡬ࠩᇠ"), bstack11ll1l_opy_ (u"࠭ࡵ࡯࡮ࡲࡧࡰ࡚ࡹࡱࡧࠪᇡ"), bstack11ll1l_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡋࡦࡻࠪᇢ"),
  bstack11ll1l_opy_ (u"ࠨࡣࡸࡸࡴࡒࡡࡶࡰࡦ࡬ࠬᇣ"),
  bstack11ll1l_opy_ (u"ࠩࡶ࡯࡮ࡶࡌࡰࡩࡦࡥࡹࡉࡡࡱࡶࡸࡶࡪ࠭ᇤ"),
  bstack11ll1l_opy_ (u"ࠪࡹࡳ࡯࡮ࡴࡶࡤࡰࡱࡕࡴࡩࡧࡵࡔࡦࡩ࡫ࡢࡩࡨࡷࠬᇥ"),
  bstack11ll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩ࡜࡯࡮ࡥࡱࡺࡅࡳ࡯࡭ࡢࡶ࡬ࡳࡳ࠭ᇦ"),
  bstack11ll1l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡘࡴࡵ࡬ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᇧ"),
  bstack11ll1l_opy_ (u"࠭ࡥ࡯ࡨࡲࡶࡨ࡫ࡁࡱࡲࡌࡲࡸࡺࡡ࡭࡮ࠪᇨ"),
  bstack11ll1l_opy_ (u"ࠧࡦࡰࡶࡹࡷ࡫ࡗࡦࡤࡹ࡭ࡪࡽࡳࡉࡣࡹࡩࡕࡧࡧࡦࡵࠪᇩ"), bstack11ll1l_opy_ (u"ࠨࡹࡨࡦࡻ࡯ࡥࡸࡆࡨࡺࡹࡵ࡯࡭ࡵࡓࡳࡷࡺࠧᇪ"), bstack11ll1l_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦ࡙ࡨࡦࡻ࡯ࡥࡸࡆࡨࡸࡦ࡯࡬ࡴࡅࡲࡰࡱ࡫ࡣࡵ࡫ࡲࡲࠬᇫ"),
  bstack11ll1l_opy_ (u"ࠪࡶࡪࡳ࡯ࡵࡧࡄࡴࡵࡹࡃࡢࡥ࡫ࡩࡑ࡯࡭ࡪࡶࠪᇬ"),
  bstack11ll1l_opy_ (u"ࠫࡨࡧ࡬ࡦࡰࡧࡥࡷࡌ࡯ࡳ࡯ࡤࡸࠬᇭ"),
  bstack11ll1l_opy_ (u"ࠬࡨࡵ࡯ࡦ࡯ࡩࡎࡪࠧᇮ"),
  bstack11ll1l_opy_ (u"࠭࡬ࡢࡷࡱࡧ࡭࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᇯ"),
  bstack11ll1l_opy_ (u"ࠧ࡭ࡱࡦࡥࡹ࡯࡯࡯ࡕࡨࡶࡻ࡯ࡣࡦࡵࡈࡲࡦࡨ࡬ࡦࡦࠪᇰ"), bstack11ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡅࡺࡺࡨࡰࡴ࡬ࡾࡪࡪࠧᇱ"),
  bstack11ll1l_opy_ (u"ࠩࡤࡹࡹࡵࡁࡤࡥࡨࡴࡹࡇ࡬ࡦࡴࡷࡷࠬᇲ"), bstack11ll1l_opy_ (u"ࠪࡥࡺࡺ࡯ࡅ࡫ࡶࡱ࡮ࡹࡳࡂ࡮ࡨࡶࡹࡹࠧᇳ"),
  bstack11ll1l_opy_ (u"ࠫࡳࡧࡴࡪࡸࡨࡍࡳࡹࡴࡳࡷࡰࡩࡳࡺࡳࡍ࡫ࡥࠫᇴ"),
  bstack11ll1l_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩ࡜࡫ࡢࡕࡣࡳࠫᇵ"),
  bstack11ll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮ࡏ࡮ࡪࡶ࡬ࡥࡱ࡛ࡲ࡭ࠩᇶ"), bstack11ll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡁ࡭࡮ࡲࡻࡕࡵࡰࡶࡲࡶࠫᇷ"), bstack11ll1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡊࡩࡱࡳࡷ࡫ࡆࡳࡣࡸࡨ࡜ࡧࡲ࡯࡫ࡱ࡫ࠬᇸ"), bstack11ll1l_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡑࡳࡩࡳࡒࡩ࡯࡭ࡶࡍࡳࡈࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠩᇹ"),
  bstack11ll1l_opy_ (u"ࠪ࡯ࡪ࡫ࡰࡌࡧࡼࡇ࡭ࡧࡩ࡯ࡵࠪᇺ"),
  bstack11ll1l_opy_ (u"ࠫࡱࡵࡣࡢ࡮࡬ࡾࡦࡨ࡬ࡦࡕࡷࡶ࡮ࡴࡧࡴࡆ࡬ࡶࠬᇻ"),
  bstack11ll1l_opy_ (u"ࠬࡶࡲࡰࡥࡨࡷࡸࡇࡲࡨࡷࡰࡩࡳࡺࡳࠨᇼ"),
  bstack11ll1l_opy_ (u"࠭ࡩ࡯ࡶࡨࡶࡐ࡫ࡹࡅࡧ࡯ࡥࡾ࠭ᇽ"),
  bstack11ll1l_opy_ (u"ࠧࡴࡪࡲࡻࡎࡕࡓࡍࡱࡪࠫᇾ"),
  bstack11ll1l_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡕࡷࡶࡦࡺࡥࡨࡻࠪᇿ"),
  bstack11ll1l_opy_ (u"ࠩࡺࡩࡧࡱࡩࡵࡔࡨࡷࡵࡵ࡮ࡴࡧࡗ࡭ࡲ࡫࡯ࡶࡶࠪሀ"), bstack11ll1l_opy_ (u"ࠪࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡗࡢ࡫ࡷࡘ࡮ࡳࡥࡰࡷࡷࠫሁ"),
  bstack11ll1l_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡈࡪࡨࡵࡨࡒࡵࡳࡽࡿࠧሂ"),
  bstack11ll1l_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡹࡹ࡯ࡥࡈࡼࡪࡩࡵࡵࡧࡉࡶࡴࡳࡈࡵࡶࡳࡷࠬሃ"),
  bstack11ll1l_opy_ (u"࠭ࡳ࡬࡫ࡳࡐࡴ࡭ࡃࡢࡲࡷࡹࡷ࡫ࠧሄ"),
  bstack11ll1l_opy_ (u"ࠧࡸࡧࡥ࡯࡮ࡺࡄࡦࡤࡸ࡫ࡕࡸ࡯ࡹࡻࡓࡳࡷࡺࠧህ"),
  bstack11ll1l_opy_ (u"ࠨࡨࡸࡰࡱࡉ࡯࡯ࡶࡨࡼࡹࡒࡩࡴࡶࠪሆ"),
  bstack11ll1l_opy_ (u"ࠩࡺࡥ࡮ࡺࡆࡰࡴࡄࡴࡵ࡙ࡣࡳ࡫ࡳࡸࠬሇ"),
  bstack11ll1l_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࡇࡴࡴ࡮ࡦࡥࡷࡖࡪࡺࡲࡪࡧࡶࠫለ"),
  bstack11ll1l_opy_ (u"ࠫࡦࡶࡰࡏࡣࡰࡩࠬሉ"),
  bstack11ll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡘ࡙ࡌࡄࡧࡵࡸࠬሊ"),
  bstack11ll1l_opy_ (u"࠭ࡴࡢࡲ࡚࡭ࡹ࡮ࡓࡩࡱࡵࡸࡕࡸࡥࡴࡵࡇࡹࡷࡧࡴࡪࡱࡱࠫላ"),
  bstack11ll1l_opy_ (u"ࠧࡴࡥࡤࡰࡪࡌࡡࡤࡶࡲࡶࠬሌ"),
  bstack11ll1l_opy_ (u"ࠨࡹࡧࡥࡑࡵࡣࡢ࡮ࡓࡳࡷࡺࠧል"),
  bstack11ll1l_opy_ (u"ࠩࡶ࡬ࡴࡽࡘࡤࡱࡧࡩࡑࡵࡧࠨሎ"),
  bstack11ll1l_opy_ (u"ࠪ࡭ࡴࡹࡉ࡯ࡵࡷࡥࡱࡲࡐࡢࡷࡶࡩࠬሏ"),
  bstack11ll1l_opy_ (u"ࠫࡽࡩ࡯ࡥࡧࡆࡳࡳ࡬ࡩࡨࡈ࡬ࡰࡪ࠭ሐ"),
  bstack11ll1l_opy_ (u"ࠬࡱࡥࡺࡥ࡫ࡥ࡮ࡴࡐࡢࡵࡶࡻࡴࡸࡤࠨሑ"),
  bstack11ll1l_opy_ (u"࠭ࡵࡴࡧࡓࡶࡪࡨࡵࡪ࡮ࡷ࡛ࡉࡇࠧሒ"),
  bstack11ll1l_opy_ (u"ࠧࡱࡴࡨࡺࡪࡴࡴࡘࡆࡄࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠨሓ"),
  bstack11ll1l_opy_ (u"ࠨࡹࡨࡦࡉࡸࡩࡷࡧࡵࡅ࡬࡫࡮ࡵࡗࡵࡰࠬሔ"),
  bstack11ll1l_opy_ (u"ࠩ࡮ࡩࡾࡩࡨࡢ࡫ࡱࡔࡦࡺࡨࠨሕ"),
  bstack11ll1l_opy_ (u"ࠪࡹࡸ࡫ࡎࡦࡹ࡚ࡈࡆ࠭ሖ"),
  bstack11ll1l_opy_ (u"ࠫࡼࡪࡡࡍࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧሗ"), bstack11ll1l_opy_ (u"ࠬࡽࡤࡢࡅࡲࡲࡳ࡫ࡣࡵ࡫ࡲࡲ࡙࡯࡭ࡦࡱࡸࡸࠬመ"),
  bstack11ll1l_opy_ (u"࠭ࡸࡤࡱࡧࡩࡔࡸࡧࡊࡦࠪሙ"), bstack11ll1l_opy_ (u"ࠧࡹࡥࡲࡨࡪ࡙ࡩࡨࡰ࡬ࡲ࡬ࡏࡤࠨሚ"),
  bstack11ll1l_opy_ (u"ࠨࡷࡳࡨࡦࡺࡥࡥ࡙ࡇࡅࡇࡻ࡮ࡥ࡮ࡨࡍࡩ࠭ማ"),
  bstack11ll1l_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡐࡰࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡸࡴࡐࡰ࡯ࡽࠬሜ"),
  bstack11ll1l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡘ࡮ࡳࡥࡰࡷࡷࡷࠬም"),
  bstack11ll1l_opy_ (u"ࠫࡼࡪࡡࡔࡶࡤࡶࡹࡻࡰࡓࡧࡷࡶ࡮࡫ࡳࠨሞ"), bstack11ll1l_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷࡿࡉ࡯ࡶࡨࡶࡻࡧ࡬ࠨሟ"),
  bstack11ll1l_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࡈࡢࡴࡧࡻࡦࡸࡥࡌࡧࡼࡦࡴࡧࡲࡥࠩሠ"),
  bstack11ll1l_opy_ (u"ࠧ࡮ࡣࡻࡘࡾࡶࡩ࡯ࡩࡉࡶࡪࡷࡵࡦࡰࡦࡽࠬሡ"),
  bstack11ll1l_opy_ (u"ࠨࡵ࡬ࡱࡵࡲࡥࡊࡵ࡙࡭ࡸ࡯ࡢ࡭ࡧࡆ࡬ࡪࡩ࡫ࠨሢ"),
  bstack11ll1l_opy_ (u"ࠩࡸࡷࡪࡉࡡࡳࡶ࡫ࡥ࡬࡫ࡓࡴ࡮ࠪሣ"),
  bstack11ll1l_opy_ (u"ࠪࡷ࡭ࡵࡵ࡭ࡦࡘࡷࡪ࡙ࡩ࡯ࡩ࡯ࡩࡹࡵ࡮ࡕࡧࡶࡸࡒࡧ࡮ࡢࡩࡨࡶࠬሤ"),
  bstack11ll1l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡌ࡛ࡉࡖࠧሥ"),
  bstack11ll1l_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡴࡻࡣࡩࡋࡧࡉࡳࡸ࡯࡭࡮ࠪሦ"),
  bstack11ll1l_opy_ (u"࠭ࡩࡨࡰࡲࡶࡪࡎࡩࡥࡦࡨࡲࡆࡶࡩࡑࡱ࡯࡭ࡨࡿࡅࡳࡴࡲࡶࠬሧ"),
  bstack11ll1l_opy_ (u"ࠧ࡮ࡱࡦ࡯ࡑࡵࡣࡢࡶ࡬ࡳࡳࡇࡰࡱࠩረ"),
  bstack11ll1l_opy_ (u"ࠨ࡮ࡲ࡫ࡨࡧࡴࡇࡱࡵࡱࡦࡺࠧሩ"), bstack11ll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈ࡬ࡰࡹ࡫ࡲࡔࡲࡨࡧࡸ࠭ሪ"),
  bstack11ll1l_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡆࡨࡰࡦࡿࡁࡥࡤࠪራ"),
  bstack11ll1l_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡎࡪࡌࡰࡥࡤࡸࡴࡸࡁࡶࡶࡲࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠧሬ")
]
bstack1lllll1ll1_opy_ = bstack11ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡡࡱ࡫࠰ࡧࡱࡵࡵࡥ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡺࡶ࡬ࡰࡣࡧࠫር")
bstack1l1111lll_opy_ = [bstack11ll1l_opy_ (u"࠭࠮ࡢࡲ࡮ࠫሮ"), bstack11ll1l_opy_ (u"ࠧ࠯ࡣࡤࡦࠬሯ"), bstack11ll1l_opy_ (u"ࠨ࠰࡬ࡴࡦ࠭ሰ")]
bstack1l1l1l1lll_opy_ = [bstack11ll1l_opy_ (u"ࠩ࡬ࡨࠬሱ"), bstack11ll1l_opy_ (u"ࠪࡴࡦࡺࡨࠨሲ"), bstack11ll1l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧሳ"), bstack11ll1l_opy_ (u"ࠬࡹࡨࡢࡴࡨࡥࡧࡲࡥࡠ࡫ࡧࠫሴ")]
bstack11lll11ll1_opy_ = {
  bstack11ll1l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ስ"): bstack11ll1l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬሶ"),
  bstack11ll1l_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩሷ"): bstack11ll1l_opy_ (u"ࠩࡰࡳࡿࡀࡦࡪࡴࡨࡪࡴࡾࡏࡱࡶ࡬ࡳࡳࡹࠧሸ"),
  bstack11ll1l_opy_ (u"ࠪࡩࡩ࡭ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨሹ"): bstack11ll1l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬሺ"),
  bstack11ll1l_opy_ (u"ࠬ࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨሻ"): bstack11ll1l_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬሼ"),
  bstack11ll1l_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡏࡱࡶ࡬ࡳࡳࡹࠧሽ"): bstack11ll1l_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩ࠯ࡱࡳࡸ࡮ࡵ࡮ࡴࠩሾ")
}
bstack11lllll11l_opy_ = [
  bstack11ll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧሿ"),
  bstack11ll1l_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨቀ"),
  bstack11ll1l_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬቁ"),
  bstack11ll1l_opy_ (u"ࠬࡹࡥ࠻࡫ࡨࡓࡵࡺࡩࡰࡰࡶࠫቂ"),
  bstack11ll1l_opy_ (u"࠭ࡳࡢࡨࡤࡶ࡮࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧቃ"),
]
bstack1l1l1lll1_opy_ = bstack1ll1l1ll1l_opy_ + bstack111ll11111_opy_ + bstack111lll1ll_opy_
bstack1l11l11111_opy_ = [
  bstack11ll1l_opy_ (u"ࠧ࡟࡮ࡲࡧࡦࡲࡨࡰࡵࡷࠨࠬቄ"),
  bstack11ll1l_opy_ (u"ࠨࡠࡥࡷ࠲ࡲ࡯ࡤࡣ࡯࠲ࡨࡵ࡭ࠥࠩቅ"),
  bstack11ll1l_opy_ (u"ࠩࡡ࠵࠷࠽࠮ࠨቆ"),
  bstack11ll1l_opy_ (u"ࠪࡢ࠶࠶࠮ࠨቇ"),
  bstack11ll1l_opy_ (u"ࠫࡣ࠷࠷࠳࠰࠴࡟࠻࠳࠹࡞࠰ࠪቈ"),
  bstack11ll1l_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠶ࡠ࠶࠭࠺࡟࠱ࠫ቉"),
  bstack11ll1l_opy_ (u"࠭࡞࠲࠹࠵࠲࠸ࡡ࠰࠮࠳ࡠ࠲ࠬቊ"),
  bstack11ll1l_opy_ (u"ࠧ࡟࠳࠼࠶࠳࠷࠶࠹࠰ࠪቋ")
]
bstack111l1ll1l1_opy_ = bstack11ll1l_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩቌ")
bstack111l1l111_opy_ = bstack11ll1l_opy_ (u"ࠩࡶࡨࡰ࠵ࡶ࠲࠱ࡨࡺࡪࡴࡴࠨቍ")
bstack1l11l1ll11_opy_ = [ bstack11ll1l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ቎") ]
bstack11ll111l1_opy_ = [ bstack11ll1l_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ቏") ]
bstack1ll1lll11l_opy_ = [ bstack11ll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬቐ") ]
bstack1llllll1ll_opy_ = bstack11ll1l_opy_ (u"࠭ࡓࡅࡍࡖࡩࡹࡻࡰࠨቑ")
bstack1lll1l111l_opy_ = bstack11ll1l_opy_ (u"ࠧࡔࡆࡎࡘࡪࡹࡴࡂࡶࡷࡩࡲࡶࡴࡦࡦࠪቒ")
bstack1l1l11llll_opy_ = bstack11ll1l_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠬቓ")
bstack1l1lll11l1_opy_ = bstack11ll1l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࠨቔ")
bstack1111111l_opy_ = [
  bstack11ll1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡇࡃࡌࡐࡊࡊࠧቕ"),
  bstack11ll1l_opy_ (u"ࠫࡊࡘࡒࡠࡖࡌࡑࡊࡊ࡟ࡐࡗࡗࠫቖ"),
  bstack11ll1l_opy_ (u"ࠬࡋࡒࡓࡡࡅࡐࡔࡉࡋࡆࡆࡢࡆ࡞ࡥࡃࡍࡋࡈࡒ࡙࠭቗"),
  bstack11ll1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡊ࡚ࡗࡐࡔࡎࡣࡈࡎࡁࡏࡉࡈࡈࠬቘ"),
  bstack11ll1l_opy_ (u"ࠧࡆࡔࡕࡣࡘࡕࡃࡌࡇࡗࡣࡓࡕࡔࡠࡅࡒࡒࡓࡋࡃࡕࡇࡇࠫ቙"),
  bstack11ll1l_opy_ (u"ࠨࡇࡕࡖࡤࡉࡏࡏࡐࡈࡇ࡙ࡏࡏࡏࡡࡆࡐࡔ࡙ࡅࡅࠩቚ"),
  bstack11ll1l_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡖࡊ࡙ࡅࡕࠩቛ"),
  bstack11ll1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡆࡖࡕࡈࡈࠬቜ"),
  bstack11ll1l_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡇࡂࡐࡔࡗࡉࡉ࠭ቝ"),
  bstack11ll1l_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭቞"),
  bstack11ll1l_opy_ (u"࠭ࡅࡓࡔࡢࡒࡆࡓࡅࡠࡐࡒࡘࡤࡘࡅࡔࡑࡏ࡚ࡊࡊࠧ቟"),
  bstack11ll1l_opy_ (u"ࠧࡆࡔࡕࡣࡆࡊࡄࡓࡇࡖࡗࡤࡏࡎࡗࡃࡏࡍࡉ࠭በ"),
  bstack11ll1l_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡕࡏࡔࡈࡅࡈࡎࡁࡃࡎࡈࠫቡ"),
  bstack11ll1l_opy_ (u"ࠩࡈࡖࡗࡥࡔࡖࡐࡑࡉࡑࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡊࡆࡏࡌࡆࡆࠪቢ"),
  bstack11ll1l_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣ࡙ࡏࡍࡆࡆࡢࡓ࡚࡚ࠧባ"),
  bstack11ll1l_opy_ (u"ࠫࡊࡘࡒࡠࡕࡒࡇࡐ࡙࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫቤ"),
  bstack11ll1l_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡎࡏࡔࡖࡢ࡙ࡓࡘࡅࡂࡅࡋࡅࡇࡒࡅࠨብ"),
  bstack11ll1l_opy_ (u"࠭ࡅࡓࡔࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡆࡂࡋࡏࡉࡉ࠭ቦ"),
  bstack11ll1l_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨቧ"),
  bstack11ll1l_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡖࡊ࡙ࡏࡍࡗࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧቨ"),
  bstack11ll1l_opy_ (u"ࠩࡈࡖࡗࡥࡍࡂࡐࡇࡅ࡙ࡕࡒ࡚ࡡࡓࡖࡔ࡞࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨቩ"),
]
bstack111l1lll1_opy_ = bstack11ll1l_opy_ (u"ࠪ࠲࠴ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡦࡸࡴࡪࡨࡤࡧࡹࡹ࠯ࠨቪ")
bstack11llllll1l_opy_ = os.path.join(os.path.expanduser(bstack11ll1l_opy_ (u"ࠫࢃ࠭ቫ")), bstack11ll1l_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬቬ"), bstack11ll1l_opy_ (u"࠭࠮ࡣࡵࡷࡥࡨࡱ࠭ࡤࡱࡱࡪ࡮࡭࠮࡫ࡵࡲࡲࠬቭ"))
bstack11l11l111l_opy_ = bstack11ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡦࡶࡩࠨቮ")
bstack111l1lll11_opy_ = [ bstack11ll1l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨቯ"), bstack11ll1l_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨተ"), bstack11ll1l_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩቱ"), bstack11ll1l_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫቲ")]
bstack1l111llll1_opy_ = [ bstack11ll1l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬታ"), bstack11ll1l_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬቴ"), bstack11ll1l_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ት"), bstack11ll1l_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨቶ") ]
bstack1l1l11ll_opy_ = {
  bstack11ll1l_opy_ (u"ࠩࡓࡅࡘ࡙ࠧቷ"): bstack11ll1l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪቸ"),
  bstack11ll1l_opy_ (u"ࠫࡋࡇࡉࡍࠩቹ"): bstack11ll1l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬቺ"),
  bstack11ll1l_opy_ (u"࠭ࡓࡌࡋࡓࠫቻ"): bstack11ll1l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨቼ")
}
bstack11111llll_opy_ = [
  bstack11ll1l_opy_ (u"ࠣࡩࡨࡸࠧች"),
  bstack11ll1l_opy_ (u"ࠤࡪࡳࡇࡧࡣ࡬ࠤቾ"),
  bstack11ll1l_opy_ (u"ࠥ࡫ࡴࡌ࡯ࡳࡹࡤࡶࡩࠨቿ"),
  bstack11ll1l_opy_ (u"ࠦࡷ࡫ࡦࡳࡧࡶ࡬ࠧኀ"),
  bstack11ll1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦኁ"),
  bstack11ll1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥኂ"),
  bstack11ll1l_opy_ (u"ࠢࡴࡷࡥࡱ࡮ࡺࡅ࡭ࡧࡰࡩࡳࡺࠢኃ"),
  bstack11ll1l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧኄ"),
  bstack11ll1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧኅ"),
  bstack11ll1l_opy_ (u"ࠥࡧࡱ࡫ࡡࡳࡇ࡯ࡩࡲ࡫࡮ࡵࠤኆ"),
  bstack11ll1l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࡷࠧኇ"),
  bstack11ll1l_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪ࡙ࡣࡳ࡫ࡳࡸࠧኈ"),
  bstack11ll1l_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡁࡴࡻࡱࡧࡘࡩࡲࡪࡲࡷࠦ኉"),
  bstack11ll1l_opy_ (u"ࠢࡤ࡮ࡲࡷࡪࠨኊ"),
  bstack11ll1l_opy_ (u"ࠣࡳࡸ࡭ࡹࠨኋ"),
  bstack11ll1l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡗࡳࡺࡩࡨࡂࡥࡷ࡭ࡴࡴࠢኌ"),
  bstack11ll1l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡑࡺࡲࡴࡪࡖࡲࡹࡨ࡮ࠢኍ"),
  bstack11ll1l_opy_ (u"ࠦࡸ࡮ࡡ࡬ࡧࠥ኎"),
  bstack11ll1l_opy_ (u"ࠧࡩ࡬ࡰࡵࡨࡅࡵࡶࠢ኏")
]
bstack111l1ll1ll_opy_ = [
  bstack11ll1l_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࠧነ"),
  bstack11ll1l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦኑ"),
  bstack11ll1l_opy_ (u"ࠣࡣࡸࡸࡴࠨኒ"),
  bstack11ll1l_opy_ (u"ࠤࡰࡥࡳࡻࡡ࡭ࠤና"),
  bstack11ll1l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧኔ")
]
bstack11111111_opy_ = {
  bstack11ll1l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥን"): [bstack11ll1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦኖ")],
  bstack11ll1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥኗ"): [bstack11ll1l_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦኘ")],
  bstack11ll1l_opy_ (u"ࠣࡣࡸࡸࡴࠨኙ"): [bstack11ll1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨኚ"), bstack11ll1l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨኛ"), bstack11ll1l_opy_ (u"ࠦࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣኜ"), bstack11ll1l_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࡉࡱ࡫࡭ࡦࡰࡷࠦኝ")],
  bstack11ll1l_opy_ (u"ࠨ࡭ࡢࡰࡸࡥࡱࠨኞ"): [bstack11ll1l_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢኟ")],
  bstack11ll1l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥአ"): [bstack11ll1l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦኡ")],
}
bstack111l1lll1l_opy_ = {
  bstack11ll1l_opy_ (u"ࠥࡧࡱ࡯ࡣ࡬ࡇ࡯ࡩࡲ࡫࡮ࡵࠤኢ"): bstack11ll1l_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࠥኣ"),
  bstack11ll1l_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤኤ"): bstack11ll1l_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥእ"),
  bstack11ll1l_opy_ (u"ࠢࡴࡧࡱࡨࡐ࡫ࡹࡴࡖࡲࡉࡱ࡫࡭ࡦࡰࡷࠦኦ"): bstack11ll1l_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࠥኧ"),
  bstack11ll1l_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡇࡣࡵ࡫ࡹࡩࡊࡲࡥ࡮ࡧࡱࡸࠧከ"): bstack11ll1l_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷࠧኩ"),
  bstack11ll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨኪ"): bstack11ll1l_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢካ")
}
bstack1l1ll1ll_opy_ = {
  bstack11ll1l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡁࡍࡎࠪኬ"): bstack11ll1l_opy_ (u"ࠧࡔࡷ࡬ࡸࡪࠦࡓࡦࡶࡸࡴࠬክ"),
  bstack11ll1l_opy_ (u"ࠨࡃࡉࡘࡊࡘ࡟ࡂࡎࡏࠫኮ"): bstack11ll1l_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࠡࡖࡨࡥࡷࡪ࡯ࡸࡰࠪኯ"),
  bstack11ll1l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡉࡆࡉࡈࠨኰ"): bstack11ll1l_opy_ (u"࡙ࠫ࡫ࡳࡵࠢࡖࡩࡹࡻࡰࠨ኱"),
  bstack11ll1l_opy_ (u"ࠬࡇࡆࡕࡇࡕࡣࡊࡇࡃࡉࠩኲ"): bstack11ll1l_opy_ (u"࠭ࡔࡦࡵࡷࠤ࡙࡫ࡡࡳࡦࡲࡻࡳ࠭ኳ")
}
bstack111l1l1lll_opy_ = 65536
bstack111l1l1l1l_opy_ = bstack11ll1l_opy_ (u"ࠧ࠯࠰࠱࡟࡙ࡘࡕࡏࡅࡄࡘࡊࡊ࡝ࠨኴ")
bstack111ll111ll_opy_ = [
      bstack11ll1l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪኵ"), bstack11ll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬ኶"), bstack11ll1l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭኷"), bstack11ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨኸ"), bstack11ll1l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠧኹ"),
      bstack11ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡚ࡹࡥࡳࠩኺ"), bstack11ll1l_opy_ (u"ࠧࡱࡴࡲࡼࡾࡖࡡࡴࡵࠪኻ"), bstack11ll1l_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩኼ"), bstack11ll1l_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾࡖࡡࡴࡵࠪኽ"),
      bstack11ll1l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫኾ"), bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭኿"), bstack11ll1l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨዀ")
    ]
bstack111ll1111l_opy_= {
  bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ዁"): bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫዂ"),
  bstack11ll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬዃ"): bstack11ll1l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ዄ"),
  bstack11ll1l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩዅ"): bstack11ll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨ዆"),
  bstack11ll1l_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬ዇"): bstack11ll1l_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ወ"),
  bstack11ll1l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪዉ"): bstack11ll1l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫዊ"),
  bstack11ll1l_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫዋ"): bstack11ll1l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬዌ"),
  bstack11ll1l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧው"): bstack11ll1l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨዎ"),
  bstack11ll1l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪዏ"): bstack11ll1l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫዐ"),
  bstack11ll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫዑ"): bstack11ll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬዒ"),
  bstack11ll1l_opy_ (u"ࠪࡸࡪࡹࡴࡄࡱࡱࡸࡪࡾࡴࡐࡲࡷ࡭ࡴࡴࡳࠨዓ"): bstack11ll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩዔ"),
  bstack11ll1l_opy_ (u"ࠬࡺࡥࡴࡶࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩዕ"): bstack11ll1l_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪዖ"),
  bstack11ll1l_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ዗"): bstack11ll1l_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬዘ"),
  bstack11ll1l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠫዙ"): bstack11ll1l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬዚ"),
  bstack11ll1l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨዛ"): bstack11ll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧዜ"),
  bstack11ll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨዝ"): bstack11ll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩዞ"),
  bstack11ll1l_opy_ (u"ࠨࡴࡨࡶࡺࡴࡔࡦࡵࡷࡷࠬዟ"): bstack11ll1l_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ዠ"),
  bstack11ll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩዡ"): bstack11ll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪዢ"),
  bstack11ll1l_opy_ (u"ࠬࡶࡥࡳࡥࡼࡓࡵࡺࡩࡰࡰࡶࠫዣ"): bstack11ll1l_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬዤ"),
  bstack11ll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾࡉࡡࡱࡶࡸࡶࡪࡓ࡯ࡥࡧࠪዥ"): bstack11ll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫዦ"),
  bstack11ll1l_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫዧ"): bstack11ll1l_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬየ"),
  bstack11ll1l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫዩ"): bstack11ll1l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬዪ"),
  bstack11ll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ያ"): bstack11ll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧዬ"),
  bstack11ll1l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬይ"): bstack11ll1l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ዮ"),
  bstack11ll1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧዯ"): bstack11ll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨደ"),
  bstack11ll1l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬዱ"): bstack11ll1l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ዲ")
}
bstack111l1lllll_opy_ = [bstack11ll1l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧዳ"), bstack11ll1l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧዴ")]