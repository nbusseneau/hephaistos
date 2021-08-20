--[[
The positions for various GUI components or effects are hardcoded all around.

We hook onto various methods such as `CreateScreenComponent` or
`CreateMetaUpgradeEntry` and single them out to reposition on a case-by-case
basis, filtering as precisely as possible (based on caller name and passed
arguments) to prevent side effects on similar items.
]]

Hephaistos.Attach = {}
Hephaistos.CreateAnimation = {}
Hephaistos.CreateKeepsakeIcon = {}
Hephaistos.CreateMetaUpgradeEntry = {}
Hephaistos.CreateScreenComponent = {}
Hephaistos.SetAnimation = {}

local __Attach = Attach
function Attach(params)
	Hephaistos.Filter(Hephaistos.Attach, params, function(params)
		params.OffsetX = Hephaistos.RecomputeFixedXFromCenter(params.OffsetX)
		params.OffsetY = Hephaistos.RecomputeFixedYFromCenter(params.OffsetY)
	end)
	return __Attach(params)
end

local __CreateAnimation = CreateAnimation
function CreateAnimation(params)
	Hephaistos.Filter(Hephaistos.CreateAnimation, params, function(params)
		params.Scale = params.Scale and params.Scale * Hephaistos.ScaleFactor or Hephaistos.ScaleFactor
	end)
	__CreateAnimation(params)
end

local __CreateKeepsakeIcon = CreateKeepsakeIcon
function CreateKeepsakeIcon(components, args)
	Hephaistos.Filter(Hephaistos.CreateKeepsakeIcon, args, function(args)
		args.X = Hephaistos.RecomputeFixedXFromCenter(args.X)
		args.Y = Hephaistos.RecomputeFixedYFromCenter(args.Y)
	end)
	__CreateKeepsakeIcon(components, args)
end

local __CreateMetaUpgradeEntry = CreateMetaUpgradeEntry
function CreateMetaUpgradeEntry(args)
	Hephaistos.Filter(Hephaistos.CreateMetaUpgradeEntry, args, function(args)
		args.Screen.IconX = Hephaistos.RecomputeFixedXFromCenter(args.Screen.IconX)
	end)
	__CreateMetaUpgradeEntry(args)
end

local __CreateScreenComponent = CreateScreenComponent
function CreateScreenComponent(params)
	Hephaistos.Filter(Hephaistos.CreateScreenComponent, params, function(params)
		params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
		params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y)
	end)
	return __CreateScreenComponent(params)
end

local __SetAnimation = SetAnimation
function SetAnimation(params)
	Hephaistos.Filter(Hephaistos.SetAnimation, params, function(params)
		params.Scale = params.Scale and params.Scale * Hephaistos.ScaleFactor or Hephaistos.ScaleFactor
	end)
	__SetAnimation(params)
end

Import "../Mods/Hephaistos/Filters/AwardMenuScripts.lua"
Import "../Mods/Hephaistos/Filters/BoonInfoScreenScripts.lua"
Import "../Mods/Hephaistos/Filters/CodexScripts.lua"
Import "../Mods/Hephaistos/Filters/CombatPresentation.lua"
Import "../Mods/Hephaistos/Filters/EventPresentation.lua"
Import "../Mods/Hephaistos/Filters/GhostAdminScreen.lua"
Import "../Mods/Hephaistos/Filters/MetaUpgrades.lua"
Import "../Mods/Hephaistos/Filters/QuestLogScreen.lua"
Import "../Mods/Hephaistos/Filters/RoomPresentation.lua"
Import "../Mods/Hephaistos/Filters/RunHistoryScreen.lua"
Import "../Mods/Hephaistos/Filters/UpgradeChoice.lua"
Import "../Mods/Hephaistos/Filters/WeaponUpgradeScripts.lua"
