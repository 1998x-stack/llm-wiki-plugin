---
title: "Convergence of random variables"
source: "https://en.wikipedia.org/wiki/Convergence_of_random_variables"
author:
  - "[[Wikipedia]]"
published: 2002-04-28
created: 2026-04-16
description:
tags:
  - "clippings"
---
In [probability theory](https://en.wikipedia.org/wiki/Probability_theory "Probability theory"), there exist several different notions of **convergence of sequences of random variables**, including *convergence in probability*, *convergence in distribution*, and *almost sure convergence*. The different notions of convergence capture different properties about the sequence, with some notions of convergence being stronger than others. For example, convergence in distribution tells us about the limit [distribution](https://en.wikipedia.org/wiki/Probability_distribution "Probability distribution") of a sequence of random variables. This is a weaker notion than convergence in probability, which tells us about the value a random variable will take, rather than just the distribution. In [probability theory](https://en.wikipedia.org/wiki/Probability_theory "Probability theory"), there exist several different notions of **convergence of sequences of random variables**, including *convergence in probability*, *convergence in distribution*, and *almost sure convergence*. The different notions of convergence capture different properties about the sequence, with some notions of convergence being stronger than others. For example, convergence in distribution tells us about the limit [distribution](https://en.wikipedia.org/wiki/Probability_distribution "Probability distribution") of a sequence of random variables. This is a weaker notion than convergence in probability, which tells us about the value a random variable will take, rather than just the distribution. 在 [概率论](https://en.wikipedia.org/wiki/Probability_theory "Probability theory") 中，随机变量序列存在多种不同的收敛概念，包括依概率收敛、依分布收敛和几乎必然收敛。不同的收敛概念刻画了序列的不同性质，其中一些收敛概念的强度强于另一些。例如，依分布收敛揭示了随机变量序列的极限 [分布](https://en.wikipedia.org/wiki/Probability_distribution "Probability distribution") ，这是一种比依概率收敛更弱的概念；依概率收敛关注的是随机变量会取到的具体值，而非仅局限于其分布。

The concept is important in probability theory, and its applications to [statistics](https://en.wikipedia.org/wiki/Statistics "Statistics") and [stochastic processes](https://en.wikipedia.org/wiki/Stochastic_process "Stochastic process"). The same concepts are known in more general [mathematics](https://en.wikipedia.org/wiki/Mathematics "Mathematics") as **stochastic convergence** and they formalize the idea that certain properties of a sequence of essentially random or unpredictable events can sometimes be expected to settle down into a behavior that is essentially unchanging when items far enough into the sequence are studied. The different possible notions of convergence relate to how such a behavior can be characterized: two readily understood behaviors are that the sequence eventually takes a constant value, and that values in the sequence continue to change but can be described by an unchanging probability distribution. The concept is important in probability theory, and its applications to [statistics](https://en.wikipedia.org/wiki/Statistics "Statistics") and [stochastic processes](https://en.wikipedia.org/wiki/Stochastic_process "Stochastic process"). The same concepts are known in more general [mathematics](https://en.wikipedia.org/wiki/Mathematics "Mathematics") as **stochastic convergence** and they formalize the idea that certain properties of a sequence of essentially random or unpredictable events can sometimes be expected to settle down into a behavior that is essentially unchanging when items far enough into the sequence are studied. The different possible notions of convergence relate to how such a behavior can be characterized: two readily understood behaviors are that the sequence eventually takes a constant value, and that values in the sequence continue to change but can be described by an unchanging probability distribution. 这一概念在概率论中至关重要，也被应用于 [统计学](https://en.wikipedia.org/wiki/Statistics "Statistics") 与 [随机过程](https://en.wikipedia.org/wiki/Stochastic_process "Stochastic process") 中。在更广义的 [数学](https://en.wikipedia.org/wiki/Mathematics "Mathematics") 领域中，相同的概念被称为随机收敛，它将这样一种思想形式化：当研究序列中足够靠后的项时，一系列本质上随机或不可预测的事件，其某些性质有时有望稳定为一种基本不变的状态。不同的收敛概念对应着对这一状态的不同刻画方式：两种易于理解的状态分别是，序列最终取一个恒定值，以及序列中的值持续变化但可由一个不变的概率分布来描述。

## Background

## Background

背景\[[编辑](https://en.wikipedia.org/w/index.php?title=Convergence_of_random_variables&action=edit&section=1 "Edit section: Background")\]

"Stochastic convergence" formalizes the idea that a sequence of essentially random or unpredictable events can sometimes be expected to settle into a pattern. The pattern may for instance be "Stochastic convergence" formalizes the idea that a sequence of essentially random or unpredictable events can sometimes be expected to settle into a pattern. The pattern may for instance be “随机收敛”将这样一种理念形式化：一系列本质上随机或不可预测的事件，有时有望稳定成一种模式。这种模式可能例如是

- [Convergence](https://en.wikipedia.org/wiki/Limit_of_a_sequence "Limit of a sequence") in the classical sense to a fixed value, perhaps itself coming from a random event [Convergence](https://en.wikipedia.org/wiki/Limit_of_a_sequence "Limit of a sequence") in the classical sense to a fixed value, perhaps itself coming from a random event [收敛](https://en.wikipedia.org/wiki/Limit_of_a_sequence "Limit of a sequence") 在经典意义上指向一个固定值，而这个固定值本身或许源自某个随机事件
- An increasing similarity of outcomes to what a purely deterministic function would produce An increasing similarity of outcomes to what a purely deterministic function would produce 结果与纯确定性函数所产生结果的相似度不断提高
- An increasing preference towards a certain outcome An increasing preference towards a certain outcome 对某一结果的偏好不断增强
- An increasing "aversion" against straying far away from a certain outcome An increasing "aversion" against straying far away from a certain outcome 对偏离某一结果的倾向愈发强烈
- That the probability distribution describing the next outcome may grow increasingly similar to a certain distribution That the probability distribution describing the next outcome may grow increasingly similar to a certain distribution 描述下一个结果的概率分布可能会变得与某一特定分布愈发相似

Some less obvious, more theoretical patterns could be Some less obvious, more theoretical patterns could be 可能存在一些不太明显、更具理论性的模式

- That the series formed by calculating the [expected value](https://en.wikipedia.org/wiki/Expected_value "Expected value") of the outcome's distance from a particular value may converge to 0 That the series formed by calculating the [expected value](https://en.wikipedia.org/wiki/Expected_value "Expected value") of the outcome's distance from a particular value may converge to 0 由计算结果与某一特定值的距离的 [期望值](https://en.wikipedia.org/wiki/Expected_value "Expected value") 所构成的序列可能收敛于0
- That the variance of the [random variable](https://en.wikipedia.org/wiki/Random_variable "Random variable") describing the next event grows smaller and smaller.That the variance of the [random variable](https://en.wikipedia.org/wiki/Random_variable "Random variable") describing the next event grows smaller and smaller.描述下一个事件的 [随机变量](https://en.wikipedia.org/wiki/Random_variable "Random variable") 的方差变得越来越小。

These other types of patterns that may arise are reflected in the different types of stochastic convergence that have been studied. These other types of patterns that may arise are reflected in the different types of stochastic convergence that have been studied. 可能出现的其他类型模式体现在已被研究的不同类型随机收敛中。

While the above discussion has related to the convergence of a single series to a limiting value, the notion of the convergence of two series towards each other is also important, but this is easily handled by studying the sequence defined as either the difference or the ratio of the two series. While the above discussion has related to the convergence of a single series to a limiting value, the notion of the convergence of two series towards each other is also important, but this is easily handled by studying the sequence defined as either the difference or the ratio of the two series. 尽管上述讨论涉及单个序列向极限值的收敛，但两个序列相互收敛的概念同样重要，而通过研究由两个序列的差或比值所定义的序列，就能轻松处理这一情况。

For example, if the average of *n* For example, if the average of *n* 例如，若n的平均值 [independent](https://en.wikipedia.org/wiki/Independence_\(probability_theory\) "Independence (probability theory)") random variables [independent](https://en.wikipedia.org/wiki/Independence_\(probability_theory\) "Independence (probability theory)") random variables [独立](https://en.wikipedia.org/wiki/Independence_\(probability_theory\) "Independence (probability theory)") 随机变量 ${\displaystyle Y_{i},\ i=1,\dots ,n}$, all having the same finite [mean](https://en.wikipedia.org/wiki/Mean "Mean") and [variance](https://en.wikipedia.org/wiki/Variance "Variance"), is given by , all having the same finite [mean](https://en.wikipedia.org/wiki/Mean "Mean") and [variance](https://en.wikipedia.org/wiki/Variance "Variance"), is given by ，均具有相同的有限 [均值](https://en.wikipedia.org/wiki/Mean "Mean") 和 [方差](https://en.wikipedia.org/wiki/Variance "Variance") ，由下式给出

${\displaystyle X_{n}={\frac {1}{n}}\sum _{i=1}^{n}Y_{i}\,,}$

then as then as 那么当 ${\displaystyle n}$ tends to infinity, tends to infinity, 当 趋于无穷大时， ${\displaystyle X_{n}}$ converges *in probability* (see below) to the common [mean](https://en.wikipedia.org/wiki/Mean "Mean"), converges *in probability* (see below) to the common [mean](https://en.wikipedia.org/wiki/Mean "Mean"), 以概率收敛（见下文）至共同的 [均值](https://en.wikipedia.org/wiki/Mean "Mean") ${\displaystyle \mu }$, of the random variables , of the random variables ，随机变量的 ${\displaystyle Y_{i}}$. This result is known as the [weak law of large numbers](https://en.wikipedia.org/wiki/Weak_law_of_large_numbers "Weak law of large numbers"). Other forms of convergence are important in other useful theorems, including the [central limit theorem](https://en.wikipedia.org/wiki/Central_limit_theorem "Central limit theorem"). . This result is known as the [weak law of large numbers](https://en.wikipedia.org/wiki/Weak_law_of_large_numbers "Weak law of large numbers"). Other forms of convergence are important in other useful theorems, including the [central limit theorem](https://en.wikipedia.org/wiki/Central_limit_theorem "Central limit theorem"). . 这一结果被称为 [弱大数定律](https://en.wikipedia.org/wiki/Weak_law_of_large_numbers "Weak law of large numbers") 。其他形式的收敛性在其他有用的定理中也很重要，包括 [中心极限定理](https://en.wikipedia.org/wiki/Central_limit_theorem "Central limit theorem") 。

Throughout the following, we assume that Throughout the following, we assume that 在接下来的内容中，我们假设 ${\displaystyle (X_{n})}$ is a sequence of random variables, and is a sequence of random variables, and 是一列随机变量，且 ${\displaystyle X}$ is a random variable, and all of them are defined on the same [probability space](https://en.wikipedia.org/wiki/Probability_space "Probability space") is a random variable, and all of them are defined on the same [probability space](https://en.wikipedia.org/wiki/Probability_space "Probability space") 是一个随机变量，且所有这些变量都定义在同一个 [概率空间](https://en.wikipedia.org/wiki/Probability_space "Probability space") 上 ${\displaystyle (\Omega ,{\mathcal {F}},\mathbb {P} )}$. .

## Convergence in distribution

## Convergence in distribution

依分布收敛\[[编辑](https://en.wikipedia.org/w/index.php?title=Convergence_of_random_variables&action=edit&section=2 "Edit section: Convergence in distribution")\]

Loosely, with this mode of convergence, we increasingly expect to see the next outcome in a sequence of random experiments becoming better and better modeled by a given [probability distribution](https://en.wikipedia.org/wiki/Probability_distribution "Probability distribution"). More precisely, the distribution of the associated random variable in the sequence becomes arbitrarily close to a specified fixed distribution. Loosely, with this mode of convergence, we increasingly expect to see the next outcome in a sequence of random experiments becoming better and better modeled by a given [probability distribution](https://en.wikipedia.org/wiki/Probability_distribution "Probability distribution"). More precisely, the distribution of the associated random variable in the sequence becomes arbitrarily close to a specified fixed distribution.

Convergence in distribution is the weakest form of convergence typically discussed, since it is implied by all other types of convergence mentioned in this article. However, convergence in distribution is very frequently used in practice; most often it arises from application of the [central limit theorem](https://en.wikipedia.org/wiki/Central_limit_theorem "Central limit theorem"). Convergence in distribution is the weakest form of convergence typically discussed, since it is implied by all other types of convergence mentioned in this article. However, convergence in distribution is very frequently used in practice; most often it arises from application of the [central limit theorem](https://en.wikipedia.org/wiki/Central_limit_theorem "Central limit theorem").

### Definition

### Definition

A sequence A sequence ${\displaystyle X_{1},X_{2},\ldots }$ of real-valued [random variables](https://en.wikipedia.org/wiki/Random_variable "Random variable"), with [cumulative distribution functions](https://en.wikipedia.org/wiki/Cumulative_distribution_function "Cumulative distribution function") of real-valued [random variables](https://en.wikipedia.org/wiki/Random_variable "Random variable"), with [cumulative distribution functions](https://en.wikipedia.org/wiki/Cumulative_distribution_function "Cumulative distribution function") ${\displaystyle F_{1},F_{2},\ldots }$, is said to **converge in distribution**, or **converge weakly**, or **converge in law** to a random variable , is said to **converge in distribution**, or **converge weakly**, or **converge in law** to a random variable ${\displaystyle X}$ with [cumulative distribution function](https://en.wikipedia.org/wiki/Cumulative_distribution_function "Cumulative distribution function") with [cumulative distribution function](https://en.wikipedia.org/wiki/Cumulative_distribution_function "Cumulative distribution function") ${\displaystyle F}$ if if

${\displaystyle \lim _{n\to \infty }F_{n}(x)=F(x),}$

for every number for every number ${\displaystyle x\in \mathbb {R} }$ at which at which ${\displaystyle F}$ is [continuous](https://en.wikipedia.org/wiki/Continuous_function "Continuous function"). is [continuous](https://en.wikipedia.org/wiki/Continuous_function "Continuous function").

The requirement that only the continuity points of The requirement that only the continuity points of ${\displaystyle F}$ should be considered is essential. For example, if should be considered is essential. For example, if ${\displaystyle X_{n}}$ are distributed [uniformly](https://en.wikipedia.org/wiki/Uniform_distribution_\(continuous\) "Uniform distribution (continuous)") on intervals are distributed [uniformly](https://en.wikipedia.org/wiki/Uniform_distribution_\(continuous\) "Uniform distribution (continuous)") on intervals ${\displaystyle \left(0,{\frac {1}{n}}\right)}$, then this sequence converges in distribution to the [degenerate](https://en.wikipedia.org/wiki/Degenerate_distribution "Degenerate distribution") random variable , then this sequence converges in distribution to the [degenerate](https://en.wikipedia.org/wiki/Degenerate_distribution "Degenerate distribution") random variable ${\displaystyle X=0}$. Indeed, . Indeed, ${\displaystyle F_{n}(x)=0}$ [for all for all](https://en.wikipedia.org/wiki/Existential_quantification "Existential quantification") ${\displaystyle n}$ when when ${\displaystyle x\leq 0}$, and , and ${\displaystyle F_{n}(x)=1}$ for all for all ${\displaystyle x\geq {\frac {1}{n}}}$ when when ${\displaystyle n>0}$. However, for this limiting random variable . However, for this limiting random variable ${\displaystyle F(0)=1}$, even though , even though ${\displaystyle F_{n}(0)=0}$ for all for all ${\displaystyle n}$. Thus the convergence of cdfs fails at the point . Thus the convergence of cdfs fails at the point ${\displaystyle x=0}$ where where ${\displaystyle F}$ is discontinuous. is discontinuous. 是不连续的。

Convergence in distribution may be denoted as Convergence in distribution may be denoted as 依分布收敛可表示为

| ${\displaystyle {\begin{aligned}{}&X_{n}\ \xrightarrow {d} \ X,\ \ X_{n}\ \xrightarrow {\mathcal {D}} \ X,\ \ X_{n}\ \xrightarrow {\mathcal {L}} \ X,\ \ X_{n}\ \xrightarrow {d} \ {\mathcal {L}}_{X},\\&X_{n}\rightsquigarrow X,\ \ X_{n}\Rightarrow X,\ \ {\mathcal {L}}(X_{n})\to {\mathcal {L}}(X),\\\end{aligned}}}$ |  | 1 1 |
| --- | --- | --- |

where where 其中 ${\displaystyle \scriptstyle {\mathcal {L}}_{X}}$ is the law (probability distribution) of is the law (probability distribution) of 是 的分布律（概率分布） ${\displaystyle X}$. For example, if . For example, if 。例如，如果 ${\displaystyle X}$ is standard normal we can write is standard normal we can write 若 服从标准正态分布，我们可以写作 ${\displaystyle X_{n}\,{\xrightarrow {d}}\,{\mathcal {N}}(0,\,1)}$. .

For [random vectors](https://en.wikipedia.org/wiki/Random_vector "Random vector") For [random vectors](https://en.wikipedia.org/wiki/Random_vector "Random vector") 对于 [随机向量](https://en.wikipedia.org/wiki/Random_vector "Random vector") ${\displaystyle \left\{X_{1},X_{2},\dots \right\}\subset \mathbb {R} ^{k}}$ the convergence in distribution is defined similarly. We say that this sequence **converges in distribution** to a random the convergence in distribution is defined similarly. We say that this sequence **converges in distribution** to a random 分布收敛的定义类似。我们称该序列依分布收敛于一个随机 ${\displaystyle k}$ -vector \-vector \-向量 ${\displaystyle X}$ if if 如果

${\displaystyle \lim _{n\to \infty }\mathbb {P} (X_{n}\in A)=\mathbb {P} (X\in A)}$

for every for every 对于每一个 ${\displaystyle A\subset \mathbb {R} ^{k}}$ which is a [continuity set](https://en.wikipedia.org/wiki/Continuity_set "Continuity set") of which is a [continuity set](https://en.wikipedia.org/wiki/Continuity_set "Continuity set") of 是 [连续集](https://en.wikipedia.org/wiki/Continuity_set "Continuity set") ${\displaystyle X}$. .

The definition of convergence in distribution may be extended from random vectors to more general [random elements](https://en.wikipedia.org/wiki/Random_element "Random element") in arbitrary [metric spaces](https://en.wikipedia.org/wiki/Metric_space "Metric space"), and even to the “random variables” which are not measurable — a situation which occurs for example in the study of [empirical processes](https://en.wikipedia.org/wiki/Empirical_process "Empirical process"). This is the “weak convergence of laws without laws being defined” — except asymptotically.[^1] The definition of convergence in distribution may be extended from random vectors to more general [random elements](https://en.wikipedia.org/wiki/Random_element "Random element") in arbitrary [metric spaces](https://en.wikipedia.org/wiki/Metric_space "Metric space"), and even to the “random variables” which are not measurable — a situation which occurs for example in the study of [empirical processes](https://en.wikipedia.org/wiki/Empirical_process "Empirical process"). This is the “weak convergence of laws without laws being defined” — except asymptotically.[^1] 依分布收敛的定义可从随机向量推广至任意 [随机元](https://en.wikipedia.org/wiki/Random_element "Random element") ，甚至推广至不可测的“随机变量”——这种情况在 [经验过程](https://en.wikipedia.org/wiki/Empirical_process "Empirical process") 的研究中便会出现。这便是“无需定义定律的弱收敛”——仅在渐近意义下成立。 [\[1\]](#cite_note-1)

In this case the term **weak convergence** is preferable (see [weak convergence of measures](https://en.wikipedia.org/wiki/Weak_convergence_of_measures "Weak convergence of measures")), and we say that a sequence of random elements In this case the term **weak convergence** is preferable (see [weak convergence of measures](https://en.wikipedia.org/wiki/Weak_convergence_of_measures "Weak convergence of measures")), and we say that a sequence of random elements 在这种情况下，术语\*\*弱收敛\*\*更为可取（参见 [测度的弱收敛](https://en.wikipedia.org/wiki/Weak_convergence_of_measures "Weak convergence of measures") ），我们称一列随机元素 ${\displaystyle (X_{n})_{n}}$ converges weakly to converges weakly to 弱收敛于 ${\displaystyle X}$ (denoted as (denoted as （记为 ${\displaystyle X_{n}\Rightarrow X}$) if ) if ) 当且仅当

${\displaystyle \mathbb {E} ^{*}h(X_{n})\to \mathbb {E} \,h(X)}$

for all continuous bounded functions for all continuous bounded functions 对所有连续有界函数 ${\displaystyle h}$.[^2] Here .[^2] Here 。 [\[2\]](#cite_note-2) 这里 ${\displaystyle E^{*}}$ denotes the *outer expectation*, that is the expectation of a “smallest measurable function denotes the *outer expectation*, that is the expectation of a “smallest measurable function 表示外期望，即“最小可测函数”的期望 ${\displaystyle g}$ that dominates that dominates ${\displaystyle h(X_{n})}$ ”. ”.

### Properties

### Properties

- Since Since ${\displaystyle F(a)=\mathbb {P} (X\leq a)}$, the convergence in distribution means that the probability for , the convergence in distribution means that the probability for ${\displaystyle X_{n}}$ to be in a given range is approximately equal to the probability that the value of to be in a given range is approximately equal to the probability that the value of ${\displaystyle X}$ is in that range, provided is in that range, provided ${\displaystyle n}$ is [sufficiently large](https://en.wikipedia.org/wiki/Sufficiently_large "Sufficiently large"). is [sufficiently large](https://en.wikipedia.org/wiki/Sufficiently_large "Sufficiently large").
- In general, convergence in distribution does not imply that the sequence of corresponding [probability density functions](https://en.wikipedia.org/wiki/Probability_density_function "Probability density function") will also converge. As an example one may consider random variables with densities In general, convergence in distribution does not imply that the sequence of corresponding [probability density functions](https://en.wikipedia.org/wiki/Probability_density_function "Probability density function") will also converge. As an example one may consider random variables with densities ${\displaystyle f_{n}(x)=(1+\cos(2\pi nx))\mathbf {1} _{(0,1)}}$. These random variables converge in distribution to a uniform . These random variables converge in distribution to a uniform ${\displaystyle U(0,1)}$, whereas their densities do not converge at all.[^3], whereas their densities do not converge at all.[^3]
	- However, according to *Scheffé’s theorem*, convergence of the [probability density functions](https://en.wikipedia.org/wiki/Probability_density_function "Probability density function") implies convergence in distribution.[^4] However, according to *Scheffé’s theorem*, convergence of the [probability density functions](https://en.wikipedia.org/wiki/Probability_density_function "Probability density function") implies convergence in distribution.[^4]
- The [portmanteau lemma](https://en.wikipedia.org/wiki/Portmanteau_lemma "Portmanteau lemma") provides several equivalent definitions of convergence in distribution. Although these definitions are less intuitive, they are used to prove a number of statistical theorems. The lemma states that The [portmanteau lemma](https://en.wikipedia.org/wiki/Portmanteau_lemma "Portmanteau lemma") provides several equivalent definitions of convergence in distribution. Although these definitions are less intuitive, they are used to prove a number of statistical theorems. The lemma states that ${\displaystyle (X_{n})_{n}}$ converges in distribution to converges in distribution to ${\displaystyle X}$ if and only if any of the following statements are true:[^5] if and only if any of the following statements are true:[^5]
	- ${\displaystyle \mathbb {P} (X_{n}\leq x)\to \mathbb {P} (X\leq x)}$ for all continuity points of for all continuity points of ${\displaystyle x\mapsto \mathbb {P} (X\leq x)}$;;
		- ${\displaystyle \mathbb {E} f(X_{n})\to \mathbb {E} f(X)}$ for all [bounded](https://en.wikipedia.org/wiki/Bounded_function "Bounded function"), [continuous functions](https://en.wikipedia.org/wiki/Continuous_function "Continuous function") for all [bounded](https://en.wikipedia.org/wiki/Bounded_function "Bounded function"), [continuous functions](https://en.wikipedia.org/wiki/Continuous_function "Continuous function") ${\displaystyle f}$ (where (where ${\displaystyle \mathbb {E} }$ denotes the [expected value](https://en.wikipedia.org/wiki/Expected_value "Expected value") operator); denotes the [expected value](https://en.wikipedia.org/wiki/Expected_value "Expected value") operator);
		- ${\displaystyle \mathbb {E} f(X_{n})\to \mathbb {E} f(X)}$ for all bounded, [Lipschitz functions](https://en.wikipedia.org/wiki/Lipschitz_function "Lipschitz function") for all bounded, [Lipschitz functions](https://en.wikipedia.org/wiki/Lipschitz_function "Lipschitz function") ${\displaystyle f}$;;
		- ${\displaystyle \lim \inf \mathbb {E} f(X_{n})\geq \mathbb {E} f(X)}$ for all nonnegative, continuous functions for all nonnegative, continuous functions ${\displaystyle f}$;;
		- ${\displaystyle \lim \inf \mathbb {P} (X_{n}\in G)\geq \mathbb {P} (X\in G)}$ for every [open set](https://en.wikipedia.org/wiki/Open_set "Open set") for every [open set](https://en.wikipedia.org/wiki/Open_set "Open set") ${\displaystyle G}$;;
		- ${\displaystyle \lim \sup \mathbb {P} (X_{n}\in F)\leq \mathbb {P} (X\in F)}$ for every [closed set](https://en.wikipedia.org/wiki/Closed_set "Closed set") for every [closed set](https://en.wikipedia.org/wiki/Closed_set "Closed set") ${\displaystyle F}$;;
		- ${\displaystyle \mathbb {P} (X_{n}\in B)\to \mathbb {P} (X\in B)}$ for all [continuity sets](https://en.wikipedia.org/wiki/Continuity_set "Continuity set") for all [continuity sets](https://en.wikipedia.org/wiki/Continuity_set "Continuity set") ${\displaystyle B}$ of random variable of random variable ${\displaystyle X}$;;
		- ${\displaystyle \limsup \mathbb {E} f(X_{n})\leq \mathbb {E} f(X)}$ for every [upper semi-continuous](https://en.wikipedia.org/wiki/Upper_semi-continuous "Upper semi-continuous") function for every [upper semi-continuous](https://en.wikipedia.org/wiki/Upper_semi-continuous "Upper semi-continuous") function ${\displaystyle f}$ bounded above; bounded above;
		- ${\displaystyle \liminf \mathbb {E} f(X_{n})\geq \mathbb {E} f(X)}$ for every [lower semi-continuous](https://en.wikipedia.org/wiki/Lower_semi-continuous "Lower semi-continuous") function for every [lower semi-continuous](https://en.wikipedia.org/wiki/Lower_semi-continuous "Lower semi-continuous") function ${\displaystyle f}$ bounded below. bounded below.
- The [continuous mapping theorem](https://en.wikipedia.org/wiki/Continuous_mapping_theorem "Continuous mapping theorem") states that for a continuous function The [continuous mapping theorem](https://en.wikipedia.org/wiki/Continuous_mapping_theorem "Continuous mapping theorem") states that for a continuous function ${\displaystyle g}$, if the sequence , if the sequence ${\displaystyle (X_{n})_{n}}$ converges in distribution to converges in distribution to ${\displaystyle X}$, then , then ${\displaystyle (g(X_{n}))_{n}}$ converges in distribution to converges in distribution to ${\displaystyle g(X)}$. .
	- Note however that convergence in distribution of Note however that convergence in distribution of ${\displaystyle (X_{n})_{n}}$ to to ${\displaystyle X}$ and and ${\displaystyle (Y_{n})_{n}}$ to to ${\displaystyle Y}$ does in general *not* imply convergence in distribution of does in general *not* imply convergence in distribution of ${\displaystyle (X_{n}+Y_{n})_{n}}$ to to ${\displaystyle X+Y}$ or of or of ${\displaystyle (X_{n}Y_{n})_{n}}$ to to ${\displaystyle XY}$..
- [Lévy’s continuity theorem](https://en.wikipedia.org/wiki/L%C3%A9vy%E2%80%99s_continuity_theorem "Lévy’s continuity theorem"): The sequence [Lévy’s continuity theorem](https://en.wikipedia.org/wiki/L%C3%A9vy%E2%80%99s_continuity_theorem "Lévy’s continuity theorem"): The sequence ${\displaystyle (X_{n})_{n}}$ converges in distribution to converges in distribution to ${\displaystyle X}$ if and only if the sequence of corresponding [characteristic functions](https://en.wikipedia.org/wiki/Characteristic_function_\(probability_theory\) "Characteristic function (probability theory)") if and only if the sequence of corresponding [characteristic functions](https://en.wikipedia.org/wiki/Characteristic_function_\(probability_theory\) "Characteristic function (probability theory)") ${\displaystyle (\varphi _{n})_{n}}$ [converges pointwise](https://en.wikipedia.org/wiki/Pointwise_convergence "Pointwise convergence") to the characteristic function [converges pointwise](https://en.wikipedia.org/wiki/Pointwise_convergence "Pointwise convergence") to the characteristic function ${\displaystyle \varphi }$ of of ${\displaystyle X}$..
- Convergence in distribution is [metrizable](https://en.wikipedia.org/wiki/Metrizable "Metrizable") by the [Lévy–Prokhorov metric](https://en.wikipedia.org/wiki/L%C3%A9vy%E2%80%93Prokhorov_metric "Lévy–Prokhorov metric").Convergence in distribution is [metrizable](https://en.wikipedia.org/wiki/Metrizable "Metrizable") by the [Lévy–Prokhorov metric](https://en.wikipedia.org/wiki/L%C3%A9vy%E2%80%93Prokhorov_metric "Lévy–Prokhorov metric").
- A natural link to convergence in distribution is the [Skorokhod's representation theorem](https://en.wikipedia.org/wiki/Skorokhod%27s_representation_theorem "Skorokhod's representation theorem").A natural link to convergence in distribution is the [Skorokhod's representation theorem](https://en.wikipedia.org/wiki/Skorokhod%27s_representation_theorem "Skorokhod's representation theorem").

## Convergence in probability

## Convergence in probability

The basic idea behind this type of convergence is that the probability of an “unusual” outcome becomes smaller and smaller as the sequence progresses. The basic idea behind this type of convergence is that the probability of an “unusual” outcome becomes smaller and smaller as the sequence progresses.

The concept of convergence in probability is used very often in statistics. For example, an estimator is called [consistent](https://en.wikipedia.org/wiki/Consistent_estimator "Consistent estimator") if it converges in probability to the quantity being estimated. Convergence in probability is also the type of convergence established by the [weak law of large numbers](https://en.wikipedia.org/wiki/Weak_law_of_large_numbers "Weak law of large numbers"). The concept of convergence in probability is used very often in statistics. For example, an estimator is called [consistent](https://en.wikipedia.org/wiki/Consistent_estimator "Consistent estimator") if it converges in probability to the quantity being estimated. Convergence in probability is also the type of convergence established by the [weak law of large numbers](https://en.wikipedia.org/wiki/Weak_law_of_large_numbers "Weak law of large numbers").

### Definition

### Definition

定义\[[编辑](https://en.wikipedia.org/w/index.php?title=Convergence_of_random_variables&action=edit&section=6 "Edit section: Definition")\]

A sequence A sequence 一个序列 ${\displaystyle (X_{n})_{n}}$ of random variables **converges in probability** towards the random variable of random variables **converges in probability** towards the random variable ${\displaystyle X}$ if for all if for all ${\displaystyle \varepsilon >0}$

${\displaystyle \lim _{n\to \infty }\mathbb {P} {\big (}|X_{n}-X|>\varepsilon {\big )}=0.}$

More explicitly, let More explicitly, let ${\displaystyle P_{n}(\varepsilon )}$ be the probability that be the probability that ${\displaystyle X_{n}}$ is outside the ball of radius is outside the ball of radius 位于半径为 的球外 ${\displaystyle \varepsilon }$ centered at centered at 以 为中心 ${\displaystyle X}$. Then . Then 。然后 ${\displaystyle (X_{n})_{n}}$ is said to converge in probability to is said to converge in probability to 称 依概率收敛于 ${\displaystyle X}$ if for any if for any 若对于任意 ${\displaystyle \varepsilon >0}$ and any and any 以及任意 ${\displaystyle \delta >0}$ there exists a number there exists a number ${\displaystyle N}$ (which may depend on (which may depend on ${\displaystyle \varepsilon }$ and and ${\displaystyle \delta }$) such that for all ) such that for all ${\displaystyle n\geq N}$, , ${\displaystyle P_{n}(\varepsilon )\leq \delta }$ (the definition of limit). (the definition of limit).

Notice that for the condition to be satisfied, it is not possible that for each Notice that for the condition to be satisfied, it is not possible that for each ${\displaystyle n}$ the random variables the random variables ${\displaystyle X}$ and and ${\displaystyle (X_{n})_{n}}$ are independent (and thus convergence in probability is a condition on the joint cdf's, as opposed to convergence in distribution, which is a condition on the individual cdf's), unless are independent (and thus convergence in probability is a condition on the joint cdf's, as opposed to convergence in distribution, which is a condition on the individual cdf's), unless ${\displaystyle X}$ is deterministic like for the weak law of large numbers. At the same time, the case of a deterministic is deterministic like for the weak law of large numbers. At the same time, the case of a deterministic ${\displaystyle X}$ cannot, whenever the deterministic value is a discontinuity point (not isolated), be handled by convergence in distribution, where discontinuity points have to be explicitly excluded. cannot, whenever the deterministic value is a discontinuity point (not isolated), be handled by convergence in distribution, where discontinuity points have to be explicitly excluded.

Convergence in probability is denoted by adding the letter Convergence in probability is denoted by adding the letter ${\displaystyle p}$ over an arrow indicating convergence, or using the "plim" probability limit operator: over an arrow indicating convergence, or using the "plim" probability limit operator:

| ${\displaystyle X_{n}\ \xrightarrow {p} \ X,\ \ X_{n}\ \xrightarrow {P} \ X,\ \ {\underset {n\to \infty }{\operatorname {plim} }}\,X_{n}=X.}$ |  | 2 2 |
| --- | --- | --- |

For random elements For random elements ${\displaystyle (X_{n})_{n}}$ on a [separable metric space](https://en.wikipedia.org/wiki/Separable_metric_space "Separable metric space") on a [separable metric space](https://en.wikipedia.org/wiki/Separable_metric_space "Separable metric space") ${\displaystyle (S,d)}$, convergence in probability is defined similarly by [^6], convergence in probability is defined similarly by [^6]

${\displaystyle \forall \varepsilon >0,\mathbb {P} {\big (}d(X_{n},X)\geq \varepsilon {\big )}\to 0.}$

### Properties

### Properties

- Convergence in probability implies convergence in distribution.<sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propA2" title="Proofs of convergence of random variables">[proof]</a></sup> Convergence in probability implies convergence in distribution.<sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propA2" title="Proofs of convergence of random variables">[proof]</a></sup>
- In the opposite direction, convergence in distribution implies convergence in probability when the limiting random variable *X* is a constant.<sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB1" title="Proofs of convergence of random variables">[proof]</a></sup> In the opposite direction, convergence in distribution implies convergence in probability when the limiting random variable *X* is a constant.<sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB1" title="Proofs of convergence of random variables">[proof]</a></sup>
- Convergence in probability does not imply almost sure convergence.<sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propA1i" title="Proofs of convergence of random variables">[proof]</a></sup> Convergence in probability does not imply almost sure convergence.<sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propA1i" title="Proofs of convergence of random variables">[proof]</a></sup>
- The [continuous mapping theorem](https://en.wikipedia.org/wiki/Continuous_mapping_theorem "Continuous mapping theorem") states that for every continuous function The [continuous mapping theorem](https://en.wikipedia.org/wiki/Continuous_mapping_theorem "Continuous mapping theorem") states that for every continuous function ${\displaystyle g}$, if , if ${\textstyle X_{n}\xrightarrow {p} X}$, then also , then also ${\textstyle g(X_{n})\xrightarrow {p} g(X)}$..
- Convergence in probability defines a [topology](https://en.wikipedia.org/wiki/Topology "Topology") on the space of random variables over a fixed probability space. This topology is [metrizable](https://en.wikipedia.org/wiki/Metrizable "Metrizable") by the *[Ky Fan](https://en.wikipedia.org/wiki/Ky_Fan "Ky Fan") metric*:[^7] Convergence in probability defines a [topology](https://en.wikipedia.org/wiki/Topology "Topology") on the space of random variables over a fixed probability space. This topology is [metrizable](https://en.wikipedia.org/wiki/Metrizable "Metrizable") by the *[Ky Fan](https://en.wikipedia.org/wiki/Ky_Fan "Ky Fan") metric*:[^7] 
	$$
	{\displaystyle d(X,Y)=\inf \!{\big \{}\varepsilon >0:\ \mathbb {P} {\big (}|X-Y|>\varepsilon {\big )}\leq \varepsilon {\big \}}}
	$$
	 or alternately by this metric or alternately by this metric 
	$$
	{\displaystyle d(X,Y)=\mathbb {E} \left[\min(|X-Y|,1)\right].}
	$$

### Counterexamples

### Counterexamples

Not every sequence of random variables which converges to another random variable in distribution also converges in probability to that random variable. As an example, consider a sequence of standard normal random variables Not every sequence of random variables which converges to another random variable in distribution also converges in probability to that random variable. As an example, consider a sequence of standard normal random variables ${\displaystyle X_{n}}$ and a second sequence and a second sequence ${\displaystyle Y_{n}=(-1)^{n}X_{n}}$. Notice that the distribution of . Notice that the distribution of ${\displaystyle Y_{n}}$ is equal to the distribution of is equal to the distribution of ${\displaystyle X_{n}}$ for all for all ${\displaystyle n}$, but: , but: 
$$
{\displaystyle P(|X_{n}-Y_{n}|\geq \epsilon )=P(|X_{n}|\cdot |(1-(-1)^{n})|\geq \epsilon )}
$$

which does not converge to which does not converge to ${\displaystyle 0}$. So we do not have convergence in probability. . So we do not have convergence in probability.

## Almost sure convergence

## Almost sure convergence

This is the type of stochastic convergence that is most similar to [pointwise convergence](https://en.wikipedia.org/wiki/Pointwise_convergence "Pointwise convergence") known from elementary [real analysis](https://en.wikipedia.org/wiki/Real_analysis "Real analysis"). This is the type of stochastic convergence that is most similar to [pointwise convergence](https://en.wikipedia.org/wiki/Pointwise_convergence "Pointwise convergence") known from elementary [real analysis](https://en.wikipedia.org/wiki/Real_analysis "Real analysis").

### Definition

### Definition

To say that the sequence X <sub>n</sub> converges **almost surely** or **almost everywhere** or **with probability 1** or **strongly** towards To say that the sequence X <sub>n</sub> converges **almost surely** or **almost everywhere** or **with probability 1** or **strongly** towards ${\displaystyle X}$ means that means that 
$$
{\displaystyle \mathbb {P} \!\left(\lim _{n\to \infty }\!X_{n}=X\right)=1.}
$$

This means that the values of This means that the values of ${\displaystyle X_{n}}$ approach the value of approach the value of ${\displaystyle X}$, in the sense that events for which , in the sense that events for which ${\displaystyle X_{n}}$ does not converge to does not converge to ${\displaystyle X}$ have probability have probability ${\displaystyle 0}$ (see *[Almost surely](https://en.wikipedia.org/wiki/Almost_surely "Almost surely")*). Using the probability space (see *[Almost surely](https://en.wikipedia.org/wiki/Almost_surely "Almost surely")*). Using the probability space ${\displaystyle (\Omega ,{\mathcal {F}},\mathbb {P} )}$ and the concept of the random variable as a function from and the concept of the random variable as a function from ${\displaystyle \Omega }$ to to ${\displaystyle \mathbb {R} }$, this is equivalent to the statement , this is equivalent to the statement 
$$
{\displaystyle \mathbb {P} {\Bigl (}\omega \in \Omega :\lim _{n\to \infty }X_{n}(\omega )=X(\omega ){\Bigr )}=1.}
$$

Using the notion of the [limit superior of a sequence of sets](https://en.wikipedia.org/wiki/Limit_superior_and_limit_inferior#Special_case:_discrete_metric "Limit superior and limit inferior"), almost sure convergence can also be defined as follows: Using the notion of the [limit superior of a sequence of sets](https://en.wikipedia.org/wiki/Limit_superior_and_limit_inferior#Special_case:_discrete_metric "Limit superior and limit inferior"), almost sure convergence can also be defined as follows: 
$$
{\displaystyle \mathbb {P} {\Bigl (}\limsup _{n\to \infty }{\bigl \{}\omega \in \Omega :|X_{n}(\omega )-X(\omega )|>\varepsilon {\bigr \}}{\Bigr )}=0\quad {\text{for all}}\quad \varepsilon >0.}
$$

Almost sure convergence is often denoted by adding the letters *a.s.* over an arrow indicating convergence: Almost sure convergence is often denoted by adding the letters *a.s.* over an arrow indicating convergence:

| ${\displaystyle {\overset {}{X_{n}\,{\xrightarrow {\mathrm {a.s.} }}\,X.}}}$ |  | 3 3 |
| --- | --- | --- |

For generic [random elements](https://en.wikipedia.org/wiki/Random_element "Random element") For generic [random elements](https://en.wikipedia.org/wiki/Random_element "Random element") ${\displaystyle (X_{n})_{n}}$ on a [metric space](https://en.wikipedia.org/wiki/Metric_space "Metric space") on a [metric space](https://en.wikipedia.org/wiki/Metric_space "Metric space") ${\displaystyle (S,d)}$, convergence almost surely is defined similarly: , convergence almost surely is defined similarly: 
$$
{\displaystyle \mathbb {P} {\Bigl (}\omega \in \Omega \colon \,d{\big (}X_{n}(\omega ),X(\omega ){\big )}\,{\underset {n\to \infty }{\longrightarrow }}\,0{\Bigr )}=1}
$$

### Properties

### Properties

- Almost sure convergence implies convergence in probability (by [Fatou's lemma](https://en.wikipedia.org/wiki/Fatou%27s_lemma "Fatou's lemma")), and hence implies convergence in distribution. It is the notion of convergence used in the strong [law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers "Law of large numbers").Almost sure convergence implies convergence in probability (by [Fatou's lemma](https://en.wikipedia.org/wiki/Fatou%27s_lemma "Fatou's lemma")), and hence implies convergence in distribution. It is the notion of convergence used in the strong [law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers "Law of large numbers").
- The concept of almost sure convergence does not come from a [topology](https://en.wikipedia.org/wiki/Topology "Topology") on the space of random variables. This means there is no topology on the space of random variables such that the almost surely convergent sequences are exactly the converging sequences with respect to that topology. In particular, there is no metric of almost sure convergence.The concept of almost sure convergence does not come from a [topology](https://en.wikipedia.org/wiki/Topology "Topology") on the space of random variables. This means there is no topology on the space of random variables such that the almost surely convergent sequences are exactly the converging sequences with respect to that topology. In particular, there is no metric of almost sure convergence.

### Counterexamples

### Counterexamples

Consider a sequence Consider a sequence ${\displaystyle \{X_{n}\}}$ of independent random variables such that of independent random variables such that ${\displaystyle \textstyle \mathbb {P} (X_{n}=1)={\frac {1}{n}}}$ and and ${\displaystyle \textstyle \mathbb {P} (X_{n}=0)=1-{\frac {1}{n}}}$. For all . For all ${\displaystyle \varepsilon >0,}$ we have we have ${\displaystyle \textstyle \mathbb {P} (|X_{n}|\geq \varepsilon )={\frac {1}{n}},}$ which converges to 0. Hence which converges to 0. Hence ${\displaystyle X_{n}\to 0}$ in probability. in probability.

Since Since ${\displaystyle \textstyle \sum _{n\geq 1}\mathbb {P} (X_{n}=1)=+\infty }$ and the events and the events ${\displaystyle \{X_{n}=1\}}$ are independent, the [second Borel Cantelli Lemma](https://en.wikipedia.org/wiki/Borel%E2%80%93Cantelli_lemma#Converse-result "Borel–Cantelli lemma") ensures that are independent, the [second Borel Cantelli Lemma](https://en.wikipedia.org/wiki/Borel%E2%80%93Cantelli_lemma#Converse-result "Borel–Cantelli lemma") ensures that ${\displaystyle \textstyle \mathbb {P} (\limsup _{n}\{X_{n}=1\})=1.}$ Therefore, the sequence Therefore, the sequence ${\displaystyle \{X_{n}\}}$ does not converge to 0 almost everywhere (in fact, the set on which this sequence does not converge to 0 has probability 1). does not converge to 0 almost everywhere (in fact, the set on which this sequence does not converge to 0 has probability 1).

## Sure convergence or pointwise convergence

## Sure convergence or pointwise convergence

To say that the sequence of [random variables](https://en.wikipedia.org/wiki/Random_variables "Random variables") To say that the sequence of [random variables](https://en.wikipedia.org/wiki/Random_variables "Random variables") ${\displaystyle (X_{n})_{n}}$ defined over the same [probability space](https://en.wikipedia.org/wiki/Probability_space "Probability space") (i.e., a [random process](https://en.wikipedia.org/wiki/Random_process "Random process")) converges **surely** or **everywhere** or **pointwise** towards *X* means defined over the same [probability space](https://en.wikipedia.org/wiki/Probability_space "Probability space") (i.e., a [random process](https://en.wikipedia.org/wiki/Random_process "Random process")) converges **surely** or **everywhere** or **pointwise** towards *X* means

$$
{\displaystyle \forall \omega \in \Omega \colon \ \lim _{n\to \infty }X_{n}(\omega )=X(\omega ),}
$$

where where ${\displaystyle \Omega }$ is the [sample space](https://en.wikipedia.org/wiki/Sample_space "Sample space") of the underlying [probability space](https://en.wikipedia.org/wiki/Probability_space "Probability space") over which the random variables are defined. is the [sample space](https://en.wikipedia.org/wiki/Sample_space "Sample space") of the underlying [probability space](https://en.wikipedia.org/wiki/Probability_space "Probability space") over which the random variables are defined.

This is the notion of [pointwise convergence](https://en.wikipedia.org/wiki/Pointwise_convergence "Pointwise convergence") of a sequence of functions extended to a sequence of [random variables](https://en.wikipedia.org/wiki/Random_variables "Random variables"). (Note that random variables themselves are functions). This is the notion of [pointwise convergence](https://en.wikipedia.org/wiki/Pointwise_convergence "Pointwise convergence") of a sequence of functions extended to a sequence of [random variables](https://en.wikipedia.org/wiki/Random_variables "Random variables"). (Note that random variables themselves are functions).

$$
{\displaystyle \left\{\omega \in \Omega :\lim _{n\to \infty }X_{n}(\omega )=X(\omega )\right\}=\Omega .}
$$

Sure convergence of a random variable implies all the other kinds of convergence stated above, but there is no payoff in [probability theory](https://en.wikipedia.org/wiki/Probability_theory "Probability theory") by using sure convergence compared to using almost sure convergence. The difference between the two only exists on sets with probability zero. This is why the concept of sure convergence of random variables is very rarely used. Sure convergence of a random variable implies all the other kinds of convergence stated above, but there is no payoff in [probability theory](https://en.wikipedia.org/wiki/Probability_theory "Probability theory") by using sure convergence compared to using almost sure convergence. The difference between the two only exists on sets with probability zero. This is why the concept of sure convergence of random variables is very rarely used.

## Convergence in mean

## Convergence in mean

Given a real number Given a real number ${\displaystyle r\geq 1}$, we say that the sequence , we say that the sequence ${\displaystyle (X_{n})_{n}}$ converges converges **in the in the ${\displaystyle r}$ -th mean \-th mean** (or **in the [*L <sup>r</sup>* -norm](https://en.wikipedia.org/wiki/Lp_space "Lp space")**) towards the random variable (or **in the [*L <sup>r</sup>* -norm](https://en.wikipedia.org/wiki/Lp_space "Lp space")**) towards the random variable ${\displaystyle X}$, if the , if the ${\displaystyle r}$ -th [absolute moments](https://en.wikipedia.org/wiki/Moment_\(mathematics\) "Moment (mathematics)") \-th [absolute moments](https://en.wikipedia.org/wiki/Moment_\(mathematics\) "Moment (mathematics)") ${\displaystyle \mathbb {E} (|X_{n}|^{r})}$ and and ${\displaystyle \mathbb {E} (|X|^{r})}$ of X <sub>n</sub> and of X <sub>n</sub> and ${\displaystyle X}$ exist, and exist, and

${\displaystyle \lim _{n\to \infty }\mathbb {E} \left(|X_{n}-X|^{r}\right)=0,}$

where the operator where the operator ${\displaystyle \mathbb {E} }$ denotes the [expected value](https://en.wikipedia.org/wiki/Expected_value "Expected value"). Convergence in denotes the [expected value](https://en.wikipedia.org/wiki/Expected_value "Expected value"). Convergence in ${\displaystyle r}$ -th mean tells us that the expectation of the \-th mean tells us that the expectation of the ${\displaystyle r}$ -th power of the difference between \-th power of the difference between ${\displaystyle X_{n}}$ and and ${\displaystyle X}$ converges to zero. converges to zero.

This type of convergence is often denoted by adding the letter This type of convergence is often denoted by adding the letter ${\displaystyle L^{r}}$ over an arrow indicating convergence: over an arrow indicating convergence:

| ${\displaystyle {\overset {}{X_{n}\,{\xrightarrow {L^{r}}}\,X.}}}$ |  | 4 4 |
| --- | --- | --- |

The most important cases of convergence in The most important cases of convergence in ${\displaystyle r}$ -th mean are: \-th mean are:

- When When ${\displaystyle X_{n}}$ converges in converges in ${\displaystyle r}$ -th mean to \-th mean to ${\displaystyle X}$ for for ${\displaystyle r=1}$, we say that , we say that ${\displaystyle X_{n}}$ converges **in mean** to converges **in mean** to ${\displaystyle X}$..
- When When ${\displaystyle X_{n}}$ converges in converges in ${\displaystyle r}$ -th mean to \-th mean to ${\displaystyle X}$ for for ${\displaystyle r=2}$, we say that , we say that ${\displaystyle X_{n}}$ converges **in mean square** (or **in quadratic mean**) to converges **in mean square** (or **in quadratic mean**) to ${\displaystyle X}$..

Convergence in the Convergence in the ${\displaystyle r}$ -th mean, for \-th mean, for ${\displaystyle r\geq 1}$, implies convergence in probability (by [Markov's inequality](https://en.wikipedia.org/wiki/Markov%27s_inequality "Markov's inequality")). Furthermore, if , implies convergence in probability (by [Markov's inequality](https://en.wikipedia.org/wiki/Markov%27s_inequality "Markov's inequality")). Furthermore, if ${\displaystyle r>s\geq 1}$, convergence in , convergence in ${\displaystyle r}$ -th mean implies convergence in \-th mean implies convergence in ${\displaystyle s}$ -th mean. Hence, convergence in mean square implies convergence in mean. \-th mean. Hence, convergence in mean square implies convergence in mean.

Additionally, Additionally,

${\displaystyle {\overset {}{X_{n}\xrightarrow {L^{r}} X}}\quad \Rightarrow \quad \lim _{n\to \infty }\mathbb {E} [|X_{n}|^{r}]=\mathbb {E} [|X|^{r}].}$

The converse is not necessarily true, however it is true if The converse is not necessarily true, however it is true if ${\displaystyle {\overset {}{X_{n}\,\xrightarrow {p} \,X}}}$ (by a more general version of [Scheffé's lemma](https://en.wikipedia.org/wiki/Scheff%C3%A9%27s_lemma "Scheffé's lemma")). (by a more general version of [Scheffé's lemma](https://en.wikipedia.org/wiki/Scheff%C3%A9%27s_lemma "Scheffé's lemma")).

## Properties

## Properties

Provided the probability space is [complete](https://en.wikipedia.org/wiki/Complete_measure "Complete measure"): Provided the probability space is [complete](https://en.wikipedia.org/wiki/Complete_measure "Complete measure"):

- If If ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{p}}}\ X}$ and and ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{p}}}\ Y}$, then , then ${\displaystyle X=Y}$ [almost surely](https://en.wikipedia.org/wiki/Almost_surely "Almost surely").[almost surely](https://en.wikipedia.org/wiki/Almost_surely "Almost surely").
- If If ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{\text{a.s.}}}}\ X}$ and and ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{\text{a.s.}}}}\ Y}$, then , then ${\displaystyle X=Y}$ almost surely. almost surely.
- If If ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{L^{r}}}}\ X}$ and and ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{L^{r}}}}\ Y}$, then , then ${\displaystyle X=Y}$ almost surely. almost surely.
- If If ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{p}}}\ X}$ and and ${\displaystyle Y_{n}\ {\xrightarrow {\overset {}{p}}}\ Y}$, then , then ${\displaystyle aX_{n}+bY_{n}\ {\xrightarrow {\overset {}{p}}}\ aX+bY}$ (for any real numbers (for any real numbers ${\displaystyle a}$ and and ${\displaystyle b}$) and ) and ${\displaystyle X_{n}Y_{n}{\xrightarrow {\overset {}{p}}}\ XY}$..
- If If ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{\text{a.s.}}}}\ X}$ and and ${\displaystyle Y_{n}\ {\xrightarrow {\overset {}{\text{a.s.}}}}\ Y}$, then , then ${\displaystyle aX_{n}+bY_{n}\ {\xrightarrow {\overset {}{\text{a.s.}}}}\ aX+bY}$ (for any real numbers (for any real numbers ${\displaystyle a}$ and and ${\displaystyle b}$ and and ${\displaystyle X_{n}Y_{n}{\xrightarrow {\overset {}{\text{a.s.}}}}\ XY}$..
- If If ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{L^{r}}}}\ X}$ and and ${\displaystyle Y_{n}\ {\xrightarrow {\overset {}{L^{r}}}}\ Y}$, then , then ${\displaystyle aX_{n}+bY_{n}\ {\xrightarrow {\overset {}{L^{r}}}}\ aX+bY}$ (for any real numbers (for any real numbers ${\displaystyle a}$ and and ${\displaystyle b}$).).
- None of the above statements are true for convergence in distribution.None of the above statements are true for convergence in distribution.

The chain of implications between the various notions of convergence are noted in their respective sections. They are, using the arrow notation: The chain of implications between the various notions of convergence are noted in their respective sections. They are, using the arrow notation:

${\displaystyle {\begin{matrix}{\xrightarrow {\overset {}{L^{s}}}}&{\underset {s>r\geq 1}{\Rightarrow }}&{\xrightarrow {\overset {}{L^{r}}}}&&\\&&\Downarrow &&\\{\xrightarrow {\text{a.s.}}}&\Rightarrow &{\xrightarrow {p}}&\Rightarrow &{\xrightarrow {d}}\end{matrix}}}$

These properties, together with a number of other special cases, are summarized in the following list: These properties, together with a number of other special cases, are summarized in the following list:

- Almost sure convergence implies convergence in probability:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propA1" title="Proofs of convergence of random variables">[proof]</a></sup> Almost sure convergence implies convergence in probability:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propA1" title="Proofs of convergence of random variables">[proof]</a></sup>
	${\displaystyle X_{n}\ {\xrightarrow {\text{a.s.}}}\ X\quad \Rightarrow \quad X_{n}\ {\xrightarrow {\overset {}{p}}}\ X}$
- Convergence in probability implies there exists a sub-sequence Convergence in probability implies there exists a sub-sequence ${\displaystyle (n_{k})}$ which almost surely converges:[^9] which almost surely converges:[^9]
	${\displaystyle X_{n}\ \xrightarrow {\overset {}{p}} \ X\quad \Rightarrow \quad X_{n_{k}}\ \xrightarrow {\text{a.s.}} \ X}$
- Convergence in probability implies convergence in distribution:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propA2" title="Proofs of convergence of random variables">[proof]</a></sup> Convergence in probability implies convergence in distribution:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propA2" title="Proofs of convergence of random variables">[proof]</a></sup>
	${\displaystyle X_{n}\ {\xrightarrow {\overset {}{p}}}\ X\quad \Rightarrow \quad X_{n}\ {\xrightarrow {\overset {}{d}}}\ X}$
- Convergence in Convergence in ${\displaystyle r}$ -th order mean implies convergence in probability: \-th order mean implies convergence in probability:
	${\displaystyle X_{n}\ {\xrightarrow {\overset {}{L^{r}}}}\ X\quad \Rightarrow \quad X_{n}\ {\xrightarrow {\overset {}{p}}}\ X}$
- Convergence in Convergence in ${\displaystyle r}$ -th order mean implies convergence in lower order mean, assuming that both orders are greater than or equal to one: \-th order mean implies convergence in lower order mean, assuming that both orders are greater than or equal to one:
	${\displaystyle X_{n}\ {\xrightarrow {\overset {}{L^{r}}}}\ X\quad \Rightarrow \quad X_{n}\ {\xrightarrow {\overset {}{L^{s}}}}\ X,}$ provided provided ${\displaystyle r\geq s\geq 1}$..
- If If ${\displaystyle X_{n}}$ converges in distribution to a constant converges in distribution to a constant ${\displaystyle c}$, then , then ${\displaystyle X_{n}}$ converges in probability to converges in probability to ${\displaystyle c}$:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB1" title="Proofs of convergence of random variables">[proof]</a></sup>:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB1" title="Proofs of convergence of random variables">[proof]</a></sup>
	${\displaystyle X_{n}\ {\xrightarrow {\overset {}{d}}}\ c\quad \Rightarrow \quad X_{n}\ {\xrightarrow {\overset {}{p}}}\ c,}$ provided provided ${\displaystyle c}$ is a constant. is a constant.
- If If ${\displaystyle X_{n}}$ converges in distribution to converges in distribution to ${\displaystyle X}$ and the difference between and the difference between ${\displaystyle X_{n}}$ and and ${\displaystyle Y_{n}}$ converges in probability to zero, then converges in probability to zero, then ${\displaystyle Y_{n}}$ also converges in distribution to also converges in distribution to ${\displaystyle X}$:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB2" title="Proofs of convergence of random variables">[proof]</a></sup>:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB2" title="Proofs of convergence of random variables">[proof]</a></sup>
	${\displaystyle X_{n}\ {\xrightarrow {\overset {}{d}}}\ X,\ \ |X_{n}-Y_{n}|\ {\xrightarrow {\overset {}{p}}}\ 0\ \quad \Rightarrow \quad Y_{n}\ {\xrightarrow {\overset {}{d}}}\ X}$
- If If ${\displaystyle X_{n}}$ converges in distribution to converges in distribution to ${\displaystyle X}$ and ' and ' ${\displaystyle Y_{n}}$ converges in distribution to a constant converges in distribution to a constant ${\displaystyle c}$, then the joint vector , then the joint vector ${\displaystyle (X_{n},Y_{n})}$ converges in distribution to converges in distribution to ${\displaystyle (X,c)}$:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB3" title="Proofs of convergence of random variables">[proof]</a></sup>:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB3" title="Proofs of convergence of random variables">[proof]</a></sup>
	${\displaystyle X_{n}\ {\xrightarrow {\overset {}{d}}}\ X,\ \ Y_{n}\ {\xrightarrow {\overset {}{d}}}\ c\ \quad \Rightarrow \quad (X_{n},Y_{n})\ {\xrightarrow {\overset {}{d}}}\ (X,c)}$ provided *c* is a constant.provided *c* is a constant.
	Note that the condition that Note that the condition that ${\displaystyle Y_{n}}$ converges to a constant is important, if it were to converge to a random variable converges to a constant is important, if it were to converge to a random variable ${\displaystyle Y}$ then we wouldn't be able to conclude that then we wouldn't be able to conclude that ${\displaystyle (X_{n},Y_{n})}$ converges to converges to ⁠ ⁠ ${\displaystyle (X,Y)}$ ⁠ ⁠..
- If If ${\displaystyle X_{n}}$ converges in probability to converges in probability to ${\displaystyle X}$ and and ${\displaystyle Y_{n}}$ converges in probability to converges in probability to ${\displaystyle Y}$, then the joint vector , then the joint vector ${\displaystyle (X_{n},Y_{n})}$ converges in probability to converges in probability to ${\displaystyle (X,Y)}$:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB4" title="Proofs of convergence of random variables">[proof]</a></sup>:[^8] <sup><a href="https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables#propB4" title="Proofs of convergence of random variables">[proof]</a></sup>
	${\displaystyle X_{n}\ {\xrightarrow {\overset {}{p}}}\ X,\ \ Y_{n}\ {\xrightarrow {\overset {}{p}}}\ Y\ \quad \Rightarrow \quad (X_{n},Y_{n})\ {\xrightarrow {\overset {}{p}}}\ (X,Y)}$
- If If ${\displaystyle X_{n}}$ converges in probability to converges in probability to ${\displaystyle X}$, and if , and if ${\displaystyle \mathbb {P} (|X_{n}|\leq b)=1}$ for all for all ${\displaystyle n}$ and some and some ${\displaystyle b}$, then , then ${\displaystyle X_{n}}$ converges in converges in ${\displaystyle r}$ th mean to th mean to ${\displaystyle X}$ for all for all ${\displaystyle r\geq 1}$. In other words, if . In other words, if ${\displaystyle X_{n}}$ converges in probability to converges in probability to ${\displaystyle X}$ and all random variables and all random variables ${\displaystyle X_{n}}$ are almost surely bounded above and below, then are almost surely bounded above and below, then ${\displaystyle X_{n}}$ converges to converges to ${\displaystyle X}$ also in any also in any ${\displaystyle r}$ th mean.[^10] th mean.[^10]
- **Almost sure representation**. Usually, convergence in distribution does not imply convergence almost surely. However, for a given sequence **Almost sure representation**. Usually, convergence in distribution does not imply convergence almost surely. However, for a given sequence ${\displaystyle (X_{n})_{n}}$ which converges in distribution to which converges in distribution to ${\displaystyle X_{0}}$ it is always possible to find a new probability space it is always possible to find a new probability space ${\displaystyle (\Omega ,F,\mathbb {P} )}$ and random variables and random variables ${\displaystyle (Y_{n})_{n}}$ defined on it such that defined on it such that ${\displaystyle Y_{n}}$ is equal in distribution to is equal in distribution to ${\displaystyle X_{n}}$ for each for each ${\displaystyle n\geq 0}$, and , and ${\displaystyle Y_{n}}$ converges to converges to ${\displaystyle Y_{0}}$ almost surely.[^11] [^12] almost surely.[^11] [^12]
- If for all If for all ${\displaystyle \varepsilon >0}$, ,
	${\displaystyle \sum _{n}\mathbb {P} \left(|X_{n}-X|>\varepsilon \right)<\infty ,}$
	then we say that then we say that ${\displaystyle X_{n}}$ *converges almost completely*, or *almost in probability* towards *converges almost completely*, or *almost in probability* towards ${\displaystyle X}$. When . When ${\displaystyle X_{n}}$ converges almost completely towards converges almost completely towards ${\displaystyle X}$ then it also converges almost surely to then it also converges almost surely to ${\displaystyle X}$. In other words, if . In other words, if ${\displaystyle X_{n}}$ converges in probability to converges in probability to ${\displaystyle X}$ sufficiently quickly (i.e. the above sequence of tail probabilities is summable for all sufficiently quickly (i.e. the above sequence of tail probabilities is summable for all ${\displaystyle \varepsilon >0}$), then ), then ${\displaystyle X_{n}}$ also converges almost surely to also converges almost surely to ${\displaystyle X}$. This is a direct implication from the [Borel–Cantelli lemma](https://en.wikipedia.org/wiki/Borel%E2%80%93Cantelli_lemma "Borel–Cantelli lemma").. This is a direct implication from the [Borel–Cantelli lemma](https://en.wikipedia.org/wiki/Borel%E2%80%93Cantelli_lemma "Borel–Cantelli lemma").
- If If ${\displaystyle S_{n}}$ is a sum of is a sum of ${\displaystyle n}$ real independent random variables: real independent random variables:
	${\displaystyle S_{n}=X_{1}+\cdots +X_{n}\,}$
	then then ${\displaystyle S_{n}}$ converges almost surely if and only if converges almost surely if and only if ${\displaystyle S_{n}}$ converges in probability. The proof can be found in Page 126 (Theorem 5.3.4) of the book by [Kai Lai Chung](https://en.wikipedia.org/wiki/Kai_Lai_Chung "Kai Lai Chung").[^13] converges in probability. The proof can be found in Page 126 (Theorem 5.3.4) of the book by [Kai Lai Chung](https://en.wikipedia.org/wiki/Kai_Lai_Chung "Kai Lai Chung").[^13]
	However, for a sequence of mutually independent random variables, convergence in probability does not imply almost sure convergence.[^14] However, for a sequence of mutually independent random variables, convergence in probability does not imply almost sure convergence.[^14]
- The [dominated convergence theorem](https://en.wikipedia.org/wiki/Dominated_convergence_theorem "Dominated convergence theorem") gives sufficient conditions for almost sure convergence to imply The [dominated convergence theorem](https://en.wikipedia.org/wiki/Dominated_convergence_theorem "Dominated convergence theorem") gives sufficient conditions for almost sure convergence to imply ${\displaystyle L^{1}}$ -convergence:\-convergence:

| ${\displaystyle \left.{\begin{matrix}X_{n}\xrightarrow {\overset {}{\text{a.s.}}} X\\\|X_{n}\|<Y\\\mathbb {E} [Y]<\infty \end{matrix}}\right\}\quad \Rightarrow \quad X_{n}\xrightarrow {L^{1}} X}$ |  | 5 5 |
| --- | --- | --- | --- | --- |

- A necessary and sufficient condition for A necessary and sufficient condition for ${\displaystyle L^{1}}$ convergence is convergence is ${\displaystyle X_{n}{\xrightarrow {\overset {}{P}}}X}$ and the sequence and the sequence ${\displaystyle (X_{n})_{n}}$ is [uniformly integrable](https://en.wikipedia.org/wiki/Uniformly_integrable "Uniformly integrable"). is [uniformly integrable](https://en.wikipedia.org/wiki/Uniformly_integrable "Uniformly integrable").
- If If ${\displaystyle X_{n}\ \xrightarrow {\overset {}{p}} \ X}$, the followings are equivalent [^15], the followings are equivalent [^15]
	- ${\displaystyle X_{n}\ {\xrightarrow {\overset {}{L^{r}}}}\ X}$,,
		- ${\displaystyle \mathbb {E} [|X_{n}|^{r}]\rightarrow \mathbb {E} [|X|^{r}]<\infty }$,,
		- ${\displaystyle \{|X_{n}|^{r}\}}$ is [uniformly integrable](https://en.wikipedia.org/wiki/Uniformly_integrable "Uniformly integrable"). is [uniformly integrable](https://en.wikipedia.org/wiki/Uniformly_integrable "Uniformly integrable").

[^1]: [Bickel et al. 1998](#CITEREFBickelKlaassenRitovWellner1998), A.8, page 475 [Bickel et al. 1998](#CITEREFBickelKlaassenRitovWellner1998), A.8, page 475

[^2]: [van der Vaart & Wellner 1996](#CITEREFvan_der_VaartWellner1996), p. 4 [van der Vaart & Wellner 1996](#CITEREFvan_der_VaartWellner1996), p. 4

[^3]: [Romano & Siegel 1985](#CITEREFRomanoSiegel1985), Example 5.26 [Romano & Siegel 1985](#CITEREFRomanoSiegel1985), Example 5.26

[^4]: Durrett, Rick (2010). *Probability: Theory and Examples*. p. 84. Durrett, Rick (2010). *Probability: Theory and Examples*. p. 84.

[^5]: [van der Vaart 1998](#CITEREFvan_der_Vaart1998), Lemma 2.2 [van der Vaart 1998](#CITEREFvan_der_Vaart1998), Lemma 2.2

[^6]: [Dudley 2002](#CITEREFDudley2002), Chapter 9.2, page 287 [Dudley 2002](#CITEREFDudley2002), Chapter 9.2, page 287

[^7]: [Dudley 2002](#CITEREFDudley2002), p. 289 [Dudley 2002](#CITEREFDudley2002), p. 289

[^8]: [van der Vaart 1998](#CITEREFvan_der_Vaart1998), Theorem 2.7 [van der Vaart 1998](#CITEREFvan_der_Vaart1998), Theorem 2.7

[^9]: Gut, Allan (2005). *Probability: A graduate course*. Theorem 3.4: Springer. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0-387-22833-4](https://en.wikipedia.org/wiki/Special:BookSources/978-0-387-22833-4 "Special:BookSources/978-0-387-22833-4"). Gut, Allan (2005). *Probability: A graduate course*. Theorem 3.4: Springer. [ISBN](https://en.wikipedia.org/wiki/ISBN_\(identifier\) "ISBN (identifier)") [978-0-387-22833-4](https://en.wikipedia.org/wiki/Special:BookSources/978-0-387-22833-4 "Special:BookSources/978-0-387-22833-4").

[^10]: [Grimmett & Stirzaker 2020](#CITEREFGrimmettStirzaker2020), p. 354 [Grimmett & Stirzaker 2020](#CITEREFGrimmettStirzaker2020), p. 354

[^11]: [van der Vaart 1998](#CITEREFvan_der_Vaart1998), Th.2.19 [van der Vaart 1998](#CITEREFvan_der_Vaart1998), Th.2.19

[^12]: [Fristedt & Gray 1997](#CITEREFFristedtGray1997), Theorem 14.5 [Fristedt & Gray 1997](#CITEREFFristedtGray1997), Theorem 14.5

[^13]: Chung, Kai-lai (2001). *A Course in Probability Theory*. p. 126. Chung, Kai-lai (2001). *A Course in Probability Theory*. p. 126.

[^14]: ["Proofs of convergence of random variables"](https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables). *Wikipedia*. Retrieved 2024-09-23. ["Proofs of convergence of random variables"](https://en.wikipedia.org/wiki/Proofs_of_convergence_of_random_variables). *Wikipedia*. Retrieved 2024-09-23.

[^15]: ["real analysis - Generalizing Scheffe's Lemma using only Convergence in Probability"](https://math.stackexchange.com/questions/4401886/generalizing-scheffes-lemma-using-only-convergence-in-probability). *Mathematics Stack Exchange*. Retrieved 2022-03-12. ["real analysis - Generalizing Scheffe's Lemma using only Convergence in Probability"](https://math.stackexchange.com/questions/4401886/generalizing-scheffes-lemma-using-only-convergence-in-probability). *Mathematics Stack Exchange*. Retrieved 2022-03-12.