---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码异味, 面向对象设计]
aliases: ["Switch Statements", "条件语句"]
relates_to:
  - target: "[[代码异味]]"
    type: part_of
supersedes: null
---

# switch语句

## 概述
switch语句是[[代码异味]]的一种，指长的switch/case或if/else链，通常表示违反了面向对象的开放/封闭原则，缺乏多态性的运用。

## 关键内容

1. **特征识别**：
   - 长switch/case或if/else链
   - 多处出现相同的switch结构
   - 按类型码进行分支判断
   - 添加新case时需要修改多处代码
   - 条件逻辑与数据紧密耦合

2. **负面影响**：
   - 违反开放/封闭原则（对扩展开放，对修改封闭）
   - 修改会扩散到所有相关switch位置
   - 难以扩展新类型
   - 往往说明缺少多态性设计
   - 当添加新类型时，所有条件语句都需要修改

3. **[[重构]]策略**：
   - [[Replace Conditional with Polymorphism]]：[[Replace Conditional with Polymorphism|用多态替换条件]]逻辑
   - [[Replace Type Code with Subclasses]]：用子类替换类型码
   - [[Replace Type Code with State/Strategy]]：用状态或策略模式替换类型码

4. **[[重构]]示例**：
   ```
   // 重构前：使用switch语句
   function calculatePay(employee) {
     switch (employee.type) {
       case 'hourly':
         return employee.hours * employee.rate;
       case 'salaried':
         return employee.salary / 12;
       case 'commissioned':
         return employee.sales * employee.commission;
     }
   }

   // 重构后：使用多态
   class HourlyEmployee {
     calculatePay() {
       return this.hours * this.rate;
     }
   }

   class SalariedEmployee {
     calculatePay() {
       return this.salary / 12;
     }
   }
   ```

## 来源
- [[Martin Fowler]] — 《重构：改善既有代码的设计》
- [[代码异味]] — 重构指导书

## 相关
- [[代码异味]] — switch语句所属的异味类别
- [[重构]] — 解决方法
- [[多态性]] — 面向对象核心概念
- [[开放封闭原则]] — 设计原则
- [[策略模式]] — 相关设计模式