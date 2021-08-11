--[[
Hades displays several vignettes/overlays to darken the main part of the screen:
- A vignette is displayed at all times in-game.
- Contextual overlays are drawn on top, e.g. for dialogues.

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
]]

local __CreateScreenObstacle = CreateScreenObstacle
function CreateScreenObstacle(params)
	Hephaistos.CreateScreenObstaclePreHook(params)
	return __CreateScreenObstacle(params)
end

function Hephaistos.CreateScreenObstaclePreHook(params)
	if
		-- In-game vignette
		(params.Name == "BlankObstacle" and params.Group == "Vignette") or
		-- Dialogue background
		(params.Name == "DialogueBackground")
	then
		if params.Scale == nil then
			params.Scale = Hephaistos.ScaleFactor
		else
			params.Scale = params.Scale * Hephaistos.ScaleFactor
		end
	end
end
