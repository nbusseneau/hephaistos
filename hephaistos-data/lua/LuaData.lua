--[[
Hades registers Lua data tables on game start both by pulling Lua state from the
save file, where part of the Lua data is stored via `luabins`, and from the Lua
scripts themselves.

Static screen values such as `ScreenCenterX` define variables off of which many
other Lua values are derived, but there is a quirk:
- Static screen values are initialized in `UIData.lua` when the Lua scripts are
  loaded. These are immediately used for computing some of the derived Lua state
  values.
- When loading a save file, new screen values are loaded from the save file and
  override the static screen values coming from `UIData.lua`.
- Since dynamic computations (e.g. in functions) pull the current values while
  the previously computed derived Lua state values did not change, they will
  be out of sync if only one is edited and not the other.

For example:
- `UIData.UsePrompt.X` is statically derived off `ScreenCenterX` in `UIData.lua`
  at game start when Lua scripts are loaded.
- `ScreenAnchors.Vignette` is dynamically derived off `ScreenCenterX` in
  `RoomManager.lua` when `CreateVignette` is called.
- If we only statically edit `ScreenCenterX` in `UIData.lua`, it will only have
  an effect on `UIData.UsePrompt.X` (computed statically at game start).
- If only we override `ScreenCenterX` after it has been loaded from the save
  file, it will only have an effect on `ScreenAnchors.Vignette` (computed
  dynamically).

Thus, we need to both:

- Edit static screen values in `UIData.lua` and recompute derived static values.
- Override screen values from the save file.

On top of that, some of the statically defined UI positioning is hardcoded and
does not depend on screen values, e.g. `GunUI.StartX = 630` in `UIData.lua`.
We must also reposition hardcoded UI elements on a case-by-case basis.

We hook onto `Load` from `Main.lua` and immediately override screen values
loaded from the save file, then recompute all derived static values as well as
manually reposition hardcoded UI elements.
]]

-- Add `Screen*` variables that we are going to recompute to ignore list, in
-- order to avoid these getting overwritten in the save file. They might be
-- removed from it, but it's fine because if user uninstalls Hephaistos it'll
-- default back to the hardcoded values in `UIData.lua` and add them back again.
SaveIgnores.ScreenWidth = true
SaveIgnores.ScreenHeight = true
SaveIgnores.ScreenCenterX = true
SaveIgnores.ScreenCenterY = true

local function recomputeLuaData()
  -- guard against self-overriding when unnecessary
  if ScreenWidth ~= Hephaistos.ScreenWidth
    or ScreenHeight ~= Hephaistos.ScreenHeight
  then
    -- Override Lua data values loaded from save file
    ScreenCenterX = Hephaistos.ScreenCenterX
    ScreenCenterY = Hephaistos.ScreenCenterY
    ScreenWidth = Hephaistos.ScreenWidth
    ScreenHeight = Hephaistos.ScreenHeight

    -- Recompute dependent and hardcoded Lua data values loaded on game start
    Import "../Mods/Hephaistos/LuaData/ConditionalItemData.lua"
    Import "../Mods/Hephaistos/LuaData/CreditsData.lua"
    Import "../Mods/Hephaistos/LuaData/QuestData.lua"
    Import "../Mods/Hephaistos/LuaData/RoomPresentation.lua"
    Import "../Mods/Hephaistos/LuaData/RunClearMessageData.lua"
    -- Import "../Mods/Hephaistos/LuaData/SeedControlScreen.lua"
    Import "../Mods/Hephaistos/LuaData/UIData.lua"
  end
end

table.insert(Hephaistos.LoadHooks, recomputeLuaData)
