--[[
Hades displays several vignettes/overlays to darken the main part of the screen:
- A vignette is displayed at all times in-game.
- Contextual overlays are drawn on top, e.g. for dialogues or shopping.

These effects are mainly registered via the `CreateScreenObstacle` function from
`UIScripts.lua`, which itself calls the native `SpawnObstacle` function to draw
resources on screen. The resources come from SJSON-loaded graphics, e.g.
`BlankObstacle` is defined in `1_DevObstacles.sjson` and loads graphic `Blank`
defined in `1_DevAnimations.sjson` and referencing file `Dev\blank_invisible`
from the game packages.

Hephaistos currently does not edit any packaged resources. Since resources are
of fixed size, we simply scale out the overlays as far as needed to cover the
whole screen, considering the loss of details in the edges of the screen in case
of non-16:9 ratio to be acceptable for simple darkening overlays.

To centralize code as much as possible, we hook onto `CreateScreenObstacle` and
filter out specific overlays to be scaled whenever possible, rather than
manually edit other functions.

Note: this approach will not work for objects bypassing `CreateScreenObstacle`
and manually using `SpawnObstacle`, should any need to be scaled.

Some overlays are additionnally rescaled via the `SetScale` native function.
For these, we assume when a `fraction` of 4 or more is passed to `SetScale`, we
are dealing with a screen-wide effect and should scale it.
]]

local __CreateScreenObstacle = CreateScreenObstacle
function CreateScreenObstacle(params)
	Hephaistos.CreateScreenObstaclePreHook(params)
	return __CreateScreenObstacle(params)
end

function Hephaistos.CreateScreenObstaclePreHook(params)
	if
		(params.Name == "BlankObstacle" and (
			params.Group == "Combat_UI_World" or -- low health overlay from `UIScripts.lua`
			params.Group == "Events" or -- alert overlay from `RoomPresentation.lua` and `EventPresentation.lua`
			params.Group == "Overlay" or -- transition overlays from `RoomPresentation.lua`
			params.Group == "Scripting" or -- alert overlay + poison/bloodstone vignettes from `RoomPresentation.lua` and `CombatPresentation.lua`
			params.Group == "Vignette" -- in-game vignette from `RoomManager.lua`
		)) or
		(params.Name == "DialogueBackground") or -- dialogue background from `EventPresentation.lua`
		(params.Name == "rectangle01" and (
			Group == "Combat_Menu" or -- shop background from `AwardMenuScripts.lua`, `MarketScreen.lua`, `MusicPlayerScreen.lua`, `QuestLogScreen.lua`, `SeedControlScreen.lua`, `GhostAdminScreen.lua`, `SellTraitScript.lua`, `UpgradeChoice.lua`, `WeaponUpgradeScripts.lua`, and `MetaUpgrades.lua`
			Group == "Combat_Menu_TraitTray_Backing" or -- shop background from `BoonInfoScreenScripts.lua`
			Group == "Combat_UI" or -- death background from `RoomPresentation.lua`
			Group == "Combat_UI_Backing" or -- advanced tooltip background from `TraitTrayScripts.lua` + game stats background from `GameStatsScreen.lua` + blackout from `RunClearScreen.lua` and `RunHistoryScreen.lua`
			Group == "Combat_UI_World" -- shop background from `StoreScripts.lua`
		))
	then
		if params.Scale == nil then
			params.Scale = Hephaistos.ScaleFactor
		else
			params.Scale = params.Scale * Hephaistos.ScaleFactor
		end
	end
end


local __SetScale = SetScale
function SetScale(params)
	Hephaistos.SetScalePreHook(params)
	__SetScale(params)
end

function Hephaistos.SetScalePreHook(params)
	-- assume a fraction of 4 or more means it's a screen-wide effect
	if params.Fraction >= 4 then
		params.Fraction = params.Fraction * Hephaistos.ScaleFactor
	end
end
