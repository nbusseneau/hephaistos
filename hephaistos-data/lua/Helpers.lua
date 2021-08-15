--[[
Recompute a fixed value, i.e. a value that was set at an offset from a reference
point. Used for moving around elements with a fixed size or fixed position.

Examples:

- Recompute X value fixed at an offset of 60 from the center of the screen:
		RecomputeFixedValue(1020, 960, 1296) = 1356
- Recompute Y value fixed at an offset of -80 from the bottom of the screen:
		RecomputeFixedValue(1000, 1080, 1600) = 1520
]]
local function RecomputeFixedValue(originalValue, originalReferencePoint, newReferencePoint)
	offset = originalReferencePoint - originalValue
	return newReferencePoint - offset
end

function Hephaistos.RecomputeFixedXFromCenter(originalValue)
	return RecomputeFixedValue(originalValue, Hephaistos.Original.ScreenCenterX, Hephaistos.ScreenCenterX)
end

function Hephaistos.RecomputeFixedXFromRight(originalValue)
	return RecomputeFixedValue(originalValue, Hephaistos.Original.ScreenWidth, Hephaistos.ScreenWidth)
end

function Hephaistos.RecomputeFixedYFromCenter(originalValue)
	return RecomputeFixedValue(originalValue, Hephaistos.Original.ScreenCenterY, Hephaistos.ScreenCenterY)
end

function Hephaistos.RecomputeFixedYFromBottom(originalValue)
	return RecomputeFixedValue(originalValue, Hephaistos.Original.ScreenHeight, Hephaistos.ScreenHeight)
end

--[[
Return name of function calling the function calling `GetCallerName`. Sounds
complicated when written like that, but it's not :D

- `foo` calls `bar`
- `bar` calls `GetCallerName`
- `GetCallerName` returns `foo`
]]
function Hephaistos.GetCallerName()
	caller = debug.getinfo(3, 'n')
	return caller ~= nil and caller.name or nil
end

--[[
Check that all keys in `check` exists in `params` and have the same value.
Useful for filtering in hooks by copy/pasting objects from original code, e.g.:

MatchParams(params, { Name = "ShrineMeterBarFill", Group = "Combat_Menu", X = thermometerCenter, Y = ScreenCenterY - 90 })
]]
local function MatchParams(params, check)
	for key, value in pairs(check) do
		if not params[key] or params[key] ~= value then
			return false
		end
	end
	return true
end

--[[
Check all varargs through `Hephaistos.MatchParams(params, vararg)` and return true if any matches.
]]
function Hephaistos.MatchParams(params, ...)
	for _, check in ipairs({...}) do
		if MatchParams(params, check) then
			return true
		end
	end
	return false
end
