--[[
The positions for various screen components are hardcoded all around.

We hook onto various methods such as `CreateScreenComponent` or
`CreateMetaUpgradeEntry` and single them out to reposition components, filtering
as precisely as possible (based on caller name and passed arguments) to prevent
potential side effects.
]]

Hephaistos.CreateScreenComponent = {}
Hephaistos.CreateMetaUpgradeEntry = {}
Hephaistos.CreateKeepsakeIcon = {}

local __CreateScreenComponent = CreateScreenComponent
function CreateScreenComponent(params)
	Hephaistos.Filter(Hephaistos.CreateScreenComponent, params, function(params)
		params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
		params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y)
	end)
	return __CreateScreenComponent(params)
end

local __CreateMetaUpgradeEntry = CreateMetaUpgradeEntry
function CreateMetaUpgradeEntry(args)
	Hephaistos.Filter(Hephaistos.CreateMetaUpgradeEntry, args, function(args)
		args.Screen.IconX = Hephaistos.RecomputeFixedXFromCenter(args.Screen.IconX)
	end)
	__CreateMetaUpgradeEntry(args)
end

local __CreateKeepsakeIcon = CreateKeepsakeIcon
function CreateKeepsakeIcon(components, args)
	Hephaistos.Filter(Hephaistos.CreateKeepsakeIcon, args, function(args)
		args.X = Hephaistos.RecomputeFixedXFromCenter(args.X)
		args.Y = Hephaistos.RecomputeFixedYFromCenter(args.Y)
	end)
	__CreateKeepsakeIcon(components, args)
end

Import "../Mods/Hephaistos/Filters/AwardMenuScripts.lua"
Import "../Mods/Hephaistos/Filters/MetaUpgrades.lua"
Import "../Mods/Hephaistos/Filters/QuestLogScreen.lua"
Import "../Mods/Hephaistos/Filters/RunHistoryScreen.lua"
Import "../Mods/Hephaistos/Filters/WeaponUpgradeScripts.lua"
