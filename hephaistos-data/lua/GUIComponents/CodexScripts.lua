local chapterSpacing = 225
local chapterX = 480
local chapterY = 205

local filterHooks = {
  OpenCodexScreen = {
    SetScale = {
      -- codex chapters
      CodexChapters = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = CodexUI.Screen.Components.BackgroundTint.Id, Fraction = 10 })
        end,
        Callback = Hephaistos.Rescale,
      },
    },
  },
  CodexUpdateChapters = {
    CreateScreenComponent = {
      -- codex chapters
      CodexChapters = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "ButtonCodexLeft", Y = chapterY, Scale = 0.8, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay" })
            and params.X >= chapterX - CodexUI.ArrowLeftSpacerX
            or Hephaistos.MatchAll(params, { Name = "ButtonCodexRight", Y = chapterY, Scale = 0.8, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay" })
            and params.X >= chapterX + CodexUI.ArrowRightSpacerX + (CodexUI.MaxChapters - 1) * chapterSpacing
            or Hephaistos.MatchAll(params, { Name = "ButtonCodexTab", Y = chapterY, Sound = "/SFX/Menu Sounds/GeneralWhooshMENU", Group = "Combat_Menu_Overlay" })
            and params.X >= chapterX
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  CodexOpenEntry = {
    CreateScreenComponent = {
      -- codex entry
      CodexEntry = {
        Filter = function(params)
          return Hephaistos.MatchAll(params,
            { Name = "BlankObstacle", X = 600, Y = 285, Group = "Combat_Menu_Overlay" },
            { Name = "BlankObstacle", X = 770 + 800, Y = 930, Group = "Combat_Menu_Overlay" },
            { Name = "CodexBoonInfoTextBacking", X = 1450, Y = 930, Group = "Combat_Menu_Overlay" })
            or Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = 670, Scale = 1.0, Group = "Combat_Menu_Overlay" })
            and params.Y >= 616
            or Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = 770, Group = "Combat_Menu_Overlay" })
            and params.Y >= 370
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
  UpdateChapterEntryArrows = {
    Teleport = {
      -- codex chapter arrows
      CodexChapterArrows = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Id = CodexUI.ChapterArrowId })
        end,
        Callback = Hephaistos.RecenterOffsets,
      },
    },
  },
  CreateRelationshipBar = {
    CreateScreenComponent = {
      -- codex relationship bar
      CodexRelationshipBar = {
        Filter = function(params)
          return Hephaistos.MatchAll(params, { Name = "BlankObstacle", X = 500, Y = 385, Group = "Combat_Menu_Overlay" })
        end,
        Callback = Hephaistos.Recenter,
      },
    },
  },
}

Hephaistos.CopyFilterHooks(filterHooks, Hephaistos.FilterHooks)
