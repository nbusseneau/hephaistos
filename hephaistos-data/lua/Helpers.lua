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
  if originalValue ~= nil then
    local offset = originalReferencePoint - originalValue
    return newReferencePoint - offset
  else
    return originalValue
  end
end

function Hephaistos.RecomputeFixedXFromLeft(originalValue, centerHud)
  centerHud = centerHud or (centerHud == nil and Hephaistos.CenterHUD)
  if centerHud then
    return Hephaistos.RecomputeFixedXFromCenter(originalValue)
  else
    return originalValue
  end
end

function Hephaistos.RecomputeFixedXFromCenter(originalValue)
  return recomputeFixedValue(originalValue, Hephaistos.Default.ScreenCenterX, Hephaistos.ScreenCenterX)
end

function Hephaistos.RecomputeFixedXFromRight(originalValue, centerHud)
  centerHud = centerHud or (centerHud == nil and Hephaistos.CenterHUD)
  if centerHud then
    return Hephaistos.RecomputeFixedXFromCenter(originalValue)
  else
    return recomputeFixedValue(originalValue, Hephaistos.Default.ScreenWidth, Hephaistos.ScreenWidth)
  end
end

function Hephaistos.RecomputeFixedYFromTop(originalValue, centerHud)
  centerHud = centerHud or (centerHud == nil and Hephaistos.CenterHUD)
  if centerHud then
    return Hephaistos.RecomputeFixedYFromCenter(originalValue)
  else
    return originalValue
  end
end

function Hephaistos.RecomputeFixedYFromCenter(originalValue)
  return recomputeFixedValue(originalValue, Hephaistos.Default.ScreenCenterY, Hephaistos.ScreenCenterY)
end

function Hephaistos.RecomputeFixedYFromBottom(originalValue, centerHud)
  centerHud = centerHud or (centerHud == nil and Hephaistos.CenterHUD)
  if centerHud then
    return Hephaistos.RecomputeFixedYFromCenter(originalValue)
  else
    return recomputeFixedValue(originalValue, Hephaistos.Default.ScreenHeight, Hephaistos.ScreenHeight)
  end
end

--[[
Reposition an object relative to the center of the screen.
]]
function Hephaistos.Recenter(args, X, Y)
  X = X or 'X'
  Y = Y or 'Y'
  args[X] = Hephaistos.RecomputeFixedXFromCenter(args[X])
  args[Y] = Hephaistos.RecomputeFixedYFromCenter(args[Y])
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
Check that all keys in `dict` exist in `params` and have the same value.
]]
local function matchAll(params, dict)
  for key, value in pairs(dict) do
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
  for _, dict in ipairs({ ... }) do
    if matchAll(params, dict) then
      return true
    end
  end
  return false
end

--[[
Used to store original functions when replacing them by custom hooks.
]]
Hephaistos.Original = {}

--[[
Register pre-hook on given function with `callback` to be executed before the
original function is called.

Important: this function should NOT be called to hook multiple times on the same
original function. Hooks should be consolidated such that a single register is
done, so that Hephaistos.Original always contains the actual original function.
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

Important: this function should NOT be called to hook multiple times on the same
original function. Hooks should be consolidated such that a single register is
done, so that Hephaistos.Original always contains the actual original function.
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
Index data from Hephaistos.FilterHooks such that it is indexed by hooked
function, rather than by caller as in the original data.

We index caller functions themselves because we want to match caller by function
object rather than by name, to avoid issues when the caller is called from an
engine event (e.g. `OnPressedFunctionName`) and thus has no "name" from Lua's
perspective (it's just `func`).
]]
local function indexHooksByCaller()
  local index = {}
  for caller, hooks in pairs(Hephaistos.FilterHooks) do
    for hook, _ in pairs(hooks) do
      if not index[hook] then
        index[hook] = {}
      end
      table.insert(index[hook], { _G[caller], caller })
    end
  end
  return index
end

--[[
Check if given hook array matches the callerFunc object, and return caller name.
]]
local function tryGetCallerName(hookArray, callerFunc)
  for _, v in ipairs(hookArray) do
    if v[1] == callerFunc then
      return v[2]
    end
  end
  return nil
end

--[[
Register all filter hooks in `Hephaistos.FilterHooks` table, using either:
- Custom hooks
- ModUtil.Path.Context.Env + ModUtil.Path.Wrap
depending on if ModUtil is available or not.

Important: this function should NOT be called multiple times. Filter hooks
should be consolidated in a `Hephaistos.FilterHooks` via `CopyFilterHooks` so
that they get registered all at once via a single call to `RegisterFilterHooks`.

This is necessary due to how the hook compatibility layer registers hooks:
- We don't want to "custom hook" onto the same function more than once so that
  Hephaistos.Original always contains the actual original function.
- We don't want to `ModUtil.Path.Context.Env` the same function more than once,
  otherwise there are side effects (e.g. same hook called several times).

Filter hooks are implicitly marked as enabled upon registration, use
`DisableFilterHooks` if need be (e.g. for dynamic centering when displaying run
clear screen, see `CenterHUD.lua`).

See `GUIComponent.lua` for user documentation on filter hooks.
]]
function Hephaistos.RegisterFilterHooks()
  if not ModUtil then
    -- register manually using custom hooks
    -- index hooks by caller
    local index = indexHooksByCaller()
    -- then iterate through hooks and register as we go
    for hook, _ in pairs(index) do
      -- store original function
      Hephaistos.Original[hook] = _G[hook]
      -- replace original function with our own version
      _G[hook] = function(...)
        -- get current caller of hooked function
        local callerFunc = Hephaistos.GetCallerFunc(3)
        -- check if current caller matches a caller registered for this hook
        local caller = tryGetCallerName(index[hook], callerFunc)
        if caller then
          -- loop through enabled filters and execute callback if they match
          for _, args in pairs(Hephaistos.FilterHooks[caller][hook]) do
            if args.IsEnabled
              and (args.Filter and args.Filter(...) -- filter function exists and matches
                or args.Filter == nil) -- filter function does not exist (= always true)
            then
              args.Callback(...)
            end
          end
        end
        -- passthrough to the original function
        return Hephaistos.Original[hook](...)
      end
    end
  else
    -- register using ModUtil.Path.Context.Env + ModUtil.Path.Wrap
    -- we iterate through Hephaistos.FiltersHooks and register as we go
    for caller, hooks in pairs(Hephaistos.FilterHooks) do
      -- register context env for caller
      ModUtil.Path.Context.Env(caller, function()
        -- loop through hooks and register contextual wraps for each one
        for hook, filterHooks in pairs(hooks) do
          ModUtil.Path.Wrap(hook, function(base, ...)
            -- loop through enabled filters and execute callback if they match
            for _, args in pairs(filterHooks) do
              if args.IsEnabled
                and (args.Filter and args.Filter(...) -- filter function exists and matches
                  or args.Filter == nil) -- filter function does not exist (= always true)
              then
                args.Callback(...)
              end
            end
            -- passthrough to the original function
            return base(...)
          end, Hephaistos)
        end
      end, Hephaistos)
    end
  end
  -- enable all registered filter hooks
  Hephaistos.EnableFilterHooks(Hephaistos.FilterHooks)
end

--[[
Enable all filters in `filters` table.
]]
function Hephaistos.EnableFilterHooks(filters)
  for caller, hooks in pairs(filters) do
    for hook, filterHooks in pairs(hooks) do
      for filterHook, _ in pairs(filterHooks) do
        Hephaistos.FilterHooks[caller][hook][filterHook].IsEnabled = true
      end
    end
  end
end

--[[
Disable all filters in `filters` table.
]]
function Hephaistos.DisableFilterHooks(filters)
  for caller, hooks in pairs(filters) do
    for hook, filterHooks in pairs(hooks) do
      for filterHook, _ in pairs(filterHooks) do
        Hephaistos.FilterHooks[caller][hook][filterHook].IsEnabled = false
      end
    end
  end
end

--[[
Copy all filter hooks from `source` table to `target` table.
]]
function Hephaistos.CopyFilterHooks(source, target)
  for caller, hooks in pairs(source) do
    if not target[caller] then
      target[caller] = hooks
    else
      for hook, filterHooks in pairs(hooks) do
        if not target[caller][hook] then
          target[caller][hook] = filterHooks
        else
          for filterHook, args in pairs(filterHooks) do
            target[caller][hook][filterHook] = args
          end
        end
      end
    end
  end
end

--[[
Return caller function object, i.e.:

- `foo` calls `GetCallerFunc`
- `GetCallerFunc` returns `foo` function object

If optional `level` argument is passed, then it overrides the stack level at
which we look for caller name (default of 2). This is useful when there are
intermediate functions between the caller we want to check for and the actual
call to `GetCallerFunc`.

Example:

- `foo` calls `bar`
- `bar` calls `GetCallerFunc(3)`
- `GetCallerFunc` returns `foo` function object

Beware of Lua tail calls, as they are "inlined" and do not increment stack
level: https://www.lua.org/manual/5.2/manual.html#3.4.9
]]
function Hephaistos.GetCallerFunc(level)
  level = level and level or 2
  local caller = debug.getinfo(level, 'f')
  return caller and caller.func or nil
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
      callstack = callstack .. " " .. caller.name
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
