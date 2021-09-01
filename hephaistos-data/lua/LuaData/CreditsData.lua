--[[
The credits are intended for being displayed on the left of the screen, but
while some of the X values are computed when `CreditsData` is loaded and thus
stay fixed on the left, most credit lines are missing an `X` position and get
automatically assigned to `ScreenCenterX - 530` from `CreditsScripts.lua`, which
is incorrect if `ScreenCenterX` has changed. We reposition these based on the
original screen center as intended.

Also, some lines have additional `Y` spacing provided via `CreditScrollStart`.
Likewise, it is computed when `CreditsData` is loaded and thus needs to
recomputed as it depends on `ScreenHeight`.
]]

local offsetX = Hephaistos.Original.ScreenCenterX - 530
local originalCreditScrollStart = CreditSpacing.CreditScrollStart
CreditSpacing.CreditScrollStart = Hephaistos.RecomputeFixedYFromBottom(CreditSpacing.CreditScrollStart)

local function reposition(args)
  -- manually position X if not provided
  if not args.X then
    args.X = offsetX
  end

  -- reposition CreditLineBuffer if it was dependent on CreditScrollStart
  if args.CreditLineBuffer and args.CreditLineBuffer == originalCreditScrollStart then
    args.CreditLineBuffer = CreditSpacing.CreditScrollStart
  end

  return args
end

-- iterate through CreditsData and reposition everything
local creditsData = DeepCopyTable(CreditsData)
for section, table in pairs(creditsData) do
  for i, args in ipairs(table) do
    CreditsData[section][i] = reposition(args)
  end
end
