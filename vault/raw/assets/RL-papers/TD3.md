Addressing Function Approximation Error in Actor-Critic Methods
|                |               | ScottFujimoto1   | HerkevanHoof2 | DavidMeger1                                       |                 |                          |               |
| -------------- | ------------- | ---------------- | ------------- | ------------------------------------------------- | --------------- | ------------------------ | ------------- |
|                | Abstract      |                  |               | meansusinganimpreciseestimatewithineachupdatewill |                 |                          |               |
|                |               |                  |               | leadtoanaccumulationoferror.                      |                 | Duetooverestimationbias, |               |
| In value-based | reinforcement | learning methods |               |                                                   |                 |                          |               |
|                |               |                  |               | this accumulated                                  | error can cause | arbitrarily              | bad states to |
suchasdeepQ-learning,functionapproximation
beestimatedashighvalue,resultinginsuboptimalpolicy
8102 tcO 22  ]IA.sc[  3v77490.2081:viXra errorsareknowntoleadtooverestimatedvalue
updatesanddivergentbehavior.
| estimatesandsuboptimalpolicies. |     | Weshowthat |     |     |     |     |     |
| ------------------------------- | --- | ---------- | --- | --- | --- | --- | --- |
thisproblempersistsinanactor-criticsettingand Thispaperbeginsbyestablishingthisoverestimationprop-
proposenovelmechanismstominimizeitseffects ertyisalsopresentfordeterministicpolicygradients(Silver
on both the actor and the critic. Our algorithm etal.,2014),inthecontinuouscontrolsetting. Furthermore,
buildsonDoubleQ-learning,bytakingthemini- wefindtheubiquitoussolutioninthediscreteactionsetting,
mumvaluebetweenapairofcriticstolimitover- DoubleDQN(VanHasseltetal.,2016), tobeineffective
estimation. Wedrawtheconnectionbetweentar- in an actor-critic setting. During training, Double DQN
getnetworksandoverestimationbias,andsuggest estimatesthevalueofthecurrentpolicywithaseparatetar-
delayingpolicyupdatestoreduceper-updateerror getvaluefunction,allowingactionstobeevaluatedwithout
and further improve performance. We evaluate maximizationbias. Unfortunately,duetotheslow-changing
our method on the suite of OpenAI gym tasks, policyinanactor-criticsetting,thecurrentandtargetvalue
outperformingthestateoftheartineveryenvi- estimates remain too similar to avoid maximization bias.
ronmenttested. Thiscanbedealtwithbyadaptinganoldervariant,Double
|     |     |     |     | Q-learning (Van                            | Hasselt, 2010), | to an actor-critic | format    |
| --- | --- | --- | --- | ------------------------------------------ | --------------- | ------------------ | --------- |
|     |     |     |     | byusingapairofindependentlytrainedcritics. |                 |                    | Whilethis |
1.Introduction allowsforalessbiasedvalueestimation,evenanunbiased
estimatewithhighvariancecanstillleadtofutureoveres-
| In reinforcement | learning problems | with discrete | action |     |     |     |     |
| ---------------- | ----------------- | ------------- | ------ | --- | --- | --- | --- |
timationsinlocalregionsofstatespace,whichinturncan
spaces,theissueofvalueoverestimationasaresultoffunc- negativelyaffecttheglobalpolicy. Toaddressthisconcern,
| tionapproximationerrorsiswell-studied. |     | However,similar |     |     |     |     |     |
| -------------------------------------- | --- | --------------- | --- | --- | --- | --- | --- |
weproposeaclippedDoubleQ-learningvariantwhichlever-
issueswithactor-criticmethodsincontinuouscontroldo-
agesthenotionthatavalueestimatesufferingfromoveres-
mainshavebeenlargelyleftuntouched. Inthispaper,we timationbiascanbeusedasanapproximateupper-boundto
showoverestimationbiasandtheaccumulationoferrorin
|     |     |     |     | thetruevalueestimate. | Thisfavorsunderestimations,which |     |     |
| --- | --- | --- | --- | --------------------- | -------------------------------- | --- | --- |
temporaldifferencemethodsarepresentinanactor-critic donottendtobepropagatedduringlearning,asactionswith
setting. Ourproposedmethodaddressestheseissues,and
lowvalueestimatesareavoidedbythepolicy.
greatlyoutperformsthecurrentstateoftheart.
Giventheconnectionofnoisetooverestimationbias,this
OverestimationbiasisapropertyofQ-learninginwhichthe
papercontainsanumberofcomponentsthataddressvari-
maximizationofanoisyvalueestimateinducesaconsistent
|     |     |     |     | ancereduction. | First,weshowthattargetnetworks,acom- |     |     |
| --- | --- | --- | --- | -------------- | ------------------------------------ | --- | --- |
overestimation (Thrun & Schwartz, 1993). In a function monapproachindeepQ-learningmethods,arecriticalfor
approximationsetting,thisnoiseisunavoidablegiventhe
variancereductionbyreducingtheaccumulationoferrors.
imprecision of the estimator. This inaccuracy is further Second, to address the coupling of value and policy, we
exaggeratedbythenatureoftemporaldifferencelearning
|     |     |     |     | propose delaying | policy updates | until the value | estimate |
| --- | --- | --- | --- | ---------------- | -------------- | --------------- | -------- |
(Sutton,1988),inwhichanestimateofthevaluefunction
|     |     |     |     | hasconverged. | Finally,weintroduceanovelregularization |     |     |
| --- | --- | --- | --- | ------------- | --------------------------------------- | --- | --- |
is updated using the estimate of a subsequent state. This strategy, where a SARSA-style update bootstraps similar
1McGillUniversity,Montreal,Canada2UniversityofAmster- actionestimatestofurtherreducevariance.
dam,Amsterdam,Netherlands.Correspondenceto:ScottFujimoto Ourmodificationsareappliedtothestateoftheartactor-
<scott.fujimoto@mail.mcgill.ca>.
|             |                      |            |            | criticmethodforcontinuouscontrol,                     |     | DeepDeterministic |     |
| ----------- | -------------------- | ---------- | ---------- | ----------------------------------------------------- | --- | ----------------- | --- |
|             | 35th                 |            |            | PolicyGradientalgorithm(DDPG)(Lillicrapetal.,2015),to |     |                   |     |
| Proceedings | of the International | Conference | on Machine |                                                       |     |                   |     |
formtheTwinDelayedDeepDeterministicpolicygradient
Learning,Stockholm,Sweden,PMLR80,2018.Copyright2018
bytheauthor(s).

AddressingFunctionApproximationErrorinActor-CriticMethods
algorithm (TD3), an actor-critic algorithm which consid- horizon. Anotherapproachisareductioninthediscount
erstheinterplaybetweenfunctionapproximationerrorin factor(Petrik&Scherrer,2009),reducingthecontribution
| bothpolicyandvalueupdates. |     |         | Weevaluateouralgorithm |        |     | ofeacherror. |        |     |                   |     |        |          |
| -------------------------- | --- | ------- | ---------------------- | ------ | --- | ------------ | ------ | --- | ----------------- | --- | ------ | -------- |
| on seven continuous        |     | control | domains from           | OpenAI | gym |              |        |     |                   |     |        |          |
|                            |     |         |                        |        |     | Our method   | builds | on  | the Deterministic |     | Policy | Gradient |
(Brockmanetal.,2016),whereweoutperformthestateof
algorithm(DPG)(Silveretal.,2014),anactor-criticmethod
theartbyawidemargin.
whichusesalearnedvalueestimatetotrainadeterministic
Given the recent concerns in reproducibility (Henderson policy. AnextensionofDPGtodeepreinforcementlearn-
etal.,2017), werunourexperimentsacrossalargenum- ing,DDPG(Lillicrapetal.,2015),hasshowntoproduce
ber of seeds with fair evaluation metrics, perform abla- stateoftheartresultswithanefficientnumberofiterations.
tionstudiesacrosseachcontribution,andopensourceboth Orthogonaltoourapproach,recentimprovementstoDDPG
ourcodeandlearningcurves(https://github.com/ includedistributedmethods(Popovetal.,2017),alongwith
sfujim/TD3). multi-stepreturnsandprioritizedexperiencereplay(Schaul
etal.,2016;Horganetal.,2018),anddistributionalmethods
(Bellemareetal.,2017;Barth-Maronetal.,2018).
2.RelatedWork
| Function approximation |     | error | and its effect | on bias | and |     |     |     |     |     |     |     |
| ---------------------- | --- | ----- | -------------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
3.Background
| variance in | reinforcement | learning | algorithms | have | been |     |     |     |     |     |     |     |
| ----------- | ------------- | -------- | ---------- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
studiedinpriorworks(Pendrithetal.,1997;Mannoretal., Reinforcementlearningconsiderstheparadigmofanagent
2007). Ourworkfocusesontwooutcomesthatoccurasthe interacting with its environment with the aim of learning
resultofestimationerror,namelyoverestimationbiasanda reward-maximizing behavior. At each discrete time step
highvariancebuild-up. t, with a given state s , the agent selects actions
|     |     |     |     |     |     |     |      |         | ∈ S           |     |     |           |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------- | ------------- | --- | --- | --------- |
|     |     |     |     |     |     | a   | with | respect | to its policy | π   | :   | , receiv- |
Severalapproachesexisttoreducetheeffectsofoverestima-
|     |     |     |     |     |     | ∈     | A      |           |     |          | S →             | A s(cid:48). |
| --- | --- | --- | --- | --- | --- | ----- | ------ | --------- | --- | -------- | --------------- | ------------ |
|     |     |     |     |     |     | ing a | reward | r and the | new | state of | the environment |              |
tionbiasduetofunctionapproximationandpolicyoptimiza-
|     |     |     |     |     |     | The return | is  | defined | as the | discounted | sum | of rewards |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ------- | ------ | ---------- | --- | ---------- |
tioninQ-learning.DoubleQ-learningusestwoindependent
|     |     |     |     |     |     | R = | (cid:80)T γi−tr(s | ,a  | ),whereγ | isadiscountfactorde- |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | -------- | -------------------- | --- | --- |
|     |     |     |     |     |     | t   | i=t               | i   | i        |                      |     |     |
estimatorstomakeunbiasedvalueestimates(VanHasselt,
terminingthepriorityofshort-termrewards.
| 2010; Van | Hasselt et | al., 2016). | Other approaches |     | have |     |     |     |     |     |     |     |
| --------- | ---------- | ----------- | ---------------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
focuseddirectlyonreducingthevariance(Anscheletal., In reinforcement learning, the objective is to find the op-
2017),minimizingover-fittingtoearlyhighvarianceesti- timalpolicyπ ,withparametersφ,whichmaximizesthe
φ
mates(Foxetal.,2016),orthroughcorrectiveterms(Lee expectedreturnJ(φ)=E [R ]. Forcontinuous
|     |     |     |     |     |     |     |     |     | si∼pπ,ai∼π |     | 0   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- |
et al., 2013). Further, the variance of the value estimate control,parametrizedpoliciesπ φ canbeupdatedbytaking
hasbeenconsidereddirectlyforrisk-aversion(Mannor& thegradientoftheexpectedreturn J(φ). Inactor-critic
∇ φ
Tsitsiklis,2011)andexploration(O’Donoghueetal.,2017), methods, the policy, known as the actor, can be updated
butwithoutconnectiontooverestimationbias. throughthedeterministicpolicygradientalgorithm(Silver
etal.,2014):
Theconcernofvarianceduetotheaccumulationoferrorin
|     |     |     |     |     |     |     |     | (cid:2) |     |     |     | (cid:3) |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | ------- |
temporaldifferencelearninghasbeenlargelydealtwithby J(φ)=E Qπ(s,a) π (s) . (1)
|     |     |     |     |     |     | ∇ φ |     | s∼pπ ∇ | a   | | a=π(s) | ∇ φ | φ   |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | -------- | --- | --- |
eitherminimizingthesizeoferrorsateachtimestepormix-
|     |     |     |     |     |     | Qπ(s,a) |     | E   |     |       |              |        |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | ----- | ------------ | ------ |
|     |     |     |     |     |     |         | =   |     | [R  | s,a], | the expected | return |
ingoff-policyandMonte-Carloreturns. Ourworkshows si∼pπ,ai∼π t |
|     |     |     |     |     |     | when | performing | action | a in | state | s and following | π af- |
| --- | --- | --- | --- | --- | --- | ---- | ---------- | ------ | ---- | ----- | --------------- | ----- |
theimportanceofastandardtechnique,targetnetworks,for
thereductionofper-updateerror,anddevelopsaregulariza- ter,isknownasthecriticorthevaluefunction.
tiontechniqueforthevariancereductionbyaveragingover InQ-learning,thevaluefunctioncanbelearnedusingtem-
valueestimates.Concurrently,Nachumetal.(2018)showed
poraldifferencelearning(Sutton,1988;Watkins,1989),an
smoothedvaluefunctionscouldbeusedtotrainstochastic
updaterulebasedontheBellmanequation(Bellman,1957).
policieswithreducedvarianceandimprovedperformance. TheBellmanequationisafundamentalrelationshipbetween
Methodswithmulti-stepreturnsofferatrade-offbetween
thevalueofastate-actionpair(s,a)andthevalueofthe
accumulatedestimationbiasandvarianceinducedbythe subsequentstate-actionpair(s(cid:48),a(cid:48)):
| policy and | the environment. |     | These methods | have | been |     |     |     |     |     |     |     |
| ---------- | ---------------- | --- | ------------- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
Qπ(s,a)=r+γE
showntobeaneffectiveapproach,throughimportancesam- [Qπ(s(cid:48),a(cid:48))], a(cid:48) π(s(cid:48)). (2)
|     |     |     |     |     |     |     |     | s(cid:48),a(cid:48) |     |     | ∼   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- |
pling(Precupetal.,2001;Munosetal.,2016),distributed
methods(Mnihetal.,2016;Espeholtetal.,2018),andap- Foralargestatespace, thevaluecanbeestimatedwitha
|                                |     |     |                    |     |     | differentiablefunctionapproximatorQ |     |     |     |     | (s,a),withparam- |     |
| ------------------------------ | --- | --- | ------------------ | --- | --- | ----------------------------------- | --- | --- | --- | --- | ---------------- | --- |
| proximatebounds(Heetal.,2016). |     |     | However,ratherthan |     |     |                                     |     |     |     |     | θ                |     |
provideadirectsolutiontotheaccumulationoferror,these etersθ. IndeepQ-learning(Mnihetal.,2015),thenetwork
methodscircumventtheproblembyconsideringalonger isupdatedbyusingtemporaldifferencelearningwithasec-
|     |     |     |     |     |     | ondaryfrozentargetnetworkQ |     |     |     | (s,a)tomaintainafixed |     |     |
| --- | --- | --- | --- | --- | --- | -------------------------- | --- | --- | --- | --------------------- | --- | --- |
θ(cid:48)

AddressingFunctionApproximationErrorinActor-CriticMethods
objectiveyovermultipleupdates: 400
300 y =r+γQ (s(cid:48),a(cid:48)), a(cid:48) π (s(cid:48)), (3)
θ(cid:48) φ(cid:48) ∼ 200
wheretheactionsareselectedfromatargetactornetwork
100
π . The weights of a target network are either updated φ(cid:48)
0
periodically to exactly match the weights of the current 0.0 0.2 0.4 0.6 0.8 1.0
network,orbysomeproportionτ ateachtimestepθ(cid:48) Timesteps(1e6)
←
τθ+(1 τ)θ(cid:48). Thisupdatecanbeappliedinanoff-policy
−
fashion,samplingrandommini-batchesoftransitionsfrom
anexperiencereplaybuffer(Lin,1992).
4.OverestimationBias
In Q-learning with discrete actions, the value estimate is
updated with a greedy target y = r +γmax Q(s(cid:48),a(cid:48)),
a(cid:48)
however,ifthetargetissusceptibletoerror(cid:15),thenthemax-
imumoverthevaluealongwithitserrorwillgenerallybe
greaterthanthetruemaximum,E [max (Q(s(cid:48),a(cid:48))+(cid:15))] (cid:15) a(cid:48) ≥
max Q(s(cid:48),a(cid:48)) (Thrun & Schwartz, 1993). As a result, a(cid:48)
eveninitiallyzero-meanerrorcancausevalueupdatesto
resultinaconsistentoverestimationbias,whichisthenprop-
agatedthroughtheBellmanequation.Thisisproblematicas
errorsinducedbyfunctionapproximationareunavoidable.
Whileinthediscreteactionsettingoverestimationbiasis
an obvious artifact fromthe analytical maximization, the
presenceandeffectsofoverestimationbiasislessclearinan
actor-criticsettingwherethepolicyisupdatedviagradient
descent. Webeginbyprovingthatthevalueestimateinde-
terministicpolicygradientswillbeanoverestimationunder
some basic assumptions in Section 4.1 and then propose
a clipped variant of Double Q-learning in an actor-critic
settingtoreduceoverestimationbiasinSection4.2.
4.1.OverestimationBiasinActor-Critic
Inactor-criticmethodsthepolicyisupdatedwithrespect
to the value estimates of an approximate critic. In this
section we assume the policy is updated using the deter-
ministicpolicygradient,andshowthattheupdateinduces
overestimationinthevalueestimate. Givencurrentpolicy
parametersφ,letφ definetheparametersfromtheac-
approx
torupdateinducedbythemaximizationoftheapproximate
criticQ (s,a)andφ theparametersfromthehypothet-
θ true
icalactorupdatewithrespecttothetrueunderlyingvalue
functionQπ(s,a)(whichisnotknownduringlearning):
φ =φ+ α E (cid:2) π (s) Q (s,a) (cid:3)
approx Z s∼pπ ∇ φ φ ∇ a θ | a=πφ(s)
1
φ =φ+ α E (cid:2) π (s) Qπ(s,a) (cid:3) ,
true Z s∼pπ ∇ φ φ ∇ a | a=πφ(s)
2
(4)
whereweassumeZ andZ arechosentonormalizethe
1 2
gradient, i.e., suchthatZ−1 E[] = 1. Withoutnormal-
|| ·||
ized gradients, overestimation bias is still guaranteed to
eulaVegarevA
500
400
300
200
CDQ TrueCDQ 100
DDPG TrueDDPG
0
0.0 0.2 0.4 0.6 0.8 1.0
Timesteps(1e6)
(a)Hopper-v1 (b)Walker2d-v1
Figure1.Measuring overestimation bias in the value estimates
ofDDPGandourproposedmethod,ClippedDoubleQ-learning
(CDQ),onMuJoCoenvironmentsover1milliontimesteps.
occurwithslightlystricterconditions. Weexaminethiscase
further in the supplementary material. We denote π
approx
andπ asthepolicywithparametersφ andφ re-
true approx true
spectively.
Asthegradientdirectionisalocalmaximizer,thereexists(cid:15) 1
sufficientlysmallsuchthatifα (cid:15) thentheapproximate 1
≤
valueofπ willbeboundedbelowbytheapproximate
approx
valueofπ :
true
E[Q (s,π (s))] E[Q (s,π (s))]. (5) θ approx θ true
≥
Conversely, there exists (cid:15) sufficiently small such that if
2
α (cid:15) thenthetruevalueofπ willbeboundedabove
2 approx
≤
bythetruevalueofπ :
true
E[Qπ(s,π (s))] E[Qπ(s,π (s))]. (6) true approx
≥
If in expectation the value estimate is at least as large as
thetruevaluewithrespecttoφ ,E[Q (s,π (s))]
true θ true E[Qπ(s,π (s))],thenEquations(5)and(6)implythat ≥ if
true
α < min((cid:15) ,(cid:15) ),thenthevalueestimatewillbeoveresti-
1 2
mated:
E[Q (s,π (s))] E[Qπ(s,π (s))]. (7)
θ approx approx
≥
Although this overestimation may be minimal with each
update,thepresenceoferrorraisestwoconcerns.Firstly,the
overestimationmaydevelopintoamoresignificantbiasover
many updates if left unchecked. Secondly, an inaccurate
value estimate may lead to poor policy updates. This is
particularlyproblematicbecauseafeedbackloopiscreated,
inwhichsuboptimalactionsmightbehighlyratedbythe
suboptimalcritic,reinforcingthesuboptimalactioninthe
nextpolicyupdate.
Does this theoretical overestimation occur in practice
forstate-of-the-artmethods? Weanswerthisquestionby
plottingthevalueestimateofDDPG(Lillicrapetal.,2015)
overtimewhileitlearnsontheOpenAIgymenvironments
Hopper-v1and Walker2d-v1(Brockmanetal.,2016). In
Figure1,wegraphtheaveragevalueestimateover10000
statesandcompareittoanestimateofthetruevalue. The

AddressingFunctionApproximationErrorinActor-CriticMethods
| 400 |     |     |     |     |     |     | demonstratesthattheactor-criticDoubleDQNsuffersfrom |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
400
asimilaroverestimationasDDPG(asshowninFigure1).
300
| eulaVegarevA |     |     |     | 300 |     |     |     |     |     |     |     |     |     |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
WhileDoubleQ-learningismoreeffective,itdoesnoten-
200
200 tirely eliminate the overestimation. We further show this
reductionisnotsufficientexperimentallyinSection6.1.
| 100 | DQ-AC | TrueDQ-AC |     | 100 |     |     |     |     |     |     |     |     |     |     |
| --- | ----- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
DDQN-AC TrueDDQN-AC
| 0   |         |         |     | 0       |     |             | As π | optimizes | with | respect | to Q | , using | an indepen- |     |
| --- | ------- | ------- | --- | ------- | --- | ----------- | ---- | --------- | ---- | ------- | ---- | ------- | ----------- | --- |
| 0.0 | 0.2 0.4 | 0.6 0.8 | 1.0 | 0.0 0.2 | 0.4 | 0.6 0.8 1.0 | φ1   |           |      |         | θ1   |         |             |     |
Timesteps(1e6) Timesteps(1e6) dentestimateinthetargetupdateofQ wouldavoidthe
θ1
|     | (a)Hopper-v1 |     |     |     | (b)Walker2d-v1 |     |                                  |          |              |     |     |                   |        |       |
| --- | ------------ | --- | --- | --- | -------------- | --- | -------------------------------- | -------- | ------------ | --- | --- | ----------------- | ------ | ----- |
|     |              |     |     |     |                |     | biasintroducedbythepolicyupdate. |          |              |     |     | Howeverthecritics |        |       |
|     |              |     |     |     |                |     | are not                          | entirely | independent, | due | to  | the use           | of the | oppo- |
Figure2.Measuringoverestimationbiasinthevalueestimatesof
|     |     |     |     |     |     |     | site critic | in the | learning | targets, | as  | well as | the same | re- |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------ | -------- | -------- | --- | ------- | -------- | --- |
actorcriticvariantsofDoubleDQN(DDQN-AC)andDoubleQ-
|     |     |     |     |     |     |     | play buffer. | As  | a result, | for some | states | s we | will | have |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --------- | -------- | ------ | ---- | ---- | ---- |
learning(DQ-AC)onMuJoCoenvironmentsover1milliontime
|        |     |     |     |     |     |     | Q (s,π | (s))    | > Q                                     | (s,π (s)). | Thisisproblematicbe- |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | ------ | ------- | --------------------------------------- | ---------- | -------------------- | --- | --- | --- |
| steps. |     |     |     |     |     |     | θ2     | φ1      | θ1                                      | φ1         |                      |     |     |     |
|        |     |     |     |     |     |     | causeQ | θ1 (s,π | φ1 (s))willgenerallyoverestimatethetrue |            |                      |     |     |     |
value,andincertainareasofthestatespacetheoverestima-
truevalueisestimatedusingtheaveragediscountedreturn
|           |          |           |     |             |         |          | tionwillbefurtherexaggerated. |     |        |             | Toaddressthisproblem, |      |        |       |
| --------- | -------- | --------- | --- | ----------- | ------- | -------- | ----------------------------- | --- | ------ | ----------- | --------------------- | ---- | ------ | ----- |
| over 1000 | episodes | following |     | the current | policy, | starting |                               |     |        |             |                       |      |        |       |
|           |          |           |     |             |         |          | we propose                    | to  | simply | upper-bound | the                   | less | biased | value |
from states sampled from the replay buffer. A very clear estimate Q by the biased estimate Q . This results in
|                |     |             |      |     |          |            |     | θ2  |     |     |     | θ1  |     |     |
| -------------- | --- | ----------- | ---- | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
| overestimation |     | bias occurs | from | the | learning | procedure, |     |     |     |     |     |     |     |     |
takingtheminimumbetweenthetwoestimates,togivethe
whichcontrastswiththenovelmethodthatwedescribein
targetupdateofourClippedDoubleQ-learningalgorithm:
thefollowingsection,ClippedDoubleQ-learning,which
greatlyreducesoverestimationbythecritic. y =r+γ minQ (s(cid:48),π (s(cid:48))). (10)
|     |     |     |     |     |     |     |     | 1   |     | θ     | (cid:48) | φ1  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | -------- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     |     | i=1,2 | i        |     |     |     |
4.2.ClippedDoubleQ-LearningforActor-Critic With Clipped Double Q-learning, the value target cannot
introduceanyadditionaloverestimationoverusingthestan-
Whileseveralapproachestoreducingoverestimationbias
|     |     |     |     |     |     |     | dardQ-learningtarget. |     |     | Whilethisupdaterulemayinduce |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------- | --- | --- | ---------------------------- | --- | --- | --- | --- |
havebeenproposed,wefindthemineffectiveinanactor-
|     |     |     |     |     |     |     | an underestimation |     | bias, | this is | far preferable |     | to overesti- |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------ | --- | ----- | ------- | -------------- | --- | ------------ | --- |
criticsetting.Thissectionintroducesanovelclippedvariant
mationbias,asunlikeoverestimatedactions,thevalueof
| of Double | Q-learning | (Van | Hasselt, | 2010), | which | can re- |                |     |         |          |               |     |            |     |
| --------- | ---------- | ---- | -------- | ------ | ----- | ------- | -------------- | --- | ------- | -------- | ------------- | --- | ---------- | --- |
|           |            |      |          |        |       |         | underestimated |     | actions | will not | be explicitly |     | propagated |     |
placethecriticinanyactor-criticmethod.
throughthepolicyupdate.
| In Double | Q-learning, |     | the greedy | update | is disentangled |     |     |     |     |     |     |     |     |     |
| --------- | ----------- | --- | ---------- | ------ | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Inimplementation,computationalcostscanbereducedby
fromthevaluefunctionbymaintainingtwoseparatevalue
|                                              |     |     |     |     |     |       | usingasingleactoroptimizedwithrespecttoQ |     |     |          |     |     | θ1 . Wethen |      |
| -------------------------------------------- | --- | --- | --- | --- | --- | ----- | ---------------------------------------- | --- | --- | -------- | --- | --- | ----------- | ---- |
| estimates,eachofwhichisusedtoupdatetheother. |     |     |     |     |     | Ifthe |                                          |     |     |          |     |     |             |      |
|                                              |     |     |     |     |     |       | usethesametargety                        |     |     | = y forQ | .   | IfQ | > Q         | then |
valueestimatesareindependent,theycanbeusedtomake 2 1 θ2 θ2 θ1
theupdateisidenticaltothestandardupdateandinducesno
unbiasedestimatesoftheactionsselectedusingtheopposite
|                |     |                                    |     |     |     |     | additionalbias. |     | IfQ | <Q ,thissuggestsoverestimation |     |     |     |     |
| -------------- | --- | ---------------------------------- | --- | --- | --- | --- | --------------- | --- | --- | ------------------------------ | --- | --- | --- | --- |
| valueestimate. |     | InDoubleDQN(VanHasseltetal.,2016), |     |     |     |     |                 |     | θ2  | θ1                             |     |     |     |     |
hasoccurredandthevalueisreducedsimilartoDoubleQ-
theauthorsproposeusingthetargetnetworkasoneofthe
learning. AproofofconvergenceinthefiniteMDPsetting
valueestimates,andobtainapolicybygreedymaximization
|     |     |     |     |     |     |     | followsfromthisintuition. |     |     | Weprovideformaldetailsand |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | ------------------------- | --- | --- | --- | --- |
ofthecurrentvaluenetworkratherthanthetargetnetwork.
justificationinthesupplementarymaterial.
Inanactor-criticsetting,ananalogousupdateusesthecur-
rentpolicyratherthanthetargetpolicyinthelearningtarget: Asecondarybenefitisthatbytreatingthefunctionapproxi-
mationerrorasarandomvariablewecanseethatthemin-
|     |     |     |     | (s(cid:48),π (s(cid:48))). |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
y =r+γQ θ(cid:48) (8) imumoperatorshouldprovidehighervaluetostateswith
φ
lowervarianceestimationerror,astheexpectedminimum
Inpracticehowever,wefoundthatwiththeslow-changing
|     |     |     |     |     |     |     | of a set | of random | variables | decreases |     | as the | variance | of  |
| --- | --- | --- | --- | --- | --- | --- | -------- | --------- | --------- | --------- | --- | ------ | -------- | --- |
policyinactor-critic,thecurrentandtargetnetworkswere
|     |     |     |     |     |     |     | therandomvariablesincreases. |     |     |     | Thiseffectmeansthatthe |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------- | --- | --- | --- | ---------------------- | --- | --- | --- |
toosimilartomakeanindependentestimation,andoffered
minimizationinEquation(10)willleadtoapreferencefor
| littleimprovement. |     | Instead,theoriginalDoubleQ-learning |      |        |           |                |             |              |     |       |            |         |     |       |
| ------------------ | --- | ----------------------------------- | ---- | ------ | --------- | -------------- | ----------- | ------------ | --- | ----- | ---------- | ------- | --- | ----- |
|                    |     |                                     |      |        |           |                | states with | low-variance |     | value | estimates, | leading | to  | safer |
| formulation        | can | be used,                            | with | a pair | of actors | (π φ1 , π φ2 ) |             |              |     |       |            |         |     |       |
policyupdateswithstablelearningtargets.
| andcritics(Q | ,Q  | ),whereπ       |     | isoptimizedwithrespect |     |     |     |     |     |     |     |     |     |     |
| ------------ | --- | -------------- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|              | θ1  | θ2             |     | φ1                     |     |     |     |     |     |     |     |     |     |     |
| toQ andπ     |     | withrespecttoQ |     | :                      |     |     |     |     |     |     |     |     |     |     |
| θ1           | φ2  |                |     | θ2                     |     |     |     |     |     |     |     |     |     |     |
5.AddressingVariance
|     | y   | =r+γQ |            | (s(cid:48),π | (s(cid:48))) |     |     |     |     |     |     |     |     |     |
| --- | --- | ----- | ---------- | ------------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | 1     | θ (cid:48) | φ1           |              |     |     |     |     |     |     |     |     |     |
|     |     |       | 2          |              |              | (9) |     |     |     |     |     |     |     |     |
(s(cid:48),π (s(cid:48))). WhileSection4dealswiththecontributionofvarianceto
|     | y   | 2 =r+γQ | θ (cid:48) | φ2  |     |     |                                                        |     |     |     |     |     |     |     |
| --- | --- | ------- | ---------- | --- | --- | --- | ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
|     |     |         | 1          |     |     |     | overestimationbias,wealsoarguethatvarianceitselfshould |     |     |     |     |     |     |     |
We measure the overestimation bias in Figure 2, which bedirectlyaddressed. Besidestheimpactonoverestimation

AddressingFunctionApproximationErrorinActor-CriticMethods
bias,highvarianceestimatesprovideanoisygradientforthe
| policyupdate. |     | Thisisknowntoreducelearningspeed(Sut- |     |     |     |     |     |     |     | 104 |     |     |
| ------------- | --- | ------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
350
eulaVegarevA
| ton&Barto,1998)aswellashurtperformanceinpractice. |     |     |     |     |     |     | 300 |     |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Inthissectionweemphasizetheimportanceofminimizing |     |     |     |     |     |     |     |     |     | 103 |     |     |
250
| error | ateach | update, | buildthe | connectionbetween |     | target |     |     |     |     |     |     |
| ----- | ------ | ------- | -------- | ----------------- | --- | ------ | --- | --- | --- | --- | --- | --- |
τ=1 τ=0.01
200
networksandestimationerrorandproposemodificationsto τ=0.1 TrueValue 102
1500.0
thelearningprocedureofactor-criticforvariancereduction. 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0
|     |     |     |     |     |     |     |                | Timesteps(1e5) |     |     | Timesteps(1e5)   |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | -------------- | --- | --- | ---------------- | --- |
|     |     |     |     |     |     |     | (a)FixedPolicy |                |     |     | (b)LearnedPolicy |     |
5.1.AccumulatingError
|     |     |     |     |     |     |     | Figure3.Average | estimated | value | of a | randomly selected | state |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --------- | ----- | ---- | ----------------- | ----- |
Duetothetemporaldifferenceupdate,whereanestimateof
|     |     |     |     |     |     |     | onHopper-v1withouttargetnetworks,(τ |     |     |     | = 1),andwithslow- |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- | ----------------- | --- |
thevaluefunctionisbuiltfromanestimateofasubsequent
|                               |     |     |     |                       |     |     | updating target | networks, | (τ = | 0.1,0.01), | with a fixed | and a |
| ----------------------------- | --- | --- | --- | --------------------- | --- | --- | --------------- | --------- | ---- | ---------- | ------------ | ----- |
| state,thereisabuildupoferror. |     |     |     | Whileitisreasonableto |     |     | learnedpolicy.  |           |      |            |              |       |
expectsmallerrorforanindividualupdate,theseestimation
| errorscanaccumulate,                          |     |     | resultinginthepotentialforlarge |     |     |        |     |     |     |     |     |     |
| --------------------------------------------- | --- | --- | ------------------------------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
| overestimationbiasandsuboptimalpolicyupdates. |     |     |                                 |     |     | Thisis |     |     |     |     |     |     |
exacerbatedinafunctionapproximationsettingwherethe procedure,andallowagreatercoverageofthetrainingdata.
Withoutafixedtarget,eachupdatemayleaveresidualerror
Bellmanequationisneverexactlysatisfied,andeachupdate
|     |     |     |     |     |     |     | whichwillbegintoaccumulate. |     |     | Whiletheaccumulationof |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------- | --- | --- | ---------------------- | --- | --- |
leavessomeamountofresidualTD-errorδ(s,a):
errorcanbedetrimentalinitself,whenpairedwithapolicy
Q (s,a)=r+γE[Q (s(cid:48),a(cid:48))] δ(s,a). maximizingoverthevalueestimate,itcanresultinwildly
|     |     | θ   |     | θ   |     | (11) |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
−
divergentvalues.
Itcanthenbeshownthatratherthanlearninganestimate
Toprovidesomeintuition,weexaminethelearningbehavior
oftheexpectedreturn,thevalueestimateapproximatesthe
withandwithouttargetnetworksonboththecriticandactor
expectedreturnminustheexpecteddiscountedsumoffuture
inFigure3,wherewegraphthevalue,inasimilarmannerto
TD-errors:
|     |             |       |       |                 |      |        | Figure1,intheHopper-v1environment.                    |     |     |     | In(a)wecompare |     |
| --- | ----------- | ----- | ----- | --------------- | ---- | ------ | ----------------------------------------------------- | --- | --- | --- | -------------- | --- |
|     |             |       | +γE[Q |                 |      |        | thebehaviorwithafixedpolicyandin(b)weexaminethe       |     |     |     |                |     |
|     | Q θ (s t ,a | t )=r | t     | θ (s t+1 ,a t+1 | )] δ | t      |                                                       |     |     |     |                |     |
|     |             |       |       |                 | −    |        | valueestimateswithapolicythatcontinuestolearn,trained |     |     |     |                |     |
|     | =r +γE[r    |       | +γE[Q | (s ,a           | )    | δ ]] δ |                                                       |     |     |     |                |     |
t t+1 θ t+2 t+2 t+1 t withthecurrentvalueestimate. Thetargetnetworksusea
− −
|     |            |     | (cid:34)        | (cid:35) |     |      |                                                    |     |     |     |     |     |
| --- | ---------- | --- | --------------- | -------- | --- | ---- | -------------------------------------------------- | --- | --- | --- | --- | --- |
|     |            |     | T               |          |     |      | slow-movingupdaterate,parametrizedbyτ.             |     |     |     |     |     |
|     | =E         |     | (cid:88) γi−t(r |          |     |      |                                                    |     |     |     |     |     |
|     | si∼pπ,ai∼π |     |                 | i δ i )  | .   | (12) |                                                    |     |     |     |     |     |
|     |            |     |                 | −        |     |      | Whileupdatingthevalueestimatewithouttargetnetworks |     |     |     |     |     |
i=t
(τ =1)increasesthevolatility,allupdateratesresultinsim-
Ifthevalueestimateisafunctionoffuturerewardandes- ilarconvergentbehaviorswhenconsideringafixedpolicy.
timationerror,itfollowsthatthevarianceoftheestimate
However,whenthepolicyistrainedwiththecurrentvalue
willbeproportionaltothevarianceoffuturerewardandes- estimate,theuseoffast-updatingtargetnetworksresultsin
timationerror. Givenalargediscountfactorγ,thevariance highlydivergentbehavior.
cangrowrapidlywitheachupdateiftheerrorfromeach
Whendoactor-criticmethodsfailtolearn?Theseresults
| updateisnottamed. |     |     | Furthermoreeachgradientupdateonly |     |     |     |     |     |     |     |     |     |
| ----------------- | --- | --- | --------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
suggestthatthedivergencethatoccurswithouttargetnet-
reduceserrorwithrespecttoasmallmini-batchwhichgives
worksistheresultofpolicyupdateswithahighvariance
| no  | guarantees |     | about the | size of errors | in value | estimates |     |     |     |     |     |     |
| --- | ---------- | --- | --------- | -------------- | -------- | --------- | --- | --- | --- | --- | --- | --- |
valueestimate.Figure3,aswellasSection4,suggestfailure
outsidethemini-batch.
canoccurduetotheinterplaybetweentheactorandcritic
|     |     |     |     |     |     |     | updates. Value | estimates | diverge | through | overestimation |     |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --------- | ------- | ------- | -------------- | --- |
5.2.TargetNetworksandDelayedPolicyUpdates
whenthepolicyispoor,andthepolicywillbecomepoorif
Inthissectionweexaminetherelationshipbetweentarget thevalueestimateitselfisinaccurate.
networksandfunctionapproximationerror,andshowthe
Iftargetnetworkscanbeusedtoreducetheerrorovermul-
| use | of a | stable | target reduces | the growth | of  | error. This |     |     |     |     |     |     |
| --- | ---- | ------ | -------------- | ---------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
tipleupdates,andpolicyupdatesonhigh-errorstatescause
| insight | allows |     | us to consider | the interplay | between | high |     |     |     |     |     |     |
| ------- | ------ | --- | -------------- | ------------- | ------- | ---- | --- | --- | --- | --- | --- | --- |
divergentbehavior,thenthepolicynetworkshouldbeup-
varianceestimatesandpolicyperformance,whendesigning
datedatalowerfrequencythanthevaluenetwork,tofirst
reinforcementlearningalgorithms.
|     |     |     |     |     |     |     | minimizeerrorbeforeintroducingapolicyupdate. |     |     |     | Wepro- |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | ------ | --- |
Target networks are a well-known tool to achieve stabil- posedelayingpolicyupdatesuntilthevalueerrorisassmall
ity in deep reinforcement learning. As deep function ap- aspossible. Themodificationistoonlyupdatethepolicy
proximatorsrequiremultiplegradientupdatestoconverge, andtargetnetworksafterafixednumberofupdatesdtothe
target networks provide a stable objective in the learning critic. ToensuretheTD-errorremainssmall,weupdatethe

AddressingFunctionApproximationErrorinActor-CriticMethods
targetnetworksslowlyθ(cid:48) τθ+(1 τ)θ(cid:48). Algorithm1TD3
← −
InitializecriticnetworksQ ,Q ,andactornetworkπ
Bysufficientlydelayingthepolicyupdateswelimitthelike- θ1 θ2 φ
withrandomparametersθ ,θ ,φ
lihoodofrepeatingupdateswithrespecttoanunchanged 1 2
Initializetargetnetworksθ(cid:48) θ ,θ(cid:48) θ ,φ(cid:48) φ
critic. Thelessfrequentpolicyupdatesthatdooccurwill 1 ← 1 2 ← 2 ←
Initializereplaybuffer
useavalueestimatewithlowervariance,andinprinciple,
B
fort=1toT do
shouldresultinhigherqualitypolicyupdates. Thiscreatesa
Selectactionwithexplorationnoisea π (s)+(cid:15),
two-timescalealgorithm,asoftenrequiredforconvergence φ
∼
(cid:15) (0,σ)andobserverewardrandnewstates(cid:48)
inthelinearsetting(Konda&Tsitsiklis,2003). Theeffec-
∼N
Storetransitiontuple(s,a,r,s(cid:48))in
tivenessofthisstrategyiscapturedbyourempiricalresults
B
presentedinSection6.1, whichshowanimprovementin
Samplemini-batchofN transitions(s,a,r,s(cid:48))from
performancewhileusingfewerpolicyupdates.
B
a˜ π (s(cid:48))+(cid:15), (cid:15) clip( (0,σ˜), c,c)
φ(cid:48)
← ∼ N −
y r+γmin Q (s(cid:48),a˜)
5.3.TargetPolicySmoothingRegularization i=1,2 θ(cid:48)
Up ← datecriticsθ argm i in N−1(cid:80) (y Q (s,a))2
A concern with deterministic policies is they can overfit iftmoddthen i ← θi − θi
tonarrowpeaksinthevalueestimate. Whenupdatingthe Updateφbythedeterministicpolicygradient:
critic,alearningtargetusingadeterministicpolicyishighly J(φ)=N−1(cid:80) Q (s,a) π (s)
susceptibletoinaccuraciesinducedbyfunctionapproxima- ∇ Up
φ
datetargetnetwor ∇ ks
a
:
θ1
|
a=πφ(s)
∇
φ φ
tionerror,increasingthevarianceofthetarget.Thisinduced θ(cid:48) τθ +(1 τ)θ(cid:48)
variancecanbereducedthroughregularization. Weintro- φ i (cid:48) ← τφ i +(1 − τ)φ(cid:48) i
ducearegularizationstrategyfordeepvaluelearning,target endif ← −
policysmoothing,whichmimicsthelearningupdatefrom endfor
SARSA (Sutton & Barto, 1998). Our approach enforces
the notion that similar actions should have similar value.
Whilethefunctionapproximationdoesthisimplicitly,the
relationshipbetweensimilaractionscanbeforcedexplicitly
bymodifyingthetrainingprocedure.Weproposethatfitting
thevalueofasmallareaaroundthetargetaction
y =r+E [Q (s(cid:48),π (s(cid:48))+(cid:15))], (13)
(cid:15) θ(cid:48) φ(cid:48)
(a) (b) (c) (d)
wouldhavethebenefitofsmoothingthevalueestimateby
bootstrappingoffofsimilarstate-actionvalueestimates. In Figure4.ExampleMuJoCoenvironments(a)HalfCheetah-v1,(b)
practice,wecanapproximatethisexpectationoveractions Hopper-v1,(c)Walker2d-v1,(d)Ant-v1.
by adding a small amount of random noise to the target
policy and averaging over mini-batches. This makes our
modifiedtargetupdate: 6.Experiments
y =r+γQ θ(cid:48) (s(cid:48),π φ(cid:48) (s(cid:48))+(cid:15)), We present the Twin Delayed Deep Deterministic policy
(14)
(cid:15) clip( (0,σ), c,c), gradientalgorithm(TD3),whichbuildsontheDeepDeter-
∼ N − ministicPolicyGradientalgorithm(DDPG)(Lillicrapetal.,
wheretheaddednoiseisclippedtokeepthetargetcloseto
2015)byapplyingthemodificationsdescribedinSections
theoriginalaction.Theoutcomeisanalgorithmreminiscent
4.2, 5.2and5.3toincreasethestabilityandperformance
ofExpectedSARSA(VanSeijenet al.,2009), wherethe
withconsiderationoffunctionapproximationerror. TD3
value estimate is instead learned off-policy and the noise
maintainsapairofcriticsalongwithasingleactor.Foreach
addedtothetargetpolicyischosenindependentlyoftheex-
timestep,weupdatethepairofcriticstowardstheminimum
plorationpolicy. Thevalueestimatelearnediswithrespect
targetvalueofactionsselectedbythetargetpolicy:
toanoisypolicydefinedbytheparameterσ.
Intuitively,itisknownthatpoliciesderivedfromSARSA y =r+γ minQ (s(cid:48),π (s(cid:48))+(cid:15)),
θ(cid:48) φ(cid:48)
valueestimatestendtobesafer,astheyprovidehighervalue i=1,2 i (15)
(cid:15) clip( (0,σ), c,c).
to actions resistant to perturbations. Thus, this style of
∼ N −
updatecanadditionallyleadtoimprovementinstochastic
domainswithfailurecases. Asimilarideawasintroduced Everyditerations,thepolicyisupdatedwithrespecttoQ
θ1
concurrentlybyNachumetal.(2018),smoothingoverQ , followingthedeterministicpolicygradientalgorithm(Silver
θ
ratherthanQ . etal.,2014). TD3issummarizedinAlgorithm1.
θ(cid:48)

AddressingFunctionApproximationErrorinActor-CriticMethods
|       |     |     | TD3 | DDPG |     | ourDDPG |     | PPO  | TRPO |     | ACKTR |     | SAC |     |     |
| ----- | --- | --- | --- | ---- | --- | ------- | --- | ---- | ---- | --- | ----- | --- | --- | --- | --- |
| 10000 |     |     |     |      |     |         |     | 5000 |      |     |       |     |     |     |     |
3500
4000
| nruteRegarevA 8000 |     |     |     | 3000 |     |     |     | 4000 |     |     |     |      |     |     |     |
| ------------------ | --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- |
|                    |     |     |     | 2500 |     |     |     |      |     |     |     | 3000 |     |     |     |
| 6000               |     |     |     |      |     |     |     | 3000 |     |     |     |      |     |     |     |
2000
| 4000 |     |     |     |      |     |     |     |      |     |     |     | 2000 |     |     |     |
| ---- | --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- |
|      |     |     |     | 1500 |     |     |     | 2000 |     |     |     |      |     |     |     |
|      |     |     |     | 1000 |     |     |     |      |     |     |     | 1000 |     |     |     |
| 2000 |     |     |     |      |     |     |     | 1000 |     |     |     |      |     |     |     |
|      |     |     |     | 500  |     |     |     |      |     |     |     | 0    |     |     |     |
0
|     |     |     |     | 0   |     |     |     | 0   |     |     |     | 1000 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0− 0.0 0.2 0.4 0.6 0.8 1.0
|     |                   | Timesteps(1e6) |     |     | Timesteps(1e6) |      |     |     | Timesteps(1e6) |       |     |     | Timesteps(1e6) |     |     |
| --- | ----------------- | -------------- | --- | --- | -------------- | ---- | --- | --- | -------------- | ----- | --- | --- | -------------- | --- | --- |
|     | (a)HalfCheetah-v1 |                |     |     | (b)Hopper-v1   |      |     |     | (c)Walker2d-v1 |       |     |     | (d)Ant-v1      |     |     |
|     |                   |                |     |     |                | 1000 |     |     |                | 10000 |     |     |                |     |     |
− 4
|     |     |     |     |     |     | 900 |     |     |     | 8000 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
nruteRegarevA
|     |     | −   | 6   |     |     | 800 |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
6000
700
|     |     | −   | 8   |     |     |     |     |     |     | 4000 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
600
|     |     | 10  |     |     |     | 500 |     |     |     | 2000 |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
−
|     |     |     |     |     |     | 400 |     |     |     | 0   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
12
− 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0
|     |     |     |               | Timesteps(1e6) |     |                        | Timesteps(1e6) |     |     |                              | Timesteps(1e6) |     |     |     |     |
| --- | --- | --- | ------------- | -------------- | --- | ---------------------- | -------------- | --- | --- | ---------------------------- | -------------- | --- | --- | --- | --- |
|     |     |     | (e)Reacher-v1 |                |     | (f)InvertedPendulum-v1 |                |     |     | (g)InvertedDoublePendulum-v1 |                |     |     |     |     |
Figure5.LearningcurvesfortheOpenAIgymcontinuouscontroltasks.Theshadedregionrepresentshalfastandarddeviationofthe
averageevaluationover10trials.Curvesaresmootheduniformlyforvisualclarity.
Table1.MaxAverageReturnover10trialsof1milliontimesteps.Maximumvalueforeachtaskisbolded.±correspondstoasingle
standarddeviationovertrials.
|     | Environment |     |     | TD3 |     | DDPG |     | OurDDPG |     | PPO | TRPO | ACKTR |     | SAC |     |
| --- | ----------- | --- | --- | --- | --- | ---- | --- | ------- | --- | --- | ---- | ----- | --- | --- | --- |
HalfCheetah 9636.95±859.065 3305.60 8577.29 1795.43 -15.57 1450.46 2347.19
Hopper 3564.07±114.74 2020.46 1860.02 2164.70 2471.30 2428.39 2996.66
Walker2d 4682.82±539.64 1843.85 3098.11 3317.69 2321.47 1216.70 1283.67
Ant 4372.44±1000.33 1005.30 888.77 1083.20 -75.85 1821.94 655.35
|     | Reacher |     |     | -3.60±0.56 |     | -6.51 |     | -4.01 |     | -6.18 | -111.43 | -4.26 |     | -4.44 |     |
| --- | ------- | --- | --- | ---------- | --- | ----- | --- | ----- | --- | ----- | ------- | ----- | --- | ----- | --- |
InvPendulum 1000.00±0.00 1000.00 1000.00 1000.00 985.40 1000.00 1000.00
InvDoublePendulum 9337.47±14.96 9355.52 8369.95 8977.94 205.85 9081.92 8487.15
6.1.Evaluation (0,0.2)totheactionschosenbythetargetactornetwork,
N
|                                                  |     |     |     |     |     |     |     | clippedto(    |     | 0.5,0.5),delayedpolicyupdatesconsistsof |     |        |                |       |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --------------------------------------- | --- | ------ | -------------- | ----- | --- |
| Toevaluateouralgorithm,wemeasureitsperformanceon |     |     |     |     |     |     |     |               | −   |                                         |     |        |                |       |     |
|                                                  |     |     |     |     |     |     |     | only updating |     | the actor                               | and | target | critic network | every | d   |
thesuiteofMuJoCocontinuouscontroltasks(Todorovetal.,
|     |     |     |     |     |     |     |     | iterations,withd |     | =   | 2. Whilealargerdwouldresultina |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | ------------------------------ | --- | --- | --- | --- |
2012),interfacedthroughOpenAIGym(Brockmanetal.,
largerbenefitwithrespecttoaccumulatingerrors,forfair
| 2016)(Figure4). |     | Toallowforreproduciblecomparison,we |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --------------- | --- | ----------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
comparison,thecriticsareonlytrainedoncepertimestep,
| use | the original | set | of tasks | from Brockman |     | et al. (2016) |     |     |     |     |     |     |     |     |     |
| --- | ------------ | --- | -------- | ------------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
andtrainingtheactorfortoofewiterationswouldcripple
withnomodificationstotheenvironmentorreward.
|     |     |     |     |     |     |     |     | learning. | Bothtargetnetworksareupdatedwithτ |     |     |     |     | =0.005. |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --------------------------------- | --- | --- | --- | --- | ------- | --- |
ForourimplementationofDDPG(Lillicrapetal.,2015),we
Toremovethedependencyontheinitialparametersofthe
useatwolayerfeedforwardneuralnetworkof400and300
policyweuseapurelyexploratorypolicyforthefirst10000
hiddennodesrespectively,withrectifiedlinearunits(ReLU)
timestepsofstablelengthenvironments(HalfCheetah-v1
betweeneachlayerforboththeactorandcritic,andafinal
andAnt-v1)andthefirst1000timestepsfortheremaining
| tanhunitfollowingtheoutputoftheactor. |     |     |     |     | Unliketheorig- |     |     |               |     |                                         |     |     |     |     |     |
| ------------------------------------- | --- | --- | --- | --- | -------------- | --- | --- | ------------- | --- | --------------------------------------- | --- | --- | --- | --- | --- |
|                                       |     |     |     |     |                |     |     | environments. |     | Afterwards,weuseanoff-policyexploration |     |     |     |     |     |
inalDDPG,thecriticreceivesboththestateandactionas
|                       |     |     |                                 |     |     |     |     | strategy, | adding | Gaussian |     | noise | (0,0.1) | to each action. |     |
| --------------------- | --- | --- | ------------------------------- | --- | --- | --- | --- | --------- | ------ | -------- | --- | ----- | ------- | --------------- | --- |
| inputtothefirstlayer. |     |     | Bothnetworkparametersareupdated |     |     |     |     |           |        |          |     | N     |         |                 |     |
UnliketheoriginalimplementationofDDPG,weusedun-
usingAdam(Kingma&Ba,2014)withalearningrateof
correlatednoiseforexplorationaswefoundnoisedrawn
10−3. Aftereachtimestep,thenetworksaretrainedwitha
fromtheOrnstein-Uhlenbeck(Uhlenbeck&Ornstein,1930)
mini-batchofa100transitions,sampleduniformlyfroma
processofferednoperformancebenefits.
replaybuffercontainingtheentirehistoryoftheagent.
Eachtaskisrunfor1milliontimestepswithevaluations
Thetargetpolicysmoothingisimplementedbyadding(cid:15)
|     |     |     |     |     |     |     |     | every | 5000 | time steps, | where | each | evaluation | reports | the |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ---- | ----------- | ----- | ---- | ---------- | ------- | --- |
∼

AddressingFunctionApproximationErrorinActor-CriticMethods
averagerewardover10episodeswithnoexplorationnoise.
Table2.Averagereturnoverthelast10evaluationsover10trials
Ourresultsarereportedover10randomseedsoftheGym
of1milliontimesteps,comparingablationoverdelayedpolicy
simulatorandthenetworkinitialization.
|     |     |     |     |     |     |     | updates | (DP), target | policy | smoothing | (TPS), | Clipped |     | Double |
| --- | --- | --- | --- | --- | --- | --- | ------- | ------------ | ------ | --------- | ------ | ------- | --- | ------ |
WecompareouralgorithmagainstDDPG(Lillicrapetal., Q-learning (CDQ) and our architecture, hyper-parameters and
exploration(AHE).Maximumvalueforeachtaskisbolded.
2015)aswellasthestateofartpolicygradientalgorithms:
| PPO (Schulman | et        | al., 2017), | ACKTR       |     | (Wu et al., | 2017) |        |     |          |        |     |          |     |     |
| ------------- | --------- | ----------- | ----------- | --- | ----------- | ----- | ------ | --- | -------- | ------ | --- | -------- | --- | --- |
| and TRPO      | (Schulman | et          | al., 2015), | as  | implemented | by    |        |     |          |        |     |          |     |     |
|               |           |             |             |     |             |       | Method |     | HCheetah | Hopper |     | Walker2d |     | Ant |
OpenAI’sbaselinesrepository(Dhariwaletal.,2017),and
|     |     |     |     |     |     |     | TD3 |     | 9532.99 | 3304.75 |     | 4565.24 |     | 4185.06 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------- | --- | ------- | --- | ------- |
SAC(Haarnojaetal.,2018),asimplementedbytheauthor’s
|     |     |     |     |     |     |     | DDPG |     | 3162.50 | 1731.94 |     | 1520.90 |     | 816.35 |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | ------- | ------- | --- | ------- | --- | ------ |
GitHub1.
Additionally,wecompareourmethodwithour AHE 8401.02 1061.77 2362.13 564.07
re-tunedversionofDDPG,whichincludesallarchitecture
|     |     |     |     |     |     |     | AHE+DP |     | 7588.64 | 1465.11 |     | 2459.53 |     | 896.13 |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | ------- | ------- | --- | ------- | --- | ------ |
andhyper-parametermodificationstoDDPGwithoutany
|     |     |     |     |     |     |     | AHE+TPS |     | 9023.40 | 907.56 |     | 2961.36 |     | 872.17 |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | ------ | --- | ------- | --- | ------ |
ofourproposedadjustments. Afullcomparisonbetween AHE+CDQ 6470.20 1134.14 3979.21 3818.71
ourre-tunedversionandthebaselinesDDPGisprovidedin
|     |     |     |     |     |     |     | TD3-DP |     | 9590.65 | 2407.42 |     | 4695.50 |     | 3754.26 |
| --- | --- | --- | --- | --- | --- | --- | ------ | --- | ------- | ------- | --- | ------- | --- | ------- |
thesupplementarymaterial. TD3-TPS 8987.69 2392.59 4033.67 4155.24
|     |     |     |     |     |     |     | TD3-CDQ |     | 9792.80 | 1837.32 |     | 2579.39 |     | 849.75 |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | ------- | --- | ------- | --- | ------ |
OurresultsarepresentedinTable1andlearningcurvesin
Figure5. TD3matchesoroutperformsallotheralgorithms DQ-AC 9433.87 1773.71 3100.45 2445.97
|     |     |     |     |     |     |     | DDQN-AC |     | 10306.90 | 2155.75 |     | 3116.81 |     | 1092.18 |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | -------- | ------- | --- | ------- | --- | ------- |
inbothfinalperformanceandlearningspeedacrossalltasks.
6.2.AblationStudies
outperformsbothpriormethods,thissuggeststhatsubdu-
ingtheoverestimationsfromtheunbiasedestimatorisan
Weperformablationstudiestounderstandthecontribution
effectivemeasuretoimproveperformance.
| ofeachindividualcomponent: |     |     | ClippedDoubleQ-learning |     |     |     |     |     |     |     |     |     |     |     |
| -------------------------- | --- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(Section4.2),delayedpolicyupdates(Section5.2)andtarget
| policysmoothing(Section5.3). |     |     |     | Wepresentourresultsin |     |     | 7.Conclusion |     |     |     |     |     |     |     |
| ---------------------------- | --- | --- | --- | --------------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
Table2inwhichwecomparetheperformanceofremoving
|     |     |     |     |     |     |     | Overestimation |     | has been | identified | as  | a key | problem | in  |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | -------- | ---------- | --- | ----- | ------- | --- |
eachcomponentfromTD3alongwithourmodificationsto
|                                     |     |     |     |     |                    |     | value-basedmethods. |     |     | Inthispaper,weestablishoveresti- |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | ------------------ | --- | ------------------- | --- | --- | -------------------------------- | --- | --- | --- | --- |
| thearchitectureandhyper-parameters. |     |     |     |     | Additionallearning |     |                     |     |     |                                  |     |     |     |     |
curvescanbefoundinthesupplementarymaterial. mationbiasisalsoproblematicinactor-criticmethods. We
findthecommonsolutionsforreducingoverestimationbias
The significance of each component varies task to task. indeepQ-learningwithdiscreteactionsareineffectiveinan
| While the | addition | of only | a single | component | causes | in- |     |     |     |     |     |     |     |     |
| --------- | -------- | ------- | -------- | --------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
actor-criticsetting,anddevelopanovelvariantofDouble
significantimprovementinmostcases,theadditionofcom- Q-learning which limits possible overestimation. Our re-
| binationsperformsat |     | amuchhigherlevel. |     |     | Thefullalgo- |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | ----------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sultsdemonstratethatmitigatingoverestimationcangreatly
rithmoutperformseveryothercombinationinmosttasks. improvetheperformanceofmodernalgorithms.
| Although | the actor | is trained | for | only | half the number | of  |     |     |     |     |     |     |     |     |
| -------- | --------- | ---------- | --- | ---- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
iterations,theinclusionofdelayedpolicyupdategenerally Duetotheconnectionbetweennoiseandoverestimation,
weexaminetheaccumulationoferrorsfromtemporaldif-
improvesperformance,whilereducingtrainingtime.
|     |     |     |     |     |     |     | ferencelearning. |     | Ourworkinvestigatestheimportanceof |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | ---------------------------------- | --- | --- | --- | --- | --- |
Weadditionallycomparetheeffectivenessoftheactor-critic
astandardtechniqueindeepreinforcementlearning,target
variantsofDoubleQ-learning(VanHasselt,2010)andDou- networks, andexaminestheirroleinlimitingerrorsfrom
bleDQN(VanHasseltetal.,2016),denotedDQ-ACand
imprecisefunctionapproximationandstochasticoptimiza-
| DDQN-AC | respectively, |     | in Table | 2. For | fairness in | com- |                                                     |     |     |     |     |     |     |     |
| ------- | ------------- | --- | -------- | ------ | ----------- | ---- | --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|         |               |     |          |        |             |      | tion. Finally,weintroduceaSARSA-styleregularization |     |     |     |     |     |     |     |
parison,thesemethodsalsobenefitedfromdelayedpolicy techniquewhichmodifiesthetemporaldifferencetargetto
updates,targetpolicysmoothinganduseourarchitecture
bootstrapoffsimilarstate-actionpairs.
| andhyper-parameters. |     | Bothmethodswereshowntoreduce |     |     |     |     |                 |     |       |              |        |     |          |     |
| -------------------- | --- | ---------------------------- | --- | --- | --- | --- | --------------- | --- | ----- | ------------ | ------ | --- | -------- | --- |
|                      |     |                              |     |     |     |     | Taken together, |     | these | improvements | define | our | proposed |     |
overestimationbiaslessthanClippedDoubleQ-learningin
Section 4. This is reflected empirically, as both methods approach,theTwinDelayedDeepDeterministicpolicygra-
|     |     |     |     |     |     |     | dient algorithm |     | (TD3), | which greatly |     | improves | both | the |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------ | ------------- | --- | -------- | ---- | --- |
resultininsignificantimprovementsoverTD3-CDQ,with
learningspeedandperformanceofDDPGinanumberof
anexceptionintheAnt-v1environment,whichappearsto
|                                               |     |     |     |     |     |       | challenging | tasks   | in  | the continuous | control |          | setting. | Our |
| --------------------------------------------- | --- | --- | --- | --- | --- | ----- | ----------- | ------- | --- | -------------- | ------- | -------- | -------- | --- |
| benefitgreatlyfromanyoverestimationreduction. |     |     |     |     |     | Asthe |             |         |     |                |         |          |          |     |
|                                               |     |     |     |     |     |       | algorithm   | exceeds | the | performance    | of      | numerous | state    | of  |
inclusionofClippedDoubleQ-learningintoourfullmethod
|     |     |     |     |     |     |     | theartalgorithms. |     | Asourmodificationsaresimpletoim- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | -------------------------------- | --- | --- | --- | --- | --- |
1Seethesupplementarymaterialforhyper-parametersanda plement,theycanbeeasilyaddedtoanyotheractor-critic
| discussiononthediscrepancyinthereportedresultsofSAC. |     |     |     |     |     |     | algorithm. |     |     |     |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |

AddressingFunctionApproximationErrorinActor-CriticMethods
References Kingma, D. and Ba, J. Adam: A method for stochastic
|          |            |     |             |     |                  | optimization. | arXivpreprintarXiv:1412.6980,2014. |     |     |
| -------- | ---------- | --- | ----------- | --- | ---------------- | ------------- | ---------------------------------- | --- | --- |
| Anschel, | O., Baram, | N., | andShimkin, |     | N. Averaged-dqn: |               |                                    |     |     |
Variancereductionandstabilizationfordeepreinforce- Konda,V.R.andTsitsiklis,J.N. Onactor-criticalgorithms.
mentlearning. InInternationalConferenceonMachine SIAMjournalonControlandOptimization,42(4):1143–
| Learning,pp.176–185,2017. |     |          |     |             |             | 1166,2003.         |                |      |                |
| ------------------------- | --- | -------- | --- | ----------- | ----------- | ------------------ | -------------- | ---- | -------------- |
| Barth-Maron,              | G., | Hoffman, | M.  | W., Budden, | D., Dabney, |                    |                |      |                |
|                           |     |          |     |             |             | Lee, D., Defourny, | B., andPowell, | W.B. | Bias-corrected |
W.,Horgan,D.,TB,D.,Muldal,A.,Heess,N.,andLil- q-learning to control max-operator bias in q-learning.
licrap,T. Distributionalpolicygradients. International InAdaptiveDynamicProgrammingAndReinforcement
ConferenceonLearningRepresentations,2018.
Learning(ADPRL),2013IEEESymposiumon,pp.93–99.
IEEE,2013.
| Bellemare,M.G.,Dabney,W.,andMunos,R. |     |     |     |     | Adistribu- |     |     |     |     |
| ------------------------------------ | --- | --- | --- | --- | ---------- | --- | --- | --- | --- |
tionalperspectiveonreinforcementlearning. InInterna- Lillicrap, T. P., Hunt, J. J., Pritzel, A., Heess, N., Erez,
| tional | Conference | on  | Machine | Learning, | pp. 449–458, |            |                 |               |               |
| ------ | ---------- | --- | ------- | --------- | ------------ | ---------- | --------------- | ------------- | ------------- |
|        |            |     |         |           |              | T., Tassa, | Y., Silver, D., | and Wierstra, | D. Continuous |
2017.
|     |     |     |     |     |     | controlwithdeepreinforcementlearning. |     |     | arXivpreprint |
| --- | --- | --- | --- | --- | --- | ------------------------------------- | --- | --- | ------------- |
arXiv:1509.02971,2015.
| Bellman,R. | DynamicProgramming. |     |     | PrincetonUniversity |     |     |     |     |     |
| ---------- | ------------------- | --- | --- | ------------------- | --- | --- | --- | --- | --- |
Press,1957. Lin,L.-J.Self-improvingreactiveagentsbasedonreinforce-
Bertsekas,D.P.Dynamicprogrammingandoptimalcontrol, mentlearning,planningandteaching. Machinelearning,
8(3-4):293–321,1992.
| volume1.  | AthenascientificBelmont,MA,1995. |           |                 |     |                    |                                                 |     |                           |      |
| --------- | -------------------------------- | --------- | --------------- | --- | ------------------ | ----------------------------------------------- | --- | ------------------------- | ---- |
|           |                                  |           |                 |     |                    | Mannor,S.andTsitsiklis,J.N.                     |     | Mean-varianceoptimization |      |
| Brockman, | G., Cheung,                      |           | V., Pettersson, |     | L., Schneider, J., |                                                 |     |                           |      |
|           |                                  |           |                 |     |                    | inmarkovdecisionprocesses.                      |     | InInternationalConfer-    |      |
| Schulman, | J.,                              | Tang, J., | andZaremba,     |     | W. Openaigym,      |                                                 |     |                           |      |
| 2016.     |                                  |           |                 |     |                    | enceonMachineLearning,pp.177–184,2011.          |     |                           |      |
|           |                                  |           |                 |     |                    | Mannor,S.,Simester,D.,Sun,P.,andTsitsiklis,J.N. |     |                           | Bias |
Dhariwal,P.,Hesse,C.,Plappert,M.,Radford,A.,Schul-
man,J.,Sidor,S.,andWu,Y. Openaibaselines. https: andvarianceapproximationinvaluefunctionestimates.
ManagementScience,53(2):308–322,2007.
//github.com/openai/baselines,2017.
Mnih,V.,Kavukcuoglu,K.,Silver,D.,Rusu,A.A.,Veness,
| Espeholt, | L., Soyer, | H., | Munos, | R., Simonyan, | K., Mnih, |     |     |     |     |
| --------- | ---------- | --- | ------ | ------------- | --------- | --- | --- | --- | --- |
V.,Ward,T.,Doron,Y.,Firoiu,V.,Harley,T.,Dunning, J.,Bellemare,M.G.,Graves,A.,Riedmiller,M.,Fidje-
I.,etal. Impala: Scalabledistributeddeep-rlwithimpor- land, A. K., Ostrovski, G., et al. Human-level control
|                                          |     |     |     |     |               | throughdeepreinforcementlearning. |     | Nature,518(7540): |     |
| ---------------------------------------- | --- | --- | --- | --- | ------------- | --------------------------------- | --- | ----------------- | --- |
| tanceweightedactor-learnerarchitectures. |     |     |     |     | arXivpreprint |                                   |     |                   |     |
| arXiv:1802.01561,2018.                   |     |     |     |     |               | 529–533,2015.                     |     |                   |     |
Fox,R.,Pakman,A.,andTishby,N. Tamingthenoisein Mnih, V., Badia, A. P., Mirza, M., Graves, A., Lillicrap,
reinforcementlearningviasoftupdates.InProceedingsof T., Harley, T., Silver, D., and Kavukcuoglu, K. Asyn-
|     |     |     |     |     |     | chronousmethodsfordeepreinforcementlearning. |     |     | In  |
| --- | --- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- |
theThirty-SecondConferenceonUncertaintyinArtificial
Intelligence,pp.202–211.AUAIPress,2016. InternationalConferenceonMachineLearning,pp.1928–
1937,2016.
| Haarnoja, | T., Zhou, | A., | Abbeel, | P., and | Levine, S. Soft |     |     |     |     |
| --------- | --------- | --- | ------- | ------- | --------------- | --- | --- | --- | --- |
actor-critic: Off-policymaximumentropydeepreinforce- Munos,R.,Stepleton,T.,Harutyunyan,A.,andBellemare,
M. Safeandefficientoff-policyreinforcementlearning.
| ment | learning | with a | stochastic | actor. | arXiv preprint |     |     |     |     |
| ---- | -------- | ------ | ---------- | ------ | -------------- | --- | --- | --- | --- |
arXiv:1801.01290,2018. InAdvancesinNeuralInformationProcessingSystems,
pp.1054–1062,2016.
| He,F.S.,Liu,Y.,Schwing,A.G.,andPeng,J. |     |     |     |     | Learning |     |     |     |     |
| -------------------------------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- |
toplayinaday: Fasterdeepreinforcementlearningby Nachum,O.,Norouzi,M.,Tucker,G.,andSchuurmans,D.
|                       |     |     |                                |     |     | Smoothed  | action value functions              | for learning | gaussian |
| --------------------- | --- | --- | ------------------------------ | --- | --- | --------- | ----------------------------------- | ------------ | -------- |
| optimalitytightening. |     |     | arXivpreprintarXiv:1611.01606, |     |     |           |                                     |              |          |
| 2016.                 |     |     |                                |     |     | policies. | arXivpreprintarXiv:1803.02348,2018. |              |          |
Henderson,P.,Islam,R.,Bachman,P.,Pineau,J.,Precup, O’Donoghue,B.,Osband,I.,Munos,R.,andMnih,V. The
D., and Meger, D. Deep Reinforcement Learning that uncertainty bellman equation and exploration. arXiv
arXivpreprintarXiv:1709.06560,2017. preprintarXiv:1709.05380,2017.
Matters.
Horgan,D.,Quan,J.,Budden,D.,Barth-Maron,G.,Hessel, Pendrith,M.D.,Ryan,M.R.,etal. Estimatorvariancein
M.,vanHasselt,H.,andSilver,D. Distributedprioritized reinforcementlearning: Theoreticalproblemsandpracti-
experiencereplay. InternationalConferenceonLearning calsolutions. UniversityofNewSouthWales,Schoolof
| Representations,2018. |     |     |     |     |     | ComputerScienceandEngineering,1997. |     |     |     |
| --------------------- | --- | --- | --- | --- | --- | ----------------------------------- | --- | --- | --- |

AddressingFunctionApproximationErrorinActor-CriticMethods
Petrik,M.andScherrer,B. Biasingapproximatedynamic VanHasselt,H.,Guez,A.,andSilver,D. Deepreinforce-
programmingwithalowerdiscountfactor.InAdvancesin mentlearningwithdoubleq-learning. InAAAI,pp.2094–
| NeuralInformationProcessingSystems,pp.1265–1272, |     |     |     |     |     |     |     | 2100,2016. |     |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- |
2009.
VanSeijen,H.,VanHasselt,H.,Whiteson,S.,andWiering,
Popov, I., Heess, N., Lillicrap, T., Hafner, R., Barth- M. Atheoreticalandempiricalanalysisofexpectedsarsa.
Maron, G., Vecerik, M., Lampe, T., Tassa, Y., Erez, InAdaptiveDynamicProgrammingandReinforcement
T., and Riedmiller, M. Data-efficient deep reinforce- Learning, 2009. ADPRL’09. IEEE Symposium on, pp.
mentlearningfordexterousmanipulation. arXivpreprint 177–184.IEEE,2009.
arXiv:1704.03073,2017.
|         |             |     |         |           |     |               |     | Watkins,C.J.C.H. | Learningfromdelayedrewards. | PhD |
| ------- | ----------- | --- | ------- | --------- | --- | ------------- | --- | ---------------- | --------------------------- | --- |
| Precup, | D., Sutton, | R.  | S., and | Dasgupta, |     | S. Off-policy |     |                  |                             |     |
thesis,King’sCollege,Cambridge,1989.
| temporal-difference |     |     | learning | with | function | approxima- |     |     |     |     |
| ------------------- | --- | --- | -------- | ---- | -------- | ---------- | --- | --- | --- | --- |
tion. InInternationalConferenceonMachineLearning, Wu, Y., Mansimov, E., Grosse, R. B., Liao, S., and Ba,
|     |     |     |     |     |     |     |     | J. Scalabletrust-regionmethodfordeepreinforcement |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------- | --- | --- |
pp.417–424,2001.
|     |     |     |     |     |     |     |     | learningusingkronecker-factoredapproximation. |     | InAd- |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------------------- | --- | ----- |
Schaul,T.,Quan,J.,Antonoglou,I.,andSilver,D. Priori- vances in Neural Information Processing Systems, pp.
| tizedexperiencereplay. |     |     | InInternationalConferenceon |     |     |     |     | 5285–5294,2017. |     |     |
| ---------------------- | --- | --- | --------------------------- | --- | --- | --- | --- | --------------- | --- | --- |
LearningRepresentations,PuertoRico,2016.
Schulman,J.,Levine,S.,Abbeel,P.,Jordan,M.,andMoritz,
| P. Trust | region | policy | optimization. |     | In  | International |     |     |     |     |
| -------- | ------ | ------ | ------------- | --- | --- | ------------- | --- | --- | --- | --- |
ConferenceonMachineLearning,pp.1889–1897,2015.
| Schulman, | J., | Wolski,  | F., Dhariwal, |              | P., Radford, |             | A., and |     |     |     |
| --------- | --- | -------- | ------------- | ------------ | ------------ | ----------- | ------- | --- | --- | --- |
| Klimov,   | O.  | Proximal | policy        | optimization |              | algorithms. |         |     |     |     |
arXivpreprintarXiv:1707.06347,2017.
Silver,D.,Lever,G.,Heess,N.,Degris,T.,Wierstra,D.,and
| Riedmiller,M.    |     | Deterministicpolicygradientalgorithms. |     |            |     |           |     |     |     |     |
| ---------------- | --- | -------------------------------------- | --- | ---------- | --- | --------- | --- | --- | --- | --- |
| In International |     | Conference                             |     | on Machine |     | Learning, | pp. |     |     |     |
387–395,2014.
| Singh, S.,             | Jaakkola,   | T., | Littman,    | M.              | L., and | Szepesva´ri, |     |     |     |     |
| ---------------------- | ----------- | --- | ----------- | --------------- | ------- | ------------ | --- | --- | --- | --- |
| C.                     | Convergence |     | results     | for single-step |         | on-policy    |     |     |     |     |
| reinforcement-learning |             |     | algorithms. |                 | Machine | learning,    |     |     |     |     |
38(3):287–308,2000.
Sutton,R.S.Learningtopredictbythemethodsoftemporal
| differences.                     |     | Machinelearning,3(1):9–44,1988. |                              |                        |                    |     |     |     |     |     |
| -------------------------------- | --- | ------------------------------- | ---------------------------- | ---------------------- | ------------------ | --- | --- | --- | --- | --- |
| Sutton,R.S.andBarto,A.G.         |     |                                 |                              | Reinforcementlearning: |                    |     | An  |     |     |     |
| introduction,volume1.            |     |                                 | MITpressCambridge,1998.      |                        |                    |     |     |     |     |     |
| Thrun,S.andSchwartz,A.           |     |                                 | Issuesinusingfunctionapprox- |                        |                    |     |     |     |     |     |
| imationforreinforcementlearning. |     |                                 |                              |                        | InProceedingsofthe |     |     |     |     |     |
1993ConnectionistModelsSummerSchoolHillsdale,NJ.
LawrenceErlbaum,1993.
| Todorov, | E., Erez,       | T., | and Tassa, | Y.  | Mujoco:        | A   | physics |     |     |     |
| -------- | --------------- | --- | ---------- | --- | -------------- | --- | ------- | --- | --- | --- |
| engine   | for model-based |     | control.   |     | In Intelligent |     | Robots  |     |     |     |
andSystems(IROS),2012IEEE/RSJInternationalCon-
ferenceon,pp.5026–5033.IEEE,2012.
| Uhlenbeck,G.E.andOrnstein,L.S. |     |                                |     |                    | Onthetheoryofthe |     |     |     |     |     |
| ------------------------------ | --- | ------------------------------ | --- | ------------------ | ---------------- | --- | --- | --- | --- | --- |
| brownianmotion.                |     | Physicalreview,36(5):823,1930. |     |                    |                  |     |     |     |     |     |
| VanHasselt,H.                  |     | Doubleq-learning.              |     | InAdvancesinNeural |                  |     |     |     |     |     |
InformationProcessingSystems,pp.2613–2621,2010.

|     |     |     |     |     |     | Supplementary |     |     | Material |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------- | --- | --- | -------- | --- | --- | --- | --- |
A.ProofofConvergenceofClippedDoubleQ-Learning
InaversionofClippedDoubleQ-learningforafiniteMDPsetting,wemaintaintwotabularvalueestimatesQA,QB.
At
eachtimestepweselectactionsa∗ =argmax QA(s,a)andthenperformanupdatebysettingtargety:
a
a∗ =argmaxQA(s(cid:48),a)
|     |     |     |     |     |     |     | a   |     |     |     |     |     | (16) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
=r+γmin(QA(s(cid:48),a∗),QB(s(cid:48),a∗)),
y
| andupdatethevalueestimateswithrespecttothetargetandlearningrateα |     |     |     |     |     |     |     |     |     | (s,a): |     |     |     |
| ---------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
t
|     |     |     |     |     | QA(s,a)=QA(s,a)+α |     |     |     | (s,a)(y | QA(s,a)) |     |     |     |
| --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | ------- | -------- | --- | --- | --- |
t
|     |     |     |     |     |                   |     |     |     | −       |           |     |     | (17) |
| --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | ------- | --------- | --- | --- | ---- |
|     |     |     |     |     | QB(s,a)=QB(s,a)+α |     |     |     | (s,a)(y | QB(s,a)). |     |     |      |
t
−
InafiniteMDPsetting,DoubleQ-learningisoftenusedtodealwithnoiseinducedbyrandomrewardsorstatetransitions,
andsoeitherQA orQB isupdatedrandomly. However, inafunctionapproximationsetting, theinterestmaybemore
towardstheapproximationerrorandthuswecanupdatebothQAandQB ateachiteration. Theproofextendsnaturallyto
updatingeitherrandomly.
TheproofborrowsheavilyfromtheproofofconvergenceofSARSA(Singhetal.,2000)aswellasDoubleQ-learning
(VanHasselt,2010). Theproofoflemma1canbefoundinSinghetal.(2000),buildingonapropositionfromBertsekas
(1995).
Rsatisfytheequation:
| Lemma1. |     | Considerastochasticprocess(ζ |     |     |     | t ,∆    | t ,F t ),t | 0whereζ  | t ,∆ t ,F | t :X  |     |     |      |
| ------- | --- | ---------------------------- | --- | --- | --- | ------- | ---------- | -------- | --------- | ----- | --- | --- | ---- |
|         |     |                              |     |     |     |         |            | ≥        |           | →     |     |     |      |
|         |     |                              |     |     | ∆   | (x )=(1 |            | ζ (x ))∆ | (x )+ζ (x | )F (x | ),  |     | (18) |
|         |     |                              |     |     | t+1 | t       | −          | t t      | t t t     | t t t |     |     |      |
wherex X andt=0,1,2,.... LetP beasequenceofincreasingσ-fieldssuchthatζ and∆ areP -measurableand
|      | t       |           |                        |     |          | t   |                             |     |     |     | 0 0 | 0   |     |
| ---- | ------- | --------- | ---------------------- | --- | -------- | --- | --------------------------- | --- | --- | --- | --- | --- | --- |
| ζ ,∆ | andF ∈  | areP      | -measurable,t=1,2,.... |     |          |     | Assumethatthefollowinghold: |     |     |     |     |     |     |
| t    | t       | t−1       | t                      |     |          |     |                             |     |     |     |     |     |     |
| 1.   | ThesetX | isfinite. |                        |     |          |     |                             |     |     |     |     |     |     |
|      |         |           | (cid:80)               |     | (cid:80) |     |                             |     |     |     |     |     |     |
2. ζ (x ) [0,1], ζ (x )= , (ζ (x ))2 < withprobability1and x=x :ζ(x)=0.
|     | t t | ∈   | t   | t t | ∞   | t t | t   | ∞   |     | ∀ (cid:54) | t   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- |
E[F
| 3.  |       | P ]       | κ       | ∆ +c | whereκ      | [0,1)andc |                | convergesto0withprobability1. |     |     |     |     |     |
| --- | ----- | --------- | ------- | ---- | ----------- | --------- | -------------- | ----------------------------- | --- | --- | --- | --- | --- |
|     | ||    | t | t ||≤ | ||      | t || | t           | ∈         |                | t                             |     |     |     |     |     |
| 4.  | Var[F | (x )P     | ] K(1+κ |      | ∆ )2,whereK |           | issomeconstant |                               |     |     |     |     |     |
|     |       | t t |     | t ≤     |      | || t ||     |           |                |                               |     |     |     |     |     |
Where denotesthemaximumnorm. Then∆ convergesto0withprobability1.
t
||·||
| Theorem1. |     | Giventhefollowingconditions: |     |     |     |     |     |     |     |     |     |     |     |
| --------- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1. Eachstateactionpairissampledaninfinitenumberoftimes.
2. TheMDPisfinite.
3. γ [0,1).
∈
4. Qvaluesarestoredinalookuptable.
| 5.  | BothQAandQB |     | receiveaninfinitenumberofupdates. |     |     |     |          |     |          |     |     |     |     |
| --- | ----------- | --- | --------------------------------- | --- | --- | --- | -------- | --- | -------- | --- | --- | --- | --- |
|     |             |     |                                   |     |     |     | (cid:80) |     | (cid:80) |     |     |     |     |
6. Thelearningratessatisfyα (s,a) [0,1], α (s,a)= , (α (s,a))2 < withprobability1andα (s,a)=
|     |             |     |     |     | t   |     | t   | t   | t t |     |     |     | t   |
| --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 0, (s,a)=(s |     | ,a  | ).  |     | ∈   |     |     | ∞   |     | ∞   |     |     |
t t
|     | ∀   | (cid:54) |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

AddressingFunctionApproximationErrorinActor-CriticMethods
7. Var[r(s,a)]< , s,a.
∞ ∀
ThenClippedDoubleQ-learningwillconvergetotheoptimalvaluefunctionQ∗,asdefinedbytheBellmanoptimality
equation,withprobability1.
Proof of Theorem 1. We apply Lemma 1 with P = QA,QB,s ,a ,α ,r ,s ,...,s ,a ,X = S A,∆ = QA
t { 0 0 0 0 0 1 1 t t } × t t −
Q∗,ζ =α .
t t
Firstnotethatcondition1and4ofthelemmaholdsbytheconditions2and7ofthetheoremrespectively. Lemmacondition
2holdsbythetheoremcondition6alongwithourselectionofζ =α .
t t
Defininga∗ =argmax QA(s ,a)wehave
a t+1
∆ (s ,a )=(1 α (s ,a ))(QA(s ,a ) Q∗(s ,a ))
t+1 t t − t t t t t t − t t
+α (s ,a )(r +γmin(QA(s ,a∗),QB(s ,a∗)) Q∗(s ,a )) (19)
t t t t t t+1 t t+1 − t t
=(1 α (s ,a ))∆ (s ,a )+α (s ,a )F (s ,a )),
t t t t t t t t t t t t
−
wherewehavedefinedF (s ,a )as:
t t t
F (s ,a )=r +γmin(QA(s ,a∗),QB(s ,a∗)) Q∗(s ,a )
t t t t t t+1 t t+1 − t t t
=r +γmin(QA(s ,a∗),QB(s ,a∗)) Q∗(s ,a )+γQA(s ,a∗) γQA(s ,a∗) (20)
t t t+1 t t+1 − t t t t t+1 − t t+1
=FQ(s ,a )+c ,
t t t t
where FQ = r + γQA(s ,a∗) Q∗(s ,a ) denotes the value of F under standard Q-learning and c =
t t t t+1 − t t t (cid:104) (cid:105) t t
γmin(QA(s ,a∗),QB(s ,a∗)) γQA(s ,a∗). AsE FQ P γ ∆ isawell-knownresult,thencondition3
t t+1 t t+1 − t t+1 t | t ≤ || t ||
oflemma1holdsifitcanbeshownthatc convergesto0withprobability1.
t
Lety =r +γmin(QB(s ,a∗),QA(s ,a∗))and∆BA(s ,a )=QB(s ,a ) QA(s ,a ),wherec convergesto0
t t t+1 t t+1 t t t t t t − t t t t
if∆BAconvergesto0. Theupdateof∆BAattimetisthesumofupdatesofQAandQB:
t
∆BA(s ,a )=∆BA(s ,a )+α (s ,a ) (cid:0) y QB(s ,a ) (y QA(s ,a )) (cid:1)
t+1 t t t t t t t t − t t t − − t t t
=∆BA(s ,a )+α (s ,a ) (cid:0) QA(s ,a ) QB(s ,a ) (cid:1) (21)
t t t t t t t t t − t t t
=(1 α (s ,a ))∆BA(s ,a ).
− t t t t t t
Clearly∆BA willconvergeto0,whichthenshowswehavesatisfiedcondition3oflemma1,implyingthatQA(s ,a )
t t t
converges to Q∗(s ,a ). Similarly, we get convergence of QB(s ,a ) to the optimal vale function by choosing ∆ =
t t t t t t
QB Q∗andrepeatingthesamearguments,thusprovingtheorem1.
t −
B.OverestimationBiasinDeterministicPolicyGradients
Ifthegradientsfromthedeterministicpolicygradientupdateareunnormalized,thisoverestimationisstillguaranteedto
occurunderaslightlystrongerconditionontheexpectationofthevalueestimate. Assumetheapproximatevaluefunctionis
equaltothetruevaluefunction,inexpectationoverthesteady-statedistribution,withrespecttopolicyparametersbetween
theoriginalpolicyandinthedirectionofthetruepolicyupdate:
E [Q (s,π (s))]=E [Qπ(s,π (s))]
s∼π θ new s∼π new
(22)
φ [φ,φ+β(φ φ)]suchthatβ >0.
new true
∀ ∈ −
Notingthatφ maximizestherateofchangeofthetruevalue∆π =Qπ(s,π (s)) Qπ(s,π (s)),∆π ∆π . By
true true true − φ true ≥ approx
thegivencondition22themaximalrateofchangeoftheapproximatevaluemustbeatleastasgreat∆θ ∆π . Given
approx ≥ true
Q (s,π )=Qπ(s,π )thisimpliesQ (s,π (s)) Qπ(s,π (s)) Qπ(s,π (s)),showinganoverestimationof
θ φ φ θ approx true approx
≥ ≥
thevaluefunction.

AddressingFunctionApproximationErrorinActor-CriticMethods
Table3.Acompletecomparisonofhyper-parameterchoicesbetweenourDDPGandtheOpenAIbaselinesimplementation(Dhariwal
etal.,2017).
|     |     | Hyper-parameter      | Ours   | DDPG        |
| --- | --- | -------------------- | ------ | ----------- |
|     |     | CriticLearningRate   | 10−3   | 10−3        |
|     |     | CriticRegularization | None   | 10−2·||θ||2 |
|     |     | ActorLearningRate    | 10−3   | 10−4        |
|     |     | ActorRegularization  | None   | None        |
|     |     | Optimizer            | Adam   | Adam        |
|     |     |                      | 5·10−3 | 10−3        |
TargetUpdateRate(τ)
|     |     |     | 100 | 64  |
| --- | --- | --- | --- | --- |
BatchSize
|     |     |     | 1   | 1   |
| --- | --- | --- | --- | --- |
Iterationspertimestep
|     |     |     | 0.99 | 0.99 |
| --- | --- | --- | ---- | ---- |
DiscountFactor
|     |     |     | 1.0 | 1.0 |
| --- | --- | --- | --- | --- |
RewardScaling
|     |     | NormalizedObservations | False                        | True  |
| --- | --- | ---------------------- | ---------------------------- | ----- |
|     |     | GradientClipping       | False                        | False |
|     |     | ExplorationPolicy      | N(0,0.1) OU,θ=0.15,µ=0,σ=0.2 |       |
C.DDPGNetworkandHyper-parameterComparison
DDPGCriticArchitecture
| (state dim, | 400) |     |     |     |
| ----------- | ---- | --- | --- | --- |
ReLU
| (action | dim + 400, | 300) |     |     |
| ------- | ---------- | ---- | --- | --- |
ReLU
(300, 1)
DDPGActorArchitecture
| (state dim, | 400) |     |     |     |
| ----------- | ---- | --- | --- | --- |
ReLU
(400, 300)
ReLU
(300, 1)
tanh
OurCriticArchitecture
| (state dim | + action | dim, 400) |     |     |
| ---------- | -------- | --------- | --- | --- |
ReLU
| (action | dim + 400, | 300) |     |     |
| ------- | ---------- | ---- | --- | --- |
RelU
(300, 1)
OurActorArchitecture
| (state dim, | 400) |     |     |     |
| ----------- | ---- | --- | --- | --- |
ReLU
(400, 300)
RelU
(300, 1)
tanh

AddressingFunctionApproximationErrorinActor-CriticMethods
D.AdditionalImplementationDetails
Forclarityinpresentation,certainimplementationdetailswereomitted,whichwedescribehere. Forthemostcomplete
possibledescriptionofthealgorithm,codecanbefoundonourGitHub(https://github.com/sfujim/TD3).
OurimplementationofbothDDPGandTD3followsastandardpracticeindeepQ-learning,inwhichtheupdatediffersfor
terminaltransitions. Fortransitionswheretheepisodeterminatesbyreachingsomefailurestate,andnotduetotheepisode
runninguntilthemaxhorizon,thevalueofQ(s, )issetto0inthetargety:
·
(cid:40)
r ifterminals(cid:48)andt<maxhorizon
y =
r+γQ (s(cid:48),π (s(cid:48))) else
θ(cid:48) φ(cid:48)
Fortargetpolicysmoothing(Section5.3),theaddednoiseisclippedtotherangeofpossibleactions,toavoiderrorintroduced
byusingvaluesofimpossibleactions:
y =r+γQ (s(cid:48),clip(π (s(cid:48))+(cid:15),minaction,maxaction)),
θ(cid:48) φ(cid:48)
(cid:15) clip( (0,σ), c,c).
∼ N −
E.SoftActor-CriticImplementationDetails
For our implementation of Soft Actor-Critic (Haarnoja et al., 2018) we use the code provided by the author (https:
//github.com/haarnoja/sac), using the hyper-parameters described by the paper. We use a Gaussian mixture
policywith4Gaussiandistributions,exceptfortheReacher-v1task,whereweuseasingleGaussiandistributiondueto
numericalinstabilityissuesintheprovidedimplementation. Weusetheenvironment-dependentrewardscalingasdescribed
bytheauthors,multiplyingtherewardsby3forWalker2d-v1andAnt-v1,and1forallremainingenvironments.
Forfaircomparisonwithourmethod,wetrainforonly1iterationpertimestep,ratherthanthe4iterationsusedbythe
resultsreportedbytheauthors. Thisalongwithfewertotaltimestepsshouldexplainforthediscrepancyinresultsonsome
oftheenvironments. Additionally,wenotethiscomparisonisagainstapriorversionofSoftActor-Critic,whilethemost
recentvariantincludesourClippedDoubleQ-learninginthevalueupdateandproducescompetitiveresultstoTD3onmost
tasks.

AddressingFunctionApproximationErrorinActor-CriticMethods
F.AdditionalLearningCurves
|     |     | TD3 | DDPG |     | AHE |     | AHE+TPS | AHE+DP |     | AHE+CDQ |     |
| --- | --- | --- | ---- | --- | --- | --- | ------- | ------ | --- | ------- | --- |
5000
| 10000 |     |     | 3500 |     |     |     |     |     |     |     |     |
| ----- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
4000
| 8000          |     |     | 3000 |     |     |     | 4000 |     |     |     |     |
| ------------- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- |
| nruteRegarevA |     |     | 2500 |     |     |     |      |     |     |     |     |
3000
| 6000 |     |     | 2000 |     |     |     | 3000 |     |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- |
2000
| 4000 |     |     | 1500 |     |     |     | 2000 |     |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- |
1000
| 2000 |     |     | 1000 |     |     |     |      |     |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- |
|      |     |     | 500  |     |     |     | 1000 |     |     | 0   |     |
| 0    |     |     | 0    |     |     |     | 0    |     |     |     |     |
0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0− 1000 0.0 0.2 0.4 0.6 0.8 1.0
|                   | Timesteps(1e6) |     |     | Timesteps(1e6) |     |     |     | Timesteps(1e6) |     |     | Timesteps(1e6) |
| ----------------- | -------------- | --- | --- | -------------- | --- | --- | --- | -------------- | --- | --- | -------------- |
| (a)HalfCheetah-v1 |                |     |     | (b)Hopper-v1   |     |     |     | (c)Walker2d-v1 |     |     | (d)Ant-v1      |
Figure6.AblationoverthevaryingmodificationstoourDDPG(AHE),comparingthesubtractionofdelayedpolicyupdates(TD3-DP),
targetpolicysmoothing(TD3-TPS)andClippedDoubleQ-learning(TD3-CDQ).
|       |     | TD3 |      | DDPG | AHE |     | TD3-TPS | TD3-DP |     | TD3-CDQ |     |
| ----- | --- | --- | ---- | ---- | --- | --- | ------- | ------ | --- | ------- | --- |
| 10000 |     |     | 3500 |      |     |     | 5000    |        |     |         |     |
4000
|     |     |     | 3000 |     |     |     | 4000 |     |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- |
nruteRegarevA 8000
|      |     |     | 2500 |     |     |     |      |     |     | 3000 |     |
| ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | ---- | --- |
| 6000 |     |     | 2000 |     |     |     | 3000 |     |     |      |     |
2000
| 4000 |     |     | 1500 |     |     |     | 2000 |     |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- |
1000
1000
| 2000 |     |     |     |     |     |     | 1000 |     |     | 0   |     |
| ---- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
500
| 0   |     |     | 0   |     |     |     | 0   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0− 1000 0.0 0.2 0.4 0.6 0.8 1.0
|                   | Timesteps(1e6) |     |     | Timesteps(1e6) |     |     |     | Timesteps(1e6) |     |     | Timesteps(1e6) |
| ----------------- | -------------- | --- | --- | -------------- | --- | --- | --- | -------------- | --- | --- | -------------- |
| (a)HalfCheetah-v1 |                |     |     | (b)Hopper-v1   |     |     |     | (c)Walker2d-v1 |     |     | (d)Ant-v1      |
Figure7.AblationoverthevaryingmodificationstoourDDPG(AHE),comparingtheadditionofdelayedpolicyupdates(AHE+DP),
targetpolicysmoothing(AHE+TPS)andClippedDoubleQ-learning(AHE+CDQ).
|       |     |     | TD3  |     | AHE | TD3-CDQ |      | DQ-AC | DDQN-AC |      |     |
| ----- | --- | --- | ---- | --- | --- | ------- | ---- | ----- | ------- | ---- | --- |
|       |     |     | 3500 |     |     |         | 5000 |       |         |      |     |
| 10000 |     |     |      |     |     |         |      |       |         | 4000 |     |
|       |     |     | 3000 |     |     |         | 4000 |       |         |      |     |
nruteRegarevA 8000
|      |     |     | 2500 |     |     |     |      |     |     | 3000 |     |
| ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | ---- | --- |
| 6000 |     |     | 2000 |     |     |     | 3000 |     |     |      |     |
2000
|      |     |     | 1500 |     |     |     | 2000 |     |     |      |     |
| ---- | --- | --- | ---- | --- | --- | --- | ---- | --- | --- | ---- | --- |
| 4000 |     |     |      |     |     |     |      |     |     | 1000 |     |
1000
| 2000 |     |     |     |     |     |     | 1000 |     |     | 0   |     |
| ---- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
500
| 0   |     |     |     |     |     |     | 0   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
0.0 0.2 0.4 0.6 0.8 1.0 0 0.0 0.2 0.4 0.6 0.8 1.0 0.0 0.2 0.4 0.6 0.8 1.0− 1000 0.0 0.2 0.4 0.6 0.8 1.0
|                   | Timesteps(1e6) |     |     | Timesteps(1e6) |     |     |     | Timesteps(1e6) |     |     | Timesteps(1e6) |
| ----------------- | -------------- | --- | --- | -------------- | --- | --- | --- | -------------- | --- | --- | -------------- |
| (a)HalfCheetah-v1 |                |     |     | (b)Hopper-v1   |     |     |     | (c)Walker2d-v1 |     |     | (d)Ant-v1      |
Figure8.ComparisonofTD3andtheDoubleQ-learning(DQ-AC)andDoubleDQN(DDQN-AC)actor-criticvariants,whichalso
leveragedelayedpolicyupdatesandtargetpolicysmoothing.