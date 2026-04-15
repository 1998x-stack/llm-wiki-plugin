---
title: "Lua 移动方块示例"
source: "https://chatgpt.com/c/69d660a8-9c94-8322-afa2-e9b6a13176af"
author:
published:
created: 2026-04-08
description: "ChatGPT 是一款供日常使用的 AI 聊天机器人。与最先进的 AI 模型互动，探索创意、解决问题以及提升学习效率。"
tags:
  - "clippings"
---
当然。下面用 **LÖVE（Love2D）** 写一个 **20 行代码** 的小例子：运行后会出现一个能用方向键移动的小方块。

```markdown
x, y = 100, 100
speed = 200

function love.load()
end

function love.update(dt)
    if love.keyboard.isDown("left") then x = x - speed * dt end
    if love.keyboard.isDown("right") then x = x + speed * dt end
    if love.keyboard.isDown("up") then y = y - speed * dt end
    if love.keyboard.isDown("down") then y = y + speed * dt end
end

function love.draw()
    love.graphics.rectangle("fill", x, y, 50, 50)
    love.graphics.print("Use arrow keys to move", 10, 10)
end
```

下面逐行解释：

1. `x, y = 100, 100`  
	定义方块的初始位置，横坐标是 100，纵坐标也是 100。
2. `speed = 200`  
	定义移动速度，表示每秒移动 200 像素。
3. `function love.load()`  
	LÖVE 启动时会自动调用这个函数，通常用来做初始化。
4. `end`  
	`love.load` 结束。这里暂时没有初始化内容，所以是空的。
5. `function love.update(dt)`  
	每一帧都会自动调用这个函数。 `dt` 是这一帧距离上一帧经过了多少秒。
6. `if love.keyboard.isDown("left") then x = x - speed * dt end`  
	如果按着左方向键，就让 `x` 变小，也就是向左移动。
7. `if love.keyboard.isDown("right") then x = x + speed * dt end`  
	如果按着右方向键，就让 `x` 变大，也就是向右移动。
8. `if love.keyboard.isDown("up") then y = y - speed * dt end`  
	如果按着上方向键，就让 `y` 变小，也就是向上移动。
9. `if love.keyboard.isDown("down") then y = y + speed * dt end`  
	如果按着下方向键，就让 `y` 变大，也就是向下移动。
10. `end`  
	`love.update` 结束。
11. `function love.draw()`  
	每一帧都会自动调用这个函数，用来画画面。
12. `love.graphics.rectangle("fill", x, y, 50, 50)`  
	画一个实心矩形。左上角坐标是 `(x, y)` ，宽 50，高 50。
13. `love.graphics.print("Use arrow keys to move", 10, 10)`  
	在窗口左上角显示一行提示文字。
14. `end`  
	`love.draw` 结束。

15-20. 空行  
只是为了把代码凑成 20 行，Lua 不会报错。

你可以把这段代码保存成 `main.lua` ，然后用 LÖVE 打开它运行。

再补一句最核心的理解：

- `love.update(dt)` ：负责“算位置”
- `love.draw()` ：负责“画出来”
- `x, y` ：记录方块在哪
- `speed * dt` ：保证不同电脑帧率不同，移动速度仍然差不多

如果你愿意，我还可以继续给你一个 **“同样 20 行，但加上边界限制，不让方块跑出屏幕”** 的版本。