--First enable Hammerspoon in security/privacy/accessibility
--https://github.com/Hammerspoon/hammerspoon/issues/237#issuecomment-476320469


hs.hotkey.bind({"cmd", "ctrl"}, "j", function()
  hs.application.launchOrFocus("Safari")
end)

hs.hotkey.bind({"cmd", "ctrl"}, "k", function()
  hs.application.launchOrFocus("Terminal")
end)

hs.hotkey.bind({"ctrl"}, "Y", function()
  local win = hs.window.focusedWindow()
  local f = win:frame()
  local screen = win:screen()
  local max = screen:frame()

  f.x = max.x
  f.y = max.y
  f.w = max.w / 2
  f.h = max.h
  win:setFrame(f)
end)

hs.hotkey.bind({"ctrl"}, "O", function()
  local win = hs.window.focusedWindow()
  local f = win:frame()
  local screen = win:screen()
  local max = screen:frame()

  f.x = max.x + max.w / 2
  f.y = max.y
  f.w = max.w / 2
  f.h = max.h
  win:setFrame(f)
end)

hs.hotkey.bind({"ctrl"}, "P", function()
  local win = hs.window.focusedWindow()
  local f = win:frame()
  local screen = win:screen()
  local max = screen:frame()

  f.x = max.x
  f.y = max.y
  f.w = max.w
  f.h = max.h
  win:setFrame(f)
end)
