--[[
The positions for quest log (fates) descriptions are passed hardcoded to 
`CreateScreenComponent` from `OpenQuestLogScreen` in `QuestLogScreen.lua`.

We hook onto `CreateScreenComponent` and single them out to reposition.
]]

local __CreateScreenComponent = CreateScreenComponent
function CreateScreenComponent(params)
	Hephaistos.CreateScreenComponentPreHook(params)
	return __CreateScreenComponent(params)
end

function Hephaistos.CreateScreenComponentPreHook(params)
  -- force replace hardcoded QuestLogScreen DescriptionBox X/Y values
	if params.Name == "BlankObstacle" and params.Group == "Combat_Menu" and params.X == 795 and params.Y == 300 then
		params.X = Hephaistos.RecomputeFixedXFromCenter(params.X)
		params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y + 10)
	end
end
