local filterHooks = {
  DisplayTextLine = {
    CreateScreenObstacle = {
      -- encounter choices (Eurydice, etc.)
      EncounterChoices = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "ButtonDialogueChoice", Group = "Combat_Menu" })
        end,
        Callback = function(params) params.Y = Hephaistos.RecomputeFixedYFromCenter(params.Y) end,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
