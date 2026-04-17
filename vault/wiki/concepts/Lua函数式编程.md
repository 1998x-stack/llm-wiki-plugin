---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [技术, Lua, 编程语言, 方法论, Lua编程]
aliases: [Lua函数式, Lua FP, Lua map filter reduce, Lua柯里化, Lua记忆化]
relates_to:
  - target: "[[Lua-OOP]]"
    type: extends
    confidence: 0.7
  - target: "[[Lua模块系统]]"
    type: uses
    confidence: 0.8
  - target: "[[Lua-table]]"
    type: depends_on
    confidence: 0.95
supersedes: null
---
# Lua 函数式编程

## 概述
Lua 一等公民函数支持完整[[函数式编程]][[规范化理论|范式]]：map/filter/reduce、函数组合（compose/pipe）、柯里化（curry）、记忆化（memoize）均可用闭包实现。

## 关键内容

### 核心高阶函数

```lua
local F = {}

-- map: 对每个元素应用变换
function F.map(t, fn)
    local result = {}
    for i, v in ipairs(t) do result[i] = fn(v, i) end
    return result
end

-- filter: 保留满足谓词的元素
function F.filter(t, pred)
    local result = {}
    for _, v in ipairs(t) do
        if pred(v) then result[#result+1] = v end
    end
    return result
end

-- reduce: 折叠为单值
function F.reduce(t, fn, init)
    local acc = init
    for _, v in ipairs(t) do acc = fn(acc, v) end
    return acc
end
```

### 函数组合与管道

```lua
-- compose: 右到左，数学风格 f(g(h(x)))
function F.compose(...)
    local fns = {...}
    return function(x)
        local result = x
        for i = #fns, 1, -1 do result = fns[i](result) end
        return result
    end
end

-- pipe: 左到右，数据流风格
function F.pipe(...)
    local fns = {...}
    return function(x)
        local result = x
        for _, fn in ipairs(fns) do result = fn(result) end
        return result
    end
end

-- 实用示例：过滤偶数并取平方
local even_squares = F.pipe(
    function(t) return F.filter(t, function(x) return x % 2 == 0 end) end,
    function(t) return F.map(t, function(x) return x * x end) end
)({1,2,3,4,5,6,7,8,9,10})
-- 结果: {4, 16, 36, 64, 100}
```

### 柯里化

```lua
-- curry: 将多参函数变为可逐步应用的单参函数链
function F.curry(fn, arity)
    arity = arity or debug.getinfo(fn, "u").nparams
    local function curried(args)
        if #args >= arity then return fn(table.unpack(args)) end
        return function(...)
            local new_args = {table.unpack(args)}
            for _, v in ipairs({...}) do new_args[#new_args+1] = v end
            return curried(new_args)
        end
    end
    return curried({})
end

-- 使用：add(1)(2)(3) 或 add(1, 2)(3) 均可
local add = F.curry(function(a, b, c) return a + b + c end)
print(add(1)(2)(3))  -- 6
```

### 记忆化

```lua
-- memoize: 缓存计算结果，适合纯函数重复调用
function F.memoize(fn)
    local cache = {}
    return function(...)
        local key = table.concat({...}, ",")
        if cache[key] == nil then
            cache[key] = fn(...)
        end
        return cache[key]
    end
end

-- 经典用例：斐波那契数列（注意需先声明 local）
local fib
fib = F.memoize(function(n)
    if n <= 1 then return n end
    return fib(n-1) + fib(n-2)
end)
```

### 设计原则

1. **纯函数优先**：无副作用，相同输入永远相同输出，便于测试和组合
2. **惰性管道**：pipe/compose 延迟执行，只在传入数据时触发
3. **记忆化适用范围**：仅适用于纯函数；若 key 包含 table 引用，需自定义序列化
4. **柯里化 arity**：Lua 不支持函数签名反射时手动指定 `arity` 参数

## 常见陷阱

- **memoize key 冲突**：`table.concat({1,2}, ",")` 与 `table.concat({12}, ",")` 相同，需更健壮的 key 生成
- **curry + vararg**：Lua 的 `...` 在闭包中传递需用 `{...}` 打包，不能直接捕获
- **compose 顺序**：compose 是右到左（数学），pipe 是左到右（数据流），混淆是高频错误

## 来源
- [[raw/articles/programming/lua/lua-skill/references/patterns.md]] — Lua 高级模式参考，函数式编程模式章节

## 相关
- [[Lua-OOP]] — 面向对象与函数式可以混用，函数作为一等公民是两者共同基础
- [[Lua模块系统]] — 函数式工具库通常以模块形式组织和导出
- [[Lua-table]] — map/filter/reduce 操作的基础数据结构
