--[[
The positions for various GUI components or effects are hardcoded all around.
When possible, we first try to reposition elements from SJSON resource files as
doing so is more efficient and more compatible when also using other mods,
however some elements can only be reposition dynamically from Lua code.

For these, we hook onto various functions such as `CreateScreenComponent` or
`CreateMetaUpgradeEntry` and single them out to handle on a case-by-case
basis, filtering as precisely as possible (based on caller function and passed
arguments) to prevent side effects on similar items, and then repositioning
or resizing as desired.

Since actions to take on arguments are always the same for a specific function,
they are registered here. Filters are registered in separate files and always
take the form:

	Hephaistos.OverridenFunction[CallerFunction] = FilterCondition

with the filename being the one where CallerFunction is defined.

For example, `WeaponUpgradeScripts.lua` originally defines `ShowWeaponUpgradeScreen`,
which itself calls `CreateScreenComponent` with hardcoded X/Y values to position
the weapon image when opening the weapon aspects menu screen (where we can spend
Titan Blood for upgrades):

	components.WeaponImage = CreateScreenComponent({ Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 335, Y = 435 })

To reposition the weapon image, we register a filter with a filter condition
specifically matching the weapon image `CreateScreenComponent` arguments from
`ShowWeaponUpgradeScreen`:

	Hephaistos.CreateScreenComponent[ShowWeaponUpgradeScreen] = function(params)
		return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 335, Y = 435 })
	end

And then we register a filter hook on `CreateScreenComponent`:

	Hephaistos.CreateScreenComponent = {}
	Hephaistos.RegisterFilterHook("CreateScreenComponent", actionCallback)

This will call `actionCallback` with `CreateScreenComponent` arguments, but only
if `CreateScreenComponent` is called from `ShowWeaponUpgradeScreen` with these
specific arguments.
]]

local function recenter(args)
	args.X = args.X and Hephaistos.RecomputeFixedXFromCenter(args.X) or nil
	args.Y = args.Y and Hephaistos.RecomputeFixedYFromCenter(args.Y) or nil
end

local function recenterOffsets(args)
	args.OffsetX = args.OffsetX and Hephaistos.RecomputeFixedXFromCenter(args.OffsetX) or nil
	args.OffsetY = args.OffsetY and Hephaistos.RecomputeFixedYFromCenter(args.OffsetY) or nil
end

local function rescale(args)
	local originalFraction = args.Fraction
	args.Fraction = originalFraction and originalFraction * Hephaistos.ScaleFactorX or Hephaistos.ScaleFactorX
	SetScaleX(args)
	args.Fraction = originalFraction and originalFraction * Hephaistos.ScaleFactorY or Hephaistos.ScaleFactorY
	SetScaleY(args)
end

Hephaistos.Attach = {}
Hephaistos.RegisterFilterHook("Attach", recenterOffsets)

Hephaistos.CreateKeepsakeIcon = {}
Hephaistos.RegisterFilterHook("CreateKeepsakeIcon", function(components, args)
	recenter(args)
end)

Hephaistos.CreateMetaUpgradeEntry = {}
Hephaistos.RegisterFilterHook("CreateMetaUpgradeEntry", function(args)
	args.Screen.IconX = Hephaistos.RecomputeFixedXFromCenter(args.Screen.IconX)
end)

Hephaistos.CreateScreenComponent = {}
Hephaistos.RegisterFilterHook("CreateScreenComponent", recenter)

Hephaistos.SetScale = {}
Hephaistos.RegisterFilterHook("SetScale", rescale, true)

Hephaistos.Teleport = {}
Hephaistos.RegisterFilterHook("Teleport", recenterOffsets)

Import "../Mods/Hephaistos/GUIComponents/AwardMenuScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/BoonInfoScreenScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/CodexScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/CombatPresentation.lua"
Import "../Mods/Hephaistos/GUIComponents/GameStatsScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/GhostAdminScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/MarketScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/MetaUpgrades.lua"
Import "../Mods/Hephaistos/GUIComponents/MusicPlayerScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/QuestLogScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/RoomPresentation.lua"
Import "../Mods/Hephaistos/GUIComponents/RunClearScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/RunHistoryScreen.lua"
Import "../Mods/Hephaistos/GUIComponents/SellTraitScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/StoreScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/TraitTrayScripts.lua"
Import "../Mods/Hephaistos/GUIComponents/UIPresentation.lua"
Import "../Mods/Hephaistos/GUIComponents/UpgradeChoice.lua"
Import "../Mods/Hephaistos/GUIComponents/WeaponUpgradeScripts.lua"
