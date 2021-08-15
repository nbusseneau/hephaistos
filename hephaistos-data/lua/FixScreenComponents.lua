--[[
The positions for various screen components hardcoded all around.

We hook onto `CreateScreenComponent` and `CreateMetaUpgradeEntry` and single
them out to reposition, filtering as precisely as possible to prevent potential
side effects.
]]

local __CreateScreenComponent = CreateScreenComponent
function CreateScreenComponent(params)
	caller = Hephaistos.GetCallerName()
	if caller then
		Hephaistos.CreateScreenComponentPreHook(params, caller)
	end
	return __CreateScreenComponent(params)
end

function Hephaistos.CreateScreenComponentPreHook(params, caller)
	if
		-- mirror shards in `MetaUpgrades.lua`
		caller == "OpenMetaUpgradeMenu" and Hephaistos.MatchParams(params,
			{ Name = "rectangle01", Group = "Combat_Menu", X = 464, Y = 415 },
			{ Name = "rectangle01", Group = "Combat_Menu", X = 1446, Y = 415 },
			{ Name = "rectangle01", Group = "Combat_Menu", X = 814, Y = 50 },
			{ Name = "rectangle01", Group = "Combat_Menu", X = 1096, Y = 50 })
	or
		-- patch of punishment meter bar in `MetaUpgrades.lua`.
		caller == "OpenShrineUpgradeMenu" and Hephaistos.MatchParams(params,
			{ Name = "ShrineMeterBarFill", Group = "Combat_Menu", X = 550, Y = ScreenCenterY - 90 })
	or
		-- patch of punishment weapon image in `MetaUpgrades.lua`.
		caller == "OpenShrineUpgradeMenu" and Hephaistos.MatchParams(params,
			{ Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 250, Y = 470 })
	or
		-- run history meta upgrades (pacts + mirror)` in `RunHistoryScreen.lua`.
		caller == "ShowRunHistory" and Hephaistos.MatchParams(params,
			{ Name = "BlankObstacle", Group = "Combat_Menu_TraitTray_Backing" },
			{ Name = "TraitTrayMetaUpgradeIconButton", Group = "Combat_Menu_TraitTray" }) and
			params.X >= 320 and params.Y >= 900
	or
		-- quest log (fates) descriptions in `QuestLogScreen.lua`.
		caller == "OpenQuestLogScreen" and Hephaistos.MatchParams(params,
			{ Name = "BlankObstacle", Group = "Combat_Menu", X = 795, Y = 300 })
	then
		params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
		params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y + 10)
	end
end


local __CreateMetaUpgradeEntry = CreateMetaUpgradeEntry
function CreateMetaUpgradeEntry(args)
	caller = Hephaistos.GetCallerName()
	if caller then
		Hephaistos.CreateMetaUpgradeEntryPreHook(args, caller)
	end
	__CreateMetaUpgradeEntry(args)
end

function Hephaistos.CreateMetaUpgradeEntryPreHook(args, caller)
	if
		-- mirror upgrade icons in `MetaUpgrades.lua`
		caller == "OpenMetaUpgradeMenu" and args.Screen.IconX == 663
	or
		-- pact of punishment icons in `MetaUpgrades.lua`
		caller == "OpenShrineUpgradeMenu" and args.Screen.IconX == 970 - 68
	then
		args.Screen.IconX = Hephaistos.RecomputeFixedXFromCenter(args.Screen.IconX)
	end
end
