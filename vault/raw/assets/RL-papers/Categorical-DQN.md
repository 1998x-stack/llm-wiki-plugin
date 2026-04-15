A Distributional Perspective on Reinforcement Learning

Marc G. Bellemare * 1 Will Dabney * 1 R´emi Munos 1

7
1
0
2

l
u
J

1
2

]

G
L
.
s
c
[

1
v
7
8
8
6
0
.
7
0
7
1
:
v
i
X
r
a

Abstract
In this paper we argue for the fundamental impor-
tance of the value distribution: the distribution
of the random return received by a reinforcement
learning agent. This is in contrast to the com-
mon approach to reinforcement learning which
models the expectation of this return, or value.
Although there is an established body of liter-
ature studying the value distribution, thus far it
has always been used for a speciﬁc purpose such
as implementing risk-aware behaviour. We begin
with theoretical results in both the policy eval-
uation and control settings, exposing a signiﬁ-
cant distributional instability in the latter. We
then use the distributional perspective to design
a new algorithm which applies Bellman’s equa-
tion to the learning of approximate value distri-
butions. We evaluate our algorithm using the
suite of games from the Arcade Learning En-
vironment. We obtain both state-of-the-art re-
sults and anecdotal evidence demonstrating the
importance of the value distribution in approxi-
mate reinforcement learning. Finally, we com-
bine theoretical and empirical evidence to high-
light the ways in which the value distribution im-
pacts learning in the approximate setting.

1. Introduction

One of the major tenets of reinforcement learning states
that, when not otherwise constrained in its behaviour, an
agent should aim to maximize its expected utility Q, or
value (Sutton & Barto, 1998). Bellman’s equation succintly
describes this value in terms of the expected reward and ex-
(X (cid:48), A(cid:48)):
pected outcome of the random transition (x, a)

→
Q(x, a) = E R(x, a) + γ E Q(X (cid:48), A(cid:48)).

In this paper, we aim to go beyond the notion of value and
argue in favour of a distributional perspective on reinforce-

*Equal contribution 1DeepMind, London, UK. Correspon-

dence to: Marc G. Bellemare <bellemare@google.com>.

Proceedings of the 34 th International Conference on Machine
Learning, Sydney, Australia, PMLR 70, 2017. Copyright 2017
by the author(s).

ment learning. Speciﬁcally, the main object of our study is
the random return Z whose expectation is the value Q. This
random return is also described by a recursive equation, but
one of a distributional nature:

Z(x, a) D= R(x, a) + γZ(X (cid:48), A(cid:48)).

The distributional Bellman equation states that the distribu-
tion of Z is characterized by the interaction of three random
variables: the reward R, the next state-action (X (cid:48), A(cid:48)), and
its random return Z(X (cid:48), A(cid:48)). By analogy with the well-
known case, we call this quantity the value distribution.

Although the distributional perspective is almost as old
as Bellman’s equation itself (Jaquette, 1973; Sobel, 1982;
White, 1988), in reinforcement learning it has thus far been
subordinated to speciﬁc purposes: to model parametric un-
certainty (Dearden et al., 1998), to design risk-sensitive al-
gorithms (Morimura et al., 2010b;a), or for theoretical anal-
ysis (Azar et al., 2012; Lattimore & Hutter, 2012). By con-
trast, we believe the value distribution has a central role to
play in reinforcement learning.

Contraction of the policy evaluation Bellman operator.
Basing ourselves on results by R¨osler (1992) we show that,
for a ﬁxed policy, the Bellman operator over value distribu-
tions is a contraction in a maximal form of the Wasserstein
(also called Kantorovich or Mallows) metric. Our partic-
ular choice of metric matters: the same operator is not a
contraction in total variation, Kullback-Leibler divergence,
or Kolmogorov distance.

Instability in the control setting. We will demonstrate an
instability in the distributional version of Bellman’s opti-
mality equation, in contrast to the policy evaluation case.
Speciﬁcally, although the optimality operator is a contrac-
tion in expected value (matching the usual optimality re-
sult), it is not a contraction in any metric over distributions.
These results provide evidence in favour of learning algo-
rithms that model the effects of nonstationary policies.

Better approximations. From an algorithmic standpoint,
there are many beneﬁts to learning an approximate distribu-
tion rather than its approximate expectation. The distribu-
tional Bellman operator preserves multimodality in value
distributions, which we believe leads to more stable learn-
ing. Approximating the full distribution also mitigates the
effects of learning from a nonstationary policy. As a whole,

A Distributional Perspective on Reinforcement Learning

we argue that this approach makes approximate reinforce-
ment learning signiﬁcantly better behaved.

We will illustrate the practical beneﬁts of the distributional
perspective in the context of the Arcade Learning Environ-
ment (Bellemare et al., 2013). By modelling the value dis-
tribution within a DQN agent (Mnih et al., 2015), we ob-
tain considerably increased performance across the gamut
of benchmark Atari 2600 games, and in fact achieve state-
of-the-art performance on a number of games. Our results
echo those of Veness et al. (2015), who obtained extremely
fast learning by predicting Monte Carlo returns.

From a supervised learning perspective, learning the full
value distribution might seem obvious: why restrict our-
selves to the mean? The main distinction, of course, is that
in our setting there are no given targets. Instead, we use
Bellman’s equation to make the learning process tractable;
we must, as Sutton & Barto (1998) put it, “learn a guess
from a guess”. It is our belief that this guesswork ultimately
carries more beneﬁts than costs.

2. Setting

,

We consider an agent interacting with an environment in
the standard fashion: at each step, the agent selects an ac-
tion based on its current state, to which the environment re-
sponds with a reward and the next state. We model this in-
teraction as a time-homogeneous Markov Decision Process
are respectively the
(
X
state and action spaces, P is the transition kernel P (
x, a),
[0, 1] is the discount factor, and R is the reward func-
γ
tion, which in this work we explicitly treat as a random
variable. A stationary policy π maps each state x
to a
.
probability distribution over the action space
A

, R, P, γ). As usual,

∈ X

and

A

A

· |

X

∈

2.1. Bellman’s Equations

The return Z π is the sum of discounted rewards along the
agent’s trajectory of interactions with the environment. The
value function Qπ of a policy π describes the expected re-
turn from taking action a
, then
acting according to π:

from state x

∈ A

∈ X

Qπ(x, a) := E Z π(x, a) = E

(cid:35)

γtR(xt, at)

,

(1)

(cid:34) ∞
(cid:88)

t=0

· |

π(

P (

xt−1, at−1), at ∼

xt ∼
Fundamental to reinforcement learning is the use of Bell-
man’s equation (Bellman, 1957) to describe the value func-
tion:

xt), x0 = x, a0 = a.

· |

Figure 1. A distributional Bellman operator with a deterministic
reward function: (a) Next state distribution under policy π, (b)
Discounting shrinks the distribution towards 0, (c) The reward
shifts it, and (d) Projection step (Section 4).

proach for doing so involves the optimality equation

Q∗(x, a) = E R(x, a) + γ EP max
a(cid:48)∈A

Q∗(x(cid:48), a(cid:48)).

This equation has a unique ﬁxed point Q∗, the optimal
value function, corresponding to the set of optimal policies
Π∗ (π∗ is optimal if Ea∼π∗ Q∗(x, a) = maxa Q∗(x, a)).
We view value functions as vectors in RX ×A, and the ex-
pected reward function as one such vector. In this context,
the Bellman operator

π and optimality operator

are

T

T

πQ(x, a) := E R(x, a) + γ E
P,π

Q(x(cid:48), a(cid:48))

T

Q(x, a) := E R(x, a) + γ EP max
a(cid:48)∈A

Q(x(cid:48), a(cid:48)).

T

(2)

(3)

These operators are useful as they describe the expected
behaviour of popular learning algorithms such as SARSA
and Q-Learning.
In particular they are both contraction
mappings, and their repeated application to some initial Q0
converges exponentially to Qπ or Q∗, respectively (Bert-
sekas & Tsitsiklis, 1996).

3. The Distributional Bellman Operators

In this paper we take away the expectations inside Bell-
man’s equations and consider instead the full distribution
of the random variable Z π. From here on, we will view Z π
as a mapping from state-action pairs to distributions over
returns, and call it the value distribution.

Our ﬁrst aim is to gain an understanding of the theoretical
behaviour of the distributional analogues of the Bellman
operators, in particular in the less well-understood control
setting. The reader strictly interested in the algorithmic
contribution may choose to skip this section.

Qπ(x, a) = E R(x, a) + γ E
P,π

Qπ(x(cid:48), a(cid:48)).

3.1. Distributional Equations

In reinforcement learning we are typically interested in act-
ing so as to maximize the return. The most common ap-

It will sometimes be convenient to make use of the proba-
, Pr). The reader unfamiliar with mea-
bility space (Ω,

F

 P⇡ZR+P⇡Z ZP⇡(a)(b)(c)(d)T⇡Z A Distributional Perspective on Reinforcement Learning

∈

U

≤

∞

(cid:107)
p

(cid:107)p := (cid:2)E (cid:2)

→
(cid:3)(cid:3)1/p, and for p =

sure theory may think of Ω as the space of all possible
outcomes of an experiment (Billingsley, 1995). We will
RX for
(cid:107)p to denote the Lp norm of a vector u
u
write
∈
; the same applies to vectors in RX ×A. The
1
≤ ∞
RX (or RX ×A) is
Lp norm of a random vector U : Ω
p
we have
then
U (ω)
p
(cid:107)
(cid:107)
(cid:107)
∞ (we will omit the dependency
∞ = ess sup
U (ω)
U
(cid:107)
(cid:107)
(cid:107)
(cid:107)
Ω whenever unambiguous). We will denote the
on ω
c.d.f. of a random variable U by FU (y) := Pr
,
and its inverse c.d.f. by F −1

U (q) := inf
D
A distributional equation U
:= V indicates that the ran-
dom variable U is distributed according to the same law
as V . Without loss of generality, the reader can understand
the two sides of a distributional equation as relating the dis-
tributions of two independent random variables. Distribu-
tional equations have been used in reinforcement learning
by Engel et al. (2005); Morimura et al. (2010a) among oth-
ers, and in operations research by White (1988).

U
{
y : FU (y)
{

y
≤
.
q
}

≥

}

3.2. The Wasserstein Metric

The main tool for our analysis is the Wasserstein metric dp
between cumulative distribution functions (see e.g. Bickel
& Freedman, 1981, where it is called the Mallows metric).
For F , G two c.d.fs over the reals, it is deﬁned as

dp(F, G) := inf

U

U,V (cid:107)

V

(cid:107)p,

−

where the inﬁmum is taken over all pairs of random vari-
ables (U, V ) with respective cumulative distributions F
and G. The inﬁmum is attained by the inverse c.d.f. trans-
uniformly distributed on [0, 1]:
form of a random variable

U
F −1(

dp(F, G) =

(cid:107)

)

−

G−1(

(cid:107)p.
)

U

U

For p <

∞

this is more explicitly written as

of U, V . The metric dp has the following properties:

dp(aU, aV )
dp(A + U, A + V )
dp(AU, AV )

≤ |

≤

dp(U, V )

a
|
dp(U, V )
A

≤ (cid:107)

(cid:107)pdp(U, V ).

(P1)

(P2)

(P3)

We will need the following additional property, which
makes no independence assumptions on its variables. Its
proof, and that of later results, is given in the appendix.

Lemma 1 (Partition lemma). Let A1, A2, . . . be a set of
random variables describing a partition of Ω, i.e. Ai(ω)
0, 1
{
}
1. Let U, V be two random variables. Then

∈
and for any ω there is exactly one Ai with Ai(ω) =

(cid:0)U, V (cid:1)

dp

(cid:88)

≤

i

dp(AiU, AiV ).

Z

denote the space of value distributions with bounded
we will

Let
moments. For two value distributions Z1, Z2 ∈ Z
make use of a maximal form of the Wasserstein metric:

¯dp(Z1, Z2) := sup
x,a

dp(Z1(x, a), Z2(x, a)).

We will use ¯dp to establish the convergence of the distribu-
tional Bellman operators.
Lemma 2. ¯dp is a metric over value distributions.

3.3. Policy Evaluation

In the policy evaluation setting (Sutton & Barto, 1998) we
are interested in the value function V π associated with a
given policy π. The analogue here is the value distribu-
tion Z π. In this section we characterize Z π and study the
π. We em-
behaviour of the policy evaluation operator
phasize that Z π describes the intrinsic randomness of the
agent’s interactions with its environment, rather than some
measure of uncertainty about the environment itself.

T

dp(F, G) =

(cid:18)(cid:90) 1

0

(cid:12)
(cid:12)F −1(u)

−

G−1(u)(cid:12)
(cid:12)

p

(cid:19)1/p

du

.

We view the reward function as a random vector R
and deﬁne the transition operator P π :

Z → Z

Given two random variables U , V with c.d.fs FU , FV , we
will write dp(U, V ) := dp(FU , FV ). We will ﬁnd it conve-
nient to conﬂate the random variables under consideration
with their versions under the inf, writing

dp(U, V ) = inf

U,V (cid:107)

U

V

(cid:107)p.

−

whenever unambiguous; we believe the greater legibility
justiﬁes the technical inaccuracy. Finally, we extend this
metric to vectors of random variables, such as value distri-
butions, using the corresponding Lp norm.

Consider a scalar a and a random variable A independent

P πZ(x, a)
X (cid:48)

D
:= Z(X (cid:48), A(cid:48))

P (

· |

∼

x, a), A(cid:48)

π(

· |

∼

X (cid:48)),

where we use capital letters to emphasize the random na-
ture of the next state-action pair (X (cid:48), A(cid:48)). We deﬁne the
distributional Bellman operator

as

π :

T

Z → Z

πZ(x, a)

D
:= R(x, a) + γP πZ(x, a).

(5)

T
π bears a surface resemblance to the usual Bell-
While
man operator (2), it is fundamentally different. In particu-
lar, three sources of randomness deﬁne the compound dis-
tribution

πZ:

T

T

,

∈ Z

(4)

A Distributional Perspective on Reinforcement Learning

a) The randomness in the reward R,
b) The randomness in the transition P π, and
c) The next-state value distribution Z(X (cid:48), A(cid:48)).

In particular, we make the usual assumption that these three
In this section we will show
quantities are independent.
that (5) is a contraction mapping whose unique ﬁxed point
is the random return Z π.

3.3.1. CONTRACTION IN ¯dp

T

πZk, starting with some
Consider the process Zk+1 :=
. We may expect the limiting expectation of
Zk}
Z0 ∈ Z
{
to converge exponentially quickly, as usual, to Qπ. As we
π
now show, the process converges in a stronger sense:
is a contraction in ¯dp, which implies that all moments also
converge exponentially quickly.
π :

is a γ-contraction in ¯dp.

Lemma 3.

T

T

Z → Z

Using Lemma 3, we conclude using Banach’s ﬁxed point
π has a unique ﬁxed point. By inspection,
theorem that
this ﬁxed point must be Z π as deﬁned in (1). As we assume
all moments are bounded, this is sufﬁcient to conclude that
.
the sequence
≤ ∞

converges to Z π in ¯dp for 1

Zk}

≤

T

p

{

To conclude, we remark that not all distributional metrics
are equal; for example, Chung & Sobel (1987) have shown
π is not a contraction in total variation distance. Sim-
that
ilar results can be derived for the Kullback-Leibler diver-
gence and the Kolmogorov distance.

T

3.3.2. CONTRACTION IN CENTERED MOMENTS

Observe that d2(U, V ) (and more generally, dp) relates to a
coupling C(ω) := U (ω)

V (ω), in the sense that

d2
2(U, V )

E[(U

≤

−

−
V )2] = V(cid:0)C(cid:1) + (cid:0) E C(cid:1)2

.

V(
T
|

πZ(x, a))

As a result, we cannot directly use d2 to bound the variance
V(Z π(x, a))
π
difference
−
|
is in fact a contraction in variance (Sobel, 1982, see also
π is not a contraction in the pth
appendix). In general,
centered moment, p > 2, but the centered moments of the
iterates
still converge exponentially quickly to those
of Z π; the proof extends the result of R¨osler (1992).

. However,

Zk}

T

T

{

3.4. Control

Thus far we have considered a ﬁxed policy π, and studied
π. We now set
the behaviour of its associated operator
out to understand the distributional operators of the control
setting – where we seek a policy π that maximizes value
– and the corresponding notion of an optimal value distri-
bution. As with the optimal value function, this notion is
intimately tied to that of an optimal policy. However, while
all optimal policies attain the same value Q∗, in our case

T

a difﬁculty arises: in general there are many optimal value
distributions.

In this section we show that the distributional analogue
of the Bellman optimality operator converges, in a weak
sense, to the set of optimal value distributions. However,
this operator is not a contraction in any metric between dis-
tributions, and is in general much more temperamental than
the policy evaluation operators. We believe the conver-
gence issues we outline here are a symptom of the inherent
instability of greedy updates, as highlighted by e.g. Tsitsik-
lis (2002) and most recently Harutyunyan et al. (2016).

Let Π∗ be the set of optimal policies. We begin by charac-
terizing what we mean by an optimal value distribution.

Deﬁnition 1 (Optimal value distribution). An optimal
value distribution is the v.d. of an optimal policy. The set
.
of optimal value distributions is
}

Z π∗
{

∗ :=

: π∗

Π∗

Z

∈

We emphasize that not all value distributions with expecta-
tion Q∗ are optimal: they must match the full distribution
of the return under some optimal policy.

Deﬁnition 2. A greedy policy π for Z
expectation of Z. The set of greedy policies for Z is

∈ Z

maximizes the

GZ :=

π :
{

(cid:88)
a

π(a

|

x) E Z(x, a) = max
a(cid:48)∈A

E Z(x, a(cid:48))

.
}

Recall that the expected Bellman optimality operator

is

T

Q(x, a) = E R(x, a) + γ EP max
a(cid:48)∈A

T

Q(x(cid:48), a(cid:48)).

(6)

The maximization at x(cid:48) corresponds to some greedy policy.
Although this policy is implicit in (6), we cannot ignore it
in the distributional setting. We will call a distributional
Bellman optimality operator any operator
which imple-
ments a greedy selection rule, i.e.

T

Z =

T

T

πZ for some π

∈ GZ.

T

T

E

E
(cid:107)

. Then

Z2(cid:107)∞ ≤

As in the policy evaluation setting, we are interested in the
behaviour of the iterates Zk+1 :=
. Our ﬁrst
Zk, Z0 ∈ Z
result is to assert that E Zk behaves as expected.
Lemma 4. Let Z1, Z2 ∈ Z
Z1 −
T
and in particular E Zk →
By inspecting Lemma 4, we might expect that Zk con-
verges quickly in ¯dp to some ﬁxed point in
∗. Unfor-
tunately, convergence is neither quick nor assured to reach
a ﬁxed point. In fact, the best we can hope for is pointwise
∗ but to the larger set of
convergence, not even to the set
nonstationary optimal value distributions.

E Z2(cid:107)∞ ,
E Z1 −
(cid:107)
Q∗ exponentially quickly.

Z

Z

γ

A Distributional Perspective on Reinforcement Learning

Deﬁnition 3. A nonstationary optimal value distribution
Z ∗∗ is the value distribution corresponding to a sequence
of optimal policies. The set of n.o.v.d. is

∗∗.

Theorem 1 (Convergence in the control setting). Let
measurable and suppose that

is ﬁnite. Then

be

X

lim
k→∞

inf
Z∗∗∈Z ∗∗

A
dp(Zk(x, a), Z ∗∗(x, a)) = 0

x, a.

∀

Z

x1

x2, a1

x2, a2

Z ∗

Z

T

Z

1

1

(cid:15)

(cid:15)

±

±
0

0

0

0

(cid:15)

1

±
(cid:15)

−
(cid:15)

±
1

±

1

∗∗ uniformly. Further-
Z
on Π∗, such that for any

Figure 2. Undiscounted two-state MDP for which the optimality
operator T is not a contraction, with example. The entries that
contribute to ¯d1(Z, Z ∗) and ¯d1(T Z, Z ∗) are highlighted.

is ﬁnite, then Zk converges to

If
X
more, if there is a total ordering
Z ∗

∗,

≺

∈ Z
Z ∗ =

T
Then

T

πZ ∗ with π

∈ GZ∗ , π

≺
T
has a unique ﬁxed point Z ∗

π(cid:48)

π(cid:48)
∀
∗.

∈ Z

∈ GZ∗

π

.
}

\ {

Comparing Theorem 1 to Lemma 4 reveals a signiﬁcant
difference between the distributional framework and the
usual setting of expected return. While the mean of Zk
converges exponentially quickly to Q∗, its distribution need
not be as well-behaved! To emphasize this difference, we
now provide a number of negative results concerning

.

Proposition 1. The operator

is not a contraction.

T
Consider the following example (Figure 2, left). There are
two states, x1 and x2; a unique transition from x1 to x2;
from x2, action a1 yields no reward, while the optimal ac-
tion a2 yields 1 + (cid:15) or
1 + (cid:15) with equal probability. Both
actions are terminal. There is a unique optimal policy and
therefore a unique ﬁxed point Z ∗. Now consider Z as given
in Figure 2 (right), and its distance to Z ∗:

−

T

Proposition 3. That
T
insufﬁcient to guarantee the convergence of

has a ﬁxed point Z ∗ =
Zk}
{

T
to

Z ∗ is
∗.

Z

Theorem 1 paints a rather bleak picture of the control set-
ting. It remains to be seen whether the dynamical eccen-
tricies highlighted here actually arise in practice. One open
question is whether theoretically more stable behaviour can
be derived using stochastic policies, for example from con-
servative policy iteration (Kakade & Langford, 2002).

4. Approximate Distributional Learning

In this section we propose an algorithm based on the dis-
tributional Bellman optimality operator. In particular, this
will require choosing an approximating distribution. Al-
though the Gaussian case has previously been considered
(Morimura et al., 2010a; Tamar et al., 2016), to the best of
our knowledge we are the ﬁrst to use a rich class of para-
metric distributions.

¯d1(Z, Z ∗) = d1(Z(x2, a2), Z ∗(x2, a2)) = 2(cid:15),

4.1. Parametric Distribution

where we made use of the fact that Z = Z ∗ everywhere
except at (x2, a2). When we apply
to Z, however, the
Z(x1) = Z(x2, a1). But
greedy action a1 is selected and

T

d1(

T

Z,

T

Z ∗) = d1(
T
= 1
1
2 |

T
Z(x1), Z ∗(x1))
(cid:15)

1 + (cid:15)

+ 1
2 |

> 2(cid:15)

|

|

−
for a sufﬁciently small (cid:15). This shows that the undiscounted
Z ∗) > ¯d1(Z, Z ∗).
update is not a nonexpansion: ¯d1(
T
With γ < 1, the same proof shows it is not a contraction.
Using a more technically involved argument, we can extend
this result to any metric which separates Z and

Z.

Z,

T

Proposition 2. Not all optimality operators have a ﬁxed
point Z ∗ =

Z ∗.

T

T

To see this, consider the same example, now with (cid:15) = 0,
which breaks ties by picking a2
and a greedy operator
if Z(x1) = 0, and a1 otherwise. Then the sequence
)2Z ∗(x1), . . . alternates between Z ∗(x2, a1)

T

Z ∗(x1), (
T
T
and Z ∗(x2, a2).

We will model the value distribution using a discrete distri-
N and VMIN, VMAX ∈
R, and
bution parametrized by N
whose support is the set of atoms
zi = VMIN + i
z : 0
≤
(cid:52)
{
. In a sense, these atoms are the
i < N
“canonical returns” of our distribution. The atom probabil-
ities are given by a parametric model θ :

z := VMAX−VMIN

RN

,
}

N −1

(cid:52)

∈

Zθ(x, a) = zi w.p. pi(x, a) :=

X × A →
eθi(x,a)
j eθj (x,a) .

(cid:80)

The discrete distribution has the advantages of being highly
expressive and computationally friendly (see e.g. Van den
Oord et al., 2016).

4.2. Projected Bellman Update

the Bell-
Using a discrete distribution poses a problem:
Zθ and our parametrization Zθ almost al-
man update
ways have disjoint supports. From the analysis of Section
3 it would seem natural to minimize the Wasserstein met-
Zθ and Zθ, which is also
ric (viewed as a loss) between

T

T

R = 0R = 𝜀 ± 1x2x1a1a2A Distributional Perspective on Reinforcement Learning

conveniently robust to discrepancies in support. However,
a second issue prevents this: in practice we are typically
restricted to learning from sample transitions, which is not
possible under the Wasserstein loss (see Prop. 5 and toy
results in the appendix).

cade Learning Environment (ALE; Bellemare et al., 2013).
While the ALE is deterministic, stochasticity does occur in
a number of guises: 1) from state aliasing, 2) learning from
a nonstationary policy, and 3) from approximation errors.
We used ﬁve training games (Fig 3) and 52 testing games.

Instead, we project the sample Bellman update ˆ
Zθ onto
T
the support of Zθ (Figure 1, Algorithm 1), effectively re-
ducing the Bellman update to multiclass classiﬁcation. Let
π be the greedy policy w.r.t. E Zθ. Given a sample transi-
tion (x, a, r, x(cid:48)), we compute the Bellman update ˆ
zj :=
T
r + γzj for each atom zj, then distribute its probability
pj(x(cid:48), π(x(cid:48))) to the immediate neighbours of ˆ
zj. The ith
T
component of the projected update Φ ˆ
T
− zi|

Zθ(x, a) is
(cid:35)1

(cid:34)

(Φ ˆT Zθ(x, a))i =

N −1
(cid:88)

j=0

1 −

|[ ˆT zj]VMAX
VMIN
(cid:52)z

pj(x(cid:48), π(x(cid:48))),

0

(7)
a bounds its argument in the range [a, b].1 As is
]b
where [
·
usual, we view the next-state distribution as parametrized
by a ﬁxed parameter ˜θ. The sample loss
Lx,a(θ) is the
cross-entropy term of the KL divergence

DKL(Φ ˆ
T

Z˜θ(x, a)

(cid:107)

Zθ(x, a)),

which is readily minimized e.g. using gradient descent. We
call this choice of distribution and loss the categorical al-
gorithm. When N = 2, a simple one-parameter alternative
is Φ ˆ
0; we call
Zθ(x, a)]
T
this the Bernoulli algorithm. We note that, while these al-
gorithms appear unrelated to the Wasserstein metric, recent
work (Bellemare et al., 2017) hints at a deeper connection.

Zθ(x, a) := [E[ ˆ
T

VMIN)/

z]1

(cid:52)

−

Algorithm 1 Categorical Algorithm
input A transition xt, at, rt, xt+1, γt ∈
arg maxa Q(xt+1, a)
1

Q(xt+1, a) := (cid:80)
a∗
←
mi = 0,
for j

0, . . . , N
1 do

i
∈
0, . . . , N

i zipi(xt+1, a)

−

[0, 1]

∈

zj onto the support

−
# Compute the projection of ˆ
T
[rt + γtzj]VMAX
ˆ
zj ←
VMIN
T
( ˆ
VMIN)/∆z # bj ∈
bj ←
zj −
T
, u
bj(cid:101)
bj(cid:99)
l
← (cid:100)
← (cid:98)
# Distribute probability of ˆ
zj
T
ml + pj(xt+1, a∗)(u
bj)
ml ←
−
mu + pj(xt+1, a∗)(bj −
l)
mu ←
end for
(cid:80)
i mi log pi(xt, at) # Cross-entropy loss

[0, N

1]

−

output

−

zi}
{

5. Evaluation on Atari 2600 Games

To understand the approach in a complex setting, we ap-
plied the categorical algorithm to games from the Ar-

1Algorithm 1 computes this projection in time linear in N .

−

For our study, we use the DQN architecture (Mnih et al.,
2015), but output the atom probabilities pi(x, a) instead
of action-values, and chose VMAX =
VMIN = 10 from
preliminary experiments over the training games. We call
the resulting architecture Categorical DQN. We replace the
squared loss (r + γQ(x(cid:48), π(x(cid:48)))
Lx,a(θ)
and train the network to minimize this loss.2 As in DQN,
we use a simple (cid:15)-greedy policy over the expected action-
values; we leave as future work the many ways in which an
agent could select actions on the basis of the full distribu-
tion. The rest of our training regime matches Mnih et al.’s,
including the use of a target network for ˜θ.

Q(x, a))2 by

−

Figure 4 illustrates the typical value distributions we ob-
served in our experiments. In this example, three actions
(those including the button press) lead to the agent releas-
ing its laser too early and eventually losing the game. The
corresponding distributions reﬂect this: they assign a sig-
niﬁcant probability to 0 (the terminal value). The safe
actions have similar distributions (LEFT, which tracks the
invaders’ movement, is slightly favoured). This example
helps explain why our approach is so successful: the dis-
tributional update keeps separated the low-value, “losing”
event from the high-value, “survival” event, rather than av-
erage them into one (unrealizable) expectation.3

One surprising fact is that the distributions are not concen-
trated on one or two values, in spite of the ALE’s determin-
ism, but are often close to Gaussians. We believe this is due
to our discretizing the diffusion process induced by γ.

5.1. Varying the Number of Atoms

We began by studying our algorithm’s performance on the
training games in relation to the number of atoms (Figure
3). For this experiment, we set (cid:15) = 0.05. From the data, it
is clear that using too few atoms can lead to poor behaviour,
and that more always increases performance; this is not im-
mediately obvious as we may have expected to saturate the
network capacity. The difference in performance between
the 51-atom version and DQN is particularly striking: the
latter is outperformed in all ﬁve games, and in SEAQUEST
we attain state-of-the-art performance. As an additional
point of the comparison, the single-parameter Bernoulli al-
gorithm performs better than DQN in 3 games out of 5, and
is most notably more robust in ASTERIX.

2For N = 51, our TensorFlow implementation trains at

roughly 75% of DQN’s speed.

3Video: http://youtu.be/yFBwyPuO2Vg.

A Distributional Perspective on Reinforcement Learning

Figure 3. Categorical DQN: Varying number of atoms in the discrete distribution. Scores are moving averages over 5 million frames.

evaluate our agent’s performance with (cid:15) = 0.001.

We compare our algorithm to DQN ((cid:15) = 0.01), Double
DQN (van Hasselt et al., 2016), the Dueling architecture
(Wang et al., 2016), and Prioritized Replay (Schaul et al.,
2016), comparing the best evaluation score achieved during
training. We see that C51 signiﬁcantly outperforms these
other algorithms (Figures 6 and 7). In fact, C51 surpasses
the current state-of-the-art by a large margin in a number of
games, most notably SEAQUEST. One particularly striking
fact is the algorithm’s good performance on sparse reward
games, for example VENTURE and PRIVATE EYE. This
suggests that value distributions are better able to propa-
gate rarely occurring events. Full results are provided in
the appendix.

We also include in the appendix (Figure 12) a compari-
son, averaged over 3 seeds, showing the number of games
in which C51’s training performance outperforms fully-
trained DQN and human players. These results continue
to show dramatic improvements, and are more representa-
tive of an agent’s average performance. Within 50 million
frames, C51 has outperformed a fully trained DQN agent
on 45 out of 57 games. This suggests that the full 200 mil-
lion training frames, and its ensuing computational cost,
are unnecessary for evaluating reinforcement learning al-
gorithms within the ALE.

The most recent version of the ALE contains a stochastic
execution mechanism designed to ward against trajectory
overﬁtting.Speciﬁcally, on each frame the environment re-
jects the agent’s selected action with probability p = 0.25.
Although DQN is mostly robust to stochastic execution,
there are a few games in which its performance is reduced.
On a score scale normalized with respect to the random
and DQN agents, C51 obtains mean and median score im-
provements of 126% and 21.5% respectively, conﬁrming
the beneﬁts of C51 beyond the deterministic setting.

Figure 4. Learned value distribution during an episode of SPACE
INVADERS. Different actions are shaded different colours. Re-
turns below 0 (which do not occur in SPACE INVADERS) are not
shown here as the agent assigns virtually no probability to them.

One interesting outcome of this experiment was to ﬁnd
out that our method does pick up on stochasticity. PONG
exhibits intrinsic randomness: the exact timing of the re-
ward depends on internal registers and is truly unobserv-
able. We see this clearly reﬂected in the agent’s prediction
(Figure 5): over ﬁve consecutive frames, the value distribu-
tion shows two modes indicating the agent’s belief that it
has yet to receive a reward. Interestingly, since the agent’s
state does not include past rewards, it cannot even extin-
guish the prediction after receiving the reward, explaining
the relative proportions of the modes.

5.2. State-of-the-Art Results

The performance of the 51-atom agent (from here onwards,
C51) on the training games, presented in the last section, is
particularly remarkable given that it involved none of the
other algorithmic ideas present in state-of-the-art agents.
We next asked whether incorporating the most common
hyperparameter choice, namely a smaller training (cid:15), could
lead to even better results. Speciﬁcally, we set (cid:15) = 0.01
(instead of 0.05); furthermore, every 1 million frames, we

ASTERIXQ*BERTBREAKOUTPONGSEAQUESTCategorical DQN5 returns11 returns21 returns51 returnsDQNBernoulliAverage ScoreTraining Frames (millions)Dueling Arch.ReturnProbabilityRightLeftRight+LaserLeft+LaserLaserNoopA Distributional Perspective on Reinforcement Learning

Figure 5. Intrinsic stochasticity in PONG.

DQN
DDQN
DUEL.
PRIOR.
PR. DUEL.
C51
UNREAL†

Mean Median > H.B. > DQN
0
228%
43
307%
50
373%
48
434%
44
592%
50
701%
-
880%

79%
118%
151%
124%
172%
178%
250%

24
33
37
39
39
40
-

Figure 6. Mean and median scores across 57 Atari games, mea-
sured as percentages of human baseline (H.B., Nair et al., 2015).

Figure 7. Percentage improvement, per-game, of C51 over Dou-
ble DQN, computed using van Hasselt et al.’s method.

6. Discussion

In this work we sought a more complete picture of rein-
forcement learning, one that involves value distributions.
We found that learning value distributions is a powerful no-
tion that allows us to surpass most gains previously made
on Atari 2600, without further algorithmic adjustments.

6.1. Why does learning a distribution matter?

It is surprising that, when we use a policy which aims to
maximize expected return, we should see any difference
in performance. The distinction we wish to make is that
learning distributions matters in the presence of approxi-
mation. We now outline some possible reasons.

Reduced chattering. Our results from Section 3.4 high-
lighted a signiﬁcant instability in the Bellman optimal-
ity operator. When combined with function approxima-
tion, this instability may prevent the policy from converg-
ing, what Gordon (1995) called chattering. We believe
the gradient-based categorical algorithm is able to mitigate
these effects by effectively averaging the different distri-

† The UNREAL results are not altogether comparable, as
they were generated in the asynchronous setting with per-game
hyperparameter tuning (Jaderberg et al., 2017).

butions, similar to conservative policy iteration (Kakade &
Langford, 2002). While the chattering persists, it is inte-
grated to the approximate solution.

State aliasing. Even in a deterministic environment, state
aliasing may result in effective stochasticity. McCallum
(1995), for example, showed the importance of coupling
representation learning with policy learning in partially ob-
servable domains. We saw an example of state aliasing in
PONG, where the agent could not exactly predict the re-
ward timing. Again, by explicitly modelling the resulting
distribution we provide a more stable learning target.

A richer set of predictions. A recurring theme in artiﬁcial
intelligence is the idea of an agent learning from a mul-
titude of predictions (Caruana 1997; Utgoff & Stracuzzi
2002; Sutton et al. 2011; Jaderberg et al. 2017). The dis-
tributional approach naturally provides us with a rich set
of auxiliary predictions, namely:
the probability that the
return will take on a particular value. Unlike previously
proposed approaches, however, the accuracy of these pre-
dictions is tightly coupled with the agent’s performance.

Framework for inductive bias. The distributional per-
spective on reinforcement learning allows a more natural
framework within which we can impose assumptions about
the domain or the learning problem itself. In this work we
used distributions with support bounded in [VMIN, VMAX].
Treating this support as a hyperparameter allows us to
change the optimization problem by treating all extremal
returns (e.g. greater than VMAX) as equivalent. Surprisingly,
a similar value clipping in DQN signiﬁcantly degrades per-
formance in most games. To take another example:
in-
terpreting the discount factor γ as a proper probability, as
some authors have argued, leads to a different algorithm.

Well-behaved optimization. It is well-accepted that the
KL divergence between categorical distributions is a rea-
sonably easy loss to minimize. This may explain some of
our empirical performance. Yet early experiments with al-
ternative losses, such as KL divergence between continu-
ous densities, were not fruitful, in part because the KL di-
vergence is insensitive to the values of its outcomes. A
closer minimization of the Wasserstein metric should yield
even better results than what we presented here.

In closing, we believe our results highlight the need to ac-
count for distribution in the design, theoretical or other-
wise, of algorithms.

A Distributional Perspective on Reinforcement Learning

Acknowledgements

The authors acknowledge the important role played by their
colleagues at DeepMind throughout the development of
this work. Special thanks to Yee Whye Teh, Alex Graves,
Joel Veness, Guillaume Desjardins, Tom Schaul, David
Silver, Andre Barreto, Max Jaderberg, Mohammad Azar,
Georg Ostrovski, Bernardo Avila Pires, Olivier Pietquin,
Audrunas Gruslys, Tom Stepleton, Aaron van den Oord;
and particularly Chris Maddison for his comprehensive re-
view of an earlier draft. Thanks also to Marek Petrik for
pointers to the relevant literature, and Mark Rowland for
ﬁne-tuning details in the ﬁnal version.

Erratum

The camera-ready copy of this paper incorrectly reported a
mean score of 1010% for C51. The corrected ﬁgure stands
at 701%, which remains higher than the other comparable
baselines. The median score remains unchanged at 178%.

The error was due to evaluation episodes in one game (At-
lantis) lasting over 30 minutes; in comparison, the other
results presented here cap episodes at 30 minutes, as is
standard. The previously reported score on Atlantis was
3.7 million; our 30-minute score is 841,075, which we be-
lieve is close to the achievable maximum in this time frame.
Capping at 30 minutes brings our human-normalized score
on Atlantis from 22824% to a mere (!) 5199%, unfortu-
nately enough to noticeably affect the mean score, whose
sensitivity to outliers is well-documented.

References

Azar, Mohammad Gheshlaghi, Munos, R´emi, and Kappen,
Hilbert. On the sample complexity of reinforcement learning
with a generative model. In Proceedings of the International
Conference on Machine Learning, 2012.

Bellemare, Marc G, Naddaf, Yavar, Veness, Joel, and Bowling,
Michael. The arcade learning environment: An evaluation plat-
form for general agents. Journal of Artiﬁcial Intelligence Re-
search, 47:253–279, 2013.

Bellemare, Marc G., Danihelka,

Ivo, Dabney, Will, Mo-
hamed, Shakir, Lakshminarayanan, Balaji, Hoyer, Stephan,
and Munos, R´emi. The cramer distance as a solution to biased
wasserstein gradients. arXiv, 2017.

Bellman, Richard E. Dynamic programming. Princeton Univer-

sity Press, Princeton, NJ, 1957.

Bertsekas, Dimitri P. and Tsitsiklis, John N. Neuro-Dynamic Pro-

gramming. Athena Scientiﬁc, 1996.

Bickel, Peter J. and Freedman, David A. Some asymptotic the-
ory for the bootstrap. The Annals of Statistics, pp. 1196–1217,
1981.

Billingsley, Patrick. Probability and measure.

John Wiley &

Sons, 1995.

Caruana, Rich. Multitask learning. Machine Learning, 28(1):

41–75, 1997.

Chung, Kun-Jen and Sobel, Matthew J. Discounted mdps: Distri-
bution functions and exponential utility maximization. SIAM
Journal on Control and Optimization, 25(1):49–62, 1987.

Dearden, Richard, Friedman, Nir, and Russell, Stuart. Bayesian
Q-learning. In Proceedings of the National Conference on Ar-
tiﬁcial Intelligence, 1998.

Engel, Yaakov, Mannor, Shie, and Meir, Ron. Reinforcement
In Proceedings of the In-

learning with gaussian processes.
ternational Conference on Machine Learning, 2005.

Geist, Matthieu and Pietquin, Olivier. Kalman temporal differ-
ences. Journal of Artiﬁcial Intelligence Research, 39:483–532,
2010.

Gordon, Geoffrey. Stable function approximation in dynamic pro-
gramming. In Proceedings of the Twelfth International Confer-
ence on Machine Learning, 1995.

Harutyunyan, Anna, Bellemare, Marc G., Stepleton, Tom, and
Munos, R´emi. Q(λ) with off-policy corrections. In Proceed-
ings of the Conference on Algorithmic Learning Theory, 2016.

Hoffman, Matthew D., de Freitas, Nando, Doucet, Arnaud, and
Peters, Jan. An expectation maximization algorithm for con-
tinuous markov decision processes with arbitrary reward.
In
Proceedings of the International Conference on Artiﬁcial In-
telligence and Statistics, 2009.

Jaderberg, Max, Mnih, Volodymyr, Czarnecki, Wojciech Marian,
Schaul, Tom, Leibo, Joel Z, Silver, David, and Kavukcuoglu,
Koray. Reinforcement learning with unsupervised auxiliary
tasks. Proceedings of the International Conference on Learn-
ing Representations, 2017.

Jaquette, Stratton C. Markov decision processes with a new opti-
mality criterion: Discrete time. The Annals of Statistics, 1(3):
496–505, 1973.

Kakade, Sham and Langford, John. Approximately optimal ap-
proximate reinforcement learning. In Proceedings of the Inter-
national Conference on Machine Learning, 2002.

Kingma, Diederik and Ba, Jimmy. Adam: A method for stochas-
tic optimization. Proceedings of the International Conference
on Learning Representations, 2015.

Lattimore, Tor and Hutter, Marcus. PAC bounds for discounted
In Proceedings of the Conference on Algorithmic

MDPs.
Learning Theory, 2012.

Mannor, Shie and Tsitsiklis, John N. Mean-variance optimization

in markov decision processes. 2011.

McCallum, Andrew K. Reinforcement learning with selective per-
ception and hidden state. PhD thesis, University of Rochester,
1995.

Mnih, Volodymyr, Kavukcuoglu, Koray, Silver, David, Rusu, An-
drei A, Veness, Joel, Bellemare, Marc G, Graves, Alex, Ried-
miller, Martin, Fidjeland, Andreas K, Ostrovski, Georg, et al.
Human-level control through deep reinforcement learning. Na-
ture, 518(7540):529–533, 2015.

A Distributional Perspective on Reinforcement Learning

van Hasselt, Hado, Guez, Arthur, and Silver, David. Deep rein-
forcement learning with double Q-learning. In Proceedings of
the AAAI Conference on Artiﬁcial Intelligence, 2016.

Veness, Joel, Bellemare, Marc G., Hutter, Marcus, Chua, Alvin,
and Desjardins, Guillaume. Compress and control. In Proceed-
ings of the AAAI Conference on Artiﬁcial Intelligence, 2015.

Wang, Tao, Lizotte, Daniel, Bowling, Michael, and Schuurmans,
Dale. Dual representations for dynamic programming. Journal
of Machine Learning Research, pp. 1–29, 2008.

Wang, Ziyu, Schaul, Tom, Hessel, Matteo, Hasselt, Hado van,
Lanctot, Marc, and de Freitas, Nando. Dueling network archi-
tectures for deep reinforcement learning. In Proceedings of the
International Conference on Machine Learning, 2016.

White, D. J. Mean, variance, and probabilistic criteria in ﬁnite
markov decision processes: a review. Journal of Optimization
Theory and Applications, 56(1):1–29, 1988.

Morimura, Tetsuro, Hachiya, Hirotaka, Sugiyama, Masashi,
Tanaka, Toshiyuki, and Kashima, Hisashi. Parametric return
In Proceed-
density estimation for reinforcement learning.
ings of the Conference on Uncertainty in Artiﬁcial Intelligence,
2010a.

Morimura, Tetsuro, Sugiyama, Masashi, Kashima, Hisashi,
Hachiya, Hirotaka, and Tanaka, Toshiyuki. Nonparametric re-
turn distribution approximation for reinforcement learning. In
Proceedings of the 27th International Conference on Machine
Learning (ICML-10), pp. 799–806, 2010b.

Nair, Arun, Srinivasan, Praveen, Blackwell, Sam, Alcicek,
Cagdas, Fearon, Rory, De Maria, Alessandro, Panneershelvam,
Vedavyas, Suleyman, Mustafa, Beattie, Charles, and Petersen,
Stig et al. Massively parallel methods for deep reinforcement
learning. In ICML Workshop on Deep Learning, 2015.

Prashanth, LA and Ghavamzadeh, Mohammad. Actor-critic algo-
rithms for risk-sensitive mdps. In Advances in Neural Informa-
tion Processing Systems, 2013.

Puterman, Martin L. Markov Decision Processes: Discrete
stochastic dynamic programming. John Wiley & Sons, Inc.,
1994.

R¨osler, Uwe. A ﬁxed point theorem for distributions. Stochastic

Processes and their Applications, 42(2):195–214, 1992.

Schaul, Tom, Quan, John, Antonoglou, Ioannis, and Silver,
In Proceedings of the
David. Prioritized experience replay.
International Conference on Learning Representations, 2016.

Sobel, Matthew J. The variance of discounted markov decision
processes. Journal of Applied Probability, 19(04):794–802,
1982.

Sutton, Richard S. and Barto, Andrew G. Reinforcement learning:

An introduction. MIT Press, 1998.

Sutton, R.S., Modayil, J., Delp, M., Degris, T., Pilarski, P.M.,
White, A., and Precup, D. Horde: A scalable real-time archi-
tecture for learning knowledge from unsupervised sensorimo-
tor interaction. In Proceedings of the International Conference
on Autonomous Agents and Multiagents Systems, 2011.

Tamar, Aviv, Di Castro, Dotan, and Mannor, Shie. Learning the
variance of the reward-to-go. Journal of Machine Learning
Research, 17(13):1–36, 2016.

Tieleman, Tijmen and Hinton, Geoffrey. Lecture 6.5-rmsprop:
Divide the gradient by a running average of its recent magni-
tude. COURSERA: Neural networks for machine learning, 4
(2), 2012.

Toussaint, Marc and Storkey, Amos. Probabilistic inference for
solving discrete and continuous state markov decision pro-
cesses. In Proceedings of the International Conference on Ma-
chine Learning, 2006.

Tsitsiklis, John N. On the convergence of optimistic policy itera-
tion. Journal of Machine Learning Research, 3:59–72, 2002.

Utgoff, Paul E. and Stracuzzi, David J. Many-layered learning.

Neural Computation, 14(10):2497–2529, 2002.

Van den Oord, Aaron, Kalchbrenner, Nal, and Kavukcuoglu, Ko-
In Proceedings of the

ray. Pixel recurrent neural networks.
International Conference on Machine Learning, 2016.

A Distributional Perspective on Reinforcement Learning

A. Related Work

To the best of our knowledge, the work closest to ours are
two papers (Morimura et al., 2010b;a) studying the distri-
butional Bellman equation from the perspective of its cu-
mulative distribution functions. The authors propose both
parametric and nonparametric solutions to learn distribu-
tions for risk-sensitive reinforcement learning. They also
provide some theoretical analysis for the policy evaluation
setting, including a consistency result in the nonparamet-
ric case. By contrast, we also analyze the control setting,
and emphasize the use of the distributional equations to im-
prove approximate reinforcement learning.

The variance of the return has been extensively stud-
ied in the risk-sensitive setting. Of note, Tamar et al.
(2016) analyze the use of linear function approximation
to learn this variance for policy evaluation, and Prashanth
& Ghavamzadeh (2013) estimate the return variance in the
design of a risk-sensitive actor-critic algorithm. Mannor
& Tsitsiklis (2011) provides negative results regarding the
computation of a variance-constrained solution to the opti-
mal control problem.

The distributional formulation also arises when modelling
uncertainty. Dearden et al. (1998) considered a Gaussian
approximation to the value distribution, and modelled the
uncertainty over the parameters of this approximation us-
ing a Normal-Gamma prior. Engel et al. (2005) leveraged
the distributional Bellman equation to deﬁne a Gaussian
process over the unknown value function. More recently,
Geist & Pietquin (2010) proposed an alternative solution to
the same problem based on unscented Kalman ﬁlters. We
believe much of the analysis we provide here, which deals
with the intrinsic randomness of the environment, can also
be applied to modelling uncertainty.

Our work here is based on a number of foundational re-
sults, in particular concerning alternative optimality crite-
ria. Early on, Jaquette (1973) showed that a moment opti-
mality criterion, which imposes a total ordering on distri-
butions, is achievable and deﬁnes a stationary optimal pol-
icy, echoing the second part of Theorem 1. Sobel (1982)
is usually cited as the ﬁrst reference to Bellman equations
for the higher moments (but not the distribution) of the re-
turn. Chung & Sobel (1987) provides results concerning
the convergence of the distributional Bellman operator in
total variation distance. White (1988) studies “nonstandard
MDP criteria” from the perspective of optimizing the state-
action pair occupancy.

A number of probabilistic frameworks for reinforcement
learning have been proposed in recent years. The plan-
ning as inference approach (Toussaint & Storkey, 2006;
Hoffman et al., 2009) embeds the return into a graphical
model, and applies probabilistic inference to determine the

sequence of actions leading to maximal expected reward.
Wang et al. (2008) considered the dual formulation of re-
inforcement learning, where one optimizes the stationary
distribution subject to constraints given by the transition
function (Puterman, 1994), in particular its relationship to
linear approximation. Related to this dual is the Compress
and Control algorithm Veness et al. (2015), which describes
a value function by learning a return distribution using den-
sity models. One of the aims of this work was to address
the question left open by their work of whether one could
be design a practical distributional algorithm based on the
Bellman equation, rather than Monte Carlo estimation.

B. Proofs

Lemma 1 (Partition lemma). Let A1, A2, . . . be a set of
random variables describing a partition of Ω, i.e. Ai(ω)
0, 1
{
}
1. Let U, V be two random variables. Then

∈
and for any ω there is exactly one Ai with Ai(ω) =

(cid:0)U, V (cid:1)

dp

(cid:88)

≤

i

dp(AiU, AiV ).

Proof. We will give the proof for p <
same applies to p =
respectively. First note that

. Let Yi

∞

∞
D
:= AiU and Zi

, noting that the
D
:= AiV ,

p(cid:3)

dp
p(AiU, AiV ) = inf
Yi,Zi

= inf
Yi,Zi

E (cid:2)
Yi −
|
(cid:104)
E (cid:2)
|

Zi|
Yi −
p = 0 whenever Ai = 0. It follows that
|
p = 0 whenever
Zi|

Yi −

Zi|

AiU
|

Now,
AiV
we can choose Yi, Zi so that also
Ai = 0, without increasing the expected norm. Hence

(cid:3)(cid:105)

Ai

−

E

p

|

.

|

(8)

(9)

dp
p(AiU, AiV ) =
inf
Yi,Zi

Ai = 1
Pr
}
{
Next, we claim that

E (cid:2)
Yi −
|

p

Zi|

|

Ai = 1(cid:3).

(cid:88)

inf
U,V

Pr
{

Ai = 1
}

i

E

(cid:104)(cid:12)
(cid:12)AiU

−

≤

inf
Y1,Y2,...
Z1,Z2,...

(cid:88)
i

Pr

Ai = 1
}
{

AiV

p

(cid:12)
(cid:12)

(cid:105)
Ai = 1

(cid:104)

E

|
Yi −
|

(cid:105)
Ai = 1

.

p

(cid:12)
(cid:12)

Zi

|

Speciﬁcally, the left-hand side of the equation is an inﬁ-
mum over all r.v.’s whose cumulative distributions are FU
and FV , respectively, while the right-hand side is an in-
ﬁmum over sequences of r.v’s Y1, Y2, . . . and Z1, Z2, . . .
whose cumulative distributions are FAiU , FAiV , respec-
tively. To prove this upper bound, consider the c.d.f. of
U :

FU (y) = Pr
{
(cid:88)

U

y

}
Ai = 1
}
Ai = 1
}

U
Pr
{
≤
AiU
Pr
{

y

Ai = 1
}

|

y

.
Ai = 1
}

|

≤

≤
Pr
{
Pr
{

i

i

=

(cid:88)

=

A Distributional Perspective on Reinforcement Learning

Hence the distribution FU is equivalent, in an almost sure
sense, to one that ﬁrst picks an element Ai of the partition,
then picks a value for U conditional on the choice Ai. On
the other hand, the c.d.f. of Yi

D= AiU is

y

≤
y

AiU
Pr
{
Pr

Ai = 1
|
}
y
Ai = 0
}
|
Ai = 1
}

Ai = 1
FAiU (y) = Pr
{
}
≤
Ai = 0
+ Pr
AiU
{
}
{
AiU
Pr
Ai = 1
= Pr
{
{
}
I [y
Ai = 0
+ Pr
}
{
Thus the right-hand side inﬁmum in (9) has the additional
constraint that it must preserve the conditional c.d.fs, in
particular when y
0. Put another way, instead of hav-
ing the freedom to completely reorder the mapping U :
R, we can only reorder it within each element of the
Ω
partition. We now write

≤
0] .

→

≥

≥

|

V

(cid:107)p

−
p(cid:3)

U,V (cid:107)
V
U

= inf
U,V

dp
p(U, V ) = inf
E (cid:2)
|
(cid:88)
i

(a)
= inf
U,V

−

U

|

= inf
U,V

(cid:88)

i

E (cid:2)
|

U

Pr
{

Ai = 1
}
E (cid:2)
AiU
|

Ai = 1
Pr
}
{

−

Ai = 1(cid:3)

V

p

|

|

AiV

p

|

|

−

Ai = 1(cid:3),

where (a) follows because A1, A2, . . . is a partition. Using
(9), this implies

dp
p(U, V )

E

(cid:88)
Ai = 1
Pr
}
{
i
(cid:88)
i

Ai = 1
Pr
}
{

(cid:104)(cid:12)
(cid:12)AiU
−
(cid:104)(cid:12)
(cid:12)Yi −

E

|

p

(cid:12)
(cid:12)

Zi

|

AiV (cid:12)
(cid:12)

p

(cid:105)
Ai = 1

(cid:105)
Ai = 1

= inf
U,V

≤

(b)
=

(c)
=

inf
Y1,Y2,...
Z1,Z2,...
(cid:88)

i
(cid:88)

i

Lemma 3.

π :

Z → Z

T
Proof. Consider Z1, Z2 ∈ Z
¯dp(
πZ2) = sup
dp(
x,a

πZ1,

T

T

is a γ-contraction in ¯dp.

. By deﬁnition,

T

πZ1(x, a),

T

πZ2(x, a)).

(10)

By the properties of dp, we have

dp(T πZ1(x, a), T πZ2(x, a))

= dp(R(x, a) + γP πZ1(x, a), R(x, a) + γP πZ2(x, a))
≤ γdp(P πZ1(x, a), P πZ2(x, a))
≤ γ sup
x(cid:48),a(cid:48)

dp(Z1(x(cid:48), a(cid:48)), Z2(x(cid:48), a(cid:48))),

where the last line follows from the deﬁnition of P π (see
(4)). Combining with (10) we obtain

¯dp(
T

πZ1,

πZ2) = sup
x,a

T

dp(

πZ1(x, a),

πZ2(x, a))

T
dp(Z1(x(cid:48), a(cid:48)), Z2(x(cid:48), a(cid:48)))

T

γ sup
≤
x(cid:48),a(cid:48)
= γ ¯dp(Z1, Z2).

Proposition 1 (Sobel, 1982). Consider two value distri-
, and write V(Zi) to be the vector of
butions Z1, Z2 ∈ Z
variances of Zi. Then

E
(cid:107)
V(
T
(cid:107)

T
πZ1)

E
πZ1 −
V(
T
−

πZ2(cid:107)∞ ≤
T
πZ2)
(cid:107)∞ ≤

γ
(cid:107)
γ2

E Z1 −
VZ1 −
(cid:107)

E Z2(cid:107)∞ , and
VZ2(cid:107)∞ .

πZ =

Proof. The ﬁrst statement is standard, and its proof follows
π E Z, where the second
from E
π denotes the
T
usual operator over value functions. Now, by independence
of R and P πZi:

T

T

πZi(x, a)) = V

(cid:16)

R(x, a) + γP πZi(x, a)
= V(R(x, a)) + γ2V(P πZi(x, a)).

(cid:17)

inf
Yi,Zi

Ai = 1
Pr
}
{

E

(cid:104)(cid:12)
(cid:12)Yi −

p

(cid:12)
(cid:12)

Zi

|

(cid:105)
Ai = 1

V(
T

dp(AiU, AiV ),

because in (b) the individual components of the sum are
independently minimized; and (c) from (8).
Lemma 2. ¯dp is a metric over value distributions.

Proof. The only nontrivial property is the triangle inequal-
ity. For any value distribution Y

, write

∈ Z

¯dp(Z1, Z2) = sup
x,a

dp(Z1(x, a), Z2(x, a))

(a)

≤

sup
x,a

[dp(Z1(x, a), Y (x, a)) + dp(Y (x, a), Z2(x, a))]

sup
x,a

dp(Z1(x, a), Y (x, a)) + sup
x,a

≤
= ¯dp(Z1, Y ) + ¯dp(Y, Z2),

dp(Y (x, a), Z2(x, a))

where in (a) we used the triangle inequality for dp.

And now

= sup
x,a

= sup
x,a

≤

sup
x(cid:48),a(cid:48)
γ2

V(
(cid:107)

V(
πZ2)
(cid:107)∞
T
πZ1(x, a))

πZ1)
−
T
(cid:12)
(cid:12)V(
= sup
T
−
x,a
γ2(cid:12)
(cid:12) [V(P πZ1(x, a))

−
(cid:12) E [V(Z1(X (cid:48), A(cid:48)))

γ2(cid:12)

γ2(cid:12)

(cid:12)V(Z1(x(cid:48), a(cid:48)))

−

VZ1 −

VZ2(cid:107)∞ .

. Then

≤

(cid:107)
Lemma 4. Let Z1, Z2 ∈ Z
Z1 −
T
and in particular E Zk →

E
(cid:107)

E

T

πZ2(x, a))(cid:12)
(cid:12)

V(
T
V(P πZ2(x, a))]

(cid:12)
(cid:12)

V(Z2(X (cid:48), A(cid:48)))]

(cid:12)
(cid:12)

−
V(Z2(x(cid:48), a(cid:48)))(cid:12)
(cid:12)

Z2(cid:107)∞ ≤

γ

E Z2(cid:107)∞ ,
E Z1 −
Q∗ exponentially quickly.

(cid:107)

A Distributional Perspective on Reinforcement Learning

∈ GZ∗

π

,
}

\ {

Xk,i := (cid:8)x : x

∈ Xk, P (

Xk−1,i−1 |

x, π∗(x))

δ(cid:9),

1

−

≥

Proof. The proof follows by linearity of expectation. Write
TE for the usual op-
TD for the distributional operator and
erator. Then

(cid:107)

E

E

TDZ1 −

(cid:107)TE E Z1 − TE E Z2(cid:107)∞
Z2(cid:107)∞ .
Z1 −
γ
(cid:107)

TDZ2(cid:107)∞ =
≤
Theorem 1 (Convergence in the control setting). Let
be measurable and
Zk :=
suppose that

Zk−1 with Z0 ∈ Z
is ﬁnite. Then

. Let

X

T

A

lim
k→∞

inf
Z∗∗∈Z ∗∗

dp(Zk(x, a), Z ∗∗(x, a)) = 0

x, a.

∀

is ﬁnite, then Zk converges to

If
X
more, if there is a total ordering
Z ∗

∗,

≺

∗∗ uniformly. Further-
Z
on Π∗, such that for any

∈ Z
Z ∗ =

T
then

T

T

πZ ∗ with π

∈ GZ∗ , π
≺
has a unique ﬁxed point Z ∗

π(cid:48)

π(cid:48)
∀
∗.

∈ Z

The gist of the proof of Theorem 1 consists in showing that
for every state x, there is a time k after which the greedy
policy w.r.t. Qk is mostly optimal. To clearly expose the
steps involved, we will ﬁrst assume a unique (and there-
fore deterministic) optimal policy π∗, and later return to
the general case; we will denote the optimal action at x by
π∗(x). For notational convenience, we will write Qk :=
E Zk and
(cid:107)∞ <
Z
∞
and let (cid:15)k := γkB. We ﬁrst deﬁne the set of states
Xk ⊆ X
whose values must be sufﬁciently close to Q∗ at time k:

GZk . Let B := 2 supZ∈Z (cid:107)

Gk :=

(cid:110)

x : Q∗(x, π∗(x))

Xk :=

max
a(cid:54)=π∗(x)

−

Q∗(x, a) > 2(cid:15)k

(cid:111)
.

(11)

Indeed, by Lemma 4, we know that after k iterations

Qk(x, a)

Q∗(x, a)

γk

Q0(x, a)

Q∗(x, a)

−
−
, write a∗ := π∗(x). For any a

| ≤

|

(cid:15)k.

| ≤
, we deduce

∈ A

|
For x
that

∈ X

2(cid:15)k.

Qk(x, a∗)

Qk(x, a)

Q∗(x, a∗)

Q∗(x, a)

−

≥

−

= π∗(x):

−
∈ Xk, then also Qk(x, a∗) > Qk(x, a(cid:48))
It follows that if x
for all a(cid:48)
for these states, the greedy policy
πk(x) := arg maxa Qk(x, a) corresponds to the optimal
policy π∗.
Lemma 5. For each x
that,
k, x
arg maxa Qk(x, a) = π∗(x).

there exists a k such
∈ Xk(cid:48), and in particular

for all k(cid:48)

∈ X

≥

Proof. Because

A

is ﬁnite, the gap

∆(x) := Q∗(x, π∗(x))

max
a(cid:54)=π∗(x)

−

Q∗(x, a)

is attained for some strictly positive ∆(x) > 0. By deﬁni-
tion, there exists a k such that

(cid:15)k = γkB <

∆(x)
2

,

and hence every x

must eventually be in

Xk.

∈ X

This lemma allows us to guarantee the existence of an
iteration k after which sufﬁciently many states are well-
behaved, in the sense that the greedy policy at those states
chooses the optimal action. We will call these states
“solved”. We in fact require not only these states to be
solved, but also most of their successors, and most of the
successors of those, and so on. We formalize this notion as
follows: ﬁx some δ > 0, let
Xk, and deﬁne for
i > 0 the set

Xk,0 :=

Lemma 6. For any i
such that for all k(cid:48)

Xk,i, for any i.
∈ X

As the following lemma shows, any x is eventually con-
tained in the recursively-deﬁned sets
N and any x
∈ Xk(cid:48),i.
Proof. Fix i and let us suppose that
. By Lemma
Xk,i ↑ X
5, this is true for i = 0. We infer that for any probability
measure P on
) = 1. In particular, for
a given x

, there exists a k

Xk,i)

∈
k, x

, P (

→

≥

X

X

P (
∈ Xk, this implies that
x, π∗(x))
P (

P (

Xk,i |

→

X |

x, π∗(x)) = 1.

Therefore, for any x, there exists a time after which it is
Xk,i+1, the set of states for which
and remains a member of
1
P (
Xk,i+1 ↑
−

Xk−1,i |
≥
also. The statement follows by induction.

δ. We conclude that

x, π∗(x))

X

is

similar

Proof of Theorem 1. The proof
to policy
iteration-type results, but requires more care in dealing
with the metric and the possibly inﬁnite state space.
:= Zk(x, πk(x)), deﬁne W ∗
We will write Wk(x)
similarly and with some overload of notation write
Zk(x, πk+1(x)). Finally, let
T
∈ Xk,i] and ¯Sk
i (x).
i (x) = 1

Wk(x) := Wk+1(x) =
T
i (x) := I [x
Sk
−
Fix i > 0 and x
∈ Xk+1,i+1 ⊆ Xk. We begin by using
Lemma 1 to separate the transition from x into a solved
term and an unsolved term:

Sk

P πk Wk(x) = Sk

i Wk(X (cid:48)) + ¯Sk

i Wk(X (cid:48)),

where X (cid:48)
πk(x) := π∗(x), and we write Sk
¯Sk
i (X (cid:48)) to ease the notation. Similarly,

is the random successor from taking action
i =

i (X (cid:48)), ¯Sk

i = Sk

P πk W ∗(x) = Sk

i W ∗(X (cid:48)) + ¯Sk

i W ∗(X (cid:48)).

(cid:54)
A Distributional Perspective on Reinforcement Learning

Now

such that

dp(Wk+1(x), W ∗(x)) = dp(
T
γdp(P πk Wk(x), P π∗

(a)

W ∗(x))

Wk(x),

T

W ∗(x))

≤
(b)

≤

γdp(Sk
+ γdp( ¯Sk

i Wk(X (cid:48)), Sk
i Wk(X (cid:48)), ¯Sk

i W ∗(X (cid:48)))
i W ∗(X (cid:48))),

Now denote by
cies. If we take any Z ∗

Z

Zk+1 =

T

¯πk Zk−i+1.

∗∗ the set of nonstationary optimal poli-

∗, we deduce that

∈ Z

(12)

inf
Z∗∗∈Z ∗∗

dp(

T

¯πk Z ∗(x, a), Z ∗∗(x, a))

,

δB
γ

−

≤

1

where in (a) we used Properties P1 and P2 of the Wasser-
stein metric, and in (b) we separate states for which πk =
i , ¯Sk
π∗ from the rest using Lemma 1 (
Sk
form a parti-
i }
{
¯Sk
= E
i (X (cid:48))
tion of Ω). Let δi := Pr
=
∈ Xk,i}
}
{
{
¯Sk
i (X (cid:48))
(cid:107)p. From property P3 of the Wasserstein metric,
(cid:107)
we have

X (cid:48) /

since Z ∗ corresponds to some optimal policy π∗ and ¯πk is
optimal along most of the trajectories from (x, a). In effect,
¯πk Z ∗ is close to the value distribution of the nonstation-

T
ary optimal policy ¯πkπ∗. Now for this Z ∗,

dp(Zk(x, a), Z ∗∗(x, a))

inf
Z∗∗

≤

dp(Zk(x, a),
+ inf
Z∗∗

dp(

T

T

¯πk Z ∗(x, a))

¯πk Z ∗(x, a), Z ∗∗(x, a))

dp(Wk(x(cid:48)), W ∗(x(cid:48)))

dp(

T

≤

¯πk Zk−i+1(x, a),

T

¯πk Z ∗(x, a)) +

δB
γ

−

1

i (X (cid:48))Wk(x(cid:48)), ¯Sk

i (X (cid:48))W ∗(x(cid:48)))

dp( ¯Sk

i W ∗(X (cid:48)))
dp( ¯Sk

i Wk(X (cid:48)), ¯Sk
sup
x(cid:48)
¯Sk
i (X (cid:48))

≤

(cid:107)p sup

x(cid:48)

≤ (cid:107)

≤

δi sup
x(cid:48)
δiB.

dp(Wk(x(cid:48)), W ∗(x(cid:48)))

≤
Recall that B <
also δi < δ by our choice of x
bound the second term in (12) by γδB. This yields

(cid:107)∞. Since
Z
(cid:107)
∈ Xk+1,i+1, we can upper

is the largest attainable

∞

dp(Wk+1(x), W ∗(x))
γdp(Sk

≤

i Wk(X (cid:48)), Sk

i W ∗(X (cid:48))) + γδB.

By induction on i > 0, we conclude that for x
and some random state X (cid:48)(cid:48) i steps forward,

∈ Xk+i,i

dp(Wk+i(x), W ∗(x))

≤

γidp(Sk

0 Wk(X (cid:48)(cid:48)), Sk

0 W ∗(X (cid:48)(cid:48))) +

γiB +

≤

δB
γ

−

1

.

δB
γ

−

1

Hence for any x
, (cid:15) > 0, we can take δ, i, and ﬁnally k
large enough to make dp(Wk(x), W ∗(x)) < (cid:15). The proof
then extends to Zk(x, a) by considering one additional ap-
plication of

∈ X

.

We now consider the more general case where there are
multiple optimal policies. We expand the deﬁnition of
Xk,i
as follows:
Xk,i := (cid:8)x ∈ Xk : ∀π∗ ∈ Π∗, E

P (Xk−1,i−1 | x, a∗) ≥ 1−δ(cid:9),

a∗∼π∗(x)

T

Because there are ﬁnitely many actions, Lemma 6 also
holds for this new deﬁnition. As before, take x
∈ Xk,i, but
now consider the sequence of greedy policies πk, πk−1, . . .
selected by successive applications of

, and write

¯πk :=

T

πk

πk−1

T

T

· · · T

T
πk−i+1,

γiB +

≤

2δB
γ
1

−

,

using the same argument as before with the newly-deﬁned
Xk,i. It follows that

When

X

inf
Z∗∗∈Z ∗∗

dp(Zk(x, a), Z ∗∗(x, a))

0.

→

is ﬁnite, there exists a ﬁxed k after which

Xk =

. The uniform convergence result then follows.

X
To prove the uniqueness of the ﬁxed point Z ∗ when
se-
lects its actions according to the ordering
, we note that
for any optimal value distribution Z ∗, its set of greedy poli-
cies is Π∗. Denote by π∗ the policy coming ﬁrst in the or-
dering over Π∗. Then
, which has a unique ﬁxed
point (Section 3.3).

=

≺

π∗

T

T

T

Proposition 4. That
T
insufﬁcient to guarantee the convergence of

has a ﬁxed point Z ∗ =
Zk}
{

T
to

Z ∗ is
∗.

Z

We provide here a sketch of the result. Consider a single
state x1 with two actions, a1 and a2 (Figure 8). The ﬁrst
action yields a reward of 1/2, while the other either yields
0 or 1 with equal probability, and both actions are optimal.
Now take γ = 1/2 and write R0, R1, . . . for the received
rewards. Consider a stochastic policy that takes action a2
with probability p. For p = 0, the return is

Zp=0 =

1

1

γ

1
2

= 1.

−
For p = 1, on the other hand, the return is random and is
given by the following fractional number (in binary):

Zp=1 = R0.R1R2R3 · · ·

.

A Distributional Perspective on Reinforcement Learning

consider the d1 metric between this distribution P and an-
other distribution Q. The ﬁrst distribution is

P =

(cid:26) 0 w.p. 1/2
1 w.p. 1/2.

Figure 8. A simple example illustrating the effect of a nonstation-
ary policy on the value distribution.

As a result, Zp=1 is uniformly distributed between 0 and 2!
In fact, note that

Zp=0 = 0.11111

= 1.

· · ·

For some intermediary value of p, we obtain a different
probability of the different digits, but always putting some
probability mass on all returns in [0, 2].

Now suppose we follow the nonstationary policy that takes
a1 on the ﬁrst step, then a2 from there on. By inspec-
tion, the return will be uniformly distributed on the interval
[1/2, 3/2], which does not correspond to the return under
any value of p. But now we may imagine an operator
T
which alternates between a1 and a2 depending on the ex-
act value distribution it is applied to, which would in turn
converge to a nonstationary optimal value distribution.
be a
Lemma 7 (Sample Wasserstein distance). Let
Pi}
{
N a random index
collection of random variables, I
independent from
, and consider the mixture random
variable P = PI . For any random variable Q independent
of I,

Pi}

∈

{

dp(P, Q)

≤

E
i∼I

dp(Pi, Q),

and in general the inequality is strict and

∇Qdp(PI , Q)

= E

i∼I ∇Qdp(Pi, Q).

Proof. We prove this using Lemma 1. Let Ai := I [I = i].
We write

dp(P, Q) = dp(PI , Q)

(cid:16) (cid:88)

AiPi,

i

(cid:88)
i

(cid:17)

AiQ

dp(AiPi, AiQ)

i

= dp
(cid:88)

≤

(cid:88)

dp(Pi, Q)
Pr
I = i
}
≤
{
= EI dP (Pi, Q).

i

where in the penultimate line we used the independence of
I from Pi and Q to appeal to property P3 of the Wasserstein
metric.

To show that the bound is in general strict, consider the
mixture distribution depicted in Figure 9. We will simply

In this example, i
, P1 = 0, and P2 = 1. Now
}
consider the distribution with the same support but that puts
probability p on 0:

∈ {

1, 2

Q =

(cid:26) 0 w.p. p
1 w.p. 1

p.

−

The distance between P and Q is

|

p

d1(P, Q) =

1
.
2 |
This is d1(P, Q) = 1
, and strictly less than
}
∈ {
1
2 for any other values of p. On the other hand, the corre-
sponding expected distance (after sampling an outcome x1
or x2 with equal probability) is

2 for p

0, 1

−

EI d1(Pi, Q) = 1

2 p + 1

2 (1

p) = 1
2 .

−

Hence d1(P, Q) < EI d1(Pi, Q) for p
(0, 1). This shows
that the bound is in general strict. By inspection, it is clear
that the two gradients are different.

∈

Figure 9. Example MDP in which the expected sample Wasser-
stein distance is greater than the Wasserstein distance.

Proposition 5. Fix some next-state distribution Z and pol-
icy π. Consider a parametric value distribution Zθ, and
and deﬁne the Wasserstein loss

LW (θ) := dp(Zθ(x, a), R(x, a) + γZ(X (cid:48), π(X (cid:48)))).

Let r
sample loss

∼

R(x, a) and x(cid:48)

P (

· |

∼

x, a) and consider the

LW (θ, r, x(cid:48)) := dp(Zθ(x, a), r + γZ(x(cid:48), π(x(cid:48))).

Its expectation is an upper bound on the loss

LW :

LW (θ)

≤

E
R,P

LW (θ, r, x(cid:48)),

in general with strict inequality.

The result follows directly from the previous lemma.

R = 1/2R = 0 or 1x1a1a2R = 0R = 1xx1x2½½(cid:54)
A Distributional Perspective on Reinforcement Learning

Figure 10. (a) Wasserstein distance between ground truth distribution Z π and approximating distributions Zθ. Varying number of atoms
in approximation, training target, and loss function. (b) Approximate cumulative distributions for ﬁve representative states in CliffWalk.

C. Algorithmic Details

While our training regime closely follows that of DQN
(Mnih et al., 2015), we use Adam (Kingma & Ba, 2015)
instead of RMSProp (Tieleman & Hinton, 2012) for gra-
dient rescaling. We also performed some hyperparam-
eter tuning for our ﬁnal results. Speciﬁcally, we eval-
uated two hyperparameters over our ﬁve training games
and choose the values that performed best. The hyperpa-
rameter values we considered were VMAX ∈ {
3, 10, 100
}
,
and (cid:15)adam ∈ {
1/L, 0.1/L, 0.01/L, 0.001/L, 0.0001/L
}
where L = 32 is the minibatch size. We found VMAX = 10
and (cid:15)adam = 0.01/L performed best. We used the same
step-size value as DQN (α = 0.00025).

Pseudo-code for the categorical algorithm is given in Algo-
rithm 1. We apply the Bellman update to each atom sepa-
rately, and then project it into the two nearest atoms in the
original support. Transitions to a terminal state are handled
with γt = 0.

D. Comparison of Sampled Wasserstein Loss

and Categorical Projection

T

Lemma 3 proves that for a ﬁxed policy π the distributional
Bellman operator is a γ-contraction in ¯dp, and therefore
π will converge in distribution to the true distribution
that
of returns Z π. In this section, we empirically validate these
results on the CliffWalk domain shown in Figure 11. The
dynamics of the problem match those given by Sutton &
Barto (1998). We also study the convergence of the distri-
butional Bellman operator under the sampled Wasserstein
loss and the categorical projection (Equation 7) while fol-

Figure 11. CliffWalk Environment (Sutton & Barto, 1998).

lowing a policy that tries to take the safe path but has a 10%
chance of taking another action uniformly at random.

We compute a ground-truth distribution of returns Z π using
10000 Monte-Carlo (MC) rollouts from each state. We then
perform two experiments, approximating the value distri-
bution at each state with our discrete distributions.

In the ﬁrst experiment, we perform supervised learning us-
ing either the Wasserstein loss or categorical projection
(Equation 7) with cross-entropy loss. We use Z π as the
supervised target and perform 5000 sweeps over all states
to ensure both approaches have converged. In the second
experiment, we use the same loss functions, but the training
target comes from the one-step distributional Bellman op-
erator with sampled transitions. We use VMIN =
100 and
1.4 For the sample updates we perform 10 times
VMAX =
as many sweeps over the state space. Fundamentally, these
experiments investigate how well the two training regimes

−

−

4Because there is a small probability of larger negative returns,
some approximation error is unavoidable. However, this effect is
relatively negligible in our experiments.

# AtomsWassersteinCategoricalMonte-Carlo TargetStochastic Bellman TargetWassersteinCategoricald1(Z⇡,Z✓)ReturnFZ(a)(b)The CliﬀSGsafe pathoptimal pathr = -1r = -100A Distributional Perspective on Reinforcement Learning

(minimizing the Wasserstein or categorical loss) minimize
the Wasserstein metric under both ideal (supervised target)
and practical (sampled one-step Bellman target) conditions.

In Figure 10a we show the ﬁnal Wasserstein distance
d1(Z π, Zθ) between the learned distributions and the
ground-truth distribution as we vary the number of atoms.
The graph shows that the categorical algorithm does indeed
minimize the Wasserstein metric in both the supervised and
sample Bellman setting. It also highlights that minimizing
the Wasserstein loss with stochastic gradient descent is in
general ﬂawed, conﬁrming the intuition given by Propo-
sition 5.
In repeat experiments the process converged to
different values of d1(Z π, Zθ), suggesting the presence of
local minima (more prevalent with fewer atoms).

Figure 10 provides additional insight into why the sampled
Wasserstein distance may perform poorly. Here, we see the
cumulative densities for the approximations learned under
these two losses for ﬁve different states along the safe path
in CliffWalk. The Wasserstein has converged to a ﬁxed-
point distribution, but not one that captures the true (Monte
Carlo) distribution very well. By comparison, the categor-
ical algorithm captures the variance of the true distribution
much more accurately.

E. Supplemental Videos and Results

In Figure 13 we provide links to supplemental videos show-
ing the C51 agent during training on various Atari 2600
games. Figure 12 shows the relative performance of C51
over the course of training. Figure 14 provides a table
of evaluation results, comparing C51 to other state-of-the-
art agents. Figures 15–18 depict particularly interesting
frames.

Figure 12. Number of Atari games where an agent’s training per-
formance is greater than a baseline (fully trained DQN & human).
Error bands give standard deviations, and averages are over num-
ber of games.

GAMES
Freeway
Pong
Q*Bert
Seaquest
Space Invaders

VIDEO URL
http://youtu.be/97578n9kFIk
http://youtu.be/vIz5P6s80qA
http://youtu.be/v-RbNX4uETw
http://youtu.be/d1yz4PNFUjI
http://youtu.be/yFBwyPuO2Vg

Figure 13. Supplemental videos of C51 during training.

# Games SuperiorTraining Frames (millions)C51 vs. DQNC51 vs. HUMANDQN vs. HUMANA Distributional Perspective on Reinforcement Learning

GAMES
Alien
Amidar
Assault
Asterix
Asteroids
Atlantis
Bank Heist
Battle Zone
Beam Rider
Berzerk
Bowling
Boxing
Breakout
Centipede
Chopper Command
Crazy Climber
Defender
Demon Attack
Double Dunk
Enduro
Fishing Derby
Freeway
Frostbite
Gopher
Gravitar
H.E.R.O.
Ice Hockey
James Bond
Kangaroo
Krull
Kung-Fu Master
Montezuma’s Revenge
Ms. Pac-Man
Name This Game
Phoenix
Pitfall!
Pong
Private Eye
Q*Bert
River Raid
Road Runner
Robotank
Seaquest
Skiing
Solaris
Space Invaders
Star Gunner
Surround
Tennis
Time Pilot
Tutankham
Up and Down
Venture
Video Pinball
Wizard Of Wor
Yars’ Revenge
Zaxxon

RANDOM
227.8
5.8
222.4
210.0
719.1
12,850.0
14.2
2,360.0
363.9
123.7
23.1
0.1
1.7
2,090.9
811.0
10,780.5
2,874.5
152.1
-18.6
0.0
-91.7
0.0
65.2
257.6
173.0
1,027.0
-11.2
29.0
52.0
1,598.0
258.5
0.0
307.3
2,292.3
761.4
-229.4
-20.7
24.9
163.9
1,338.5
11.5
2.2
68.4
-17,098.1
1,236.3
148.0
664.0
-10.0
-23.8
3,568.0
11.4
533.4
0.0
16,256.9
563.5
3,092.9
32.5

HUMAN
7,127.7
1,719.5
742.0
8,503.3
47,388.7
29,028.1
753.1
37,187.5
16,926.5
2,630.4
160.7
12.1
30.5
12,017.0
7,387.8
35,829.4
18,688.9
1,971.0
-16.4
860.5
-38.7
29.6
4,334.7
2,412.5
3,351.4
30,826.4
0.9
302.8
3,035.0
2,665.5
22,736.3
4,753.3
6,951.6
8,049.0
7,242.6
6,463.7
14.6
69,571.3
13,455.0
17,118.0
7,845.0
11.9
42,054.7
-4,336.9
12,326.7
1,668.7
10,250.0
6.5
-8.3
5,229.2
167.6
11,693.2
1,187.5
17,667.9
4,756.5
54,576.9
9,173.3

DQN
1,620.0
978.0
4,280.4
4,359.0
1,364.5
279,987.0
455.0
29,900.0
8,627.5
585.6
50.4
88.0
385.5
4,657.7
6,126.0
110,763.0
23,633.0
12,149.4
-6.6
729.0
-4.9
30.8
797.4
8,777.4
473.0
20,437.8
-1.9
768.5
7,259.0
8,422.3
26,059.0
0.0
3,085.6
8,207.8
8,485.2
-286.1
19.5
146.7
13,117.3
7,377.6
39,544.0
63.9
5,860.6
-13,062.3
3,482.8
1,692.3
54,282.0
-5.6
12.2
4,870.0
68.1
9,989.9
163.0
196,760.4
2,704.0
18,098.9
5,363.0

DDQN
3,747.7
1,793.3
5,393.2
17,356.5
734.7
106,056.0
1,030.6
31,700.0
13,772.8
1,225.4
68.1
91.6
418.5
5,409.4
5,809.0
117,282.0
35,338.5
58,044.2
-5.5
1,211.8
15.5
33.3
1,683.3
14,840.8
412.0
20,130.2
-2.7
1,358.0
12,992.0
7,920.5
29,710.0
0.0
2,711.4
10,616.0
12,252.5
-29.9
20.9
129.7
15,088.5
14,884.5
44,127.0
65.1
16,452.7
-9,021.8
3,067.8
2,525.5
60,142.0
-2.9
-22.8
8,339.0
218.4
22,972.2
98.0
309,941.9
7,492.0
11,712.6
10,163.0

DUEL
4,461.4
2,354.5
4,621.0
28,188.0
2,837.7
382,572.0
1,611.9
37,150.0
12,164.0
1,472.6
65.5
99.4
345.3
7,561.4
11,215.0
143,570.0
42,214.0
60,813.3
0.1
2,258.2
46.4
0.0
4,672.8
15,718.4
588.0
20,818.2
0.5
1,312.5
14,854.0
11,451.9
34,294.0
0.0
6,283.5
11,971.1
23,092.2
0.0
21.0
103.0
19,220.3
21,162.6
69,524.0
65.3
50,254.2
-8,857.4
2,250.8
6,427.3
89,238.0
4.4
5.1
11,666.0
211.4
44,939.6
497.0
98,209.5
7,855.0
49,622.1
12,944.0

PRIOR. DUEL.
3,941.0
2,296.8
11,477.0
375,080.0
1,192.7
395,762.0
1,503.1
35,520.0
30,276.5
3,409.0
46.7
98.9
366.0
7,687.5
13,185.0
162,224.0
41,324.5
72,878.6
-12.5
2,306.4
41.3
33.0
7,413.0
104,368.2
238.0
21,036.5
-0.4
812.0
1,792.0
10,374.4
48,375.0
0.0
3,327.3
15,572.5
70,324.3
0.0
20.9
206.0
18,760.3
20,607.6
62,151.0
27.5
931.6
-19,949.9
133.4
15,311.5
125,117.0
1.2
0.0
7,553.0
245.9
33,879.1
48.0
479,197.0
12,352.0
69,618.1
13,886.0

C51
3,166
1,735
7,203
406,211
1,516
841,075
976
28,742
14,074
1,645
81.8
97.8
748
9,646
15,600
179,877
47,092
130,955
2.5
3,454
8.9
33.9
3,965
33,641
440
38,874
-3.5
1,909
12,853
9,735
48,192
0.0
3,415
12,542
17,490
0.0
20.9
15,095
23,784
17,322
55,839
52.3
266,434
-13,901
8,342
5,747
49,095
6.8
23.1
8,329
280
15,612
1,520
949,604
9,300
35,050
10,513

Figure 14. Raw scores across all games, starting with 30 no-op actions. Reference values from Wang et al. (2016).

A Distributional Perspective on Reinforcement Learning

Figure 15. FREEWAY: Agent differentiates action-value distributions under pressure.

Figure 16. Q*BERT: Top, left and right: Predicting which actions are unrecoverably fatal. Bottom-Left: Value distribution shows steep
consequences for wrong actions. Bottom-Right: The agent has made a huge mistake.

Figure 17. SEAQUEST: Left: Bimodal distribution. Middle: Might hit the ﬁsh. Right: Deﬁnitely going to hit the ﬁsh.

Figure 18. SPACE INVADERS: Top-Left: Multi-modal distribution with high uncertainty. Top-Right: Subsequent frame, a more certain
demise. Bottom-Left: Clear difference between actions. Bottom-Middle: Uncertain survival. Bottom-Right: Certain success.

