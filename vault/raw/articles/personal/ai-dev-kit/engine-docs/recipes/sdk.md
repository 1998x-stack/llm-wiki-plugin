# SDK 接口使用指南


## 📢 激励视频广告

### API

```lua
sdk:ShowRewardVideoAd(callback)
```

**回调参数 `result`：**
- `success` (boolean): 广告播放是否成功
- `msg` (string): 结果消息

### 示例

```lua
local function watchAdForReward()
    sdk:ShowRewardVideoAd(function(result)
        if result.success then
            playerCoins = playerCoins + 100
            showMessage("获得 100 金币！")
        else
            showMessage("广告播放失败: " .. result.msg)
        end
    end)
end
```

### 回调 `result.msg` 取值说明

| msg | success | 含义 |
|-----|---------|------|
| `"embed success"` | `true` | 广告完整观看，可发放奖励 |
| `"embed manual close"` | `false` | 用户在广告播放完成前**主动关闭**，不应发放奖励 |
| `"unsupported platform"` | `false` | 非嵌入式环境或平台不支持广告 |
| 其他字符串 | `false` | TapSDK 内部错误，值为错误描述 |

> **`embed manual close`**：仅出现在 iOS Embed 模式下。表示广告 `onClose` 回调触发时 `finished = false`，即用户未完整观看即手动关闭。此时**不应给予奖励**，可提示用户"需完整观看广告才能获得奖励"。

### 注意事项
- 只有在 `result.success` 为 `true` 时才给予玩家奖励
- 遵循平台广告约束：
  - 用户体验优先，禁止生成用户在无预期下需要强制观看的广告
  - 尽可能贴合游戏原本的设计，较为自然地接入广告
  - 鼓励使用激励形式，用户观看广告后可以获得一些奖励

---

## 🚪 宿主退出按钮位置

在嵌入式容器（TapTap）中运行时，宿主环境会在屏幕上显示一个退出按钮。游戏可以通过此接口获取退出按钮的位置，避免自身 UI 与之重叠。

### API

```lua
sdk:GetNativeExitMenuRect() -> table | nil
```

**返回值：**
- 成功：`table { left, top, right, bottom }` — 归一化坐标 (0~1)，左上角为原点
- 不可用（非嵌入环境）：`nil`

| 字段 | 类型 | 说明 |
|------|------|------|
| `left` | number | 矩形左边缘 x (0~1) |
| `top` | number | 矩形上边缘 y (0~1) |
| `right` | number | 矩形右边缘 x (0~1) |
| `bottom` | number | 矩形下边缘 y (0~1) |

### 示例

```lua
local rect = sdk:GetNativeExitMenuRect()
if rect then
    -- rect ≈ {left=0.92, top=0.01, right=0.99, bottom=0.05}
    -- 避免在退出按钮区域放置游戏 UI
end
```

### 注意事项
- 坐标为 **归一化值 (0~1)**，与设备分辨率无关
- 仅在嵌入式容器环境下返回有效值，其他运行时返回 `nil`
- 建议在 `Start()` 中调用一次并缓存结果，按钮位置在运行期间不会变化

---