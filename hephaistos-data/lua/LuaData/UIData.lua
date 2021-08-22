Hephaistos.Recenter(CodexUI, 'EntryX', 'EntryY')

UIData.CurrentRunDepth.X = Hephaistos.RecomputeFixedXFromRight(UIData.CurrentRunDepth.X)
UIData.UsePrompt.X = ScreenCenterX
UIData.UsePrompt.Y = Hephaistos.RecomputeFixedYFromBottom(UIData.UsePrompt.Y)

Hephaistos.Recenter(ShopUI, 'ShopItemStartX', 'ShopItemStartY')

SuperUI.PipY = Hephaistos.RecomputeFixedYFromBottom(SuperUI.PipY)

TraitUI.StartY = Hephaistos.RecomputeFixedYFromCenter(TraitUI.StartY)
TraitUI.IconStartY = Hephaistos.RecomputeFixedYFromCenter(TraitUI.IconStartY)

ConsumableUI.StartX = Hephaistos.RecomputeFixedXFromRight(ConsumableUI.StartX)
ConsumableUI.StartY =  Hephaistos.RecomputeFixedYFromBottom(ConsumableUI.StartY)
