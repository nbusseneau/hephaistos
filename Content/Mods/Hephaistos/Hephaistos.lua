-- The following `Import` statement must be added to `RoomManager.lua` in order
-- for the mod to be properly loaded. This should be done automatically by
-- Hephaistos.
-- Import "../Mods/Hephaistos/Hephaistos.lua"

-- Hephaistos table
-- Will hold all mod variables and functions
Hephaistos = {}

-- Original screen values
-- As loaded from the save file, originally coming from `UIData.lua` on creation
Hephaistos.Original = {
	ScreenWidth = ScreenWidth,
	ScreenHeight = ScreenHeight,
	ScreenCenterX = ScreenCenterX,
	ScreenCenterY = ScreenCenterY,
}

-- New screen values, as computed by Hephaistos
Import "../Mods/Hephaistos/HephaistosConfig.lua"
Hephaistos.ScreenCenterX = Hephaistos.ScreenWidth / 2
Hephaistos.ScreenCenterY = Hephaistos.ScreenHeight / 2
Hephaistos.ScaleFactorX = Hephaistos.ScreenWidth / Hephaistos.Original.ScreenWidth
Hephaistos.ScaleFactorY = Hephaistos.ScreenHeight / Hephaistos.Original.ScreenHeight
Hephaistos.ScaleFactor = math.max(Hephaistos.ScaleFactorX, Hephaistos.ScaleFactorY)

-- Helper functions
Import "../Mods/Hephaistos/Helpers.lua"

-- Actual Hades modding happens here
Import "../Mods/Hephaistos/FixLuaState.lua"
Import "../Mods/Hephaistos/FixVignetteOverlays.lua"
