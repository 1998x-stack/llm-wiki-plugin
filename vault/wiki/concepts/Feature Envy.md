---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码异味, 封装性, AI工程]
aliases: ["Feature Envy", "特性眷恋"]
relates_to: []
supersedes: null
---

# Feature Envy

## 概述
Feature Envy是耦合类[[代码异味]]的一种，指一个方法更多地访问其他类的数据而不是自己所在类的数据，表明该方法可能属于另一个类。

## 关键内容

1. **特征识别**：
   - 一个方法使用其他类的数据比自己类的数据更多
   - 对另一个对象调用大量的getter方法
   - 数据和行为分离
   - 方法频繁访问其他对象的内部状态

2. **负面影响**：
   - 行为放在了错误的地方
   - 封装性差
   - 违反了面向对象设计原则
   - 难以维护和理解
   - 增加了类之间的耦合

3. **典型示例**：
   ```
   // 重构前：方法访问另一个对象的数据过多
   class Order {
     getDiscountedPrice(customer) {
       // 这里大量使用 customer 数据
       if (customer.loyaltyYears > 5) {
         return this.price * customer.discountRate;
       }
       return this.price;
     }
   }

   // 重构后：方法移到更合适的类
   class Customer {
     getDiscountedPriceFor(price) {
       if (this.loyaltyYears > 5) {
         return price * this.discountRate;
       }
       return price;
     }
   }
   ```

4. **[[重构]]策略**：
   - [[Move Method]]：将方法移到更合适的类
   - [[Move Field]]：将字段移到更合适的类
   - [[Extract Method]]：先[[Extract Method|提取方法]]再移动

5. **判断准则**：
   - 观察方法主要操作哪个类的数据
   - 如果方法更多地使用其他类的数据，考虑[[Move Method|移动方法]]
   - 遵循"数据和使用数据的行为应该在一起"的原则

## 来源
- [[Martin Fowler]] — 《重构：改善既有代码的设计》
- [[代码异味]] — 重构指导书

## 相关
- [[代码异味]] — Feature Envy所属的异味类别
- [[重构]] — 解决方法
- [[封装性]] — 面向对象核心概念
- [[Move Method]] — 重构技巧
- [[高内聚]] — 设计原则