--[[
Hades registers Lua state values on game start both by pulling data from the
save file, where part of the Lua state is stored via `luabins`, and from the Lua
scripts themselves.

One issue is that screen values and derived computations only incidentally work:
- Static screen values are initialized in `UIData.lua` when the Lua scripts are
	loaded, and are immediately used for computing dependent Lua state values.
- When loading a save file, screen values are loaded from the save file and
	override the static screen values coming from `UIData.lua`.
- Since dynamic computations (e.g. in functions) pull the current values while
	previously the computed dependent Lua state values did not change, they will
	be out of sync if only one is edited and not the other.

For example:
- `UIData.UsePrompt.X` is statically derived off `ScreenCenterX` in `UIData.lua`
	at game	start.
- `ScreenAnchors.Vignette` is dynamically derived off `ScreenCenterX` in
	`RoomManager.lua` when `CreateVignette` is called.
- If we only statically edit `ScreenCenterX` in `UIData.lua`, it will only have
	an effect on `UIData.UsePrompt.X` because the actual `ScreenCenterX` value
	will be overriden from the save file and used when computing
	`ScreenAnchors.Vignette`.
- If only we override `ScreenCenterX` after it has been loaded from the save
	file, it will only have an effect on `ScreenAnchors.Vignette` because the
	original `ScreenCenterX` value was used at the time `UIData.UsePrompt.X` was
	computed.

Thus, both must be modified by Hephaistos.

On top of that, some of the statically defined UI positioning is hardcoded and
does not depend on screen values, e.g. `GunUI.StartX = 630` in `UIData.lua`.
Simply editing both the static screen values in `UIData.lua` and the save file
screen values is insufficient, and we must also reposition hardcoded UI elements
on a case-by-case basis.

We hook onto `Load` from `Main.lua` and immediately override screen values
loaded from the save file, then recompute all dependent computed values as well
as manually reposition hardcoded UI elements. 
]]

local __Load = Load
function Load(data)
	__Load(data)
	Hephaistos.LoadPostHook()
end

function Hephaistos.LoadPostHook()
	-- Override Lua state values loaded from save file
	ScreenCenterX = Hephaistos.ScreenCenterX
	ScreenCenterY = Hephaistos.ScreenCenterY
	ScreenWidth = Hephaistos.ScreenWidth
	ScreenHeight = Hephaistos.ScreenHeight

	-- Recompute dependent and hardcoded Lua state values loaded on game start
	Import "../Mods/Hephaistos/FixLuaState/ConditionalItemData.lua"
	Import "../Mods/Hephaistos/FixLuaState/CreditsData.lua"
	Import "../Mods/Hephaistos/FixLuaState/QuestData.lua"
	Import "../Mods/Hephaistos/FixLuaState/RoomPresentation.lua"
	Import "../Mods/Hephaistos/FixLuaState/RunClearMessageData.lua"
	-- Import "../Mods/Hephaistos/FixLuaState/SeedControlScreen.lua"
	Import "../Mods/Hephaistos/FixLuaState/UIData.lua"
end
