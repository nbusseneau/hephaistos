--[[
Hephaistos' hooking mechanism requires that hooks be consolidated such that a
single register is done (see `Helpers.lua` for more details).

When a function needs to be hooked from multiple places in the code:

- `HooksInit.lua` is loaded first and prepares tables to store shared hooks.
- Other mod files load hooks into the shared tables.
- `HooksRegister.lua` is loaded last and registers all hooks at once.
]]

Hephaistos.LoadHooks = {}
Hephaistos.FilterHooks = {}
