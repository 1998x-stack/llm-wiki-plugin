# Input Module

UrhoX Lua API - Input Module

---

## 鼠标模式设置指南

> **重要提示**：引擎默认**显示鼠标光标**（`mouseVisible = true`）。

### 何时需要设置鼠标模式？

对于**需要鼠标控制视角方向**的游戏类型（如 FPS 第一人称射击、TPS 第三人称射击、飞行模拟等），需要在游戏启动时设置鼠标模式为 `MM_RELATIVE`

### 鼠标模式说明

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `MM_ABSOLUTE` | 默认模式，鼠标可自由移动，可显示/隐藏光标 | 菜单界面、RTS策略游戏、编辑器 |
| `MM_RELATIVE` | 鼠标锁定在窗口内，**强制隐藏光标**，获取相对移动量 | **FPS、TPS、飞行模拟等需要鼠标控制视角的游戏** |
| `MM_WRAP` | 鼠标到达边界时环绕到另一边 | 特殊需求 |
| `MM_FREE` | 鼠标不被限制，即使隐藏也不锁定 | 需要自定义光标渲染的场景 |

### 典型使用场景

```lua
-- 场景1: 普通 UI 界面（菜单、商店等）
input.mouseMode = MM_ABSOLUTE
input.mouseVisible = true

-- 场景2: FPS/TPS 游戏主循环
input.mouseMode = MM_RELATIVE
-- mouseVisible 自动被设为 false，通过 input:GetMouseMove() 获取移动量

-- 场景3: RTS/策略游戏（使用自定义 UI 光标）
input.mouseMode = MM_ABSOLUTE
input.mouseVisible = false  -- 隐藏系统光标，使用 UI Cursor 组件

-- 场景4: 暂停菜单时临时释放鼠标
input.mouseMode = MM_ABSOLUTE
input.mouseVisible = true
```

### ⚠️ Web 平台特殊限制 (Pointer Lock API)

在 Web 平台上，`MM_RELATIVE` 模式使用浏览器的 **Pointer Lock API**，有以下重要限制：

| 限制 | 说明 |
|------|------|
| **ESC 强制退出** | 用户按 ESC 键，浏览器会**强制**退出 Pointer Lock，`mouseMode` 自动变为 `MM_FREE` |
| **ESC 后冷却期** | ESC 退出后约 **1-2 秒内**无法重新锁定，否则报 `SecurityError`（不影响逻辑，仅控制台报错） |
| **需要用户交互** | 必须在用户点击事件中请求锁定 |

**推荐做法**：使用 `Sample.lua` 提供的 `SampleInitMouseMode(MM_RELATIVE)` 函数，自动处理 Web 平台兼容（点击恢复锁定、ESC 退出等）。

> 参见：`LuaScripts/Utilities/Sample.lua` 中的 `SampleInitMouseMode`、`HandleMouseModeRequest`、`HandleMouseModeChange`

> **注**：ESC 退出后立即点击会报 `SecurityError`，等 1-2 秒后再点击即可（不影响功能）。

---

## Classes

- [Input](#input)
- [Controls](#controls)
- [TouchState](#touchstate)
- [JoystickState](#joystickstate)

---

**Inherits from**: Object

## Input : Object


### Methods


- void SetToggleFullscreen(bool enable)
- void SetMouseVisible(bool enable, bool suppressEvent = false)
- void SetMouseGrabbed(bool grab, bool suppressEvent = false)
- void SetMouseMode(MouseMode mode, bool suppressEvent = false)
- bool IsMouseLocked()
- int AddScreenJoystick(XMLFile* layoutFile = 0, XMLFile* styleFile = 0)
- bool RemoveScreenJoystick(int id)
- void SetScreenJoystickVisible(int id, bool enable)
- void SetScreenKeyboardVisible(bool enable)
- void SetTouchEmulation(bool enable)
- bool RecordGesture()
- bool SaveGestures(File* dest)
- bool SaveGesture(File* dest, unsigned gestureID)
- unsigned LoadGestures(File* source)
- bool SaveGestures(const String fileName)
- bool SaveGesture(const String fileName, unsigned gestureID)
- unsigned LoadGestures(const String fileName)
- bool RemoveGesture(unsigned gestureID)
- void RemoveAllGestures()
- void SetMousePosition(const IntVector2& position)
- void CenterMousePosition()
- Key GetKeyFromName(const String name) const
- Key GetKeyFromScancode(Scancode scancode) const
- String GetKeyName(Key key) const
- Scancode GetScancodeFromKey(Key key) const
- Scancode GetScancodeFromName(const String name) const
- String GetScancodeName(Scancode scancode) const
- bool GetKeyDown(Key key) const
- bool GetKeyPress(Key key) const
- bool GetScancodeDown(Scancode scancode) const
- bool GetScancodePress(Scancode scancode) const
- bool GetMouseButtonDown(MouseButton button) const
- bool GetMouseButtonPress(MouseButton button) const
- bool GetQualifierDown(Qualifier qualifier) const
- bool GetQualifierPress(Qualifier qualifier) const
- int GetQualifiers() const
- IntVector2 GetMousePosition() const
- IntVector2 GetMouseMove() const
- int GetMouseMoveX() const
- int GetMouseMoveY() const
- int GetMouseMoveWheel() const
- Vector2 GetInputScale() const
- unsigned GetNumTouches() const
- TouchState* GetTouch(unsigned index) const
- unsigned GetNumJoysticks() const
- JoystickState* GetJoystick(int id)
- JoystickState* GetJoystickByIndex(unsigned index)
- JoystickState* GetJoystickByName(const String name)
- bool GetToggleFullscreen() const
- bool GetScreenKeyboardSupport() const
- bool IsScreenJoystickVisible(int id) const
- bool IsScreenKeyboardVisible() const
- bool GetTouchEmulation() const
- bool IsMouseVisible() const
- bool IsMouseGrabbed() const
- MouseMode GetMouseMode() const
- bool HasFocus()
- bool IsMinimized() const

### Properties


- int qualifiers (readonly)
- IntVector2 mousePosition
- IntVector2 mouseMove (readonly)
- int mouseMoveX (readonly)
- int mouseMoveY (readonly)
- int mouseMoveWheel (readonly)
- Vector2 inputScale (readonly)
- unsigned numTouches (readonly)
- unsigned numJoysticks (readonly)
- bool toggleFullscreen (readonly)
- bool screenKeyboardSupport (readonly)
- MouseMode mouseMode
- bool screenKeyboardVisible
- bool touchEmulation
- bool mouseVisible
- bool mouseGrabbed
- bool mouseLocked (readonly)
- bool focus (readonly)
- bool minimized (readonly)



---

## Controls



### Methods


- Controls() (GC)
- Controls* new()
- void delete()
- void Reset()
- void Set(unsigned buttons, bool down = true)
- bool IsDown(unsigned button) const
- bool IsPressed(unsigned button, const Controls& previousControls) const

### Properties


- unsigned buttons
- float yaw
- float pitch
- VariantMap extraData



---

## TouchState



### Methods


- UIElement* GetTouchedElement()

### Properties


- int touchID
- IntVector2 position
- IntVector2 lastPosition
- IntVector2 delta
- float pressure
- UIElement* touchedElement (readonly)



---

## JoystickState



### Methods


- bool IsController() const
- unsigned GetNumButtons() const
- unsigned GetNumAxes() const
- unsigned GetNumHats() const
- bool GetButtonDown(unsigned index) const
- bool GetButtonPress(unsigned index) const
- float GetAxisPosition(unsigned index) const
- int GetHatPosition(unsigned index) const

### Properties


- const String name
- const int joystickID
- bool controller (readonly)
- unsigned numButtons (readonly)
- unsigned numAxes (readonly)
- unsigned numHats (readonly)



---

