--[[
The positions for various screen components hardcoded all around:

- Run history meta upgrades (pacts) from `ShowRunHistory` in `RunHistoryScreen.lua`.
- Quest log (fates) descriptions from `OpenQuestLogScreen` in `QuestLogScreen.lua`.

We hook onto `CreateScreenComponent` and single them out to reposition.
]]

local __CreateScreenComponent = CreateScreenComponent
function CreateScreenComponent(params)
	Hephaistos.CreateScreenComponentPreHook(params)
	return __CreateScreenComponent(params)
end

function Hephaistos.CreateScreenComponentPreHook(params)
	-- hardcoded RunHistoryScreen MetaUpgrades X/Y values
	if ((params.Name == "BlankObstacle" and params.Group == "Combat_Menu_TraitTray_Backing") or
		(params.Name == "TraitTrayMetaUpgradeIconButton" and params.Group == "Combat_Menu_TraitTray")) and
		params.X >= 320 and params.Y >= 900
	then
		params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
		params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y)
	-- hardcoded QuestLogScreen DescriptionBox X/Y values
  elseif (params.Name == "BlankObstacle") and params.Group == "Combat_Menu" and params.X == 795 and params.Y == 300 then
		params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
		params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y + 10)
	end
end
