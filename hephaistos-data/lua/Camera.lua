--[[
The camera has a soft clamping system where it clamps onto points of interest
such as exit doors in various situations. The default clamping weight is too
strong for larger viewports such as 32:9 or 48:9, with the camera not following
Zagreus anymore, resulting in an unpleasant experience especially if the HUD was
centered as Zagreus appears to exit the main play area.

We simply scale down the soft clamp depending on the viewport scale factor,
which allows the camera to behave identically to the original 16:9 viewport
after being extended. Also, when clamp weight is set to 0.0 as in Asphodel, we
manually force it to 0.001 as otherwise it defaults to 1.0 and does weird things
at higher resolutions. Funnily enough, the 0.001 kludge is already used by in
the original Lua (`LeaveDeathAreaRoomPresentation` from `RoomPresentation.lua`).
]]

Hephaistos.RegisterPreHook("SetCameraClamp", function(args)
  args.SoftClamp = args.SoftClamp == 0.0 and 0.001 or args.SoftClamp
  args.SoftClamp = args.SoftClamp and args.SoftClamp * (1.0 / Hephaistos.ScaleFactorX) or args.SoftClamp
end)
