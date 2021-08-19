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
Check that all keys in `check` exist in `params` and have the same value.
]]
local function MatchAll(params, check)
	for key, value in pairs(check) do
		if not params[key] or params[key] ~= value then
			return false
		end
	end
	return true
end

--[[
Return true if any vararg has all its keys in `params` with the same value.
Useful for filtering in hooks by copy/pasting objects from original code, e.g.:

MatchAll(params,
	{ Name = "Foo", Group = "Bar", X = 10, Y = 20 },
	{ Name = "Foo2", Group = "Bar2", X = 30, Y = 40 })
=> check if `params` matches any of those 2
]]
function Hephaistos.MatchAll(params, ...)
	for _, check in ipairs({...}) do
		if MatchAll(params, check) then
			return true
		end
	end
	return false
end

--[[
By default return name of function calling the function calling `GetCallerName`.
Sounds complicated when written like that, but it's not :D

- `foo` calls `bar`
- `bar` calls `GetCallerName`
- `GetCallerName` returns `foo`

If optional `level` parameter is passed, then it overrides the stack level at
which we look for caller name (default of 3). This is useful when adding
intermediate functions between the caller we want to check for and the actual
call to `GetCallerName`.
]]
function Hephaistos.GetCallerName(level)
	level = level ~= nil and level or 3
	caller = debug.getinfo(level, 'n')
	return caller ~= nil and caller.name or nil
end

--[[
Filters `params` by executing `doFilter` when the caller of a specific function
we hooked with `Hephaistos.Filter` matches `filterTable` and `params`.

- `foo` calls `bar` in original Lua code
- We hook onto `bar` and add a call to `Hephaistos.Filter` with an arbitrary `doFilter`:
		Hephaistos.Filter(filterTable, params, function(params)
			...
		end)
- Separately, we register a hook for `foo` in `filterTable`:
		filterTable.foo = function(params)
			return Hephaistos.MatchAll(params, ...)
		end
- When `bar` is called, `Hephaistos.Filter` checks the caller the name:
	- If the caller is `foo` and `params` matches the filter from `filterTable`,
	  it executes `doFilter` on `params`.
	- If the caller is not `foo` or `params` do not match the filter from
		`filterTable`, nothing happens.

This is useful for filtering on a specific caller function passing specific
params that we want to modify.
]]
function Hephaistos.Filter(filterTable, params, doFilter)
	caller = Hephaistos.GetCallerName(4)
	if caller then
		shouldFilter = filterTable[caller]
		if shouldFilter and shouldFilter(params) then
			doFilter(params)
		end
	end
end
