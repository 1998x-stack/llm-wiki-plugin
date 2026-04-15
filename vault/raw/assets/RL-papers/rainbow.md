Rainbow: Combining Improvements in Deep Reinforcement Learning
MatteoHessel JosephModayil HadovanHasselt TomSchaul GeorgOstrovski
| DeepMind   |     |     | DeepMind  |     |     | DeepMind  |     |     | DeepMind     |     |     |     | DeepMind    |     |
| ---------- | --- | --- | --------- | --- | --- | --------- | --- | --- | ------------ | --- | --- | --- | ----------- | --- |
| WillDabney |     |     | DanHorgan |     |     | BilalPiot |     |     | MohammadAzar |     |     |     | DavidSilver |     |
| DeepMind   |     |     | DeepMind  |     |     | DeepMind  |     |     | DeepMind     |     |     |     | DeepMind    |     |
Abstract
7102 tcO 6  ]IA.sc[  1v89220.0171:viXra
| The deep                                          | reinforcement | learning | community |     | has made | sev- |     |     | DQN  |     |     |     |     |     |
| ------------------------------------------------- | ------------- | -------- | --------- | --- | -------- | ---- | --- | --- | ---- | --- | --- | --- | --- | --- |
| eralindependentimprovementstotheDQNalgorithm.How- |               |          |           |     |          |      |     |     | DDQN |     |     |     |     |     |
Prioritized DDQN
ever,itisunclearwhichoftheseextensionsarecomplemen-
Dueling DDQN
| tary and | can be fruitfully |     | combined. | This paper | examines |     | 200% |     |     |     |     |     |     |     |
| -------- | ----------------- | --- | --------- | ---------- | -------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
A3C
sixextensionstotheDQNalgorithmandempiricallystudies
|                                                       |     |     |     |     |     |     | erocs dezilamron-namuh naideM |     | Distributional DQN |     |     |     |     |     |
| ----------------------------------------------------- | --- | --- | --- | --- | --- | --- | ----------------------------- | --- | ------------------ | --- | --- | --- | --- | --- |
| theircombination.Ourexperimentsshowthatthecombina-    |     |     |     |     |     |     |                               |     | Noisy DQN          |     |     |     |     |     |
| tionprovidesstate-of-the-artperformanceontheAtari2600 |     |     |     |     |     |     |                               |     | Rainbow            |     |     |     |     |     |
benchmark,bothintermsofdataefficiencyandfinalperfor-
mance.Wealsoprovideresultsfromadetailedablationstudy
thatshowsthecontributionofeachcomponenttooverallper-
formance.
100%
Introduction
| The many | recent successes |            | in scaling      | reinforcement |     | learn-   |     |     |     |     |     |     |     |     |
| -------- | ---------------- | ---------- | --------------- | ------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
| ing (RL) | to complex       | sequential | decision-making |               |     | problems |     |     |     |     |     |     |     |     |
werekick-startedbytheDeepQ-Networksalgorithm(DQN;
Mnihetal.2013,2015).ItscombinationofQ-learningwith
| convolutional | neural         | networks | and experience |         | replay | en-   |     | 0%  |     |     |     |     |     |     |
| ------------- | -------------- | -------- | -------------- | ------- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
|               |                |          |                |         |        |       |     | 7   | 44  |     | 100 |     |     | 200 |
| abled it      | to learn, from | raw      | pixels, how    | to play | many   | Atari |     |     |     |     |     |     |     |     |
Millions of frames
gamesathuman-levelperformance.Sincethen,manyexten-
sionshavebeenproposedthatenhanceitsspeedorstability. Figure1:Medianhuman-normalizedperformanceacross
57Atarigames.Wecompareourintegratedagent(rainbow-
| Double          | DQN (DDQN;           |                | van Hasselt, | Guez,         | and        | Silver  |          |          |            |        |             |           |            |            |
| --------------- | -------------------- | -------------- | ------------ | ------------- | ---------- | ------- | -------- | -------- | ---------- | ------ | ----------- | --------- | ---------- | ---------- |
|                 |                      |                |              |               |            |         | colored) | to       | DQN (grey) | and    | six         | published | baselines. | Note       |
| 2016) addresses | an                   | overestimation | bias         | of Q-learning |            | (van    |          |          |            |        |             |           |            |            |
|                 |                      |                |              |               |            |         | that     | we match | DQN’s      | best   | performance |           | after      | 7M frames, |
| Hasselt         | 2010), by decoupling |                | selection    | and           | evaluation | of      |          |          |            |        |             |           |            |            |
|                 |                      |                |              |               |            |         | surpass  | any      | baseline   | within | 44M         | frames,   | and        | reach sub- |
| the bootstrap   | action.              | Prioritized    | experience   |               | replay     | (Schaul |          |          |            |        |             |           |            |            |
etal.2015)improvesdataefficiency,byreplayingmoreof- stantiallyimprovedfinalperformance.Curvesaresmoothed
withamovingaverageover5points.
| ten transitions | from | which | there is more | to  | learn. | The du- |     |     |     |     |     |     |     |     |
| --------------- | ---- | ----- | ------------- | --- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
elingnetworkarchitecture(Wangetal.2016)helpstogen-
| eralize | across actions     | by separately | representing |                 |     | state val- |           |           |     |         |           |      |       |             |
| ------- | ------------------ | ------------- | ------------ | --------------- | --- | ---------- | --------- | --------- | --- | ------- | --------- | ---- | ----- | ----------- |
|         |                    |               |              |                 |     |            | radically | different |     | issues, | and since | they | build | on a shared |
| ues and | action advantages. |               | Learning     | from multi-step |     | boot-      |           |           |     |         |           |      |       |             |
straptargets(Sutton1988;SuttonandBarto1998),asused framework,theycouldplausiblybecombined.Insomecases
thishasbeendone:PrioritizedDDQNandDuelingDDQN
| in A3C | (Mnih et al. | 2016), | shifts the | bias-variance |     | trade- |      |            |             |     |     |         |      |          |
| ------ | ------------ | ------ | ---------- | ------------- | --- | ------ | ---- | ---------- | ----------- | --- | --- | ------- | ---- | -------- |
|        |              |        |            |               |     |        | both | use double | Q-learning, |     | and | Dueling | DDQN | was also |
offandhelpstopropagatenewlyobservedrewardsfasterto
|                 |           |                |                      |     |              |     | combined   |     | with prioritized |          | experience | replay.  |                 | In this paper  |
| --------------- | --------- | -------------- | -------------------- | --- | ------------ | --- | ---------- | --- | ---------------- | -------- | ---------- | -------- | --------------- | -------------- |
| earlier visited | states.   | Distributional | Q-learning           |     | (Bellemare,  |     |            |     |                  |          |            |          |                 |                |
|                 |           |                |                      |     |              |     | we propose |     | to study         | an agent | that       | combines |                 | all the afore- |
| Dabney,         | and Munos | 2017)          | learns a categorical |     | distribution |     |            |     |                  |          |            |          |                 |                |
|                 |           |                |                      |     |              |     | mentioned  |     | ingredients.     | We       | show       | how      | these different | ideas          |
ofdiscountedreturns,insteadofestimatingthemean.Noisy
DQN(Fortunatoetal.2017)usesstochasticnetworklayers can be integrated, and that they are indeed largely com-
|     |     |     |     |     |     |     | plementary. |     | In fact, | their | combination |     | results | in new state- |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | -------- | ----- | ----------- | --- | ------- | ------------- |
forexploration.Thislistis,ofcourse,farfromexhaustive.
|     |     |     |     |     |     |     | of-the-art | results | on  | the benchmark |     | suite | of 57 | Atari 2600 |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | --- | ------------- | --- | ----- | ----- | ---------- |
Eachofthesealgorithmsenablessubstantialperformance
gamesfromtheArcadeLearningEnvironment(Bellemareet
| improvements | in isolation. |     | Since they | do so | by addressing |     |     |     |     |     |     |     |     |     |
| ------------ | ------------- | --- | ---------- | ----- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
al.2013),bothintermsofdataefficiencyandoffinalperfor-
Copyright(cid:13)c 2018,AssociationfortheAdvancementofArtificial mance.Finallyweshowresultsfromablationstudiestohelp
Intelligence(www.aaai.org).Allrightsreserved. understandthecontributionsofthedifferentcomponents.

Background given state S (which is fed as input to the network in the
t
|               |     |          |           |     |         |     |          | form of | a stack | of raw | pixel | frames). | At each | step, | based |
| ------------- | --- | -------- | --------- | --- | ------- | --- | -------- | ------- | ------- | ------ | ----- | -------- | ------- | ----- | ----- |
| Reinforcement |     | learning | addresses | the | problem | of  | an agent |         |         |        |       |          |         |       |       |
learning to act in an environment in order to maximize a on the current state, the agent selects an action (cid:15)-greedily
scalarrewardsignal.Nodirectsupervisionisprovidedtothe with respect to the action values, and adds a transition
agent,forinstanceitisneverdirectlytoldthebestaction. (S ,A ,R ,γ ,S ) to a replay memory buffer (Lin
|     |     |     |     |     |     |     |     | t t         | t+1   | t+1 t+1  |         |              |     |             |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | -------- | ------- | ------------ | --- | ----------- | --- |
|     |     |     |     |     |     |     |     | 1992), that | holds | the last | million | transitions. |     | The parame- |     |
tersoftheneuralnetworkareoptimizedbyusingstochastic
Ateachdiscretetimestept=
Agentsandenvironments.
gradientdescenttominimizetheloss
| 0,1,2..., | the | environment | provides |     | the agent | with | an ob- |     |     |     |     |               |     |      |     |
| --------- | --- | ----------- | -------- | --- | --------- | ---- | ------ | --- | --- | --- | --- | ------------- | --- | ---- | --- |
|           |     |             |          |     |           |      |        |     |     |     |     | ,a(cid:48))−q |     | ))2, |     |
s e r va t i o n S , t h e a g e n t r e sp o n d s b y s e lec t in g a n a c tio n A , (R t+1 +γ t+1 m a xq (S t+1 θ (S t ,A t (1)
|           | t           |              |           |            |          |             | t      |     |     | a (cid:48) | θ   |     |     |     |     |
| --------- | ----------- | ------------ | --------- | ---------- | -------- | ----------- | ------ | --- | --- | ---------- | --- | --- | --- | --- | --- |
| a n d t h | e n t h e e | n vi r o n m | e n t p r | o v id e s | th e n e | x t r e w a | rd R , |     |     |            |     |     |     |     |     |
t+1
discountγ ,andstateS .Thisinteractionisformalized where t is a time step randomly picked from the replay
|     | t+1 |     | t+1 |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
as a Markov Decision Process, or MDP, which is a tuple memory. The gradient of the loss is back-propagated only
|                                    |     |     |                                 |     |     |     |     | into the | parameters | θ of | the online | network |     | (which is | also |
| ---------------------------------- | --- | --- | ------------------------------- | --- | --- | --- | --- | -------- | ---------- | ---- | ---------- | ------- | --- | --------- | ---- |
| (cid:104)S,A,T,r,γ(cid:105),whereS |     |     | isafinitesetofstates,Aisafinite |     |     |     |     |          |            |      |            |         |     |           |      |
setofactions,T(s,a,s(cid:48)) = P[S = s(cid:48) | S = s,A = a] used to select actions); the term θ represents the parame-
|     |     |     |     | t+1 |     | t   | t   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
is the (stochastic) transition function, r(s,a) = E[R | ters of a target network; a periodic copy of the online net-
t+1
S = s,A = a] is the reward function, and γ ∈ [0,1] is work which is not directly optimized. The optimization is
| t   | t   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
adiscountfactor.InourexperimentsMDPswillbeepisodic performed using RMSprop (Tieleman and Hinton 2012), a
variantofstochasticgradientdescent,onmini-batchessam-
| withaconstantγ |     | t =γ,exceptonepisodeterminationwhere |     |     |     |     |     |     |     |     |     |     |     |     |     |
| -------------- | --- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
γ =0,butthealgorithmsareexpressedinthegeneralform. pleduniformlyfromtheexperiencereplay.Thismeansthat
t
Ontheagentside,actionselectionisgivenbyapolicyπ inthelossabove,thetimeindextwillbearandomtimein-
that defines a probability distribution over actions for each dexfromthelastmilliontransitions,ratherthanthecurrent
state. From the state S encountered at time t, we define time. The use of experience replay and target networks en-
t
(cid:80)∞ γ(k)R ablesrelativelystablelearningofQvalues,andledtosuper-
| the discounted |     | return | G = |     |         | as  | the dis- |                                      |     |     |     |     |     |     |     |
| -------------- | --- | ------ | --- | --- | ------- | --- | -------- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
|                |     |        | t   | k=0 | t t+k+1 |     |          | humanperformanceonseveralAtarigames. |     |     |     |     |     |     |     |
countedsumoffuturerewardscollectedbytheagent,where
thediscountforarewardkstepsinthefutureisgivenbythe
|         |              |        |     |            | γ(k) | (cid:81)k |         |     |     | ExtensionstoDQN |     |     |     |     |     |
| ------- | ------------ | ------ | --- | ---------- | ---- | --------- | ------- | --- | --- | --------------- | --- | --- | --- | --- | --- |
| product | of discounts | before |     | that time, |      | =         | γ .     |     |     |                 |     |     |     |     |     |
|         |              |        |     |            | t    |           | i=1 t+i |     |     |                 |     |     |     |     |     |
An agent aims to maximize the expected discounted return DQN has been an important milestone, but several limita-
byfindingagoodpolicy. tionsofthisalgorithmarenowknown,andmanyextensions
|          |               |        |         |           |         |             |         | have been  | proposed. | We             | propose | a            | selection | of six exten- |     |
| -------- | ------------- | ------ | ------- | --------- | ------- | ----------- | ------- | ---------- | --------- | -------------- | ------- | ------------ | --------- | ------------- | --- |
| The      | policy        | may be | learned | directly, | or      | it may      | be con- |            |           |                |         |              |           |               |     |
|          |               |        |         |           |         |             |         | sions that | each      | have addressed |         | a limitation |           | and improved  |     |
| structed | as a function |        | of some | other     | learned | quantities. | In      |            |           |                |         |              |           |               |     |
overallperformance.Tokeepthesizeoftheselectionman-
| value-based | reinforcement |     | learning, |     | the agent | learns | an es- |     |     |     |     |     |     |     |     |
| ----------- | ------------- | --- | --------- | --- | --------- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
timate of the expected discounted return, or value, when ageable, we picked a set of extensions that address distinct
following a policy π starting from a given state, vπ(s) = concerns(e.g.,justoneofthemanyaddressingexploration).
=s],orstate-actionpair,qπ(s,a)=E
| E π [G t | |S t |     |     |     |     | π   | [G t |S t = |     |     |     |     |     |     |     |     |
| -------- | ---- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
s,A =a].Acommonwayofderivinganewpolicyfroma Double Q-learning. Conventional Q-learning is affected
t
state-actionvaluefunctionistoact(cid:15)-greedilywithrespectto by an overestimation bias, due to the maximization step in
theactionvalues.Thiscorrespondstotakingtheactionwith Equation 1, and this can harm learning. Double Q-learning
thehighestvalue(thegreedyaction)withprobability(1−(cid:15)), (vanHasselt2010),addressesthisoverestimationbydecou-
andtootherwiseactuniformlyatrandomwithprobability(cid:15). pling, in the maximization performed for the bootstrap tar-
Policies of this kind are used to introduce a form of explo- get,theselectionoftheactionfromitsevaluation.Itispos-
ration: by randomly selecting actions that are sub-optimal sible to effectively combine this with DQN (van Hasselt,
accordingtoitscurrentestimates,theagentcandiscoverand Guez,andSilver2016),usingtheloss
correctitsestimateswhenappropriate.Themainlimitation
|     |     |     |     |     |     |     |     | (R +γ | q     | (S ,argmaxq |     | (S    | ,a(cid:48)))−q | (S ,A | ))2. |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | ----------- | --- | ----- | -------------- | ----- | ---- |
|     |     |     |     |     |     |     |     | t+1   | t+1 θ | t+1         |     | θ t+1 |                | θ t   | t    |
isthatitisdifficulttodiscoveralternativecoursesofaction a(cid:48)
thatextendfarintothefuture;thishasmotivatedresearchon
|     |     |     |     |     |     |     |     | This change | was | shown | to reduce | harmful |     | overestimations |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----- | --------- | ------- | --- | --------------- | --- |
moredirectedformsofexploration.
thatwerepresentforDQN,therebyimprovingperformance.
| Deep      | reinforcement |             | learning | and         | DQN.                | Large | state   |                    |          |                               |       |           |      |            |      |
| --------- | ------------- | ----------- | -------- | ----------- | ------------------- | ----- | ------- | ------------------ | -------- | ----------------------------- | ----- | --------- | ---- | ---------- | ---- |
|           |               |             |          |             |                     |       |         | Prioritizedreplay. |          | DQNsamplesuniformlyfromthere- |       |           |      |            |      |
| and/or    | action        | spaces make | it       | intractable | to                  | learn | Q value |                    |          |                               |       |           |      |            |      |
|           |               |             |          |             |                     |       |         | play buffer.       | Ideally, | we                            | want  | to sample | more | frequently |      |
| estimates | for           | each state  | and      | action      | pair independently. |       | In      |                    |          |                               |       |           |      |            |      |
|           |               |             |          |             |                     |       |         | those transitions  |          | from                          | which | there is  | much | to learn.  | As a |
deepreinforcementlearning,werepresentthevariouscom-
|     |     |     |     |     |     |     |     | proxy for | learning | potential, |     | prioritized | experience | replay |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | -------- | ---------- | --- | ----------- | ---------- | ------ | --- |
ponentsofagents,suchaspoliciesπ(s,a)orvaluesq(s,a),
|                                                        |     |     |     |     |     |     |     | (Schaul | et al. 2015) | samples | transitions |     | with | probability | p   |
| ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | ------- | ------------ | ------- | ----------- | --- | ---- | ----------- | --- |
| withdeep(i.e.,multi-layer)neuralnetworks.Theparameters |     |     |     |     |     |     |     |         |              |         |             |     |      |             | t   |
relativetothelastencounteredabsoluteTDerror:
| of these | networks | are | trained | by gradient |     | descent | to mini- |     |          |     |     |     |     |           |     |
| -------- | -------- | --- | ------- | ----------- | --- | ------- | -------- | --- | -------- | --- | --- | --- | --- | --------- | --- |
|          |          |     |         |             |     |         |          |     | (cid:12) |     |     |     |     | (cid:12)ω |     |
mizesomesuitablelossfunction. ∝(cid:12)R ,a(cid:48))−q )(cid:12)
|                                               |     |     |     |     |     |     |     | p t | (cid:12) t+1 +γ | t+1 maxq | (S          | t+1 |     | θ (S t ,A t (cid:12) | ,   |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | -------- | ----------- | --- | --- | -------------------- | --- |
| InDQN(Mnihetal.2015)deepnetworksandreinforce- |     |     |     |     |     |     |     |     |                 |          | a(cid:48) θ |     |     |                      |     |
ment learning were successfully combined by using a con- where ω is a hyper-parameter that determines the shape of
volutionalneuralnettoapproximatetheactionvaluesfora thedistribution.Newtransitionsareinsertedintothereplay

bufferwithmaximumpriority,providingabiastowardsre- Here Φ is a L2-projection of the target distribution onto
z
cent transitions. Note that stochastic transitions might also the fixed support z, and a∗ = argmax q (S ,a) is
|     |     |     |     |     |     |     |     |     |     |     | t+1 |     | a   | θ t+1 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- |
befavoured,evenwhenthereislittlelefttolearnaboutthem. the greedy action with respect to the mean action values
|         |           |     |             |     |         |      |             | q (S ,a)=z(cid:62)p |                        | (S  | ,a)instateS |       | .      |       |        |
| ------- | --------- | --- | ----------- | --- | ------- | ---- | ----------- | ------------------- | ---------------------- | --- | ----------- | ----- | ------ | ----- | ------ |
|         |           |     |             |     |         |      |             | θ t+1               |                        | θ   | t+1         |       | t+1    |       |        |
|         |           |     |             |     |         |      |             | As in               | the non-distributional |     |             | case, | we can | use a | frozen |
| Dueling | networks. |     | The dueling |     | network | is a | neural net- |                     |                        |     |             |       |        |       |        |
copyoftheparametersθtoconstructthetargetdistribution.
| work architecture |         | designed |              | for value | based     | RL. | It fea-   |                 |     |                   |     |     |                |     |      |
| ----------------- | ------- | -------- | ------------ | --------- | --------- | --- | --------- | --------------- | --- | ----------------- | --- | --- | -------------- | --- | ---- |
|                   |         |          |              |           |           |     |           | Theparametrized |     | distributioncanbe |     |     | representedbya |     | neu- |
| tures two         | streams | of       | computation, |           | the value | and | advantage |                 |     |                   |     |     |                |     |      |
streams, sharing a convolutional encoder, and merged by a ralnetwork,asinDQN,butwithN atoms ×N actions outputs.A
special aggregator (Wang et al. 2016). This corresponds to softmaxisappliedindependentlyforeachactiondimension
oftheoutputtoensurethatthedistributionforeachactionis
thefollowingfactorizationofactionvalues:
appropriatelynormalized.
|                |        |                    |                               |         | (cid:80)        | a (f        | (s),a(cid:48)) |                                                    |           |             |      |                |         |                 |         |
| -------------- | ------ | ------------------ | ----------------------------- | ------- | --------------- | ----------- | -------------- | -------------------------------------------------- | --------- | ----------- | ---- | -------------- | ------- | --------------- | ------- |
|                |        |                    |                               |         |                 | a(cid:48) ψ | ξ              |                                                    |           |             |      |                |         |                 |         |
| q (s,a)=v      | (f     | (s))+a             | (f                            | (s),a)− |                 |             | ,              |                                                    |           |             |      |                |         |                 |         |
| θ              | η      | ξ                  | ψ                             | ξ       |                 | N           |                |                                                    |           |             |      |                |         |                 |         |
|                |        |                    |                               |         |                 | actions     |                | Noisy Nets.                                        | The       | limitations |      | of exploring   | using   | (cid:15)-greedy |         |
| where ξ,       | η, and | ψ are,             | respectively,                 |         | the             | parameters  | of the         |                                                    |           |             |      |                |         |                 |         |
|                |        |                    |                               |         |                 |             |                | policies                                           | are clear | in games    | such | as Montezuma’s |         | Revenge,        |         |
| sharedencoderf |        | ,ofthevaluestreamv |                               |         | ,andoftheadvan- |             |                |                                                    |           |             |      |                |         |                 |         |
|                |        | ξ                  |                               |         | η               |             |                | wheremanyactionsmustbeexecutedtocollectthefirstre- |           |             |      |                |         |                 |         |
| tagestreama    |        | ;andθ              | ={ξ,η,ψ}istheirconcatenation. |         |                 |             |                |                                                    |           |             |      |                |         |                 |         |
|                | ψ      |                    |                               |         |                 |             |                | ward. Noisy                                        | Nets      | (Fortunato  |      | et al. 2017)   | propose |                 | a noisy |
linearlayerthatcombinesadeterministicandnoisystream,
| Multi-steplearning. |     |     | Q-learningaccumulatesasinglere- |     |     |     |     |              |     |     |                      |     |                       |     |     |
| ------------------- | --- | --- | ------------------------------- | --- | --- | --- | --- | ------------ | --- | --- | -------------------- | --- | --------------------- | --- | --- |
|                     |     |     |                                 |     |     |     |     | y =(b+Wx)+(b |     |     | (cid:12)(cid:15)b+(W |     | (cid:12)(cid:15)w)x), |     | (4) |
wardandthenusesthegreedyactionatthenextsteptoboot- noisy noisy
| strap. Alternatively, |        | forward-view |           | multi-step |           | targets | can be |                 |               |            |     |            |              |         |     |
| --------------------- | ------ | ------------ | --------- | ---------- | --------- | ------- | ------ | --------------- | ------------- | ---------- | --- | ---------- | ------------ | ------- | --- |
|                       |        |              |           |            |           |         |        | where (cid:15)b | and (cid:15)w | are random |     | variables, | and (cid:12) | denotes | the |
| used (Sutton          | 1988). |              | We define | the        | truncated | n-step  | return |                 |               |            |     |            |              |         |     |
element-wiseproduct.Thistransformationcanthenbeused
| fromagivenstateS |     |     | as  |     |     |     |     |                             |     |     |     |                     |     |     |     |
| ---------------- | --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | --- | ------------------- | --- | --- | --- |
|                  |     | t   |     |     |     |     |     | inplaceofthestandardlineary |     |     |     | = b+Wx.Overtime,the |     |     |     |
n −1
(cid:88) n e tw o rk c a n l e a r n t o i g n o re th e no i s y st r e a m , b u t w i l l d o s o
|     |     | R (n) | ≡   | γ (k)R |     | .   | (2) |     |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
t t t+k+1 at d if fe re n t ra t e s i n d if f e re n tp a rts o f t he s t a t es p a c e ,a l l o w in g
|     |     |     | k=0 |     |     |     |     | state-conditionalexplorationwithaformofself-annealing. |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
Amulti-stepvariantofDQNisthendefinedbyminimizing
| thealternativeloss, |     |     |     |     |     |     |     |     |     | TheIntegratedAgent |     |     |     |     |     |
| ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- |
(R(n)+γ(n)maxq ,a(cid:48))−q ))2. In this paper we integrate all the aforementioned compo-
|     |     |     | (S          | t+n | θ   | (S t ,A | t   |     |     |     |     |     |     |     |     |
| --- | --- | --- | ----------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | t   | t   | a(cid:48) θ |     |     |         |     |     |     |     |     |     |     |     |     |
nentsintoasingleintegratedagent,whichwecallRainbow.
Multi-steptargetswithsuitablytunednoftenleadtofaster First, we replace the 1-step distributional loss (3) with a
learning(SuttonandBarto1998). multi-step variant. We construct the target distribution by
|     |     |     |     |     |     |     |     | contracting | the | value distribution |     | in  | S according |     | to the |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------------------ | --- | --- | ----------- | --- | ------ |
t+n
cumulativediscount,andshiftingitbythetruncatedn-step
| Distributional |     | RL. | We can | learn | to approximate |     | the dis- |     |     |     |     |     |     |     |     |
| -------------- | --- | --- | ------ | ----- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
tributionofreturnsinsteadoftheexpectedreturn.Recently discounted return. This corresponds to defining the target
Bellemare, Dabney, and Munos (2017) proposed to model distribution as d(n) = (R(n) + γ(n)z, p (S ,a∗ )).
|                    |     |      |             |     |        |        |           |     |     | t   | t   | t   | θ   | t+n | t+n |
| ------------------ | --- | ---- | ----------- | --- | ------ | ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
| such distributions |     | with | probability |     | masses | placed | on a dis- |     |     |     |     |     |     |     |     |
Theresultinglossis
|               |     | z,    | z   |             |      | N     | ∈ N+ |     |     |     |     |        |     |     |     |
| ------------- | --- | ----- | --- | ----------- | ---- | ----- | ---- | --- | --- | --- | --- | ------ | --- | --- | --- |
| crete support |     | where |     | is a vector | with | atoms |      |     |     |     |     |        |     |     |     |
|               |     | zi    |     |             |      | 1)vm  | − v  |     |     |     |     | (n)||d |     |     |     |
atoms, defined by = v min + (i − a x m in for D KL (Φ z d t ),
|              |         |           |                   |           |       | N            | a to ms − 1     |                                                    |     |                       |     | t   |     |     |     |
| ------------ | ------- | --------- | ----------------- | --------- | ----- | ------------ | --------------- | -------------------------------------------------- | --- | --------------------- | --- | --- | --- | --- | --- |
| i ∈ {1,...,N |         | }.        | The approximating |           |       | distribution | d at            |                                                    |     |                       |     |     |     |     |     |
|              |         | atoms     |                   |           |       |              | t               | where,again,Φ                                      |     | istheprojectionontoz. |     |     |     |     |     |
| time t is    | defined | on this   | support,          | with      | the   | probability  | mass            |                                                    |     | z                     |     |     |     |     |     |
| pi(S         |         |           |                   |           |       |              |                 | Wecombinethemulti-stepdistributionallosswithdouble |     |                       |     |     |     |     |     |
| t ,A         | t ) on  | each atom | i,                | such that | d t = | (z,p         | θ (S t ,A t )). |                                                    |     |                       |     |     |     |     |     |
θ Q-learning by using the greedy action in S t+n selected ac-
| The goal                               | is to | update | θ such | that | this distribution |     | closely |                           |     |     |     |                        |     |     |     |
| -------------------------------------- | ----- | ------ | ------ | ---- | ----------------- | --- | ------- | ------------------------- | --- | --- | --- | ---------------------- | --- | --- | --- |
|                                        |       |        |        |      |                   |     |         | cordingtotheonlinenetwork |     |     |     | asthebootstrapactiona∗ |     |     | ,   |
| matchestheactualdistributionofreturns. |       |        |        |      |                   |     |         |                           |     |     |     |                        |     |     | t+n |
andevaluatingsuchactionusingthetargetnetwork.
| To learn             | the   | probability |            | masses, | the key            | insight | is that   |               |              |             |             |         |                |         |          |
| -------------------- | ----- | ----------- | ---------- | ------- | ------------------ | ------- | --------- | ------------- | ------------ | ----------- | ----------- | ------- | -------------- | ------- | -------- |
|                      |       |             |            |         |                    |         |           | In standard   | proportional |             | prioritized |         | replay         | (Schaul | et al.   |
| return distributions |       | satisfy     | a          | variant | of Bellman’s       |         | equation. |               |              |             |             |         |                |         |          |
|                      |       |             |            |         |                    |         |           | 2015) the     | absolute     | TD          | error       | is used | to prioritize  | the     | tran-    |
| For a given          | state | S t         | and action | A t     | , the distribution |         | of the    |               |              |             |             |         |                |         |          |
|                      |       |             |            |         |                    |         |           | sitions. This | can          | be computed |             | in the  | distributional |         | setting, |
| returns              | under | the optimal |            | policy  | π∗ should          | match   | a tar-    |               |              |             |             |         |                |         |          |
usingthemeanactionvalues.However,inourexperiments
| get distribution |     | defined | by     | taking | the distribution |     | for the     |                    |     |         |          |            |     |             |     |
| ---------------- | --- | ------- | ------ | ------ | ---------------- | --- | ----------- | ------------------ | --- | ------- | -------- | ---------- | --- | ----------- | --- |
|                  |     |         |        |        |                  |     |             | all distributional |     | Rainbow | variants | prioritize |     | transitions | by  |
| next state       | S   | and     | action | a∗ =   | π∗(S             | ),  | contracting |                    |     |         |          |            |     |             |     |
t+1 t+1 t+1 theKLloss,sincethisiswhatthealgorithmisminimizing:
| it towards | zero | according |     | to the discount, |     | and | shifting it |     |     |          |     |     |           |     |     |
| ---------- | ---- | --------- | --- | ---------------- | --- | --- | ----------- | --- | --- | -------- | --- | --- | --------- | --- | --- |
|            |      |           |     |                  |     |     |             |     |     | (cid:16) |     |     | (cid:17)ω |     |     |
by the reward (or distribution of rewards, in the stochas- d(n)||d
|     |     |     |     |     |     |     |     |     |     | p t ∝ D | (Φ  | z   | t ) . |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | ----- | --- | --- |
tic case). A distributional variant of Q-learning is then de- KL t
| rived by   | first constructing |                 | a   | new support |                  | for the | target dis- |        |         |          |       |     |             |     |       |
| ---------- | ------------------ | --------------- | --- | ----------- | ---------------- | ------- | ----------- | ------ | ------- | -------- | ----- | --- | ----------- | --- | ----- |
|            |                    |                 |     |             |                  |         |             | The KL | loss as | priority | might | be  | more robust | to  | noisy |
| tribution, | and                | then minimizing |     | the         | Kullbeck-Leibler |         | diver-      |        |         |          |       |     |             |     |       |
stochasticenvironmentsbecausethelosscancontinuetode-
| gencebetweenthedistributiond |        |        |      | andthetargetdistribution |     |     |     |                                              |     |              |     |           |         |           |     |
| ---------------------------- | ------ | ------ | ---- | ------------------------ | --- | --- | --- | -------------------------------------------- | --- | ------------ | --- | --------- | ------- | --------- | --- |
|                              |        |        |      | t                        |     |     |     | creaseevenwhenthereturnsarenotdeterministic. |     |              |     |           |         |           |     |
| d(cid:48)                    |        |        |      | ,a∗                      |     |     |     |                                              |     |              |     |           |         |           |     |
| t ≡(R                        | t+1 +γ | t+1 z, | p (S | t+1 t+1                  | )), |     |     |                                              |     |              |     |           |         |           |     |
|                              |        |        | θ    |                          |     |     |     | The network                                  |     | architecture | is  | a dueling | network | architec- |     |
d(cid:48)||d
D (Φ ). (3) ture adapted for use with return distributions. The network
|     |     |     | KL  | z t | t   |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

has a shared representation f (s), which is then fed into a Hyper-parameter tuning. All Rainbow’s components
ξ
valuestreamv withN outputs,andintoanadvantage have a number of hyper-parameters. The combinatorial
|     |     | η   | atoms |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
streama withN ×N outputs,whereai(f (s),a) space of hyper-parameters is too large for an exhaustive
|     | ξ   | atoms | actions |     |     | ξ   | ξ   |     |     |     |     |     |     |     |     |
| --- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
will denote the output corresponding to atom i and action search, therefore we have performed limited tuning. For
a. For each atom zi, the value and advantage streams are eachcomponent,westartedwiththevaluesusedinthepaper
thatintroducedthiscomponent,andtunedthemostsensitive
| aggregated, |     | as in dueling | DQN, | and | then passed | through | a   |     |     |     |     |     |     |     |     |
| ----------- | --- | ------------- | ---- | --- | ----------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
amonghyper-parametersbymanualcoordinatedescent.
| softmax | layer | to obtain | the | normalised | parametric |     | distribu- |     |     |     |     |     |     |     |     |
| ------- | ----- | --------- | --- | ---------- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
tionsusedtoestimatethereturns’distributions: DQNanditsvariantsdonotperformlearningupdatesdur-
ingthefirst200Kframes,toensuresufficientlyuncorrelated
|     |     | exp(vi(φ)+ai |     | (φ,a)−ai |     | (s)) |     |     |     |     |     |     |     |     |     |
| --- | --- | ------------ | --- | -------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
η ψ ψ updates. We have found that, with prioritized replay, it is
|     | pi(s,a)= |     |     |     |     |     | ,   |     |     |     |     |     |     |     |     |
| --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
θ (cid:80) exp(vj(φ)+aj(φ,a)−aj(s)) possibletostartlearningsooner,afteronly80K frames.
η
|     |     | j   |     | ψ   |     | ψ   |     |     |             |     |             |          |                     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----------- | -------- | ------------------- | --- | --- |
|     |     |     |     |     |     |     |     | DQN | starts with | an  | exploration | (cid:15) | of 1, corresponding |     | to  |
(cid:80)
whereφ=f (s)andai (s)= 1 ai (φ,a(cid:48)). actinguniformlyatrandom;itannealstheamountofexplo-
|     |     | ξ   | ψ   | N   | a (cid:48) ψ |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Wethenre placealll inearlay e a r ct s ion w s ith t he irnoisyequiva- rationoverthefirst4Mframes,toafinalvalueof0.1(low-
eredto0.01inlatervariants).WheneverusingNoisyNets,
lentdescribedinEquation(4).Withinthesenoisylinearlay-
weactedfullygreedily((cid:15)=0),withavalueof0.5fortheσ
| ersweusefactorisedGaussiannoise(Fortunatoetal.2017) |     |     |     |     |     |     |     |     |     |     |     |     |     |     | 0   |
| --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
toreducethenumberofindependentnoisevariables. hyper-parameter used to initialize the weights in the noisy
|     |     |     |     |     |     |     |     | stream1. | For agents | without | Noisy | Nets, | we  | used (cid:15)-greedy |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | ------- | ----- | ----- | --- | -------------------- | --- |
ExperimentalMethods butdecreasedtheexplorationratefasterthanwaspreviously
|     |     |     |     |     |     |     |     | used,annealing(cid:15)to0.01inthefirst250K |     |     |     |     | frames. |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | ------- | --- | --- |
Wenowdescribethemethodsandsetupusedforconfiguring
|     |     |     |     |     |     |     |     | We used | the | Adam | optimizer | (Kingma |     | and Ba | 2014), |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ---- | --------- | ------- | --- | ------ | ------ |
andevaluatingthelearningagents.
|     |     |     |     |     |     |     |     | which we | found         | less | sensitive | to the | choice   | of the  | learn- |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | ---- | --------- | ------ | -------- | ------- | ------ |
|     |     |     |     |     |     |     |     | ing rate | than RMSProp. |      | DQN       | uses a | learning | rate of | α =    |
Evaluation Methodology. We evaluated all agents on 57 0.00025 In all Rainbow’s variants we used a learning rate
Atari 2600 games from the arcade learning environment of α/4, selected among {α/2,α/4,α/6}, and a value of
(Bellemare et al. 2013). We follow the training and evalu- 1.5×10−4forAdam’s(cid:15)hyper-parameter.
ationproceduresofMnihetal.(2015)andvanHasseltetal. For replay prioritization we used the recommended pro-
(2016).Theaveragescoresoftheagentareevaluatedduring portional variant, with priority exponent ω of 0.5, and lin-
training,every1Mstepsintheenvironment,bysuspending early increased the importance sampling exponent β from
learning and evaluating the latest agent for 500K frames. 0.4 to 1 over the course of training. The priority exponent
| Episodes |     | are truncated | at 108K | frames | (or | 30 minutes | of  |     |     |     |     |     |     |     |     |
| -------- | --- | ------------- | ------- | ------ | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ω wastunedcomparingvaluesof{0.4,0.5,0.7}.Usingthe
simulatedplay),asinvanHasseltetal.(2016). KLlossofdistributionalDQNaspriority,wehaveobserved
Agents’scoresarenormalized,pergame,sothat0%cor- thatperformanceisveryrobusttothechoiceofω.
respondstoarandomagentand100%totheaveragescore The value of n in multi-step learning is a sensitive
of a human expert. Normalized scores can be aggregated hyper-parameter of Rainbow. We compared values of n =
| across | all | Atari levels | to compare | the | performance |     | of dif- |             |     |          |      |      |       |           |      |
| ------ | --- | ------------ | ---------- | --- | ----------- | --- | ------- | ----------- | --- | -------- | ---- | ---- | ----- | --------- | ---- |
|        |     |              |            |     |             |     |         | 1, 3, and5. | We  | observed | that | both | n = 3 | and 5 did | well |
ferentagents.Itiscommontotrackthemedianhumannor- initially,butoveralln=3performedthebestbytheend.
malizedperformanceacrossallgames.Wealsoconsiderthe The hyper-parameters (see Table 1) are identical across
number of games where the agent’s performance is above all57games,i.e.,theRainbowagentreallyisasingleagent
somefractionofhumanperformance,todisentanglewhere
setupthatperformswellacrossallthegames.
| improvements |     | in the median |     | come from. | The | mean | human |     |     |     |     |     |     |     |     |
| ------------ | --- | ------------- | --- | ---------- | --- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
normalizedperformanceispotentiallylessinformative,asit 1ThenoisewasgeneratedontheGPU.Tensorflownoisegen-
is dominated by a few games (e.g., Atlantis) where agents eration can be unreliable on GPU. If generating the noise on the
achievescoresordersofmagnitudehigherthanhumansdo. CPU,loweringσ to0.1maybehelpful.
0
Besidestrackingthemedianperformanceasafunctionof
environmentsteps,attheendoftrainingwere-evaluatethe
|     |     |     |     |     |     |     |     | Parameter |     |     |     |     |     | Value |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | ----- | --- |
best agent snapshot using two different testing regimes. In Minhistorytostartlearning 80Kframes
theno-opsstartsregime,weinsertarandomnumber(upto Adamlearningrate 0.0000625
30)ofno-opactionsatthebeginningofeachepisode(aswe Exploration(cid:15) 0.0
do also in training). In the human starts regime, episodes NoisyNetsσ 0.5
0
areinitializedwithpointsrandomlysampledfromtheinitial TargetNetworkPeriod 32Kframes
portion of human expert trajectories (Nair et al. 2015); the Adam(cid:15) 1.5×10−4
|            |     |             |     |         |           |            |     | Prioritizationtype      |     |     |     |     | proportional |     |     |
| ---------- | --- | ----------- | --- | ------- | --------- | ---------- | --- | ----------------------- | --- | --- | --- | --- | ------------ | --- | --- |
| difference |     | between the | two | regimes | indicates | the extent | to  |                         |     |     |     |     |              |     |     |
|            |     |             |     |         |           |            |     | Prioritizationexponentω |     |     |     |     |              | 0.5 |     |
whichtheagenthasover-fittoitsowntrajectories.
|          |            |                    |       |              |              |         |         | Prioritizationimportancesamplingβ |     |     |     |     | 0.4→1.0 |          |     |
| -------- | ---------- | ------------------ | ----- | ------------ | ------------ | ------- | ------- | --------------------------------- | --- | --- | --- | --- | ------- | -------- | --- |
| Due      | to         | space constraints, |       | we focus     | on aggregate |         | results |                                   |     |     |     |     |         |          |     |
|          |            |                    |       |              |              |         |         | Multi-stepreturnsn                |     |     |     |     |         | 3        |     |
| across   | games.     | However,           | in    | the appendix | we           | provide | full    |                                   |     |     |     |     |         |          |     |
|          |            |                    |       |              |              |         |         | Distributionalatoms               |     |     |     |     |         | 51       |     |
| learning | curves     | for all            | games | and all      | agents,      | as well | as de-  |                                   |     |     |     |     |         |          |     |
|          |            |                    |       |              |              |         |         | Distributionalmin/maxvalues       |     |     |     |     |         | [−10,10] |     |
| tailed   | comparison | tables             | of    | raw and      | normalized   | scores, | in      |                                   |     |     |     |     |         |          |     |
Table1:Rainbowhyper-parameters
boththeno-opandhumanstartstestingregimes.

#games > 20% human #games > 50% human #games > 100% human #games > 200% human #games > 500% human
57
DQN
DDQN
Prioritized DDQN
| semag fo rebmun 40 |     |     |     |     |     |     |     |     |     |     |     | Dueling DDQN |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- |
A3C
Distributional DQN
Noisy DQN
25
Rainbow
10
57
DQN
no double
no priority
| semag fo rebmun 40 |     |     |     |     |     |     |     |     |     |     |     | no dueling |     |     |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- |
no multi-step
no distribution
no noisy
25
Rainbow
10
0 50 100 150 200 0 50 100 150 200 0 50 100 150 200 0 50 100 150 200 0 50 100 150 200
Millions of frames Millions of frames Millions of frames Millions of frames Millions of frames
Figure2:Eachplotshows,forseveralagents,thenumberofgameswheretheyhaveachievedatleastagivenfractionofhuman
performance,asafunctionoftime.Fromlefttorightweconsiderthe20%,50%,100%,200%and500%thresholds.Onthe
firstrowwecompareRainbowtothebaselines.OnthesecondrowwecompareRainbowtoitsablations.
Analysis
mance.Thisallowsustoidentifywheretheoverallimprove-
mentsinperformancecomefrom.Notethatthegapinper-
| In this section |     | we analyse | the | main experimental |     | results. |     |     |     |     |     |     |     |     |
| --------------- | --- | ---------- | --- | ----------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
formancebetweenRainbowandotheragentsisapparentat
First,weshowthatRainbowcomparesfavorablytoseveral
|           |         |         |         |          |          |      | all levels | of performance: |     | the | Rainbow | agent | is  | improving |
| --------- | ------- | ------- | ------- | -------- | -------- | ---- | ---------- | --------------- | --- | --- | ------- | ----- | --- | --------- |
| published | agents. | Then we | perform | ablation | studies, | com- |            |                 |     |     |         |       |     |           |
paring several variants of the agent, each corresponding to scores on games where the baseline agents were already
good,aswellasimprovingingameswherebaselineagents
removingasinglecomponentfromRainbow.
arestillfarfromhumanperformance.
| Comparisontopublishedbaselines. |           |             |     |           | InFigure1wecom- |        |            |        |          |        |          |           |          |        |
| ------------------------------- | --------- | ----------- | --- | --------- | --------------- | ------ | ---------- | ------ | -------- | ------ | -------- | --------- | -------- | ------ |
|                                 |           |             |     |           |                 |        | Learning   | speed. | As       | in the | original | DQN       | setup,   | we ran |
| pare the                        | Rainbow’s | performance |     | (measured | in terms        | of the |            |        |          |        |          |           |          |        |
|                                 |           |             |     |           |                 |        | each agent | on     | a single | GPU.   | The      | 7M frames | required | to     |
medianhumannormalizedscoreacrossgames)tothecorre-
matchDQN’sfinalperformancecorrespondtolessthan10
spondingcurvesforA3C,DQN,DDQN,PrioritizedDDQN,
|     |     |     |     |     |     |     | hours of | wall-clock | time. | A   | full run | of 200M | frames | cor- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ---------- | ----- | --- | -------- | ------- | ------ | ---- |
DuelingDDQN,DistributionalDQN,andNoisyDQN.We
|             |              |                |       |                 |                  |            | responds | to approximately |     | 10     | days,     | and this    | varies | by less |
| ----------- | ------------ | -------------- | ----- | --------------- | ---------------- | ---------- | -------- | ---------------- | --- | ------ | --------- | ----------- | ------ | ------- |
| thank the   | authors      | of the Dueling |       | and Prioritized |                  | agents for |          |                  |     |        |           |             |        |         |
|             |              |                |       |                 |                  |            | than 20% | between          | all | of the | discussed | variants.   | The    | litera- |
| providing   | the learning | curves         | of    | these,          | and report       | our own    |          |                  |     |        |           |             |        |         |
| re-runs for | DQN,         | A3C,           | DDQN, | Distributional  |                  | DQN and    |          |                  |     |        |           |             |        |         |
|             |              |                |       |                 |                  |            | Agent    |                  |     |        | no-ops    | humanstarts |        |         |
| Noisy DQN.  | The          | performance    | of    | Rainbow         | is significantly |            |          |                  |     |        |           |             |        |         |
better than any of the baselines, both in data efficiency, as DQN 79% 68%
well as in final performance. Note that we match final per- DDQN(*) 117% 110%
formance of DQN after 7M frames, surpass the best final PrioritizedDDQN(*) 140% 128%
|                                        |     |                 |     |        |         |           | DuelingDDQN(*) |     |     |     | 151% |     | 117% |     |
| -------------------------------------- | --- | --------------- | --- | ------ | ------- | --------- | -------------- | --- | --- | --- | ---- | --- | ---- | --- |
| performance                            | of  | these baselines |     | in 44M | frames, | and reach |                |     |     |     |      |     |      |     |
| substantiallyimprovedfinalperformance. |     |                 |     |        |         |           | A3C(*)         |     |     |     | -    |     | 116% |     |
Inthefinalevaluationsoftheagent,aftertheendoftrain- NoisyDQN 118% 102%
ing,Rainbowachievesamedianscoreof223%intheno-ops DistributionalDQN 164% 125%
regime; in the human starts regime we measured a median Rainbow 223% 153%
| score of | 153%. | In Table 2 | we compare |     | these scores | to the |          |        |            |     |        |        |            |       |
| -------- | ----- | ---------- | ---------- | --- | ------------ | ------ | -------- | ------ | ---------- | --- | ------ | ------ | ---------- | ----- |
|          |       |            |            |     |              |        | Table 2: | Median | normalized |     | scores | of the | best agent | snap- |
publishedmedianscoresoftheindividualbaselines.
InFigure2(toprow)weplotthenumberofgameswhere shotsforRainbowandbaselines.Formethodsmarkedwith
anagenthasreachedsomespecifiedlevelofhumannormal- anasterisk,thescorescomefromthecorrespondingpublica-
ized performance. From left to right, the subplots show on tion.DQN’sscorescomesfromtheduelingnetworkspaper,
|          |       |               |        |      |          |      | since DQN’s | paper | did | not report | scores | for | all | 57 games. |
| -------- | ----- | ------------- | ------ | ---- | -------- | ---- | ----------- | ----- | --- | ---------- | ------ | --- | --- | --------- |
| how many | games | the different | agents | have | achieved | 20%, |             |       |     |            |        |     |     |           |
Theothersscorescomefromourownimplementations.
| 50%, 100%, | 200% | and 500% |     | human | normalized | perfor- |     |     |     |     |     |     |     |     |
| ---------- | ---- | -------- | --- | ----- | ---------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |

almostuniformlyacrossgames(thefullRainbowperformed
|     | DQN |     |     |     |     | betterthaneitherablationin53gamesoutof57). |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
no double
no priority Distributional Q-learning ranked immediately below the
no dueling previous techniques for relevance to the agent’s perfor-
| 200% | no multi-step |     |     |     |     |        |          |          |          |     |               |     |        |
| ---- | ------------- | --- | --- | --- | --- | ------ | -------- | -------- | -------- | --- | ------------- | --- | ------ |
|      |               |     |     |     |     | mance. | Notably, | in early | learning |     | no difference | is  | appar- |
no distribution
|     |     |     |     |     |     | ent, as | shown | in Figure | 3,  | where | for the | first 40 | million |
| --- | --- | --- | --- | --- | --- | ------- | ----- | --------- | --- | ----- | ------- | -------- | ------- |
no noisy
erocs dezilamron naideM
Rainbow frames the distributional-ablation performed as well as the
fullagent.However,withoutdistributions,theperformance
oftheagentthenstartedlaggingbehind.Whentheresultsare
|      |     |     |     |     |     | separated                              | relatively                  | to          | human        | performance |           | in Figure       | 2, we     |
| ---- | --- | --- | --- | --- | --- | -------------------------------------- | --------------------------- | ----------- | ------------ | ----------- | --------- | --------------- | --------- |
|      |     |     |     |     |     | see that                               | the distributional-ablation |             |              |             | primarily | seems           | to lags   |
| 100% |     |     |     |     |     | ongamesthatareabovehumanlevelornearit. |                             |             |              |             |           |                 |           |
|      |     |     |     |     |     | In terms                               | of                          | median      | performance, |             | the       | agent performed |           |
|      |     |     |     |     |     | better when                            | Noisy                       | Nets        | were         | included;   | when      | these           | are re-   |
|      |     |     |     |     |     | moved                                  | and exploration             |             | is           | delegated   | to        | the traditional | (cid:15)- |
|      |     |     |     |     |     | greedy                                 | mechanism,                  | performance |              |             | was worse | in aggregate    |           |
(redlineinFigure3).WhiletheremovalofNoisyNetspro-
ducedalargedropinperformanceforseveralgames,italso
| 0%  |     |     |     |     |     | providedsmallincreasesinothergames(Figure4). |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|     | 50  |     | 100 | 150 | 200 |                                              |     |     |     |     |     |     |     |
Millions of frames In aggregate, we did not observe a significant difference
whenremovingtheduelingnetworkfromthefullRainbow.
Figure3:Medianhuman-normalizedperformanceacross
|     |     |     |     |     |     | The median | score, | however, |     | hides | the fact | that the | impact |
| --- | --- | --- | --- | --- | --- | ---------- | ------ | -------- | --- | ----- | -------- | -------- | ------ |
57 Atari games, as a function of time. We compare our in- of Dueling differed between games, as shown by Figure 4.
tegrated agent (rainbow-colored) to DQN (gray) and to six Figure 2 shows that Dueling perhaps provided some im-
differentablations(dashedlines).Curvesaresmoothedwith provementongameswithabove-humanperformancelevels
amovingaverageover5points. (# games > 200%), and some degradation on games with
sub-humanperformance(#games>20%).
AlsointhecaseofdoubleQ-learning,theobserveddiffer-
| ture contains | many alternative |     | training setups | that | improve |         |        |             |     |         |       |               |     |
| ------------- | ---------------- | --- | --------------- | ---- | ------- | ------- | ------ | ----------- | --- | ------- | ----- | ------------- | --- |
|               |                  |     |                 |      |         | ence in | median | performance |     | (Figure | 3) is | limited, with | the |
performance asa function ofwall-clock time by exploiting componentsometimesharmingorhelpingdependingonthe
| parallelism, | e.g., Nair et | al. (2015), | Salimans | et al. | (2017), |     |     |     |     |     |     |     |     |
| ------------ | ------------- | ----------- | -------- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
game(Figure4).TofurtherinvestigatetheroleofdoubleQ-
| and Mnih | et al. (2016). | Properly | relating | the performance |     |     |     |     |     |     |     |     |     |
| -------- | -------------- | -------- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
learning,wecomparedthepredictionsofourtrainedagents
| across such  | very different | hardware/compute |     | resources   | is    |                  |            |         |         |          |       |              |     |
| ------------ | -------------- | ---------------- | --- | ----------- | ----- | ---------------- | ---------- | ------- | ------- | -------- | ----- | ------------ | --- |
|              |                |                  |     |             |       | to the actual    | discounted |         | returns | computed |       | from clipped | re- |
| non-trivial, | so we focused  | exclusively      | on  | algorithmic | vari- |                  |            |         |         |          |       |              |     |
|              |                |                  |     |             |       | wards. Comparing |            | Rainbow |         | to the   | agent | where double | Q-  |
ations, allowing apples-to-apples comparisons. While we learningwasablated,weobservedthattheactualreturnsare
considerthemtobeimportantandcomplementary,weleave
|     |     |     |     |     |     | often higher | than | 10  | and therefore |     | fall outside | the | support |
| --- | --- | --- | --- | --- | --- | ------------ | ---- | --- | ------------- | --- | ------------ | --- | ------- |
questionsofscalabilityandparallelismtofuturework.
ofthedistribution,spanningfrom−10to+10.Thisleadsto
underestimatedreturns,ratherthanoverestimations.Wehy-
Ablationstudies. SinceRainbowintegratesseveraldiffer- pothesize that clipping the values to this constrained range
entideasintoasingleagent,weconductedadditionalexper- counteracts the overestimation bias of Q-learning. Note,
imentstounderstandthecontributionofthevariouscompo-
|     |     |     |     |     |     | however,that | theimportanceof |     |     | doubleQ-learningmay |     |     | in- |
| --- | --- | --- | --- | --- | --- | ------------ | --------------- | --- | --- | ------------------- | --- | --- | --- |
nents,inthecontextofthisspecificcombination. creaseifthesupportofthedistributionsisexpanded.
Togainabetterunderstandingofthecontributionofeach Intheappendix,foreachgameweshowfinalperformance
component to the Rainbow agent, we performed ablation andlearningcurvesforRainbow,itsablations,andbaselines.
studies.Ineachablation,weremovedonecomponentfrom
| the full | Rainbow combination. |     | Figure 3 shows | a   | compari- |     |     |     |     |     |     |     |     |
| -------- | -------------------- | --- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Discussion
sonformediannormalizedscoreofthefullRainbowtosix
ablated variants. Figure 2 (bottom row) shows a more de- We have demonstrated that several improvements to DQN
tailedbreakdownofhowtheseablationsperformrelativeto can be successfully integrated into a single learning algo-
differentthresholdsofhumannormalizedperformance,and rithmthatachievesstate-of-the-artperformance.Moreover,
Figure4showsthegainorlossfromeachablationforevery wehaveshownthatwithintheintegratedalgorithm,allbut
game,averagedoverthefulllearningrun. one of the components provided clear performance bene-
Prioritized replay and multi-step learning were the two fits. There are many more algorithmic components that we
most crucial components of Rainbow, in that removing ei- werenotabletoinclude,whichwouldbepromisingcandi-
thercomponentcausedalargedropinmedianperformance. dates for further experiments on integrated agents. Among
Unsurprisingly,theremovalofeitherofthesehurtearlyper- themanypossiblecandidates,wediscussseveralbelow.
formance.Perhapsmoresurprisingly,theremovalofmulti- We have focused here on value-based methods in the
steplearningalsohurtfinalperformance.Zoominginonin- Q-learning family. We have not considered purely policy-
dividualgames(Figure4),weseebothcomponentshelped based RL algorithms such as trust-region policy optimisa-

Rainbow
DQN
ysion
on
Rainbow
DQN
noitubirtsid
on
Rainbow
DQN
pets-itlum
on
Rainbow
DQN
gnileud
on
Rainbow
DQN
ytiroirp
on
neila radima tluassa xiretsa sdioretsa sitnalta tsieh_knab enoz_elttab redir_maeb krezreb gnixob tuokaerb edepitnec dnammoc_reppohc rebmilc_yzarc rednefed kcatta_nomed knud_elbuod orudne ybred_gnihsif yaweerf etibtsorf rehpog rativarg oreh yekcoh_eci dnobsemaj ooragnak llurk retsam_uf_gnuk egnever_amuzetnom namcap_sm emag_siht_eman xineohp llaftip gnop eye_etavirp trebq diarrevir rennur_daor knatobor tseuqaes gniiks siralos sredavni_ecaps rennug_rats dnuorrus sinnet tolip_emit mahknatut nwod_n_pu llabnip_oediv row_fo_draziw egnever_sray noxxaz
Rainbow
DQN
elbuod
on
Figure 4: Performance drops of ablation agents on all 57 Atari games. Performance is the area under the learning curve,
normalizedrelativetotheRainbowagentandDQN.TwogameswhereDQNoutperformsRainbowareomitted.Theablation
leadingtothestrongestdropishighlightedforeachgame.Theremovalofeitherprioritizationormulti-steplearningreduces
performanceacrossmostgames,butthecontributionofeachcomponentvariessubstantiallypergame.
tion(Schulmanetal.2015),noractor-criticmethods(Mnih dates,withoutexploringalternativecomputationalarchitec-
etal.2016;O’Donoghueetal.2016). tures.Asynchronouslearningfromparallelcopiesoftheen-
A number of algorithms exploit a sequence of data to vironment,asinA3C(Mnihetal.2016),Gorila(Nairetal.
achieveimprovedlearningefficiency.Optimalitytightening 2015),orEvolutionStrategies(Salimansetal.2017),canbe
(He et al. 2016) uses multi-step returns to construct addi- effective in speeding up learning, at least in terms of wall-
tional inequality bounds, instead of using them to replace clocktime.Note,however,theycanbelessdataefficient.
the 1-step targets used in Q-learning. Eligibility traces al- HierarchicalRLhasalsobeenappliedwithsuccesstosev-
low a soft combination over n-step returns (Sutton 1988). eralcomplexAtarigames.Amongsuccessfulapplicationsof
However, sequential methods all leverage more computa- HRLwehighlighth-DQN(Kulkarnietal.2016a)andFeu-
tionpergradientthanthemulti-steptargetsusedinRainbow. dalNetworks(Vezhnevetsetal.2017).
Furthermore,introducingprioritizedsequencereplayraises
The state representation could also be made more effi-
questionsofhowtostore,replayandprioritisesequences.
cient by exploiting auxiliary tasks such as pixel control or
Episodic control (Blundell et al. 2016) also focuses on feature control (Jaderberg et al. 2016), supervised predic-
dataefficiency,andwasshowntobeveryeffectiveinsome tions (Dosovitskiy and Koltun 2016) or successor features
domains.Itimprovesearlylearningbyusingepisodicmem- (Kulkarnietal.2016b).
oryasacomplementarylearningsystem,capableofimme-
ToevaluateRainbowfairlyagainstthebaselines,wehave
diatelyre-enactingsuccessfulactionsequences.
followedthecommondomainmodificationsofclippingre-
BesidesNoisyNets,numerousotherexplorationmethods wards,fixedaction-repetition,andframe-stacking,butthese
could also be useful algorithmic ingredients: among these might be removed by other learning algorithm improve-
Bootstrapped DQN (Osband et al. 2016), intrinsic motiva- ments. Pop-Art normalization (van Hasselt et al. 2016) al-
tion(Stadie,Levine,andAbbeel2015)andcount-basedex- lows reward clipping to be removed, while preserving a
ploration(Bellemareetal.2016).Integrationofthesealter- similarlevelofperformance.Fine-grainedactionrepetition
nativecomponentsisfruitfulsubjectforfurtherresearch. (Sharma,Lakshminarayanan,andRavindran2017)enabled
In this paper we have focused on the core learning up- to learn how to repeat actions. A recurrent state network

(HausknechtandStone2015)canlearnatemporalstaterep- S.; and Hassabis, D. 2015. Human-level control through
resentation,replacingthefixedstackofobservationframes. deepreinforcementlearning. Nature518(7540):529–533.
In general, we believe that exposing the real game to the Mnih,V.;Badia,A.P.;Mirza,M.;Graves,A.;Lillicrap,T.;
agentisapromisingdirectionforfutureresearch.
|     |     |     |     |     |     |     | Harley,  | T.; Silver, | D.; | and Kavukcuoglu,   |     | K.        | 2016. | Asyn-  |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | --- | ------------------ | --- | --------- | ----- | ------ |
|     |     |     |     |     |     |     | chronous | methods     | for | deep reinforcement |     | learning. |       | In In- |
References
ternationalConferenceonMachineLearning.
Bellemare,M.G.;Naddaf,Y.;Veness,J.;andBowling,M.
Nair,A.;Srinivasan,P.;Blackwell,S.;Alcicek,C.;Fearon,
2013. Thearcadelearningenvironment:Anevaluationplat- R.;DeMaria,A.;Panneershelvam,V.;Suleyman,M.;Beat-
formforgeneralagents. J.Artif.Intell.Res.(JAIR)47:253– tie, C.; Petersen, S.; Legg, S.; Mnih, V.; Kavukcuoglu, K.;
279. and Silver, D. 2015. Massively parallel methods for deep
Bellemare,M.G.;Srinivasan,S.;Ostrovski,G.;Schaul,T.; reinforcementlearning. arXivpreprintarXiv:1507.04296.
Saxton, D.; and Munos, R. 2016. Unifying count-based O’Donoghue, B.; Munos, R.; Kavukcuoglu, K.; and Mnih,
| explorationandintrinsicmotivation. |     |     |     | InNIPS. |     |     |          |      |           |        |          |     |                 |     |
| ---------------------------------- | --- | --- | --- | ------- | --- | --- | -------- | ---- | --------- | ------ | -------- | --- | --------------- | --- |
|                                    |     |     |     |         |     |     | V. 2016. | Pgq: | Combining | policy | gradient |     | and q-learning. |     |
Bellemare,M.G.;Dabney,W.;andMunos,R. 2017. Adis- CoRRabs/1611.01626.
| tributionalperspectiveonreinforcementlearning. |     |     |     |     |     | InICML. |         |               |     |          |     |          |       |       |
| ---------------------------------------------- | --- | --- | --- | --- | --- | ------- | ------- | ------------- | --- | -------- | --- | -------- | ----- | ----- |
|                                                |     |     |     |     |     |         | Osband, | I.; Blundell, | C.; | Pritzel, | A.; | and Roy, | B. V. | 2016. |
Blundell, C.; Uria, B.; Pritzel, A.; Li, Y.; Ruderman, A.; Deepexplorationviabootstrappeddqn. InNIPS.
| Leibo, J.                  | Z.; Rae, | J.; Wierstra, | D.;            | and Hassabis, |     | D. 2016. |                                           |     |               |     |             |     |               |      |
| -------------------------- | -------- | ------------- | -------------- | ------------- | --- | -------- | ----------------------------------------- | --- | ------------- | --- | ----------- | --- | ------------- | ---- |
|                            |          |               |                |               |     |          | Salimans,T.;Ho,J.;Chen,X.;andSutskever,I. |     |               |     |             |     | 2017.         | Evo- |
| Model-FreeEpisodicControl. |          |               | ArXive-prints. |               |     |          |                                           |     |               |     |             |     |               |      |
|                            |          |               |                |               |     |          | lution strategies                         |     | as a scalable |     | alternative | to  | reinforcement |      |
Dosovitskiy, A., and Koltun, V. 2016. Learning to act by learning. CoRRabs/1703.03864.
| predictingthefuture. |     | CoRRabs/1611.01779. |     |     |     |     |         |           |                 |     |     |             |     |       |
| -------------------- | --- | ------------------- | --- | --- | --- | --- | ------- | --------- | --------------- | --- | --- | ----------- | --- | ----- |
|                      |     |                     |     |     |     |     | Schaul, | T.; Quan, | J.; Antonoglou, |     | I.; | and Silver, | D.  | 2015. |
Fortunato, M.; Azar, M. G.; Piot, B.; Menick, J.; Osband, Prioritizedexperiencereplay. InProc.ofICLR.
I.;Graves,A.;Mnih,V.;Munos,R.;Hassabis,D.;Pietquin,
Schulman,J.;Levine,S.;Moritz,P.;Jordan,M.;andAbbeel,
| O.; Blundell, | C.;                 | and Legg, | S. 2017. | Noisy | networks | for |          |       |        |                      |     |     |                |     |
| ------------- | ------------------- | --------- | -------- | ----- | -------- | --- | -------- | ----- | ------ | -------------------- | --- | --- | -------------- | --- |
|               |                     |           |          |       |          |     | P. 2015. | Trust | region | policy optimization. |     |     | In Proceedings |     |
| exploration.  | CoRRabs/1706.10295. |           |          |       |          |     |          |       |        |                      |     |     |                |     |
ofthe32NdInternationalConferenceonInternationalCon-
| Hausknecht, | M., | and Stone, | P. 2015. |     | Deep | recurrent Q- |     |     |     |     |     |     |     |     |
| ----------- | --- | ---------- | -------- | --- | ---- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
ferenceonMachineLearning-Volume37,ICML’15,1889–
| learning | for partially | observable |     | MDPs. | arXiv | preprint | 1897. JMLR.org. |     |     |     |     |     |     |     |
| -------- | ------------- | ---------- | --- | ----- | ----- | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- |
arXiv:1507.06527.
|     |     |     |     |     |     |     | Sharma, | S.; Lakshminarayanan, |     |     | A.  | S.; and | Ravindran, |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | --------------------- | --- | --- | --- | ------- | ---------- | --- |
He,F.S.;Liu,Y.;Schwing,A.G.;andPeng,J.2016.Learn- B. 2017. Learning to repeat: Fine grained action rep-
ingto playin aday: Fasterdeep reinforcementlearning by etition for deep reinforcement learning. arXiv preprint
| optimalitytightening. |     | CoRRabs/1611.01606. |     |     |     |     | arXiv:1702.06054. |     |     |     |     |     |     |     |
| --------------------- | --- | ------------------- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
Jaderberg, M.; Mnih, V.; Czarnecki, W. M.; Schaul, T.; Stadie,B.C.;Levine,S.;andAbbeel,P. 2015. Incentivizing
| Leibo, J. | Z.; Silver, | D.; | and Kavukcuoglu, |     | K.  | 2016. Rein- |             |     |               |          |     |      |                 |     |
| --------- | ----------- | --- | ---------------- | --- | --- | ----------- | ----------- | --- | ------------- | -------- | --- | ---- | --------------- | --- |
|           |             |     |                  |     |     |             | exploration | in  | reinforcement | learning |     | with | deep predictive |     |
forcementlearningwithunsupervisedauxiliarytasks.CoRR
models. CoRRabs/1507.00814.
abs/1611.05397.
|                         |            |     |                               |       |     |            | Sutton,R.S.,andBarto,A.G. |     |                          |     | 1998. | ReinforcementLearn- |     |     |
| ----------------------- | ---------- | --- | ----------------------------- | ----- | --- | ---------- | ------------------------- | --- | ------------------------ | --- | ----- | ------------------- | --- | --- |
| Kingma,                 | D. P., and | Ba, | J. 2014.                      | Adam: | A   | method for |                           |     |                          |     |       |                     |     |     |
|                         |            |     |                               |       |     |            | ing:AnIntroduction.       |     | TheMITpress,CambridgeMA. |     |       |                     |     |     |
| stochasticoptimization. |            |     | InProceedingsofthe3rdInterna- |       |     |            |                           |     |                          |     |       |                     |     |     |
tionalConferenceonLearningRepresentations(ICLR). Sutton, R. S. 1988. Learning to predict by the methods of
|           |        |             |     |         |     |            | temporaldifferences. |     | Machinelearning3(1):9–44. |     |     |     |     |     |
| --------- | ------ | ----------- | --- | ------- | --- | ---------- | -------------------- | --- | ------------------------- | --- | --- | --- | --- | --- |
| Kulkarni, | T. D.; | Narasimhan, | K.; | Saeedi, | A.; | and Tenen- |                      |     |                           |     |     |     |     |     |
baum,J.B. 2016a. Hierarchicaldeepreinforcementlearn- Tieleman, T., and Hinton, G. 2012. Lecture 6.5-rmsprop:
Dividethegradientbyarunningaverageofitsrecentmag-
| ing: Integrating | temporal |     | abstraction | and | intrinsic | motiva- |     |     |     |     |     |     |     |     |
| ---------------- | -------- | --- | ----------- | --- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
nitude. COURSERA:Neuralnetworksformachinelearning
tion. CoRRabs/1604.06057.
4(2):26–31.
| Kulkarni, | T. D.; | Saeedi, | A.; Gautam, | S.; | and | Gershman, |     |     |     |     |     |     |     |     |
| --------- | ------ | ------- | ----------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
vanHasselt,H.;Guez,A.;Guez,A.;Hessel,M.;Mnih,V.;
| S.J. 2016b. | Deepsuccessorreinforcementlearning. |     |     |     |     | arXiv |     |     |     |     |     |     |     |     |
| ----------- | ----------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
preprintarXiv:1606.02396. andSilver,D. 2016. Learningvaluesacrossmanyordersof
|            |       |                |     |          |        |          | magnitude. | In  | Advances | in Neural | Information |     | Processing |     |
| ---------- | ----- | -------------- | --- | -------- | ------ | -------- | ---------- | --- | -------- | --------- | ----------- | --- | ---------- | --- |
| Lin, L.-J. | 1992. | Self-improving |     | reactive | agents | based on |            |     |          |           |             |     |            |     |
Systems29,4287–4295.
| reinforcement | learning, |     | planning | and teaching. |     | Machine |     |     |     |     |     |     |     |     |
| ------------- | --------- | --- | -------- | ------------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Learning8(3):293–321. van Hasselt, H.; Guez, A.; and Silver, D. 2016. Deep re-
|       |                  |     |     |         |             |     | inforcement | learning | with | double | Q-learning. |     | In Proc. | of  |
| ----- | ---------------- | --- | --- | ------- | ----------- | --- | ----------- | -------- | ---- | ------ | ----------- | --- | -------- | --- |
| Mnih, | V.; Kavukcuoglu, |     | K.; | Silver, | D.; Graves, | A.; |             |          |      |        |             |     |          |     |
AAAI,2094–2100.
| Antonoglou, | I.; Wierstra, |     | D.; and | Riedmiller, | M.  | A. 2013. |     |     |     |     |     |     |     |     |
| ----------- | ------------- | --- | ------- | ----------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Playing atari with deep reinforcement learning. CoRR van Hasselt, H. 2010. Double Q-learning. In Advances in
abs/1312.5602. NeuralInformationProcessingSystems23,2613–2621.
Mnih,V.;Kavukcuoglu,K.;Silver,D.;Rusu,A.A.;Veness, Vezhnevets,A.S.;Osindero,S.;Schaul,T.;Heess,N.;Jader-
J.;Bellemare,M.G.;Graves,A.;Riedmiller,M.;Fidjeland, berg, M.; Silver, D.; and Kavukcuoglu, K. 2017. Feu-
A. K.; Ostrovski, G.; Petersen, S.; Beattie, C.; Sadik, A.; dalnetworksforhierarchicalreinforcementlearning. CoRR
| Antonoglou,I.;King,H.;Kumaran,D.;Wierstra,D.;Legg, |     |     |     |     |     |     | abs/1703.01161. |     |     |     |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- |

Wang,Z.;Schaul,T.;Hessel,M.;vanHasselt,H.;Lanctot,
| M.; and de Freitas, | N. 2016. Dueling | network architec- |
| ------------------- | ---------------- | ----------------- |
turesfordeepreinforcementlearning.InProceedingsofThe
33rdInternationalConferenceonMachineLearning,1995–
2003.

Appendix
Table3liststhepreprocessingofenvironmentframes,rewardsanddiscountsintroducedbyDQN.Table4liststheadditional
hyper-parametersthatRainbowinheritsfromDQNandtheotherbaselinesconsideredinthispaper.Thehyper-parametersfor
whichRainbowusesnonstandardsettingsareinsteadlistedinthemaintext.Inthesubsequentpages,welistthetablesshowing,
foreachgame,thescoreachievedbyRainbowandseveralbaselinesinboththeno-opsregime(Table6)andthehuman-starts
regime (Table 5). In Figures 5 and 6 we also plot, for each game, the learning curves of Rainbow, several baselines, and all
ablationexperiments.Theselearningcurvesaresmoothedwithamovingaverageoverawindowof10.
Hyper-parameter value
Grey-scaling True
Observationdown-sampling (84,84)
Framesstacked 4
Actionrepetitions 4
Rewardclipping [-1,1]
Terminalonlossoflife True
Maxframesperepisode 108K
Table3:Preprocessing:thevaluesofthesehyper-parametersarethesameusedbyDQNanditsvariants.Theyareherelisted
forcompleteness.Observationsaregrey-scaledandrescaledto84×84pixels.4consecutiveframesareconcatenatedaseach
state’srepresentation.Eachactionselectedbytheagentisrepeatedfor4times.Rewardsareclippedbetween−1,+1.Ingames
wheretheplayerhasmultiplelives,transitionsassociatedtothelossofalifeareconsideredterminal.Allepisodesarecapped
after108Kframes.
Hyper-parameter value
Qnetwork:channels 32,64,64
Qnetwork:filtersize 8×8,4×4,3×3
Qnetwork:stride 4,2,1
Qnetwork:hiddenunits 512
Qnetwork:outputunits Numberofactions
Discountfactor 0.99
Memorysize 1Mtransitions
Replayperiod every4agentsteps
Minibatchsize 32
Table4:Additionalhyper-parameters:thevaluesofthesehyper-parametersarethesameusedbyDQNandit’svariants.The
networkhas3convolutionallayers:with32,64and64channels.Thelayersuse8×8,4×4,3×3filterswithstridesof4,
2, 1, respectively. The value and advantage streams of the dueling architecture have both a hidden layer with 512 units. The
outputlayerofthenetworkhasanumberofunitsequaltothenumberofactionsavailableinthegame.Weuseadiscountfactor
of0.99,whichissetto0onterminaltransitions.Weperformalearningupdateevery4agentsteps,usingmini-batchesof32
transitions.

Game DQN A3C DDQN Prior.DDQN Duel.DDQN Distrib.DQN NoisyDQN Rainbow
| alien  | 634.0 | 518.4 | 1033.4 | 900.5 | 1,486.5 | 1,997.5 | 533.3 | 6,022.9 |
| ------ | ----- | ----- | ------ | ----- | ------- | ------- | ----- | ------- |
| amidar | 178.4 | 263.9 | 169.1  | 218.4 | 172.7   | 237.7   | 148.0 | 202.8   |
assault 3489.3 5474.9 6060.8 7,748.5 3,994.8 5,101.3 5,124.3 14,491.7
asterix 3170.5 22140.5 16837.0 31,907.5 15,840.0 395,599.5 8,277.3 280,114.0
asteroids 1458.7 4474.5 1193.2 1,654.0 2,035.4 2,071.7 4,078.1 2,249.4
atlantis 292491.0 911,091.0 319688.0 593,642.0 445,360.0 289,803.0 303,666.5 814,684.0
| bank heist | 312.7 | 970.1 | 886.0 | 816.8 | 1,129.3 | 835.6 | 955.0 | 826.0 |
| ---------- | ----- | ----- | ----- | ----- | ------- | ----- | ----- | ----- |
battle zone 23750.0 12950.0 24740.0 29,100.0 31,320.0 32,250.0 26,985.0 52,040.0
beam rider 9743.2 22707.9 17417.2 26,172.7 14,591.3 15,002.4 15,241.5 21,768.5
berzerk 493.4 817.9 1011.1 1,165.6 910.6 1,000.0 670.8 1,793.4
| bowling  | 56.5  | 35.1  | 69.6  | 65.8  | 65.7  | 76.8  | 79.3  | 39.4  |
| -------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| boxing   | 70.3  | 59.8  | 73.5  | 68.6  | 77.3  | 62.1  | 66.3  | 54.9  |
| breakout | 354.5 | 681.9 | 368.9 | 371.6 | 411.6 | 548.7 | 423.3 | 379.5 |
centipede 3973.9 3755.8 3853.5 3,421.9 4,881.0 7,476.9 4,214.4 7,160.9
chopper command 5017.0 7021.0 3495.0 6,604.0 3,784.0 9,600.5 8,778.5 10,916.0
crazy climber 98128.0 112646.0 113782.0 131,086.0 124,566.0 154,416.5 98,576.5 143,962.0
defender 15917.5 56533.0 27510.0 21,093.5 33,996.0 32,246.0 18,037.5 47,671.3
demon attack 12550.7 113,308.4 69803.4 73,185.8 56,322.8 109,856.6 25,207.8 109,670.7
| double dunk | -6.0 | -0.1 | -0.3 | 2.7 | -0.8 | -3.7 | -1.0 | -0.6 |
| ----------- | ---- | ---- | ---- | --- | ---- | ---- | ---- | ---- |
enduro 626.7 -82.5 1216.6 1,884.4 2,077.4 2,133.4 1,021.5 2,061.1
| fishing derby | -1.6 | 18.8 | 3.2 | 9.2 | -4.1 | -4.9 | -3.7 | 22.6 |
| ------------- | ---- | ---- | --- | --- | ---- | ---- | ---- | ---- |
29.1
| freeway | 26.9 | 0.1 | 28.8 | 27.9 | 0.2 | 28.8 | 27.1 |     |
| ------- | ---- | --- | ---- | ---- | --- | ---- | ---- | --- |
frostbite 496.1 190.5 1448.1 2,930.2 2,332.4 2,813.9 418.8 4,141.1
gopher 8190.4 10022.8 15253.0 57,783.8 20,051.4 27,778.3 13,131.0 72,595.7
| gravitar | 298.0 | 303.5 | 200.5 | 218.0 | 297.0 | 422.0 | 250.5 | 567.5 |
| -------- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
hero 14992.9 32464.1 14892.5 20,506.4 15,207.9 28,554.2 2,454.2 50,496.8
| ice hockey | -1.6 | -2.8 | -2.5 | -1.0 | -1.3 | -0.1 | -2.4 | -0.7 |
| ---------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
kangaroo 4496.0 94.0 11204.0 10,241.0 10,334.0 9,555.5 7,465.0 10,841.0
krull 6206.0 5560.0 6796.1 7,406.5 8,051.6 6,757.8 6,833.5 6,715.5
kung fu master 20882.0 28819.0 30207.0 31,244.0 24,288.0 33,890.0 27,921.0 28,999.8
| montezuma revenge | 47.0 | 67.0 | 42.0 | 13.0 | 22.0 | 130.0 | 55.0 | 154.0 |
| ----------------- | ---- | ---- | ---- | ---- | ---- | ----- | ---- | ----- |
ms pacman 1092.3 653.7 1241.3 1,824.6 2,250.6 2,064.1 1,012.1 2,570.2
name this game 6738.8 10476.1 8960.3 11,836.1 11,185.1 11,382.3 7,186.4 11,686.5
phoenix 7484.8 52894.1 12366.5 27,430.1 20,410.5 31,358.3 15,505.0 103,061.6
| pitfall | -113.2 | -78.5 | -186.7 | -14.8 | -46.9 | -342.8 | -154.4 | -37.6 |
| ------- | ------ | ----- | ------ | ----- | ----- | ------ | ------ | ----- |
| pong    | 18.0   | 5.6   | 19.1   | 18.9  | 18.8  | 18.9   | 18.0   | 19.0  |
private eye 207.9 206.9 -575.5 179.0 292.6 5,717.5 5,955.4 1,704.4
qbert 9271.5 15148.8 11020.8 11,277.0 14,175.8 15,035.9 9,176.6 18,397.6
road runner 35215.0 34216.0 43156.0 56,990.0 58,549.0 56,086.0 35,376.5 54,261.0
| robotank | 58.7 | 32.8 | 59.1 | 55.4 | 62.0 | 49.8 | 50.9 | 55.2 |
| -------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
seaquest 4216.7 2355.4 14498.0 39,096.7 37,361.6 3,275.4 2,353.1 19,176.0
skiing -12142.1 -10911.1 -11490.4 -10,852.8 -11,928.0 -13,247.7 -13,905.9 -11,685.8
solaris 1295.4 1956.0 810.0 2,238.2 1,768.4 2,530.2 2,608.2 2,860.7
space invaders 1293.8 15,730.5 2628.7 9,063.0 5,993.1 6,368.6 1,697.2 12,629.0
star gunner 52970.0 138218.0 58365.0 51,959.0 90,804.0 67,054.5 31,864.5 123,853.0
| surround | -6.0 | -9.7 | 1.9  | -0.9 | 4.0 | 4.5  | -3.1 | 7.0  |
| -------- | ---- | ---- | ---- | ---- | --- | ---- | ---- | ---- |
| tennis   | 11.1 | -6.3 | -7.8 | -2.0 | 4.4 | 22.6 | -2.1 | -2.2 |
time pilot 4786.0 12,679.0 6608.0 7,448.0 6,601.0 7,684.5 5,311.0 11,190.5
| tutankham | 45.6  | 156.3 | 92.2 | 33.6  | 48.0  | 124.3 | 123.3 | 126.9 |
| --------- | ----- | ----- | ---- | ----- | ----- | ----- | ----- | ----- |
| venture   | 136.0 | 23.0  | 21.0 | 244.0 | 200.0 | 462.0 | 10.5  | 45.0  |
video pinball 154414.1 331628.1 367823.7 374,886.9 110,976.2 455,052.7 241,851.7 506,817.2
wizard of wor 1609.0 17,244.0 6201.0 7,451.0 7,054.0 11,824.5 4,796.5 14,631.5
yars revenge 4577.5 7157.5 6270.6 5,965.1 25,976.5 8,267.7 5,487.3 93,007.9
zaxxon 4412.0 24,622.0 8593.0 9,501.0 10,164.0 15,130.0 7,650.5 19,658.0
Table 5: Human Starts evaluation regime: Raw scores across all games, averaged over 200 testing episodes, from the agent
snapshot that obtained the highest score during training. We report the published scores for DQN, A3C, DDQN, Dueling
DDQN,andPrioritizedDDQN.ForDistributionalDQNandRainbowwereportourownevaluationsoftheagents.

Game DQN DDQN Prior.DDQN Duel.DDQN Distrib.DQN NoisyDQN Rainbow
| alien  | 1620.0 | 3747.7 | 6,648.6 | 4,461.4 | 4,055.8 | 2,394.9 | 9,491.7 |
| ------ | ------ | ------ | ------- | ------- | ------- | ------- | ------- |
| amidar | 978.0  | 1793.3 | 2,051.8 | 2,354.5 | 1,267.9 | 1,608.0 | 5,131.2 |
assault 4280.0 5393.2 7,965.7 4,621.0 5,909.0 5,198.6 14,198.5
asterix 4359.0 17356.5 41,268.0 28,188.0 400,529.5 12,403.8 428,200.3
asteroids 1364.5 734.7 1,699.3 2,837.7 2,354.7 4,814.1 2,712.8
atlantis 279987.0 106056.0 427,658.0 382,572.0 273,895.0 329,010.0 826,659.5
bank heist 455.0 1030.6 1,126.8 1,611.9 1,056.7 1,323.0 1,358.0
battle zone 29900.0 31700.0 38,130.0 37,150.0 41,145.0 32,050.0 62,010.0
beam rider 8627.5 13772.8 22,430.7 12,164.0 13,213.4 12,534.0 16,850.2
| berzerk  | 585.6 | 1225.4 | 1,614.2 | 1,472.6 | 1,421.8 | 837.3 | 2,545.6 |
| -------- | ----- | ------ | ------- | ------- | ------- | ----- | ------- |
| bowling  | 50.4  | 68.1   | 62.6    | 65.5    | 74.1    | 77.3  | 30.0    |
| boxing   | 88.0  | 91.6   | 98.8    | 99.4    | 98.1    | 83.3  | 99.6    |
| breakout | 385.5 | 418.5  | 381.5   | 345.3   | 612.5   | 459.1 | 417.5   |
centipede 4657.7 5409.4 5,175.4 7,561.4 9,015.5 4,355.8 8,167.3
chopper command 6126.0 5809.0 5,135.0 11,215.0 13,136.0 9,519.0 16,654.0
crazy climber 110763.0 117282.0 183,137.0 143,570.0 178,355.0 118,768.0 168,788.5
defender 23633.0 35338.5 24,162.5 42,214.0 37,896.8 23,083.0 55,105.0
demon attack 12149.4 58044.2 70,171.8 60,813.3 110,626.5 24,950.1 111,185.2
| double dunk   | -6.6  | -5.5   | 4.8     | 0.1     | -3.8    | -1.8    | -0.3    |
| ------------- | ----- | ------ | ------- | ------- | ------- | ------- | ------- |
| enduro        | 729.0 | 1211.8 | 2,155.0 | 2,258.2 | 2,259.3 | 1,129.2 | 2,125.9 |
| fishing derby | -4.9  | 15.5   | 30.2    | 46.4    | 9.1     | 7.7     | 31.3    |
| freeway       | 30.8  | 33.3   | 32.9    | 0.0     | 33.6    | 32.0    | 34.0    |
9,590.5
| frostbite | 797.4 | 1683.3 | 3,421.6 | 4,672.8 | 3,938.2 | 583.6 |     |
| --------- | ----- | ------ | ------- | ------- | ------- | ----- | --- |
gopher 8777.4 14840.8 49,097.4 15,718.4 28,841.0 15,107.9 70,354.6
| gravitar | 473.0 | 412.0 | 330.5 | 588.0 | 681.0 | 443.5 | 1,419.3 |
| -------- | ----- | ----- | ----- | ----- | ----- | ----- | ------- |
hero 20437.8 20130.2 27,153.9 20,818.2 33,860.9 5,053.1 55,887.4
| ice hockey | -1.9 | -2.7 | 0.3 | 0.5 | 1.3 | -2.1 | 1.1 |
| ---------- | ---- | ---- | --- | --- | --- | ---- | --- |
kangaroo 7259.0 12992.0 14,492.0 14,854.0 12,909.0 12,117.0 14,637.5
krull 8422.3 7920.5 10,263.1 11,451.9 9,885.9 9,061.9 8,741.5
kung fu master 26059.0 29710.0 43,470.0 34,294.0 43,009.0 34,099.0 52,181.0
| montezuma revenge | 0.0 | 0.0 | 0.0 | 0.0 | 367.0 | 0.0 | 384.0 |
| ----------------- | --- | --- | --- | --- | ----- | --- | ----- |
ms pacman 3085.6 2711.4 4,751.2 6,283.5 3,769.2 2,501.6 5,380.4
name this game 8207.8 10616.0 13,439.4 11,971.1 12,983.6 8,332.4 13,136.0
phoenix 8485.2 12252.5 32,808.3 23,092.2 34,775.0 16,974.3 108,528.6
| pitfall     | -286.1 | -29.9 | 0.0   | 0.0   | -2.1     | -18.2   | 0.0     |
| ----------- | ------ | ----- | ----- | ----- | -------- | ------- | ------- |
| pong        | 19.5   | 20.9  | 20.7  | 21.0  | 20.8     | 21.0    | 20.9    |
| private eye | 146.7  | 129.7 | 200.0 | 103.0 | 15,172.9 | 3,966.0 | 4,234.0 |
qbert 13117.3 15088.5 18,802.8 19,220.3 16,956.0 15,276.3 33,817.5
road runner 39544.0 44127.0 62,785.0 69,524.0 63,366.0 41,681.0 62,041.0
| robotank | 63.9 | 65.1 | 58.6 | 65.3 | 54.2 | 53.5 | 61.4 |
| -------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
seaquest 5860.6 16452.7 44,417.4 50,254.2 4,754.4 2,495.4 15,898.9
skiing -13062.3 -9021.8 -9,900.5 -8,857.4 -14,959.8 -16,307.3 -12,957.8
solaris 3482.8 3067.8 1,710.8 2,250.8 5,643.1 3,204.5 3,560.3
space invaders 1692.3 2525.5 7,696.9 6,427.3 6,869.1 2,145.5 18,789.0
star gunner 54282.0 60142.0 56,641.0 89,238.0 69,306.5 34,504.5 127,029.0
| surround | -5.6 | -2.9  | 2.1 | 4.4 | 6.2  | -3.3 | 9.7  |
| -------- | ---- | ----- | --- | --- | ---- | ---- | ---- |
| tennis   | 12.2 | -22.8 | 0.0 | 5.1 | 23.6 | 0.0  | -0.0 |
time pilot 4870.0 8339.0 11,448.0 11,666.0 7,875.0 6,157.0 12,926.0
| tutankham | 68.1  | 218.4 | 87.2  | 211.4 | 249.4   | 231.6 | 241.0 |
| --------- | ----- | ----- | ----- | ----- | ------- | ----- | ----- |
| venture   | 163.0 | 98.0  | 863.0 | 497.0 | 1,107.0 | 0.0   | 5.5   |
video pinball 196760.4 309941.9 406,420.4 98,209.5 478,646.7 270,444.6 533,936.5
wizard of wor 2704.0 7492.0 10,373.0 7,855.0 15,994.5 5,432.0 17,862.5
yars revenge 18089.9 11712.6 16,451.7 49,622.1 16,608.6 9,570.1 102,557.0
zaxxon 5363.0 10163.0 13,490.0 12,944.0 18,347.5 9,390.0 22,209.5
Table 6: No-op starts evaluation regime: Raw scores across all games, averaged over 200 testing episodes, from the agent
snapshotthatobtainedthehighestscoreduringtraining.WereportthepublishedscoresforDQN,DDQN,DuelingDDQN,and
PrioritizedDDQN.ForDistributionalDQNandRainbowwereportourownevaluationsoftheagents.A3Cisnotlistedsince
thepaperdidnotreportthescoresfortheno-opsregime.

1.01e4 alien 61e3 amidar 2.01e4 assault 81e5 asterix 1e3 asteroids
4
|     | 4   |     | 1.5 | 6   |     |
| --- | --- | --- | --- | --- | --- |
| 0.5 |     |     | 1.0 | 4   | 2   |
2
|     |     |     | 0.5 | 2   |     |
| --- | --- | --- | --- | --- | --- |
| 0.0 | 0   |     | 0.0 | 0   | 0   |
1.51e6 atlantis 1.51e3 bank_heist 81e4 battle_zone 2.01e4 beam_rider 31e3 berzerk
| 1.0 | 1.0 |     | 6   | 1.5 | 2   |
| --- | --- | --- | --- | --- | --- |
|     |     |     | 4   | 1.0 |     |
| 0.5 | 0.5 |     |     |     | 1   |
|     |     |     | 2   | 0.5 |     |
| 0.0 | 0.0 |     | 0   | 0.0 | 0   |
bowling boxing breakout 1.01e4 centipede 2.01e4chopper_command
| 80  | 100 |     | 800 |     |     |
| --- | --- | --- | --- | --- | --- |
| 60  | 50  |     | 600 |     | 1.5 |
| 40  | 0   |     | 400 | 0.5 | 1.0 |
| 20  | 50  |     | 200 |     | 0.5 |
| 0   | 100 |     | 0   | 0.0 | 0.0 |
2.01e5 crazy_climber 61e4 defender 1.51e5 demon_attack double_dunk 41e3 enduro
10
| 1.5 | 4   |     | 1.0 | 0   | 3   |
| --- | --- | --- | --- | --- | --- |
| 1.0 |     |     |     | 10  | 2   |
|     | 2   |     | 0.5 |     |     |
| 0.5 |     |     |     | 20  | 1   |
| 0.0 | 0   |     | 0.0 | 30  | 0   |
fishing_derby freeway 1.01e4 frostbite 81e4 gopher 31e3 gravitar
| 50  | 40  |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
| 0   | 30  |     |     | 6   | 2   |
|     | 20  |     | 0.5 | 4   |     |
| 50  |     |     |     |     | 1   |
|     | 10  |     |     | 2   |     |
| 100 | 0   |     | 0.0 | 0   | 0   |
61e4 hero ice_hockey 31e4 jamesbond 1.51e4 kangaroo 1.01e4 krull
10
| 4   | 0   |     | 2   | 1.0 |     |
| --- | --- | --- | --- | --- | --- |
|     | 10  |     |     |     | 0.5 |
| 2   |     |     | 1   | 0.5 |     |
20
| 0   | 30  |     | 0   | 0.0 | 0.0 |
| --- | --- | --- | --- | --- | --- |
61e4 kung_fu_master montezuma_revenge 61e3 ms_pacman 1.51e4name_this_game 31e5 phoenix
400
| 4   | 300 |     | 4   | 1.0 | 2   |
| --- | --- | --- | --- | --- | --- |
200
| 2   |     |     | 2   | 0.5 | 1   |
| --- | --- | --- | --- | --- | --- |
100
| 0   | 0   |     | 0   | 0.0 | 0   |
| --- | --- | --- | --- | --- | --- |
0.01e3 pitfall pong 21e4 private_eye 41e4 qbert 31e4 riverraid
40
| 0.5 | 20  |     | 1   | 3   | 2   |
| --- | --- | --- | --- | --- | --- |
|     | 0   |     |     | 2   |     |
| 1.0 |     |     | 0   |     | 1   |
|     | 20  |     |     | 1   |     |
| 1.5 | 40  |     | 1   | 0   | 0   |
81e4 road_runner robotank 41e4 seaquest 01e4 skiing 41e3 solaris
80
| 6   | 60  |     | 3   | 1   | 3   |
| --- | --- | --- | --- | --- | --- |
| 4   | 40  |     | 2   | 2   | 2   |
| 2   | 20  |     | 1   | 3   | 1   |
| 0   | 0   |     | 0   | 4   | 0   |
31e4 space_invaders 1.51e5 star_gunner surround tennis 2.01e4 time_pilot
|     |     |     | 10  | 40  |     |
| --- | --- | --- | --- | --- | --- |
| 2   | 1.0 |     | 5   | 20  | 1.5 |
|     |     |     | 0   | 0   | 1.0 |
| 1   | 0.5 |     |     |     |     |
|     |     |     | 5   | 20  | 0.5 |
| 0   | 0.0 |     | 10  | 40  | 0.0 |
tutankham 1.51e5 up_n_down venture 81e5 video_pinball 2.01e4 wizard_of_wor
| 400 |     |     | 800 |     |     |
| --- | --- | --- | --- | --- | --- |
| 300 | 1.0 |     | 600 | 6   | 1.5 |
| 200 |     |     | 400 | 4   | 1.0 |
0.5
| 100 |     |     | 200 | 2   | 0.5 |
| --- | --- | --- | --- | --- | --- |
| 0   | 0.0 |     | 0   | 0   | 0.0 |
1.51e5 yars_revenge 31e4 zaxxon 0 50 100 150 200 0 50 100 150 200 0 50 100 150 200
DQN A3C
| 1.0 | 2   |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
DDQN Distributional DQN
Prioritized DDQN Noisy DQN
| 0.5 | 1   |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
Dueling DDQN Rainbow
| 0.0  | 0           |          |         |     |     |
| ---- | ----------- | -------- | ------- | --- | --- |
| 0 50 | 100 150 200 | 0 50 100 | 150 200 |     |     |
Figure 5: Learning curves for Rainbow and the baselines discussed in the paper, for each individual game. Every curve is
smoothedwithamovingaverageof10toimprovereadability.

1.51e4 alien 61e3 amidar 2.01e4 assault 61e5 asterix 81e3 asteroids
| 1.0 | 4   |     | 1.5 | 4   | 6   |
| --- | --- | --- | --- | --- | --- |
|     |     |     | 1.0 |     | 4   |
| 0.5 | 2   |     |     | 2   |     |
|     |     |     | 0.5 |     | 2   |
| 0.0 | 0   |     | 0.0 | 0   | 0   |
1.51e6 atlantis 2.01e3 bank_heist 81e4 battle_zone 31e4 beam_rider 61e3 berzerk
| 1.0 | 1.5 |     | 6   | 2   | 4   |
| --- | --- | --- | --- | --- | --- |
|     | 1.0 |     | 4   |     |     |
| 0.5 |     |     |     | 1   | 2   |
|     | 0.5 |     | 2   |     |     |
| 0.0 | 0.0 |     | 0   | 0   | 0   |
bowling boxing breakout 1.01e4 centipede 2.01e4chopper_command
| 100 | 100 |     | 600 |     |     |
| --- | --- | --- | --- | --- | --- |
|     | 50  |     | 400 |     | 1.5 |
| 50  |     |     |     | 0.5 | 1.0 |
|     | 0   |     | 200 |     |     |
0.5
| 0   | 50  |     | 0   | 0.0 | 0.0 |
| --- | --- | --- | --- | --- | --- |
31e5 crazy_climber 31e5 defender 1.51e5 demon_attack 21e1 double_dunk 31e3 enduro
| 2   | 2   |     | 1.0 | 0   | 2   |
| --- | --- | --- | --- | --- | --- |
| 1   | 1   |     | 0.5 | 2   | 1   |
| 0   | 0   |     | 0.0 | 4   | 0   |
fishing_derby 41e1 freeway 1.01e4 frostbite 81e4 gopher 31e3 gravitar
100
| 50  | 3   |     |     | 6   | 2   |
| --- | --- | --- | --- | --- | --- |
| 0   | 2   |     | 0.5 | 4   |     |
1
| 50  | 1   |     |     | 2   |     |
| --- | --- | --- | --- | --- | --- |
| 100 | 0   |     | 0.0 | 0   | 0   |
61e4 hero 11e1 ice_hockey 31e4 jamesbond 1.51e4 kangaroo 1.51e4 krull
| 4   | 0   |     | 2   | 1.0 | 1.0 |
| --- | --- | --- | --- | --- | --- |
| 2   | 1   |     | 1   | 0.5 | 0.5 |
| 0   | 2   |     | 0   | 0.0 | 0.0 |
61e4 kung_fu_master montezuma_revenge 61e3 ms_pacman 2.01e4name_this_game 41e5 phoenix
600
| 4   | 400 |     | 4   | 1.5 | 3   |
| --- | --- | --- | --- | --- | --- |
|     |     |     |     | 1.0 | 2   |
| 2   | 200 |     | 2   |     |     |
|     |     |     |     | 0.5 | 1   |
| 0   | 0   |     | 0   | 0.0 | 0   |
0.01e3 pitfall 41e1 pong 21e3 private_eye 41e4 qbert 31e4 riverraid
| 0.5 | 2   |     | 1   | 3   | 2   |
| --- | --- | --- | --- | --- | --- |
|     | 0   |     |     | 2   |     |
| 1.0 |     |     | 0   |     | 1   |
|     | 2   |     |     | 1   |     |
| 1.5 | 4   |     | 1   | 0   | 0   |
81e4 road_runner 81e1 robotank 31e5 seaquest 01e4 skiing 41e3 solaris
| 6   | 6   |     | 2   | 1   | 3   |
| --- | --- | --- | --- | --- | --- |
| 4   | 4   |     |     | 2   | 2   |
1
| 2   | 2   |     |     | 3   | 1   |
| --- | --- | --- | --- | --- | --- |
| 0   | 0   |     | 0   | 4   | 0   |
31e4 space_invaders 1.51e5 star_gunner 1.01e1 surround 11e1 tennis 2.01e4 time_pilot
| 2   | 1.0 |     | 0.5 | 0   | 1.5 |
| --- | --- | --- | --- | --- | --- |
|     |     |     | 0.0 | 1   | 1.0 |
| 1   | 0.5 |     |     |     |     |
|     |     |     | 0.5 | 2   | 0.5 |
| 0   | 0.0 |     | 1.0 | 3   | 0.0 |
tutankham 2.01e5 up_n_down 1.51e3 venture 81e5 video_pinball 2.01e4 wizard_of_wor
400
| 300 | 1.5 |     | 1.0 | 6   | 1.5 |
| --- | --- | --- | --- | --- | --- |
| 200 | 1.0 |     |     | 4   | 1.0 |
0.5
| 100 | 0.5 |     |     | 2   | 0.5 |
| --- | --- | --- | --- | --- | --- |
| 0   | 0.0 |     | 0.0 | 0   | 0.0 |
1.51e5 yars_revenge 31e4 zaxxon 0 50 100 150 200 0 50 100 150 200 0 50 100 150 200
DQN no n-steps
| 1.0 | 2   |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
no double no distrib
no prior no noisy
| 0.5 | 1   |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
no duel Rainbow
| 0.0  | 0           |          |         |     |     |
| ---- | ----------- | -------- | ------- | --- | --- |
| 0 50 | 100 150 200 | 0 50 100 | 150 200 |     |     |
Figure 6: Learning curves for Rainbow and its ablations, for each individual game. Every curve is smoothed with a moving
averageof10toimprovereadability.