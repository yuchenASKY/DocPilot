# Conditional Tensor Diffusion: Distributional Counterfactual Learning and Inference

> **领域**：`econ.EM`　**发布**：2026-09-22　**arXiv**：[2609.25924v1](https://arxiv.org/abs/2609.25924v1)
>
> **作者**：Xinbing Kong, Zeyu Li, Junfan Mao, Bin Wu
>
> **来源**：arXiv 预印本（开放获取）　**页数**：102

---

## Abstract

Causal inference guides operational and managerial decisions but remains challenging in high-dimensional panel or tensor settings, where decisions may depend on the joint conditional distribution of missing control outcomes. We develop \emph{Counterfactual Tucker Diffusion} (\CFTDiff), which integrates the treatment mask and latent Tucker structure into conditional diffusion to recover this distribution given observed control outcomes through efficient nonlinear score learning in a low-dimensional core. The masked Tucker score preserves dependence across tensor modes while reducing the dimension of nonlinear score learning from the product of mode dimensions to the much smaller product of Tucker ranks. We establish high-probability error bounds for conditional score estimation that depend on the Tucker ranks, largest mode dimension, and the factor-strength-adjusted number of missing outcomes, and show how these bounds translate into recovery guaranties for the conditional distribution of the missing control outcomes. Across missing rates, simulations show more accurate point recovery than common causal panel and matrix/tensor completion methods; comparisons with nested diffusion specifications further demonstrate the gains from masked conditioning and Tucker dimension reduction. In Norway's iFlex experiment, \CFTDiff recovers missing outcomes more accurately than competing methods; when applied to causal analysis, its estimated conditional distributions yield counterfactual prediction intervals and target-attainment probabilities, allowing pricing interventions to be evaluated by demand-reduction magnitude and reliability.

---

## 正文（由 PDF 提取）

Conditional Tensor Diffusion: Distributional
Counterfactual Learning and Inference
Xinbing Kong,a Zeyu Li,a Junfan Mao,a Bin Wub
aSoutheast University; bUniversity of Science and Technology of China
Contact:xinbingkong@126.com (XK), zeyuli@seu.edu.cn (ZL), maojf@seu.edu.cn (JM), bin.w@ustc.edu.cn (BW)
Abstract.Causal inference guides operational and managerial decisions but remains challenging in high-dimensional panel or
tensor settings, where decisions may depend on the joint conditional distribution of missing control outcomes. We developCoun-
terfactual Tucker Diffusion(CFT-DIFF), which integrates the treatment mask and latent Tucker structure into conditional diffusion
to recover this distribution given observed control outcomes through efficient nonlinear score learning in a low-dimensional core.
The masked Tucker score preserves dependence across tensor modes while reducing the dimension of nonlinear score learning
from the product of mode dimensions to the much smaller product of Tucker ranks. We establish high-probability error bounds for
conditional score estimation that depend on the Tucker ranks, largest mode dimension, and the factor-strength-adjusted number of
missing outcomes, and show how these bounds translate into recovery guaranties for the conditional distribution of the missing con-
trol outcomes. Across missing rates, simulations show more accurate point recovery than common causal panel and matrix/tensor
completion methods; comparisons with nested diffusion specifications further demonstrate the gains from masked conditioning and
Tucker dimension reduction. In Norway’s iFlex experiment,CFT-DIFFrecovers missing outcomes more accurately than compet-
ing methods; when applied to causal analysis, its estimated conditional distributions yield counterfactual prediction intervals and
target-attainment probabilities, allowing pricing interventions to be evaluated by demand-reduction magnitude and reliability.
Key words:Diffusion model; counterfactual; tensor completion; generative AI; distributional recovery.

## Introduction

Causal inference is central to pricing, policy evaluation, and intervention design, yet the outcome needed to
evaluate an intervention is missing where treatment occurs. At a treated entry in a panel, the intervention
outcome is observed, but the corresponding control outcome is missing. Point estimates of the missing
control outcomes may be sufficient for reporting an average effect. They are not sufficient when a decision
maker must assess the probability of meeting a demand, service, or risk target, quantify uncertainty in the
missing outcomes, or compare the reliability of alternative interventions. The central statistical problem is
therefore to recover the joint conditional distribution of the missing control outcomes given the observed
control outcomes, rather than a single point estimate.
Recovering this distribution is difficult in high-dimensional panel or tensor settings. Outcomes may be
indexed by units, dates, hours, products, or locations, so the full dimension grows as the product of the
mode dimensions. A tensor formulation preserves these indexing dimensions and their dependence, while
including vector and matrix settings. Treatment determines where the control outcomes are missing, often
producing a structured missingness pattern. The missing outcomes may remain dependent across units, time
1
arXiv:2609.25924v1 [stat.ML] 22 Sep 2026

Kong et al.:Conditional Tensor Diffusion
2
periods, and other dimensions. Estimating each missing outcome separately does not capture this depen-
dence and therefore cannot evaluate probabilities involving multiple missing outcomes. Directly learning
a conditional distribution in the tensor space is also statistically and computationally demanding. A useful
method must therefore incorporate the treatment mask, use information from the observed control outcomes,
and exploit the intrinsic structure of the control-outcome tensor.
We developCounterfactual Tucker Diffusion(CFT-DIFF), a masked conditional diffusion model for recov-
ering the joint conditional distribution of the missing control outcomes. Its central construction is a masked
Tucker score that incorporates the treatment pattern and observed control outcomes while confining non-
linear score learning to a low-dimensional Tucker core. The method therefore provides joint conditional
generation rather than point recovery and avoids learning an unrestricted nonlinear score in the full tensor
space. During training, the treatment mask is synthetically applied to complete training tensors, allowing
the model to learn the distribution of the masked outcomes given the observed outcomes. During causal
analysis, the observed control outcomes remain fixed and only the missing control outcomes are gener-
ated; observed treated outcomes enter subsequently when causal contrasts are formed. Repeated conditional
draws provide point estimates, quantiles, counterfactual prediction intervals, target-attainment probabilities,
and other summaries from a single learned distribution.
The key structural result explains why this conditional distribution can be learned efficiently. Mode-
specific linear encoders combine the noised outcomes in the treated region and the observed control out-
comes into a core-level statistic, and a Tucker decoder maps the learned core representation back to the
original coordinates. Only the conditional map within the core is nonlinear. LetDdenote the number of
modes,p d the dimension of moded, andr d its Tucker rank. The full tensor hasp= QD
d=1pd coordinates,
whereas the Tucker core has onlyr= QD
d=1rd coordinates, withr≪p. Nonlinear learning therefore oper-
ates in dimensionrrather thanp, while the separately parameterized loading matrices contribute through
pmax = maxdpd rather than the productp.
We establish nonasymptotic, high-probability error bounds for conditional-score estimation. Letndenote
the number of training tensors. The bound separates the errors from learning the nonlinear core regression
and estimating the mode-specific loading spaces. The dominant sample-size term for the nonlinear com-
ponent isn−2/(r+5), whose exponent depends on the intrinsic core dimensionrrather than the full tensor
dimensionp. Becauser≪punder low Tucker rank, this rate yields more accurate score estimation from
the same training sample size than a rate governed by the full tensor dimension. Estimating the loading
spaces contributesp maxn−(r+3)/(r+5), so this component depends on the largest mode dimensionpmax rather
than the product of all mode dimensionsp. The number of missing control outcomesp T and the strength
of the low-rank signalβenter through the effective dimensiond T,β =r+p Tp−β. Thus, the contribution
of the missing region enters asp Tp−β, rather thanp T itself, and remains bounded whenp T≲pβ and the
Tucker ranks are fixed. We further show that conditional-score accuracy transfers to recovery of the condi-
tional distribution of the missing outcomes. Under the stated growth and regularity conditions, prediction
intervals constructed from samples drawn from the estimated conditional distribution attain nominal condi-
tional coverage as the training and generation sample sizes increase, without requiring a separate Gaussian
approximation or asymptotic variance estimation.

Kong et al.:Conditional Tensor Diffusion
3
Simulations with known conditional distributions show thatCFT-DIFFimproves point recovery over the
causal panel and matrix/tensor completion methods considered. Comparisons with two nested diffusion
specifications attribute the additional gains to Tucker dimension reduction and conditioning on the observed
control outcomes through the treatment mask;CFT-DIFFalso improves distributional recovery and produces
sharper prediction intervals while retaining coverage close to the nominal level.
We applyCFT-DIFFto Norway’s iFlex dynamic-pricing experiment. Before estimating demand responses,
we artificially mask fully observed no-policy (control) outcomes and evaluate recovery under switchback,
staggered-adoption, and simultaneous-adoption designs.CFT-DIFFattains the lowest point-recovery errors
among the causal panel and matrix/tensor completion methods and the nested diffusion specifications, and it
achieves more accurate distributional recovery than both nested diffusion specifications across the treatment
patterns and missing proportions considered. For intervention days, the estimated conditional distributions
yield counterfactual prediction intervals, characterize variation in demand reductions across interventions,
and quantify the probability that a price signal achieves a specified peak-demand reduction. The results
show that price signals with similar average demand reductions can differ substantially in their probability
of achieving a specified reduction target. This information allows price signals to be compared by both their
average demand reduction and how reliably they achieve a desired peak reduction.
1.1. Contributions
We make four contributions. First, we formulate counterfactual distribution recovery for general multi-way
outcome arrays and develop a conditional diffusion framework for this problem. The formulation includes
vectors and matrices as special cases, thereby covering conventional panels as well as higher-order tensors.
CFT-DIFFincorporates prespecified intervention masks into training, allowing the model to learn the distri-
bution of masked outcomes given the observed control outcomes. Because the construction does not rely
on random missingness or a particular treatment pattern, it accommodates switchback, staggered-adoption,
simultaneous-adoption, and other structured intervention patterns under the stated conditions. During coun-
terfactual generation, the observed control outcomes remain fixed and only the missing control outcomes
are generated, producing samples from their estimated joint conditional distribution. Existing tensor-based
causal methods and common causal panel and completion methods primarily target point counterfactu-
als, common components, or low-dimensional causal summaries. By recovering the conditional distribu-
tion,CFT-DIFFalso permits distributional comparisons and provides quantiles, counterfactual prediction
intervals, target-attainment probabilities, and other summaries without requiring a separate model for each
quantity.
Second, we introduce a masked Tucker score that makes high-dimensional conditional generation for
tensor data statistically tractable and computationally efficient. Generic diffusion networks learn nonlinear
scores in the full data space, while conventional low-rank completion methods do not recover a joint condi-
tional distribution. Under the control-outcome factor model, we show that the conditional score admits a rep-
resentation in which mode-wise linear maps preserve the tensor structure and nonlinear learning takes place
through a core-dimensional conditional regression. The neural approximation burden, therefore, depends on
the Tucker core dimensionr, rather than the full tensor dimensionp. Our nonasymptotic score bounds for-
malize this intrinsic-dimensional advantage: nonlinear estimation is governed by the Tucker core, loading-

Kong et al.:Conditional Tensor Diffusion
4
space estimation byp max, and the joint effect of the size of the treated region and factor strength byd T,β .
The result provides a statistical foundation for using low-rank Tucker structure in conditional diffusion.
Third, we establish end-to-end guaranties that carry conditional-score accuracy through to the recovery of
the missing-outcome distribution, weighted causal summaries, and counterfactual prediction intervals. We
derive high-probability bounds for the recovery of the joint conditional distribution of the missing control
outcomes and extend these bounds to weighted summaries of the missing outcomes. Combined with the
corresponding observed treated outcomes, these summaries yield familiar causal estimands (e.g., average
treatment effects). We further establish coverage guaranties for counterfactual prediction intervals derived
from the estimated conditional distribution and explicitly account for the additional error arising from a
finite generation sample. The interval theory requires neither a Gaussian approximation nor asymptotic
variance estimation. These intervals quantify uncertainty about the missing control outcomes conditional
on the observed control outcomes. The results therefore carry score-learning accuracy through to the causal
estimands and counterfactual uncertainty measures used in subsequent analysis.
Finally, simulations and the iFlex experiment identify the gains from the two components ofCFT-DIFFand
demonstrate the decision value of recovering a conditional distribution. Simulations with known counterfac-
tual distributions compareCFT-DIFFwith established causal panel and matrix/tensor completion methods in
point recovery and use distributional measures to evaluateCFT-DIFFand its nested diffusion specifications
beyond point estimates. The two nested specifications separately identify the gains from Tucker dimension
reduction and conditioning on the observed control outcomes. We then validate the method on observed
no-policy outcomes in the iFlex data under switchback, staggered-adoption, and simultaneous-adoption pat-
terns. In the causal application, the recovered distribution is used to compare dynamic-pricing signals in
terms of both the magnitude of demand reduction and the probability of attaining specified peak-reduction
targets. The results show that price signals with similar estimated average effects can differ materially in
their reliability, illustrating the additional decision-relevant information provided by counterfactual distri-
bution recovery.
1.2. Related Literature
Causal panel methods and counterfactual recovery.Existing causal panel methods address important
parts of this problem, but their primary targets are different. Difference-in-differences and event-study esti-
mators recover average effects under restrictions such as parallel trends and no anticipation, with modern
procedures allowing heterogeneous treatment effects (Borusyak et al. 2024). Synthetic-control methods use
pretreatment outcomes and a suitable donor pool to construct point estimates under stable preintervention
relationships. Synthetic difference-in-differences combines these comparison strategies through outcome
balancing and time and unit weighting (Arkhangelsky et al. 2021). Low-rank causal panel methods repre-
sent the untreated outcome surface using interactive factors and view treated coordinates as missing entries
(Athey et al. 2021, Bai and Ng 2021). Subsequent work permits nonrandom or more general observation
patterns and develops entrywise inference (Choi and Yuan 2024, Xiong and Pelger 2023, Duan et al. 2024).
A small recent literature uses tensor completion directly for causal recovery with treatment histories, mul-
tiple outcomes, or multiple exposures (Mandal and Parkes 2019, Auerbach et al. 2022, Zhen and Wang
2024, Gao et al. 2025, Zhou et al. 2026). Synthetic interventions extend this logic to several treatments and
tensor-valued potential outcomes and estimate potential outcomes or low-dimensional causal summaries

Kong et al.:Conditional Tensor Diffusion
5
(Agarwal et al. 2026).CFT-DIFFshares the potential-outcome and low-rank viewpoints but targets a differ-
ent statistical object: the joint conditional distribution of the missing control outcomes given the observed
control outcomes. The treatment design and identifying assumptions determine the causal interpretation of
the resulting comparisons;CFT-DIFFaddresses estimation of this conditional distribution.
Matrix and tensor completion.Matrix and tensor completion methods exploit low rank structures to
recover missing entries, but their guaranties often depend on how the observed coordinates cover the matri-
ces or tensors (Xia and Yuan 2019, Xia et al. 2021, Xia and Yuan 2021). Causal panels are especially
demanding because treatment creates structured and potentially nonrandom observation patterns rather than
dispersed incidental missingness. Factor methods have been adapted to these patterns, but their outputs
remain point imputations or entrywise sampling distributions. Treatment designs can also create very differ-
ent patterns, including switchback schedules and staggered or simultaneous adoption (Bojinov et al. 2023,
Chen and Simchi-Levi 2026). Tensor factor models preserve mode-specific dependence in matrix sequences
and tensors (Wang et al. 2019, Chang et al. 2023, 2026a,b, Han et al. 2024), and tensor time-series imputa-
tion allows broad missing patterns (Cen and Lam 2025).CFT-DIFFuses the same multilinear structure for a
different purpose. It incorporates the treatment mask into training and uses the observed control outcomes to
generate the missing control outcomes, thereby providing their joint conditional distribution in addition to
point estimates. The fixed-mask formulation does not require a random-missingness model for estimation.
Marginal counterfactual distributions.A separate literature studies how interventions change out-
come distributions. Changes-in-changes models identify nonlinear and quantile effects under distributional
restrictions (Athey and Imbens 2006); counterfactual distribution methods provide inference for population
distributions constructed from conditional models (Chernozhukov et al. 2013); and distributional synthetic
controls match the distribution of an aggregate treated unit over time (Gunsilius 2023). Related work stud-
ies treatment-effect risk, formalized through the conditional value at risk of the individual treatment-effect
distribution, and develops bounds and inference based on the conditional average treatment effect (Kallus
2023). Bayesian and semiparametric procedures characterize posterior or sampling uncertainty for low-
dimensional causal parameters such as the average treatment effect (Breunig et al. 2025). These methods
answer questions about marginal counterfactual distributions, distributional treatment effects, treatment-
effect risk, or estimator uncertainty. Our target is the joint conditional distribution of the missing control
outcomes given the observed control outcomes. Recovering this distribution provides prediction intervals
for individual and aggregate counterfactuals, tail probabilities, and probabilities of joint target attainment,
enabling interventions to be evaluated by both effect magnitude and reliability.
Diffusion models and conditional generation.Diffusion models can simulate from complex multivari-
ate distributions by estimating scores along a noise-perturbation path and running the reverse dynamics
(Song and Ermon 2019, Ho et al. 2020, Song et al. 2021). Conditional score models have been used for
probabilistic time-series imputation (Tashiro et al. 2021) and conditional response generation for boot-
strap inference (Chang et al. 2026c). Causal diffusion methods have generated structural counterfactuals
for images or learned individual potential-outcome distributions conditional on covariates, with the latter
using an orthogonal loss to address treatment-selection bias (Sanchez and Tsaftaris 2022, Ma et al. 2024).
General conditional-diffusion theory and recovery results under low-dimensional structure supply important
foundations (Fu et al. 2024, Chen et al. 2023, Fan et al. 2025). Related work integrates factor structure into

Kong et al.:Conditional Tensor Diffusion
6
high-dimensional financial simulation (Chen et al. 2025), develops diffusion methods for heavy-tailed and
conditional simulation in operations research (Liu et al. 2026), and studies unconditional Tucker diffusion
(Guo et al. 2026). These studies establish the feasibility of using diffusion models for related missing-data
and causal tasks. For the target studied here, however, an unconditional diffusion model cannot directly
exploit the observed control outcomes. A general conditional diffusion model permits such conditioning,
but does not by itself determine how the treatment pattern enters training and generation or how the result-
ing distribution is linked to the missing control outcomes. Learning the conditional score directly in the full
tensor space would also require a high-dimensional nonlinear model whose input and output dimensions
grow with the total number of tensor entries. Building on these foundations,CFT-DIFFincorporates the
treatment mask and observed control outcomes into a conditional score for the missing control outcomes,
with nonlinear learning conducted in the Tucker core.
Organization.Section 3 formulates counterfactual distribution recovery for tensor data, developsCFT-
DIFF, and establishes its score-learning guaranties. Section 4 studies recovery of the conditional distribution
of the missing control outcomes, weighted summaries, and prediction intervals. Sections 5 and 6 report
the simulation and empirical studies. Section 7 concludes. The Appendix contains complete proofs and
additional results.
Notation.For random elementsXandY,L(X)denotes the probability law ofX,L(X|Y)denotes
its conditional law givenY, andL(X|Y=y)denotes the conditional law evaluated atY=y. For
m∈N, let[m] ={1,...,m}. The operatorvec(·)denotes vectorization under a fixed convention.
The symbol1denotes an all-ones array whose dimensions are determined by context. For a vectorg,
reshape{g; (m1,...,m D)}denotes its rearrangement into anm 1×···×m D tensor according to the vec-
torization convention used byvec. We write∥·∥ 2,∥·∥ F , and∥·∥ op for the Euclidean norm of a vector, the
Frobenius norm of a matrix or tensor, and the operator norm of a matrix, respectively. The notationO(·)sup-
presses constants depending only on fixed model parameters, whereaseO(·)additionally suppresses polylog-
arithmic factors in the asymptotic quantities specified in the result. In this paper,⊙and⊘denote entrywise
multiplication and division. We writeKL(µ∥ν)for relative entropy andTV(µ,ν) = sup A|µ(A)−ν(A)|
for total variation distance. For probability measuresµandνonR, we use the bounded–Lipschitz metric
dBL(µ,ν) := sup∥φ∥∞≤1
Lip(φ)≤1
R
φdµ−
R
φdν
, whereLip(φ)denotes the Lipschitz constant ofφ.
2. Diffusion Models: Preliminaries
Diffusion models represent a target distribution through two linked stochastic processes: a known forward
process that gradually perturbs data into noise and a reverse-time process that transforms noise back into
data. The reverse-time process depend on the scores of the noise-perturbed distributions along the forward
path; these scores must be learned from data. By outlining the basic principles of diffusion models in a
simple scalar setting, this section provides the background needed to understand our framework for tensor
generation developed in the paper.
2.1. Forward Diffusion and Reverse-Time Generation
Forward diffusion.LetX 0∈Rhave data distributionP 0. We consider the variance-preserving Ornstein–
Uhlenbeck (OU) diffusion, 1 a continuous-time formulation of the Gaussian noising mechanism used in

Kong et al.:Conditional Tensor Diffusion
7
diffusion models (Ho et al. 2020, Song et al. 2021):
dXt =− 1
2η(t)Xt dt+η(t) 1/2 dWt, X 0∼P 0, t∈[0,T],(2.1)
where{W t}t≥0 is a standard Wiener process andη(t)>0is a deterministic noise schedule. Defineα t =
exp(− 1
2
Rt
0η(v) dv)andh t = 1−α 2
t . For eacht, the linear structure of (2.1) gives the explicit perturbation
representation
Xt =αtX0 +h 1/2
t Zt, Z t∼N(0,1), Z t⊥⊥X0.
Letq t(·|x 0)denote the Gaussian transition density ofX t conditional onX 0 =x 0. The corresponding
time-tmarginal density is
pt(x) =
Z
R
qt(x|x 0)P 0(dx0), P t =L(Xt).
The distinction betweenq t andp t is important. The transition densityq t(·|x 0)is the known Gaussian
perturbation kernel selected by the modeler, whereaspt is the generally unknown marginal density obtained
by mixing this kernel over the data distributionP 0. Althoughq t remains Gaussian, its mean and variance
vary witht; the marginal densityp t need not belong to a fixed parametric family, and its form generally
changes witht.
Astincreases, the contribution ofα tX0 diminishes and the Gaussian component becomes dominant.
Consequently, whenα T is sufficiently small, the terminal distributionP T is close to the standard normal
distributionN(0,1).
Reverse-time generation.Fort>0, define the time-tscore of the marginal distributionP t bys t(x) :=
∇x logpt(x). Thus, the score used in the reverse-time process is the gradient of the log marginal densitypt,
not the score of the Gaussian transition kernelqt(·|x 0).
Under standard regularity conditions, the forward diffusion admits a reverse-time representation (Ander-
son 1982, Song et al. 2021). Usinguto denote time elapsed in the reverse direction, the exact reverse-time
process satisfies
dX←
u =
1
2η(T−u)X ←
u +η(T−u)s T−u
 
X←
u

du+η(T−u) 1/2 dWu, u∈[0,T−t 0],(2.2)
where{Wu}u≥0 is a standard Wiener process andt 0>0is a small early-stopping time. IfX ←
0 ∼PT , then
X←
u ∼PT−u foru∈[0,T−t 0], and henceX←
T−t 0∼Pt0.
The forward process therefore provides analytically noised observations for learning, whereas the reverse-
time process provides the mechanism for generation.2 Once the forward coefficients are specified, the only
unknown quantity in the reverse drift is the time-dependent marginal score.
2.2. Conditional Scores, Denoising Score Matching, and Generation
Conditional target and reverse dynamics.LetCdenote observed conditioning information, and suppose
that the target is the conditional distributionP 0(·|c) =L(X 0|C=c). Conditional diffusion perturbs the
target variableX 0 while leaving the conditioning information unchanged. Thus,
Xt =αtX0 +h 1/2
t Zt, Z t∼N(0,1), Z t⊥⊥(X0,C).
For a realized conditionC=c, the conditional time-tdensity isp t(x|c) =
R
Rqt(x|x 0)P 0(dx0|c). It is
therefore a conditional mixture of the known perturbation kernel. Its score iss t(x|c) =∇ x logpt(x|c).

Kong et al.:Conditional Tensor Diffusion
8
Both arguments are essential: the functional form ofp t(·|c), and hence that ofs t(·|c), generally changes
with the diffusion timetand the conditioning valuec.
Conditional onC=c, replacing the marginal score in (2.2) withs t(x|c)gives the exact conditional
reverse-time process:
dX←
u =
1
2η(T−u)X ←
u +η(T−u)s T−u
 
X←
u |c

du+η(T−u) 1/2 dWu, u∈[0,T−t 0].(2.3)
IfX ←
0 ∼P T (·|c), thenX ←
u ∼P T−u (·|c)andX ←
T−t 0∼P t0(·|c). For each fixedc, the termα TX0
becomes negligible whenTis sufficiently large. Hence,P T (·|c)is close to the standard normal distribution
N(0,1), which supplies a tractable initialization for conditional generation.
Denoising score matching.The conditional reverse process cannot be implemented directly becausept(·|
c), and therefore its score, is unknown. For a candidate score functions(x,c,t), the natural population
score-matching criterion is
LSM(s) =
Z T
t0
λ(t)E
h
(s(Xt,C,t)−s t(Xt|C))
2
i
dt,(2.4)
whereλ(t)>0and
RT
t0
λ(t) dt= 1.3 The expectation is taken under the joint distribution of(X0,C)and the
forward perturbation.
The forward perturbation kernel, by contrast, is known. Sinceq t(·|x 0)is the density ofN(α tx0,ht), its
score (transition score) is available in closed form:
∇xt logqt(xt|x 0) =αtx0−xt
ht
,∇ Xt logqt(Xt|X 0) =− Zt
h1/2
t
.(2.5)
The second expression follows by substitutingXt =αtX0 +h 1/2
t Zt into the first. BecauseZt is independent
ofCconditional onX 0, the conditional denoising identity givesst(x|c) =E
h
αtX0−x
ht
Xt =x, C=c
i
. In
other words, the conditional marginal score is the regression function of the analytically available transition
score on(X t,C).
The conditional-expectation projection identity then implies that replacings t(Xt|C)in (2.4) by the
transition score in (2.5) changes the loss only by an additive term that does not depend ons. The two pop-
ulation objectives therefore have the same minimizer. This yields the conditional denoising score-matching
criterion
LDSM(s) =
Z T
t0
λ(t)E
"
s(Xt,C,t)− αtX0−Xt
ht
2#
dt.(2.6)
Empirical score learning.Given finite training observations{(X (i)
0 ,C (i))}n
i=1, we take the uniform time
weightλ(t) = 1/(T−t 0). The corresponding empirical counterpart of (2.6) is
bLDSM(s) = 1
n
nX
i=1
1
T−t 0
Z T
t0
EZt
"
s

αtX(i)
0 +h 1/2
t Zt,C (i),t

+ Zt
h1/2
t
2#
dt.
For a parameterized score classS, the trained conditional score is defined bybs∈arg min s∈S bLDSM(s).
In computation, the diffusion timetand Gaussian noiseZ t are sampled, so this optimization can be car-
ried out by stochastic gradient methods. The cutofft 0>0excludes the near-zero-noise region, where the
varianceh−1
t of the denoising target diverges ast↓0(making the score-learning problem increasingly
ill-conditioned).

Kong et al.:Conditional Tensor Diffusion
9
Figure 1Training and conditional generation inCFT-DIFF.
Note.Panel (a) shows the masked Tucker score architecture and its estimation from training tensors. The missing-outcome and
observed-outcome branches are encoded into the Tucker core, combined by the Core-Net, and decoded back to the treated region;
only the missing outcomes are noised during training. Panel (b) holds the observed control outcomes fixed and applies the learned
score to transform Gaussian noise in the missing region into samples frombPT
t0 (·|XC). Observed treated outcomes are reserved for
subsequent causal analysis.
Conditional generation.Letbsdenote the learned (trained) conditional score. Replacing the unknown
conditional score in (2.3) withbsand initializing the reverse process from the Gaussian approximation to
PT (·|c)yields the implementable generator
dbX←
u =
1
2η(T−u) bX←
u +η(T−u)bs
 bX←
u ,c,T−u

du+η(T−u) 1/2 dWu, u∈[0,T−t 0],(2.7)
with bX←
0 ∼N(0,1). For a fixed conditionc, repeated independent solutions of (2.7) produce draws from the
learned conditional distribution. Omitting the conditioning variableCrecovers the unconditional diffusion
model as a special case (Chen et al. 2023, Fu et al. 2024).
Section 3 extends this conditional-diffusion principle to tensor data for counterfactual distribution recov-
ery. The framework keeps the observed control outcomes fixed while generating the missing control out-
comes conditional on them. For notational simplicity, from Section 3 onward we setη(t)≡1, so thatα t =
e−t/2 andh t = 1−e−t.
3. Learning the Missing Control-World Distribution
This section developsCFT-DIFF, a tensor conditional-diffusion framework for recovering the conditional
distribution of missing control outcomes. We formulate the counterfactual problem under a fixed treatment
mask and introduce a masked diffusion that perturbs only the missing outcomes while holding the observed
control outcomes fixed. Tucker structure then reduces nonlinear score learning to the latent core, leading to
the estimation procedure and its intrinsic-dimensional guaranties. Figure 1 summarizes its implementation.

Kong et al.:Conditional Tensor Diffusion
10
3.1. Counterfactual Target and Training Sample
Counterfactual learning as tensor completion.Consider aD-way outcome array withp= QD
d=1pd
entries and index setI= [p 1]×···×[p D]. For each coordinatei= (i 1,...,i D)∈I, letY i(a)denote the
potential outcome under interventiona∈{0,1,...,A}, wherea= 0denotes control. The tensor modes may
represent units, time periods, outcome dimensions, or other sources of multi-way variation.
Let the mutually disjoint setsT a⊆Icollect the coordinates assigned to interventiona, and defineT=SA
a=1Ta andC=I\T. Under consistency, the observed outcome satisfies
Y obs
i =



Yi(0),i∈C,
Yi(a),i∈T a, a= 1,...,A.
Thus, every coordinate has an observed outcome, but a treated coordinate does not reveal the outcome that
would have occurred under control. Equivalently, the missing control outcomes are{Y i(0) :i∈T}.
Collect all control potential outcomes in the control-world tensorX 0 =

Yi(0)

i∈I∈R p1×···×pD. Let
P0 =L(X 0)denote its joint distribution. LetMT be the binary tensor equal to one onTand zero elsewhere,
and setMC =1−M T . The treatment design partitionsX 0 into
XC =MC⊙X 0 =MC⊙Y obs, X T =MT⊙X 0.(3.1)
BothXC andXT retain the dimensions ofX 0 and are padded with zeros outside the coordinates selected by
their respective masks. BecauseMC +MT =1, this partition satisfiesX 0 =XC +XT . When vector nota-
tion is needed, we writeMT = diag{vec(MT )}andM C =Ip−MT . The blockXC contains the observed
control outcomes, whereasX T contains the control outcomes missing at treated coordinates. Throughout,
“treated region” refers to the coordinate setT;X T therefore contains outcomes under control for coordi-
nates at which an intervention occurs. Treatment creates a structured missing region in the control-outcome
tensor even though the realized-outcome tensorY obs is fully observed. Unlike conventional tensor com-
pletion, our objective is to recover the conditional distribution of the missing control outcomes rather than
merely impute each missing entry. This distribution directly yields conditional means, quantiles, and other
distributional summaries.
Specifically, conditional on the observed control outcomes, our target is
PT
0 (·|X C) :=L(XT|XC).(3.2)
The treatment mask is prespecified and held fixed,4 so it is suppressed from the conditioning set. Recovering
(3.2) provides the full conditional distribution of the missing control outcomes in the treated region.
To connect this distributional target to downstream causal summaries, letM Ta denote the binary mask
for the intervention-specific supportTa. For interventiona, a deterministic weight vectorw∈R p supported
onT a defines the control-outcome summary
U0,a(w) =w⊤ vec
 
MTa⊙X 0

.(3.3)
The vectorwspecifies which coordinates enter the comparison and how they are aggregated. Because
U0,a(w)is a linear functional ofX T , its conditional distribution is determined by (3.2). A coordinate-
selection weight isolates the control outcome at a specified tensor coordinate, whereas equal weights
yield an average over selected coordinates. 5 The corresponding weighted outcome under interventionais
observed and enters only the subsequent causal analysis; it is not supplied to the conditional generator.

Kong et al.:Conditional Tensor Diffusion
11
Training sample.We learn (3.2) using a finite training sample{X (i)
0 }n
i=1 of complete tensors drawn from
P0. These tensors may correspond to comparable historical periods or external panels observed entirely
under control.
Applying the fixed treatment mask synthetically to each training tensor givesX (i)
T =MT⊙X (i)
0 and
X(i)
C =MC⊙X (i)
0 . This construction produces paired missing and observed control outcomes for learning
the conditional score. For the data used in causal analysis, the observed control outcomesX C are held
fixed and provided to the learned conditional generator, which generates the missing control outcomesXT
conditionally on them. The observed treated outcomes remain outside the generator and enter only the
subsequent causal analysis.
3.2. Masked Conditional Diffusion in the Treated Region
We now develop the masked conditional diffusion underlyingCFT-DIFFfor the tensor partition in (3.1).
Under the unit noise schedule adopted above,α t =e−t/2 andh t = 1−e −t. The forward process perturbs
only the missing outcomesX T , while the observed control outcomesX C remain fixed and condition the
diffusion throughout.
Let{Wt}t≥0 be a tensor-valued Wiener process with independent standard Brownian entries. The forward
diffusion of the missing outcomes is
dXT,t =− 1
2XT,t dt+MT⊙dWt, X T,0 =XT.(3.4)
For every fixedt∈[0,T], the solution of (3.4) has the explicit form
XT,t =αtXT +h 1/2
t (MT⊙Zt), Z t⊥⊥(XT,XC),(3.5)
whereZ t has independent standard Gaussian entries.
LetX T ={X∈R p1×···×pD :MT⊙X=X}be the tensor space supported onT. Conditional onX C,
letP T
t (·|X C) =L(XT,t|XC)denote the conditional distribution ofX T,t on this space, and letp T
t (·|
XC)denote its density with respect to Lebesgue measure over the coordinates in the treated region. The
corresponding conditional score iss t(X|X C) =∇T logpT
t (X|X C)forX∈X T , where∇T differentiates
only with respect to entries onTand pads the coordinates outsideTwith zeros. Consequently,M T⊙st(X|
XC) =st(X|X C)forX∈X T .
With this conditional score, the exact reverse-time diffusion is
dX←
T,u =
1
2X←
T,u +sT−u
 
X←
T,u|XC

du+MT⊙dWu, u∈[0,T−t 0].(3.6)
Here{Wu}u≥0 is a tensor-valued Wiener process with independent standard Brownian entries. Conditional
onXC, ifX←
T,0∼PT
T (·|X C), thenX←
T,u∼PT
T−u (·|X C)andX ←
T,T−t 0∼PT
t0 (·|X C). The conditional score
therefore determines the reverse-time process and is the central object to be learned. Because an unrestricted
tensor score is high dimensional, the next subsection develops a Tucker-structured representation whose
nonlinear component operates only on a low-dimensional core.
3.3. Low-Dimensional Tucker Structure of the Conditional Score
The conditional score in Section 3.2 is a tensor-valued function whose inputs and output are all high dimen-
sional. Estimating and repeatedly evaluating such a function can be prohibitively costly, particularly because
reverse-time generation requires score evaluation at every discretization step. Tucker structure provides a

Kong et al.:Conditional Tensor Diffusion
12
parsimonious representation of large tensors and can substantially reduce the cost of tensor computation
(Kolda and Bader 2009). We, therefore, posit a low-Tucker-rank model for the complete control-outcome
(control-world) tensor. This structure exploits dependence across tensor modes, organizes score learning and
generation around a low-dimensional core, and yields the conditional-score representation derived below.
Recall thatp= QD
d=1pd, and definepβ =QD
d=1pβd
d , whereβd∈[0,1]indexes factor strength along mode
d.6 For compactness, writeF× D
d=1Ad :=F× 1A1×2···× DAD. We assume
X0 =F× D
d=1Ad +p−β/2E, A ⊤
dAd =Ird, d∈[D].(3.7)
HereF∈R r1×···×rD is the Tucker core,Ad∈Rpd×rd is the loading matrix for moded, andEis idiosyncratic
tensor noise. The full dimension isp, whereasr= QD
d=1rd is the intrinsic core dimension. The scaling
p−β/2 allows factor strength to increase with the tensor dimensions.
REMARK3.1 (CONNECTION WITH VECTOR AND MATRIX FACTOR MODELS).The Tucker representa-
tion nests familiar factor models as special cases. WhenD= 1, (3.7) becomesX 0 =A 1F+p −β/2E, where
F∈R r1 is a vector of latent factors andA 1 contains their loading vectors, as in the standard vector fac-
tor model (Bai 2003, Bai and Ng 2023). WhenD= 2, it becomesX 0 =A 1FA⊤
2 +p−β/2E, whereA 1
andA 2 are the row and column loading matrices, respectively, andF∈R r1×r2 is the matrix-valued factor.
This is the bilinear, or two-way, matrix factor specification (Wang et al. 2019, Yu et al. 2023, Yuan et al.
2023, Zhang et al. 2025, He et al. 2025). TheD-way formulation retains this loading-factor interpreta-
tion while representing the structured component throughrcore coordinates rather thanpfull coordinates.
Consequently, the proposed framework also covers counterfactual recovery with vector- or matrix-valued
outcomes by takingD= 1orD= 2, respectively.
ASSUMPTION3.1(Control-world tensor factor model).The complete control-world tensor follows
(3.7). The vectorized coref= vec(F)∈R r has densityp core, mean zero, and finite second moment.
It is independent ofe= vec(E), wheree∼N(0,Σ ⊗
e )andΣ ⊗
e = Σe,D⊗···⊗Σ e,1, withΣ e,d =
diag(σ2
d1,...,σ 2
dpd)and0<σ 2
min≤σ 2
dj≤σ 2
max<∞ford∈[D], j∈[p d].
Assumption 3.1 concerns the joint distribution of the control outcomes; no factor model is imposed on
the outcomes under active interventions. The separable diagonal covariance makes the conditional score
under the treatment mask analytically tractable, while the uniform variance bounds rule out degenerate
coordinates. To expose the resulting score structure, letA ⊗ =AD⊗···⊗A 1 and define the idiosyncratic
variance tensorQσ by(Q σ)i1,...,iD =QD
d=1σ2
did.
The construction below combines the noised missing outcomes and the observed control outcomes as two
measurements of the same latent core. Conditional onf,X T,t is a Gaussian measurement of the scaled core
αtfin the treated region, with coordinatewise variancesh t +α 2
tp−βQσ. The observed control outcomesXC
measurefonC, or equivalentlyα tfafter rescaling byα t. Because the two measurements are conditionally
independent, they can be combined by precision-weighted least squares in the core space.
Define their coordinatewise precision tensors by
WT,t =MT⊘
 
ht1+α 2
tp−βQσ

,W C =MC⊘
 
p−βQσ

.
Each tensor assigns the inverse conditional variance to coordinates in its corresponding support and zero
weight elsewhere. Projecting these precisions onto the Tucker loading space gives the core-level information

Kong et al.:Conditional Tensor Diffusion
13
matrices
HT,t =A⊤
⊗ diag{vec(WT,t )}A⊗, H C =A⊤
⊗ diag{vec(WC)}A⊗.
BecauseMT andMC partition the tensor coordinates andA⊤
⊗A⊗ =Ir, the combined core-level precision
matrix is positive definite. We therefore define
Vt =
 
HT,t +α−2
t HC
−1
.
The key step is to combine the two precision-weighted encoder outputs into a single core statistic:
gt =Vt

vec


(WT,t⊙XT,t )×D
d=1A⊤
d| {z }
missing-outcome encoder


 +α−1
t vec


(WC⊙XC)×D
d=1A⊤
d| {z }
observed-outcome encoder




,(3.8)
LetG t = Tucker(gt), whereTucker(g) := reshape{g; (r1,...,r D)}. Standard Gaussian least-squares cal-
culations then giveg t|f∼N(α tf,Vt). Thus,g t is anr-dimensional sufficient statistic for the scaled core
signalαtf: it pools the information retained in the noised missing outcomes with the undiffused information
in the observed control outcomes.
PROPOSITION3.1(Conditional Tucker score decomposition).Under Assumption 3.1, for everyt∈
[t0,T], the conditional tensor score satisfies
st(XT,t|XC) =W T,t
|{z}
treated-region precision
⊙




E(αtF|G t)| {z }
core regression
×D
d=1Ad
| {z }
Tucker decoder


 −XT,t
| {z }
skip connection

. (3.9)
The score is supported onTand is padded with zeros onC.
The statisticg t pools the noised outcomes in the treated region and the observed control outcomes accord-
ing to their precisions. Its conditional core mean is decoded to the original tensor coordinates, yielding a
precision-weighted denoising score in the treated region, while the observed control outcomes remain fixed.
3.4.CFT-DIFF: Estimation and Generation
Masked Tucker score class.Proposition 3.1 depends on the unknown loading matrices, idiosyncratic vari-
ances, and conditional core regression. To obtain an estimable score class, we replace them with trainable
counterparts. LetΓ ={Γ d}D
d=1 denote candidate Tucker loading matrices satisfyingΓ⊤
d Γd =Ird ford∈[D],
and letω={ω dj}denote candidate idiosyncratic variances satisfyingσ 2
min≤ω dj≤σ 2
max ford∈[D]and
j∈[p d]. For any(Γ,ω), letW T,t (ω),WC(ω),V t(Γ,ω), andG t(Γ,ω)denote the quantities obtained from
the precision-weighted construction defined in Section 3.3 after replacing(A d,σ 2
dj)with(Γ d,ωdj). Thus,
Gt(Γ,ω)is the candidate Tucker-core summary of(X T,t,XC), withr= QD
d=1rd coordinates.
LetZ θ :Rr1×···×rD×[t 0,T]→R r1×···×rD be a Core-Net. The corresponding score network is
sΓ,ω,θ(XT,t,XC,t) =WT,t (ω)⊙

Zθ (Gt(Γ,ω),t)× D
d=1 Γd−XT,t

. (3.10)
Forg∈R r, defineζ θ(g,t) = vec [Zθ(Tucker(g),t)]. LetF core(L,m,J,K,κ,γ g,γt)denote the class of
feed-forward ReLU networks with depth at mostL, hidden-layer width at mostm, at mostJnonzero
parameters, and parameter magnitudes bounded byκ. The constantsK,γ g, andγt bound the network output

Kong et al.:Conditional Tensor Diffusion
14
and its Lipschitz variation in the core and time arguments, respectively. A formal definition is provided in
Appendix EC.3.2. For a fixed constantCV >0, themasked Tucker classis
SMT =

sΓ,ω,θ : Γ⊤
d Γd =Ird, d∈[D],σ 2
min≤ωdj≤σ 2
max,
sup
t∈[t0,T]
∥Vt(Γ,ω)∥ op≤CV, ζ θ∈F core(L,m,J,K,κ,γ g,γt)

.
The bound onV t(Γ,ω)controls the amplification induced by aggregating the missing-outcome and
observed-outcome branches in the core space, while the constraint onζ θ controls the complexity of the
nonlinear core regression. As displayed in (3.10), each score evaluation pools the two branches in the core
space, applies the Core-Net, decodes the result through the mode-wise loadings, and forms the precision-
weighted residual onT.
Score estimation.The Gaussian transition in (3.5) has treated-region scoreh −1
t (αtXT −XT,t ) =
−h−1/2
t (MT⊙Zt). Applying the conditional denoising identity from Section 2.2, the population masked
score-matching loss is
Lmask(s) = 1
T−t 0
Z T
t0
E
h

s(XT,t,XC,t)−h −1
t (αtXT−XT,t )

2
F
i
dt.
The expectation is over a complete control-outcome tensor and its forward perturbation. Its population
minimizer iss t(XT,t|XC). For the training sample introduced in Section 3.1, define
bs∈arg min
s∈SMT
bLmask(s), bLmask(s) = 1
n
nX
i=1
ℓ(X(i)
0 ;s),
ℓ(X0;s) = 1
T−t 0
Z T
t0
EXT,t|XT
h

s(XT,t,XC,t)−h −1
t (αtXT−XT,t )

2
F
i
dt.
(3.11)
Stochastic training samples a training tensor, a diffusion time, and Gaussian perturbation noise. The same
fixed mask is used throughout, so the learned score is aligned with the missing-region pattern used in
conditional generation.
Conditional generation.Given the observed control outcomesX C,CFT-DIFFuses the learned scorebsin
the reverse dynamics (3.6) and initializes the missing-outcome tensor from its large-TGaussian approxi-
mation:
dbX←
T,u =
1
2
bX←
T,u +bs
 bX←
T,u,XC,T−u

du+MT⊙dWu, u∈[0,T−t 0], bX←
T,0 =MT⊙Z 0,
(3.12)
withvec(Z 0)∼N(0,I p). The output bX←
T,T−t 0 is one generated sample of the missing control outcomes
in the treated region. Conditional on the observed control outcomes, denote its early-stopped distribution
by bPT
t0 (·|X C) :=L( bX←
T,T−t 0|XC). By the support convention following (3.1), bX←
T,T−t 0 is zero onC.
Consequently,XC + bX←
T,T−t 0 is the corresponding completed control-outcome tensor. Independent runs of
(3.12) yield samples from bPT
t0 (·|X C).
3.5. Intrinsic-Dimensional Guaranties for Conditional Score Learning
The Tucker representation reduces the nonlinear component of the conditional score to ther-dimensional
core space. Its statistical analysis depends on two features: concentration of the latent core and regularity of
the conditional core regression. We state these conditions below.

Kong et al.:Conditional Tensor Diffusion
15
Recall from (3.8) thatg t|f∼N(α tf,Vt). ForR≥1, defineG R ={g∈R r :∥g∥∞≤R}and let
ξ(g,t) :=E(α tf|g t =g) =
Z
αtfϕ(g;α tf,Vt)pcore(f) df
Z
ϕ(g;αtf,Vt)pcore(f) df
,
whereϕ(·;µ,V)is the Gaussian density with meanµand covarianceV. This vector-valued map is the core
representation of the conditional mean in Proposition 3.1:E(α tF|G t) = Tucker{ξ(gt,t)}.
ASSUMPTION3.2(Sub-gaussianlity of the latent core).LetΣ f = Cov(f). The eigenvalues ofΣ f are
bounded away from zero and infinity. Moreover, there exist constantsB f,C 1,C 2>0such that, whenever
∥f∥ 2≥Bf,p core(f)≤(2π) −r/2C1 exp
 
−C2∥f∥ 2
2/2

.
Assumption 3.2 is a standard concentration condition for light-tailed factor models and is rather mild.
The covariance bounds only rule out degenerate or excessively dispersed factor directions, while the density
bound controls the probability of extreme core realizations. Together with the Gaussian noise ing t|f, this
condition ensures thatgt lies inGR with high probability for the radiusRchosen below. The next assumption
controls the conditional core regression on this high-probability region.
ASSUMPTION3.3(Regularity of the conditional core regression).For the radiusRunder considera-
tion, suppose that, uniformly overt∈[t 0,T],V t⪯v maxIr for a constantv max <∞. Assume thatξis
Lg-Lipschitz ingandL t-Lipschitz intonG R×[t 0,T]. In addition,K 0 := 1 + supt∈[t0,T]∥ξ(0,t)∥ 2<∞.
Assumption 3.3 is imposed only on ther-dimensional conditional core regression, rather than on the full
p-dimensional score. The bound onV t uniformly limits the conditional variance ofg t|fin every core-
space direction. The Lipschitz conditions ensure thatξcan be approximated uniformly by the Core-Net
onG R×[t 0,T], whileK 0 anchors the magnitude of the regression at the origin. Because these restrictions
are required only in a high-probability region, they are weaker than the corresponding global smoothness
conditions.
For example, iff∼N(0,Σ f), thenξ(g,t) =α 2
tΣf
 
α2
tΣf +Vt
−1
g. In this case,ξis linear ingand
K0 = 1, and the Lipschitz condition ingfollows directly. Meanwhile, the condition intholds wheneverα t
andV t vary smoothly over[t 0,T]. WhenV t is small relative toα 2
tΣf, the statisticg t is highly informative
aboutα tf, andξ(g,t)is close tog.
Approximation in the core space.A central implication of Proposition 3.1 is that nonparametric score
approximation can be carried out after Tucker compression. All masking, precision weighting, and mode-
wise transformations are represented exactly. The only function to be approximated is the conditional core
regressionξ. The result below quantifies this reduction: the nonlinear approximation depends on thercore
coordinates and time, rather than on thepentries of the original tensor.
For an approximation toleranceϵ∈(0,1), defineR ϵ =C R
p
log{ctailr/(t0ϵ)}, whereC R andc tail are
sufficiently large constants. This radius contains the core statistic with sufficiently high probability, so the
Core-Net need only approximateξaccurately onG Rϵ×[t 0,T].
Consider a Core-Net class whose complexity parameters satisfy
m=O
 
(1 +LgRϵ)r(1 +TLt)ϵ−(r+1)
, K=O(K 0 +LgRϵ), L=O(log(K/ϵ) + 1),
J=O(mL), κ=O
 
max
 
K0 +LgRϵ,TL t,T −1
, γ g =CrLg, γ t =CrLt,
(3.13)

Kong et al.:Conditional Tensor Diffusion
16
whereC r depends only on the core dimension.
THEOREM3.1(Conditional score approximation).Suppose Assumptions 3.1 and 3.2 hold, and
Assumption 3.3 holds withR=R ϵ. Let0<t 0≤1,T >t 0, andC V≥v max, and configure the Core-Net
class according to(3.13). LetA • = (A1,...,A D)denote the population loading matrices, and letω 0 =
(σ2
dj)d,j denote the population idiosyncratic variances. Then there exists a Core-Net parameter set ¯θsuch
thats A•,ω0,¯θ∈S MT and, for everyt∈[t 0,T],
EXC EXT,t|XC
h

sA•,ω0,¯θ(XT,t,XC,t)−s t(XT,t|XC)

2
F
i
≤h−2
t (√r+ 1)2ϵ2.
Theorem 3.1 isolates the approximation benefit of the Tucker score representation. At the population
loading spaces and idiosyncratic variances, approximating thep-dimensional conditional score reduces to
approximatingξonR r×[t 0,T]. Accordingly, the network width in (3.13) scales asϵ −(r+1). The exponent
r+ 1is the input dimension ofξ:rcore coordinates and one scalar time input. It does not involve the full
dimensionp. The factorh −2
t reflects the increasing sensitivity of the score near the data distribution and
explains the use of the early-stopping timet 0>0. The next result incorporates estimation of the loading
spaces and variance parameters from the training samples.
Learning from finitely many training tensors.The preceding approximation result fixes the loading
spaces and idiosyncratic variances at their population values. We now allow these components, together
with the conditional core regression, to be learned from the training sample. The resulting bound separates
the cost of learning the nonlinear core map from that of estimating the mode-wise loading spaces.
DefinepT = tr(MT ),dT,β =r+p Tp−β, andp max = maxd∈[D]pd. Herep T is the number of missing
control outcomes. The quantitydT,β combines thercore coordinates with the aggregate scalep Tp−β of the
idiosyncratic component on that support, whilep max is the largest mode dimension. For the sample sizen,
setδ n = (r+ 12) log log(n)/{2 log(n)}andϵ=n −(1−δn)/(r+5).
THEOREM3.2(Conditional score generalization).Suppose Assumptions 3.1 and 3.2 hold, and suppose
Assumption 3.3 holds onG Rϵ×[t 0,T]. Configure the Core-Net class according to(3.13)at the value ofϵ
specified above, and chooseC V≥v max. Suppose thatD, the mode ranks(r 1,...,r D),L g,L t, andK 0 are
fixed. For fixed constantsc 0,cT >0and all sufficiently largen, assumec −1
0 p−β<t 0≤1andT−t 0≥cT .
Then, with probability at least1−1/nover the training sample,
1
dT,β (T−t 0)
Z T
t0
EXC EXT,t|XC

∥bs(XT,t,XC,t)−s t(XT,t|XC)∥2
F

dt= eO
 1
t0
+T
n
n− 2−2δn
r+5 +p maxn−r+3+2δn
r+5
o
.
(3.14)
The notation eOsuppresses fixed model constants and polylogarithmic factors inn,p max,t−1
0 ,ϵ−1, andα−1
T .
The left-hand side of (3.14) is the time-integrated prediction error of the learned conditional score, nor-
malized by the effective dimensiondT,β . The two terms in the bound correspond to distinct learning tasks.
The first is the cost of estimating the nonlinear conditional core regressionξ; becauseδn→0, its leading rate
isn−2/(r+5) up to logarithmic factors. The second is the cost of estimating the mode-wise loading spaces. It
depends onp max rather than on the vectorized dimensionp, and vanishes providedp maxn−r+3+2δn
r+5 →0.
The size of the missing region enters only throughdT,β =r+p Tp−β. In the strong-signal regimepT≲pβ,
this effective dimension remains bounded when the mode ranks are fixed. Thus, the nonlinear component
of score learning is governed by the Tucker-core dimension, while the cost of recovering the full loading
structure depends only on the largest individual mode.

Kong et al.:Conditional Tensor Diffusion
17
Section 4 translates this score bound into recovery guaranties for the conditional distribution of the miss-
ing control outcomes.
4. Counterfactual Distribution Recovery
This section shows how conditional-score error propagates to the generated distribution and establishes
recovery and prediction-interval guaranties for the missing control outcomes and their weighted summaries.
4.1. A Score-to-Distribution Transfer Bound
Recall thatP T
t (·|X C)is the conditional distribution of the forward-diffused missing outcomesX T,t ,
whereas bPT
t0 (·|X C)is the conditional distribution generated by the trained reverse-time process (3.12).
Both distributions are defined over thepT coordinates in the treated region, wherepT = tr(MT ); att 0>0,
they admit densities onRpT . Recall also thatp max = maxd∈[D]pd.
The following result isolates the mechanism by which conditional-score error affects the generated dis-
tribution. It applies to a fixed realization of the training sample and therefore treats the trained scorebsas
given.
PROPOSITION4.1(Score-to-distribution transfer).Suppose that the reverse SDE driven bybsis well
defined and that
Z T
t0
EXC EXT,t|XC∥bs(XT,t,XC,t)−s t(XT,t|XC)∥
2
F dt<∞.
Then
EXC
h
KL

PT
t0 (·|X C)

bPT
t0 (·|X C)
i
≤1
2
Z T
t0
EXC EXT,t|XC∥bs(XT,t,XC,t)−s t(XT,t|XC)∥
2
F dt
+EXC

KL
 
PT
T (·|X C)

N(0,I pT )

.
(4.1)
Under Assumption 3.1, for fixedD, there exist constantsC,c>0such that
EXC

KL
 
PT
T (·|X C)

N(0,I pT )

≤Cexp(−cT){r+p T log(1 +pmax)}.(4.2)
The two terms in (4.1) correspond to the two approximations made by the implementable sampler. The
integral accumulates the error introduced along the reverse-time process when the population score is
replaced bybs. The second term arises from initialization. The exact reverse-time process would start from
the conditional terminal distributionP T
T (·|X C), which is unknown, whereas the implementable sampler
starts fromN(0,I pT ). Under the Ornstein–Uhlenbeck forward process, the contribution of the initial miss-
ing outcomes diminishes, andPT
T (·|X C)approaches the standard normal distribution asTincreases. Bound
(4.2) makes this approximation precise: its contribution decays exponentially inT, up to the displayed
dimension factor.7 Consequently, for sufficiently largeT, the initialization approximation contributes little
to the error in the generated distribution, which is then governed primarily by the integrated score error.
Proposition 4.1 compares the true and generated distributions at the same early-stopping timet 0. This
common-time comparison excludes the error caused by stopping before time zero. The remaining differ-
ence betweenP T
t0 (·|X C)and the original target distributionP T
0 (·|X C)is the early-stopping error, which
vanishes ast 0↓0.

Kong et al.:Conditional Tensor Diffusion
18
4.2. Recovery of the Missing-Outcome Distribution
We now combine the conditional-score bound in Theorem 3.2 with Proposition 4.1 to establish recovery of
the generated distribution. Recall thatd T,β =r+p Tp−β is the effective dimension of the missing region.
Recall thatδ n = (r+12) log log(n)
2 log(n) andϵ=n − 1−δn
r+5 , and definea n = 1−δn
3r+15 . Under the choices oft 0 andT
stated below, the polylogarithmic factors suppressed in Theorem 3.2 are bounded byL n = (1 + log(n) +
log(pmax))cL for a sufficiently large fixed constantcL>0. Define
Rn =Ln

n
− 5(1−δn)
6(r+5) +√pmaxn
− 3r+8+7δn
6(r+5)

.(4.3)
The exponentcL only records the logarithmic factors hidden by theeOnotation and is not an implementation
parameter.
THEOREM4.1(Recovery of the missing-outcome distribution).Suppose Assumptions 3.1 and 3.2 hold
and Assumption 3.3 holds onG Rϵ×[t 0,T]. Configurebsas in Theorem 3.2 with the value ofϵdisplayed
above. Suppose thatD, the mode ranks(r 1,...,r D),L g,L t, andK 0 are fixed. Chooset 0≍n−an,T=
CT{log(n) + log(pmax)}, and suppose thatp β≥Cβnan, whereCT andC β are sufficiently large constants.
Then there exists an eventAn, measurable with respect to the training sample, such thatP(A n)≥1−1/n
and, onA n,
EXC
h
KL

PT
t0 (·|X C)

bPT
t0 (·|X C)
i
≤CdT,β R2
n,(4.4)
withR n defined in(4.3). Consequently,
EXC
h
TV

PT
t0 (·|X C),bPT
t0 (·|X C)
i
≤Cd 1/2
T,β Rn.(4.5)
Theorem 4.1 converts the conditional-score guaranty in Theorem 3.2 into a recovery guaranty for the
generated conditional distribution. The first component ofRn arises from learning the nonlinear regression
in ther-dimensional core, whereas the second arises from estimating the mode-wise loading spaces and
depends onp max rather than on the full dimensionp. The factord T,β captures the idiosyncratic variation
remaining in the treated region. In the strong-signal regimep T≲p β, this factor remains bounded when
the mode ranks are fixed. More generally, ifd T,β R2
n→0, the average conditional KL divergence in (4.4)
converges to zero; (4.5) then gives the same conclusion for the average conditional total variation distance.
Hence, the generated conditional distribution consistently recovers the early-stopped target distribution
PT
t0 (·|X C)under both metrics.
The prescribed choices oft 0 andTcontrol different approximation errors. The terminal timeT=
CT (log(n) + log(pmax))grows only logarithmically with the sample size and the largest mode dimension.
Substituting this choice into (4.2) changesexp(−cT)inton −cCTp−cCT
max . BecauseDis fixed, a sufficiently
largeC T makes the Gaussian-initialization error negligible relative to the score-learning error. The early-
stopping timet 0 has a different role. Choosingt 0≍n−an allows the perturbation of the original target
to vanish while preventing the factort −1
0 in the score bound from increasing too rapidly. The condition
pβ≥Cβnan ensures that this choice remains above the idiosyncratic-noise scale required by Theorem 3.2.
Becauset 0→0, the forward coupling in (3.5) implies thatP T
t0 (·|X C)approaches the original conditional
distribution of the missing control outcomesP T
0 (·|X C).
REMARK4.1 (IMPLEMENTATION IMPLICATIONS OF THE RECOVERY RATE).The recovery bound also
clarifies how statistical accuracy depends on the diffusion horizon and the intrinsic dimensions of the prob-

Kong et al.:Conditional Tensor Diffusion
19
lem. The early-stopping timet 0 balances approximation and estimation. It should decrease with the training
sample size, witht 0≍n−an providing a theoretically justified benchmark. Movingt 0 closer to zero leaves
less perturbation in the target distribution but makes the score more difficult to estimate near the data distri-
bution. At the other end of the diffusion path, a terminal timeTthat grows logarithmically is sufficient for
the forward-diffused missing region to approach a standard Gaussian. The bound further shows that recov-
ery depends onr,p max, anddT,β rather than on the full dimensionp. Because nonlinear score learning is
governed byr, network capacity is most effectively allocated to the Tucker core. When the term involving
pmax dominates, estimation of the loading spaces becomes the principal bottleneck. A larger missing region
or a weaker factor signal increasesdT,β and therefore requires a larger training sample to attain comparable
recovery accuracy.
4.3. Recovery of Weighted Counterfactual Summaries
Theorem 4.1 concerns the entire conditional distribution of the missing control outcomes in the treated
region. Most causal analyzes, however, concern selected entries or averages of these outcomes. We therefore
consider prespecified weighted summaries of the recovered control outcomes.
For interventiona, letMTa denote the binary mask for the intervention-specific regionTa. A deterministic
weight vectorw∈R p supported onT a defines the control-outcome summary
U0,a(w) =w⊤ vec
 
MTa⊙X 0

.(4.6)
The vectorwspecifies which coordinates enter the comparison and how they are aggregated. Because
U0,a(w)is a linear functional ofX T , its conditional distribution is determined by (3.2). A coordinate-
selection weight isolates the control outcome at a specified tensor coordinate, whereas equal weights yield
an average over selected coordinates.8
To accommodate causal analysis involving several tensors, letn e tensors be used in the causal analysis,
hereafter called the analysis tensors. For analysis tensorℓ, letX (ℓ)
C denote its observed control outcomes
andX (ℓ)
T its missing control outcomes in the treated region, with conditional distributionX (ℓ)
T |X (ℓ)
C ∼
PT
0
 
·|X (ℓ)
C

forℓ= 1,...,n e. The collectionX 1:ne
C =
 
X(1)
C ,...,X (ne)
C

contains the observed control
outcomes supplied to the conditional generator. These analysis tensors are separate from the training sample
of complete control-outcome tensors used to estimate the score. They are independent draws from the
population distribution and are independent of the training sample.
For a deterministic vectorw=M Tw∈R p, define the control-outcome summary for the analysis tensorℓ
byU w,ℓ,0 =w⊤ vec
 
X(ℓ)
T

. If the comparison concerns interventionaandwis supported onT a, thenU w,ℓ,0
is the analysis-tensor counterpart ofU 0,a(w)in (4.6). When a causal comparison combines several analysis
tensors, define their average control-outcome summary as follows:V ne,w,0 = 1
ne
Pne
ℓ=1Uw,ℓ,0. Heren e is
the number of analysis tensors entering the downstream comparison, rather than the number of generated
samples. Thus,Vne,w,0 is directly interpretable as an average missing control outcome and can be compared
with the corresponding average observed outcome under treatment.
For each analysis tensorℓ, let bX(ℓ)
T,t 0 := bX←,(ℓ)
T,T−t 0 be generated conditional onX (ℓ)
C by the reverse-time
process (3.12) driven by the estimated score. Then bX(ℓ)
T,t 0∼ bPT
t0 (·|X (ℓ)
C ), and the generated counterpart
ofV ne,w,0 isbVne,w,t0 = 1
ne
Pne
ℓ=1w⊤ vec(bX(ℓ)
T,t 0). Conditional onX 1:ne
C and the learned score, the generated
vector follows the product conditional distributionNne
ℓ=1
bPT
t0 (·|X (ℓ)
C ). LetF tr =σ(X (1)
0 ,...,X (n)
0 )denote

Kong et al.:Conditional Tensor Diffusion
20
the sigma-field generated by the training sample. For a fixed realization ofFtr belonging toAn, the learned
score and its induced conditional distributions are fixed; this conditioning is suppressed below. The follow-
ing result usesd BL to compare the target and generated conditional distributions of the weighted aggregate.
BecauseV ne,w,0 is an arithmetic average, its distribution may contract mechanically asn e increases. We
therefore state distributional recovery on the fluctuation scale√neVne,w,0. This deterministic normalization
is neither a studentization nor an appeal to a central limit theorem.
COROLLARY4.1(Recovery of weighted counterfactual summaries).Under the conditions of Theo-
rem 4.1, for everyne∈Nand every deterministicw=M Tw, onA n,
EX1:ne
C
dBL
h
L{√neVne,w,0|X 1:ne
C },L{√nebVne,w,t0|X 1:ne
C }
i
≤C∥w∥ 2n−an/2 +C√ned1/2
T,β Rn.
(4.7)
The first term in (4.7) bridges the original and early-stopped distributions. Independence and center-
ing keep the mean-square forward perturbation of √neVne,w,0 of order∥w∥ 2
2t0.9 The second term is
the conditional-distribution estimation error: relative entropy adds over then e product components, and
Pinsker’s inequality yields the factor√ne. Thus, ifn e andw=w n vary withn, consistency follows when
∥wn∥2n−an/2→0and √ned1/2
T,β Rn→0. The targetV ne,w,0 itself remains on the average-outcome scale
used below.
4.4. Counterfactual Prediction Intervals
Recovering the conditional distribution also provides quantiles and prediction intervals for the missing con-
trol outcomes. With suitable weights, the same construction applies to averages used in treatment-effect
comparisons. Combining such an interval with the corresponding observed treated outcome yields an inter-
val for the resulting treatment-effect contrast.
We next establish the coverage of these intervals. Although Corollary 4.1 controls the bounded–Lipschitz
distance between the weighted-summary distributions, interval coverage is not a continuous functional of
the underlying distribution. We therefore impose a mild anti-concentration condition. Suppose that, for
almost everyX 1:ne
C , the conditional density of √neVne,w,0 is uniformly bounded over its argument by a
finite constantM n,ne,w. Equivalently, the conditional density ofV ne,w,0 is bounded by√neMn,ne,w. This
condition prevents excessive probability mass from accumulating near a prediction-interval endpoint.
For a realizationx= (x (1)
C ,...,x (ne)
C )of the observed control outcomes, let bFx denote the conditional
distribution function of bVne,w,t0. The density condition excludes the degenerate choicew= 0. Because the
reverse diffusion is nondegenerate on the positions in the treated region, bFx is continuous. Definebqx(u) =
inf{v: bFx(v)≥u}foru∈(0,1). We report intervals on the average-outcome scale. Multiplying both the
statistic and the interval by√ne leaves the coverage event unchanged. The central interval induced by the
estimated conditional distribution is
bIne,w,1−α(x) = [bqx(α/2),bqx(1−α/2)],0<α<1.(4.8)
In computation, let
n
bV (b)
ne,w,t0
oB
b=1
beBindependent draws from the estimated conditional distribution. Let
bq(B)
x (u)denote their empiricalu-quantile and define bI(B)
ne,w,1−α(x) =

bq(B)
x (α/2),bq(B)
x (1−α/2)

. Also, let
Fgen
B =F tr∨σ{bV (1)
ne,w,t0,..., bV (B)
ne,w,t0}.

Kong et al.:Conditional Tensor Diffusion
21
COROLLARY4.2(Coverage of counterfactual prediction intervals).Under the conditions of Theo-
rem 4.1 and the conditional-density bound above, onAn,
EX1:ne
C
P
n
Vne,w,0∈bIne,w,1−α(X1:ne
C )
X1:ne
C ,F tr
o
−(1−α)

≤C√ned1/2
T,β Rn +C
 
Mn,ne,w∥w∥2
2/3
n−an/3.
(4.9)
Moreover,
EX1:ne
C
Egen|X1:ne
C ,Ftr
P
n
Vne,w,0∈bI(B)
ne,w,1−α(X1:ne
C )
X1:ne
C ,F gen
B
o
−(1−α)

≤C√ned1/2
T,β Rn +C
 
Mn,ne,w∥w∥2
2/3
n−an/3 +CB−1/2.
(4.10)
Here the inner expectation is taken over the finite generation sample, conditional on the observed control
outcomes and the training sample.
The three terms in (4.10) arise from recovery of the early-stopped distribution, the early-stopping approx-
imation, and finite generation, respectively. On the fluctuation scale, the forward coupling perturbs the target
byO(∥w∥ 2
√t0); combining this bound withM n,ne,w gives the second term. The final term follows from
replacing the quantiles of the estimated conditional distribution with empirical quantiles based onBcondi-
tional draws (Massart 1990). Hence, the finite-generation interval is asymptotically calibrated whenever
√ned1/2
T,β Rn→0, M n,ne,w∥w∥2n−an/2→0, B→∞.
These intervals concern unobserved counterfactual realizations rather than a fixed population parameter.
BecauseVne,w,0 is an arithmetic average, the interval endpoints retain the units relevant for an average causal
comparison. The fluctuation-scale density condition is compatible with this presentation because common
scaling leaves coverage unchanged. The result does not use an additional Gaussian approximation or require
estimation of an asymptotic variance; its quantiles are obtained directly from conditional draws generated
byCFT-DIFF.
The control-world intervals can be translated directly into intervals for treatment effects on the analysis
tensors. For interventiona, letwbe supported onT a and define the corresponding average of the observed
treated outcomes byV obs
ne,w,a = 1
ne
Pne
ℓ=1w⊤ vec
 
MTa⊙Y obs,(ℓ)
. The associated weighted sample-average
counterfactual contrast is
τne,w,a = 1
ne
neX
ℓ=1
w⊤ vec
h
MTa⊙

Y obs,(ℓ)−X (ℓ)
T
i
=V obs
ne,w,a−Vne,w,0. (4.11)
With equal weights over the relevant treated coordinates, this quantity is the sample average treatment effect
for the analysis tensors.
Because the treated outcomes are observed, a prediction interval for the contrast in (4.11) is obtained by
translating the interval forVne,w,0. In particular, the interval induced by (4.8) is
bIτ,ne,w,a,1−α(x) =

V obs
ne,w,a−bqx(1−α/2),V obs
ne,w,a−bqx(α/2)

.
Its finite-Bcounterpart is obtained by replacingbqx withbq(B)
x . The reversal of the quantile endpoints reflects
that the treatment effect is the observed treated outcome minus the unobserved control outcome. Treating
the realized treated summary as fixed, this transformation preserves the conditional coverage guarantee
of the underlying control-world interval and requires no model for the treated-outcome distribution. The
resulting interval quantifies counterfactual uncertainty in the weighted sample-average treatment effect.10

Kong et al.:Conditional Tensor Diffusion
22
5. Simulation Study
This section evaluates the finite-sample performance ofCFT-DIFFin recovering both missing control out-
comes and their conditional distribution. We vary the size of the missing region and the strength of the latent
factor structure and compareCFT-DIFFwith established point-recovery methods and two nested diffusion
benchmarks. The main text reports the more challenging setting,β= 0.50; results forβ= 0.75are provided
in Appendix EC.4.
5.1. Simulation Setting
For the tensor design, we setβ 1 =β 2 =βand generate64×64control-world matrices from the bilin-
ear factor modelX=A 1FA⊤
2 +p−β/2E, whereFis a16×16Gaussian factor matrix andEcontains
independent Gaussian idiosyncratic noise. Each replication contains 360 complete training matrices and 12
independently generated test matrices.
For each evaluation matrix, we remove a contiguous rectangular block containing approximately 25%,
50%, or 75% of its entries. The remaining entries are the observed control outcomes supplied to the methods,
and recovery is evaluated only in the missing region. Because the data-generating process is Gaussian, the
exact conditional distribution of the missing outcomes given the observed control outcomes is available and
provides a benchmark for distributional recovery.
We compareCFT-DIFFwith five competing point-recovery methods, organized into causal panel esti-
mators and matrix/tensor completion methods. The first group includes difference-in-differences (DID),
synthetic control (SC), and synthetic difference-in-differences (SDID) (Arkhangelsky et al. 2021). The sec-
ond includes nuclear-norm matrix completion (NMC) (Athey et al. 2021) and tensor factor imputation (TFI)
based on the Tucker factor model of Cen and Lam (2025). All methods use the same observed entries and
are evaluated on the same missing regions.
To distinguish the sources of performance gains, we construct two nested diffusion benchmarks. Con-
volutional Diffusion (CONV-DIFF) replaces the structured score network with a conventional convolutional
U-Net and learns directly in the full matrix space. Tucker Diffusion (TUCKER-DIFF) employs the Tucker-
U-Net architecture, thereby exploiting multilinear low-rank structure without the masked conditional con-
struction ofCFT-DIFF. Our method combines Tucker-based dimension reduction with conditioning on the
observed control outcomes through the treatment mask. This nested design separates the gains from multi-
linear structure and conditional generation.
The five competing methods provide point estimates. ForCONV-DIFF,TUCKER-DIFF, andCFT-DIFF, the
mean of the generated draws serves as the point estimate, while the draws themselves provide an esti-
mated conditional distribution. Point recovery is evaluated by mean absolute error (MAE) and root mean
squared error (RMSE). Distributional recovery is evaluated by the energy score and continuous ranked
probability score (CRPS), together with the coverage and width of 90% intervals, the interval score (IS),
and the weighted interval score (WIS). Results are averaged over five independent simulation replications.
Appendix EC.4.1 provides the complete data-generating process, implementation details, and metric defi-
nitions.

Kong et al.:Conditional Tensor Diffusion
23
5.2. Simulation Results
We first examine counterfactual recovery performance as the missing rate increases. Table 1 reports point,
distributional, and interval recovery at missing rates of 25%, 50%, and 75%. These designs progressively
reduce the observed control outcomes and therefore assess how recovery changes as less conditioning infor-
mation remains available.
Table 1Counterfactual recovery across missing rates (β= 0.50).
Point Recovery Distributional Recovery Interval Recovery
Method MAE RMSE Energy CRPS Coverage Width IS WIS
Panel A: Missing Rate= 25%
NMC0.0588 (0.0042) 0.0740 (0.0054) – – – – – –
DID0.1688 (0.0129) 0.2170 (0.0169) – – – – – –
SC0.0533 (0.0035) 0.0674 (0.0045) – – – – – –
SDID0.1172 (0.0075) 0.1502 (0.0095) – – – – – –
TFI0.0586 (0.0035) 0.0745 (0.0045) – – – – – –
CONV-DIFF0.1191 (0.0075) 0.1527 (0.0095) 3.4293 (0.2163) 0.0851 (0.0054) 0.8831 (0.0120) 0.4785 (0.0210) 0.6469 (0.0398) 0.0640 (0.0041)
TUCKER-DIFF0.0497 (0.0027) 0.0637 (0.0033) 1.4746 (0.0770) 0.0355 (0.0019) 0.9614 (0.0101) 0.2745 (0.0169) 0.2931 (0.0161) 0.0272 (0.0015)
CFT-DIFF0.0371 (0.0023) 0.0470 (0.0029) 1.0679 (0.0655) 0.0263 (0.0017) 0.9225 (0.0094) 0.1744 (0.0098) 0.2056 (0.0125) 0.0199 (0.0013)
Panel B: Missing Rate= 50%
NMC0.0688 (0.0054) 0.0871 (0.0068) – – – – – –
DID0.1711 (0.0142) 0.2195 (0.0184) – – – – – –
SC0.0635 (0.0057) 0.0815 (0.0075) – – – – – –
SDID0.1188 (0.0086) 0.1523 (0.0109) – – – – – –
TFI0.0769 (0.0057) 0.0983 (0.0072) – – – – – –
CONV-DIFF0.1206 (0.0087) 0.1546 (0.0110) 4.9108 (0.3529) 0.0861 (0.0062) 0.8830 (0.0117) 0.4839 (0.0235) 0.6560 (0.0469) 0.0648 (0.0047)
TUCKER-DIFF0.0699 (0.0050) 0.0900 (0.0063) 2.8968 (0.2026) 0.0500 (0.0036) 0.9500 (0.0092) 0.3544 (0.0253) 0.3895 (0.0270) 0.0378 (0.0027)
CFT-DIFF0.0490 (0.0037) 0.0631 (0.0049) 2.0091 (0.1558) 0.0347 (0.0027) 0.9148 (0.0144) 0.2195 (0.0183) 0.2668 (0.0202) 0.0261 (0.0020)
Panel C: Missing Rate= 75%
NMC0.1081 (0.0076) 0.1394 (0.0098) – – – – – –
DID0.1693 (0.0126) 0.2176 (0.0164) – – – – – –
SC0.0963 (0.0065) 0.1253 (0.0086) – – – – – –
SDID0.1185 (0.0081) 0.1521 (0.0101) – – – – – –
TFI0.1023 (0.0063) 0.1312 (0.0080) – – – – – –
CONV-DIFF0.1197 (0.0081) 0.1535 (0.0102) 5.9757 (0.4011) 0.0855 (0.0058) 0.8867 (0.0123) 0.4862 (0.0204) 0.6517 (0.0430) 0.0644 (0.0043)
TUCKER-DIFF0.0937 (0.0067) 0.1207 (0.0086) 4.7137 (0.3321) 0.0668 (0.0047) 0.9301 (0.0093) 0.4330 (0.0269) 0.5010 (0.0344) 0.0501 (0.0035)
CFT-DIFF0.0801 (0.0065) 0.1037 (0.0084) 4.0358 (0.3276) 0.0570 (0.0047) 0.9192 (0.0129) 0.3564 (0.0287) 0.4253 (0.0347) 0.0426 (0.0035)
Note.The table reports recovery at three missing rates. Entries are means across five independent simulation replications, with standard
deviations in parentheses. MAE and RMSE evaluate point recovery; Energy and CRPS evaluate the generated conditional distribution.
Coverage and Width denote the empirical coverage and average width of nominal 90% intervals, and IS and WIS denote the interval
score and weighted interval score. Smaller MAE, RMSE, Energy, CRPS, IS, and WIS indicate better performance. Width is interpreted
jointly with Coverage, whose nominal level is 0.90. Dashes indicate measures that are not applicable to point estimators. Each diffusion
method uses 100 conditional draws per evaluation matrix.
Among the five established point-recovery methods,SChas the lowest MAE and RMSE at each missing
rate, whileNMCandTFIare also competitive when the missing region is relatively small. Their recovery
errors nevertheless increase as the number of observed control outcomes decreases.CFT-DIFFattains the
lowest MAE and RMSE in every design. Relative toSC, the strongest of the five established methods, it
reduces MAE by 17%–30%; even after including the two nested generative specifications, its MAE remains
15%–25% below that of the next-best method.
The nested specifications further clarify the source of these gains.TUCKER-DIFFimproves substantially
onCONV-DIFF, demonstrating the value of Tucker dimension reduction, whileCFT-DIFFdelivers a further
improvement by incorporating the observed control outcomes through the masked conditional construction.

Kong et al.:Conditional Tensor Diffusion
24
Relative toTUCKER-DIFF,CFT-DIFFreduces both Energy and CRPS by 14%–31% across the three missing
rates. Its 90% coverage remains between 0.915 and 0.923, while its intervals are 18%–38% narrower than
those ofTUCKER-DIFF. The corresponding reductions in IS and WIS show that the sharper intervals retain
coverage close to the nominal level.
Figure 2 complements these aggregate measures with pointwise conditional distributions at a 25% miss-
ing rate. The three rows cover lower, central, and upper realized values within the missing region. This
comparison examines whether the methods recover not only a point prediction but also the local shape and
scale of the exact conditional distribution.
Figure 2Pointwise conditional distribution recovery (β= 0.50).
Note.Columns correspond toCONV-DIFF,TUCKER-DIFF, andCFT-DIFF. Rows display entries whose realized missing values are
near the 25th, 50th, and 75th percentiles within the missing region. Each histogram is based on 10,000 conditional draws, and the
missing rate is 25%. The solid curve shows the exact conditional density; the dashed and dotted vertical lines indicate the exact
conditional mean and the mean of the generated draws, respectively.
Across the three displayed entries, theCFT-DIFFhistograms closely track the location and concentration
of the exact conditional densities, and their means nearly coincide with the exact conditional means.CONV-

Kong et al.:Conditional Tensor Diffusion
25
DIFFandTUCKER-DIFFproduce visibly more dispersed distributions and larger location discrepancies,
particularly away from the center of the missing region’s realized-value distribution. Thus, the advantage
in Table 1 reflects a closer approximation to the conditional distribution rather than only a more accurate
generated mean.
6. Distributional Demand Response to Dynamic Electricity Pricing
Electricity systems increasingly rely on demand flexibility to manage short-run imbalances, especially dur-
ing periods of high demand or variable supply. Dynamic pricing can shift electricity use away from costly or
constrained hours, but its operational value depends on the magnitude, timing, and reliability of household
response. Evaluating these interventions therefore requires counterfactual demand estimates that character-
ize both average demand reductions and uncertainty in whether a price signal attains its intended target.
We examine these questions using the Norwegian iFlex dynamic-pricing experiment. The experiment fol-
lowed 3,746 households in five Norwegian regions during the winter of 2020–2021.11 The iFlex experiment
included 11 treatment groups and five regional control groups. Its within-region random allocation of house-
holds supports baseline exchangeability, while contemporaneous regional controls support counterfactual
comparisons on the realized intervention dates (Hofmann and Lindberg 2024). On selected experiment days,
each treatment group received one of 14 day-ahead hourly price signals implemented through a reward
scheme. The signals differed in their peak price levels, the timing of the peak periods, and their duration.
The data combine household-level hourly electricity consumption with treatment assignments, complete
hourly price paths, and local temperature measurements. This design generates repeated multi-arm interven-
tions with 24-hour outcome trajectories and substantial heterogeneity across households, dates, and pricing
regimes.
For the empirical analysis, we use hourly electricity consumption from December 1, 2020, through March
26, 2021, and restrict the sample to weekdays excluding holidays. We also exclude households that did not
satisfy the recruitment criteria, withdrew from the study, lacked complete electricity-consumption records
over the study period, or exhibited outlying consumption profiles. The resulting balanced panel contains
3,746 households, each represented by a74×24day-by-hour outcome matrix. Households assigned to the
five control groups form the training sample used to learn the conditional generator. For each treatment-
group household,CFT-DIFFgenerates the missing 24-hour no-policy (control) outcomes on intervention
days conditional on the observed no-policy outcomes. We use this setting to assess point and counterfactual
distribution recovery across competing methods and to quantify the average and distributional effects of the
dynamic-pricing interventions.
6.1. The iFlex Experiment and Counterfactual Structure
The iFlex experiment assigns dynamic-pricing interventions at the experimental-group-by-day level. Let
Gi denote the experimental group of householdi, and letD gt∈{0,1,...,14}denote the pricing regime
assigned to groupgon working dayt, whereD gt = 0denotes no active intervention. We define the cor-
responding household-level assignment byD it =D Git. Thus, all households within the same treatment
group are assigned the same day-ahead 24-hour price path, hereafter referred to as a price signal, on an
intervention day.12

Kong et al.:Conditional Tensor Diffusion
26
Figure 3Dynamic-pricing signals and group-level intervention schedule.
/uni00000014 /uni00000017 /uni0000001b /uni00000014/uni00000015 /uni00000014/uni00000019 /uni00000015/uni00000013 /uni00000015/uni00000017
/uni0000002b/uni00000052/uni00000058/uni00000055
/uni00000024/uni00000042/uni00000018
/uni00000024/uni00000042/uni00000014/uni00000013
/uni00000025/uni00000042/uni00000015
/uni00000025/uni00000042/uni00000018
/uni00000025/uni00000042/uni00000014/uni00000013
/uni00000025/uni00000042/uni00000014/uni00000018
/uni00000026
/uni00000033/uni00000042/uni00000015
/uni00000033/uni00000042/uni00000018
/uni00000033/uni00000042/uni00000014/uni00000013
/uni00000033/uni00000042/uni00000014/uni00000018
/uni00000033/uni00000013/uni00000042/uni00000015
/uni00000033/uni00000013/uni00000042/uni00000014/uni00000013
/uni00000033/uni00000013/uni00000042/uni00000016/uni00000013
/uni00000033/uni00000044/uni00000051/uni00000048/uni0000004f/uni00000003/uni0000000b/uni00000044/uni0000000c/uni00000003/uni0000002b/uni00000052/uni00000058/uni00000055/uni0000004f/uni0000005c/uni00000003/uni00000053/uni00000055/uni0000004c/uni00000046/uni00000048/uni00000003/uni00000056/uni0000004c/uni0000004a/uni00000051/uni00000044/uni0000004f/uni00000056
/uni00000027/uni00000048/uni00000046/uni00000011/uni00000003/uni00000015/uni00000013/uni00000015/uni00000013 /uni0000002d/uni00000044/uni00000051/uni00000011/uni00000003/uni00000015/uni00000013/uni00000015/uni00000014 /uni00000029/uni00000048/uni00000045/uni00000011/uni00000003/uni00000015/uni00000013/uni00000015/uni00000014 /uni00000030/uni00000044/uni00000055 /uni00000011/uni00000003/uni00000015/uni00000013/uni00000015/uni00000014
/uni0000003a /uni00000052/uni00000055/uni0000004e/uni0000004c/uni00000051/uni0000004a/uni00000003/uni00000047/uni00000044/uni0000005c
/uni00000025/uni00000048/uni00000055/uni00000042/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f
/uni00000025/uni00000048/uni00000055/uni00000042/uni00000014
/uni00000025/uni00000052/uni00000042/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f
/uni00000025/uni00000052/uni00000042/uni00000014
/uni00000032/uni00000056/uni00000042/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f
/uni00000032/uni00000056/uni00000042/uni00000014
/uni00000032/uni00000056/uni00000042/uni00000015
/uni00000032/uni00000056/uni00000042/uni00000016
/uni00000032/uni00000056/uni00000042/uni00000017
/uni00000032/uni00000056/uni00000042/uni00000018
/uni00000032/uni00000056/uni00000042/uni00000019
/uni00000037 /uni00000055/uni00000052/uni00000050/uni00000042/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f
/uni00000037 /uni00000055/uni00000052/uni00000050/uni00000042/uni00000014
/uni00000037 /uni00000055/uni00000052/uni00000050/uni00000042/uni00000015
/uni00000037 /uni00000055/uni00000052/uni00000051/uni00000047/uni00000042/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f
/uni00000037 /uni00000055/uni00000052/uni00000051/uni00000047/uni00000042/uni00000014
/uni00000028/uni0000005b/uni00000053/uni00000048/uni00000055/uni0000004c/uni00000050/uni00000048/uni00000051/uni00000057/uni00000044/uni0000004f/uni00000003/uni0000004a/uni00000055/uni00000052/uni00000058/uni00000053
/uni00000033/uni00000044/uni00000051/uni00000048/uni0000004f/uni00000003/uni0000000b/uni00000045/uni0000000c/uni00000003/uni0000002a/uni00000055 /uni00000052/uni00000058/uni00000053/uni00000010/uni0000004f/uni00000048/uni00000059/uni00000048/uni0000004f/uni00000003/uni00000046/uni00000052/uni00000058/uni00000051/uni00000057/uni00000048/uni00000055/uni00000049/uni00000044/uni00000046/uni00000057/uni00000058/uni00000044/uni0000004f/uni00000003/uni00000050/uni0000004c/uni00000056/uni00000056/uni0000004c/uni00000051/uni0000004a/uni00000051/uni00000048/uni00000056/uni00000056
/uni00000013 /uni00000018 /uni00000014/uni00000013 /uni00000014/uni00000018 /uni00000015/uni00000013 /uni00000015/uni00000018 /uni00000016/uni00000013
/uni00000028/uni0000005b/uni00000053/uni00000048/uni00000055/uni0000004c/uni00000050/uni00000048/uni00000051/uni00000057/uni00000044/uni0000004f/uni00000003/uni00000053/uni00000055/uni0000004c/uni00000046/uni00000048/uni00000003/uni0000000b/uni00000031/uni00000032/uni0000002e/uni00000012/uni0000004e/uni0000003a/uni0000004b/uni0000000c
/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f/uni00000003/uni0000004a/uni00000055/uni00000052/uni00000058/uni00000053 /uni00000031/uni00000052/uni00000003/uni00000044/uni00000046/uni00000057/uni0000004c/uni00000059/uni00000048/uni00000003/uni00000053/uni00000055/uni0000004c/uni00000046/uni00000048/uni00000003/uni00000056/uni0000004c/uni0000004a/uni00000051/uni00000044/uni0000004f /uni00000024/uni00000042/uni00000018 /uni00000024/uni00000042/uni00000014/uni00000013 /uni00000025/uni00000042/uni00000015 /uni00000025/uni00000042/uni00000018 /uni00000025/uni00000042/uni00000014/uni00000013 /uni00000025/uni00000042/uni00000014/uni00000018 /uni00000026 /uni00000033/uni00000042/uni00000015 /uni00000033/uni00000042/uni00000018 /uni00000033/uni00000042/uni00000014/uni00000013 /uni00000033/uni00000042/uni00000014/uni00000018 /uni00000033/uni00000013/uni00000042/uni00000015 /uni00000033/uni00000013/uni00000042/uni00000014/uni00000013 /uni00000033/uni00000013/uni00000042/uni00000016/uni00000013
Note.Panel (a) shows the 24-hour price paths for the 14 active dynamic-pricing interventions. Panel (b) shows the realized inter-
vention schedule for the 11 treatment groups and five regional control groups over the 74 working days in the analysis sample. Gray
cells denote control groups, white cells denote treatment-group days without an active intervention, and colored cells identify the
assigned price signal. Because assignment occurs at the group-day level, all households within a group share the same assignment
on a given day.
We take the household as the causal unit. LetY ith(d)denote householdi’s total electricity consumption
at hourhon daytunder assignment to the complete daily price signald, withd= 0denoting the no-
policy regime. Interactions among household members are incorporated into this household-level potential
response. We assume no interference across households: a household’s potential outcomes are unaffected
by the intervention assignments of other households. This causal restriction is distinct from statistical inde-
pendence, since households may share regional and temporal shocks.
Figure 3 summarizes the intervention design. Panel (a) displays the 14 active price signals as complete
hourly price paths. Profiles A and C feature separate morning and afternoon peak periods; profile B main-
tains elevated prices over an extended daytime period; and profiles P and P0 concentrate the peak price in
a short afternoon window. The numeric suffix denotes the peak price level in NOK/kWh and distinguishes
signals with the same profile but different incentive intensities; profile C is asymmetric and therefore has
no single numeric suffix. Panel (b) reports the realized group-level intervention schedule. No price signal
was implemented from December 1 through December 15, 2020, and the first interventions occurred on
December 16. Thereafter, the control groups remained untreated, whereas the treatment groups received
price signals intermittently. Each colored cell therefore represents a common intervention for all households
in the corresponding group.
In the empirical implementation, each household contributes one day-by-hour tensor. For householdi,
define the no-policy outcome matrix and its observed counterpart byX (i)
0 =

Yith(0)

t∈[74],h∈[24]∈R 74×24
andY obs
i =

Y obs
ith

t∈[74],h∈[24] . EachX (i)
0 is an order-two tensor corresponding toX 0 in Section 3.1, while
iindexes household-level samples. The complete matrices from households in the control groups form the
training sample used for score learning.

Kong et al.:Conditional Tensor Diffusion
27
For treatment groupg, define the intervention-day maskM (g)
T ∈{0,1} 74×24 and its complement by
M (g)
T (t,h) =1{D gt̸= 0}, t∈[74], h∈[24], M (g)
C =1−M (g)
T .
Thus, each intervention day corresponds to a completely masked 24-hour row, and households in the same
experimental group share the same mask. Although Hofmann and Lindberg (2024) report no clear aggregate
intraday rebound, a price signal may affect non-peak consumption through within-day load shifting or other
behavioral responses. Masking the entire intervention day prevents these potentially treatment-affected out-
comes from entering the conditioning set for recovery of the no-policy counterfactual.
Retaining non-intervention days as observed no-policy outcomes requires an additional temporal exclu-
sion restriction: interventions have no carryover effects on subsequent non-intervention days, and advance
notifications have no anticipatory effects on preceding non-intervention days. These are identifying assump-
tions, not consequences of random allocation. They permit responses across hours within an intervention
day while requiring that retained non-intervention days remain unaffected. Accordingly, the mask selects
complete intervention-day rows without extending to adjacent non-intervention days. The reduced con-
sumption on non-intervention days reported by Hofmann and Lindberg (2024) indicates that this restriction
may fail; the causal interpretation of recovery using the retained rows depends on its validity. Under consis-
tency, no interference across households, and the temporal exclusion restriction, a householdiwithG i =g
satisfies the observed control-outcome relation:
X(i)
C =M (g)
C ⊙X (i)
0 =M (g)
C ⊙Y obs
i ,
whereasM (g)
T ⊙X (i)
0 contains the missing no-policy outcomes on intervention days. Each group-specific
mask is applied synthetically to the training matrices during score learning. Conditional generation then
produces the missing no-policy rows of each treatment-group household matrix conditional on its observed
no-policy outcomes. Observed outcomes from all 24 hours of each intervention day are excluded from the
generator’s conditioning set and enter only the subsequent treatment-effect comparisons.
6.2. Counterfactual Recovery Accuracy
Before using the estimated counterfactuals to evaluate demand responses, we examine how accurately the
methods recover no-policy outcomes when these outcomes are available for validation. We artificially mask
complete household–day profiles observed under no policy. The masked 24-hour trajectories are treated as
missing no-policy outcomes, while their observed values provide the ground truth for measuring recovery.
We compareCFT-DIFFwith five point-recovery benchmarks: the causal panel methodsDID,SC, and
SDID, and the matrix/tensor completion methodsNMCandTFI. We also include the two diffusion specifi-
cations nested withinCFT-DIFF,CONV-DIFFandTUCKER-DIFF, to assess the gains from Tucker dimension
reduction and conditioning on the observed no-policy outcomes. All methods receive the same observed
no-policy outcomes and are evaluated on the same artificially masked outcomes. Point recovery is measured
by MAE; for the three diffusion methods, distributional recovery is assessed using the energy score, CRPS,
and interval-based measures.
We consider three missingness patterns that represent different structures of missing outcomes in panel
settings. Under the switchback pattern, missing household–days occur intermittently over time. Under stag-
gered adoption, households enter the missing region at different dates, whereas under simultaneous adoption

Kong et al.:Conditional Tensor Diffusion
28
they enter at a common date. Whenever a household–day is selected as missing, all 24 hourly outcomes are
removed. Appendix EC.5.2 provides a visual illustration of the three patterns. For each pattern, we consider
seven target missing proportions, ranging from 0.149 to 0.581, so that the evaluation covers missingness
levels both below and above that observed in the iFlex application. Letρdenote the realized missing pro-
portion and letρ emp = 0.265denote the empirical treated share. Figure 4 reports the relative missingness
levelρ/ρ emp, with the vertical dashed line indicatingρ=ρ emp.
Figure 4Counterfactual recovery across missingness patterns and levels.
Note.The figure evaluates counterfactual recovery by artificially masking observed no-policy outcomes and comparing the recov-
ered outcomes with their observed values. Panels (a)–(c) report MAE across different missingness levels under the switchback,
staggered-adoption, and simultaneous-adoption patterns, respectively. Panels (d)–(f) report the corresponding energy scores for
CFT-DIFFand its two nested diffusion specifications. The horizontal axis reports the realized missing proportion relative to the
empirical treated share,ρ/ρ emp, and the vertical dashed line indicatesρ=ρ emp. Lower values indicate better recovery.
Panels (a)–(c) of Figure 4 compare point recovery across the full range of missingness levels. We report
MAE under the switchback, staggered-adoption, and simultaneous-adoption patterns, respectively. For the
three diffusion methods, the point prediction is obtained by averaging the 100 generated draws.CFT-DIFF
has the lowest MAE across the three patterns and remains stable as the missing proportion increases. The
inset in each panel is a local enlargement of the corresponding region in the original panel and provides a
more detailed view of the methods with relatively low errors. The results show that the advantage ofCFT-
DIFFpersists across missingness levels. By contrast, the error ofTFIincreases substantially as the missing
region expands, especially under the switchback and staggered-adoption patterns.
Panels (d)–(f) examine counterfactual distribution recovery forCFT-DIFFand its two nested diffusion
specifications. We use the energy score to compare the generated distribution of each missing 24-hour tra-

Kong et al.:Conditional Tensor Diffusion
29
jectory with its observed trajectory. The energy score accounts for both the discrepancy between generated
and observed trajectories and the dispersion of the generated trajectories; smaller values indicate better dis-
tributional recovery. Its formal definition and sample implementation, together with the definitions of the
other evaluation measures, are provided in Appendix EC.5.3.
The lower panels show that the energy score generally increases with the missing proportion, reflecting
the greater difficulty of recovering a trajectory from fewer observed no-policy outcomes. This increase is
substantially smaller forCFT-DIFF. Its energy score remains below those ofCONV-DIFFandTUCKER-DIFF
under all three missingness patterns and throughout the range of missingness levels, with the gap tending to
widen under staggered and simultaneous adoption. The point-recovery advantage ofCFT-DIFFis therefore
accompanied by more accurate recovery of the joint distribution of the missing 24-hour trajectory.
Table 2Counterfactual recovery at the missingness level closest to the empirical treated share.
Panel A: Point counterfactual recovery
Switchback Staggered adoption Simultaneous adoption
Method MAE RMSE MAE RMSE MAE RMSE
DID0.0344 0.0498 0.0437 0.0664 0.0391 0.0606
SC0.0314 0.0475 0.0323 0.0488 0.0324 0.0487
SDID0.0299 0.0455 0.0305 0.0465 0.0306 0.0464
NMC0.0302 0.0464 0.0299 0.0465 0.0300 0.0463
TFI0.1599 0.2517 0.1773 0.3072 0.0618 0.0935
CONV-DIFF0.0328 0.0513 0.0354 0.0524 0.0337 0.0508
TUCKER-DIFF0.0326 0.0507 0.0343 0.0528 0.0329 0.0508
CFT-DIFF0.0289 0.0449 0.0295 0.0453 0.0297 0.0454
Panel B: Counterfactual distribution recovery under the switchback mask
Method Energy score CRPS 90% coverage 90% width IS WIS
CONV-DIFF0.1479 0.0239 0.887 1.7246 2.6548 0.2569
TUCKER-DIFF0.1476 0.0239 0.907 1.8352 2.6898 0.2583
CFT-DIFF0.1314 0.0210 0.893 1.2559 2.0126 0.1819
Note.The table evaluates counterfactual recovery by artificially masking observed no-policy outcomes and comparing the recovered
outcomes with their observed values. Panel A reports MAE and RMSE at the available missingness level closest to the empirical treated
share,ρ emp = 0.265. The target missing proportion is 0.284, with realized missing proportions of 0.283, 0.284, and 0.284 under the
switchback, staggered-adoption, and simultaneous-adoption patterns, respectively. Point predictions forCFT-DIFFand its two nested
diffusion specifications are obtained by averaging 100 generated draws. Panel B reports distributional recovery under the switchback
pattern. The energy score evaluates the joint 24-hour trajectory, whereas CRPS is computed for individual hourly outcomes. Coverage
and width refer to 90% central intervals for household–day totals. The interval score is computed for the 90% central interval, and WIS
denotes the weighted interval score combining the predictive median and the 50%, 60%, 70%, 80%, 90%, and 95% central intervals.
Errors, scores, and interval widths are reported on the normalized experimental scale. Boldface and underlining indicate the best and
second-best values in each column, respectively; coverage is ranked by absolute deviation from the nominal level of 0.90, and the
remaining measures are ranked from smallest to largest.
Table 2 provides a more detailed comparison at the available missingness level closest to the empirical
treated share. The common target missing proportion is 0.284, with realized missing proportions close to
0.284 under all three patterns. Panel A reports MAE and RMSE.CFT-DIFFachieves the lowest value for
every point-recovery measure. Under the switchback pattern, its MAE and RMSE are 0.0289 and 0.0449,
compared with 0.0299 and 0.0455 for the second-best method. Under staggered adoption, the correspond-
ing values are 0.0295 and 0.0453, while under simultaneous adoption they are 0.0297 and 0.0454. The
improvement is therefore consistent across both error measures and all three missingness patterns.
Panel B evaluates the generated counterfactual distribution in more detail under the switchback pattern.
The energy score evaluates the joint 24-hour trajectory, whereas CRPS evaluates the marginal distribution

Kong et al.:Conditional Tensor Diffusion
30
of individual hourly outcomes. The 90% coverage measures how often the observed household–day total
falls within the generated 90% central interval, and should therefore be close to its nominal level of 0.90.
The 90% width measures the average width of these intervals, with a smaller value indicating a sharper
interval when coverage remains comparable. The interval score (IS) jointly penalizes wide intervals and
observations falling outside the interval, while the weighted interval score (WIS) combines the predictive
median with several central intervals. For the energy score, CRPS, IS, and WIS, smaller values indicate
better distributional recovery.
The distributional measures give a consistent picture.CFT-DIFFreduces the energy score from approxi-
mately 0.148 for the two nested diffusion specifications to 0.1314 and reduces CRPS from 0.0239 to 0.0210.
Its 90% empirical coverage is 0.893, close to the nominal level of 0.90, while its average interval width
is 1.2559, compared with 1.7246 forCONV-DIFFand 1.8352 forTUCKER-DIFF. The interval score and
WIS likewise decrease to 2.0126 and 0.1819, respectively. Thus, the narrower intervals produced byCFT-
DIFFretain coverage close to the nominal level. Together with Figure 4, these results show thatCFT-DIFF
improves point and counterfactual distribution recovery across the missingness patterns and levels consid-
ered.
6.3. Causal Estimands
Having evaluated counterfactual recovery, we define the causal measures used to assess each price sig-
nal relative to the no-policy outcome. Within the analysis sample, our estimands are defined by assigned
price signals and include households regardless of active response, targeting the effect of assignment to
the implemented intervention package. For a household–day–hour observation withD it =d, define the
demand reduction as∆ ith(d) =Y ith(0)−Y ith(d), so that a positive value indicates lower electricity use
under the price signal. BecauseY ith(d) =Y obs
ith wheneverD it =d, estimating∆ ith(d)requires recovering
the corresponding no-policy outcomeYith(0).
For a price signaldand a set of hoursH, we consider two aggregate estimands. The pooled relative
demand reduction is
Rd(H) = 100×
X
(i,t):Dit=d
X
h∈H
{Yith(0)−Y ith(d)}
X
(i,t):Dit=d
X
h∈H
Yith(0)
,
and the average absolute reduction per assigned household–day is
∆abs
d (H) = 1
Nd
X
(i,t):Dit=d
X
h∈H
{Yith(0)−Y ith(d)},
whereN d is the number of household–day observations assigned signald. We evaluate both estimands
over the signal-specific peak-price hours and additionally evaluate the relative reduction over the full 24-
hour period. The peak-period estimands measure demand changes during the hours targeted by the price
signal, whereas the full-day estimand measures the overall change in daily electricity use. These estimands
characterize responses under the realized repeated-intervention schedule. Their operational relevance is
supported by the sustained responsiveness documented by Hofmann and Lindberg (2024) during the study
period.

Kong et al.:Conditional Tensor Diffusion
31
In the empirical analysis, the unobservedY ith(0)is replaced by its estimated no-policy counterfactual.
ForCFT-DIFF, the point estimates in Section 6.4 use the mean ofB= 100generated draws, while the
complete set of draws is retained for the distributional summaries defined below.
Letν= (g,t)denote a group–day intervention event, letE d be the set of realized events assigned signal
d, and letH d denote the signal-specific peak-price hours. For thebth sample from bPT
t0 (·|X C), let eY (b)
ν (0)
denote the generated no-policy outcomes for eventν, and write eY (b)
ith (0)for the generated no-policy out-
come of householdiat hourh. Forν= (g,t)∈E d, define the corresponding peak-period relative demand
reduction by
R(b)
ν = 100×
X
i:Gi=g
X
h∈Hd
n
eY (b)
ith (0)−Y obs
ith
o
X
i:Gi=g
X
h∈Hd
eY (b)
ith (0)
, b= 1,...,B.
The pooled response distribution for signaldis represented byR d =

R(b)
ν :ν∈E d;b= 1,...,B
 
. To mea-
sure how reliably a signal attains a target reductionc, definebπd(c) = 1
B|Ed|
P
ν∈Ed
PB
b=1 I

R(b)
ν ≥c
 
. Thus,
bπd(c)is the fraction of pooled reductions that reach the target. The collectionR d combines variation across
realized intervention events with uncertainty in the generated no-policy counterfactuals.13
6.4. Demand Response to Dynamic Pricing
We now use the no-policy counterfactuals generated byCFT-DIFFto evaluate the demand-response measures
defined in Section 6.3. Point estimates are obtained by averagingB= 100conditional draws.
Figure 5 shows the intraday pattern of electricity demand and its response to the different price signals.
Across signals, demand follows a similar daily profile, with a morning peak and a larger evening peak. Dur-
ing the high-price hours, observed demand generally remains close to its estimated no-policy counterfactual,
although the direction and magnitude of the difference vary across signals. The clearest reduction occurs for
P0 30, which imposes a peak price of 30 NOK/kWh over a two-hour afternoon window, whereas most other
signals produce only modest changes. For several signals, observed demand exceeds its estimated counter-
factual outside the high-price window. This pattern is consistent with intertemporal substitution: households
may shift some deferrable electricity use to lower-price hours rather than eliminate it altogether. Within
a given price profile, higher peak prices are associated with larger reductions in some cases, most visibly
among theP0signals, although the pattern also varies with the timing and duration of the intervention. The
responses therefore differ across price designs in both magnitude and timing.
Table 3 quantifies these patterns. Seven signals—allPandP0signals—have positive peak-period esti-
mates, and the peak-period percentage exceeds the corresponding full-day percentage for 12 of the 14
signals. Thus, except for the twoAsignals, the demand response is more favorable during the targeted hours
than over the day as a whole. The largest estimated peak reduction occurs underP 15, at 2.51%, or 0.163
kWh per assigned household–day over the two-hour peak period. The comparison between peak-period and
full-day estimates is consistent with households shifting electricity use away from high-price hours rather
than uniformly reducing daily consumption.
The aggregate estimates in Table 3 do not show when the offsetting demand adjustments occur. We
therefore examine the temporal pattern of the response more closely. Figure 6 reports the hourly effects and
then expands the evaluation window from the signal-specific peak hours toward the full day.

Kong et al.:Conditional Tensor Diffusion
32
Figure 5Observed and counterfactual electricity demand by price signal.
Note.The solid line reports observed hourly electricity demand under the assigned price signal, and the dashed line reports the esti-
mated no-policy counterfactual. The counterfactual curve averages 100CFT-DIFFconditional draws. Background shading indicates
the experimental electricity price, with darker shading corresponding to higher prices.
Table 3Causal and distributional effects by price signal.
Signal Peak h Events Peak kWh Peak % Full-day %Q 0.10 bπd(3%)
A5 8 9 -0.164 -0.76 -0.36 -2.34 0.01
A10 8 10 -0.154 -0.61 -0.46 -2.54 0.00
B2 13 35 -0.080 -0.22 -0.77 -2.15 0.02
B5 13 29 -0.103 -0.27 -0.78 -2.26 0.04
B10 13 39 -0.034 -0.09 -0.58 -2.13 0.02
B15 13 28 -0.079 -0.20 -1.01 -2.31 0.02
C8 8 -0.064 -0.31 -0.41 -2.27 0.02
P2 2 16 0.070 1.14 -0.49 -2.56 0.24
P5 2 13 0.158 2.29 -0.71 -1.54 0.41
P10 2 27 0.140 2.22 -0.69 -1.77 0.41
P15 2 20 0.163 2.51 -0.75 -1.62 0.42
P0 2 2 5 0.089 1.58 -0.80 -1.98 0.31
P0 10 2 10 0.069 1.15 -0.54 -1.56 0.22
P0 30 2 5 0.139 2.43 -0.61 -0.04 0.35
Note.Positive values denote electricity-demand reductions. Peak h is the number of hours in the signal-specific peak-price period, and
Events is the number of group-day intervention events assigned signald. Peak kWh is the average absolute reduction per assigned
household–day over the peak-price period. Peak and full-day percentages are pooled ratio-of-sums estimates based on the mean
of 100CFT-DIFFconditional draws.Q 0.10 is the 10th percentile of the event-by-draw peak-reduction distribution andbπ d(3%)is the
corresponding fraction of outcomes with a peak reduction of at least 3%.

Kong et al.:Conditional Tensor Diffusion
33
Figure 6Hourly and cumulative demand reductions.
Note.Panel (a) reports hourly relative demand reductions for each price signal, with positive values indicating lower observed
demand relative to the estimated no-policy counterfactual. Thin outlines identify the signal-specific peak-price hours. Panel (b)
reports cumulative demand changes in kWh per assigned household–day as the evaluation window expands from the peak-price
hours to the full day. Results in Panel (b) are aggregated by price profile and weighted by the observed frequency of household–day
assignments.
Panel (a) shows that, for many price signals, observed demand decreases relative to the estimated no-
policy counterfactual during the high-price hours, with larger reductions inside the targeted periods than in
surrounding hours. The magnitude and timing of the response vary across signals with different price levels
and intervention durations. Panel (b) shows that the estimated cumulative reduction generally becomes
smaller as the evaluation window expands beyond the signal-specific peak hours, turning from positive
around the peak hours to negative over the full day for profilesPandP0. This pattern is consistent with, but
does not by itself establish, intertemporal shifting of electricity use from the targeted periods to other hours.
From an operational perspective, shifting demand away from a constrained period may remain valuable
even without a reduction in total daily consumption.
6.5. Counterfactual Distributions, Intervals, and Response Reliability
The preceding analysis uses the mean of theCFT-DIFFdraws to study average demand responses. We now
use the pooled response distributionsRd and target-attainment ratesbπd(c)defined in Section 6.3 to examine
variation in event-level responses and the reliability with which each signal attains a specified reduction
target. The estimated conditional distributions provide prediction intervals for the missing no-policy out-
comes.
Figure 7 shows substantial differences in the distribution and reliability of demand response across price
signals. Panel (a) shows that peak-period responses span a wide range across intervention events and condi-
tional draws for most signals. TheAandBsignals are generally concentrated at lower reductions, whereas
thePsignals place more of their distributions above zero. Panel (b) translates these distributions into
target-attainment rates.P0 30 produces a positive peak reduction in 89% of the event–draw outcomes and
a reduction of at least 3% in 35%. For theAandBsignals, the corresponding fractions attaining a 3%

Kong et al.:Conditional Tensor Diffusion
34
Figure 7Counterfactual distribution and reliability of demand response.
Note.For each intervention eventνandCFT-DIFFdrawb,R (b)
ν denotes the peak-period relative demand reduction computed
using the generated no-policy counterfactual eY (b)
ν (0)from bPT
t0 (·|X C). Panel (a) reports the empirical distribution ofR (b)
ν across
intervention events andB= 100generated samples for each price signal; the white point denotes the median and the horizontal
segment spans the 10th to the 90th percentile. Panel (b) reports the corresponding probability of achieving alternative peak-period
reduction targets. Positive values indicate lower observed demand relative to the generated no-policy counterfactual.
reduction range from 0% to 4%. The relative performance of the P signals also varies with the target:P0 30
has the highest probability of attaining the lower targets, whereasP 15 performs better at the 3% and 5%
targets. Thus, the full counterfactual distribution provides information that is not available from the mean
response alone: price signals with similar average effects can differ substantially in how consistently they
reduce demand during the targeted high-price hours.
The conditional distributions also provide prediction intervals for the average no-policy outcomes in the
treated region. Table 4 reports central 90% prediction intervals fromCFT-DIFFand its two nested diffusion
specifications, together with their√ne-scaled widths and width ratios.
Table 4 shows thatCFT-DIFFproduces the narrowest prediction interval for every price signal. Its mean
√ne-scaled width is 0.764, compared with 1.355 forCONV-DIFFand 1.441 forTUCKER-DIFF. The corre-
sponding mean width ratios are 1.790 and 1.903, so theCONV-DIFFandTUCKER-DIFFintervals are, on
average, 79.0% and 90.3% wider than theCFT-DIFFintervals, respectively. The artificial-mask validation in
Table 2 provides the corresponding calibration evidence: the narrowerCFT-DIFFintervals retain empirical
coverage close to the nominal level.

## Conclusion

This paper developsCFT-DIFFto extend counterfactual analysis in panel or tensor data beyond point recov-
ery to the joint conditional distribution of missing control outcomes. The method generates these outcomes
conditional on the observed control outcomes, with efficiency gained by learning the nonlinear component
of the score in a low-dimensional Tucker core. Repeated draws from the learned distribution preserve depen-
dence among the missing outcomes and yield point estimates, quantiles, counterfactual prediction intervals,
and target-attainment probabilities from a single model.
Nonasymptotic, high-probability bounds show that the difficulty of conditional-score estimation depends
on the Tucker core dimension, the largest mode dimension, and the effective number of missing outcomes

Kong et al.:Conditional Tensor Diffusion
35
Table 4Counterfactual prediction intervals for average no-policy outcomes by price signal.
No-policy prediction interval Scaled interval width Width ratio
SignalCONV TUCKER CFT CONV TUCKER CFT CONV/CFT TUCKER/CFT
A5 [2.297, 2.345] [2.233, 2.289] [2.454, 2.482] 1.089 1.265 0.631 1.725 2.004
A10 [2.592, 2.654] [2.538, 2.598] [2.847, 2.880] 1.394 1.360 0.747 1.867 1.822
B2 [2.534, 2.574] [2.464, 2.497] [2.658, 2.678] 1.593 1.347 0.818 1.948 1.647
B5 [2.636, 2.682] [2.559, 2.606] [2.772, 2.800] 1.665 1.740 1.039 1.603 1.675
B10 [2.512, 2.548] [2.437, 2.479] [2.648, 2.671] 1.566 1.793 1.008 1.553 1.778
B15 [2.725, 2.771] [2.629, 2.680] [2.839, 2.862] 1.707 1.870 0.867 1.968 2.156
C[2.218, 2.269] [2.178, 2.224] [2.335, 2.369] 1.135 1.033 0.769 1.475 1.342
P2 [2.608, 2.654] [2.529, 2.577] [2.741, 2.768] 1.231 1.277 0.747 1.648 1.709
P5 [2.926, 2.980] [2.861, 2.922] [3.109, 3.143] 1.441 1.656 0.895 1.610 1.850
P10 [2.642, 2.687] [2.560, 2.609] [2.818, 2.843] 1.578 1.740 0.858 1.839 2.027
P15 [2.713, 2.762] [2.635, 2.695] [2.908, 2.931] 1.510 1.862 0.708 2.132 2.629
P0 2 [2.339, 2.396] [2.284, 2.341] [2.532, 2.562] 0.923 0.911 0.476 1.939 1.914
P0 10 [2.449, 2.504] [2.390, 2.449] [2.683, 2.711] 1.251 1.348 0.637 1.964 2.116
P0 30 [2.420, 2.475] [2.353, 2.413] [2.579, 2.610] 0.887 0.977 0.496 1.790 1.972
Mean across signals 1.355 1.441 0.764 1.790 1.903
Note.The table uses all hourly outcomes in the signal-specific treated region. TheCONV,TUCKER, andCFTcolumns correspond to
CONV-DIFF,TUCKER-DIFF, andCFT-DIFF, respectively, and report central 90% prediction intervals for their generated average no-policy
outcomes. For each signal, the scaled interval width equals the interval width multiplied by √ne, wheren e is the number of treated
households contributing to that signal. The interval endpoints remain on the original kWh scale. The width ratios compare theCONVand
TUCKERwidths with theCFTwidth; values above one indicate wider intervals than underCFT. The final row reports arithmetic means of
the displayed width statistics across signals.
rather than on the full tensor dimension alone. The score bounds imply recovery guaranties for the con-
ditional distribution and weighted summaries, while the prediction-interval guarantee accounts for a finite
number of generated draws. Simulations confirm the roles of both components ofCFT-DIFF: Tucker dimen-
sion reduction and conditioning on the observed control outcomes each improve recovery, andCFT-DIFFis
more accurate than the causal panel and matrix/tensor completion methods considered. In the iFlex study,
artificial-mask validation confirms these gains across three treatment patterns. The subsequent causal anal-
ysis shows that price signals with similar average demand reductions can have different target-attainment
probabilities. Rankings based only on average responses can therefore conceal meaningful differences in
intervention reliability.
Future research can extendCFT-DIFFto causal settings with pretreatment covariates, more complex treat-
ment patterns, or heavy-tailed outcomes. The heavy-tailed setting is especially important when decisions
depend on rare or extreme counterfactual events. Another direction is to use the recovered distributions
directly in intervention selection and optimization and establish guaranties for the resulting decisions. When
Tucker structure is too restrictive, learned nonlinear representations such as variational autoencoders may
provide an alternative form of dimension reduction. Comparing these representations with Tucker reduction
would clarify which low-dimensional structure is most effective across data settings and sample sizes.

## Acknowledgments

All authors contributed equally and are listed in alphabetical order.
Endnotes
1Alternative forward processes, including variance-exploding and sub-variance-preserving diffusions, are also possible. We
adopt the variance-preservingOUprocess because its transition law is available in closed form and it drives the data distribution

Kong et al.:Conditional Tensor Diffusion
36
toward a standard Gaussian reference distribution, thereby simplifying score estimation and theoretical analysis. It is also a standard
and widely used specification in diffusion modeling (Ho et al. 2020, Song et al. 2021).
2The reverse-time equality is distributional: the process reproduces the forward marginal distributions but does not retrace an
individual forward sample path.
3Throughout, a time subscript in score denotes the population counterpart, whereas the final time argument denotes a candidate
or estimated score function.
4The tensor-completion step conditions on the specified treatment mask. Thus, even when the mask arises from randomized
assignment, its sampling distribution need not be modeled by the conditional generator.
5For example, ifTa ={i 1,i 2,i 3}andwassigns weight1/3to each coordinate, thenU 0,a(w) = 1
3
P3
j=1Yij (0).
6Under the normalization below,βd = 0gives the weak factor boundary, with no dimension-driven attenuation of idiosyncratic
noise along moded, whereasβ d = 1gives the strong-factor boundary, with attenuation at a rate ofp −1/2
d . Values in(0,1)accom-
modate intermediate strength, and allowingβ d to vary across modes permits heterogeneous factor strengths; related prediction
theory under weak factors is developed by Giglio et al. (2026).
7The score-error term follows from a change of measure between the exact and trained reverse-time processes and contraction
under the endpoint map (Girsanov 1960, F ¨ollmer 2005, Csisz ´ar 1967, Fu et al. 2024); the terminal bound follows from entropy
contraction of the Ornstein–Uhlenbeck forward process (Bakry et al. 2014).
8For example, ifTa =i 1,i 2,i 3 andwassign weight1/3to each coordinate, thenU 0,a(w) = 1
3
P3
j=1Yij (0).
9LetU w,ℓ,t =w⊤ vec(X(ℓ)
T,t ). Under the forward coupling,U w,ℓ,t0−Uw,ℓ,0 = (αt0−1)Uw,ℓ,0 +h 1/2
t0 w⊤ vec(Zℓ). Indepen-
dence across analysis tensors, centering, andEU 2
w,ℓ,0≤C∥w∥ 2
2 therefore giveE

|√ne{Vne,w,t0−Vne,w,0}|2
≤C∥w∥ 2
2{(1−
αt0 )2 +ht0}≤C∥w∥ 2
2t0. Taking the square root yields the contributionC∥w∥ 2
√t0 =C∥w∥ 2n−an/2 in (4.7).
10It is not a sampling confidence interval for a population average treatment effect; population-level inference would additionally
require assumptions linking the analysis tensors to the target population.
11The iFlex project was conducted in two phases. We use the full-scale second phase. The first phase, conducted during the winter
of 2019–2020, was stopped earlier than planned because of the onset of the COVID-19 pandemic and therefore did not cover the
originally intended winter experimental window. The anonymized data are publicly available through the official iFlex repository
on Zenodo (doi:10.5281/zenodo.8248802).
12Each treatment group was associated with a prespecified set of four candidate price signals, one of which was assigned when-
ever the group was treated. Consequently, not every signal was available to every treatment group; the group-specific candidate sets
are reported in Appendix Table EC.5.
13It is distinct from the sampling distribution of an average-effect estimator and from a joint cross-world distribution of individual
treatment effects.

## References

Agarwal A, Shah D, Shen D (2026) Synthetic interventions: Extending synthetic controls to multiple treatments.
Operations Research74(2):840–859.
Anderson BD (1982) Reverse-time diffusion equation models.Stochastic Processes and their Applications12(3):313–
326.
Arkhangelsky D, Athey S, Hirshberg DA, Imbens GW, Wager S (2021) Synthetic difference-in-differences.American
Economic Review111(12):4088–4118.
Athey S, Bayati M, Doudchenko N, Imbens G, Khosravi K (2021) Matrix completion methods for causal panel data
models.Journal of the American Statistical Association116(536):1716–1730.
Athey S, Imbens GW (2006) Identification and inference in nonlinear difference-in-differences models.Econometrica
74(2):431–497.

Kong et al.:Conditional Tensor Diffusion
37
Auerbach J, Slawski M, Zhang S (2022) Tensor completion for causal inference with multivariate longitudinal data: A
reevaluation of COVID-19 mandates.arXiv preprint arXiv:2203.04689.
Bai J (2003) Inferential theory for factor models of large dimensions.Econometrica71(1):135–171.
Bai J, Ng S (2021) Matrix completion, counterfactuals, and factor analysis of missing data.Journal of the American
Statistical Association116(536):1746–1763.
Bai J, Ng S (2023) Approximate factor models with weaker loadings.Journal of Econometrics235(2):1893–1916.
Bakry D, Gentil I, Ledoux M, et al. (2014)Analysis and geometry of Markov diffusion operators, volume 103
(Springer).
Bojinov I, Simchi-Levi D, Zhao J (2023) Design and analysis of switchback experiments.Management Science
69(7):3759–3777.
Borusyak K, Jaravel X, Spiess J (2024) Revisiting event-study designs: Robust and efficient estimation.Review of
Economic Studies91(6):3253–3285.
Breunig C, Liu R, Yu Z (2025) Double robust bayesian inference on average treatment effects.Econometrica
93(2):539–568.
Cen Z, Lam C (2025) Tensor time series imputation through tensor factor modelling.Journal of Econometrics
249:105974.
Chang J, Du Y , Huang G, Yao Q (2026a) Identification and estimation for matrix time series CP-factor models.The
Annals of Statistics54(3):1372–1397.
Chang J, He J, Yang L, Yao Q (2023) Modelling matrix time series via a tensor CP-decomposition.Journal of the
Royal Statistical Society Series B: Statistical Methodology85(1):127–148.
Chang J, Huang G, Yao Q, Yu L (2026b) CP-factorization for high dimensional tensor time series and double projection
iterations.arXiv preprint arXiv:2606.08560.
Chang J, Jiao Y , Kang L, Shi J (2026c) Deep bootstrap.arXiv preprint arXiv:2602.10587.
Chen H, Simchi-Levi D (2026) Efficient switchback experiments with surrogate variables: Estimation and experimen-
tal design.Management Science72(6):4854–4870.
Chen M, Huang K, Zhao T, Wang M (2023) Score approximation, estimation and distribution recovery of diffusion
models on low-dimensional data.International Conference on Machine Learning, 4672–4712 (PMLR).
Chen M, Xu R, Xu Y , Zhang R (2025) Diffusion factor models: Generating high-dimensional returns with factor
structure.arXiv preprint arXiv:2504.06566.
Chernozhukov V , Fern ´andez-Val I, Melly B (2013) Inference on counterfactual distributions.Econometrica
81(6):2205–2268.
Choi J, Yuan M (2024) Matrix completion when missing is not at random and its applications in causal panel data
models.Journal of the American Statistical Association1–15.
Csisz´ar I (1967) Information-type measures of difference of probability distributions and indirect observations.Studia
Scientiarum Mathematicarum Hungarica2:299–318.
Duan J, Pelger M, Xiong R (2024) Factor analysis for causal inference on large non-stationary panels with endogenous
treatment.Available at SSRN.
Fan J, Gu Y , Li X (2025) Optimal estimation of a factorizable density using diffusion models with ReLU neural
networks.arXiv preprint arXiv:2510.03994.
F¨ollmer H (2005) An entropy approach to the time reversal of diffusion processes.Stochastic Differential Systems
Filtering and Control: Proceedings of the IFIP-WG 7/1 Working Conference Marseille-Luminy, France, March
12–17, 1984, 156–163 (Springer).
Fu H, Yang Z, Wang M, Chen M (2024) Unveil conditional diffusion models with classifier-free guidance: A sharp
statistical theory.arXiv preprint arXiv:2403.11968.
Gao C, Chen H, Zhang AR, Yang S (2025) Causal inference on sequential treatments via tensor completion.arXiv
preprint arXiv:2511.15866.

Kong et al.:Conditional Tensor Diffusion
38
Giglio S, Xiu D, Zhang D (2026) Prediction when factors are weak.Journal of the American Statistical Association
Forthcoming.
Girsanov IV (1960) On transforming a certain class of stochastic processes by absolutely continuous substitution of
measures.Theory of Probability & Its Applications5(3):285–301.
Gunsilius FF (2023) Distributional synthetic controls.Econometrica91(3):1105–1117.
Guo J, Kong X, Li Z, Mao J (2026) Tucker diffusion model for high-dimensional tensor generation.arXiv preprint
arXiv:2604.00481.
Han Y , Chen R, Yang D, Zhang CH (2024) Tensor factor model estimation by iterative projection.The Annals of
Statistics52(6):2641–2667.
He Y , Wang Y , Yu L, Zhou W, Zhou WX (2025) A new non-parametric kendall’s tau for matrix-valued elliptical
observations.Bernoulli31(4):3331–3355.
Ho J, Jain A, Abbeel P (2020) Denoising diffusion probabilistic models.Advances in Neural Information Processing
Systems33:6840–6851.
Hofmann M, Lindberg KB (2024) Evidence of households’ demand flexibility in response to variable hourly electricity
prices—results from a comprehensive field experiment in Norway.Energy Policy184:113821.
Kallus N (2023) Treatment effect risk: Bounds and inference.Management Science69(8):4579–4590.
Kolda TG, Bader BW (2009) Tensor decompositions and applications.SIAM Review51(3):455–500.
Liu H, Zhu T, Jia N, He J, Zheng Z (2026) Learning to simulate from heavy-tailed distribution via diffusion model.
Operations Research.
Ma Y , Melnychuk V , Schweisthal J, Feuerriegel S (2024) DiffPO: A causal diffusion model for learning distributions
of potential outcomes.Advances in Neural Information Processing Systems37:43663–43692.
Mandal D, Parkes DC (2019) Weighted tensor completion for time-series causal inference.arXiv preprint
arXiv:1902.04646.
Massart P (1990) The tight constant in the Dvoretzky-Kiefer-Wolfowitz inequality.The Annals of Probability
18(3):1269–1283.
Sanchez P, Tsaftaris SA (2022) Diffusion causal models for counterfactual estimation.Proceedings of the First Con-
ference on Causal Learning and Reasoning, volume 140 ofProceedings of Machine Learning Research, 1–21
(PMLR).
Song Y , Ermon S (2019) Generative modeling by estimating gradients of the data distribution.Advances in Neural
Information Processing Systems32.
Song Y , Sohl-Dickstein J, Kingma DP, Kumar A, Ermon S, Poole B (2021) Score-based generative modeling through
stochastic differential equations.International Conference on Learning Representations.
Tashiro Y , Song J, Song Y , Ermon S (2021) CSDI: Conditional score-based diffusion models for probabilistic time
series imputation.Advances in Neural Information Processing Systems, volume 34, 24804–24816.
Wang D, Liu X, Chen R (2019) Factor models for matrix-valued high-dimensional time series.Journal of Econometrics
208(1):231–248.
Xia D, Yuan M (2019) On polynomial time methods for exact low-rank tensor completion.Foundations of Computa-
tional Mathematics19(6):1265–1313.
Xia D, Yuan M (2021) Statistical inferences of linear forms for noisy matrix completion.Journal of the Royal Statis-
tical Society Series B: Statistical Methodology83(1):58–77.
Xia D, Yuan M, Zhang CH (2021) Statistically optimal and computationally efficient low rank tensor completion from
noisy entries.The Annals of Statistics49(1):76–99.
Xiong R, Pelger M (2023) Large dimensional latent factor modeling with missing observations and applications to
causal inference.Journal of Econometrics233(1):271–301.
Yu L, Xie J, Zhou W (2023) Testing kronecker product covariance matrices for high-dimensional matrix-variate data.
Biometrika110(3):799–814.

Kong et al.:Conditional Tensor Diffusion
39
Yuan C, Gao Z, He X, Huang W, Guo J (2023) Two-way dynamic factor models for high-dimensional matrix-valued
time series.Journal of the Royal Statistical Society Series B: Statistical Methodology85(5):1517–1537.
Zhang X, Liu CC, Guo J, Yuen KC, Welsh AH (2025) Modeling and learning on high-dimensional matrix-variate
sequences.Journal of the American Statistical Association120(549):419–434.
Zhen Y , Wang J (2024) Nonnegative tensor completion for dynamic counterfactual prediction on COVID-19 pandemic.
The Annals of Applied Statistics18(1):224–245.
Zhou X, Reich BJ, Yang S (2026) Spatial causal tensor completion for multiple exposures and outcomes: An applica-
tion to the health effects of PFAS pollution.arXiv preprint arXiv:2603.16854.

e-companion toKong et al.:Conditional Tensor Diffusionec1
Technical Proofs and Additional Results
This appendix contains technical proofs and additional results for the paper.
• Appendix EC.1 provides the summary of notation.
• Appendix EC.2 provides the proofs of theorems in the main text.
• Appendix EC.3 provides the details of our framework.
• Appendix EC.4 provides the additional simulation results.
• Appendix EC.5 provides additional empirical results.
EC.1. Summary of Notation
Table EC.1 summarizes the principal notation used in the main text, while Table EC.2 collects additional
notation used in the e-companion. Both tables group notation by its role in the analysis.
EC.2. Proofs
Throughout this section, tensor-valued scores are identified with their vectorizations when vector notation
is used. Vectorization preserves inner products and hence identifies the Frobenius norm with the Euclidean
norm. In vector coordinates,p t(·|x C)denotes the densityp T
t (·|X C)under this identification. For a candi-
date loading–variance pair(Γ,ω), write
Γ⊗ = ΓD⊗···⊗Γ 1, g t(Γ,ω) = vec{Gt(Γ,ω)},
ΛT,t (ω) = diag{vec(WT,t (ω))},Λ C(ω) = diag{vec(WC(ω))}.
EC.2.1. Proof of Proposition 3.1
We first vectorize the tensor model in Proposition 3.1 for the sake of notational brevity, which is a proof
device only. The model and algorithm are stated in tensor notation in Section 3. Recall the identity
vec(G×D
d=1Bd) = (BD⊗···⊗B 1) vec(G). WritexT,t = vec(XT,t ),x C = vec(XC),f= vec(F), and
A⊗ =AD⊗···⊗A 1. The matrix forms of the two noise covariances and the masked precision matrices are
Ωt =htIp +α 2
tp−βΣ⊗
e ,Ω 0 =p−βΣ⊗
e ,ΛT,t =MT Ω−1
t MT = diag{vec(WT,t )}, andΛC =MCΩ−1
0 MC =
diag{vec(WC)}. Then, we defineHT,t =A⊤
⊗ΛT,tA⊗,HC =A⊤
⊗ΛCA⊗, andV t ={HT,t +α−2
t HC}−1. The
vector coordinate of the core statistic is defined as
gt := vec(Gt) =Vt
 
A⊤
⊗ΛT,txT,t +α−1
t A⊤
⊗ΛCxC

.
They agree directly with the tensor operations because
vec
 
G×D
d=1Ad

=A⊗ vec(G),vec

(W⊙X)× D
d=1A⊤
d
 
=A⊤
⊗ diag{vec(W)}vec(X).
Finally, recall thatξ(g,t) =E(α tf|g t =g). The tensor proposition is therefore equivalent to proving the
vectorized identity
∇xT,t logpt(xT,t|xC) = ΛT,t{A⊗ξ(gt,t)−x T,t}.
In the following, we prove the vectorized identity above, where we writeA=A ⊗ andΣ e = Σ⊗
e for
brevity. Letx 0∈Rp denote the complete vector. LetM∈{0,1} p be a fixed binary mask, whereM j = 1

ec2 e-companion toKong et al.:Conditional Tensor Diffusion
Table EC.1Principal notation used in the main text.
General notation
L(X),L(X|Y)Probability law and conditional
probability law
∥·∥2,∥·∥F,∥·∥ op Euclidean, Frobenius, and operator
norms
vec(·),Tucker(·)Vectorization and reshaping into a
Tucker core tensor
⊙,⊘Entrywise multiplication and division
Potential outcomes and counterfactual target Tucker factor structure
D,pd,pNumber of modes, dimension of mode
d, and full dimensionp= QD
d=1pd
FLatent Tucker core tensor
ITensor index set[p 1]×···×[p D]A d Mode-dloading matrix, with
A⊤
dAd =Ird
Yi(a)Potential outcome at coordinateiunder
interventiona;a= 0denotes control
EIdiosyncratic tensor component
Y obs
i Observed outcome at coordinateir d,rMode-dTucker rank and core
dimensionr= QD
d=1rd
Ta,T,CIntervention-asupport, treated region,
and the observed-control region
βd,pβ Mode-dfactor strength and scaling
pβ = QD
d=1p
βd
d
MTa,MT,MC Binary masks forTa,T, andCf,eVectorized coref= vec(F)and
idiosyncratic componente= vec(E)
X0,P 0 Complete control-world tensor and its
distributionP 0 =L(X 0)
pcore Density of the vectorized coref
XT,XC Missing and observed control outcomesΣ e,d,Σ⊗
e Mode-specific and separable
idiosyncratic covariance matrices
PT
0 (·|XC)Target lawL(X T|XC)A ⊗,Qσ Kronecker loading matrix and tensor of
coordinatewise idiosyncratic variances
{X
(i)
0 }n
i=1 Training sampleW T,t,WC Coordinatewise precision tensors for the
two regions
w,U 0,a(w)Prespecified weight vector and
intervention-specific control-world
summary
HT,t,HC Core-level information matrices for the
two regions
Vt,gt,Gt Core covariance, vectorized core
statistic, and its tensorization
Masked conditional diffusion Estimation and distributional recovery
t,t 0,T,uDiffusion time, early-stopping time,
terminal time, and reverse elapsed time
ξ(g,t)Conditional core regression
E(αtf|g t =g)
αt,ht Signal coefficient and noise variance;
αt =e−t/2 andht = 1−e−t
Γ,ωCandidate Tucker loadings and
idiosyncratic variances
Wt,Wu,Zt Forward and reverse Wiener processes
and Gaussian perturbation tensor
Zθ,ζθ Tensor-valued Core-Net and its
vectorized form
XT,t Forward-diffused outcomes in the
treated region at timet
sΓ,ω,θ Candidate masked Tucker score
PT
t ,pT
t Conditional distribution and density of
XT,t givenXC
SMT Masked Tucker conditional-score class
st(X|X C)Conditional score∇ T logpT
t (X|X C)L mask, bLmask Population and empirical masked
score-matching losses
X←
T,u Exact reverse-time process in the treated
region
bsConditional score learned from the
training sample
bX←
T,u Reverse process driven bybs p T,dT,β,p max Number of missing outcomes, effective
treated dimension, and largest mode
dimension
bPT
t0(·|XC)Conditional distribution generated by
the trained reverse process
Vne,w,0, bVne,w,t0 Target and generated weighted
control-world averages
bI
(B)
ne,w,1−α(x)Counterfactual prediction interval based
onBgenerated draws
τne,w,a Weighted treated-minus-control
counterfactual contrast
means that coordinatejbelongs to the missing-outcome block in the treated region. The mask partitions the
coordinates into two deterministic sets, i.e.,T={j:M j = 1}andC={1,...,p}\T.
The mask, equivalently the partition(T,C), is fixed and non-random. We therefore suppressMfrom the
conditioning notation for brevity. Define the diagonal mask matricesMT = diag(M)andM C =Ip−MT .
The treated-region and observed-control-outcome vectors are kept in the originalp-dimensional full space,
that is,xT =MTx0 andxC =MCx0. Thus,xT is supported only onT, whilex C is supported only onC.

e-companion toKong et al.:Conditional Tensor Diffusionec3
Table EC.2Additional notation used in the e-companion.
Vectorized proof notation Discrete training and generation
x0,xT,xC Vectorizations ofX 0,XT,XC j,N step,¯αj Discrete diffusion index, number of
steps, and cumulative signal coefficient
xT,t Vectorized forward-diffused outcomes
in the treated region
xj,bϵθ Masked input and learned noise
predictor at stepj
MT,MC Diagonal matrix forms of the region
masks
bX0, eX
(b)
0 Inferred clean tensor and conditional
completionb
Ωt,Ω 0 Full-dimensional noise covariance
matrices at timestand0
H,W,k 1,k 2 Matrix dimensions and implemented
Tucker-core dimensions
ΛT,t,ΛC Masked precision matrices for the two
regions
ϕenc,U,VFeature stem and trainable row and
column Tucker bases
ϕ(·;µ,V)Gaussian density with meanµand
covarianceV
EC,ET Encoded observed-control and
treated-region features
pt
con Marginal density of the low-dimensional
core statisticgt
BNumber of independently generated
conditional draws
∥v∥2
B Quadratic seminormv⊤Bv x max Clipping threshold in DDIM generation
Theoretical rate quantities Simulation and empirical evaluation
Σf,GR Core covariance and region
{g:∥g∥ ∞≤R}
ρ,ρ emp Simulation missing rate and empirical
treated proportion
Bf,C 1,C 2 Constants in the tail condition forp core J,NJ Set and number of missing simulation
entries
vmax,Lg,Lt,K 0 Core-variance, Lipschitz, and magnitude
constants
yi,x
(b)
i ,byi Realized value, generated draw, and
generated-mean prediction
Rϵ High-probability core truncation radiusL i,Ui Endpoints of an entrywise prediction
interval
L,m,J,κNetwork depth, width, sparsity, and
parameter bound
µi,σi,bµmi,bσmi Exact and generated conditional
moments
K,γg,γt,CV Network output, Lipschitz, and
core-covariance bounds
Dmi Pointwise location-and-scale
discrepancy for methodm
A•,ω 0 Population loading matrices and
idiosyncratic variances
MAE,RMSEPoint-recovery measures
δn,ϵ,a n Exponent adjustment, approximation
tolerance, and early-stopping exponent
Energy,CRPSJoint and marginal distributional scores
Ln,Rn,An Polylogarithmic factor, recovery-rate
sequence, and high-probability event
IS,WISInterval and weighted interval scores
Ftr Sigma-field generated by the training
sample
M,nM Set and number of artificially masked
empirical outcomes
Mn,ne,w Conditional-density bound used for
anti-concentration
Uj, eU
(b)
j Observed and generated household–day
totals
bFx,bqx Conditional CDF and quantile function
of the generated weighted summary
Lj,α,Hj,α,mj Interval endpoints and predictive
median for household–dayj
bFB,x,DB,x Empirical generated CDF and its
uniform error
nB,KC Number of evaluated blocks and number
of central coverage levels
Recall that we writeA=A ⊗ andΣ e = Σ⊗
e . Consider the following vectorized factor model
x0 =Af+p −β/2e.(EC.2.1)
Under Assumption 3.1,A⊤A=I r, the factorfhas densityp core, and the diagonal idiosyncratic covariance
is bounded above and below. The signal is kept at a constant spectral scale, while the factor-strength param-
eterβ∈[0,1]enters through the idiosyncratic noise scalep −β/2. The missing-outcome distribution in the
treated region is denoted byP T
0 (·|x C), with the fixed partition(T,C)given in advance.
Letϕ(·;µ,Σ)denote the Gaussian density with meanµand covariance matrixΣ. For a positive semidef-
inite matrixB, write∥u∥
2
B =u⊤Bu, allowing this to be a seminorm. All gradients are taken with respect to
the displayed argument. Whenever a masked vector is used as the argument of a density, its active coordinate
subspace is identified with the corresponding Euclidean space.
Forward diffusion on positions in the treated region.

ec4 e-companion toKong et al.:Conditional Tensor Diffusion
The forward diffusion corrupts only the positions in the treated region, while the observed-control-
outcome coordinates remain fixed throughout the process. For diffusion timet∈[0,T], we use the stan-
dard Ornstein–Uhlenbeck schedule, that is,α t = exp(−t/2)andh t = 1−α 2
t = 1−exp(−t). Hence, the
noise-treated-region coordinates admit the marginal representationx T,t =αtxT +h 1/2
t MTzt, wherez t∼
N(0,I p)andz t⊥⊥x0.
Define the full-dimensional noise scales asΩ t =htIp +α 2
tp−βΣe,Ω 0 =p−βΣe, and define the masked
precision matrices asΛT,t =MT Ω−1
t MT ,ΛC =MCΩ−1
0 MC. The matricesΛT,t andΛC arep×pmatrices.
They are singular as full matrices, but they are positive definite on the treated and observed-control regions,
respectively.
Under (EC.2.1), marginalizing out the latent factor gives the conditional density of the diffused treated-
region coordinates:p t(xT,t|xC) = [
R
p(xT,t,xC|f)p core(f)df]/p(xC). The denominatorp(x C)does not
depend onxT,t and, hence, does not affect the score with respect toxT,t . Therefore, for the score calculation,
it is enough to keep the numerator
R
p(xT,t,xC|f)p core(f)df. The relevant likelihood, viewed as a function
off, is the joint likelihoodp(x T,t,xC|f). Due to the block-independent idiosyncratic noise,x T,t andxC
are conditionally independent givenf. Consequently,p(x T,t,xC|f) =p(x T,t|f)p(xC|f). After omitting
factors independent off, define the joint likelihood kernelL t(f;xT,t,xC)by
Lt(f;xT,t,xC)∝exp

−1
2∥xT,t−αtAf∥
2
ΛT,t

exp

−1
2∥xC−Af∥
2
ΛC

= exp

−1
2∥xT,t−αtAf∥
2
ΛT,t
− 1
2∥xC−Af∥
2
ΛC

.
Therefore, we have
pt(xT,t|xC)∝
Z
Lt(f;xT,t,xC)pcore(f)df,(EC.2.2)
where the proportionality is with respect tox T,t ; the omitted normalizing factor depends only on the fixed
control vectorxC.
Conditional score decomposition.
Define the two precision Gram matrices asH T,t =A⊤ΛT,tAandH C =A⊤ΛCA. LetV t = (HT,t +
α−2
t HC)−1, and define the low-dimensional conditional encoder asg t =V t(A⊤ΛT,txT,t +α−1
t A⊤ΛCxC).
The matrixV t is the effective noise scale of the encoded factor information after combining the treated-
region and observed-control-region branches. Since the observed-control-outcome term contributes addi-
tional precisionα−2
t HC, the effective factor noise is smaller than the treated-region-only factor noise when-
ever the observed-control-outcome coordinates carry nontrivial factor information. Forg∈R r, define the
conditional core density asp t
con(g) =
R
ϕ(g;αtf,Vt)pcore(f)df. Equivalently,p t
con is the marginal density
ofg|f∼N(α tf,Vt). Because the complementary masks provide positive precision on every coordinate
andA⊤A=I r,(HT,t +α−2
t HC)is positive definite. Thus,V t is well defined, and the treated-region score
satisfies
∇xT,t logpt(xT,t|xC) = ΛT,tAVt∇g logpt
con(gt)| {z }
factor score
−ΛT,t (xT,t−Agt)| {z }
residual score
.(EC.2.3)
Equivalently, letξ(g,t) =E(α tf|g) =g+V t∇g logpt
con(g), then
∇xT,t logpt(xT,t|xC) = ΛT,t{Aξ(gt,t)−x T,t}.(EC.2.4)

e-companion toKong et al.:Conditional Tensor Diffusionec5
Proof.By (EC.2.2), we havep t(xT,t |xC)∝
R
Lt(f;xT,t,xC)pcore(f)df. Taking the gradient with
respect toxT,t and moving the derivative inside the integral, we obtain
∇xT,t logpt(xT,t|xC) =
R
∇xT,tLt(f;xT,t,xC)pcore(f)dfR
Lt(f;xT,t,xC)pcore(f)df
= ΛT,t

A
R
αtfLt(f;xT,t,xC)pcore(f)dfR
Lt(f;xT,t,xC)pcore(f)df −xT,t

= ΛT,t{AE(αtf|x T,t,xC)−xT,t}.
Define the quadratic coefficient ofαtfasV −1
t =A⊤ΛT,tA+α−2
t A⊤ΛCA, and define the corresponding
center asg t =V t(A⊤ΛT,txT,t +α−1
t A⊤ΛCxC). As a function off, the exponent inL t(f;xT,t,xC)is a
quadratic form. Expanding the two terms gives
∥xT,t−αtAf∥
2
ΛT,t
+∥xC−Af∥
2
ΛC
= (αtf)⊤A⊤ΛT,tA(αtf)−2(α tf)⊤A⊤ΛT,txT,t +x⊤
T,t ΛT,txT,t
+f⊤A⊤ΛCAf−2f ⊤A⊤ΛCxC +x⊤
C ΛCxC.
To express everything in terms of the scaled factorα tf, note thatf ⊤A⊤ΛCAf= (α tf)⊤α−2
t HC(αtf)and
f⊤A⊤ΛCxC = (αtf)⊤α−1
t A⊤ΛCxC. Therefore, we have
∥xT,t−αtAf∥
2
ΛT,t
+∥xC−Af∥
2
ΛC
= (αtf)⊤{HT,t +α−2
t HC}(αtf)
−2(αtf)⊤
A⊤ΛT,txT,t +α−1
t A⊤ΛCxC
 
+x⊤
T,t ΛT,txT,t +x⊤
C ΛCxC.
By the definitions ofV t andg t, we know thatV −1
t =H T,t +α−2
t HC andV −1
t gt =A ⊤ΛT,txT,t +
α−1
t A⊤ΛCxC. Substituting these identities into the previous display yields
∥xT,t−αtAf∥
2
ΛT,t
+∥xC−Af∥
2
ΛC
= (αtf)⊤V−1
t (αtf)−2(α tf)⊤V−1
t gt +x⊤
T,t ΛT,txT,t +x⊤
C ΛCxC
=∥αtf−g t∥
2
V−1
t
+

x⊤
T,t ΛT,txT,t +x⊤
C ΛCxC−g⊤
t V−1
t gt
 
.
The remainder can be written asRt(xT,t,xC) =x⊤
T,t ΛT,txT,t +x⊤
C ΛCxC−g⊤
t V−1
t gt. which depends only on
the observed pair(xT,t,xC). It shows that, as a function off, the likelihood kernel of the high-dimensional
observation(xT,t,xC)is proportional toexp{−∥α tf−g t∥
2
V−1
t
/2}. All remaining factors are independent
off. Hence, the posterior distribution offgiven(x T,t,xC)is the same as the posterior distribution offin
the low-dimensional Gaussian experimentgt =αtf+η t, forη t∼N(0,V t). In particular, we have
E(αtf|x T,t,xC) =E(αtf|g t).
It remains to express this posterior mean through the score of the low-dimensional marginal density.
By definition,p t
con(g) =
R
ϕ(g;αtf,Vt)pcore(f)dfis the marginal density of the experimentg=α tf+
ηt. Differentiating under the integral gives∇ gpt
con(g) =
R
∇gϕ(g;αtf,Vt)pcore(f)df=
R
{−V−1
t (g−
αtf)}ϕ(g;α tf,Vt)pcore(f)df. Dividing byp t
con(g), we obtain∇ g logpt
con(g) =V −1
t {E(αtf|g)−g}.
Therefore,E(α tf|g) =g+V t∇g logpt
con(g). Evaluating this identity at the sufficient statisticg=g t gives
E(αtf|x T,t,xC) =E(αtf|g t) =gt +Vt∇g logpt
con(gt).
Substituting this expression into the score identity∇ xT,t logpt(xT,t |xC) = ΛT,t{AE(αtf|x T,t,xC)−
xT,t}proves (EC.2.3) and (EC.2.4).

ec6 e-companion toKong et al.:Conditional Tensor Diffusion
Finally, it remains to return to the tensor expressions used in the main text. For the tensor model, letxT,t =
vec(XT,t ), andx C = vec(XC). Moreover, writeΛ T,t = diag{vec(WT,t )}andA ⊗ξ(gt,t) = vec{E(αtF|
Gt)×D
d=1Ad}. It follows that
∇xT,t logpt(xT,t|xC) = diag{vec(WT,t )}

vec

E(αtF|G t)×D
d=1Ad
 
−vec(XT,t )

= vec

WT,t⊙

E(αtF|G t)×D
d=1Ad−XT,t
 
.
Finally, vectorization preserves the Frobenius inner product, sovec{∇ XT,t logpt(XT,t |X C)}=
∇xT,t logpt(xT,t|xC). Since vectorization is one-to-one, the preceding identity proves (3.9).
□
EC.2.2. Proof of Theorem 3.1
Proof.For clarity, we also prove Theorem 3.1 in the vectorized notation. ForR>0, writeG R ={g∈
Rr :∥g∥∞≤R}, andK R = 1 + supg∈GR, t∈[t0,T]∥ξ(g,t)∥ 2.
First, recall that conditioned onf,x T,t ∼ N(αtMTA⊗f,MT ΩtMT ), andx C ∼
N(MCA⊗f,MCΩ0MC). BecauseΣ ⊗
e is diagonal, the treated-region and control-complement noises
are independent. Therefore,A ⊤
⊗ΛT,txT,t +α−1
t A⊤
⊗ΛCxC has a conditional meanα tHT,tf+α −1
t HCf=
(HT,t +α−2
t HC)αtfand conditional covarianceH T,t +α−2
t HC. Multiplying byV t = (HT,t +α−2
t HC)−1
givesgt|f∼N(α tf,Vt). Equivalently, we can writegt =αtf+η t, whereη t∼N(0,V t), andη t⊥⊥f. By
Assumptions 3.2 and 3.3,fis sub-Gaussian, andη t has covariance bounded byv maxIr, uniformly over
t∈[t 0,T]. Hence,g t is uniformly sub-Gaussian. Moreover, Assumption 3.3 givesK R≤K 0 +√rLgR, so
KRϵ =O(K 0 +LgRϵ).
Second, we approximate the core regression on the truncated domainG Rϵ ={g∈R r :∥g∥∞≤Rϵ}. We
can rescaleg′ = (g+R ϵ1r)/(2Rϵ)andt ′ =t/T. Then, define the rescaled regression function as
eξ(g′,t′) =ξ(2Rϵg′−Rϵ1r,τ(t′)),whereτ(t ′) = max{Tt′,t 0}.
Under Assumption 3.3, eξis2R ϵLg-Lipschitz ing ′ andTL t-Lipschitz int′. Partition[0,1] r intoN r
g cubes
and[0,1]intoN t intervals with
Ng =
2r+3√rRϵLg
ϵ

, N t =
2r+2TLt
ϵ

.
Letψ(a) = 1for|a|<1,ψ(a) = 2−|a|for|a|∈[1,2], andψ(a) = 0for|a|>2. For a multi-index
q= (q 1,...,q r)⊤∈{0,1,...,N g}r andj∈{0,1,...,N t}, we follow the partition-of-unity construction in
Guo et al. (2026) and consider
eζi(g′,t′) =
X
q
X
j
eξi(q/Ng,j/Nt)ψ{3Nt(t′−j/Nt)}
rY
k=1
ψ{3Ng(g′
k−qk/Ng)},
for each coordinatei∈[r]. We use the partition-and-product construction in Appendix B.1 of Chen et al.
(2023), which adapts the local ReLU construction of?. We apply it coordinatewise to the centered func-
tions eξi−eξi(0,0), and restore eξi(0,0)through the output bias. In the notation of that construction, the
input dimension isr+ 1, the two coordinatewise Lipschitz moduli are2R ϵLg andTL t, and the centered

e-companion toKong et al.:Conditional Tensor Diffusionec7
range is bounded by a constant multiple ofK Rϵ. The stated uniform output bound then follows from the
approximation error and the bound on the target range:
m=O{(1 +L gRϵ)r(1 +TLt)ϵ−(r+1)}, K=O(K 0 +LgRϵ), L=O{log(K/ϵ) + 1},
J=O(mL), κ=O
 
max{K0 +LgRϵ,TL t,T−1}

, γ ′
g =CrRϵLg, γ ′
t =CrTLt,
there exists a rescaled ReLU networkeζ¯θ such that
sup
g′∈[0,1]r, t′∈[t0/T,1]
∥eζ¯θ(g′,t′)− eξ(g′,t′)∥∞≤ϵ,sup
g′∈[0,1]r, t′∈[t0/T,1]
∥eζ¯θ(g′,t′)∥2≤Cr(KRϵ +ϵ),
∥eζ¯θ(g′
1,t′)−eζ¯θ(g′
2,t′)∥2≤CrRϵLg∥g′
1−g′
2∥2,∥ eζ¯θ(g′,t′
1)−eζ¯θ(g′,t′
2)∥2≤CrTLt|t′
1−t′
2|.
Transforming back to the original variables gives a ReLU networkζ 0
¯θ(g,t) = eζ¯θ((g+R ϵ1r)/(2Rϵ),t/T).
Implementingt7→t/Tas an additional affine input layer addsT −1 to the coefficient boundκ; its constant
depth and sparsity costs are absorbed by the stated architecture orders. Extend the network toR r using
the coordinate-wise clipping mapΠ Rϵ(g)j =−R ϵ + ReLU(gj +Rϵ)−ReLU(g j−Rϵ)forj∈[r], and
setζ ¯θ(g,t) =ζ 0
¯θ(ΠRϵ(g),t). The clipping map is represented exactly by anO(r)-size ReLU module, is1-
Lipschitz, mapsR r intoG Rϵ, and equals the identity on that box. Thereforeζ ¯θ agrees withζ 0
¯θ onG Rϵ, is
globally bounded byK, and has the original-scale Lipschitz bounds
∥ζ¯θ(g1,t)−ζ ¯θ(g2,t)∥ 2≤CrLg∥g1−g 2∥2,∥ζ ¯θ(g,t 1)−ζ ¯θ(g,t 2)∥2≤CrLt|t1−t 2|,
globally onRr×[t 0,T], up to changing the numerical constantC r. The additional width, sparsity, and coef-
ficient size are absorbed by the displayed architecture orders. Thereforeζ ¯θ∈F core(L,m,J,K,κ,γ g,γt),
and the constructed network satisfies
sup
g∈GRϵ, t∈[t0,T]
∥ζ¯θ(g,t)−ξ(g,t)∥ ∞≤ϵ.(EC.2.5)
Third, we convert the uniform approximation into anL 2 core approximation. For fixedt∈[t 0,T], define
Et ={∥gt∥∞≤Rϵ}. OnE t, (EC.2.5) gives∥{ζ ¯θ(gt,t)−ξ(g t,t)}IEt∥2≤√rϵ. OnE c
t , the clipped network
remains bounded byK. Hence, we have
E

∥ζ¯θ(gt,t)−ξ(g t,t)∥ 2
2IEc
t

≤2K 2P(Ec
t ) + 2E

∥ξ(gt,t)∥ 2
2IEc
t

.
By Jensen’s inequality, we have∥ξ(g,t)∥ 2
2 =∥E(α tf|g)∥ 2
2≤E(∥α tf∥ 2
2|g)≤E(∥f∥ 2
2|g). SinceE c
t is
measurable with respect tog t, the tower property gives
E

∥ξ(gt,t)∥ 2
2IEc
t

≤E

E(∥f∥ 2
2|gt)IEc
t

=E

∥f∥ 2
2IEc
t

.
It remains to bound the right hand side uniformly int. Fromg t =αtf+η t,α t≤1, andη t∼N(0,V t)with
Vt⪯v maxIr, we know thatE c
t ={∥gt∥∞>Rϵ}⊆{∥f∥ ∞>Rϵ/2}∪{∥η t∥∞>Rϵ/2}. Therefore, we can
obtain
E

∥f∥ 2
2IEc
t

≤E

∥f∥ 2
2I{∥f∥∞>Rϵ/2}

+E

∥f∥ 2
2I{∥ηt∥∞>Rϵ/2}

.
The first term is controlled by the sub-Gaussian tail off. For the second term,η t is independent off, so
we haveE[∥f∥ 2
2I{∥ηt∥∞>Rϵ/2}] =E∥f∥ 2
2P(∥ηt∥∞>Rϵ/2). The Gaussian tail bound andV t⪯v maxIr

ec8 e-companion toKong et al.:Conditional Tensor Diffusion
implyP(∥η t∥∞>Rϵ/2)≤2rexp(−cR 2
ϵ)for a constantc>0that is independent oft. Together with the
sub-Gaussian tail off, this gives, for a fixed constantq r>0,P(E c
t )+E[∥f∥ 2
2IEc
t ]≤C(1+R qr
ϵ ) exp(−cR2
ϵ)
uniformly overt∈[t 0,T]. Combining this bound withK 2 =O{(K 0 +LgRϵ)2}, and enlargingq r if nec-
essary, givesE[∥ζ ¯θ(gt,t)−ξ(g t,t)∥ 2
2IEc
t ]≤C(1 +R qr
ϵ ) exp(−cR2
ϵ)uniformly overt∈[t 0,T]. Letu ϵ =
ctailr/(t0ϵ)and chooseC R such thatcC 2
R≥4. Sinceu ϵ≥1, for the fixed constantq r, there existsC qr>0
such that1 + (logu)qr/2≤Cqru2, whereu≥1, we have
(1 +Rqr
ϵ ) exp(−cR2
ϵ)≤C{1 + (logu ϵ)qr/2}u−4
ϵ ≤Cu−2
ϵ =C
 t0ϵ
ctailr
2
≤ C
c2
tail
ϵ2.
Here, the last inequality follows from0<t 0≤1andr≥1. Takingc tail sufficiently large makes the final
upper bound at mostϵ 2. Therefore, we haveE[∥ζ ¯θ(gt,t)−ξ(g t,t)∥ 2
2IEc
t ]≤ϵ 2 uniformly overt∈[t 0,T].
Combining the bounds onEt andE c
t by the triangle inequality inL 2, we have that uniformly overt∈[t 0,T]:
n
E
h
∥ζ¯θ(gt,t)−ξ(g t,t)∥
2
2
io1/2
≤(√r+ 1)ϵ.(EC.2.6)
Finally, we lift the core approximation to the treated-region score. SetΓ d =Ad for everyd, equivalently
Γ =A•, and setω=ω 0. Then,Γ⊗ =A⊗ andg t(A•,ω 0) =gt. Vectorizing the network with coreζ ¯θ gives
vec{sA•,ω0,¯θ(XT,t,XC,t)}= ΛT,t{A⊗ζ¯θ(gt,t)−x T,t}.
Meanwhile, by (3.9),∇ xT,t logpt(xT,t|xC) = ΛT,t{A⊗ξ(gt,t)−x T,t}. The shortcut cancels exactly, so
vec{sA•,ω0,¯θ(XT,t,XC,t)}−∇ xT,t logpt(xT,t|xC) = ΛT,tA⊗{ζ¯θ(gt,t)−ξ(g t,t)}.
Taking the nested conditional risk and applying (EC.2.6) gives
EXC EXT,t|XC
h

sA•,ω0,¯θ(XT,t,XC,t)−∇ XT,t logpt(XT,t|XC)

2
F
i
≤∥ΛT,tA⊗∥2
op(√r+ 1)2ϵ2.
SinceΩ t⪰h tIp, the treatment precision weights satisfy∥Λ T,t∥op≤h−1
t . SinceA ⊤
⊗A⊗ =I r, we have
∥ΛT,tA⊗∥op≤∥ΛT,t∥op∥A⊗∥op≤h−1
t . Combining the preceding two displays proves the result.
□
EC.2.3. Proof of Theorem 3.2
Proof.Fixa∈(0,1)andδ∈(0,1). We first decompose the raw DSM loss into statistical, truncation,
and approximation terms. We begin with the truncation radii. For later use, define the Gaussian transition
score and the population raw DSM loss byr t(xT,xT,t ) =h−1
t (αtxT−xT,t )andL mask(s) =E{ℓ(X 0;s)},
respectively, whereℓis defined in (3.11). Letd C,β =r+ (p−p T )p−β,d + =dT,β +dC,β + 1, andu n =
A0 log(nd+). Here,A 0>0is a sufficiently large constant. Meanwhile, takeC 2
T,x =A 1dT,βun andC 2
C,x =
A1dC,βun, whereA 1>0is sufficiently large. Hence, up to logarithmic factors,C 2
T,x = eO(dT,β )andC 2
C,x =
eO{dC,β}. Then, define the truncation eventEtr ={∥XT∥F≤CT,x,∥X C∥F≤CC,x}. In vectorized notation,
we can write
XT =MTA⊗f+p −β/2MTe, X C =MCA⊗f+p −β/2MCe.
SinceA ⊤
⊗A⊗ =I r andM T,MC are coordinate projections, we have∥M TA⊗f∥ 2 ≤ ∥f∥2 and
∥MCA⊗f∥ 2≤∥f∥ 2. Then, by Assumption 3.2,fis sub-Gaussian in the sense that, for allu≥1,P{∥f∥ 2
2>

e-companion toKong et al.:Conditional Tensor Diffusionec9
C(r+u)}≤Ce −cu. Moreover, Assumption 3.1 implies that the covariance ofp −β/2MTeis dominated
byCp −βMT , while that ofp −β/2MCeis dominated byCp −βMC. Hence, foru≥1, the standard Gaus-
sian quadratic-form tail bound givesP{p −β∥MTe∥2
2>Cp−β(pT +u)}≤Ce −cu andP{p−β∥MCe∥2
2>
Cp−β(p−pT +u)}≤Ce −cu.
Combining the signal and idiosyncratic parts and increasingCif necessary, we obtainP{∥X T∥2
F >
CdT,βu}+P{∥X C∥2
F >CdC,βu}≤Ce −cu foru≥1. Takingu=u n and choosingA 1 sufficiently large
yields
P(∥XT∥F >CT,x ) +P(∥XC∥F >CC,x)≤Ce −cun≤(3n 2)−1,
where the last inequality follows from the choiceun =A 0 log(nd+)withA 0 sufficiently large. Indeed, since
d+≥1, we haveCe −cun =C(nd +)−cA0≤Cn−cA0. ChooseA 0 such thatcA 0≥3. Then, for all sufficiently
largen, we haveCe −cun≤Cn−3≤(3n 2)−1. Therefore, we haveP(E c
tr)≤(3n 2)−1.
It remains to control the second moment on the truncation complement. The same tail bound, integrated
over the tail, implies
E

∥XT∥2
F I{∥XT∥F >CT,x}

≤CdT,βune−cun,E

∥XC∥2
F I{∥XC∥F >CC,x}

≤CdC,βune−cun.
Also, by the sub-Gaussian moment bound forfand the Gaussian moment bound fore, we haveE∥X T∥4
F≤
Cd2
T,β andE∥XC∥4
F≤Cd 2
C,β. SinceI Ec
tr≤I{∥XT∥F >CT,x}+I{∥X C∥F >CC,x}, we need to control
both own-tail and cross-tail terms. The own-tail terms are bounded by the previous integrated tail estimate.
For the cross-tail terms, the Cauchy–Schwarz inequality gives
E

∥XT∥2
F I{∥XC∥F >CC,x}

≤{E∥XT∥4
F}1/2P(∥XC∥F >CC,x)1/2≤CdT,βe−cun/2,
and similarlyE[∥XC∥2
F I{∥XT∥F >CT,x}]≤Cd C,βe−cun/2. Combining the own-tail and cross-tail bounds,
we have
E{∥XT∥2
F IEc
tr}+E{∥XC∥2
F IEc
tr}≤C(d T,β +dC,β)une−cun +C(dT,β +dC,β)e−cun/2.
SincedT,β +dC,β≤d + andu ne−cun≤Ce−cun/2, the right-hand side is bounded byCd +e−cun/2. By the
choiceu n =A 0 log(nd+), we haved +e−cun/2 =d +(nd+)−cA0/2 =n−cA0/2d1−cA0/2
+ . Again, choosingA 0
sufficiently large so thatcA 0/2≥3, and usingd +≥1, it follows for sufficiently largenthatCd +e−cun/2≤
n−2. Therefore, we haveE{∥XT∥2
F IEc
tr}+E{∥XC∥2
F IEc
tr}≤n −2. As a result, the selected radii satisfy
P(Ec
tr)≤(3n 2)−1,E{∥X T∥2
F IEc
tr}+E{∥XC∥2
F IEc
tr}≤n −2.
Then, defineℓ tr(X0;s) =ℓ(X 0;s)IEtr,L tr
mask(s) =Eℓ tr(X0;s), and bLtr
mask(s) = 1
n
Pn
i=1ℓtr(X(i)
0 ;s).
Lets◦ =sA•,ω0,¯θ be the approximator from Theorem 3.1, and letE tr,n =Tn
i=1Etr,i, whereE tr,i denotes
Etr for the sampleX (i)
0 . The eventE tr,n is introduced to transfer the empirical optimality ofbsfrom the
original empirical loss to the truncated empirical loss. Indeed,bsminimizes bLmask, while the empirical
process argument below is applied to the truncated loss class. OnE tr,n, every training sample lies in the
truncation set. Consequently, we havebLtr
mask(s) =bLmask(s), for alls∈S MT.

ec10 e-companion toKong et al.:Conditional Tensor Diffusion
Therefore, onE tr,n, the empirical minimizerbsalso satisfies the truncated empirical optimality inequality
bLtr
mask(bs) =bLmask(bs)≤bLmask(s◦) =bLtr
mask(s◦). Using this inequality, we obtain the deterministic raw-loss
decomposition
Lmask(bs) =

Lmask(bs)−Ltr
mask(bs)
 
+L tr
mask(bs)
=

Lmask(bs)−Ltr
mask(bs)
 
+
n
Ltr
mask(bs)−(1 +a)bLtr
mask(bs)
o
+ (1 +a)bLtr
mask(bs)
≤

Lmask(bs)−Ltr
mask(bs)
 
+
n
Ltr
mask(bs)−(1 +a)bLtr
mask(bs)
o
+ (1 +a)bLtr
mask(s◦)
=

Lmask(bs)−Ltr
mask(bs)
 
| {z }
Etrunc
+
n
Ltr
mask(bs)−(1 +a)bLtr
mask(bs)
o
| {z }
Estat,1
+ (1 +a)
n
bLtr
mask(s◦)−(1 +a)L tr
mask(s◦)
o
| {z }
Estat,2
+(1 +a)2Ltr
mask(s◦)
≤E trunc +E stat,1 + (1 +a)Estat,2 + (1 +a)2Lmask(s◦)| {z }
Eapp
,(EC.2.7)
where the last inequality usesL tr
mask(s◦)≤L mask(s◦).
Step 1: statistical error for the truncated raw loss.We first derive an upper bound forℓ tr. Fors=s Γ,ω,θ,
let
Wσ :=

ω= (ωdj) :σ 2
min≤ωdj≤σ 2
max, d∈[D], j∈[p d]
 
.
Sinces(xT,t,xC,t) = ΛT,t (ω){Γ⊗ζθ(gt(Γ,ω),t)−x T,t}, we have
s(xT,t,xC,t)−r t(xT,xT,t ) = ΛT,t (ω)Γ⊗ζθ(gt(Γ,ω),t) +{h −1
t MT−ΛT,t (ω)}xT,t−αth−1
t xT.
(EC.2.8)
For allω∈W σ,∥ΛT,t (ω)∥op≤h−1
t , and∥h−1
t MT−ΛT,t (ω)∥op≤Cp−βh−2
t . Indeed, each diagonal entry
sofΣ ⊗
e (ω)lies in[σ 2D
min,σ 2D
max], so thath−1
t −(ht +α 2
tp−βs)−1 =α 2
tp−βs/[ht(ht +α 2
tp−βs)]≤Cp −βh−2
t .
Then, using∥ζ θ∥2≤Kand∥x T∥2≤CT,x onE tr, we obtain
∥s(XT,t,XC,t)−r t(XT,XT,t )∥2≤K+C T,x
ht
+C p−β∥XT,t∥2
h2
t
.
Moreover, we haveE(∥XT,t∥2
2|X 0)≤C 2
T,x +pTht onE tr. Therefore
sup
s∈SMT
sup
X0
ℓtr(X0;s)≤B ℓ,mask := 1 + C
T−t 0
Z T
t0
K2 +C 2
T,x
h2
t
+p−2βC2
T,x
h4
t
+pTp−2β
h3
t

dt.(EC.2.9)
For the Ornstein–Uhlenbeck schedule,h t = 1−α 2
t is comparable totnear zero and is bounded away
from zero fortaway from zero. Sincet 0≤1, there exists a constantc h>0such thath t≥c ht0 fort∈
[t0,T]. Together with the early-stopping conditionp −β≤c 0t0, this impliesp −β≤Ch t fort∈[t 0,T]. We
now simplify the three terms in the integrand of (EC.2.9). By the choice of the truncation radius, we have
C2
T,x = eO(dT,β ). Moreover, Theorem 3.1 givesK 2 =O{(K 0 +LgRϵ)2}=O{K 2
0 +L 2
g log[ctailr/(t0ϵ)]}.
SinceK 0 andL g are treated as fixed model constants and eO(·)hides logarithmic factors inr,t −1
0 ,ϵ−1 and
n, this term is eO(1). Therefore, becausedT,β =r+p Tp−β≥1, we haveK 2 +C 2
T,x = eO(dT,β ).

e-companion toKong et al.:Conditional Tensor Diffusionec11
For the second term in (EC.2.9), the boundp−β≤Ch t givesh−4
t p−2βC2
T,x≤Ch−2
t C2
T,x = eO(h−2
t dT,β ).
For the last term, usingp Tp−β≤dT,β andp−β≤Ch t, we obtainh −3
t pTp−2β = [h−2
t pTp−β][h−1
t p−β]≤
Ch−2
t dT,β . Thus, the whole integrand in (EC.2.9) is bounded by eO(dT,βh−2
t ). Consequently,
Bℓ,mask≤ eO
 dT,β
T−t 0
Z T
t0
h−2
t dt

.(EC.2.10)
The bound(T−t 0)−1RT
t0
h−2
t dt≤C(t −1
0 +T)follows by splitting[t 0,T]at1. On[t 0,1∧T],h t≍t, whereas
ht≍1on[1,T]whenT >1. Hence, the two contributions are bounded byCt −1
0 andCT, respectively.
Therefore
Bℓ,mask≤ eO

dT,β
 1
t0
+T

.(EC.2.11)
Following the parameter-covering reduction in Guo et al. (2026), we cover the truncated loss classG tr =
{ℓtr(·;s) :s∈S MT}. Since the loss integrates out the unbounded Gaussian variableX T,t|XT , the inter-
mediate score metric is defined using the same conditional second moment. We begin with a parameter
perturbation bound. Lets Γ,ω,θ ands eΓ,eω,eθ be two elements ofS MT, and write∆ Γ = maxd∈[D]∥Γd−eΓd∥op,
∆ω = maxd∈[D],j∈[pd]|ωdj−eωdj|. Denote the admissible loading–variance parameter set by
PΓ,ω :=
(
(Γ,ω) : Γ⊤
d Γd =Ird, d∈[D], ω∈W σ,sup
t∈[t0,T]
∥Vt(Γ,ω)∥ op≤CV
)
.
Thus, the loading–variance components of both parameter triples belong toP Γ,ω. The telescoping identity
ΓD⊗···⊗Γ 1−eΓD⊗···⊗ eΓ1 =
DX
d=1
eΓD⊗···⊗ eΓd+1⊗(Γd−eΓd)⊗Γ d−1⊗···⊗Γ 1
and∥Γ d∥op =∥eΓd∥op = 1imply
∥Γ⊗−eΓ⊗∥op≤D∆ Γ.(EC.2.12)
For a tensor indexj= (j 1,...,j D), sets j(ω) =QD
d=1ωdjd. A second telescoping identity gives|sj(ω)−
sj(eω)|≤Cσ∆ω, whereC σ depends only onD,σ min,σ max. On a treatment coordinate, the correspond-
ing precision is{h t +α 2
tp−βsj(ω)}−1. Hence, we have|[h t +α 2
tp−βsj(ω)]−1−[ht +α 2
tp−βsj(eω)]−1|≤
Cp−βh−2
t ∆ω. On a control coordinate, the precision isp β/sj(ω), and the lower variance bound gives

pβ
sj(ω)− pβ
sj(eω)
≤Cp β∆ω.
Since all precision matrices are diagonal, these entry-wise bounds are also operator-norm bounds. Thus
∥ΛT,t (ω)−Λ T,t (eω)∥op≤Cp−βh−2
t ∆ω,∥Λ C(ω)−Λ C(eω)∥op≤Cp β∆ω.(EC.2.13)
In addition, we shall have
∥ΛT,t (ω)∥op≤h−1
t ,∥Λ C(ω)∥op≤Cp β.(EC.2.14)
For the matricesHandV t, adding and subtractingeΓ⊤
⊗ΛT,t (ω)Γ⊗ andeΓ⊤
⊗ΛT,t (eω)Γ⊗ gives
HT,t (Γ,ω)−H T,t (eΓ,eω) = (Γ⊗−eΓ⊗)⊤ΛT,t (ω)Γ⊗ +eΓ⊤
⊗{ΛT,t (ω)−ΛT,t (eω)}Γ⊗ +eΓ⊤
⊗ΛT,t (eω)(Γ⊗−eΓ⊗).

ec12 e-companion toKong et al.:Conditional Tensor Diffusion
Equations (EC.2.12)– (EC.2.14) therefore imply
∥HT,t (Γ,ω)−H T,t (eΓ,eω)∥op≤C{h−1
t ∆Γ +p−βh−2
t ∆ω},(EC.2.15)
∥HC(Γ,ω)−H C(eΓ,eω)∥op≤Cp β(∆Γ + ∆ω).(EC.2.16)
DefineB t(Γ,ω) =H T,t (Γ,ω) +α −2
t HC(Γ,ω)andV t(Γ,ω) =B t(Γ,ω)−1. Both loading–variance pairs
belong toP Γ,ω, so the two inverses exist and have an operator norm of at mostC V . The inverse identity
Vt(Γ,ω)−V t(eΓ,eω) =Vt(Γ,ω){Bt(eΓ,eω)−Bt(Γ,ω)}Vt(eΓ,eω)and (EC.2.15)–(EC.2.16) yield
∥Vt(Γ,ω)−V t(eΓ,eω)∥op≤LV (t)(∆Γ + ∆ω),whereL V (t) =CC 2
V{h−1
t +p−βh−2
t +α−2
t pβ}.
(EC.2.17)
For the low-dimensional encoder, defineaenc
t (Γ,ω) = Γ⊤
⊗ΛT,t (ω)XT,t +α−1
t Γ⊤
⊗ΛC(ω)XC andgt(Γ,ω) =
Vt(Γ,ω)a enc
t (Γ,ω). OnE tr, setQT (t) ={C 2
T,x +pTht}1/2. The forward transition gives

E(∥XT,t∥2
2|XT )
 1/2
≤QT (t).(EC.2.18)
By Minkowski’s inequality and (EC.2.14), we have

EXT,t|XT∥aenc
t (Γ,ω)∥ 2
2
 1/2
≤Ga(t), G a(t) =h−1
t QT (t) +Cα−1
t pβCC,x.(EC.2.19)
To compare the two encoder inputs, we first decompose the treated-region branch as
Γ⊤
⊗ΛT,t (ω)XT,t−eΓ⊤
⊗ΛT,t (eω)XT,t = (Γ⊗−eΓ⊗)⊤ΛT,t (ω)XT,t +eΓ⊤
⊗{ΛT,t (ω)−Λ T,t (eω)}XT,t.
The control branch satisfies the corresponding identity
α−1
t Γ⊤
⊗ΛC(ω)XC−α−1
t eΓ⊤
⊗ΛC(eω)XC =α−1
t (Γ⊗−eΓ⊗)⊤ΛC(ω)XC +α−1
t eΓ⊤
⊗{ΛC(ω)−Λ C(eω)}XC.
Equations (EC.2.12)– (EC.2.18) then give
n
EXT,t|XT∥aenc
t (Γ,ω)−a enc
t (eΓ,eω)∥2
2
o1/2
≤La(t)(∆Γ + ∆ω),where (EC.2.20)
La(t) =C

{h−1
t +p−βh−2
t }QT (t) +α−1
t pβCC,x

.(EC.2.21)
Finally, add and subtractVt(eΓ,eω)aenc
t (Γ,ω)to obtain
gt(Γ,ω)−g t(eΓ,eω) ={Vt(Γ,ω)−V t(eΓ,eω)}aenc
t (Γ,ω) +Vt(eΓ,eω){aenc
t (Γ,ω)−a enc
t (eΓ,eω)}.
Combining (EC.2.17), (EC.2.19), and (EC.2.20) yields
sup
X0∈Etr
n
EXT,t|XT∥gt(Γ,ω)−g t(eΓ,eω)∥2
2
o1/2
≤L enc(t)(∆Γ + ∆ω),(EC.2.22)
sup
(Γ,ω)∈PΓ,ω
sup
X0∈Etr

EXT,t|XT∥gt(Γ,ω)∥ 2
2
 1/2
≤G enc(t),where (EC.2.23)
Lenc(t) =LV (t)Ga(t) +CVLa(t), G enc(t) =CVGa(t).(EC.2.24)
These bounds are finite in the conditionalL 2 metric.

e-companion toKong et al.:Conditional Tensor Diffusionec13
The network depth is included as a discrete index in the cover below, so it suffices to compare two
networks of a common depth ¯L≤L. Pad every hidden layer to a width ofm. Enlargingmtom∨(r+ 1),
if necessary, does not change its order and ensures that every layer dimension is at mostm. For a common
inputz 0 = (g⊤,t)⊤, writez ℓ =ρ(W ℓzℓ−1 +bℓ),1≤ℓ< ¯Landζ θ(g,t) =W ¯Lz¯L−1 +b ¯L, and defineezℓ
analogously. Putδθ =∥θ− eθ∥∞. Since every matrix has at mostmrows and columns, and every parameter
is bounded byκ, we have∥W ℓ∥op∨∥fWℓ∥op≤mκand∥W ℓ−fWℓ∥op +∥bℓ−ebℓ∥2≤2mδθ. Because ReLU
is1-Lipschitz, the activations satisfy the two recursions
∥zℓ∥2≤(m+ 1)(1∨κ){1 +∥z ℓ−1∥2},∥z ℓ−ezℓ∥2≤mκ∥zℓ−1−ezℓ−1∥2 + 2mδθ{1 +∥zℓ−1∥2}.
LetM κ = (m+ 1)(1∨κ), which is at least2. Starting fromz 0 =ez0, induction over the preceding recur-
sions gives∥zℓ∥2≤2M ℓ
κ{1 +∥z0∥2}and∥z ℓ−ezℓ∥2≤Cℓ(m+ 1)M ℓ−1
κ {1 +∥z0∥2}δθ. Applying the same
difference decomposition to the final affine layer therefore gives
∥ζθ(g,t)−ζ eθ(g,t)∥ 2≤L net
θ (1 +|t|+∥g∥ 2)δθ,(EC.2.25)
where the following uniform choice is valid for every ¯L≤L:
Lnet
θ =CL 2(m+ 1)L+2(1∨κ) L.(EC.2.26)
For different encoder and network parameters, insert the intermediate termζ θ(gt(eΓ,eω),t). The global
input Lipschitz constraint inF core and (EC.2.25) imply
∥ζθ(gt(Γ,ω),t)−ζ eθ(gt(eΓ,eω),t)∥2≤γg∥gt(Γ,ω)−g t(eΓ,eω)∥2 +L net
θ {1 +T+∥g t(eΓ,eω)∥2}δθ.
Taking the conditionalL 2 norm and applying (EC.2.22)–(EC.2.23) yields
sup
X0∈Etr
n
EXT,t|XT∥ζθ(gt(Γ,ω),t)−ζ eθ(gt(eΓ,eω),t)∥2
2
o1/2
≤L core(t)(∆Γ + ∆ω +δθ),(EC.2.27)
whereL core(t) =γgLenc(t) +Lnet
θ {1 +T+G enc(t)}.
For the score output itself, writeg=g t(Γ,ω)andeg=g t(eΓ,eω). Then we have
sΓ,ω,θ(xT,t,xC,t)−s eΓ,eω,eθ(xT,t,xC,t) ={ΛT,t (ω)−Λ T,t (eω)}{Γ⊗ζθ(g,t)−x T,t}
+ ΛT,t (eω)(Γ⊗−eΓ⊗)ζθ(g,t) + ΛT,t (eω)eΓ⊗{ζθ(g,t)−ζ eθ(eg,t)}.
By (EC.2.13),∥Γ⊗ζθ(g,t)∥ 2≤K, and (EC.2.18), the first term satisfies
n
EXT,t|XT∥{ΛT,t (ω)−Λ T,t (eω)}{Γ⊗ζθ(g,t)−X T,t}∥
2
2
o1/2
≤Cp−βh−2
t {K+Q T (t)}∆ω.
For the second term, Equations (EC.2.12) and (EC.2.14) give∥ΛT,t (eω)(Γ⊗−eΓ⊗)ζθ(g,t)∥ 2≤Ch−1
t K∆Γ.
Finally, (EC.2.14) and (EC.2.27) give

EXT,t|XT

ΛT,t (eω)eΓ⊗{ζθ(g,t)−ζ eθ(eg,t)}

2
2
1/2
≤h−1
t Lcore(t)(∆Γ + ∆ω +δθ).
Consequently, we have
sup
X0∈Etr

EXT,t|XT∥sΓ,ω,θ(XT,t,XC,t)−s eΓ,eω,eθ(XT,t,XC,t)∥ 2
2
 1/2
≤Ls(t)(∆Γ + ∆ω +δθ),(EC.2.28)

ec14 e-companion toKong et al.:Conditional Tensor Diffusion
Ls(t) =C

p−βh−2
t {K+Q T (t)}+h−1
t K+h −1
t Lcore(t)

, Ls = sup
t∈[t0,T]
Ls(t)(EC.2.29)
The supremum above is finite becauset 0>0,α T >0, and all members of the score class satisfy the
uniformC V ,K, and parameter bounds. Define the time-averaged score metric
ds
av(s,es) = sup
X0∈Etr
 1
T−t 0
Z T
t0
EXT,t|XT∥s(XT,t,XC,t)−es(XT,t,XC,t)∥ 2
2dt
1/2
.
Then we haved s
av(sΓ,ω,θ,s eΓ,eω,eθ)≤ Ls(∆Γ + ∆ω +δ θ). ForR s(XT,t,XC,t) =s(X T,t,XC,t)−
rt(XT,XT,t ), recall that
1
T−t 0
Z T
t0
EXT,t|XT∥Rs(XT,t,XC,t)∥ 2
2dt≤B ℓ,mask
onE tr, uniformly ins. Defined ℓ
∞ byd ℓ
∞{ℓtr(·;s),ℓ tr(·;es)}= supX0|ℓtr(X0;s)−ℓ tr(X0;es)|. Then, since
|∥Rs∥2
2−∥R es∥2
2|≤(∥R s∥2 +∥R es∥2)∥s−es∥2, the difference of the two truncated losses is zero outsideEtr,
and the Cauchy–Schwarz inequality in the time-forward expectation gives
|ℓtr(X0;s)−ℓ tr(X0;es)|= IEtr
T−t 0

Z T
t0
EXT,t|XT{∥Rs∥2
2−∥R es∥2
2}dt

≤
 1
T−t 0
Z T
t0
EXT,t|XT{∥Rs∥2 +∥R es∥2}2dt
1/2
ds
av(s,es)≤2B1/2
ℓ,maskds
av(s,es),
uniformly overX 0∈E tr, where the last step uses(a+b) 2≤2a 2 + 2b2 and the definition ofB ℓ,mask for
each ofsandes. Hence, we haved ℓ
∞{ℓtr(·;s),ℓ tr(·;es)}≤2B1/2
ℓ,maskds
av(s,es). Letτℓ =Bℓ,mask/nand choose
τs =τℓ/(4B1/2
ℓ,mask). It is enough to construct aτ s-cover of the score class underd s
av, because such a cover
gives a loss-cover radius of at mostτℓ. By (EC.2.28), it suffices to take
τΓ = τs
3Ls
, τ ω = τs
3Ls
, τ θ = τs
3Ls
for the loading, variance, and core-network parameter covers, respectively.
It remains to calculate the three parameter covering numbers. Under the metricmaxd∥Γd−eΓd∥op, a prod-
uct ofτ Γ/2-covers of the individual Stiefel manifolds is aτ Γ/2-cover of the loading space. The volumetric
bound forSt(p d,rd)in Lemma 8 of?, together with∥A∥ op≤∥A∥F , gives
logN
τΓ
2 ,{Γ⊤
d Γd =Ird}D
d=1,max
d
∥·∥ op

≤C
DX
d=1
pdrd log

1 +C
τΓ

≤Cp max log

1 +C
τΓ

,
becauseDand the mode ranks are fixed. Similarly,W σ is a bounded rectangle of dimension PD
d=1pd≤
Dpmax, so
logN
τω
2 ,Wσ,∥·∥ ∞

≤Cp max log

1 +C
τω

.
For the core network, writeΘ core for the set of parameter vectors satisfying the architecture, coefficient,
and sparsity constraints ofF core. For a fixed depth, pad all hidden layers to widthm, and letP θ be the
maximum number of weight and bias entries among the padded architectures. Since the input and output

e-companion toKong et al.:Conditional Tensor Diffusionec15
dimensions are fixed atr+ 1andr, respectively, we haveP θ≤CL(m+ 1) 2. PutJ θ =J∧P θ. Since the
architecture budgets are positive,1≤J θ≤Pθ, and
JθX
j=0
Pθ
j

≤
ePθ
Jθ
Jθ
.
For a fixed support of cardinality at mostJ θ, the active parameters lie in[−κ,κ] Jθ, which admits anℓ ∞-
cover of radiusτθ/2with at most{1 + 4κ/τθ}Jθ elements. Taking the union over the admissible depths and
supports therefore gives
logN
τθ
2,Θ core,∥·∥ ∞

≤logL+CJ θ log
ePθ
Jθ

+CJθ log

1 +Cκ
τθ

.
The preceding parameter covers may have centers outsideS MT, because the inverse and global network
constraints need not be preserved by coordinate discretization. Fix an ordering of the centers in each half-
radius cover and assign every admissible parameter to the first center whose covering ball contains it.
Together with the network depth, the three resulting center indices partitionS MT into no more cells than
the product of the three covering numbers. From every nonempty cell, select one admissible parameter
triple. Two triples assigned to the same cell are withinτ Γ,τ ω, andτ θ in the loading, variance, and network
metrics, respectively. It follows from (EC.2.28) that their score distance is at mostτ s. The selected triples
therefore form an internalτs-cover ofS MT; in particular, every center satisfies the defining bound onVt and
the common loss envelopeBℓ,mask.
Multiplying the three parameter covering numbers gives
logN(τ ℓ,G tr,dℓ
∞)≤Cp max log

1 +C
τΓ

+Cp max log

1 +C
τω

+ logL
+CJθ log
ePθ
Jθ

+CJθ log

1 +Cκ
τθ

.(EC.2.30)
Since
τs =B1/2
ℓ,mask
4n , τ Γ =τω =τθ =B1/2
ℓ,mask
12nLs
,
each metric-entropy logarithm in (EC.2.30) is bounded by a constant multiple oflog(nΞ mask), where we
may take
Ξmask = 2 +Ls +Pθ +κ+L+B −1/2
ℓ,mask.(EC.2.31)
Indeed,h −1
t0 ≤Ct −1
0 ,p β≤p≤p D
max, andp T ≤p D
max. The definitions (EC.2.17), (EC.2.21), (EC.2.24),
(EC.2.26), and (EC.2.29) imply
log Ξmask≤C

1 + log(1 +CV ) + log{1 +B−1/2
ℓ,mask}+ log(1 +K+C T,x +CC,x)
+ log(1 +pmax) + log(t−1
0 ) + log(α−1
T ) + log(1 +L) +Llog{(m+ 1)(1∨κ)}

.
Under the configuration of Theorem 3.1 and the chosen truncation radii, the right-hand side consists only
of polylogarithmic factors in the quantities suppressed by eO. Consequently,log Ξ mask is absorbed into the
logarithmic factor in the statistical rate. SinceJθ≤J, we conclude that
logN(τ ℓ,G tr,dℓ
∞)≤C{J+p max}log(nΞ mask),(EC.2.32)

ec16 e-companion toKong et al.:Conditional Tensor Diffusion
where the contributionJcomes from the core network cover, while the contributionp max comes from the
finite-dimensional loading and variance parameter covers;Dand the ranksr d are treated as fixed.
WritePg=Eg(X 0)andP ng=n −1Pn
i=1g(X (i)
0 ). Since everyg∈G tr takes values in[0,B ℓ,mask], the
two one-sided relative-deviation inequalities in Lemma 15 of Chen et al. (2023) imply
sup
g∈Gtr
{Pg−(1 +a)P ng}∨sup
g∈Gtr
{Png−(1 +a)Pg}≤ CBℓ,mask
na

logN(τ ℓ,G tr,dℓ
∞) + log(2/δ)

+Cτℓ.
with probability at least1−δ, where the two directions are assigned a failure probability ofδ/2. This is
the relative empirical-process reduction used in the proof of the score-estimation theorem of Guo et al.
(2026). Substitutingτℓ =Bℓ,mask/nand (EC.2.32), the following inequalities therefore hold simultaneously
for everys∈S MT:L tr
mask(s)≤(1 +a) bLtr
mask(s) + ∆stat and bLtr
mask(s)≤(1 +a)L tr
mask(s) + ∆stat, where
∆stat≤CBℓ,mask
na [{J+p max}log(nΞ mask) + log(2/δ)] +CBℓ,mask
n .(EC.2.33)
The first term in∆ stat is the relative empirical-process contribution, and the finalCB ℓ,mask/nis the dis-
cretization contribution.
Step 2: truncation error.The residual identity (EC.2.8) gives, without imposingE tr,
∥s(XT,t,XC,t)−r t(XT,XT,t )∥2
2≤C
K2 +∥XT∥2
2
h2
t
+p−2β∥XT,t∥2
2
h4
t

.
Here, the right-hand side is independent of the particular core network except through the uniform output
boundK. SinceE(∥X T,t∥2
2|X 0)≤C∥X T∥2
2 +pTht, we have uniformly overs∈S MT that
Lmask(s)−L tr
mask(s)
≤ C
T−t 0
Z T
t0
"
K2P(Ec
tr) +E{∥XT∥2
2IEc
tr}
h2
t
+p−2βE{∥XT∥2
2IEc
tr}
h4
t
+pTp−2βhtP(Ec
tr)
h4
t
#
dt.
The selected radii inE tr satisfyP(E c
tr)≤(3n 2)−1 andE{∥XT∥2
2IEc
tr}≤n −2. Substituting these two esti-
mates gives
Lmask(s)−L tr
mask(s)≤ C
n2(T−t 0)
Z T
t0
K2 + 1
h2
t
+p−2β
h4
t
+pTp−2βht
h4
t

dt.
This last integral is dominated term-by-term by the deterministic envelope in (EC.2.9):K 2 + 1≤C(K 2 +
C2
T,x ),p−2β≤p−2βC2
T,x sinceC 2
T,x≥1fornsufficiently large, and the finalp Tp−2βht/h4
t term is exactly
the third envelope term. Sincen−2≤n−1, the preceding display is bounded byCB ℓ,mask/n. Hence
∆tr := sup
s∈SMT
{Lmask(s)−L tr
mask(s)}≤ CBℓ,mask
n .(EC.2.34)
Moreover, we have
P
 n\
i=1
Etr,i
!
≥1−
nX
i=1
P(Ec
tr,i)≥1− 1
3n,
and on this event bLtr
mask(s) =bLmask(s)for alls.
Step 3: approximation term and raw-loss oracle inequality.LetA stat be the concentration event from
Step 1 and letA tr =∩n
i=1Etr,i be the sample truncation event from Step 2. OnAstat∩A tr, the two statistical

e-companion toKong et al.:Conditional Tensor Diffusionec17
terms in (EC.2.7) are at most∆ stat, the truncation term is at most∆ tr, and the empirical optimality used in
that decomposition is valid. Consequently,
Lmask(bs)≤(1 +a)2Lmask(s◦) + (2 +a)∆stat + ∆tr.(EC.2.35)
Step 4: conversion from the DSM loss to score risk.Finally, letst(xT,t|xC) =∇xT,t logpt(xT,t|xC). For
fixedt,r t(XT,XT,t )is the score of the forward Gaussian kernelp(XT,t|XT )with respect to the treatment
coordinateXT,t . Therefore, the usual denoising identity givesst(XT,t|XC) =E{rt(XT,XT,t )|X T,t,XC}.
This identity is the conditional version of theL 2-projection property of denoising score matching. To use
it, writes−r t = (s−s t) + (st−rt). For every square-integrables, expanding the square and conditioning
on(XT,t,XC)yields
EXC EXT|XC EXT,t|XT∥s(XT,t,XC,t)−r t(XT,XT,t )∥2
2 =EXC EXT,t|XC∥s(XT,t,XC,t)−s t(XT,t|XC)∥2
2
+EXC EXT|XC EXT,t|XT∥rt(XT,XT,t )−s t(XT,t|XC)∥2
2.
Indeed, the cross term is2E[⟨s(X T,t,XC,t)−s t(XT,t |X C),st(XT,t |X C)−r t(XT,XT,t )⟩], which
vanishes becauseE{r t−s t|XT,t,XC}= 0. Integrating over time, we obtain the exact decomposition
Lmask(s) =R mask(s) +CDSM, where
CDSM = 1
T−t 0
Z T
t0
EXC EXT|XC EXT,t|XT∥rt(XT,XT,t )−s t(XT,t|XC)∥2
2dt,and
Rmask(s) = (T−t 0)−1
Z T
t0
EXC EXT,t|XC∥s(XT,t,XC,t)−∇ xT,t logpt(XT,t|XC)∥2
2dt.
Note thatC DSM does not depend ons. Applying this identity to the raw oracle inequality (EC.2.35) yields
Rmask(bs)≤(1 +a)2Rmask(s◦) +{(1 +a) 2−1}C DSM + (2 +a)∆stat + ∆tr.(EC.2.36)
The term{(1 +a) 2−1}C DSM results from the multiplicative raw-loss inequality. We next bound
CDSM, which is independent ofs. By the exact score decomposition, we know thats t(XT,t |XC) =
ΛT,t{A⊗ξ(gt,t)−X T,t}. Hence,
rt−st =αth−1
t XT−h−1
t XT,t−ΛT,tA⊗ξ(gt,t) + ΛT,tXT,t
=αth−1
t XT−{h−1
t MT−ΛT,t}XT,t−ΛT,tA⊗ξ(gt,t).
The same precision-difference bound used in (EC.2.8) gives∥h −1
t MT −ΛT,t∥op≤Cp −βh−2
t . By
Jensen’s inequality and the definitionξ(g t,t) =E(α tf|g t), we haveE∥ξ(g t,t)∥ 2
2≤E∥αtf∥ 2
2≤E∥f∥ 2
2≤
Cr. Also,E∥XT∥2
2≤CdT,β , whileE∥XT,t∥2
2≤C(dT,β +pTht). Using(a+b+c) 2≤3(a 2 +b 2 +c 2), the
three pieces inr t−st are bounded as follows:
E∥αth−1
t XT∥2
2≤CdT,βh−2
t ,E∥{h −1
t MT−ΛT,t}XT,t∥2
2≤Cp−2βh−4
t (dT,β +pTht),
andE∥Λ T,tA⊗ξ(gt,t)∥ 2
2≤Ch−2
t ≤CdT,βh−2
t ,
where the last inequality usesdT,β≥1. After time averaging, these bounds imply
CDSM≤C
 dT,β
T−t 0
Z T
t0
h−2
t dt+ dT,βp−2β
T−t 0
Z T
t0
h−4
t dt+ pTp−2β
T−t 0
Z T
t0
h−3
t dt

.

ec18 e-companion toKong et al.:Conditional Tensor Diffusion
Underp −β≤c 0t0, the same argument used in the envelope bound givesp −β≤Ch t for allt∈[t 0,T].
Therefore , the second term in the preceding display satisfiesdT,βp−2βh−4
t ≤CdT,βh−2
t , and the third term
satisfiespTp−2βh−3
t =pTp−βh−2
t (p−βh−1
t )≤Cd T,βh−2
t . Consequently, we have
CDSM≤C dT,β
T−t 0
Z T
t0
h−2
t dt≤Cd T,β
 1
t0
+T

.(EC.2.37)
Thus,C DSM/dT,β has the same time singularity as the statistical upper bound after the early-stopping nor-
malization.
Step 5: balancing.Theorem 3.1 givesR mask(s◦)≤(T−t 0)−1RT
t0
h−2
t (√r+ 1)2ϵ2dt. Setδ= 1/(3n)and
a=c aϵ2, wherec a>0is a small numerical constant. Sincea∈(0,1),(1 +a) 2≤4and(1 +a) 2−1≤3a.
Define
Cϵ := (1 +LgRϵ)r(1 +TLt)

1 + log

1 +K0 +LgRϵ
ϵ

.
The displayed choices ofmandLin Theorem 3.1 then giveJ=O{C ϵϵ−(r+1)}. SetL ϵ = log(nΞmask) +
log(6n). By (EC.2.11), (EC.2.33), andδ= 1/(3n), we have
∆stat
dT,β
≤ eO
 1
t0
+T
{Cϵϵ−(r+1) +p max}Lϵ
nϵ2 + 1
n

,
wherea −1 =c −1
a ϵ−2. The estimate following (EC.2.31) shows thatL ϵ is polylogarithmic in
{t−1
0 ,ϵ−1,α−1
T ,p max,n}under the network configuration of Theorem 3.1. In particular, the layerwise factor
(m+ 1)L+2(1∨κ) L enters only throughlogL net
θ ≤C[log(1 +L) +Llog{(m+ 1)(1∨κ)}], and therefore
introduces no additional polynomial dependence onϵ −1 orp max. The truncation bound (EC.2.34) gives
d−1
T,β ∆tr = eO{n−1t−1
0 +n−1T},which is dominated by the preceding statistical bound becauseϵ∈(0,1),
Cϵϵ−(r+1) +p max≥1, andL ϵ≥1. For the approximation term, Theorem 3.1 gives the pointwise bound
EXC EXT,t|XC
h
∥s◦(XT,t,XC,t)−s t(XT,t|XC)∥
2
2
i
≤Ch−2
t ϵ2.
Asris treated as fixed, integration and (EC.2.37) give
Rmask(s◦)
dT,β
≤ eO
 1
t0
+T

ϵ2

, aCDSM
dT,β
≤ eO
 1
t0
+T

ϵ2.

Thus, the oracle inequality (EC.2.36), after division bydT,β , gives
Rmask(bs)
dT,β
≤ eO
 1
t0
+T

ϵ2 +{Cϵϵ−(r+1) +p max}Lϵ
nϵ2

.
The concentration event has a probability of at least1−δ, while the sample truncation event has a probability
of at least1−1/(3n). Withδ= 1/(3n), a union bound gives a failure probability of at most2/(3n)≤
1/n. Hence, the displayed bound holds with a probability of at least1−1/n. Finally, the choice ofϵ
givesϵ 2 =n−(2−2δn)/(r+5). By the definition ofC ϵ, the identityR 2
ϵ =O{log((t 0ϵ)−1)},T= 2 log(α −1
T ),
and the bound following (EC.2.31), the explicitn-logarithmic order, apart from the polylogarithmic factors
already suppressed in the theorem, can be stated precisely as follows: there is a factorΠ n, polynomial in
log(1 +t−1
0 ),log(1 +p max), andlog(1 +α −1
T ), such thatC ϵLϵ≤CΠ n(logn) (r+8)/2. Moreover,n −δn =
(logn)−(r+12)/2. Consequently,(nϵ 2)−1Cϵϵ−(r+1)Lϵ =ϵ 2CϵLϵn−δn =O{Π nϵ2(logn)−2}= eO(ϵ2). Hence,

e-companion toKong et al.:Conditional Tensor Diffusionec19
the enlarged covering-number bound does not alter the polynomial balance between approximation and
statistical error. Moreover, we have(nϵ 2)−1pmaxLϵ = eO(pmaxn−r+3+2δn
r+5 ); substitution into the preceding
oracle bound proves (3.14).
□
EC.2.4. Proof of Theorem 4.1
Proof.For a sufficiently largeC β, the choices in the theorem implyc−1
0 p−β<t 0. Moreover,T−t 0≥cT
for all sufficiently largen. Hence, Theorem 3.2 applies. On the event given in Theorem 3.2, we can fix the
training sample and hencebs. FixxC in the full-measure set considered below. On reverse time[0,T−t 0],
letP x,ePx, andQ x be, respectively, the path laws of the exact-score process initialized fromP T
T (·|x C),
the estimated-score process initialized from the same law, and the trained process initialized fromγ T =
N(0,I pT ). Their endpoint laws areP T
t0 (·|x C), ePT
t0 (·|x C), and bPT
t0 (·|x C).
We first control the score-estimation term. Lets t(xT,t |xC) =∇ xT,t logpt(xT,t |xC). We verify the
square-integrability required below. The DSM projection identity in Step 4 of the proof of Theorem 3.2 and
Jensen’s inequality give
EXT,t|xC∥st(XT,t|xC)∥2
2≤E{∥rt(XT,XT,t )∥2
2|XC =xC}= pT
ht
.
Here the last equality follows becauser t =−h−1/2
t MTzt, wherez t∼N(0,I p)is independent ofX C.
Moreover, everys Γ,ω,θ∈S MT satisfies∥ΛT,t (ω)∥op≤h−1
t ,∥Γ⊗∥op = 1, and∥ζθ∥2≤K. Consequently,
EXT,t|xC∥bs(XT,t,xC,t)∥ 2
2≤Ch−2
t

K2 +E(∥XT∥2
2|XC =xC) +pTht
 
forPC-almost everyxC. SinceE(∥XT∥2
2|XC)<∞almost surely andh t≥ht0>0, the preceding bounds
implysupt∈[t0,T] EXT,t|xC∥bs(XT,t,xC,t)−s t(XT,t|xC)∥2
2<∞. Moreover, for fixedxC, every score inSMT
is globally Lipschitz with at most linear growth inxT,t on[t 0,T]. Hence, the estimated reverse SDE defines
a Markov kernel in the treated region.
Then, to apply the change-of-measure argument on a non-degenerate state space, letJ T∈Rp×pT be the
treated-region-coordinate selection matrix, so thatJ ⊤
TJT =I pT andJTJ⊤
T =MT . Every state and score
in the reverse process is supported onT. Thus, writey u =J ⊤
Tx←
T,u for the exact-score reverse process
andeyu =J ⊤
Tex←
T,u for the auxiliary reverse process, and setb t(y,xC) =J ⊤
Tst(JTy|x C)and bbt(y,xC) =
J⊤
Tbs(JTy,xC,t). The true and auxiliary reverse processes, in these coordinates, have the respective SDEs
dyu ={ 1
2yu +bT−u (yu,xC)}du+ dBu,dey u ={ 1
2eyu +bbT−u (eyu,xC)}du+ d eBu,
with the same initial law and a common identity diffusion coefficient;B u and eBu are standardp T -
dimensional Brownian motions. SinceJ T is an isometry between the treated region andR pT , relative
entropy and the squared drift difference are unchanged by this coordinate representation. Clearly, the pre-
ceding moment bounds verify the change-of-measure condition used in Lemma D.4 of Fu et al. (2024). The
first line below is the additive property of relative entropy under disintegration (?, Theorem 2.4), applied
to the initial-coordinate map. The second line is the localized Girsanov bound for the two path laws with a
common initial distribution (Girsanov 1960, F¨ollmer 2005, Fu et al. 2024):
KL(Px∥Qx) = KL(Px∥ePx) + KL

PT
T (·|x C)

γT
 

ec20 e-companion toKong et al.:Conditional Tensor Diffusion
≤ 1
2
Z T
t0
EXT,t|xC∥bs(XT,t,xC,t)−s t(XT,t|xC)∥2
2dt+ KL

PT
T (·|x C)

γT
 
.
The Girsanov bound is understood by first stopping when the accumulated squared drift difference reaches
a finite level and then passing to the limit by lower semicontinuity of relative entropy; thus the finite-energy
condition verified above suffices. Indeed, ePx andQ x use the same estimated reverse dynamics, so their
likelihood ratio depends only on the initial state. Data processing under the endpoint map (Csisz ´ar 1967)
and averaging overXC therefore yield
EXC KL
n
PT
t0 (·|X C)

bPT
t0 (·|X C)
o
≤ 1
2(T−t 0)Rmask(bs) +EXC KL

PT
T (·|X C)

γT
 
.
The definition ofR mask and Theorem 3.2 give
(T−t 0)Rmask(bs)
dT,β
≤ eO
 1
t0
+T
n
n− 2−2δn
r+5 +p maxn−r+3+2δn
r+5
o
,(EC.2.38)
where the factorT−t 0 is absorbed into the logarithmic term becauseT≍logn+ logp max.
It remains to bound the terminal relative-entropy term in (EC.2.38). The forward process for the miss-
ing outcomes is the Ornstein-Uhlenbeck process onR pT with invariant lawγ T . Before applying entropy
contraction pointwise inx C, we verify that its initial conditional relative entropy is finite almost surely.
Identifying the treated region withRpT , writexT =MTA⊗f+G T , whereGT∼N(0,p −β(Σ⊗
e )T ),(Σ⊗
e )T
is the treated-region principal submatrix andG T is independent of(f,X C). Conditional onX C =xC, the
law ofx T is therefore the convolution of the conditional distribution ofM TA⊗fwith the law ofG T .
More explicitly, ifY T has the conditional distribution ofM TA⊗fgivenX C =xC, thenh(Y T +GT )−
h(GT ) =I(YT ;YT +GT )≥0, where the identity uses the independence ofY T andGT . Indeed, the condi-
tional entropy and KL identities used next are integrable since Gaussian convolution bounds the conditional
entropy from below, while the finite conditional second moment, the Gaussian maximum-entropy bound,
and Jensen’s inequality control it from above after averaging overXC. Therefore,
h(xT|XC =xC)≥h(G T ) = 1
2 log

(2πe)pT (pβ)−pT det((Σ⊗
e )T )
 
,
andEXC E(∥xT∥2
2|XC) =E∥xT∥2
2≤C(r+p Tp−β). Using the identityKL(P∥γT ) = 1
2 EP∥X∥2
2−h(P) +
pT
2 log(2π), we obtain
EXCKL{PT
0 (·|X C)∥γT}= 1
2 E∥xT∥2
2−EXCh(xT|XC) +pT
2 log(2π)
≤C(r+p Tp−β)−h(GT ) +pT
2 log(2π).
Moreover, the eigenvalues ofΣ⊗
e are bounded above and below by fixed constants. Sincep≤p D
max andD
is fixed,
−h(GT ) +pT
2 log(2π) =pT
2 log(pβ)− pT
2 − 1
2 log det{(Σ⊗
e )T}
≤CpT{1 + log(pβ)}≤Cp T log(1 +pmax),
where the last two bounds use the fixed variance bounds andlog(pβ) =PD
d=1βd logpd≤Dlogp max. Com-
bining the preceding two displays gives
EXCKL{PT
0 (·|X C)∥γT}≤C{r+p T log(1 +pmax)}(EC.2.39)

e-companion toKong et al.:Conditional Tensor Diffusionec21
for a constant depending only on the fixed variance bounds and the core-factor tail constants. Since relative
entropy is nonnegative, (EC.2.39) impliesKL{P T
0 (·|x C)∥γT}<∞forP C-almost everyx C. For each
such context, the standard Ornstein–Uhlenbeck entropy contraction (Bakry et al. 2014) therefore applies
pointwise; see also the proof of Theorem 4.2 in Fu et al. (2024). Integrating that pointwise inequality and
using (EC.2.39) yields
EXCKL{PT
T (·|X C)∥γT}≤e −cT EXCKL{PT
0 (·|X C)∥γT}≤Ce −cT{r+pT log(1 +pmax)}.
SincepT≤p≤p D
max andDis fixed, takingC T sufficiently large inT=C T (logn+ logp max)gives directly
EXC KL

PT
T (·|X C)

γT
 
=o
 
dT,β R2
n

.
Finally, substitutet 0≍n−an into the score-estimation bound (EC.2.38). SinceT=C T (logn+logp max),
we have(1/t 0 +T) = eO(nan). For the first score-estimation term, we have
nann− 2−2δn
r+5 =n
− 5(1−δn)
3(r+5) ,
becausea n = (1−δ n)/{3(r+ 5)}. As for the second term, we have
nanpmaxn−r+3+2δn
r+5 =p maxn
− 3r+8+7δn
3(r+5) .
Combining these rates with (EC.2.38) proves (4.4).
□
EC.2.5. Proof of Corollaries 4.1 and 4.2
Proof.Fix a realization ofF tr inA n and condition onX 1:ne
C =x 1:ne
C . Forℓ= 1,...,n e, writeP ℓ =
PT
t0 (·|x (ℓ)
C )andQ ℓ = bPT
t0 (·|x (ℓ)
C ). LetJT∈Rp×pT select the positions in the treated region, withJ ⊤
TJT =
IpT andJTJ⊤
T =MT , and setwT =J⊤
Tw. Extend the aggregate notation to the forward process by defining
uℓ,t =J⊤
T vec(X(ℓ)
T,t )∈R pT, U w,ℓ,t =w⊤ vec(X(ℓ)
T,t ), V ne,w,t = 1
ne
neX
ℓ=1
Uw,ℓ,t.
Thus,U w,ℓ,t =w⊤
Tuℓ,t. Conditional independence gives the joint laws Nne
ℓ=1Pℓ and Nne
ℓ=1Qℓ. Relative
entropy is additive over product measures and contracts under measurable maps. Applying these properties
(Csisz´ar 1967) toΦ ne,w(u1,...,u ne) = (ne)−1/2Pne
ℓ=1w⊤
Tuℓ gives
KL
h
L{√neVne,w,t0|x 1:ne
C }

L{√nebVne,w,t0|x 1:ne
C }
i
≤KL
 neO
ℓ=1
Pℓ

neO
ℓ=1
Qℓ
!
=
neX
ℓ=1
KL(Pℓ∥Qℓ).
Averaging over the contexts and applying (4.4), we shall have
EX1:ne
C
KL
h
L{√neVne,w,t0|X 1:ne
C }

L{√nebVne,w,t0|X 1:ne
C }
i
≤Cn edT,β R2
n.
Pinsker’s and Jensen’s inequalities, therefore, give
EX1:ne
C
TV
h
L{√neVne,w,t0|X 1:ne
C },L{√nebVne,w,t0|X 1:ne
C }
i
≤C√ned1/2
T,β Rn.(EC.2.40)

ec22 e-companion toKong et al.:Conditional Tensor Diffusion
For each analysis tensor, couple the original and early-stopped variables using an independent copyZ ℓ
of the Gaussian tensor in (3.5). Then
√ne
 
Vne,w,t−Vne,w,0

= (αt−1)√neVne,w,0 + h1/2
t√ne
neX
ℓ=1
w⊤ vec(Zℓ).(EC.2.41)
Assumption 3.1 impliesEUw,ℓ,0 = 0andEU 2
w,ℓ,0 =w⊤A⊗ΣfA⊤
⊗w+p−βw⊤Σ⊗
ew≤C∥w∥ 2
2. Independence
across analysis tensors and (EC.2.41) imply, for0<t≤1,
E
√ne
 
Vne,w,t−Vne,w,0
2
≤C∥w∥ 2
2{(1−α t)2 +ht}≤C∥w∥ 2
2t.(EC.2.42)
For almost every context vector, (EC.2.41) is a conditional coupling. Averaging its cost and applying
Jensen’s inequality yield
EX1:ne
C
dBL

L{√neVne,w,0|X 1:ne
C },L{√neVne,w,t0|X 1:ne
C }

≤C∥w∥ 2
√t0≤C∥w∥ 2n−an/2.
Combining this display with (EC.2.40),d BL≤2 TV, and the triangle inequality proves (4.7).
For Corollary 4.2, write the exact learned-quantile interval as[a(X 1:ne
C ),b(X 1:ne
C )]. Its learned law has a
conditional probability of1−α. Multiplying the statistic and both endpoints by √ne, (EC.2.40) gives
EX1:ne
C
P
√neVne,w,t0∈[√nea(X1:ne
C ),√neb(X1:ne
C )]|X 1:ne
C
 
−(1−α)
≤C√ned1/2
T,β Rn.
Under (EC.2.41), the membership of √neVne,w,0 and√neVne,w,t0 in the scaled interval can differ only if
√ne|Vne,w,t0−Vne,w,0|>η, or if √neVne,w,0 lies withinηof an endpoint. The conditional density bound,
Markov’s inequality, and (EC.2.42) give, for everyη>0,
EX1:ne
C
P
√neVne,w,0∈[√nea,√neb]|X 1:ne
C
 
−P
√neVne,w,t0∈[√nea,√neb]|X 1:ne
C
 
≤C∥w∥2
2n−an
η2 + 4Mn,ne,wη,
where the context-dependent endpoints are suppressed in the second display. Optimizing overηand com-
bining the last two displays gives the right-hand side of (4.9). Finally, as{Vne,w,0∈[a,b]}={ √neVne,w,0∈
[√nea,√neb]}, it proves the stated coverage result on the average-outcome scale.
For the finite-Bresult, fixX 1:ne
C =x. Let bFx be the conditional cumulative distribution function of
bVne,w,t0, let bPx be its law, and define bFB,x(v) =B −1PB
b=1 I{bV (b)
ne,w,t0≤v},D B,x = supv∈R|bFB,x(v)−
bFx(v)|. Conditionally on(x,F tr), the generated values are independent draws from bPx. The Dvoretzky-
Kiefer-Wolfowitz-Massart inequality (Massart 1990) gives
P{DB,x>ε|x,F tr}≤2 exp(−2Bε 2),E(D B,x|x,F tr)≤
r π
2B.
LetbqB,x(u) = inf{v: bFB,x(v)≥u}. Continuity of bFx and absence of ties imply| bFx{bqB,x(u)}−u|≤
DB,x +B−1, for0<u<1. Applying this inequality to both endpoints yields
bPx
n
bI(B)
ne,w,1−α
o
−(1−α)
≤2DB,x + 2B−1,

e-companion toKong et al.:Conditional Tensor Diffusionec23
whose conditional expectation is at mostCB −1/2. Common multiplication of the generated values and
empirical endpoints by√ne leaves this error unchanged.
Construct a fresh set of(√neVne,w,0,√neVne,w,t0)whose Gaussian variables in (EC.2.41) are indepen-
dent of the finite generation sample. Conditional onF gen
B , the random interval has fixed endpoints. After
multiplying these endpoints by √ne, the total-variation and coupling arguments above apply pointwise.
Averaging over the contexts and the finite generation sample addsCB−1/2 to (4.9), proving (4.10).
□
EC.3. Framework Details
In this section, we report the score-network architecture and the discrete training and generation proce-
dures used forCFT-DIFF. The central construction of the candidate network class is a masked Tucker score
architecture: the observed control outcomes and the noised missing region are encoded through two masked
Tucker pathways, fused in a low-dimensional core, decoded back to the original matrix coordinates, and
connected to a missing-region residual.
The numerical experiments use matrix-valued inputs. Although the iFlex data can be stored as a3,746×
74×24household-by-day-by-hour array, the trained tensor object is the household-level day-by-hour matrix
X(i)
0 =

Yith(0)

t∈[74],h∈[24]∈R 74×24.
Thus, the empirical implementation takesD= 2, with(p 1,p 2) = (74,24), while the household indexiiden-
tifies training samples or analysis samples. Matrices from the control-group households form the training
sample. For each group-specific intervention calendar, its fixed74×24mask is applied synthetically to
these training matrices during training and to the corresponding treatment-group matrices during condi-
tional generation. Accordingly, the implementation description and architecture figure are written for the
order-two specializationX∈R H×W ; batch and feature-channel indices are suppressed when they are not
material.
EC.3.1. Architecture
LetMC denote the external binary mask received by the code, with one on the observed control outcomes,
and setMT =1−M C. Thus,MT is one on the treated region. At diffusion stepj, the score network receives
xj =MC⊙XC +MT⊙XT,j,
together withM C and the time labelj. The first term is kept fixed, and the second term is the noised
missing region. Figure EC.1 displays the score architecture used in the experiments, which consists of two
masked Tucker encoders, a low-dimensional nonlinear core, a Tucker decoder, and a missing-region shortcut
connection. Note that the two encoders are not duplicate input channels, as they carry complementary
information from the noised missing region and the observed control outcomes, respectively.
For the order-two implementation,ϕ enc is a shared full-resolution feature stem, andU∈R H×k1 andV∈
RW×k 2 are shared, trainable Tucker bases. In our experiments,ϕ enc is instantiated as a zero-padded7×7
convolution. The two core tensors are concatenated in the channel direction as[EC;ET ]ch. A sinusoidal time
embedding followed by an MLP modulates a conventional two-dimensional ResNet/attention U-Net in the
k1×k2 core space. Its output is reduced by a1×1channel projection and decoded byU(·)V ⊤ to the original

ec24 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.1CFT-Diff masked Tucker score architecture.
diffusion step
j
noised matrix
xj ∈ ℝ H × W
observed-region mask
M
time embedding
τj = MLP(SinEmb(j))
x = M ⊙ xj x = (1 − M) ⊙ xj
shared ϕenc, U, V
Tucker encoder
ϕenc U ⊤ (⋅)V E
Tucker encoder
ϕenc U ⊤ (⋅)V E
core fusion
Z0 = Concatch(E, E)
time-conditioned core regression
k1×k2
2× ResBlock · linear attn.
(k1/2)×(k2/2)
2× ResBlock · ↓2
(k1/4)×(k2/4)
ResBlock · full attention
(k1/2)×(k2/2)
↑2 · 2× ResBlock
k1×k2
linear attn. · 2× ResBlock
missing-region
residual head
fuse decoded + missing feature
ResBlock(time) · 1×1
Tucker decoder
FD = U Π1 × 1(Zcore)V ⊤
missing-region feature skip
r = ϕenc(x)
missing-region output
M ⊙ ̂εθ, j
r
Note.The masked matrix input is split into the fixed observed control outcomes and a noised missing region. Each part is mapped
by the same Tucker encoderES =U⊤ϕenc(MS⊙xj)V,S∈{C,T}, whereϕ enc is an application-specific full-resolution feature
stem. The two core maps are concatenated along the channel dimension and processed by a time-conditioned core regression on
the low-dimensional Tucker core; the displayed multi-resolution residual and attention stages are a representative realization of
this map. A1×1projection followed by the Tucker decoder combines the core output with the shortcutr T =ϕ enc(MT⊙xj).
The network outputs the learned noise prediction in the missing region. The observed control outcomes remain fixed during the
conditional reverse update. The brighter blue dashed link denotes a representative skip; slate dashed links carry time and mask
conditioning; and the right-side rail denotes the missing-region feature shortcut.

e-companion toKong et al.:Conditional Tensor Diffusionec25
matrix resolution. The decoded feature is concatenated with the missing-region featureϕ enc(MT⊙xj)and
passed, together with the time embedding, through a residual output block and a1×1head. In the matrix-
factor experiments,U,Vare warm started with loading-space estimates and remain trainable.
EC.3.2. Core-Net Function Class
The Core-Net below is the theoretical sieve used to control approximation and stochastic complexity. All
full-dimensional masking, encoding, decoding, and residual operations are specified separately; the low-
dimensional network learns only the map from ther-dimensional core statistic and diffusion time to the
core output. This makes the theoretical function class follow the same Tucker encoder-decoder organization
displayed in Figure EC.1.
DEFINITIONEC.3.1 (CORE-NET FUNCTION CLASS).The classF core(L,m,J,K,κ,γ g,γt)consists of
feed-forward ReLU maps
ζθ :Rr×[t 0,T]→R r
with an affine output layer, depth at mostL, hidden-layer width at mostm, at mostJnonzero weights and
biases, and parameter magnitudes bounded byκ. Each map satisfies
sup
(g,t)∈Rr×[t0,T]
∥ζθ(g,t)∥ 2≤K,
∥ζθ(g,t)−ζ θ(g′,t)∥ 2≤γg∥g−g ′∥2, g,g ′∈Rr, t∈[t 0,T],
and
∥ζθ(g,t)−ζ θ(g,t′)∥2≤γt|t−t′|, g∈R r, t,t ′∈[t 0,T].
For a tensor-valued Core-NetZθ, the identification is
ζθ(g,t) = vec [Zθ{Tucker(g),t}].
The boundedness and Lipschitz restrictions in this definition are the regularity conditions needed for
the low-dimensional approximation and covering arguments. In the experiments, the corresponding low-
dimensional Core-Net is implemented using the time-conditioned U-Net displayed in Figure EC.1, with
residual blocks, SiLU/GELU activations, normalization, and linear or full attention. In both cases, nonlinear
computation is confined to the Tucker core, while dual masking, Tucker encoding and decoding, and the
missing-region shortcut remain explicit structural components.
EC.3.3. Masked DDPM Training
For a given CFT-Diff checkpoint, training uses training tensors and a fixed mask. For each minibatch, we
drawj∼Unif{0,...,N step−1}andϵ∼N(0,I), and construct the masked discrete forward input
xj =MC⊙X 0 +MT⊙
p
¯αjX0 +
p
1−¯αjϵ

.
Here, only the missing region is noised, while the observed control outcomes remain fixed. The model uses
the DDPM noise-prediction parameterization (Ho et al. 2020) and minimizes the masked noise-prediction
loss
bL= 1
B
BX
i=1

MT⊙
n
ϵi−bϵθ(x(i)
ji ,ji;MC)
o

2
F
∥MT∥0
.

ec26 e-companion toKong et al.:Conditional Tensor Diffusion
The external mask is synthetically applied to every complete training tensor, and the loss is evaluated only
over its missing outcomes.
Simulation configuration.For the matrix-factor simulations, the input has one channel of shape64×
64. The Tucker core dimension is(k 1,k 2) = (16,16), and the core U-Net has resolutions16 2,8 2, and4 2
with widths64,128, and256, respectively. Each resolution uses two time-conditioned residual blocks and
attention; the bottleneck uses full attention. We use a cosine beta schedule withNstep = 200diffusion steps,
ϵ-prediction, and 300 training epochs. Optimization uses AdamW with a learning rate of10 −4, weight
decay of0.01, a batch size of 60, gradient accumulation of 2, a 10-epoch warm-up followed by cosine
scheduling, exponential moving average decay of0.999, and automatic mixed precision. These numerical
settings describe the reported matrix-factor simulation configuration; the architectural mask convention and
the conditional objective remain unchanged when the matrix size or Tucker ranks are adapted to another
design.
Empirical demand-data configuration.For the iFlex experiment, each empirical input is a one-channel
74×24matrix from a single household. We use(k 1,k 2) = (16,16), so the nonlinear core is evaluated on
16×16,8×8, and4×4Tucker grids with a base width of 64. Similar to the simulation setting, each
represented level contains two time-conditioned residual blocks. For each mask-specific fit, the day and
hour loading spaces are initialized from the leading empirical eigenvectors computed from the complete
household training matrices. The loading matricesUandVare warm starts and remain trainable with a
learning rate of10 −5, while the other AdamW parameters use a learning rate of10 −4. We train for 300
epochs with a batch size of 64, gradient accumulation of 2, weight decay of0.01, and automatic mixed
precision. The learning-rate schedule uses a linear 10-epoch warm-up followed by cosine annealing with
Tmax = 40andη min = 10−6. The empirical runs use the same 200-step cosine DDPM noise-prediction
objective as above.
EC.3.4. Conditional Generation
The reported experiments use DDIM generation (?) withN step = 200reverse steps. Thus, each reverse
trajectory starts from independent Gaussian noise in the missing region and produces one sample from
the trained conditional generator. At every reverse step, we update only the missing region while keeping
the observed control outcomes fixed. This projection makes the generated tensor agree exactly with the
observed control outcomes throughout the trajectory. The target bX0 inferred from the predicted noise is
clipped before its DDIM update. We experimented with clipping widths from 1.5 to 2.5 (with 2.0 as the
default).
For the reported simulations, we generateB= 100conditional completions for each test matrix. The
resulting empirical distribution supports both point estimates obtained by averaging draws and the distribu-
tional measures and interval summaries reported in the paper.
Meanwhile, for each held-out household in the iFlex recovery experiments, we supply the sampler only
with the observed control outcomesM C⊙X obs. We generateB= 100completions with a seed matched
to the corresponding training split, a 200-step DDIM, and clipping of the inferred bX0 to[−2,2]. Repeated
household inputs receive independent initial Gaussian states in the missing region. Point-recovery estimates
average the 100 draws, whereas the unreduced draw set is retained for distributional evaluation, including
the joint energy score.

e-companion toKong et al.:Conditional Tensor Diffusionec27
Algorithm 1Conditional DDIM generation forCFT-DIFF
Require:observed control outcomesX C, observed maskM C,MT =1−M C, noise predictorbϵθ, and cumulative
schedule{¯αj}
Nstep−1
j=0
Ensure:conditional completions{ eX
(b)
0 }B
b=1
1:forb= 1,...,Bdo
2:drawz (b)∼N(0,I)and setx Nstep−1←MC⊙XC +MT⊙z (b)
3:forj=N step−1,N step−2,...,1do
4:bϵ←bϵ θ(xj,j;MC)
5: bX0←clip [−xmax,xmax]
 
xj−p1−¯αjbϵ

/√¯αj
 
6:x T
j−1←√¯αj−1bX0 +p1−¯αj−1bϵ
7:x j−1←MC⊙XC +MT⊙xT
j−1 ▷hard conditional projection
8:end for
9: eX
(b)
0 ←x 0
10:end for
The recovery masks are constructed at the household–day level and then expanded over all 24 hourly
entries of the selected day. Under simultaneous adoption, every held-out household uses the same bottom-
suffix mask, with 5, 11, 16, 21, 27, 32, 37, 43, or 48 missing working days. Under staggered adoption,
households are partitioned into balanced cohorts with different missing-suffix lengths whose weighted mean
equals the selected target ratio; each cohort is sampled with the same-seed CFT-Diff checkpoint matched to
that suffix mask. Under switchback, the held-out households are deterministically allocated, using the fixed
mask seed, to three nearly balanced groups. A policy calendar, rather than a held-out outcome, marks a day
as hidden when that policy occurs for at least one source household during at least one hour; each group
receives a distinct union of these calendars, expanded over all 24 hourly entries. CFT-Diff is trained once for
each resulting74×24calendar template, using the same split-specific complete training data, and reused
for every household assigned to that template. Thus, a heterogeneous empirical panel is implemented as
a collection of fixed-mask conditional generation problems while preserving the observed-entry pattern of
every individual household.
EC.4. Simulation Details and Additional Results
This appendix provides the full simulation design, defines the evaluation measures, and reports additional
results across factor strengths and numbers of latent factors.
EC.4.1. Detailed Simulation Design
Data-generating process.For each replication, we generate 372 independent64×64matrices according
to
X(ℓ)
raw =A 1F (ℓ)A⊤
2 +E (ℓ), ℓ= 1,...,372,(EC.4.1)
whereX (ℓ)
raw =p β/2X,F (ℓ)∈R 16×16, andE (ℓ)∈R 64×64 are mutually independent acrossℓ, with
vec(F (ℓ))∼N(0,4I 256)andvec(E (ℓ))∼N(0,I 4096). To construct the loading matrices, we obtain
Q1,Q 2∈R 64×16 by orthonormalizing two independent standard Gaussian matrices and setA d = 64β/2Qd

ec28 e-companion toKong et al.:Conditional Tensor Diffusion
ford= 1,2, whereβ∈{0.50,0.75}. Thus, increasingβstrengthens the common factor component while
preserving the loading directions.
The first 360 matrices constitute the training sample, and the remaining 12 are used for evaluation.
To place all methods on a common numerical scale, letc sim = max1≤ℓ≤360∥X(ℓ)
raw∥∞ and defineX (ℓ) =
X(ℓ)
raw/csim. We repeat the entire experiment five times using independently generated loading spaces, latent
factors, and idiosyncratic errors. Within each replication, the same training and evaluation matrices are used
across methods and missing rates.
Missing Regions.Each evaluation matrix is partitioned into a rectangular missing region and its observed
control outcomes. The target missing rates areρ∈{0.25,0.50,0.75}. Using one-based indexing, the 25%
design removes rows 17–48 and columns 33–64, yielding a32×32block. The 50% design removes rows
12–52 and columns 15–64, yielding a41×50block and an actual missing rate of 0.5005. The 75% design
removes rows 6–58 and columns 7–64, yielding a53×58block and an actual missing rate of 0.7505. In
each design, the block is vertically centered and reaches the final matrix column. The same block definition
is used for every evaluation matrix within a design, and accuracy is evaluated only on its missing region.
DuringCFT-DIFFtraining, the corresponding mask is applied synthetically to each complete training matrix.
Because (EC.4.1) is Gaussian, the exact conditional distribution used in the pointwise diagnostics is
available analytically. LetxT andxC denote the vectorized missing region and observed control outcomes,
respectively, and partition the covariance matrix ofvec(X (ℓ))conformably. Then
xT|xC∼N
 
ΣTC Σ−1
CCxC,ΣTT −ΣTC Σ−1
CC ΣCT

.(EC.4.2)
Methods and implementation.The comparison includes the five point estimators and three diffusion
methods described in Section 5.1. For the diffusion methods, the generated mean is used as the point esti-
mate.CONV-DIFFandTUCKER-DIFFuse one trained model within each factor-strength setting and replica-
tion across the three missing rates. BecauseCFT-DIFFincorporates the fixed mask in its conditional score
architecture, it is trained for each missing-rate design. Each diffusion model is trained for 300 epochs with
batch size 60, gradient accumulation over two batches, and 200 diffusion steps. The aggregate evaluation
uses 100 conditional draws for each of the 12 evaluation matrices in every replication. The architectures
and discrete training and generation procedures are described in Appendix EC.3.
Evaluation measures.For a given replication and missing rate, letJindex the missing entries pooled
across the 12 evaluation matrices, letN J =|J|, and writey i for the realized value at entryi∈J. For
a diffusion method, letx (1)
i ,...,x (B)
i be itsB= 100conditional draws and setby i =B−1PB
b=1x(b)
i . The
point-recovery measures are
MAE = 1
NJ
X
i∈J
|byi−yi|,RMSE =
(
1
NJ
X
i∈J
(byi−yi)2
)1/2
.
The entrywise continuous ranked probability score is estimated by
CRPSi = 1
B
BX
b=1
|x(b)
i −yi|− 1
2B2
BX
b=1
BX
b′=1
|x(b)
i −x (b′)
i |,(EC.4.3)

e-companion toKong et al.:Conditional Tensor Diffusionec29
and the reported CRPS averages (EC.4.3) overi∈J. The energy score evaluates the missing region jointly.
For a realized missing-region vectoryand generated vectorsx (1),...,x (B), it is estimated by
Energy = 1
B
BX
b=1
∥x(b)−y∥ 2− 1
2
bE∥x−x′∥2,
where the second expectation uses 200 fixed pairs of generated draws. Both scores are negatively oriented.
LetL i andU i be the 5th and 95th empirical percentiles of the draws at entryi. The reported 90% cov-
erage and width areN −1
J
P
i∈J I{Li≤yi≤Ui}andN −1
J
P
i∈J (Ui−Li), respectively. Withδ= 0.10, the
corresponding interval score is
ISδ,i = (Ui−Li) + 2
δ (Li−yi)I{yi<Li}+ 2
δ (yi−Ui)I{yi>Ui}.
The weighted interval score combines the predictive median with central intervals at the 50%, 60%, 70%,
80%, 90%, and 95% levels, using the standard weightsδ k/2, whereδ k is one minus the corresponding
coverage level. IS and WIS reward calibration and sharpness jointly; smaller values are preferred. Each
measure is first pooled over the 12 evaluation matrices within a replication. The tables report the mean and
standard deviation across the five replications.
Pointwise diagnostic.The pointwise figures use the 25% missing region and 10,000 conditional draws
from each diffusion method for the first evaluation matrix in one replication. Within the missing region, we
compute the empirical percentile of each realized entry and consider entries within 0.03 of 0.25, 0.50, or
0.75. For displayed entryiand methodm, letµ i andσ i denote the exact conditional mean and standard
deviation from (EC.4.2), and letbµmi andbσmi denote the corresponding moments of the generated draws.
We summarize pointwise agreement by
Dmi =
"bµmi−µi
σi
2
+

log
bσmi
σi
2#1/2
.(EC.4.4)
The display is designed to make differences among the conditional generators visually informative. We
therefore select, within each percentile neighborhood, an entry for which theCFT-DIFFdiscrepancy is no
larger than those of the two nested diffusion models; among the remaining candidates, selection balances
theCFT-DIFFdiscrepancy, its improvement over the benchmarks, and proximity to the target percentile. The
aggregate tables, rather than these selected entries, provide the full-sample comparison.
EC.4.2. Additional Recovery Results
Table EC.3 repeats the aggregate comparison underβ= 0.75. The stronger common factor improves recov-
ery for methods that exploit low-rank structure, while the ranking among the diffusion methods remains
unchanged.CFT-DIFFhas the lowest MAE, RMSE, Energy, CRPS, IS, and WIS among the three conditional
generators at every missing rate. Relative toTUCKER-DIFF, it lowers Energy and CRPS by 14%–42% and
produces intervals that are 17%–45% narrower. These results show that the gains from masked conditional
generation persist as the factor component becomes stronger.
EC.4.3. Additional Pointwise Distribution Diagnostics
Figure EC.2 gives the pointwise diagnostic forβ= 0.75in the baseline design. Figures EC.3–EC.6 extend
the comparison to designs with four and eight factors. Across these additional designs,CFT-DIFFcontinues

ec30 e-companion toKong et al.:Conditional Tensor Diffusion
Table EC.3Counterfactual recovery across missing rates (β= 0.75).
Point Recovery Distributional Recovery Interval Recovery
Method MAE RMSE Energy CRPS Coverage Width IS WIS
Panel A: Missing Rate= 25%
NMC0.0208 (0.0012) 0.0261 (0.0016) – – – – – –
DID0.1682 (0.0109) 0.2165 (0.0142) – – – – – –
SC0.0205 (0.0011) 0.0259 (0.0014) – – – – – –
SDID0.1164 (0.0070) 0.1495 (0.0087) – – – – – –
TFI0.0513 (0.0030) 0.0656 (0.0040) – – – – – –
CONV-DIFF0.1182 (0.0068) 0.1518 (0.0085) 3.4132 (0.1944) 0.0844 (0.0048) 0.8738 (0.0120) 0.4610 (0.0167) 0.6418 (0.0367) 0.0635 (0.0037)
TUCKER-DIFF0.0360 (0.0016) 0.0473 (0.0017) 1.1161 (0.0347) 0.0254 (0.0010) 0.9728 (0.0104) 0.2153 (0.0105) 0.2257 (0.0073) 0.0199 (0.0007)
CFT-DIFF0.0211 (0.0011) 0.0275 (0.0014) 0.6560 (0.0316) 0.0148 (0.0008) 0.9567 (0.0044) 0.1195 (0.0060) 0.1303 (0.0065) 0.0115 (0.0006)
Panel B: Missing Rate= 50%
NMC0.0235 (0.0016) 0.0297 (0.0020) – – – – – –
DID0.1704 (0.0124) 0.2189 (0.0160) – – – – – –
SC0.0245 (0.0021) 0.0313 (0.0029) – – – – – –
SDID0.1180 (0.0079) 0.1516 (0.0099) – – – – – –
TFI0.0705 (0.0050) 0.0906 (0.0061) – – – – – –
CONV-DIFF0.1197 (0.0079) 0.1538 (0.0099) 4.8924 (0.3178) 0.0855 (0.0057) 0.8739 (0.0117) 0.4670 (0.0203) 0.6510 (0.0435) 0.0644 (0.0043)
TUCKER-DIFF0.0600 (0.0034) 0.0784 (0.0043) 2.5256 (0.1340) 0.0428 (0.0024) 0.9526 (0.0115) 0.3082 (0.0180) 0.3378 (0.0173) 0.0325 (0.0018)
CFT-DIFF0.0375 (0.0025) 0.0498 (0.0033) 1.5945 (0.1057) 0.0265 (0.0018) 0.9321 (0.0193) 0.1792 (0.0154) 0.2104 (0.0136) 0.0201 (0.0014)
Panel C: Missing Rate= 75%
NMC0.0797 (0.0051) 0.1051 (0.0066) – – – – – –
DID0.1685 (0.0108) 0.2169 (0.0141) – – – – – –
SC0.0881 (0.0042) 0.1173 (0.0058) – – – – – –
SDID0.1176 (0.0073) 0.1514 (0.0091) – – – – – –
TFI0.0978 (0.0056) 0.1260 (0.0070) – – – – – –
CONV-DIFF0.1188 (0.0074) 0.1529 (0.0091) 5.9528 (0.3577) 0.0849 (0.0052) 0.8779 (0.0135) 0.4692 (0.0189) 0.6468 (0.0393) 0.0639 (0.0039)
TUCKER-DIFF0.0884 (0.0056) 0.1147 (0.0071) 4.4728 (0.2710) 0.0630 (0.0039) 0.9268 (0.0117) 0.4031 (0.0187) 0.4717 (0.0270) 0.0472 (0.0029)
CFT-DIFF0.0761 (0.0056) 0.0994 (0.0072) 3.8687 (0.2775) 0.0540 (0.0040) 0.9159 (0.0145) 0.3339 (0.0188) 0.4032 (0.0297) 0.0405 (0.0030)
Note.The table reports recovery at three missing rates. Entries are means across five independent simulation replications, with standard
deviations in parentheses. MAE and RMSE evaluate point recovery; Energy and CRPS evaluate the generated conditional distribution.
Coverage and Width denote the empirical coverage and average width of nominal 90% intervals, and IS and WIS denote the interval
score and weighted interval score. Smaller MAE, RMSE, Energy, CRPS, IS, and WIS indicate better performance. Width is interpreted
jointly with Coverage, whose nominal level is 0.90. Dashes indicate measures that are not applicable to point estimators. Each diffusion
method uses 100 conditional draws per evaluation matrix.
to track both the shape and mean of the exact conditional distribution at all three selected entries.CONV-DIFF
remains substantially overdispersed and exhibits clear mean deviations in several tail cases, whileTUCKER-
DIFFreduces these discrepancies but still produces excess dispersion, particularly with eight factors. The
relative performance of the three methods therefore remains stable as the number of factors increases.
Table EC.4 reports the corresponding location, scale, and discrepancy values for both factor-strength
settings.CFT-DIFFhas the smallestDat every displayed entry. Atβ= 0.50, its discrepancies are between
0.298 and 0.361, compared with values exceeding 1.17 for both diffusion benchmarks. Atβ= 0.75,CFT-
DIFFremains substantially closer to the exact law even though the exact conditional distributions become
more concentrated.
EC.5. Additional Empirical Analysis
EC.5.1. Overview of the iFlex Experiment
The experimental design and data construction are documented by?, while Hofmann and Lindberg (2024)
examine household demand responses in the full-scale experiment. Table EC.5 summarizes the group-
specific intervention design. Treatment groups were organized by region and assigned prespecified sets of

e-companion toKong et al.:Conditional Tensor Diffusionec31
Figure EC.2Pointwise conditional distribution recovery (β= 0.75).
Note.Columns correspond toCONV-DIFF,TUCKER-DIFF, andCFT-DIFF. Rows display entries whose realized missing values are
near the 25th, 50th, and 75th percentiles within the missing region. Each histogram is based on 10,000 conditional draws, and the
missing rate is 25%. The solid curve shows the exact conditional density; the dashed and dotted vertical lines indicate the exact
conditional mean and the mean of the generated draws, respectively.
four candidate price signals, typically varying the peak-price level within a common profile or compar-
ing alternative profile shapes. On each intervention day, one signal was selected from the corresponding
group-specific set.
Because households index samples in the empirical implementation, the Tucker structure used byCFT-
DIFFpertains to the day and hour modes of the74×24household matrices. We assess this structure using
three collections of fully observed no-policy outcomes: globally nonintervention days, the pretreatment
period, and all working days for households in the control groups. For each collection, we form the corre-
sponding household-by-day-by-hour array for diagnostic purposes and examine its mode-wise spectral con-
centration. The day- and hour-mode spectra directly assess the low-rank structure used by the trained model;

ec32 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.3Pointwise conditional distribution recovery with four factors (β= 0.50).
Note.Columns correspond toCONV-DIFF,TUCKER-DIFF, andCFT-DIFF. The design contains four latent factors. Rows display
entries whose realized missing values are near the 25th, 50th, and 75th percentiles within the missing region. Each histogram is
based on 10,000 conditional draws, and the missing rate is 25%. The solid curve shows the exact conditional density; the dashed
and dotted vertical lines indicate the exact conditional mean and the mean of the generated draws, respectively.
the household-direction spectrum is reported only as a descriptive measure of common cross-household
variation.
Figure EC.7 shows pronounced spectral concentration in both modes used by the empirical model. Across
the three sample constructions, the day-mode spectra reach the 95% threshold with only a small fraction
of the available components, while the hour-mode spectra exceed 95% within the first few components and
approach 99% well before the full 24-dimensional mode is used. The profiles are also similar across the
three samples, indicating that the observed concentration is not confined to either the short pretreatment
period or the control-group households. These results support the approximately low-rank day-by-hour
representation underlying the empiricalCFT-DIFFspecification.

e-companion toKong et al.:Conditional Tensor Diffusionec33
Figure EC.4Pointwise conditional distribution recovery with four factors (β= 0.75).
Note.Columns correspond toCONV-DIFF,TUCKER-DIFF, andCFT-DIFF. The design contains four latent factors. Rows display
entries whose realized missing values are near the 25th, 50th, and 75th percentiles within the missing region. Each histogram is
based on 10,000 conditional draws, and the missing rate is 25%. The solid curve shows the exact conditional density; the dashed
and dotted vertical lines indicate the exact conditional mean and the mean of the generated draws, respectively.
EC.5.2. Missingness Patterns
To evaluate counterfactual recovery in a controlled setting, we artificially mask fully observed no-policy
outcomes and compare the resulting imputations with their held-out values. We consider three treatment-
induced missingness patterns commonly encountered in causal panels: switchback, staggered adoption, and
simultaneous adoption. As illustrated in Figure EC.8, control households remain fully observed, whereas
complete household-day trajectories are masked after the first intervention day according to the correspond-
ing design. These patterns allow us to assess imputation performance under both intermittent and monotone
block missingness.

ec34 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.5Pointwise conditional distribution recovery with eight factors (β= 0.50).
Note.Columns correspond toCONV-DIFF,TUCKER-DIFF, andCFT-DIFF. The design contains eight latent factors. Rows display
entries whose realized missing values are near the 25th, 50th, and 75th percentiles within the missing region. Each histogram is
based on 10,000 conditional draws, and the missing rate is 25%. The solid curve shows the exact conditional density; the dashed
and dotted vertical lines indicate the exact conditional mean and the mean of the generated draws, respectively.
EC.5.3. Additional Results on Counterfactual Recovery Accuracy
EC.5.3.1. Evaluation MeasuresThis section defines the measures used to evaluate point and coun-
terfactual distribution recovery. LetMdenote the set of artificially masked outcomes and letn M =|M|.
For eachj∈M, letY j denote the observed no-policy outcome and bYj its recovered value. For a diffusion
method withBgenerated draws, the point prediction is bYj = 1
B
PB
b=1
eY (b)
j .
Point recovery.We evaluate point recovery using the mean absolute error (MAE) and root mean squared
error (RMSE):
MAE = 1
nM
X
j∈M
bYj−Yj
,RMSE =
"
1
nM
X
j∈M

bYj−Yj
2
#1/2
.

e-companion toKong et al.:Conditional Tensor Diffusionec35
Figure EC.6Pointwise conditional distribution recovery with eight factors (β= 0.75).
Note.Columns correspond toCONV-DIFF,TUCKER-DIFF, andCFT-DIFF. The design contains eight latent factors. Rows display
entries whose realized missing values are near the 25th, 50th, and 75th percentiles within the missing region. Each histogram is
based on 10,000 conditional draws, and the missing rate is 25%. The solid curve shows the exact conditional density; the dashed
and dotted vertical lines indicate the exact conditional mean and the mean of the generated draws, respectively.
Smaller values indicate more accurate point recovery.
Energy score.The energy score evaluates the joint distribution of the missing 24-hour trajectory. Let
Yj∈R 24 denote the observed trajectory for an artificially masked household–day, and let eY(1)
j ,..., eY(B)
j
denote the corresponding generated trajectories. For a predictive distributionQ, the population energy score
is
ES(Q,Yj) =EQ
h
∥eYj−Yj∥2
i
− 1
2 EQ
h
∥eYj−eY′
j∥2
i
,
where eYj and eY′
j are independent draws fromQ. Using the generated draws, the first expectation is evalu-
ated by
1
B
BX
b=1

eY(b)
j −Yj

2
.

ec36 e-companion toKong et al.:Conditional Tensor Diffusion
Table EC.4Pointwise conditional distribution fit at the displayed entries.
Exact Law Conv-Diff Tucker-Diff CFT-Diff
Empirical Quantile Realized Value Mean Std. Dev. Mean Std. Dev.DMean Std. Dev.DMean Std. Dev.D
Panel A:β= 0.50
25%−0.096−0.108 0.043−0.007 0.176 2.709−0.044 0.115 1.754−0.108 0.062 0.361
50% 0.006 0.027 0.041−0.009 0.141 1.525−0.009 0.087 1.173 0.028 0.055 0.298
75% 0.089 0.028 0.044−0.005 0.186 1.634−0.024 0.124 1.572 0.026 0.059 0.299
Panel B:β= 0.75
25%−0.089−0.109 0.014 0.010 0.126 8.582−0.075 0.067 2.867−0.110 0.042 1.076
50% 0.006 0.009 0.014 0.006 0.134 2.249 0.032 0.065 2.169 0.004 0.040 1.091
75% 0.102 0.096 0.014 0.006 0.129 6.657 0.061 0.070 2.869 0.098 0.042 1.085
Note.The table reports the entries displayed in Figures 2 and EC.2. Empirical Quantile gives the approximate rank of the realized value
within the missing region. Under Exact Law, Mean and Std. Dev. are the conditional mean and standard deviation implied by(EC.4.2);
for each diffusion method, they are calculated from 10,000 conditional draws. The discrepancyD, defined in(EC.4.4), accounts for
deviations in both conditional location and scale. Smaller values indicate closer agreement, with zero corresponding to an exact match.
The missing rate is 25%.
Table EC.5Group-specific candidate price signals in the iFlex experiment.
Region Treatment Group Candidate Price Signals
BergenBer 1{B 2,B 5,B 10,B 15}
BodøBo 1{B 2,B 5,B 10,B 15}
OsloOs 1{B 2,B 5,B 10,B 15}
Os 2{P 2,P 5,P 10,P 15}
Os 3{A 10,B 10,P 10,P0 10}
Os 4{A 5,A 10,B 10,C}
Os 5{P0 2,P0 10,P0 30,P 10}
Os 6{A 5,B 2,C,P 15}
TromsøTrom 1{B 2,B 5,B 10,B 15}
Trom 2{P 2,P 5,P 10,P 15}
TrondheimTrond 1{B 2,B 5,B 10,B 15}
Note.Each treatment group was associated with four prespecified candidate price signals. On each intervention day, one of these signals
was selected for the group, and all households within that group were assigned the same 24-hour price path. The five regional control
groups received no experimental price signal and are therefore omitted from the table. A signal label combines the price-profile family with
the peak price level in NOK/kWh. ProfileCdenotes the single asymmetric price signal with different morning and afternoon peak-price
levels.
The second expectation is evaluated using randomly sampled pairs of generated draws. We average the
resulting scores across all artificially masked household–days and across the five test samples. A smaller
energy score indicates better recovery of the joint counterfactual distribution.
Continuous ranked probability score.CRPS evaluates the marginal distribution of an individual missing
hourly outcome. LeteY (1)
j ,..., eY (B)
j be the generated draws for outcomeYj. The empirical CRPS is
CRPSj = 1
B
BX
b=1
eY (b)
j −Yj
− 1
2B2
BX
b=1
BX
b′=1
eY (b)
j −eY (b′)
j
.
The reported CRPS is averaged across the missing hourly outcomes. Smaller values indicate better marginal
distributional recovery.

e-companion toKong et al.:Conditional Tensor Diffusionec37
Figure EC.7Mode-wise spectral profiles of fully observed no-policy electricity-consumption tensors.
Note.Panels (a) and (b) report cumulative spectral energy along the day and hour modes, respectively. The three curves are con-
structed from globally nonintervention days, the pretreatment period, and all working days for households in the control groups.
Horizontal lines mark the 90%, 95%, and 99% energy thresholds.
Figure EC.8Illustrative intervention patterns.
/uni00000014 /uni00000015/uni00000013 /uni00000016/uni00000013 /uni00000018/uni00000013 /uni0000001a/uni00000017
/uni0000003a /uni00000052/uni00000055/uni0000004e/uni0000004c/uni00000051/uni0000004a/uni00000003/uni00000047/uni00000044/uni0000005c/uni00000056
/uni0000002b/uni00000052/uni00000058/uni00000056/uni00000048/uni0000004b/uni00000052/uni0000004f/uni00000047/uni00000056
/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f/uni00000003/uni0000004b/uni00000052/uni00000058/uni00000056/uni00000048/uni0000004b/uni00000052/uni0000004f/uni00000047/uni00000056
/uni00000033/uni00000055 /uni00000048/uni00000057/uni00000055 /uni00000048/uni00000044/uni00000057/uni00000050/uni00000048/uni00000051/uni00000057
/uni00000033/uni00000044/uni00000051/uni00000048/uni0000004f/uni00000003/uni0000000b/uni00000044/uni0000000c/uni00000003/uni00000036/uni0000005a/uni0000004c/uni00000057/uni00000046/uni0000004b/uni00000045/uni00000044/uni00000046/uni0000004e
/uni00000014 /uni00000015/uni00000013 /uni00000016/uni00000013 /uni00000018/uni00000013 /uni0000001a/uni00000017
/uni0000003a /uni00000052/uni00000055/uni0000004e/uni0000004c/uni00000051/uni0000004a/uni00000003/uni00000047/uni00000044/uni0000005c/uni00000056
/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f/uni00000003/uni0000004b/uni00000052/uni00000058/uni00000056/uni00000048/uni0000004b/uni00000052/uni0000004f/uni00000047/uni00000056
/uni00000033/uni00000055 /uni00000048/uni00000057/uni00000055 /uni00000048/uni00000044/uni00000057/uni00000050/uni00000048/uni00000051/uni00000057
/uni00000033/uni00000044/uni00000051/uni00000048/uni0000004f/uni00000003/uni0000000b/uni00000045/uni0000000c/uni00000003/uni00000036/uni00000057/uni00000044/uni0000004a/uni0000004a/uni00000048/uni00000055 /uni00000048/uni00000047/uni00000003/uni00000044/uni00000047/uni00000052/uni00000053/uni00000057/uni0000004c/uni00000052/uni00000051
/uni00000014 /uni00000015/uni00000013 /uni00000016/uni00000013 /uni00000018/uni00000013 /uni0000001a/uni00000017
/uni0000003a /uni00000052/uni00000055/uni0000004e/uni0000004c/uni00000051/uni0000004a/uni00000003/uni00000047/uni00000044/uni0000005c/uni00000056
/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f/uni00000003/uni0000004b/uni00000052/uni00000058/uni00000056/uni00000048/uni0000004b/uni00000052/uni0000004f/uni00000047/uni00000056
/uni00000033/uni00000055 /uni00000048/uni00000057/uni00000055 /uni00000048/uni00000044/uni00000057/uni00000050/uni00000048/uni00000051/uni00000057
/uni00000033/uni00000044/uni00000051/uni00000048/uni0000004f/uni00000003/uni0000000b/uni00000046/uni0000000c/uni00000003/uni00000036/uni0000004c/uni00000050/uni00000058/uni0000004f/uni00000057/uni00000044/uni00000051/uni00000048/uni00000052/uni00000058/uni00000056/uni00000003/uni00000044/uni00000047/uni00000052/uni00000053/uni00000057/uni0000004c/uni00000052/uni00000051
/uni00000026/uni00000052/uni00000051/uni00000057/uni00000055/uni00000052/uni0000004f/uni00000003/uni0000004b/uni00000052/uni00000058/uni00000056/uni00000048/uni0000004b/uni00000052/uni0000004f/uni00000047/uni00000056 /uni00000032/uni00000045/uni00000056/uni00000048/uni00000055/uni00000059/uni00000048/uni00000047 /uni00000030/uni0000004c/uni00000056/uni00000056/uni0000004c/uni00000051/uni0000004a
Note.Panels (a)–(c) illustrate the switchback, staggered-adoption, and simultaneous-adoption patterns, respectively. Rows rep-
resent households and columns represent working days. Gray rows denote fully observed control households, blue cells denote
observed no-policy outcomes, and red cells denote missing no-policy outcomes. The vertical dashed line marks the first intervention
day; observations to its left constitute the pretreatment period.
Coverage and interval width.For the interval-based measures, we use the household–day total of the
missing trajectory. Let
Uj =
X
h∈Mj
Yjh, eU (b)
j =
X
h∈Mj
eY (b)
jh ,
whereM j denotes the missing hours for household–dayj. Under the block-missingness designs used in
the main analysis,M j contains all 24 hours.
For a central interval with nominal coverage1−α, let
Lj,α =bQα/2

eU (1)
j ,..., eU (B)
j

, H j,α =bQ1−α/2

eU (1)
j ,..., eU (B)
j

.

ec38 e-companion toKong et al.:Conditional Tensor Diffusion
The empirical coverage is
Coverage1−α = 1
nB
nBX
j=1
I{Lj,α≤Uj≤Hj,α},
wheren B is the number of evaluated household–day blocks. A well-calibrated interval has empirical cov-
erage close to its nominal level1−α.
The average interval width is
Width1−α = 1
nB
nBX
j=1
(Hj,α−Lj,α).
For comparable coverage, a smaller width indicates a sharper counterfactual distribution.
Interval score.The interval score combines interval width and coverage in a single measure. For a central
(1−α)interval,
ISα,j =Hj,α−Lj,α + 2
α (Lj,α−Uj)I{U j<Lj,α}+ 2
α (Uj−Hj,α)I{U j>Hj,α}.
The first term penalizes wide intervals, while the remaining terms penalize observations that fall below or
above the interval. The table reports the average interval score for the 90% central interval. A smaller value
indicates a better combination of coverage and interval width.
Weighted interval score.The weighted interval score aggregates information from several central inter-
vals and the predictive median. Letm j denote the predictive median of eU (1)
j ,..., eU (B)
j , and let theK C
central coverage levels be1−α 1,...,1−α KC . We compute
WISj =
1
2|Uj−mj|+
KCX
k=1
αk
2 ISαk,j
KC + 1
2
.
In the main analysis, the central coverage levels are50%,60%,70%,80%,90%, and95%. The reported
WIS is averaged across evaluated household–days. A smaller WIS indicates better overall distributional
recovery across the different parts of the counterfactual distribution.
EC.5.3.2. Results on Counterfactual Recovery AccuracyWe provide several additional checks on
the counterfactual recovery results in Section 6.2. These analyses examine whether the main findings are
robust to an alternative point-recovery criterion, continue to hold for aggregate counterfactual outcomes,
and extend beyond the energy score used in the main figure.
Figure EC.9 reports the results over the same missingness patterns and levels as in the main analysis. The
ranking is similar to that obtained with MAE.CFT-DIFFremains highly stable as the missing region expands
and yields the lowest RMSE throughout the three designs. The two alternative diffusion models deteriorate
more rapidly with missingness, whileTFIis particularly sensitive to the size and structure of the missing
region. Thus, the point-recovery advantage documented in the main text is not specific to the absolute-error
criterion.
Pointwise accuracy need not imply accurate recovery of aggregates formed from the missing trajectory.
This distinction is relevant for the empirical analysis because the causal estimands aggregate counterfactual

e-companion toKong et al.:Conditional Tensor Diffusionec39
Figure EC.9Additional point counterfactual recovery measured by RMSE.
Note.The figure reports RMSE across different missingness levels under the switchback, staggered-adoption, and simultaneous-
adoption patterns. The horizontal axis reports the realized missing proportion relative to the empirical treated share,ρ/ρ emp,
and the vertical dashed line indicatesρ=ρ emp. Point predictions for the three diffusion methods are obtained by averaging the
100 generated counterfactual draws. Lower values indicate better recovery. The inset in each panel is a local enlargement of the
corresponding region in the original panel.
Figure EC.10Recovery of aggregate household–day counterfactual outcomes.
Note.The figure evaluates recovery of household–day totals across different missingness levels. For each artificially masked
household–day, the recovered and observed outcomes are first aggregated over the missing 24-hour trajectory. Panels (a)–(c) report
MAE and Panels (d)–(f) report RMSE under the switchback, staggered-adoption, and simultaneous-adoption patterns, respectively.
The horizontal axis reportsρ/ρ emp, and the vertical dashed line indicatesρ=ρ emp. Lower values indicate better recovery.

ec40 e-companion toKong et al.:Conditional Tensor Diffusion
outcomes across hours. We sum the 24 hourly outcomes within each artificially masked household–day
before computing the recovery error. Figure EC.10 reports MAE and RMSE for these household–day totals.
CFT-DIFFremains among the most accurate methods under all three missingness patterns and is substan-
tially more stable than the alternative diffusion models as the missing proportion increases. The results
indicate that its pointwise recovery performance carries over to aggregate counterfactual outcomes rather
than disappearing after temporal aggregation.
Figure EC.11Distribution of household–day counterfactual recovery errors.
Note.The figure reports empirical cumulative distribution functions of household–day recovery errors at the available missingness
level closest to the empirical treated share. Panels (a)–(c) report household–day MAE and Panels (d)–(f) report household–day
RMSE under the switchback, staggered-adoption, and simultaneous-adoption patterns, respectively. Errors are computed separately
for each artificially masked household–day over its 24-hour trajectory. Curves farther to the left indicate smaller recovery errors.
The inset in each panel provides a local enlargement of the low-error region.
Figure EC.11 reports the empirical distributions of household–day MAE and RMSE at the missingness
level closest to the empirical treated share. The distributions forCFT-DIFFare concentrated in the low-error
region under all three designs. The differences are particularly visible relative toTFIand remain present
relative to the two diffusion benchmarks. Hence, the favorable average performance ofCFT-DIFFreflects
broadly lower recovery errors across the masked household–days rather than improvements concentrated in
a small subset of observations.
Finally, we provide additional evidence on distributional recovery. Whereas the main figure uses the
energy score to evaluate the joint 24-hour trajectory, Figure EC.12 considers two complementary criteria.
CRPS evaluates the marginal distribution of individual hourly outcomes, while WIS evaluates the distribu-
tion of household–day totals through multiple central intervals. Across all three missingness patterns, both

e-companion toKong et al.:Conditional Tensor Diffusionec41
Figure EC.12Additional counterfactual distribution recovery across missingness levels.
Note.The figure evaluates counterfactual distribution recovery for the three diffusion methods across different missingness levels.
Panels (a)–(c) report CRPS for individual hourly outcomes, and Panels (d)–(f) report WIS for household–day totals under the
switchback, staggered-adoption, and simultaneous-adoption patterns, respectively. The horizontal axis reportsρ/ρ emp, and the
vertical dashed line indicatesρ=ρ emp. Lower values indicate better distributional recovery.
scores increase as the missing region expands, but substantially more slowly forCFT-DIFF.CFT-DIFFhas
the lowest CRPS and WIS at every reported missingness level, showing that its distributional advantage is
present for both hourly marginals and aggregate counterfactual outcomes.
Table EC.6 reports all distributional measures at the missingness level closest to that observed in the
application. Under each missingness pattern,CFT-DIFFhas the lowest energy score, CRPS, interval score,
and WIS. Its 90% intervals are also narrower than those of the alternative diffusion models, with coverage
remaining reasonably close to 0.90. Under staggered adoption, for example, the interval width decreases
from 2.2037 forTUCKER-DIFFto 1.7198 forCFT-DIFF, with coverage of 0.920. The switchback and
simultaneous-adoption designs show the same combination of lower distributional scores and sharper inter-
vals.
EC.5.3.3. Counterfactual Trajectory RecoveryThe preceding analyses summarize counterfactual
recovery using scalar error and distributional measures. These measures do not reveal whether a method
recovers the intraday shape of the missing outcome, including the timing and magnitude of demand peaks.
We therefore complement them with trajectory-level comparisons. For each artificially masked household
group, the first column of the figures compares the observed no-policy trajectory with the five point esti-
mators. The remaining columns reportCONV-DIFF,TUCKER-DIFF, andCFT-DIFF. The solid curve is the

ec42 e-companion toKong et al.:Conditional Tensor Diffusion
Table EC.6Counterfactual distribution recovery across missingness patterns.
Panel A: Switchback
Method Energy score CRPS 90% coverage 90% width IS WIS
CONV-DIFF0.1479 0.0239 0.887 1.7246 2.6548 0.2569
TUCKER-DIFF0.1476 0.0239 0.907 1.8352 2.6898 0.2583
CFT-DIFF0.1314 0.0210 0.893 1.2559 2.0126 0.1819
Panel B: Staggered adoption
Method Energy score CRPS 90% coverage 90% width IS WIS
CONV-DIFF0.1546 0.0254 0.950 2.8132 3.1717 0.3034
TUCKER-DIFF0.1553 0.02550.9052.2037 3.0402 0.3102
CFT-DIFF0.1358 0.02170.920 1.7198 2.2905 0.2140
Panel C: Simultaneous adoption
Method Energy score CRPS 90% coverage 90% width IS WIS
CONV-DIFF0.1510 0.0244 0.942 2.2955 2.7606 0.2680
TUCKER-DIFF0.1509 0.02450.8961.9824 2.8150 0.2825
CFT-DIFF0.1364 0.02180.919 1.6321 2.2463 0.2075
Note.The table evaluates the three diffusion methods at the available missingness level closest to the empirical treated share,ρ emp =
0.265. The common target missing proportion is 0.284, with realized missing proportions of 0.283, 0.284, and 0.284 under the switch-
back, staggered-adoption, and simultaneous-adoption patterns, respectively. The energy score evaluates the joint 24-hour trajectory,
CRPS evaluates individual hourly outcomes, and the interval-based measures are computed for household–day totals. Errors, scores,
and interval widths are reported in the normalized experimental scale. Lower values are better for the energy score, CRPS, IS, and WIS;
coverage is evaluated by closeness to 0.90, and a smaller width indicates a sharper interval when coverage is comparable. Boldface
and underlining indicate the best and second-best values within each panel, respectively.
median of the generated group-average trajectories, and the shaded regions are the central 50% and 90%
counterfactual prediction intervals.
Figures EC.13, EC.14, and EC.15 examine trajectory recovery as the number of households in each
group increases. This design separates errors that are specific to small groups from errors that persist after
aggregation. For small groups, the realized trajectories contain substantial hour-to-hour variation, and the
differences across methods are correspondingly more visible. Among the point estimators,DID,SC,SDID,
andNMCgenerally recover the overall level and shape, whereasTFIcan be unstable when only a few house-
holds are averaged. The three diffusion models produce smoother counterfactual trajectories, butCONV-
DIFFand especiallyTUCKER-DIFFtend to attenuate local peaks.CFT-DIFFfollows the observed trajectory
more closely while retaining the main intraday variation.
As the group size increases, idiosyncratic household variation is averaged out and the trajectories become
progressively smoother. TheCFT-DIFFmedian becomes tightly aligned with the observed group-average
trajectory, and its counterfactual prediction intervals also become more concentrated. The same pattern is
visible under switchback, staggered adoption, and simultaneous adoption. Thus, the recovery performance
is not confined to large aggregates:CFT-DIFFremains informative for relatively small groups and becomes
increasingly precise as the counterfactual object is aggregated over more households.
Figures EC.16, EC.17, and EC.18 repeat the comparison for nonoverlapping random household groups.
The resulting trajectories vary meaningfully across groups in both their levels and peak patterns, providing
a more demanding check on the cross-sectional stability of the recovery methods. The main conclusions are
similar across the three groups and missingness patterns. The stronger point estimators generally reproduce
the broad group-average profile, whileTFIexhibits noticeably larger deviations in several cases. Among the
diffusion models,CFT-DIFFconsistently preserves more of the observed intraday variation. By comparison,
CONV-DIFFandTUCKER-DIFFtend to smooth the morning and evening peaks and, for some groups, shift

e-companion toKong et al.:Conditional Tensor Diffusionec43
Figure EC.13Counterfactual trajectories across nested household groups under switchback missingness.
Note.The figure compares recovered 24-hour counterfactual trajectories as the number of households included in the group average
increases under the switchback pattern. Rows correspond to nested household groups of increasing size. The first column reports
the observed trajectory together with the five point estimators; the remaining columns reportCONV-DIFF,TUCKER-DIFF, andCFT-
DIFF, respectively. For each diffusion method, the solid line denotes the median generated trajectory and the shaded regions denote
the 50% and 90% central counterfactual prediction intervals.
the trajectory downward. The similarity of these results across independently formed groups indicates that
the trajectory-level performance is not driven by a particular household composition.
Figures EC.19, EC.20, and EC.21 stratify households by demand volatility measured from the observed
outcomes. Differences across methods are relatively small for the low-volatility groups but become more
pronounced as volatility increases. In the high-volatility groups, the observed trajectory displays larger

ec44 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.14Counterfactual trajectories across nested household groups under staggered adoption.
Note.The figure compares recovered 24-hour counterfactual trajectories as the number of households included in the group average
increases under staggered adoption. Rows correspond to nested household groups of increasing size. The first column reports the
observed trajectory together with the five point estimators; the remaining columns reportCONV-DIFF,TUCKER-DIFF, andCFT-DIFF,
respectively. For each diffusion method, the solid line denotes the median generated trajectory and the shaded regions denote the
50% and 90% central counterfactual prediction intervals.
intraday movements and more pronounced peaks.CONV-DIFFandTUCKER-DIFFtend to attenuate these
movements, whereas theCFT-DIFFmedian remains much closer to the observed trajectory. The counter-
factual bands also become wider for the more volatile groups, reflecting the greater uncertainty associated
with recovering their missing trajectories. The same qualitative pattern appears under all three missingness
structures.

e-companion toKong et al.:Conditional Tensor Diffusionec45
Figure EC.15Counterfactual trajectories across nested household groups under simultaneous adoption.
Note.The figure compares recovered 24-hour counterfactual trajectories as the number of households included in the group average
increases under simultaneous adoption. Rows correspond to nested household groups of increasing size. The first column reports
the observed trajectory together with the five point estimators; the remaining columns reportCONV-DIFF,TUCKER-DIFF, andCFT-
DIFF, respectively. For each diffusion method, the solid line denotes the median generated trajectory and the shaded regions denote
the 50% and 90% central counterfactual prediction intervals.
Figures EC.22, EC.23, and EC.24 divide households into low-, middle-, and high-demand groups using
their observed outcomes. Recovery is relatively similar across methods for the low-demand groups, where
the trajectories are comparatively flat. The differences become clearer for the middle- and high-demand
groups, whose trajectories exhibit larger morning and evening peaks.CFT-DIFFadjusts to these changes
in both level and shape and remains close to the observed trajectory. In contrast, the two nested diffusion

ec46 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.16Counterfactual trajectories across random household groups under switchback missingness.
Note.The figure examines whether trajectory recovery depends on the composition of the household group under the switchback
pattern. Each row corresponds to a different randomly selected household group. The first column reports the observed trajectory
and the five point estimators; the remaining columns report the three diffusion methods. Solid diffusion curves denote median
generated trajectories, with 50% and 90% central counterfactual prediction intervals shown by the shaded regions.
benchmarks tend to understate the higher-demand portions of the curve, particularly around peak hours.
The point estimators other thanTFIalso track the broad demand profile reasonably well, but they do not
provide the conditional distribution around the recovered trajectory. These results suggest that the gains
from counterfactual conditioning are particularly useful when the missing trajectory has more pronounced
systematic variation.
Figures EC.25, EC.26, and EC.27 repeat the comparison across different artificially masked days. The
selected days differ in both average electricity use and the shape of the intraday profile. Nevertheless, the
same broad ranking remains visible.CFT-DIFFclosely follows changes in the level, timing, and magnitude of
the observed demand peaks across days, whileCONV-DIFFandTUCKER-DIFFgenerally produce smoother
trajectories and can understate relatively sharp movements. Several point estimators remain competitive
for the average trajectory, althoughTFIagain exhibits substantial instability on some days. Overall, the
trajectory evidence complements the scalar recovery measures in Section EC.5.3.2: the advantage ofCFT-
DIFFis not limited to average error reductions, but is also reflected in its ability to recover the shape of the
missing 24-hour counterfactual trajectory across different aggregation levels, household groups, and time
periods.

e-companion toKong et al.:Conditional Tensor Diffusionec47
Figure EC.17Counterfactual trajectories across random household groups under staggered adoption.
Note.The figure examines whether trajectory recovery depends on the composition of the household group under staggered adop-
tion. Each row corresponds to a different randomly selected household group. The first column reports the observed trajectory and
the five point estimators; the remaining columns report the three diffusion methods. Solid diffusion curves denote median generated
trajectories, with 50% and 90% central counterfactual prediction intervals shown by the shaded regions.
EC.5.4. Additional Results on Demand Response
This section provides additional analyses of the demand responses reported in Section 6.4. We examine
hourly response heterogeneity, price intensity and profile design, repeated intervention exposure, and het-
erogeneity across temperature, regions, and household characteristics.
Aggregate effects can conceal substantial variation across treated observations. Figure EC.28 therefore
reports the distribution of hourly demand reductions across household–policy-day observations, using the
mean of 100CFT-DIFFconditional draws for each observation. The medians are generally close to zero,
while the distributions remain wide at many hours, indicating considerable variation across households and
intervention days. This variation is especially visible during the daytime and evening periods, when elec-
tricity use is relatively high. The aggregate estimates therefore do not characterize all treated observations
uniformly: under the same price signal, some household–day observations exhibit sizable demand reduc-
tions, whereas others show little change or an increase at particular hours.
Figure EC.29 reports the corresponding distributions of relative demand reductions. The results are qual-
itatively similar to the absolute-effect distributions in Figure EC.29. The medians remain generally close
to zero, while the distributions are wide across households and intervention days, indicating substantial
heterogeneity in hourly demand responses. Thus, expressing the effects relative to the estimated no-policy
counterfactual does not materially change the main patterns documented in Section 6.4.

ec48 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.18Counterfactual trajectories across random household groups under simultaneous adoption.
Note.The figure examines whether trajectory recovery depends on the composition of the household group under simultaneous
adoption. Each row corresponds to a different randomly selected household group. The first column reports the observed trajectory
and the five point estimators; the remaining columns report the three diffusion methods. Solid diffusion curves denote median
generated trajectories, with 50% and 90% central counterfactual prediction intervals shown by the shaded regions.
Figure EC.30 further examines whether the demand response varies with price intensity and profile
design. Panel (a) shows that the peak-demand reduction increases with the peak price for profileP. The
estimates for profileBremain close to zero, while the responses for profilesAandP0are not monotone
and several estimates remain imprecise. Panel (b) shows larger estimated reductions for thePprofile than
for the B profile at peak prices of 5, 10, and 15 NOK/kWh, with the corresponding 95% intervals excluding
zero. Most other profile-design comparisons remain imprecise, with intervals including zero. These results
indicate that the relationship between price intensity and demand response depends on the price profile,
with the clearest dose–response pattern occurring for profileP.
Figure EC.31 next examines whether the demand response changes with repeated intervention exposure.
Panels (a) and (c) show no monotone relationship between the response and cumulative exposure. The
estimates decline after the first intervention, remain similar for the 2–5 and 6–10 exposure groups, and then
increase for the 11+ group. Panels (b) and (d) show a clearer pattern for intervention spacing: the estimated
peak-demand reduction increases with the time since the previous intervention and is largest for the 7+
day group, although the intervals remain wide. Taken together, these results provide limited evidence of a
systematic learning or fatigue pattern across repeated interventions, but suggest a stronger response when
interventions are spaced farther apart.
The preceding analysis shows that demand response varies with the design and timing of the intervention.
We next examine whether it also varies with outdoor temperature, an important source of variation in resi-

e-companion toKong et al.:Conditional Tensor Diffusionec49
Figure EC.19Counterfactual trajectories across household demand-volatility groups under switchback missingness.
Note.The figure evaluates trajectory recovery across household groups with different levels of demand volatility under the switch-
back pattern. Households are grouped using demand variation measured from the observed portion of the data. Rows correspond to
the resulting volatility groups. The first column reports the observed trajectory and the five point estimators; the remaining columns
report the three diffusion methods together with their median trajectories and 50% and 90% central counterfactual prediction inter-
vals.
dential electricity demand. We classify the previous 24-hour average outdoor temperature into six intervals:
≤−15◦C,(−15,−10] ◦C,(−10,−5] ◦C,(−5,0] ◦C,(0,5] ◦C, and>5 ◦C. We first estimate the average peak-
demand response within each temperature interval, controlling for price signal, region, baseline demand,
and intervention order. We then examine whether the temperature relationship differs across price-profile
designs. For this analysis, the price signals are grouped into three profile classes: short profiles (Pand
P0), extended profiles (B), and dual-peak profiles (AandC). Panels (b) and (d) report the corresponding
temperature-response relationships for these three profile classes, controlling for region, baseline demand,
and intervention order. The analysis is conducted at the region–intervention-event level, with observations
weighted by the number of households in each event.
Figure EC.32 shows a clear relationship between outdoor temperature and demand response. Panels (a)
and (c) reveal a strong monotone pattern in the pooled estimates: as outdoor temperature increases, both rel-
ative and absolute peak-demand reductions increase steadily. At temperatures below−15◦C, the estimated
response is strongly negative, whereas it approaches zero around0 ◦C and becomes positive at higher tem-
peratures. Panels (b) and (d) show that this pattern is not driven by a single price-profile design. The short,
extended, and dual-peak profiles all exhibit generally increasing demand reductions as temperature rises,
although the estimates are less precise for some temperature–profile combinations. Overall, the results indi-

ec50 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.20Counterfactual trajectories across household demand-volatility groups under staggered adoption.
Note.The figure evaluates trajectory recovery across household groups with different levels of demand volatility under staggered
adoption. Households are grouped using demand variation measured from the observed portion of the data. Rows correspond to the
resulting volatility groups. The first column reports the observed trajectory and the five point estimators; the remaining columns
report the three diffusion methods together with their median trajectories and 50% and 90% central counterfactual prediction
intervals.
cate that households respond more strongly to dynamic pricing under warmer conditions, while peak-period
electricity use is less responsive during very cold periods.
Given the strong temperature pattern in Figure Figure EC.32, we next examine whether regional dif-
ferences remain after controlling for temperature. Figure EC.33 shows that some regional heterogeneity
persists. Bergen has a relative-effect estimate close to zero but a negative absolute-effect estimate whose
confidence interval excludes zero. Relative peak-demand reductions are positive in the other regions and
are largest in Stavanger and Trondheim, although the estimate for Stavanger is imprecise. The correspond-
ing intervals exclude zero for Oslo and Trondheim. In absolute terms, the estimates for the other regions
are close to zero or positive, with relatively wide confidence intervals. The estimates therefore do not indi-
cate a simple geographic pattern. Because the specifications already control for outdoor temperature, these
differences are unlikely to reflect temperature alone. They may instead capture remaining regional differ-
ences in household characteristics, housing conditions, heating technologies, or electricity-use patterns that
are not separately identified in our data. We therefore interpret the results as evidence of residual regional
heterogeneity rather than as causal effects of location.
We finally examine heterogeneity across household electricity-use characteristics measured before the
first intervention. For each household, we construct four pre-intervention characteristics: average electricity
demand, the share of electricity use during peak hours, the share during evening hours, and load volatility.

e-companion toKong et al.:Conditional Tensor Diffusionec51
Figure EC.21Counterfactual trajectories across household demand-volatility groups under simultaneous adoption.
Note.The figure evaluates trajectory recovery across household groups with different levels of demand volatility under simultane-
ous adoption. Households are grouped using demand variation measured from the observed portion of the data. Rows correspond to
the resulting volatility groups. The first column reports the observed trajectory and the five point estimators; the remaining columns
report the three diffusion methods together with their median trajectories and 50% and 90% central counterfactual prediction inter-
vals.
Households are ranked separately by each characteristic and divided into five equally sized groups, with Q1
denoting the lowest quintile and Q5 the highest. We also construct each household’s average 24-hour pre-
intervention load profile and normalize it by total daily use, so that the resulting profile captures the timing
rather than the level of electricity consumption. We then applyK-means clustering to these normalized
profiles and classify households into four load-shape clusters, C1–C4. The cluster labels are ordered by the
center of the daily load profile, from earlier to later concentration of electricity use. These classifications
are constructed using only electricity use observed before treatment and therefore do not depend on the
estimated treatment effects.
Figure EC.34 shows substantial heterogeneity in peak-demand response across these household groups,
although the patterns are generally nonmonotone. Panel (a) exhibits the largest differences across baseline-
demand quintiles: households in Q1 and Q4 show positive peak-demand reductions, whereas Q2 and Q5
show negative responses and Q3 is close to zero. The differences across peak-hour and evening-load shares
in Panels (b) and (c) are more modest, and all corresponding confidence intervals include zero. Panel (d)
also shows a nonmonotone pattern across load volatility, with Q5 exhibiting the largest positive response.
Panel (e) shows variation across intraday load-shape clusters, with the highest point estimate for C3 and the
lowest for C4, although the intervals are wide and overlap substantially. Overall, the results indicate mean-

ec52 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.22Counterfactual trajectories across household demand-level groups under switchback missingness.
Note.The figure evaluates trajectory recovery across household groups with different levels of average electricity use under the
switchback pattern. Households are grouped according to their mean demand computed from the observed portion of the data.
Rows correspond to the resulting demand-level groups. The first column reports the observed trajectory and the five point estima-
tors; the remaining columns report the three diffusion methods together with their median trajectories and 50% and 90% central
counterfactual prediction intervals.
ingful household heterogeneity in demand response, but no single pre-intervention characteristic provides a
simple ordering of households by their response to dynamic pricing.
Table EC.7 provides the corresponding estimates for the household groups in Figure EC.34. As described
above, the four continuous pre-intervention characteristics are divided into quintiles across treated house-
holds, while normalized 24-hour load profiles are classified into four load-shape clusters. For each house-
hold, we first average the 100CFT-DIFFdraws to obtain the estimated no-policy counterfactual and then
aggregate the counterfactual and observed demand over all of that household’s intervention days and the
corresponding signal-specific peak-price hours. For a subgroupG, letY 0
i andY obs
i denote these aggregated
counterfactual and observed outcomes for householdi, and letn i denote its number of intervention days.
We report the pooled relative peak-demand reduction
bRG = 100
P
i∈G
 
Y 0
i −Y obs
i

P
i∈GY 0
i
,
and the corresponding absolute reduction per household–policy day,
bAG =
P
i∈G
 
Y 0
i −Y obs
i

P
i∈Gni
.

e-companion toKong et al.:Conditional Tensor Diffusionec53
Figure EC.23Counterfactual trajectories across household demand-level groups under staggered adoption.
Note.The figure evaluates trajectory recovery across household groups with different levels of average electricity use under stag-
gered adoption. Households are grouped according to their mean demand computed from the observed portion of the data. Rows
correspond to the resulting demand-level groups. The first column reports the observed trajectory and the five point estimators; the
remaining columns report the three diffusion methods together with their median trajectories and 50% and 90% central counterfac-
tual prediction intervals.
Positive values therefore indicate lower observed demand relative to the estimated no-policy counterfactual.
To quantify sampling uncertainty, we resample households with replacement within each subgroup, keep-
ing each sampled household’s complete intervention history together, and recompute bRG in each of 1,000
bootstrap samples. The reported 95% confidence interval is given by the 2.5th and 97.5th percentiles of
these bootstrap estimates.
The estimates confirm substantial and nonmonotone household heterogeneity. The clearest differences
occur across baseline-demand quintiles. Q1 has the largest positive relative reduction, at 2.84%, with a
95% confidence interval of [1.72, 4.10], while Q4 also has a positive reduction of 1.85%. By contrast, Q2
and Q5 have negative estimates, and the estimate for Q3 is close to zero. The differences across peak-
hour and evening-load shares are more modest, with all corresponding confidence intervals including zero.
Load volatility exhibits a nonmonotone pattern: Q1 has a negative response, whereas Q5 has a positive
response, and both intervals exclude zero. The estimates also vary across load-shape clusters, although
their confidence intervals are wide and include zero. The absolute estimates show that relative and absolute
responses need not rank households in the same way. For example, Q1 of baseline demand has the largest
relative reduction, whereas Q4 has the largest absolute reduction, at 0.581 kWh per household–policy day.
Overall, the table reinforces the conclusion that household response to dynamic pricing varies with pre-

ec54 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.24Counterfactual trajectories across household demand-level groups under simultaneous adoption.
Note.The figure evaluates trajectory recovery across household groups with different levels of average electricity use under simul-
taneous adoption. Households are grouped according to their mean demand computed from the observed portion of the data. Rows
correspond to the resulting demand-level groups. The first column reports the observed trajectory and the five point estimators; the
remaining columns report the three diffusion methods together with their median trajectories and 50% and 90% central counterfac-
tual prediction intervals.
intervention electricity-use patterns, but this heterogeneity cannot be summarized by a simple monotone
relationship with any single household characteristic.

e-companion toKong et al.:Conditional Tensor Diffusionec55
Figure EC.25Counterfactual trajectories across missing days under switchback missingness.
Note.The figure evaluates trajectory recovery on different artificially masked days under the switchback pattern. Each row cor-
responds to a different missing day and reports the average trajectory for the selected households on that day. The first column
reports the observed trajectory and the five point estimators; the remaining columns reportCONV-DIFF,TUCKER-DIFF, andCFT-
DIFF, respectively. For each diffusion method, the solid line denotes the median generated trajectory and the shaded regions denote
the 50% and 90% central counterfactual prediction intervals.

ec56 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.26Counterfactual trajectories across missing days under staggered adoption.
Note.The figure evaluates trajectory recovery on different artificially masked days under staggered adoption. Each row corresponds
to a different missing day and reports the average trajectory for the selected households on that day. The first column reports
the observed trajectory and the five point estimators; the remaining columns reportCONV-DIFF,TUCKER-DIFF, andCFT-DIFF,
respectively. For each diffusion method, the solid line denotes the median generated trajectory and the shaded regions denote the
50% and 90% central counterfactual prediction intervals.

e-companion toKong et al.:Conditional Tensor Diffusionec57
Figure EC.27Counterfactual trajectories across missing days under simultaneous adoption.
Note.The figure evaluates trajectory recovery on different artificially masked days under simultaneous adoption. Each row corre-
sponds to a different missing day and reports the average trajectory for the selected households on that day. The first column reports
the observed trajectory and the five point estimators; the remaining columns reportCONV-DIFF,TUCKER-DIFF, andCFT-DIFF,
respectively. For each diffusion method, the solid line denotes the median generated trajectory and the shaded regions denote the
50% and 90% central counterfactual prediction intervals.

ec58 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.28Distribution of hourly demand reductions by price signal.
Note.Each boxplot reports the distribution of hourly demand reductions across household–policy-day observations. The no-policy
counterfactual is first averaged over 100CFT-DIFFconditional draws, and the demand reduction is defined as counterfactual demand
minus observed demand, so positive values indicate lower demand under the assigned price signal. Boxes denote the interquartile
range, the center line denotes the median, and whiskers extend from the 5th to the 95th percentile. Individual outliers are omitted.
Background shading indicates the experimental electricity price.

e-companion toKong et al.:Conditional Tensor Diffusionec59
Figure EC.29Distribution of hourly relative demand reductions by price signal.
Note.Each boxplot reports the distribution of hourly relative demand reductions across household–policy-day observations. For
each observation, the no-policy counterfactual is first averaged over the 100CFT-DIFFdraws. Positive values indicate lower observed
demand relative to the estimated no-policy counterfactual. Boxes denote the interquartile range, the center line denotes the median,
and whiskers extend from the 5th to the 95th percentile. Individual outliers are omitted. Background shading indicates the experi-
mental electricity price.

ec60 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.30Demand response across price intensity and profile design.
Note.Panel (a) reports peak-period relative demand reductions across peak-price levels within each price profile, using experimen-
tal groups observed under all price levels within the corresponding profile. Profile C is omitted because it does not have a single
peak-price level. Panel (b) reports pairwise differences in peak-period relative demand reductions across price-signal designs. Filled
circles denote common-group comparisons, and open squares denote covariate-adjusted cross-group comparisons. Error bars report
95% intervals. In Panel (b), positive values indicate a larger demand reduction for the first price signal in each comparison.
Table EC.7Detailed estimates of household heterogeneity in peak-demand reductions.
Characteristic Subgroup Households Relative % 95% CI Absolute kWh
Baseline demand quintile 1 621 2.84 [1.72, 4.10] 0.168
Baseline demand quintile 2 620 -0.91 [-1.68, -0.10] -0.133
Baseline demand quintile 3 621 0.24 [-0.50, 0.91] 0.051
Baseline demand quintile 4 620 1.85 [1.32, 2.40] 0.581
Baseline demand quintile 5 621 -1.52 [-2.13, -0.94] -0.676
Peak-hour share quintile 1 621 -0.46 [-1.38, 0.42] -0.103
Peak-hour share quintile 2 620 -0.06 [-0.60, 0.52] -0.017
Peak-hour share quintile 3 621 0.41 [-0.29, 1.18] 0.108
Peak-hour share quintile 4 620 0.06 [-0.80, 0.89] 0.013
Peak-hour share quintile 5 621 -0.04 [-0.82, 0.87] -0.008
Evening-load share quintile 1 621 -0.39 [-1.17, 0.27] -0.100
Evening-load share quintile 2 620 -0.17 [-0.83, 0.53] -0.045
Evening-load share quintile 3 621 0.17 [-0.58, 0.88] 0.046
Evening-load share quintile 4 620 0.28 [-0.45, 1.04] 0.066
Evening-load share quintile 5 621 0.18 [-0.59, 1.04] 0.026
Load-volatility quintile 1 621 -0.81 [-1.54, -0.16] -0.258
Load-volatility quintile 2 620 0.48 [-0.12, 1.10] 0.142
Load-volatility quintile 3 621 0.48 [-0.17, 1.16] 0.121
Load-volatility quintile 4 620 -0.71 [-1.47, 0.02] -0.147
Load-volatility quintile 5 621 1.33 [0.19, 2.58] 0.133
Load-shape cluster 1 1893 -0.16 [-0.57, 0.24] -0.043
Load-shape cluster 2 521 0.38 [-0.37, 1.13] 0.097
Load-shape cluster 3 392 1.02 [-0.23, 2.35] 0.140
Load-shape cluster 4 297 -0.73 [-2.10, 0.83] -0.098
Note.Subgroups are constructed from electricity use observed before each household’s first intervention. Relative
effects are pooled ratio-of-sums estimates. Absolute effects are kWh reductions per household–policy day over
the corresponding signal-specific peak-price hours. Confidence intervals are obtained from a household bootstrap.
Positive values indicate demand reductions.

e-companion toKong et al.:Conditional Tensor Diffusionec61
Figure EC.31Demand response by cumulative exposure and intervention spacing.
Note.Panels (a) and (c) report relative and absolute peak-demand reductions by cumulative intervention exposure, grouped into 1,
2–5, 6–10, and 11 or more prior and current intervention events. Panels (b) and (d) report the corresponding effects by the number of
days since the previous intervention, grouped into 0, 1–6, and 7 or more days. Estimates adjust for price signal, region, and baseline
demand, as well as temperature when available; the intervention-spacing specifications additionally control for intervention order.
Error bars report 95% intervals. Positive values indicate demand reductions.

ec62 e-companion toKong et al.:Conditional Tensor Diffusion
Figure EC.32Demand response by outdoor temperature.
Note.Panels (a) and (c) report pooled relative and absolute peak-demand reductions across outdoor-temperature bins. Panels (b)
and (d) report the corresponding estimates separately for short, extended, and dual-peak price profiles. The pooled estimates adjust
for price signal, region, baseline demand, and intervention order; the profile-specific estimates adjust for region, baseline demand,
and intervention order. Error bars report 95% intervals. Positive values indicate demand reductions.
Figure EC.33Regional heterogeneity in peak-demand reductions.
Note.Panel (a) reports relative peak-demand reductions by region, and Panel (b) reports the corresponding absolute reductions.
Estimates adjust for price signal, baseline demand, intervention order, and temperature when available. Error bars report 95%
intervals. Positive values indicate demand reductions.

e-companion toKong et al.:Conditional Tensor Diffusionec63
Figure EC.34Household heterogeneity in peak-demand reductions.
Note.Panels (a)–(e) report relative peak-demand reductions across subgroups defined by pre-intervention baseline demand, peak-
hour load share, evening-load share, load volatility, and load shape, respectively. Household characteristics are constructed using
electricity use observed before each household’s first intervention. Q1–Q5 denote quintiles, and C1–C4 denote clusters of normal-
ized 24-hour pre-intervention load profiles. Error bars report 95% intervals obtained from a household bootstrap. Positive values
indicate demand reductions.
