--[[
The positions for various GUI components or effects are hardcoded all around.

We hook onto various functions such as `CreateScreenComponent` or
`CreateMetaUpgradeEntry` and single them out to handle on a case-by-case
basis, filtering as precisely as possible (based on caller function and passed
arguments) to prevent side effects on similar items, and then repositioning
or resizing as desired.

Since actions to take on arguments are the always the same for a specific
function, they are registered here. Filters are registered in separate files
and always take the form:

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
	args.Scale = args.Scale and args.Scale * Hephaistos.ScaleFactor or Hephaistos.ScaleFactor
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

Hephaistos.Teleport = {}
Hephaistos.RegisterFilterHook("Teleport", recenterOffsets)

Import "../Mods/Hephaistos/Filters/AwardMenuScripts.lua"
Import "../Mods/Hephaistos/Filters/BoonInfoScreenScripts.lua"
Import "../Mods/Hephaistos/Filters/CodexScripts.lua"
Import "../Mods/Hephaistos/Filters/CombatPresentation.lua"
Import "../Mods/Hephaistos/Filters/GhostAdminScreen.lua"
Import "../Mods/Hephaistos/Filters/MetaUpgrades.lua"
Import "../Mods/Hephaistos/Filters/QuestLogScreen.lua"
Import "../Mods/Hephaistos/Filters/RoomPresentation.lua"
Import "../Mods/Hephaistos/Filters/RunHistoryScreen.lua"
Import "../Mods/Hephaistos/Filters/UpgradeChoice.lua"
Import "../Mods/Hephaistos/Filters/WeaponUpgradeScripts.lua"
