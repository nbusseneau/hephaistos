local filterHooks = {
  TraitLockedPresentation = {
    CreateScreenComponent = {
      -- locked choice overlay due to Approval Process pact
      LockedChoiceApprovalProcess = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", Group = "Combat_Menu_Overlay" })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
