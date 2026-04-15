|            |     | Phasic |        | Policy | Gradient |        |      |          |
| ---------- | --- | ------ | ------ | ------ | -------- | ------ | ---- | -------- |
| Karl Cobbe |     | Jacob  | Hilton |        | Oleg     | Klimov | John | Schulman |
0202 peS 9  ]GL.sc[  1v61440.9002:viXra karl@openai.com jhilton@openai.com oleg@openai.com joschu@openai.com
Abstract
| We introduce  |     | Phasic                                         | Policy | Gradient    | (PPG),    | a reinforcement |          | learn-     |
| ------------- | --- | ---------------------------------------------- | ------ | ----------- | --------- | --------------- | -------- | ---------- |
| ing framework |     | which modifies                                 |        | traditional | on-policy | actor-critic    |          | methods    |
| by separating |     | policy and                                     | value  | function    | training  | into            | distinct | phases. In |
| priormethods, |     | onemustchoosebetweenusingasharednetworkorsepa- |        |             |           |                 |          |            |
| rate networks |     | to represent                                   | the    | policy      | and value | function.       | Using    | separate   |
networksavoidsinterferencebetweenobjectives,whileusingasharednet-
| workallowsusefulfeaturestobeshared.       |        |                   |     |              | PPGisabletoachievethebest |                        |       |           |
| ----------------------------------------- | ------ | ----------------- | --- | ------------ | ------------------------- | ---------------------- | ----- | --------- |
| of both                                   | worlds | by splitting      |     | optimization | into                      | two phases,            | one   | that ad-  |
| vancestrainingandonethatdistillsfeatures. |        |                   |     |              |                           | PPGalsoenablesthevalue |       |           |
| function                                  | to be  | more aggressively |     | optimized    | with                      | a higher               | level | of sample |
reuse. ComparedtoPPO,wefindthatPPGsignificantlyimprovessample
| efficiency | on the | challenging |     | Procgen | Benchmark. |     |     |     |
| ---------- | ------ | ----------- | --- | ------- | ---------- | --- | --- | --- |
1 Introduction
Modelfreereinforcementlearning(RL)hasenjoyedremarkablesuccessinrecent
years,achievingimpressiveresultsindiversedomainsincludingDoTA(OpenAI
et al., 2019b), Starcraft II (Vinyals et al., 2019), and robotic control (OpenAI
et al., 2019a). Although policy gradient methods like PPO (Schulman et al.,
2017),A3C(Mnihetal.,2016),andIMPALA(Espeholtetal.,2018)arebehind
some of the most high profile results, many related algorithms have proposed
a variety of policy objectives (Schulman et al., 2015a; Wu et al., 2017; Peng
et al., 2019; Song et al., 2019; Lillicrap et al., 2015; Haarnoja et al., 2018). All
of these algorithms fundamentally rely on the actor-critic framework, with two
key quantities driving learning: the policy and the value function. In practice,
whether or not to share parameters between the policy and the value function
networks is an important implementation decision. There is a clear advantage
to sharing parameters: features trained by each objective can be used to better
optimize the other.
| However,therearealsodisadvantagestosharingnetworkparameters. |     |     |     |     |     |     |     | First, |
| ------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | ------ |
it is not clear how to appropriately balance the competing objectives of the
policyandthevaluefunction. Anymethodthatjointlyoptimizesthesetwoob-
jectiveswiththesamenetworkmustassignarelativeweighttoeach. Regardless
of how well this hyperparameter is chosen, there is a risk that the optimization
of one objective will interfere with the optimization of the other. Second, the
1

useofasharednetworkallbutrequiresthepolicyandvaluefunctionobjectives
to be trained with the same data, and consequently the same level of sample
| reuse. This | is  | an artificial | and | undesirable | restriction. |     |     |     |
| ----------- | --- | ------------- | --- | ----------- | ------------ | --- | --- | --- |
WeaddresstheseproblemswithPhasicPolicyGradient(PPG),analgorithm
whichpreservesthefeaturesharingbetweenthepolicyandvaluefunction,while
otherwise decoupling their training. PPG operates in two alternating phases:
the first phase trains the policy, and the second phase distills useful features
from the value function. More generally, PPG can be used to perform any
auxiliaryoptimizationalongsideRL,thoughinthisworkwetakevaluefunction
errortobethesoleauxiliaryobjective. UsingPPG,wehighlighttwoimportant
| observations | about | on-policy | actor-critic |     | methods: |     |     |     |
| ------------ | ----- | --------- | ------------ | --- | -------- | --- | --- | --- |
1. Interferencebetweenpolicyandvaluefunctionoptimizationcannegatively
| impact        | performance |              | when         | parameters    |           | are shared between | the policy     | and      |
| ------------- | ----------- | ------------ | ------------ | ------------- | --------- | ------------------ | -------------- | -------- |
| the           | value       | function     | networks.    |               |           |                    |                |          |
| 2. Value      | function    | optimization |              | often         | tolerates | a significantly    | higher         | level of |
| sample        | reuse       | than         | policy       | optimization. |           |                    |                |          |
| By mitigating |             | the          | interference | between       |           | the policy and     | value function | ob-      |
jectives while still sharing representations, and by optimizing each with the
appropriate level of sample reuse, PPG significantly improves sample efficiency.
2 Algorithm
In PPG, training proceeds in two alternating phases: the policy phase, followed
by the auxiliary phase. During the policy phase, we train the agent with Prox-
imal Policy Optimization (PPO) (Schulman et al., 2017). During the auxiliary
phase, we distill features from the value function into the policy network, to
improve training in future policy phases. Compared to PPO, the novel contri-
bution of PPG is the inclusion of periodic auxiliary phases. We now describe
| each phase | in  | more detail. |     |     |     |     |     |     |
| ---------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
Duringthepolicyphase,weoptimizethesameobjectivesfromPPO,notably
usingdisjointnetworkstorepresentthepolicyandthevaluefunction(Figure1).
Specifically, we train the policy network using the clipped surrogate objective
|     |     |           | (cid:104) |              |     |                               | (cid:105) |     |
| --- | --- | --------- | --------- | ------------ | --- | ----------------------------- | --------- | --- |
|     |     | Lclip =Eˆ |           | (θ)Aˆ,clip(r |     | (θ),1−(cid:15),1+(cid:15))Aˆ) |           |     |
|     |     |           | t min(r   | t            | t t |                               | t         |     |
|     |     | πθ(at|st) |           | Aˆ           |     |                               |           |     |
where r t (θ) = , and t is an estimator of the advantage function at
πθold (at|st)
timestep t. We optimize Lclip+β S[π], where β is a constant and S is a an
|     |     |     |     | S   |     | S   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
entropy bonus for the policy. To train the value function network, we optimize
|               |     |         |            | (cid:20) 1 |            | (cid:21)   |              |      |
| ------------- | --- | ------- | ---------- | ---------- | ---------- | ---------- | ------------ | ---- |
|               |     |         | Lvalue =Eˆ |            |            | )−Vˆtarg)2 |              |      |
|               |     |         |            | t          | (V θV (s t |            |              |      |
|               |     |         |            | 2          |            | t          |              |      |
| Vˆtarg        |     |         |            |            |            | Aˆ Vˆtarg  |              |      |
| where         | are | value   | function   | targets.   | Both       | and        | are computed | with |
| GAE (Schulman |     | et al., | 2015b).    |            |            |            |              |      |
2

Figure 1: PPG uses disjoint policy and value networks to reduce interference
between objectives. The policy network includes an auxiliary value head.
During the auxiliary phase, we optimize the policy network with a joint
objectivethatincludesanarbitraryauxiliarylossandabehavioralcloningloss:
Ljoint =Laux+β ·Eˆ [KL[π (·|s ),π (·|s )]]
clone t θold t θ t
where π is the policy right before the auxiliary phase begins. That is, we
θold
optimize the auxiliary objective while otherwise preserving the original policy,
with the hyperparameter β controlling this trade-off. In principle Laux
clone
could be any auxiliary objective. At present, we simply use the value function
loss as the auxiliary objective, thereby sharing features between the policy and
valuefunctionwhileminimizingdistortionstothepolicy. Specifically,wedefine
1 (cid:104) (cid:105)
Laux = ·Eˆ (V (s )−Vˆtarg)2
2 t θπ t t
where V is an auxiliary value head of the policy network, shown in Figure 1.
θπ
Algorithm 1 PPG
for phase = 1,2,... do
Initialize empty buffer B
for iteration = 1,2,...,N do (cid:46) Policy Phase
π
Perform rollouts under current policy π
Compute value function target Vˆtarg for each state s
t t
for epoch = 1,2,...,E do (cid:46) Policy Epochs
π
Optimize Lclip+β S[π] wrt θ
S π
for epoch = 1,2,...,E do (cid:46) Value Epochs
V
Optimize Lvalue wrt θ
V
Add all (s , Vˆtarg) to B
t t
Compute and store current policy π (·|s ) for all states s in B
θold t t
for epoch = 1,2,...,E do (cid:46) Auxiliary Phase
aux
Optimize Ljoint wrt θ , on all data in B
π
Optimize Lvalue wrt θ , on all data in B
V
3

Figure 2: Sample efficiency of PPG compared to a PPO baseline
This auxiliary value head and policy itself share all parameters except for
the final linear layers. The auxiliary value head is used purely to train repre-
sentationsforthepolicy; ithasnootherpurposeinPPG.Notethatthetargets
Vˆtargarethesametargetscomputedduringthepolicyphase. Theyremainfixed
throughout the auxiliary phase. During the auxiliary phase, we also take the
opportunity to perform additional training on the value network by further op-
timizing Lvalue. Note that Lvalue and Ljoint share no parameter dependencies,
so we can optimize these objectives separately.
Webrieflyexplaintheroleofeachhyperparameter. N controlsthenumber
π
of policy updates performed in each policy phase. E and E control the
π V
sample reuse for the policy and value function respectively, during the policy
phase. Although these are conventionally set to the same value, this is not a
strict requirement in PPG. Note that E influences the training of the true
V
valuefunction, nottheauxiliaryvaluefunction. E controlsthesamplereuse
aux
duringtheauxiliaryphase,representingthenumberofepochsperformedacross
all data in the replay buffer. It is usually by increasing E , rather than
aux
E , that we increase sample reuse for value function training. For a detailed
V
discussion on the relationship between E and E , see Appendix C. Default
aux V
values for all hyperparameters can be found in Appendix A. Code for PPG can
be found at https://github.com/openai/phasic-policy-gradient.
3 Experiments
We report results on the environments in Procgen Benchmark (Cobbe et al.,
2019). This benchmark was designed to be highly diverse, and we expect im-
4

| Figure | 3: Performance | with varying | levels of policy | sample reuse |     |
| ------ | -------------- | ------------ | ---------------- | ------------ | --- |
provementsonthisbenchmarktotransferwelltomanyotherRLenvironments.
Throughout all experiments, we use the hyperparameters found in Appendix A
unless otherwise specified. When feasible, we compute and visualize the stan-
| dard deviation | across 3 separate | runs. |     |     |     |
| -------------- | ----------------- | ----- | --- | --- | --- |
| 3.1 Comparison | to                | PPO   |     |     |     |
We begin by comparing our implementation of PPG to the highly tuned imple-
mentation of PPO from Cobbe et al. (2019). We note that this implementation
of PPO uses a near optimal level of sample reuse and a near optimal relative
weightforthevalueandpolicylosses,asdeterminedbyahyperparametersweep.
ResultsareshowninFigure2. WecanseethatPPGachievessignificantlybetter
| sample efficiency | than PPO         | in nearly  | every environment. |                 |     |
| ----------------- | ---------------- | ---------- | ------------------ | --------------- | --- |
| We have           | noticed that the | importance | of representation  | sharing between | the |
policy and value function does seem to vary between environments. While it is
criticaltoshareparametersbetweenthepolicyandthevaluefunctioninProcgen
environments (see Appendix B), this is often unnecessary in environments with
a lower dimensional input space (Haarnoja et al., 2018). We conjecture that
the high dimensional input space in Procgen contributes to the importance of
sharingrepresentationsbetweenthepolicyandthevaluefunction. Wetherefore
believe it is in environments such as these, particularly those with vision-based
observations, that PPG is most likely to outperform PPO and other similar
algorithms.
5

| Figure     | 4: Performance |        | with varying | levels | of value function | sample | reuse |
| ---------- | -------------- | ------ | ------------ | ------ | ----------------- | ------ | ----- |
| 3.2 Policy |                | Sample | Reuse        |        |                   |        |       |
In PPO, choosing the optimal level of sample reuse is not straightforward. In-
creasing sample reuse in PPO implies performing both additional policy opti-
mization and additional value function optimization. This leads to an undesir-
able confounding of effects, making it harder to analyze the impact of policy
sample reuse alone. Empirically, we find that performing 3 epochs per rollout
| is best | in PPO, | given | our other hyperparameter |          | settings       | (see Appendix | D).          |
| ------- | ------- | ----- | ------------------------ | -------- | -------------- | ------------- | ------------ |
| In PPG, | policy  | and   | value function           | training | are decoupled, | and           | we can train |
each with different levels of sample reuse. In order to better understand the
impact of policy sample reuse, we choose to vary the number of policy epochs
(E ) without changing the number of value function epochs (E ). Results are
| π        |        |     |     |     |     | V   |     |
| -------- | ------ | --- | --- | --- | --- | --- | --- |
| shown in | Figure | 3.  |     |     |     |     |     |
Aswecansee,trainingwithasinglepolicyepochisalmostalwaysoptimalor
near-optimalinPPG.ThissuggeststhatthePPObaselinebenefitsfromgreater
samplereuseonlybecausetheextraepochsofferadditionalvaluefunctiontrain-
ing. Whenvaluefunctionandpolicytrainingareproperlyisolated, weseelittle
benefit from training the policy beyond a single epoch. Of course, various hy-
perparameters will influence this result. If we use an artificially low learning
rate, for instance, it will become advantageous to increase policy sample reuse.
Our present conclusion is simply that when using well-tuned hyperparameters,
| performing | a single | policy | epoch is | near-optimal. |     |     |     |
| ---------- | -------- | ------ | -------- | ------------- | --- | --- | --- |
6

| Figure    | 5: Performance | with varying | auxiliary | phase frequency |     |
| --------- | -------------- | ------------ | --------- | --------------- | --- |
| 3.3 Value | Sample         | Reuse        |           |                 |     |
We now evaluate how performing additional epochs during the auxiliary phase
impactsperformance. Weexpecttheretobeatrade-off: usingtoomanyepochs
runs the risk of overfitting to recent data, while using fewer epochs will lead to
slowertraining. Wevarythenumberofauxiliaryepochs(E )from1to9and
aux
| report results | in Figure 4. |     |     |     |     |
| -------------- | ------------ | --- | --- | --- | --- |
Wefindthattrainingwithadditionalauxiliaryepochsisgenerallybeneficial,
withperformancetaperingoffaround6auxiliaryepochs. Wenotethattraining
with additional auxiliary epochs offers two possible benefits. First, due to the
optimizationof Ljoint, wemayexpectbetter-trainedfeaturestobesharedwith
the policy. Second, due to the optimization of Lvalue, we may expect to train
a more accurate value function, thereby reducing the variance of the policy
gradient in future policy phases. In general, which benefit is more significant
is likely to vary between environments. In Procgen environments, the feature
sharingbetweenpolicyandvaluenetworksappearstoplaythemorecriticalrole.
For a more detailed discussion of the relationship between these two objectives,
| see Appendix  | C.    |           |     |     |     |
| ------------- | ----- | --------- | --- | --- | --- |
| 3.4 Auxiliary | Phase | Frequency |     |     |     |
Wenextinvestigatealternatingbetweenpolicyandauxiliaryphasesatdifferent
frequencies, controlled by the hyperparameter N . As described in Section 2,
π
we perform each auxiliary phase after every N π policy updates. We vary this
| hyperparameter | from 2 to        | 32 and report | results in Figure | 5.               |     |
| -------------- | ---------------- | ------------- | ----------------- | ---------------- | --- |
| It is clear    | that performance | suffers when  | we perform        | auxiliary phases | too |
7

Figure6: Theimpactofreplacingtheclippingobjective(Lclip)withafixedKL
(LKL)
penalty objective
frequently. We conjecture that each auxiliary phase interferes with policy op-
timization, and that performing frequent auxiliary phases exacerbates this ef-
fect. It’s possible that future research will uncover more clever optimization
techniques to mitigate this interference. For now, we conclude that relatively
| infrequent | auxiliary phases | are critical | to success. |     |     |
| ---------- | ---------------- | ------------ | ----------- | --- | --- |
| 3.5 KL     | Penalty          | vs Clipping  |             |     |     |
As an alternative to clipping, Schulman et al. (2017) proposed using an adap-
tively weighted KL penalty. We now investigate the use of a KL penalty in
PPG, but we instead choose to keep the relative weight of this penalty fixed.
Specifically, we set the policy gradient loss (excluding the entropy bonus) to be
|     | (cid:20) |             |          |          | (cid:21) |
| --- | -------- | ----------- | -------- | -------- | -------- |
|     | =Eˆ −Aˆ  | π θ (a t |s | t )      |          |          |
|     | LKL      |             | +β ·KL[π | (·|s ),π | (·|s )]  |
|     | t        | tπ (a       | |s ) π   | θold t   | θ t      |
θold t t
where β controls the weight of the KL penalty. After performing a hyperpa-
π
rameter sweep, we set β to 1. Results are shown in Figure 6. We find that
π
a fixed KL penalty objective performs remarkably similarly to clipping when
usingPPG.Wesuspectthatusingclipping(oranadaptiveKLpenalty)ismore
important when rewards are poorly scaled. We avoid this concern by normal-
izing rewards so that discounted returns have approximately unit variance. In
any case, we highlight the effectiveness of the KL penalty variant of PPG since
LKL is arguably easier to analyze than Lclip, and since future work may wish
| to build | upon either objective. |     |     |     |     |
| -------- | ---------------------- | --- | --- | --- | --- |
8

Figure 7: A comparison between the default implementation of PPG which
trains two separate networks, and a single-network variant that mimics the
same training dynamics by detaching the gradient when necessary. PPO shown
for reference.
| 3.6 Single-Network |     | PPG |     |     |
| ------------------ | --- | --- | --- | --- |
By default, PPG comes with an increased memory footprint. Since we use
disjoint policy and value function networks instead of a single unified network,
weuseapproximatelytwiceasmanyparameterscomparedtothePPObaseline.
WecanrecoverthiscostandmaintainmostofthekeybenefitsofPPGbyusing
asinglenetworkthatappropriatelydetachesthevaluefunctiongradient. During
the policy phase, we detach the value function gradient at the last layer shared
betweenthepolicyandvalueheads,preventingthevaluefunctiongradientfrom
influencing shared parameters. During the auxiliary phase, we take the value
function gradient with respect to all parameters, including shared parameters.
Thisallowsustobenefitfromtherepresentationslearnedbythevaluefunction,
| while still | removing the interference | during           | the policy phase. |                 |
| ----------- | ------------------------- | ---------------- | ----------------- | --------------- |
| As we       | can see, using PPG        | with this single | shared network    | performs almost |
as well as PPG with a dual network architecture. We were initially concerned
that the value function might be unable to train well during the policy phase
with the detached gradient, but in practice this does not appear to be a major
problem. We believe this is because the value function can still train from the
| full gradient | during the auxiliary | phase. |     |     |
| ------------- | -------------------- | ------ | --- | --- |
| 4 Related     | Work                 |        |     |     |
Igl et al. (2020) recently proposed Iterative Relearning (ITER) to reduce the
9

impactofnon-stationarityduringRLtraining. ITERandPPGshareastriking
similarity: bothalgorithmsalternatebetweenastandardRLphaseandadistil-
lation phase. However, the nature and purpose of the distillation phase varies.
In ITER, the policy and value function teachers are periodically distilled into
newly initialized student networks, in an effort to improve generalization. In
PPG, the value function network is periodically distilled into the policy net-
work, in an effort to improve sample efficiency.
Prior work has considered the role the value function plays as an auxiliary
task. Bellemare et al. (2019) investigate using value functions to train useful
representations, specifically focusing on a special class of value functions called
Adversarial Value Functions (AVFs). They find that AVFs provide a useful
auxiliaryobjectiveinthe four-roomdomain. Lyleetal.(2019)suggestthatthe
benefits of distributional RL (Bellemare et al., 2017) can perhaps be attributed
to the rich signal the value function distribution provides as an auxiliary task.
We find that the representation learning performed by the value function is
indeed critical in Procgen environments, although we consider only the value
function of the current policy, and we do not model the full value distribution.
Off-policy algorithms like Soft Actor-Critic (SAC) (Haarnoja et al., 2018),
DeepDeterministicPolicyGradient(DDPG)(Lillicrapetal.,2015),andActor-
Critic with Experience Replay (ACER) (Wang et al., 2016) all employ replay
buffers to improve sample efficiency via off-policy updates. PPG also utilizes a
replay buffer, specifically when performing updates during the auxiliary phase.
However, unlike these algorithms, PPG does not attempt to improve the policy
fromoff-policydata. Rather,thisreplaybufferdataisusedonlytobetterfitthe
value targets and to better train features for the policy. SAC also notably uses
separate policy and value function networks, presumably, like PPG, to avoid
interference between their respective objectives.
AlthoughweusetheclippedsurrogateobjectivefromPPO(Schulmanetal.,
2017) throughout this work, PPG is in principle compatible with the policy
objectives from any actor-critic algorithm. Andrychowicz et al. (2020) recently
performed a rigorous empirical comparison of many relevant algorithms in the
on-policy setting. In particular, AWR (Peng et al., 2019) and V-MPO (Song
et al., 2019) propose alternate policy objectives that move the current policy
towards one which weights the likelihood of each action by the exponentiated
advantageofthataction. SuchobjectivescouldbeusedinPPG,inplaceofthe
PPO objective.
There are also several trust region methods, similar in spirit to PPO, that
would be compatible with PPG. Trust Region Policy Optimization (TRPO)
(Schulman et al., 2015a) proposed performing policy updates by optimizing a
surrogate objective, whose gradient is the policy gradient estimator, subject to
a constraint on the KL-divergence between the original policy and the updated
policy. Actor Critic using Kronecker-Factored Trust Region (ACKTR) (Wu
et al., 2017) uses Kronecker-factored approximated curvature (K-FAC) to per-
form a similar trust region update, but with a computational cost comparable
to SGD. Both methods could be used in the PPG framework.
10

5 Conclusion
The results in Section 3.2 and Section 3.3 make it clear that the optimal level
of sample reuse varies significantly between the policy and the value function.
Training these two objectives with varying sample reuse is not possible in a
conventional actor-critic framework using a shared network architecture. By
decoupling policy and value function training, PPG is able to reap the bene-
fits of additional value function training without significantly interfering with
the policy. To achieve this, PPG does introduce several new hyperparameters,
whichcreatessomeadditionalcomplexityrelativetopreviousalgorithms. How-
ever, we consider this a relatively minor cost, and we note that the chosen
hyperparameter values generalize well across all 16 Procgen environments.
By mitigating interference between the policy and the value function while
still maintaining the benefits of shared representations, PPG significantly im-
proves sample efficiency on the challenging Procgen Benchmark. Moreover,
PPGestablishesaframeworkforoptimizingarbitraryauxiliarylossesalongside
RL training in a stable manner. We have focused on the value function error
as the sole auxiliary loss in this work, but we consider it a compelling topic for
future research to evaluate other auxiliary losses using PPG.
References
M. Andrychowicz, A. Raichuk, P. Stan´czyk, M. Orsini, S. Girgin, R. Marinier,
L.Hussenot, M.Geist, O.Pietquin, M.Michalski, etal. Whatmattersinon-
policy reinforcement learning? a large-scale empirical study. arXiv preprint
arXiv:2006.05990, 2020.
M. Bellemare, W. Dabney, R. Dadashi, A. A. Taiga, P. S. Castro, N. Le Roux,
D. Schuurmans, T. Lattimore, and C. Lyle. A geometric perspective on opti-
mal representations for reinforcement learning. In Advances in Neural Infor-
mation Processing Systems, pages 4360–4371, 2019.
M. G. Bellemare, W. Dabney, and R. Munos. A distributional perspective on
reinforcement learning. In Proceedings of the 34th International Conference
on Machine Learning-Volume 70, pages 449–458. JMLR. org, 2017.
K.Cobbe, C.Hesse, J.Hilton, andJ.Schulman. Leveragingproceduralgenera-
tion to benchmark reinforcement learning. arXiv preprint arXiv:1912.01588,
2019.
L. Espeholt, H. Soyer, R. Munos, K. Simonyan, V. Mnih, T. Ward, Y. Doron,
V. Firoiu, T. Harley, I. Dunning, S. Legg, and K. Kavukcuoglu. IMPALA:
scalable distributed deep-rl with importance weighted actor-learner architec-
tures. CoRR, abs/1802.01561, 2018.
T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine. Soft actor-critic: Off-policy
maximumentropydeepreinforcementlearningwithastochasticactor. arXiv
preprint arXiv:1801.01290, 2018.
11

M. Igl, G. Farquhar, J. Luketina, W. Boehmer, and S. Whiteson. The impact
of non-stationarity on generalisation in deep reinforcement learning. arXiv
preprint arXiv:2006.05826, 2020.
D. P. Kingma and J. Ba. Adam: A method for stochastic optimization. arXiv
preprint arXiv:1412.6980, 2014.
T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver,
andD.Wierstra. Continuouscontrolwithdeepreinforcementlearning. arXiv
preprint arXiv:1509.02971, 2015.
C. Lyle, M. G. Bellemare, and P. S. Castro. A comparative analysis of ex-
pectedanddistributionalreinforcementlearning. InProceedings of the AAAI
Conference on Artificial Intelligence, volume 33, pages 4504–4511, 2019.
V. Mnih, A. P. Badia, M. Mirza, A. Graves, T. Lillicrap, T. Harley, D. Silver,
andK.Kavukcuoglu. Asynchronousmethodsfordeepreinforcementlearning.
In International conference on machine learning, pages 1928–1937, 2016.
OpenAI, I. Akkaya, M. Andrychowicz, M. Chociej, M. Litwin, B. McGrew,
A.Petron,A.Paino,M.Plappert,G.Powell,R.Ribas,J.Schneider,N.Tezak,
J. Tworek, P. Welinder, L. Weng, Q. Yuan, W. Zaremba, and L. Zhang.
Solving rubik’s cube with a robot hand. arXiv preprint arXiv:1910.07113,
2019a.
OpenAI,C.Berner,G.Brockman,B.Chan,V.Cheung,P.Debiak,C.Dennison,
D.Farhi, Q.Fischer, S.Hashme, C.Hesse, R.J´ozefowicz, S.Gray, C.Olsson,
J. Pachocki, M. Petrov, H. P. de Oliveira Pinto, J. Raiman, T. Salimans,
J. Schlatter, J. Schneider, S. Sidor, I. Sutskever, J. Tang, F. Wolski, and
S.Zhang. Dota2withlargescaledeepreinforcementlearning. arXiv preprint
arXiv:1912.06680, 2019b.
X. B. Peng, A. Kumar, G. Zhang, and S. Levine. Advantage-weighted regres-
sion: Simple and scalable off-policy reinforcement learning. arXiv preprint
arXiv:1910.00177, 2019.
J. Schulman, S. Levine, P. Abbeel, M. Jordan, and P. Moritz. Trust region
policy optimization. In International conference on machine learning, pages
1889–1897, 2015a.
J.Schulman,P.Moritz,S.Levine,M.Jordan,andP.Abbeel. High-dimensional
continuous control using generalized advantage estimation. arXiv preprint
arXiv:1506.02438, 2015b.
J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov. Proximal
policy optimization algorithms. CoRR, abs/1707.06347, 2017.
H.F.Song,A.Abdolmaleki,J.T.Springenberg,A.Clark,H.Soyer,J.W.Rae,
S. Noury, A. Ahuja, S. Liu, D. Tirumala, et al. V-mpo: On-policy maximum
a posteriori policy optimization for discrete and continuous control. arXiv
preprint arXiv:1909.12238, 2019.
12

O.Vinyals,I.Babuschkin,W.M.Czarnecki,M.Mathieu,A.Dudzik,J.Chung,
| D. H. Choi,  | R.    | Powell, | T.          | Ewalds,       | P. Georgiev, | et al.            | Grandmaster | level |
| ------------ | ----- | ------- | ----------- | ------------- | ------------ | ----------------- | ----------- | ----- |
| in starcraft | ii    | using   | multi-agent | reinforcement |              | learning. Nature, | 575(7782):  |       |
| 350–354,     | 2019. |         |             |               |              |                   |             |       |
Z. Wang, V. Bapst, N. Heess, V. Mnih, R. Munos, K. Kavukcuoglu, and
| N. de Freitas. |                   | Sample | efficient | actor-critic |     | with experience | replay. | arXiv |
| -------------- | ----------------- | ------ | --------- | ------------ | --- | --------------- | ------- | ----- |
| preprint       | arXiv:1611.01224, |        |           | 2016.        |     |                 |         |       |
Y. Wu, E. Mansimov, R. B. Grosse, S. Liao, and J. Ba. Scalable trust-region
| method           | for deep | reinforcement |        | learning    | using      | kronecker-factored      | approxima- |     |
| ---------------- | -------- | ------------- | ------ | ----------- | ---------- | ----------------------- | ---------- | --- |
| tion. InAdvances |          | in            | neural | information | processing | systems,pages5279–5288, |            |     |
2017.
13

A Hyperparameters
We use the Adam optimizer (Kingma and Ba, 2014) in all experiments.
A.1 PPG-Specific Hyperparameters
N 32
π
E 1
π
E 1
V
E 6
aux
β 1
clone
# minibatches per aux epoch per N 16
π
A.2 Other Hyperparameters
γ .999
λ .95
# timesteps per rollout 256
# minibatches per epoch 8
Entropy bonus coefficient (β ) .01
S
PPO clip range ((cid:15)) .2
Reward Normalization? Yes
Learning rate 5×10−4
# workers 4
# environments per worker 64
Total timesteps 100M
LSTM? No
Frame Stack? No
14

| B Shared | vs  | Separate | Networks |     |
| -------- | --- | -------- | -------- | --- |
Figure 8: A comparison between two implementations of PPO on Procgen
Benchmark. The baseline shares features between the policy and value net-
| works, while | the ablation | trains separate | policy and value | networks. |
| ------------ | ------------ | --------------- | ---------------- | --------- |
15

| C Auxiliary | Phase Value | Function | Training |     |
| ----------- | ----------- | -------- | -------- | --- |
Figure 9: The performance of a variant of PPG which skips the optimization of
| Lvalue                                              |                           |               |              | Lvalue |
| --------------------------------------------------- | ------------------------- | ------------- | ------------ | ------ |
| during the                                          | auxiliary phase, in favor | of additional | optimization | of     |
| during the policy phase.                            |                           |               |              |        |
| WenowdiscusstherelativeimportanceofoptimizingLvalue |                           |               | andLjoint    | dur-   |
ing the auxiliary phase. From Appendix B, we know that Ljoint is crucial;
without some optimization of this objective, there is no mechanism to share
featuresbetweenthevaluefunctionandthepolicy. Althoughitisconvenientto
Lvalue
optimize during the auxiliary phase as well, it is not strictly necessary.
It is also viable to perform extra value function optimization during the pol-
icy phase (by increasing E ), while removing the optimization of Lvalue from
V
the auxiliary phase. A comparison between this variant and the PPG baseline
are shown in Figure 9. Although the PPG baseline has a slight advantage, we
can see that the choice to optimize Lvalue during the auxiliary phase is not an
| essential element of | PPG. |     |     |     |
| -------------------- | ---- | --- | --- | --- |
16

| D PPO      | Sample             | Reuse             |                  |                   |
| ---------- | ------------------ | ----------------- | ---------------- | ----------------- |
| Figure 10: | A comparison       | between different | levels of sample | reuse in PPO.     |
| We sweep   | over the different | values for        | sample reuse in  | PPO, from 1 to 6. |
Empirically, we find that a sample reuse of 3 is optimal, given our other hyper-
parameter settings. As discussed in Section 3.2, the results with PPG suggest
thatthepoorperformanceofPPOwithlowsamplereuseisduetothefactthat
| the value function, | not the | policy, is being | under-trained. |     |
| ------------------- | ------- | ---------------- | -------------- | --- |
17