--[[
The camera has a soft clamping system where it clamps onto points of interest
such as exit doors in various situations. The default clamping weight is too
strong for larger viewports such as 32:9 or 48:9, with the camera not following
Zagreus anymore, resulting in an unpleasant experience especially if the HUD was
centered as Zagreus appears to exit the main play area.

We simply scale down the soft clamp depending on the viewport scale factor,
which allows the camera to behave identically to the original 16:9 viewport
after being extended.
]]

local function rescaleSoftClamp(args)
  args.SoftClamp = args.SoftClamp and args.SoftClamp * (1 / Hephaistos.ScaleFactorX) or nil
end

Hephaistos.RegisterFilterHook("SetCameraClamp", rescaleSoftClamp)

local function hasClamp(args)
  return args.SoftClamp
end

Hephaistos.SetCameraClamp[StartRoomPresentation] = hasClamp
Hephaistos.SetCameraClamp[RestoreUnlockRoomExitsPresentation] = hasClamp
Hephaistos.SetCameraClamp[StartDeathLoopPresentation] = hasClamp
Hephaistos.SetCameraClamp[StartDeathLoopFromBoatPresentation] = hasClamp
