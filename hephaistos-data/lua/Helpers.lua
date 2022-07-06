--[[
Recompute a fixed value, i.e. a value that was set at an offset from a reference
point. Used for moving around elements with a fixed size or fixed position.

Examples:

- Recompute X value fixed at an offset of 60 from the center of the screen:
    recomputeFixedValue(1020, 960, 1296) = 1356
- Recompute Y value fixed at an offset of -80 from the bottom of the screen:
    recomputeFixedValue(1000, 1080, 1600) = 1520
]]
local function recomputeFixedValue(originalValue, originalReferencePoint, newReferencePoint)
  local offset = originalReferencePoint - originalValue
  return newReferencePoint - offset
end

function Hephaistos.RecomputeFixedXFromLeft(originalValue, centerHud)
  centerHud = centerHud or Hephaistos.CenterHUD
  if centerHud then
    return Hephaistos.RecomputeFixedXFromCenter(originalValue)
  else
    return originalValue
  end
end

function Hephaistos.RecomputeFixedXFromCenter(originalValue)
  return recomputeFixedValue(originalValue, Hephaistos.Original.ScreenCenterX, Hephaistos.ScreenCenterX)
end

function Hephaistos.RecomputeFixedXFromRight(originalValue, centerHud)
  centerHud = centerHud or Hephaistos.CenterHUD
  if centerHud then
    return Hephaistos.RecomputeFixedXFromCenter(originalValue)
  else
    return recomputeFixedValue(originalValue, Hephaistos.Original.ScreenWidth, Hephaistos.ScreenWidth)
  end
end

function Hephaistos.RecomputeFixedYFromTop(originalValue, centerHud)
  centerHud = centerHud or Hephaistos.CenterHUD
  if centerHud then
    return Hephaistos.RecomputeFixedYFromCenter(originalValue)
  else
    return originalValue
  end
end

function Hephaistos.RecomputeFixedYFromCenter(originalValue)
  return recomputeFixedValue(originalValue, Hephaistos.Original.ScreenCenterY, Hephaistos.ScreenCenterY)
end

function Hephaistos.RecomputeFixedYFromBottom(originalValue, centerHud)
  centerHud = centerHud or Hephaistos.CenterHUD
  if centerHud then
    return Hephaistos.RecomputeFixedYFromCenter(originalValue)
  else
    return recomputeFixedValue(originalValue, Hephaistos.Original.ScreenHeight, Hephaistos.ScreenHeight)
  end
end

--[[
Reposition an object relative to the center of the screen.
]]
function Hephaistos.Recenter(args, X, Y)
  X = X or 'X'
  Y = Y or 'Y'
  args[X] = args[X] and Hephaistos.RecomputeFixedXFromCenter(args[X]) or args[X]
  args[Y] = args[Y] and Hephaistos.RecomputeFixedYFromCenter(args[Y]) or args[Y]
end

function Hephaistos.RecenterOffsets(args)
  Hephaistos.Recenter(args, 'OffsetX', 'OffsetY')
end

--[[
Rescale an object relative to the size of the screen.
]]
function Hephaistos.Rescale(args)
  local originalFraction = args.Fraction
  args.Fraction = originalFraction and originalFraction * Hephaistos.ScaleFactorX or Hephaistos.ScaleFactorX
  SetScaleX(args)
  args.Fraction = originalFraction and originalFraction * Hephaistos.ScaleFactorY or Hephaistos.ScaleFactorY
  SetScaleY(args)
end

--[[
Register pre-hook on given function with `callback` to be executed before the
original function is called.
]]
function Hephaistos.RegisterPreHook(functionName, callback)
  if not ModUtil then
    -- store original function
    Hephaistos.Original[functionName] = _G[functionName]
    -- replace original function with our own version
    _G[functionName] = function(...)
      -- call our callback, then original function
      callback(...)
      return Hephaistos.Original[functionName](...)
    end
  else
    ModUtil.Path.Wrap(functionName, function(base, ...)
      callback(...)
      return base(...)
    end, Hephaistos)
  end
end

--[[
Register post-hook on given function with `callback` to be executed after the
original function has been called.
]]
function Hephaistos.RegisterPostHook(functionName, callback)
  if not ModUtil then
    -- store original function
    Hephaistos.Original[functionName] = _G[functionName]
    -- replace original function with our own version
    _G[functionName] = function(...)
      -- call original function, then our callback
      local val = Hephaistos.Original[functionName](...)
      callback(...)
      return val
    end
  else
    ModUtil.Path.Wrap(functionName, function(base, ...)
      local val = base(...)
      callback(...)
      return val
    end, Hephaistos)
  end
end

--[[
Unregister hook on given function, restoring the original one.
]]
function Hephaistos.UnregisterHook(functionName)
  _G[functionName] = Hephaistos.Original[functionName]
  Hephaistos.Original[functionName] = nil
end

--[[
Check if hook exists on given function.
]]
function Hephaistos.HasHook(functionName)
  return Hephaistos.Original[functionName] ~= nil
end

--[[
Check that all keys in `check` exist in `params` and have the same value.
]]
local function matchAll(params, check)
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
    if matchAll(params, check) then
      return true
    end
  end
  return false
end

--[[
By default return function `GetCallerFunc`:

- `foo` calls `GetCallerFunc`
- `GetCallerFunc` returns `foo` (function)

If optional `level` argument is passed, then it overrides the stack level at
which we look for caller name (default of 2). This is useful when there are
intermediate functions between the caller we want to check for and the actual
call to `GetCallerFunc`.

Example:

- `foo` calls `bar`
- `bar` calls `GetCallerFunc(3)`
- `GetCallerFunc` returns `foo` (function)

Beware of Lua tail calls, as they are "inlined" and do not increment stack
level: https://www.lua.org/manual/5.2/manual.html#3.4.9
]]
function Hephaistos.GetCallerFunc(level)
  level = level and level or 2
  local caller = debug.getinfo(level, 'f')
  return caller and caller.func or nil
end

--[[
Return true when the caller of a specific function we hooked onto with
`Hephaistos.RegisterFilterHook` is registered in `filterTable`, and its filter
condition matches.

See `Hephaistos.RegisterFilterHook` for details.
]]
local function filterHook(filterTable, ...)
  -- check caller of functionName
  local caller = Hephaistos.GetCallerFunc(4)
  if caller then
    -- if caller matches a registered filter from Hephaistos filters, pass
    -- function arguments to filter for analysis
    local shouldFilter = filterTable[caller]
    if shouldFilter and shouldFilter(...) then
      return true
    end
  end
  return false
end

--[[
Register filter hook on given function with `callback` to be executed if a
filter (based on caller function and passed arguments) matches. This is useful
for filtering values in specific function calls when coming from specific
functions with specific arguments.

Everytime a function we've hooked on is called, our hook checks the caller
function and looks up registered filters. If any filter is found for the caller
function, original function call arguments are passed to the filter. If the
filter matches the given arguments, the registered `callback` is called with the
original function call arguments. Afterwards:
- If replaceOriginalCall is set, the callback return value replaces the original
  function call return value (filter and replace mode).
- Otherwise, the original function is called after the callback has been called
  (filter-only mode).

For example, `WeaponUpgradeScripts.lua` originally defines `ShowWeaponUpgradeScreen`,
which itself calls `CreateScreenComponent` with hardcoded X/Y values to position
the weapon image when opening the weapon aspects menu screen (where we can spend
Titan Blood for upgrades):

  components.WeaponImage = CreateScreenComponent({ Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 335, Y = 435 })

To reposition the weapon image, we register a filter with a filter condition
specifically matching the weapon image `CreateScreenComponent` arguments from
`ShowWeaponUpgradeScreen`:

  Hephaistos.CreateScreenComponent[ShowWeaponUpgradeScreen] = function(params)
    return Hephaistos.MatchAll(params, { Name = "rectangle01", Group = "Combat_Menu_TraitTray", X = 335, Y = 435 })
  end

And then we register a filter hook on `CreateScreenComponent`:

  Hephaistos.CreateScreenComponent = {}
  Hephaistos.RegisterFilterHook("CreateScreenComponent", callback)

This will call `callback` with `CreateScreenComponent` arguments, but only
if `CreateScreenComponent` is called from `ShowWeaponUpgradeScreen` with these
specific arguments.
]]
function Hephaistos.RegisterFilterHook(functionName, callback, replaceOriginalCall)
  -- create filter table for storing caller filters
  if not Hephaistos[functionName] then
    Hephaistos[functionName] = {}
  end
  -- store original function
  Hephaistos.Original[functionName] = _G[functionName]
  -- replace original function with our own version
  _G[functionName] = function(...)
    -- if filter matches, pass function arguments to callback
    if filterHook(Hephaistos[functionName], ...) then
      -- if replaceOriginalCall is set, return callback instead of original function call
      if replaceOriginalCall then
        return callback(...)
      -- otherwise return original function call after callback
      else
        callback(...)
        return Hephaistos.Original[functionName](...)
      end
    end
    -- if filter do not match, act as passthrough to the original function call
    return Hephaistos.Original[functionName](...)
  end
end

--[[
Copy all filters from `sourceFilters` to `targetFilters`.
]]
function Hephaistos.LoadFilters(sourceFilters, targetFilters)
  for caller, hooks in pairs(sourceFilters) do
    if not targetFilters[caller] then
      targetFilters[caller] = {}
    end
    for _, hook in ipairs(hooks) do
      table.insert(targetFilters[caller], hook)
    end
  end
end

--[[
Register all filters in `filters` (table) via either:
- Hephaistos.RegisterFilterHook + Hephaistos[OverridenFunction][CallerFunction] = FilterCondition
- ModUtil.Path.Context.Env + ModUtil.Path.Wrap
depending on if ModUtil is available or not.

All filters should be consolidated in a single table via `LoadFilters` so that
they get loaded all at once via a single call to `RegisterFilters`. This is
necessary due to how the ModUtil compatibility layer registers hooks (we don't
want to `ModUtil.Path.Context.Env` the same function multiple times, but only
once).

Multiple calls are idempotent w.r.t. to hooking: the hooks are only set up once,
if the hook already exists then `RegisterFilter` will only re-enable the
filtering itself.
]]
Hephaistos.EnabledFilters = {}
function Hephaistos.RegisterFilters(filters)
  for caller, hooks in pairs(filters) do
    if not ModUtil then
      for _, args in ipairs(hooks) do
        if not Hephaistos.HasHook(args.Hook) then
          Hephaistos.RegisterFilterHook(args.Hook, args.Action)
        end
        if not args.Filter then
          args.Filter = function() return true end
        end
        Hephaistos[args.Hook][_G[caller]] = args.Filter
      end
    else
      if not Hephaistos.EnabledFilters[caller] then
        Hephaistos.EnabledFilters[caller] = {}
        ModUtil.Path.Context.Env(caller, function()
          for _, args in ipairs(hooks) do
            ModUtil.Path.Wrap(args.Hook, function(base, ...)
              if Hephaistos.EnabledFilters[caller][args.Hook] and ( -- filter enabled
                args.Filter and args.Filter(...) -- filter function exists and matches
                or args.Filter == nil -- filter function does not exist (= always true)
              ) then
                args.Action(...)
              end
              return base(...)
            end, Hephaistos)
          end
        end, Hephaistos)
      end
      for _, args in ipairs(hooks) do
        Hephaistos.EnabledFilters[caller][args.Hook] = true
      end
    end
  end
end

--[[
Disable all filters in `filters` (table). The hooks will stay in place and
filtering can be re-enabled by calling `RegisterFilter` again.
]]
function Hephaistos.UnregisterFilters(filters)
  for caller, hooks in pairs(filters) do
    for _, args in ipairs(hooks) do
      if not ModUtil then
        Hephaistos[args.Hook][_G[caller]] = nil
      else
        Hephaistos.EnabledFilters[caller][args.Hook] = nil
      end
    end
  end
end

--[[
FUNCTIONS BELOW ONLY FOR DEVELOPMENT PURPOSES
]]

function Hephaistos.GetCallStack()
  local callstack = ""
  local level = 2
  local caller = true
  while caller do
    caller = debug.getinfo(level, 'n')
    if caller and caller.name then
      callstack = callstack.." "..caller.name
    end
    level = level + 1
  end
  return callstack
end

-- Hephaistos.DevelopmentMode = true
if Hephaistos.DevelopmentMode then
  --[[
  Force roll the end credits (the ones displayed after passing [Redacted] 10
  times).

  Note: the `StartRoom` logic from `RoomManager.lua` has special handling
  related to `BiomeSpeedShrineUpgrade` (the Tight Deadline pact). If this pact
  is enabled, the code below will crash. It must be used with Tight Deadline
  disabled.
  ]]
  OnControlPressed { "Use",
    function(triggerArgs)
      CurrentRun.CurrentRoom = RoomSetData.Surface.E_Story01
      LeaveRoomWithNoDoor(_, { NextMap = "Return01" })
      thread(HandleReturnBoatRideIntro, CurrentRun.CurrentRoom)
    end
  }

  --[[
  Force roll the run clear screen (displayed after passing [Redacted]).
  ]]
  OnControlPressed { "Gift",
    function(triggerArgs)
      ShowRunClearScreen()
    end
  }
end
