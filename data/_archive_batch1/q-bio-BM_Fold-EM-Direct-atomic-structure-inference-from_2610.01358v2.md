# Fold'EM: Direct atomic structure inference from Cryo-EM particles

> **领域**：`q-bio.BM`　**发布**：2026-10-01　**arXiv**：[2610.01358v2](https://arxiv.org/abs/2610.01358v2)
>
> **作者**：Advaith Maddipatla, Märt-Erik Mäeots, Marco Pegoraro, Nikolaus Dräger 等 8 人
>
> **来源**：arXiv 预印本（开放获取）　**页数**：47

---

## Abstract

Single-particle cryo-electron microscopy (cryo-EM) has become a widely adopted technique for biomolecular structure determination. The conventional cryo-EM computational pipeline first combines many particle images to reconstruct an electrostatic potential (ESP) map and then fits an atomic model to the recovered map. Density reconstruction has high sample complexity, requiring large numbers of particle images and making structure determination high-cost and low-throughput, particularly for heterogeneous samples. Downstream atomic model building, in turn, becomes increasingly difficult as the resolution of the reconstructed map deteriorates. Protein structure prediction models provide strong sequence-derived priors on atomic structure, and experiment-guided approaches can use these priors to recover structures consistent with experimental measurements. Yet, in cryo-EM, such priors are typically integrated only after density reconstruction during atomic model fitting. We introduce Fold'EM, an inference-time framework that combines priors from protein generative models directly with cryo-EM particle images to determine atomic models from a small number of single particle images, bypassing both intermediate density reconstruction and downstream model building against the reconstructed map. Across synthetic and experimental cryo-EM datasets, Fold'EM recovers accurate atomic structures both with known particle orientations and in an ab-initio setting where orientations are inferred jointly with structure. In heterogeneous datasets, Fold'EM further resolves distinct conformational states from mixed particle populations without separately reconstructing a density map and building an atomic model for each state. We believe these results open new avenues for structure determination in the low-sample regime and for characterizing low-population conformational states directly from cryo-EM particles.

---

## 正文（由 PDF 提取）

Fold’EM: Direct atomic structure inference from Cryo-EM particles
Advaith Maddipatla1,* Märt-Erik Mäeots2,* Marco Pegoraro1,* Nikolaus Dräger1
Roberto Covino3 Sanketh Vedula4,5,† Martin Pacesa2,† Alex Bronstein1,†
1Institute of Science and Technology Austria 2University of Zurich
3Frankfurt Institute for Advanced Studies 4Princeton University
5Broad Institute of MIT and Harvard

## Abstract

Single-particle cryo-electron microscopy (cryo-EM) has become a widely adopted technique for
biomolecular structure determination. The conventional cryo-EM computational pipeline first combines
many particle images to reconstruct an electrostatic potential (ESP) map and then fits an atomic model
to the recovered map. Density reconstruction has high sample complexity, requiring large numbers
of particle images and making structure determination high-cost and low-throughput, particularly for
structurally heterogeneous samples. Downstream atomic model building, in turn, becomes increasingly
difficult as the resolution of the reconstructed map deteriorates. Protein structure prediction models
provide strong sequence-derived priors on atomic structure, and experiment-guided approaches can
use these priors to recover structures consistent with experimental measurements. Yet, in cryo-EM,
such priors are typically integrated only after density reconstruction during atomic model fitting. We
introduce Fold’EM, an inference-time framework that combines priors from protein structure generative
models directly with cryo-EM particle images to determine atomic models from a small number of single
particle images, bypassing both intermediate density reconstruction and downstream model building
against the reconstructed map. Across synthetic benchmarks and experimental cryo-EM data, Fold’EM
recovers accurate atomic structures both with known particle orientations and in anab initiosetting
where orientations are inferred jointly with structure. In heterogeneous datasets, Fold’EM further resolves
distinct conformational states from mixed particle populations without separately reconstructing a density
map and building an atomic model for each state. We believe these results open new avenues for structure
determination in the low-sample regime and for characterizing low-population conformational states
directly from cryo-EM particles.

## Introduction

Single-particle cryo-electron microscopy (cryo-EM) has transformed structural biology by enabling high-
resolution structure determination of large macromolecular assemblies without crystallization (Fernandez-
Leiro and Scheres, 2016). Its ability to image individual molecules in different conformations also provides a
route to understanding how structural changes drive biological function (Ourmazd, 2019; Mäeots and Enchev,
2022). Yet the fundamental measurement is extremely noisy. Radiation damage limits the electron dose that
can be applied to each particle, leaving individual images unsuitable for direct structural interpretation and
requiring large numbers of observations to be aligned and combined into a three-dimensional electrostatic
potential (ESP) map (Scheres, 2012; Kimanius et al., 2024). The resulting density must then be interpreted as
an atomic model, a step that can remain difficult despite advances in automated model building, particularly
where local resolution is poor (Jamali et al., 2024; Fadini et al., 2026).
*Equally contributing first authors. †Equally contributing senior authors.
1
arXiv:2610.01358v2 [q-bio.BM] 2 Oct 2026

The demand for coherent averaging creates a tension between spatial resolution and biological complete-
ness. Combining particles from different conformations blurs structural features, whereas separating them
into increasingly homogeneous populations leaves fewer observations available for each state (Frank and
Ourmazd, 2016). Low-population and transient states are especially difficult because they may be merged
with more abundant conformations, excluded during particle selection, or remain too sparsely represented for
independent reconstruction. For scarce samples or proteins that cannot be obtained in sufficient quantity, the
observations required to reconstruct each state may simply not be available.
Heterogeneity modeling can recover conformational variability beyond a small set of discrete structural
classes (Frank and Ourmazd, 2016; Zhong et al., 2021; Gilles and Singer, 2025). However, these approaches
generally require prior particle orientations, and thus remain dependent on upstream particle selection
and alignment. Improving heterogeneous reconstruction therefore addresses only part of the difficulty of
obtaining mechanistic information from sparse, noisy observations, while leaving unresolved the fundamental
requirement for large numbers of particles.
Conventional single-particle cryo-EM reconstruction pipelines primarily estimate densities from image
measurements, making limited use of prior knowledge about protein structures in general, or the sequence
of the sample under study. Blush regularization in RELION demonstrates the value of incorporating such
knowledge by using a denoiser trained on experimental cryo-EM maps to provide richer regularization than a
generic smoothness prior, improving reconstruction when particle signals are weak (Kimanius et al., 2024).
AlphaFold and related prediction models encode knowledge of sequence-dependent folds and interactions
learned from evolutionary and structural data, providing strong sequence-conditioned structural priors (Jumper
et al., 2021; Baek et al., 2021). Building on these priors, a recent line of work has shown that experimental
guidance can steer these models toward conformations consistent with the experimental data but missed
by unconditioned predictions (Maddipatla et al., 2025; 2026b; Fadini et al., 2026; Raghu et al., 2026). In
cryo-EM, however, these approaches have focused on reconstructed maps, applying structural knowledge
after particle selection, alignment, and averaging have already taken place. They therefore inherit the need for
sufficiently many particles to support reliable reconstruction. In this work, we ask:can structural priors be
introduced directly at the particle level, enabling atomic inference from sparse cryo-EM observations without
requiring a high-resolution intermediate reconstruction?
1.1 Contributions and main results
We introduceFold’EM, an inference-time framework that guides protein structure generative models directly
using cryo-EM particle images. Rather than first reconstructing a three-dimensional density and subsequently
building an atomic model into it, Fold’EM uses sequence-conditioned structural priors to infer atomic
structures directly from sparse particle observations. We formulate structure determination as joint inference
over the structural representation and particle-specific latent variables, including pose and conformational
assignment (Figure 1).
Particle vs. density guidance.We characterize when inference from individual particle images can be
replaced by inference from a reconstructed density. For a homogeneous sample with known poses, we show
that the two are equivalent only when density mismatch is measured under the experiment-induced metric
defined by the imaging operators and noise model. The standard density-spaceL2 objective therefore does
not, in general, reproduce the particle likelihood. When poses or conformational assignments are uncertain,
the distinction becomes more fundamental, as collapsing particles into a consensus density can discard
particle-specific information required to infer these latent variables (Figure 2). This provides the statistical
motivation for introducing structural priors directly at the particle level.
2

Adaptorsequence PairformerMSA
AlphaFold3
sequence
database
Particle
embedding 
Particle
classiﬁcation
Ensemble
inference
Pose & class
reﬁnement
Pose
estimation
particles
poses
classes
sequence
Diffusion
generator
 structure
latents
Forward
model
poses
particles
latents update
∇
ESPs
classes
Log
likelihood
Pose
estimation
A
B
C
D
structure
AlphaFold3
Fold'EM ab initio
1000 particles
PDB 9B9J
Integrin α-5
Integrin β-1
BIIG2 Fab
(wrong location)
BIIG2 Fab
(correct location)
Figure 1: Fold’EM infers atomic structures directly from sparse cryo-EM particle images.(A) Fold’EM alternates
structural inference with pose and class refinement. (B) Particle evidence is back-propagated into intermediate
Pairformer states H, filtering experimental updates through the remaining Pairformer blocks before AlphaFold3
diffusion. (C) For the integrin–BIIG2 Fab complex (PDB 9B9J), AlphaFold3 predicts the individual components but
places the Fab at the wrong binding site. (D)Ab initioFold’EM recovers the bound complex and epitope from only
1,000 particles—0.26% of those used for the deposited reconstruction—with RMSD 2.49Å , TM-score 0.956, and FSC
resolution3.52Å (deposited map:2.6Å).
Improved experimental guidance.Existing approaches condition AlphaFold on experimental data either
by optimizing its terminal embedding before sampling (Maddipatla et al., 2026a; Li et al., 2026), or by
directly guiding the diffusion trajectory in coordinate space (Maddipatla et al., 2025; 2026b; Raghu et al.,
2026). Fold’EM instead optimizes intermediate representations within the Pairformer module. Passing
experimental updates through the remaining Pairformer blocks induces a sequence- and state-dependent
geometry in the terminal conditioning space, constraining perturbations through transformations learned by
the pretrained model. We find that this reparameterization substantially strengthens experimental guidance
(Figure 3) and is a key enabling component of direct particle-level structure inference.
Low-sample structure inference.We first evaluate Fold’EM in the known-pose setting, where it recovers
accurate atomic structures on both experimental (Figure 4; Tables A3– A4) and synthetic (Tables A5–A6)
datasets using fewer than 1% of the particles used for conventional density reconstruction. Structures inferred
directly from particle images reach comparable structural resolution to those obtained through density
reconstruction, and on experimental homogeneous data from EMPIAR, as few as 0.1% of the particles are
sufficient to reach comparable Fourier shell correlation (FSC) and atomic RMSD. Heterogeneous results
are shown in Figures 6 and 5, Tables A15–A16 and A19–A20. In continuously heterogeneous systems, we
further find that the organization of conformational states in particle space is reflected in the AlphaFold
embedding space, indicating that experimentally observed conformational structure is preserved within the
learned representation and allowing a continuous trajectory to be represented by a small number of optimized
anchor states (Figure 8).
3

Ab initioFold’EM.We further proposeab initioFold’EM, a framework for structure determination from
cryo-EM particles with unknown poses and conformational states. The problem is formulated as a joint
inference of the atomic structures, particle poses, and class assignments under the particle-level likelihood and
sequence-conditioned structural prior. We solve this as a joint optimization problem by alternating between
two stages: (i)structure inference given the current poses and class assignments, which uses particle-level
guidance to optimize the atomic structures; (ii)pose and class inference given the inferred structures, which
refines each particle’s pose and class assignment under the current structural ensemble. For low-sample
heterogeneous data, we further introduce a RECOV AR-inspired residual-subspace estimator, B-RECOV AR,
that provides more robust particle assignments and confidence estimates, which are used to prioritize reliable
assignments during heterogeneous structure inference (Figure 7, and Table A26). In experimental datasets
with unknown poses,ab initioFold’EM reaches comparable structural accuracy using approximately 3%
of the particles used in the deposited reconstruction (Figure 4, Tables A9–A10). In heterogeneous data, it
resolves distinct conformational states using approximately 5% of the particles (experimental: Figure 6,
Tables A17–A18; synthetic: Tables A21–A22).
Together, these results show that strong structural priors can substantially reduce the particle counts
needed for atomic and conformational inference and suggest a route toward characterizing low-population
states directly from cryo-EM particle images.
2 Problem formulation
Notation.Let a denote the molecular sequence specification supplied to AlphaFold3 and X=
{x1,...,x m} the resulting 3D structure, where xi∈R 3 is the Cartesian coordinate of atom i. We view
AlphaFold3 as a sequence-conditioned latent model whose structure prediction comprises two stages. The
Pairformer first maps the sequence information to a latent representation Z=f(a) , which then conditions a
diffusion generator producing atomic coordinatesX∼p(X|Z).
The Pairformer consists of N blocks, f=f N◦···◦f 1, acting on single and pair representations
s∈R |a|×cs and z∈R |a|×|a|×cz that together form the latent state Z= (s,z) . We split the Pairformer trunk
at depthN−ℓ asf=g◦h , where h=f N−ℓ◦···◦f 1 produces an intermediate state H=h(a) , and
g=f N◦···◦f N−ℓ+1 denotes the finalℓ blocks, so that Z=g(H) . Since every Pairformer block preserves
the tensor shapes of the single and pair representations, H and Z belong to the same representation space.
We useℓ= 3throughout.
Inference objective.Let Y={y k}K
k=1 denote a set ofK raw cryo-EM particle images. Our goal is to
infer an ensemble ofn structures X={X 1,...,X n} that explains the observed particles while remaining
faithful to the AlphaFold3 prior. We parameterize these structures through a corresponding set of intermediate
Pairformer states H={H j}n
j=1, Z=g(H) , and optimize H directly at inference time. Each particle is
associated with nuisance variablesηk = (ϕk,ck,...) , whereϕk denotes its pose andck∈{1,...,n} the
structural class from which it originates. The nuisance variables may also include additional per-particle or
shared acquisition parameters entering the image-formation model, such as the contrast transfer function
(CTF) or other imaging parameters. We denote the complete set of nuisance variables byη={η k}K
k=1. In
this work we assume all imaging parameters other than pose and class to be known, suppress them from
the notation, and therefore infer onlyϕk andck. Conditioned on the structures and nuisance variables, and
assuming particles are independent,
p(Y|X,η) =
KY
k=1
p(yk|X ck,ϕk),
4

where Xck denotes the conformation corresponding to class labelck. This can be generalized to continuous
heterogeneity. In this case,ck becomes a vector of barycentric coordinates and the conformation is decoded
from the interpolated state H(ck) =P
jcj
kHj. We relax the deterministic Pairformer state H0 =h(a) into
a separable prior p(H|a) = Qn
j=1N(Hj;H 0,σ 2I). Treating the nuisance variables as unknowns, our
inference problem can then be written as joint MAP estimation of the marginal objective
J(H,η) = logE X∼p(X|g(H))p(Y|X,η) + logp(H|a) + logp(η),(1)
where p(X|g(H)) = Qn
j=1p(Xj |g(H j)). The term p(η) can encode priors over particle orienta-
tions, translations, and class frequencies; in the absence of additional information these may be taken as
uninformative.
The stochastic AlphaFold generator makes direct optimization of Equation 1 inconvenient. Applying
Jensen’s inequality,logEp≥Elogp, gives the tractable ELBO-like surrogate
(H∗,η∗) = arg max
H,η

EX∼p(X|g(H)) logp(Y|X,η) + logp(H|a) + logp(η)

.(2)
Optimizing H induces a learned geometry in Z.Optimizing the intermediate Pairformer state H
constrains the optimization to representations of the form Z=g(H) , but more importantly, it changes the
local geometry of optimization in conditioning space. Consider a single ensemble member Z=g(H) , let
J(H) =∂Z/∂H be its Jacobian, and let L(Z) =E X∼p(X|Z) logp(Y|X,η) denote the experimental
data term in Equation 2. By the chain rule, ∇HL=J ⊤∇ZL. Consequently, a gradient-ascent step
∆H=γJ ⊤∇ZLinduces, to first order,
∆Z=g(H+ ∆H)−g(H)≈γJJ ⊤∇ZL.
Thus, Euclidean optimization in H corresponds locally to preconditioned optimization in Z, with positive-
semidefinite preconditioner JJ⊤. Directions in conditioning space to which the final Pairformer blocks
are highly sensitive are amplified, whereas directions to which they are insensitive are suppressed. The
resulting local geometry is learned by the Pairformer itself and depends on both the sequence and the current
representation.
The same interpretation applies to the prior. We place an isotropic Gaussian anchor on the precursor
representation,p(H|a) =N(H 0,σ 2I), where H0 =h(a) . Let J0 =J(H 0) and Z0 =g(H 0). Linearizing
g around H0 gives approximately p(Z|a) =N(Z 0,σ 2J0J⊤
0 ). Hence, an isotropic relaxation of the
precursor state becomes a sequence-dependent anisotropic relaxation of the terminal Pairformer representation.
In contrast, treating Z as a free optimization variable with an isotropic prior assumes the same local geometry
in every direction of the conditioning space.
Intuitively, perturbations of H are filtered through the final Pairformer blocks before they affect the
structure generator. They are therefore expressed through transformations that the trained trunk itself has
learned to realize, rather than as arbitrary perturbations of its terminal representation. Figure 3 and Section 4.2
empirically demonstrate this.
Advantages of particle-domain fitting.Our formulation operates directly on particle-level likelihoods
rather than first averaging the particles into a reconstructed density. This distinction has two consequences.
First, when the imaging operators are known, particle-level fitting is equivalent to density fitting only under
an experiment-specific metric determined by the imaging operators and noise covariance. Second, when
poses are uncertain, the particles generally cannot be reduced to a single sufficient density statistic.
Consider the linearized image formation model yk =A kρ+ε k, εk ∼ N(0,Σk), where Ak are
known operators encapsulating the pose, CTF, and the sampling of a particlek, andρ is the underlying 3D
5

density. When all imaging operators Ak are known exactly, no information is lost by first reconstructing
a density—provided that the subsequent structure fit uses the correct experiment-induced metric. Indeed,
defining Q=
X
k
A∗
kΣ−1
k Ak, q=
X
k
A∗
kΣ−1
k yk, and letting ˜ρ=Q†q denote the reconstructed density,
the particle-level data term satisfies
1
2
X
k
∥yk−Akρ(H)∥2
Σ−1
k
= 1
2∥ρ(H)−˜ρ∥2
Q + const,
whereρ(H) is the density generated by the structural latent H being solved for. Thus, with known poses,
fitting a structural model directly to all particle likelihoods is equivalent to first reconstructing a density and
fitting to that density, but only when the latter uses the experiment-induced metricQ.
Importantly, the correct metric is generally not the ordinary density-spaceL2 norm. Even for equal white
noise and uniformly distributed viewing directions, the idealized normal operator is isotropic but frequency
dependent, satisfying cQρ(ξ)∝∥ξ∥ −1ˆρ(ξ)in the Fourier domain, with∥ξ∥ denoting radial spatial frequency,
or equivalently Q∝(−∆) −1/2, with ∆ denoting the Laplacian, very far from Q=I . Consequently,
guidance against a reconstructed density using a Euclidean map loss, as done in recent works (Maddipatla
et al., 2026b; Raghu et al., 2026),does notin general reproduce the original particle likelihood, even when the
poses are known; equivalence requires the density-space loss to incorporate the experiment-specific metric Q.
Particle averaging under uncertainty.The distinction becomes more fundamental when poses or classes
are uncertain. In this case the imaging operators themselves depend on latent variables, Ak =A(ϕ k), and
inference depends on the individual residualsyk−A(ϕk)ρ(H). Collapsing the particles into a single density
at nominal or estimated poses generally destroys information required to update the ϕk. A simple scalar
analogue illustrates this. Ifyk =ϕ kρ+ε k, withϕk∼N(1,τ 2) andεk∼N(0,σ 2), then after marginalizing
the uncertain pose one obtains yk|ρ∼N(ρ,σ 2 +τ 2ρ2). The likelihood therefore depends not only onP
kyk but also onP
ky2
k; the sample mean retains the former but not the latter and is therefore not a sufficient
statistic.
Particle-level inference therefore has two advantages in our setting. With known poses, it preserves
the statistically correct image-space metric without requiring it to be approximated in density space. With
uncertain poses or class assignments, it additionally retains particle-specific information that can be lost
when the observations are first collapsed into a reconstructed map. This motivates structure inference directly
against the individual particle likelihoods while refining nuisance variables, rather than reconstructing an
intermediate density and guiding the structural model against that density.

## Methods

Fold’EM jointly infers an ensemble of atomic structures and particle-specific nuisance variables directly from
raw cryo-EM particle images. Each ensemble member is represented by an intermediate Pairformer state
that conditions the AlphaFold3 diffusion model, and the nuisance variables of a particle are its pose and, in a
heterogeneous sample, its discrete class. Fold’EM first places the particles in a common reference frame
and, for heterogeneous data, assigns initial classes; it then alternates between updating the structural states
given the particle images and refining the nuisance variables under the current ensemble. Reconstructed
volumes, when used, serve only for initialization and class-specific frame alignment; structural guidance itself
operates on individual particles. In what follows, we describe the ingredients of this solver of Equation 2,
schematically depicted in Figure 1 and summarized in Algorithm 1.
6

3.1 Inputs, initialization, and reference frame
Inputs.The inputs to Fold’EM are a collection of particle images and the molecular sequence specification
a of the target. We assume knowledge of the pixel/box size and CTF parameters from preprocessing;
additionally, the particles are assumed to be centered. The sequence is the only structural input. AlphaFold3
constructs its MSA and unguided prediction from it, and no deposited atomic model or high-resolution
experimental reconstruction is supplied. For heterogeneous data the number of classes n is specified; for
homogeneous data, n= 1 . Poses and class labels are provided only in theknown-poseandknown-class
evaluations, in which the poses are those of the deposited consensus refinement.
Pose estimation.In theab initiosetting, poses are estimated in three stages: (i) VDAM, a variable-metric
gradient descent algorithm with adaptive moments estimation (Kimanius et al., 2021), jointly estimates a
coarse volume and particle poses from random initialization by marginalizing over poses; (ii) a consensus
density is reconstructed from these poses by Wiener back-projection; and (iii) an AlphaFold3 prediction
is docked into this density by L1 map guidance to define a structural reference frame. Since the cryo-
EM likelihood is invariant to a global rigid transformation of the structure and the corresponding inverse
transformation of the poses, the solution is defined only up to a global SE(3) transformation. We fix this
gauge by expressing all particle poses relative to the docked structure before particle classification and
structural inference.
Particle embedding and classification.When class labels are unknown, we infer them directly from the
particle images, without state-specific reference structures or atomic models. We consider cryoDRGN (Zhong
et al., 2021), which embeds particles using a learned latent representation, and RECOV AR (Gilles and Singer,
2025), which embeds them by projection onto principal components of the estimated volume covariance.
In the low-particle regime, however, experimental nuisance variation can be comparable to the structural
differences of interest, and we find that these embeddings do not reliably separate classes.
We therefore introduce B-RECOV AR, a bootstrapped residual-subspace estimator inspired by RECOV AR.
For the two-state case, it (i) fits class-deviation volumes to residuals from a consensus reconstruction,
pooled through the current poses and restricted by a solvent mask; (ii) refines assignments by cross-validated
comparison against per-class reconstructions; and (iii) combines the assignments from randomized subsamples
and frequency bands using a label-free spectral meta-learner (Parisi et al., 2014). For more than two states,
successive modes are extracted by deflation; for continuous heterogeneity, the same modes are interpreted as
variability directions. The ensemble vote margin defines a per-particle confidence score, which is used to
prioritize reliable assignments during structural inference.
After classification, we reconstruct one auxiliary consensus volume per class, used only to establish
its reference frame. We dock the reference structure into each volume as in the pose-estimation stage and
re-synchronize particle poses to the corresponding class reference. The resulting classified particles, reference
ensemble, and poses are then passed to structural inference. The full procedure is given in Algorithm 2 and
Appendix D.4, which also details its relation to RECOV AR.
3.2 Ensemble inference
The inputs to structure inference are the particles, the reference structure, and the poses expressed with
respect to it; for a heterogeneous sample, they are the classified particles, the ensemble of references, and the
poses re-synchronized to their classes. Equation 2 couples the structural states H with the particle-specific
nuisance variablesη, and we approximately optimize the two blocks by alternating coordinate ascent. Given
the current nuisance estimates, we infer structures by an IT-Opt-style update (Maddipatla et al., 2026a); given
7

the resulting structures, we refine the nuisance variables. Depending on the evaluation setting, known poses
or classes are held fixed rather than updated. The full procedure is summarized in Algorithm 1.
Step 1: structure inference given nuisance variables.At outer iteration r, we hold the current nuisance
estimatesη (r) ={(ϕ (r)
k ,c (r)
k )}K
k=1 fixed and update the structural latent variables as
H(r+1)≈arg max
H
h
EX∼p(X|g(H)) logp(Y|X,η (r)) + logp(H|a)
i
.(3)
For fixed nuisance variables, the likelihood factorizes over particles as
logp(Y|X,η (r)) =
KX
k=1
logp(yk|X c(r)
k ,ϕ (r)
k ).
Hence each ensemble member is guided by the particles currently assigned to it, projected according to their
current pose estimates. The implemented particle likelihood and image formation model are described in
Appendix D.3.
We solve Equation 3 by an IT-Opt-style inference-time update (Maddipatla et al., 2026a) that back-
propagates likelihood gradients into AlphaFold3 latents, but optimize the intermediate state H rather than
the terminal Pairformer representation. AlphaFold3 (Abramson et al., 2024) is a diffusion-based generative
model (Ho et al., 2020; Karras et al., 2022). LetRθ denote one step of its pretrained reverse diffusion process,
Xt−1 =R θ(Xt;g(H),t,n t),n t∼N(0,I),(4)
and let Dθ denote its current denoised structure estimate. Integrating the reverse process from XT ∼
N(0,σ 2
TI)tot= 0generates a structure conditioned ong(H).
For each structural update we perform Q independent reverse-diffusion runs, retaining the optimized
H between runs. At run q, we initialize each ensemble member independently as Xq,j
T ∼N(0,σ 2
TI) for
j= 1,...,n . Resampling the diffusion noise while retaining the optimized Pairformer states encourages H
to explain the experimental observations across different stochastic realizations of the AlphaFold generator.
At every reverse-diffusion stept, the current denoised structures are used to update the Pairformer states
by gradient ascent,
Hq
t−1 =H q
t +γh∇Hq
t
h
logp

Y|D θ(Xq
t ;g(Hq
t ),t),η (r)

+λp logp(Hq
t|a)
i
,(5)
whereγh denotes the step size. The updated latent states are then used to condition the next reverse-diffusion
step. For ensemble memberj, this amounts to conditioningRθ in Equation 4 ong(Hq,j
t−1). At the end of each
reverse process, Hq
0 initializes the next run. Thus, H acts as persistent memory across stochastic diffusion
samples, progressively biasing the AlphaFold generator toward structures supported by the experimental
particles. After the final run,g(H (r+1))is decoded to obtain the updated structural ensembleX (r+1).
Step 2: nuisance inference given structure.We next hold the structural ensemble X (r+1) fixed and update
the nuisance variables as
η(r+1) = arg max
η
h
logp(Y|X (r+1),η) + logp(η)
i
.(6)
In this work, the unknown nuisance variables are particle pose and structural class. Assuming their priors
factorize across particles, the update can be performed independently for each particle as
(ϕ(r+1)
k ,c (r+1)
k ) = arg max
ϕ,c
h
logp(yk|X c,(r+1),ϕ) + logp(ϕ,c)
i
.
8

Pose refinement therefore aligns each particle against the currently inferred structures, while class refinement
assigns it to the ensemble member that best explains its image. Poses remain expressed in the docked
reference frame, fixing the otherwise arbitrary globalSE(3)gauge.
The updated nuisance variables are then returned to Equation 3, and the two coordinate steps are alternated.
This coupling is particularly important in the low-signal regime. Inaccurate poses or class assignments can
produce misleading structural gradients, while an inaccurate structural model can in turn bias particle
alignment and classification.
If both coordinate steps were solved exactly for a deterministic objective, each iteration would be non-
decreasing in Equation 2 and convergence would yield a coordinate-wise stationary solution. In practice,
the structural step uses stochastic diffusion samples, minibatches of particles, and finite gradient updates,
so monotonic improvement is not guaranteed at every iteration. We therefore use the coordinate-ascent
interpretation primarily as the organizing principle for joint structure and nuisance inference.

## Experiments

We evaluate Fold’EM on synthetic particles rendered from deposited structures and on experimental particle
stacks from EMPIAR (Tables A2 and A1). Sections 4.1 and 4.2 test in isolation the two design choices of
Sections 2 and 3, namely guidance by the particles rather than by a reconstructed density, and optimization of
the intermediate Pairformer state rather than of the terminal embedding or the atomic coordinates. Sections 4.3
and 4.4 evaluate structure determination for homogeneous samples and for two-state mixtures, in each case
first with known poses, which tests structure inference alone, and thenab initio, with poses and classes
inferred from the particles as described in Section 3.1. In the known-pose setting the poses are those used
to render the synthetic particles or, for experimental data, those of the deposited consensus refinement.
Section 4.5 evaluates the label-free class assignment by B-RECOV AR that initializes the heterogeneous
experiments, and Section 4.6 treats continuous heterogeneity. Unless stated otherwise, we report the C α
RMSD and TM-score against the deposited model, and the resolution at which the Fourier shell correlation
(FSC) against the deposited map crosses0.143 (Appendix D.2.4); for synthetic data the deposited model is the
ground truth from which the particles were rendered. The density-based baselines are RELION (Zivanov et al.,
2018) and cryoDRGN (Zhong et al., 2021) with known poses, and RELIONab initioand cryoDRGN-AI
(Levy et al., 2025) without them (Appendix D.2). We also report the unguided AlphaFold3 prediction, which
represents the structure obtained without experimental conditioning and serves as a control for its effect.
4.1 Particle guidance vs. density guidance
Experimental setup.We first ask whether guidance by the individual particles recovers more of the
structure than guidance by the density reconstructed from them, at equal particle count. To evaluate this,
we take the synthetic 8U4E assembly, the largest target in Table A2 (3,304 residues), and performab initio
inference from 500 particles at SNR 0.005. A consensus density is reconstructed from these particles at the
estimated poses. Density guidance, the baseline, optimizes the same Pairformer state with the same particles,
poses and optimizer as Fold’EM, but replaces the particle likelihood by a loss against this consensus density.
The two settings therefore differ only in the data term.
Results.At equal particle count, particle guidance recovers the assembly and density guidance does not.
The unguided AlphaFold3 prediction misplaces the domains of8U4E (Cα RMSD 22.99Å ). Density guidance
reduces this only to 17.95Å , whereas Fold’EM, guided by the same particles while refining their poses,
reaches 6.88Å with TM-score 0.809 (Table A12) and is the only one whose domains follow the envelope
of the density (Figure 2). As argued in Section 2, a density loss reproduces the particle likelihood only for
9

A. 8U4E B. AlphaFold3
22.99 Å
C. ESP guidance ab-initio
17.95 Å
D. Fold'EM ab-initio
6.88 Å
Figure 2: Guiding with the particles recovers the structure, whereas guiding with their reconstructed ESP
fails.Ab initioinference on synthetic 8U4E (3,304 residues) from 500 particles at SNR 0.005. The grey surface is
the consensus density reconstructed from these particles at the estimated poses, and the numbers are C α RMSD to
the deposited model. (A) The deposited model. (B) AlphaFold3 misplaces the domains of the assembly. (C) ESP
guidance optimizes the same Pairformer state with the same particles, poses and optimizer, but replaces the particle
likelihood by a loss against the consensus density, and improves the prediction without recovering the arrangement.
(D) Fold’EM, guided by the particle likelihood, recovers it, with a TM-score of 0.81 against 0.48 for AlphaFold3. As
argued in Section 2, a density loss reproduces the particle likelihood only under the experiment-induced metric, and
with estimated poses the consensus density is not a sufficient statistic for the particles, so the information needed to
refine the poses together with the istructure is lost.
100
101
RMSD (Å) ( ↓ )
8U4B
RMSD
0.00
0.25
0.50
0.75
1.00
TM-score ( ↑ )
TM-Score
0
10
20
30
FSC 0.143 (Å) ( ↓ )
FSC 0.143
250 1000
# Particles
100
101
RMSD (Å) ( ↓ )
9UGB
250 1000
# Particles
0.00
0.25
0.50
0.75
1.00
TM-score ( ↑ )
250 1000
# Particles
0.0
2.5
5.0
7.5
10.0
FSC 0.143 (Å) ( ↓ )
AlphaFold3 Fold'EM IT-Opt Guidance Deposited
Figure 3: Optimizing the intermediate Pairformer state improves particle-level guidance.We compare three
ways of steering AlphaFold3 with the same particle likelihood, poses and particle subsets: Fold’EM, which optimizes
the intermediate Pairformer state H and passes the updates through the finalℓ Pairformer blocks (Section 2); IT-Opt
(Maddipatla et al., 2026a), which optimizes the terminal embedding Z directly under an isotropic prior; and coordinate-
space guidance of the reverse diffusion process (Maddipatla et al., 2026b).Rows:synthetic 8U4B and 9UGB from
Table A2 at SNR 0.005 with known poses, using 250 and 1000 particles.Columns:C α-RMSD (↓, log scale) and
TM-score (↑) against the deposited PDB model; the dashed line marks the AlphaFold3 prediction. On both targets
Fold’EM improves substantially over both alternatives and reaches near-atomic agreement with the deposited model;
the learned geometry induced by optimizing H thus keeps particle-level guidance stable at low SNR and on large
assemblies.
10

known poses and under the experiment-induced metric Q, and with estimated poses the consensus density is
not a sufficient statistic for the particles. At 500 particles the density is coarse and formed at uncertain poses;
it serves to initialize the reference frame (Section 3.1) but cannot replace the particles as the data term.
4.2 OptimizingHvs.Zvs. coordinate-space guidance
Experimental setup.We next ask whether optimizing the intermediate Pairformer state H gives stronger
particle guidance than optimizing the terminal embedding Z or guiding the atomic coordinates directly. To
evaluate this, we take synthetic 9UGB and 8U4B at SNR 0.005 with 250 or 1,000 particles and known poses,
so that differences reflect the guidance mechanism rather than pose estimation. We compare Fold’EM with
IT-Opt (Maddipatla et al., 2026a), which optimizes Z under an isotropic prior (see also Li et al., 2026),
and with coordinate-space guidance of the reverse diffusion process (Maddipatla et al., 2026b). The three
schemes use the same particle likelihood, poses and particle subsets, and differ only in the variable that the
likelihood gradient updates.
Results.Optimizing H gives the strongest guidance of the three. All three schemes correct the AlphaFold3
prediction of 9UGB, and Fold’EM attains the lowest Cα RMSD, highest TM-score and finest FSC resolution.
On the larger 8U4B assembly, Fold’EM recovers the deposited structure, whereas IT-Opt and coordinate-
space guidance degrade the initial prediction (Figure 3). As argued in Section 2, the update of Equation 5 is
locally a gradient ascent in Z preconditioned by JJ⊤, under a sequence-dependent anisotropic prior on Z.
The separation is largest on the larger assembly, where unfiltered updates of Z or of the coordinates carry the
prediction away from the deposited model.
4.3 Guidance on homogeneous samples
Experimental setup.Having fixed the guidance mechanism, we ask how few particles suffice to determine
the structure of a single conformational state, first with known poses and thenab initio. To evaluate this,
we take the synthetic targets 9UGB, 9UGC, 8U4B and 8U4E (Table A2), rendered at SNR 0.01 and 0.005,
with 100 to 1,000 particles and known poses, or 500 particlesab initio. We further take the five experimental
datasets of Table A1, namely integrinα5β1 bound to the BIIG2 Fab (9B9J), 9B77, 8PWH, and the two UvrA
states 9GXQ and 9GXR, each with its own deposited particle set. With known poses we use between 1/1000
and 1/50 of the deposited particles;ab initiowe use 1,000 particles for 9B9J and 9B77 and 5,000 for the
remaining three. The baselines reconstruct a density from the same particles. For the baselines the FSC is
computed from the reconstructed map, and for Fold’EM from the map rendered from its atomic model; the
deposited model is reported for reference.
Results.On the synthetic targets, 100 particles with known poses suffice. AlphaFold3 mispredicts the
Pma1 conformation 9UGB (TM-score 0.699, Cα RMSD 8.96Å ; Figure 4A). From 100 particles at SNR
0.005, Fold’EM reaches 3.25Å FSC resolution, TM-score 0.965 and Cα RMSD 1.01Å , comparable to the
deposited model (3.39Å ; Tables A5 and A6), and 3.45, 3.80 and 4.18Å on 9UGC, 8U4B and 8U4E, with
TM-scores 0.983, 0.979 and 0.973. cryoDRGN remains coarser than 5.8Å on the two larger targets at every
particle count, and RELION coarser than 5Å on every target. Increasing the particle count to 1,000 alters the
Fold’EM results little, consistent with the prior supplying most of the molecular detail while the particles
select the realized conformation.Ab initio, 500 particles give comparable accuracy on 9UGB, 3.25Å at SNR
0.005 with TM-score 0.976 and Cα RMSD 1.57Å , against 8.93 and 27.70Å for RELIONab initioand
cryoDRGN-AI (Tables A11 and A12). 8U4B and 8U4E are resolved less wellab initio( 5.87 and 11.38Å at
SNR0.01), although Fold’EM still raises their TM-scores from0.798and0.477to0.917and0.810.
11

3
5
10
20
30FSC 0.143 (Å)
Fold'EM
cryoDRGN
RELION known poses
ab initioAlphaFold3
100 250 500 1000
# particles
0.8
0.9
1.0TM-Score
AlphaFold3 Fold'EM
known poses
500 particles
Fold'EM
ab initio
1000 particlesPDB 9UGB
(synthetic)
AlphaFold3 Fold'EM
known poses
500 particles
Fold'EM
ab initio
1000 particlesPDB 9B9J
EMPIAR 12552
3
5
10
20
40FSC 0.143 (Å)
1 10 100 400 800 1500 3600
# particles
0.8
0.9
1.0TM-Score
10−5 10−4 10−3 10−2
fraction of dataset
PDB: 2.6Å
A B
C D
E F
G H
Figure 4: Fold’EM recovers atomic structures from 0.03% of the deposited particles with known poses and from
0.27% ab initio.Each column is one target: a synthetic dataset on the left (A, C, E, G) and an experimental one on the
right (B, D, F, H). Rows show the structures (A, B; AlphaFold3 in blue, Fold’EM in red, deposited model in grey),
representative particles (C, D), FSC resolution (E, F) and TM-score against the deposited model (G, H) as a function of
the number of particles; filled markers denote known poses, open markersab initio, and the dotted line the AlphaFold3
prediction.Left:Pma1, the yeast plasma-membrane H +-ATPase, in its activated (E2P) state (9UGB); synthetic particles
at SNR 0.005. AlphaFold3 predicts the transmembrane domain but misplaces the cytosolic A-, N- and P-domains,
whose arrangement changes along the catalytic cycle (TM-score 0.70). Fold’EM recovers the deposited state, reaching
3.3Å and a TM-score of 0.97 from 100 particles with known poses, and 3.3Å from 500 particlesab initio.Right:
Integrinα5β1–BIIG2 (9B9J, EMPIAR-12552), where AlphaFold3 predicts both component folds but places the Fab
at the wrong site (TM-score 0.78); antibody–antigen pairs provide little paired coevolutionary information. Fold’EM
recovers the bound complex and epitope, although not the interface variable loops, reaching 3.5Å and a TM-score
of 0.97 from 100 particles with known poses and 3.5Å from 1,000 particlesab initio; no baseline reaches 6Å , and
Fold’EM improves over AlphaFold3 even at the smallest particle counts. Sparse particle evidence therefore corrects the
global arrangement largely supplied by the structural prior. Resolution (Å; FSC= 0.143).
12

On experimental data, a few hundred particles suffice when the component folds are already present in
the unguided prediction. AlphaFold3 predicts the integrin and Fab components of 9B9J individually but
places the Fab at the wrong site, illustrating the difficulty of antibody–antigen interfaces, for which paired
coevolutionary information is limited (Figure 4B). Fold’EM identifies the correct epitope from 400 particles
with poses estimatedab initio, compared with 374,814 particles used in the deposited reconstruction. With
fewer than 1,500 particles it reaches a resolution finer than3.5Å in both the known-pose andab initiosettings
(Figure 4F), and it exceeds a TM-score of 0.9 from 400 particles (Figure 4H), while no baseline reaches 6Å
on this target. The particles thus correct the relative arrangement of the predicted components and reveal
the epitope, although the interface variable loops of BIIG2 are not recovered with atomic accuracy. With
1/1000 of the deposited particles and known poses, Fold’EM reaches 2.88, 3.08 and 3.18Å on 9B77, 9GXQ
and 9GXR (Table A3). 8PWH is the one exception. Fold’EM raises the TM-score of the unguided prediction
from 0.397 to 0.900 (Table A4), but from 1/100 of the particles onward cryoDRGN attains a finer FSC
resolution (5.16 and 5.01Å against 7.06 and 6.13Å ), as does RELIONab initiofrom 5,000 particles (9.84
against 10.83Å ; Table A9). When the unguided prediction departs this far from the deposited model, density
reconstruction attains the finer resolution once roughly7,000particles are available.
4.4 Guidance under two-state heterogeneity
Experimental setup.We then ask whether two conformational states can be resolved from a single mixed
particle stack, first with known poses and then with poses and class labels inferred from the particles. To
evaluate this, we take a synthetic mixture of the activated (9UGB) and autoinhibited (9UGC) states of Pma1,
about 9Å apart in Cα RMSD, rendered in equal proportion at SNR0.01 and 0.005 with 250 to 1,000 particles
per state. We further take the experimental mixture EMPIAR-13396, which contains two states of UvrA
bound to DNA carrying an abasic site (9GXQ and 9GXR), and draw balanced stacks of500 to 10,000 particles
per state. In theab initiosetting, B-RECOV AR initializes the class labels (Section 4.5), and Fold’EM then
alternates structure, pose and class refinement, guiding each ensemble member with the more confident half
of the particles assigned to it (Section 3). The baselines first cluster the particles and then reconstruct one
density per class from its assigned subset (Appendix D.2), using RELION and cryoDRGN with known poses
and RELIONab initioand cryoDRGN-AI otherwise.
Results.On the synthetic mixture, a few hundred particles per state suffice to resolve both states. Al-
phaFold3 recovers neither (TM-score 0.699 and 0.661; Figure 5). With known poses, Fold’EM resolves both
from 250 particles per state at SNR 0.005, reaching 3.3 and 3.5Å with TM-scores 0.96 and 0.98 (Tables A19
and A20), whereas at the same noise level RELION remains coarser than 7.9Å and cryoDRGN requires
1,000 particles per state to reach 3.6 and 4.8Å .Ab initio, 500 particles per state give 3.4 and 3.6Å with
TM-scores 0.95 and 0.94 at SNR 0.005, within about 0.1Å of the known-pose results (Tables A21 and A22),
whereas RELIONab initioand cryoDRGN-AI remain coarser than 6.9 and 16.6Å , respectively, on either
state at every sample size. At 250 particles per state and SNR 0.005, 9UGB degrades to 7.6Å , which marks
the sample size at which the signal no longer suffices for the joint inference of pose, class and structure.
On UvrA, the particle count required to resolve a state depends on how closely the unguided prediction
already reproduces it. AlphaFold3 predicts 9GXR (3.54Å , TM-score 0.886) but not 9GXQ (11.69Å , TM-
score 0.734). With known poses, Fold’EM resolves both from 1,000 particles per state, reaching 3.09 and
2.95Å on 9GXQ and 9GXR, against 4.34 and 4.41Å for cryoDRGN and 6.89 and 10.75Å for RELION
(Table A15).Ab initio, Fold’EM reaches 3.58Å on 9GXR from 500 particles per state and 3.02Å from 5,000,
whereas 9GXQ is recovered from 10,000 particles per state, about 5% of its deposited stack, at 4.63Å and
TM-score 0.836 (Figure 6; Tables A17 and A18). RELIONab initioand cryoDRGN-AI remain coarser than
8Å on both states at every sample size. The larger particle count requiredab initiois therefore attributable to
9GXQ, the state absent from the unguided prediction.
13

A B C
D
E F
9UGB 9UGC
AlphaFold3
Fold'EM (known poses)
1K particles
Fold'EM ab initio
2K particles
250
500 1,000 # particles / conformation
2
3
5
10
20
40
FSC 0.143 (Å)
PDB: 3.12 Å
250
500 1,000 # particles / conformation
2
3
5
10
20
40
FSC 0.143 (Å)
PDB: 3.39 Å
250
500 1,000 # particles / conformation
0.8
0.9
1.0
TM-Score
250
500 1,000 # particles / conformation
0.6
0.7
0.8
0.9
1.0
TM-Score
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB
Figure 5: Fold’EM resolves both states of a synthetic 9UGB/9UGC mixture from 250 particles per state with
known poses, and from 500 ab initio.Pma1 is the plasma-membrane proton pump of yeast, a P-type ATPase whose
cytosolic A-, N- and P-domains rearrange along the catalytic cycle; 9UGB is the activated (E2P) state and 9UGC the
autoinhibited state. Particles are rendered from the two deposited conformations, approximately 9 Å apart in Cα RMSD,
and mixed in equal proportion at SNR0.005. In every panel, 9UGB is on the left and 9UGC on the right. (A) AlphaFold3
(blue) over the deposited models (grey) recovers neither state (TM-score 0.70 and 0.66): the transmembrane domain is
predicted correctly and the error is confined to the cytosolic domains, whose arrangement depends on the state of the
cycle. (B) Fold’EM (red) with known poses resolves both from the mixed stack of 1,000 particles (500 per state). (C)
Fold’EMab initioresolves both from 2,000 particles (1,000 per state). (D) Representative particles of each state. (E, F)
FSC resolution (top) and TM-score against the deposited model (bottom) as a function of the number of particles per
state, for 9UGB (E) and 9UGC (F); filled markers denote known poses and open markersab initio, the dashed grey line
is the resolution of the deposited model and the dotted blue line the AlphaFold3 prediction.
14

AlphaFold3 Fold'EM (known poses)
2K particles
Fold'EM ab initio
20K particles
AlphaFold3
0.25 0.5 1 2.5 5.0
fraction of dataset
PDB 9GXQ
EMPIAR 13396
PDB 9GXR
2
3
5
10
20
40FSC 0.143 (Å)
PDB: 2.64 Å
500 1,000 2,000 5,000 10,000
# particles / conformation
0.7
0.8
0.9TM-Score
500 1,000 2,000 5,000 10,000
# particles / conformation
PDB: 2.89 Å
0.25 0.5 1 2.5 5.0
Abasic
site
Distorted
dsDNA
Canonical
dsDNA
Fold'EM
cryoDRGN
RELION
known poses
ab initio
AlphaFold3
PDB structure
AlphaFold3
Fold’EM
PDB 9GXQ fraction of datasetPDB 9GXR
A B C
D
E
F
G
Figure 6: Fold’EM resolves both UvrA–DNA conformations from 0.5% of the deposited particles with known
poses and from 5% ab initio.EMPIAR-13396 contains two states of UvrA bound to DNA carrying an abasic site (PDB
9GXQ/9GXR); damage recognition involves insertion of the Y62/Q65/F66 wedge into the duplex. (A) AlphaFold3
recovers 9GXR but not 9GXQ (TM-score 0.734). (B,C) Fold’EM resolves both states from 1,000 particles per state with
known poses and from 10,000 particles per stateab initio(left: 9GXQ, right: 9GXR). (D) Representative particles. (E)
FSC versus particles per state (filled: known poses; open:ab initio). With known poses Fold’EM reaches3.1/3.0Å from
1,000 particles per state;ab initioit reaches 3.0Å on 9GXR and 4.6Å on 9GXQ, while RELION and cryoDRGN-AI
remain above8Å. (F) TM-score against the deposited models. (G) AlphaFold3 retains a fully paired duplex, whereas
Fold’EM recovers the wedge insertion and disrupted DNA, but not the flipped-out nucleotide, as expected because the
lesion was supplied to both models as intact DNA. Resolution (Å; FSC= 0.143).
15

250 500 1000 2500 5000
particles / state
50
60
70
80
90
100accuracy (%)
B-RECOVAR RECOVAR cryoDRGN
A
0.0–0.2 0.2–0.4 0.4–0.6 0.6–0.8 0.8–1.0
confidence
40
50
60
70
80
90
100accuracy (%)
55
12%
50
13%
51
16%
63
15%
80
44% B
rank-1 PCA + solvent mask + cross-half ensemble
50
60
70
80
90accuracy (%)
63.8
d′ 0.54
69.1
d′ 0.81
72.1
d′ 1.13
80.6
d′ 2.33 C
−3 −2 −1 0 1 2 3
d′ = 0.54
rank-1 PCA
9GXQ
9GXR
−3 −2 −1 0 1 2 3
d′ = 0.81
+ solvent mask
−3 −2 −1 0 1 2 3
d′ = 1.13
+ cross-half
−3 −2 −1 0 1 2 3
d′ = 2.33
ensemble
D
Figure 7: B-RECOV AR assigns particles to conformational states more accurately and more reliably than
RECOV AR and cryoDRGN at low particle counts, and its confidence score orders the assignments by their
reliability.Label-free class assignment on the UvrA protein–DNA complex (EMPIAR-13396, 9GXQ vs. 9GXR), scored
against the deposited labels.(A)Accuracy as a function of the number of particles per state, from 250 to 5,000,
that is, 0.13–2.6% of the particles deposited for each state. Boxes summarize ten random draws per size, shared by
B-RECOV AR and RECOV AR; triangles mark cryoDRGN. The RECOV AR estimator is ill-conditioned at these sample
sizes and its accuracy ranges from chance to near-perfect between draws of the same size; B-RECOV AR trails it at
250 particles but is both more accurate and markedly more stable from 500 particles onward, and cryoDRGN remains
below B-RECOV AR throughout.(B)Accuracy of B-RECOV AR stratified by its confidence scoreκk, the normalized
margin of the ensemble vote (Appendix D.4). The percentage in each bar is the fraction of particles in that bin; the solid
line is the accuracy over all particles and the dashed line chance. Accuracy increases monotonically with confidence,
so the score ranks the particles by the reliability of their label; Fold’EM uses this ordering to guide each ensemble
member with the more confident half of its particles (Table A26).(C, D)Ablation of the estimator at 1000 particles per
state. The base estimator is a single rank-one fit to the consensus-subtracted residuals, a one-dimensional RECOV AR
fit without noise correction, and is improved in turn by restricting the mode to a solvent mask, by the cross-validated
refinement of the labels, and by ensembling replicates over particle subsamples, frequency bands and initializations.(C)
Accuracy of each stage, with error bars over repeated draws.(D)Distribution of the per-particle class score at each
stage for the particles of either state, with their separation d′, the difference of the two means in units of the pooled
standard deviation. Every step widens the separation between the states, and the ensemble accounts for the largest gain.
The recovered difference is functionally meaningful. UvrA recognizes damaged DNA by inserting the
Y62, Q65 and F66 wedge into the duplex. AlphaFold3 predicts a largely canonical duplex, whereas Fold’EM
recovers the wedge insertion and the associated distortion of the DNA (Figure 6G). It does not recover the
flipped-out abasic nucleotide, which was not represented as an abasic site in the input molecular specification.
4.5 Label-free class assignment with B-RECOV AR
Experimental setup.The heterogeneous experiments depend on the class labels that initialize them. We
therefore ask whether particles can be assigned to their states without reference structures, at particle counts
at which existing embeddings are unreliable. To evaluate this, we take the UvrA mixture of EMPIAR-13396
at 250 to 5,000 particles per state, between 0.13% and 2.6% of the particles deposited for each state, with
ten random draws per size and poses from the consensus refinement, and score the assignments against the
deposited labels. We compare B-RECOV AR (Section 3.1; Appendix D.4) with RECOV AR (Gilles and Singer,
16

2025), applied to the same draws with the same label-free protocol, and with cryoDRGN, reported as the
median over ten seeds. The ablation of B-RECOV AR is carried out at1,000particles per state.
Results.From 500 particles per state onward, B-RECOV AR assigns the particles more accurately and
far more consistently than either baseline (Figure 7A). At these sample sizes the leading direction of the
RECOV AR covariance depends as much on the particles drawn as on the structural difference between the
states, and across ten draws of the same size the accuracy of RECOV AR ranges from chance to near-perfect,
so that the median over draws does not represent any single draw. B-RECOV AR is less accurate at 250
particles per state, but at 5,000 it reaches 92.5% with a range across draws of under one percentage point,
and cryoDRGN remains below it at every sample size.
The normalized margin κk of the ensemble vote serves as a confidence score. Accuracy increases
monotonically with it, from near chance in the lowest bins to 80% in the highest, which contains 44%
of the particles (Figure 7B), so the score orders the labels by reliability although it is not a calibrated
probability. Fold’EM uses this ordering in the heterogeneous experiments of Section 4.4, and discarding
the less confident half of the particles assigned to each member increases the separation between the two
modelled conformations, measured by their Cα RMSD, and raises their TM-score against the deposited
models (Table A26). This is consistent with the least confident particles being the most likely to be mislabelled,
since mislabelled particles draw both members toward a common average rather than their respective states.
The ablation of Figures 7C and D isolates the contribution of each component of the estimator. The base
estimator, a rank-one fit to the consensus-subtracted residuals equivalent to a one-dimensional RECOV AR fit
without noise correction and without a solvent mask, reaches 63.8% accuracy with strongly overlapping class
scores (d′ = 0.54). Restricting the fitted mode to the interior of a solvent mask raises the accuracy to 69.1%,
and refining the labels by cross-validated comparison against per-class reconstructions raises it to 72.1%.
The largest gain comes from the ensemble over particle subsets, frequency bands and initializations, which
yields 80.6% and doubles the separation between the states, fromd′ = 1.13 tod′ = 2.33. The class direction
recurs across replicates, whereas the nuisance directions that compete with it at these particle counts do not,
and aggregation over replicates therefore separates the two states.
4.6 Guidance under continuous heterogeneity
Experimental setup.Finally, we ask whether a continuous conformational trajectory can be represented by
a small number of optimized Pairformer states and their interpolation. To evaluate this, we take the IgG-1D
dataset of CryoBench (Jeon et al., 2024), which consists of 100 ground-truth atomic models, generated
from PDB entry 1HZH by rotating one Fab domain about the hinge through a closed 360◦ trajectory, and
25,000 synthetic particles at SNR 0.01, 250 per state, with ground-truth poses and per-particle CTFs. We
embed each particle in three label-free conformational coordinates, namely the latent of a cryoDRGN V AE
trained on the stack, the leading principal components of RECOV AR, and the residual-subspace embedding
of B-RECOV AR (Appendix D.4). Each coordinate defines one arm of the experiment, and the arms differ
only in the coordinate used to select the particles of each state.
In each arm, we fix eightanchorconformations at equispaced positions along the ring and, for each
anchor, optimize one structure against the 250 particles nearest to it in the conformational coordinate of
that arm. This yields eight Pairformer states H1,...,H 8, optimized independently against disjoint particle
sets, with no term coupling them. An intermediate conformation at position α along the ring is obtained
as the convex combination H(α) =P
kck(α)Hk of the two neighbouring anchors, with piecewise-linear
coefficientsck. For each of the 100 ground-truth states we decode H(α) through a full reverse-diffusion
trajectory, with a brief coordinate-space refinement against the 250 particles that the same coordinate places
nearest to that state, and relax the result (Appendix D.2.3).
17

0°
90°
180°
270° Hinge
angle
Groundtruth B-RECOVAR + Fold’EM
250×100 particles
0° 36° 72° 108° 144° 180° 216° 252° 288° 324° 360°
0.10
0.15
0.20
Hinge angle
NCC
0.7
0.8
0.9
1.0
TM-score
cryoDRGN RECOVAR B-RECOVAR Ground truth
A C
D
B
Figure 8: Fold’EM resolves continuous heterogeneity of an IgG antibody complex.(A) Shown as ensembles are
10 of the 100 ground-truth CryoBench IgG-1D synthetic models, colored by hinge angle; and (B) the corresponding
structures recovered by Fold’EM with B-RECOV AR particle classification. The inset depicts the two leading principal
components of the optimized Pairformer states, overlaid on the B-RECOV AR embedding of the particles. (C) TM-score
and (D) Fourier NCC plotted as a function of hinge angle, for the three conformational coordinates.
cryoDRGN 
+ Fold’EM
Hinge 
angle
RECOVAR 
+ Fold’EM
B-RECOVAR 
+ Fold’EM
Figure 9: Optimized Pairformer states preserve the hinge-angle ordering for all three conformational coordinates.
We show the geometry and the generated structures for each of the three particle classifiers: cryoDRGN, RECOV AR
and B-RECOV AR. Left of each panel: the two leading principal components of the optimized Pairformer states, with
the eight anchors as large dots and the interpolated states as small dots, overlaid on the per-particle coordinates of the
corresponding method mapped into the same plane; all are coloured by the hinge angle of the state they represent, as
indicated by the colour wheel. Right of each panel: a subset of 10 structures decoded from the interpolated states,
superimposed on the fixed body of the antibody and coloured by hinge angle (top), and in white to show the sweep of
the moving Fab about the hinge (bottom). In all three cases the anchors, ordered by hinge angle, form a simple closed
ring in the representation and the decoded structures trace the full rotation of the Fab.
18

The comparison is among the three coordinates, and between the interpolated structures and the anchors,
rather than against a density-based baseline. Each structure is scored by the TM-score against the ground-truth
model of its state and by the Fourier NCC between the rendered structure and the particles of that state,
expressed as a fraction of the NCC of the ground-truth model against the same particles.
Results.Eight anchors suffice to represent the trajectory. Over the full ring, the 100 structures of the
B-RECOV AR arm, all decoded from interpolated states, attain a median NCC of92% of the ground-truth
value and a median TM-score of 0.93, comparable to the eight anchors themselves ( 89% and 0.91). The
cryoDRGN coordinate reaches 85% and 0.89, and the RECOV AR coordinate90% and 0.92 (Figure 8). The
leading principal components of the optimized Pairformer states preserve the ordering in hinge angle for all
three coordinates (Figure 9), although the anchors are optimized independently and nothing in the objective
couples them. Table A25 reports the stereochemical quality of the anchors and of the interpolated structures.
The conformational organization of the particles is therefore mirrored in the AlphaFold representation, and a
continuous trajectory can be represented by a small number of experimentally optimized states.
5 Related work
Map reconstruction.Reconstructing an electrostatic potential (ESP) map at a resolution sufficient for
atomic model building typically requires tens to hundreds of thousands of particles. RELION (Zivanov
et al., 2018) and cryoSPARC (Punjani et al., 2017) estimate the particle poses and the map jointly within a
Bayesian framework. For heterogeneous data, these pipelines partition the particles intoK discrete classes
and reconstruct one map per class. cryoDRGN (Zhong et al., 2021) instead learns a continuous latent space
over the particles with a variational autoencoder and decodes each latent into a three-dimensional density,
and RECOV AR (Gilles and Singer, 2025) estimates the covariance of the underlying volume and embeds
the particles in its leading principal components. Both take the poses from a prior consensus reconstruction.
CryoDRGN-AI (Levy et al., 2025) extends this approach to theab initiosetting by estimating the poses
and the heterogeneous structural distribution jointly from the images. More recent approaches use a protein
structure prediction model (Abramson et al., 2024) as a structural prior and guide it with the experimental
density. In X-ray crystallography, Maddipatla et al. (2024) fit ensembles to electron densities by jointly
guiding a diffusion model of protein structure, recovering alternate backbone conformations, and Maddipatla
et al. (2025) extend this ensemble guidance to AlphaFold3, treated as a sequence-conditioned structural prior,
to infer ensembles consistent with crystallographic densities and NMR restraints. In cryo-EM, CryoBoltz
(Raghu et al., 2026) steers Boltz (Passaro et al., 2025) toward conformations consistent with an ESP map,
but requires an input structure roughly aligned to the map to establish the correspondence used during
guidance. Maddipatla et al. (2026b) instead guide AlphaFold3ab initio, from sequence alone, toward
structures consistent with experimental ESP maps. Embed-Opt (Li et al., 2026) and IT-Opt (Maddipatla et al.,
2026a) take a complementary inference-time approach and optimize the latent representations of AlphaFold
to produce structures consistent with synthetic ESP maps.
(Riley et al., 2021)
The closest prior work is CoCoFold (Liao et al., 2026), which constrains AlphaFold directly with
individual cryo-EM particle images. CoCoFold performs target-specific fine-tuning of the AlphaFold-
Multimer structure module, with the Evoformer frozen, using an FRC loss between experimental particles
and differentiable projections; it assumes upstream pose/CTF estimates and uses a coarse reconstruction to
establish a fixed coordinate frame.
19


## Conclusion

We introduced Fold’EM, an inference-time framework that infers atomic structures directly from cryo-EM
particle images by guiding AlphaFold3 with particle-level evidence, bypassing density reconstruction and
model building. We showed that density fitting reproduces the particle likelihood only under the experiment-
induced metric and that, under pose or class uncertainty, a consensus density need not be a sufficient
statistic; and that optimizing intermediate rather than terminal Pairformer states induces a learned geometry
that substantially strengthens guidance. Fold’EM recovers accurate structures from fewer than 1% of the
particles used by conventional reconstruction with known poses, roughly 3% ab initio, and roughly 5%
for heterogeneous samples, recovering features missed by the unguided prediction, such as the Integrin
α5β1–BIIG2 binding site and the distorted DNA of UvrA. Conformational organization in particle space
is also reflected in the AlphaFold representation, so that continuous motions can be represented by a few
anchor states. Together, these results suggest a shorter route to structure determination in which the prior
supplies what is already known and the experiment determines what it does not: assembly, conformation, and
interaction geometry.
Limitations.Fold’EM is not yet an end-to-end replacement for the cryo-EM pipeline: inputs are curated
particle collections with known CTF parameters, andab initioinference relies on accurate pose estimates
for initialization. Components absent from the model, such as glycans, ligands or flexible regions, are
treated as unexplained signal, and fine local details, such as interface loops, remain harder to recover than
global assemblies and major conformational changes. Uncurated particles, unmodelled density, better pose
initialization, and finer local refinement are natural directions for future work.
AI use statement
Generative AI tools, primarily OpenAI ChatGPT and Anthropic Claude, were used during manuscript
preparation for language editing, improving clarity and organization, checking mathematical exposition,
assisting with code development and debugging, and literature and reference formatting. All scientific claims,
derivations, code, experimental results, interpretations, and citations were reviewed and verified by the
authors. The authors take full responsibility for the content of the paper and full credit for its scientific claims.
Ethics statement
This work does not involve human subjects or sensitive personal data, and poses no identifiable risks to
individuals or their security. All datasets used in this work were either synthetically generated from protein
structures available in the Protein Data Bank (PDB) (Burley et al., 2017) or derived from publicly available
cryo-EM particle datasets in EMPIAR (Iudin et al., 2016).
Reproducibility statement
All hyperparameters and implementation details are provided in Appendix D.5, and the full Fold’EM proce-
dure is given as pseudocode in Algorithm 1. The hardware resources, model weights and software versions
are listed in Appendix D.2.1. The datasets, their pre-processing and the baseline protocols are described in Ap-
pendices B.1, D.1 and D.2. The image formation model and likelihood are derived in Appendix D.3, the stere-
ochemical losses and relaxation in Appendices D.2.2 and D.2.3, and the evaluation metrics in Appendix D.2.4.
The code will be publicly released.
20


## References

EMDB—the electron microscopy data bank.Nucleic Acids Research, 52(D1):D456–D465, 2024.(Cited on
page 26.)
Josh Abramson, Jonas Adler, Jack Dunger, Richard Evans, Tim Green, Alexander Pritzel, Olaf Ronneberger,
Lindsay Willmore, Andrew J Ballard, Joshua Bambrick, et al. Accurate structure prediction of biomolecular
interactions with AlphaFold 3.Nature, 630(8016):493–500, 2024.(Cited on pages 8, 19, and 39.)
Minkyung Baek et al. Accurate prediction of protein structures and interactions using a three-track neural
network.Science, 373:871–876, 2021. doi: 10.1126/science.abj8754.(Cited on page 2.)
Stephen K Burley, Helen M Berman, Gerard J Kleywegt, John L Markley, Haruki Nakamura, and Sameer
Velankar. Protein data bank (PDB): the single global macromolecular structure archive.Protein Crystal-
lography: Methods and Protocols, pages 627–641, 2017.(Cited on pages 20, 26, and 38.)
Alisia Fadini, Minhuan Li, Airlie J McCoy, Suresh Banjara, Hiroki Okumura, Eve Napier, Pietro Fontana,
Amir R Khan, Luca Jovine, Thomas C Terwilliger, et al. AlphaFold as a prior: experimental structure
determination conditioned on a pretrained neural network.Nature Methods, pages 785–795, 2026.(Cited on
pages 1 and 2.)
Rafael Fernandez-Leiro and Sjors H. W. Scheres. Unravelling biological macromolecules with cryo-electron
microscopy.Nature, 537:339–346, 2016. doi: 10.1038/nature19948.(Cited on page 1.)
Joachim Frank and Abbas Ourmazd. Continuous changes in structure mapped by manifold embedding of
single-particle data in cryo-EM.Methods, 100:61–67, 2016. doi: 10.1016/j.ymeth.2016.02.007.(Cited on
page 2.)
Marc Aurèle Gilles and Amit Singer. Cryo-EM heterogeneity analysis using regularized covariance estimation
and kernel regression.Proceedings of the National Academy of Sciences, 122(9):e2419140122, 2025.
(Cited on pages 2, 7, 16, 19, and 45.)
Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffusion probabilistic models. InAdvances in Neural
Information Processing Systems, volume 33, pages 6840–6851, 2020.(Cited on page 8.)
Viktor Hornak, Robert Abel, Asim Okur, Bentley Strockbine, Adrian Roitberg, and Carlos Simmerling.
Comparison of multiple amber force fields and development of improved protein backbone parameters.
Proteins: Structure, Function, and Bioinformatics, 65(3):712–725, 2006.(Cited on page 40.)
Andrii Iudin, Paul K Korir, José Salavert-Torres, Gerard J Kleywegt, and Ardan Patwardhan. EMPIAR: a
public archive for raw electron microscopy image data.Nature Methods, 13(5):387–388, 2016.(Cited on
pages 20, 26, and 38.)
Kiarash Jamali, Lukas Käll, Rui Zhang, Alan Brown, Dari Kimanius, and Sjors HW Scheres. Automated
model building and protein identification in cryo-EM maps.Nature, 628(8007):450–457, 2024.(Cited on
page 1.)
Minkyu Jeon, Rishwanth Raghu, Miro Astore, Geoffrey Woollard, Ryan Feathers, Alkin Kaz, Sonya M
Hanson, Pilar Cossio, and Ellen D Zhong. CryoBench: diverse and challenging datasets for the hetero-
geneity problem in cryo-EM. InAdvances in Neural Information Processing Systems, volume 37, pages
89468–89512, 2024.(Cited on page 17.)
21

John Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf Ronneberger, Kathryn
Tunyasuvunakool, Russ Bates, Augustin Žídek, Anna Potapenko, et al. Highly accurate protein structure
prediction with AlphaFold.Nature, 596(7873):583–589, 2021.(Cited on page 2.)
Wolfgang Kabsch. A solution for the best rotation to relate two sets of vectors.Acta Crystallographica, 32
(5):922–923, 1976.(Cited on page 40.)
Tero Karras, Miika Aittala, Timo Aila, and Samuli Laine. Elucidating the design space of diffusion-based
generative models. InAdvances in Neural Information Processing Systems, volume 35, pages 26565–26577,
2022.(Cited on page 8.)
Dari Kimanius, Liyi Dong, Grigory Sharov, Takanori Nakane, and Sjors HW Scheres. New tools for
automated cryo-EM single-particle analysis in RELION-4.0.Biochemical Journal, 478(24):4169–4185,
2021.(Cited on page 7.)
Dari Kimanius et al. Data-driven regularization lowers the size barrier of cryo-EM structure determination.
Nature Methods, 21:1216–1221, 2024. doi: 10.1038/s41592-024-02304-8.(Cited on pages 1 and 2.)
Diederik P Kingma and Jimmy Ba. Adam: a method for stochastic optimization. InInternational Conference
on Learning Representations (ICLR), 2015.(Cited on page 47.)
Harold W Kuhn. The hungarian method for the assignment problem.Naval Research Logistics Quarterly, 2
(1–2):83–97, 1955.(Cited on page 46.)
Axel Levy, Rishwanth Raghu, J Ryan Feathers, Michal Grzadkowski, Frédéric Poitevin, Jake D Johnston,
Francesca Vallese, Oliver Biggs Clarke, Gordon Wetzstein, and Ellen D Zhong. cryoDRGN-AI: neural ab
initio reconstruction of challenging cryo-EM and cryo-ET datasets.Nature Methods, 22(7):1486–1494,
2025.(Cited on pages 9, 19, and 39.)
Minhuan Li, Jiequn Han, Pilar Cossio, and Luhuan Wu. Robust inference-time steering of protein diffusion
models via embedding optimization.arXiv preprint arXiv:2602.05285, 2026.(Cited on pages 3, 11, and 19.)
Junwen Liao, Dihan Zheng, Hui Zhang, Linfeng Zhang, Mingxu Hu, and Chenglong Bao. Fine-tuning
AlphaFold with limited cryo-EM observations.Communications Chemistry, 9:95, 2026. doi: 10.1038/
s42004-026-01899-7. URL https://doi.org/10.1038/s42004-026-01899-7.(Cited on page 19.)
Dorothee Liebschner, Pavel V Afonine, Matthew L Baker, Gábor Bunkóczi, Vincent B Chen, Tristan I Croll,
Bradley Hintze, L-W Hung, Swati Jain, Airlie J McCoy, et al. Macromolecular structure determination
using X-rays, neutrons and electrons: recent developments in Phenix.Acta Crystallographica Section D:
Structural Biology, 75(10):861–877, 2019.(Cited on page 39.)
Advaith Maddipatla, Anar Rzayev, Marco Pegoraro, Martin Pacesa, Paul Schanda, Ailie Marx, Sanketh
Vedula, and Alex M Bronstein. Inference-time optimization for experiment-grounded protein ensemble
generation. InInternational Conference on Machine Learning, 2026a.(Cited on pages 3, 7, 8, 10, 11, 19, and 47.)
Advaith Maddipatla, Nadav Sellam Bojan, Meital Bojan, V olodymyr Masalitin, Sanketh Vedula, Paul Schanda,
Ailie Marx, and Alex M. Bronstein. Experiment-guided AlphaFold3 resolves measurement-consistent
protein ensembles.Nature Biotechnology, 2026b. doi: 10.1038/s41587-026-03166-5.(Cited on pages 2, 3, 6,
10, 11, and 19.)
Sai Advaith Maddipatla, Nadav Bojan Sellam, Sanketh Vedula, Ailie Marx, and Alex M Bronstein. Generative
modeling of protein ensembles guided by crystallographic electron densities. InNeurIPS Workshop on
Machine Learning in Structural Biology, 2024. arXiv:2412.13223.(Cited on page 19.)
22

Sai Advaith Maddipatla, Nadav Bojan, Meital Bojan, Sanketh Vedula, Paul Schanda, Ailie Marx, and
Alexander Bronstein. Inverse problems with experiment-guided AlphaFold. InInternational Conference
on Machine Learning, volume 267 ofProceedings of Machine Learning Research, pages 42366–42393,
2025.(Cited on pages 2, 3, and 19.)
M.-E. Mäeots and R. I. Enchev. Structural dynamics: review of time-resolved cryo-EM.Acta Crystallo-
graphica Section D: Structural Biology, 78:927–935, 2022. doi: 10.1107/S2059798322006155.(Cited on
page 1.)
Abbas Ourmazd. Cryo-EM, XFELs and the structure conundrum in structural biology.Nature Methods, 16:
941–944, 2019. doi: 10.1038/s41592-019-0587-4.(Cited on page 1.)
Fabio Parisi, Francesco Strino, Boaz Nadler, and Yuval Kluger. Ranking and combining multiple predictors
without labeled data.Proceedings of the National Academy of Sciences, 111(4):1253–1258, 2014.(Cited on
pages 7 and 46.)
Saro Passaro, Gabriele Corso, Jeremy Wohlwend, Mateo Reveiz, Stephan Thaler, Vignesh Ram Somnath,
Noah Getz, Tally Portnoi, Julien Roy, Hannes Stark, et al. Boltz-2: towards accurate and efficient binding
affinity prediction.bioRxiv, 2025.(Cited on page 19.)
Ali Punjani, John L Rubinstein, David J Fleet, and Marcus A Brubaker. cryoSPARC: algorithms for rapid
unsupervised cryo-EM structure determination.Nature Methods, 14(3):290–296, 2017.(Cited on page 19.)
Rishwanth Raghu, Axel Levy, Gordon Wetzstein, and Ellen D Zhong. Multiscale guidance of protein structure
prediction with heterogeneous cryo-EM data. InAdvances in Neural Information Processing Systems,
volume 38, pages 10175–10203, 2026.(Cited on pages 2, 3, 6, and 19.)
Blake T Riley, Stephanie A Wankowicz, Saulo HP de Oliveira, Gydo CP van Zundert, Daniel W Hogan,
James S Fraser, Daniel A Keedy, and Henry van den Bedem. qfit 3: Protein and ligand multiconformer
modeling for x-ray crystallographic and single-particle cryo-em density maps.Protein science, 30(1):
270–285, 2021.(Cited on page 19.)
Alexis Rohou and Nikolaus Grigorieff. CTFFIND4: fast and accurate defocus estimation from electron
micrographs.Journal of Structural Biology, 192(2):216–221, 2015.(Cited on page 43.)
Peter B Rosenthal and Richard Henderson. Optimal determination of particle orientation, absolute hand, and
contrast loss in single-particle electron cryomicroscopy.Journal of Molecular Biology, 333(4):721–745,
2003.(Cited on page 41.)
Sjors H. W. Scheres. RELION: implementation of a bayesian approach to cryo-EM structure determination.
Journal of Structural Biology, 180:519–530, 2012. doi: 10.1016/j.jsb.2012.09.006.(Cited on pages 1 and 42.)
RH Wade. A brief look at imaging and contrast transfer.Ultramicroscopy, 46(1–4):145–156, 1992.(Cited on
page 43.)
Christopher J Williams, Jeffrey J Headd, Nigel W Moriarty, Michael G Prisant, Lizbeth L Videau, Lindsay N
Deis, Vishal Verma, Daniel A Keedy, Bradley J Hintze, Vincent B Chen, et al. MolProbity: more and
better reference data for improved all-atom structure validation.Protein Science, 27(1):293–315, 2018.
(Cited on pages 29, 30, 31, 35, 36, and 41.)
Yang Zhang and Jeffrey Skolnick. Scoring function for automated assessment of protein structure template
quality.Proteins: Structure, Function, and Bioinformatics, 57(4):702–710, 2004.(Cited on page 41.)
23

Yuxuan Zhang, Chengyue Gong, Hanyu Zhang, Wenzhi Ma, Zhenyu Liu, Xinshi Chen, Jiaqi Guan, Lan Wang,
Yanping Yang, Yu Xia, and Wenzhi Xiao. Protenix-v1: toward high-accuracy open-source biomolecular
structure prediction.bioRxiv, 2026. doi: 10.64898/2026.02.05.703733. URL https://www.biorxiv.org/
content/early/2026/02/22/2026.02.05.703733.1.(Cited on page 39.)
Ellen D Zhong, Tristan Bepler, Bonnie Berger, and Joseph H Davis. cryoDRGN: reconstruction of heteroge-
neous cryo-EM structures using neural networks.Nature Methods, 18(2):176–185, 2021.(Cited on pages 2, 7,
9, 19, and 38.)
Jasenko Zivanov, Takanori Nakane, Björn O Forsberg, Dari Kimanius, Wim JH Hagen, Erik Lindahl,
and Sjors HW Scheres. New tools for automated high-resolution cryo-EM structure determination in
RELION-3.eLife, 7:e42166, 2018.(Cited on pages 9, 19, 38, and 39.)
24

A Overview of the appendix
The appendix is organized as follows.
• Appendix B: Additional tables.The experimental and synthetic datasets (Appendix B.1), and the full
quantitative results for homogeneous reconstruction with known poses (Appendix B.2), homogeneous
ab initioreconstruction (Appendix B.3), heterogeneous reconstruction (Appendix B.4), and continuous
heterogeneity on IgG-1D (Appendix B.5).
• Appendix C: Algorithms.Pseudocode for Fold’EM (Algorithm 1) and for the residual-subspace
estimator of B-RECOV AR (Algorithm 2).
• Appendix D: Additional details.Data pre-processing and baselines (Appendices D.1 and D.2),
software and hardware (Appendix D.2.1), the stereochemical losses and relaxation (Appendices D.2.2
and D.2.3), the evaluation metrics (Appendix D.2.4), the image formation model used to render particles
from atomic structures, the contrast transfer function, and likelihood computation (Appendix D.3), the
B-RECOV AR class-assignment method (Appendix D.4) and the hyperparameters and implementation
details (Appendix D.5).
25

B Additional tables
B.1 Datasets
Table A1: Experimental cryo-EM datasets from EMPIAR (Iudin et al., 2016).For each PDB entry, we report the
corresponding EMPIAR and EMDB entries (wwp, 2024), reported resolution, molecular weight (kDa), and number of
particles in original dataset.
PDB ID EMPIAR ID EMD ID Resolution(Å) # Particles Protein size (kDa)
9B9J12552 44386 2.60 374814 115.11
9B7712002 44302 2.74 490807 141.72
8PWH11665 17993 3.17 708609 162.75
9GXR13396 51671 3.04 197058 162.70
9GXQ13396 51672 2.74 195233 162.70
Table A2: Synthetic datasets constructed using PDB-deposited structures (Burley et al., 2017).For each entry,
we report the corresponding EMDB entry (wwp, 2024), reported resolution, molecular weight (kDa), and amino acid
sequence length.
PDB ID EMD ID Resolution(Å) Seq Length Protein size (kDa)
9UGB64135 3.25 818 88.97
9UGC64136 3.52 818 99.62
8U4B41877 3.80 2764 312.70
8U4E41880 4.20 3304 373.10
1HZHCryoBench (IgG-1D)2.70 1331 146.96
26

B.2 Homogeneous reconstruction with known poses
Table A3: Resolution at Fourier shell correlation (FSC)= 0.143 (↓,Å ) on the experimental cryo-EM datasets
from Table A1.For Fold’EM, AlphaFold3 and PDB structures, FSC is computed using phenix.model_map. All
baselines at different fraction of the original dataset 500 particles with known poses and are evaluated against the
deposited EMD map. Entries highlighted inboldindicate the best result (excluding PDB).
Fraction of dataset Method9B9J 9B77 8PWH 9GXQ 9GXR
1/1000
Fold’EM 3.73 2.88 6.21 3.08 3.18
cryoDRGN 8.40 5.70 7.56 9.87 4.33
RELION 21.94 11.48 14.12 14.15 17.92
AlphaFold3 21.90 5.96 64.96 11.69 3.54
PDB 2.38 2.49 3.06 2.64 2.89
1/500
Fold’EM 3.73 2.85 6.63 3.02 3.20
cryoDRGN 7.41 4.87 7.55 9.60 3.90
RELION 17.95 11.48 15.47 14.15 14.93
AlphaFold3 21.90 5.96 64.96 11.69 3.54
PDB 2.38 2.49 3.06 2.64 2.89
1/250
Fold’EM 3.35 2.73 6.63 3.95 3.09
cryoDRGN 7.04 4.876.639.27 3.73
RELION 15.19 11.07 12.99 12.22 12.22
AlphaFold3 21.90 5.96 64.96 11.69 3.54
PDB 2.38 2.49 3.06 2.64 2.89
1/100
Fold’EM 3.50 2.737.063.09 3.26
cryoDRGN 6.71 3.925.169.27 3.73
RELION 12.74 7.21 10.15 10.75 9.60
AlphaFold3 21.90 5.96 64.96 11.69 3.54
PDB 2.38 2.49 3.06 2.64 2.89
1/50
Fold’EM 3.46 2.756.133.36 3.45
cryoDRGN 6.46 3.875.018.67 3.58
RELION 12.34 6.74 9.02 7.07 7.07
AlphaFold3 21.90 5.96 64.96 11.69 3.54
PDB 2.38 2.49 3.06 2.64 2.89
Table A4: Quantitative evaluation of Cα RMSD (↓, Å) and TM-score (↑) on the experimental cryo-EM datasets
from Table A1.Fold’EM structures are obtained using different fractions of the original dataset. Entries highlighted in
boldindicate the best result.
CαRMSD (↓, Å) TM-score (↑)
Fraction
of dataset 9B9J 9B77 8PWH 9GXQ 9GXR 9B9J 9B77 8PWH 9GXQ 9GXR
1/1000 1.96 1.90 4.340 2.20 1.87 0.969 0.972 0.900 0.877 0.899
1/500 1.97 1.77 4.9891.991.39 0.970 0.979 0.8970.8930.902
1/250 1.88 1.714.597 2.481.23 0.972 0.9810.885 0.8800.904
1/100 1.92 1.74 5.349 2.02 1.35 0.971 0.980 0.8840.8930.903
1/50 1.88 1.71 4.1742.09 1.47 0.972 0.981 0.9090.885 0.897
AlphaFold3 21.90 3.87 33.16 5.96 2.01 0.776 0.916 0.397 0.734 0.886
27

Table A5: Resolution at Fourier shell correlation (FSC)= 0.143 (↓) on the synthetic cryo-EM datasets from
Table A2.For Fold’EM, AlphaFold3 and PDB structures, FSC is computed using phenix.model_map. Fold’EM
structures are generated using 100,250,500,& 1000 particles at SNR 0.01 and 0.005 with known poses and are
evaluated against the deposited EMD map. Entries highlighted inboldindicate the best result (excluding PDB).
9UGB 9UGC 8U4B 8U4E
# particles Method SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
100
Fold’EM 3.24 3.25 3.59 3.45 3.76 3.80 4.04 4.18
cryoDRGN 3.63 3.95 3.81 3.96 7.85 9.80 9.47 10.03
RELION 9.79 9.79 9.79 9.79 17.78 16.84 19.20 18.29
AlphaFold3 8.21 19.29 7.29 8.84
PDB 3.39 3.47 3.50 3.67
250
Fold’EM 3.22 3.22 3.39 3.43 3.75 3.73 3.99 3.89
cryoDRGN 3.39 3.55 3.59 3.63 7.00 7.16 7.23 7.56
RELION 7.92 9.24 6.66 8.76 10.32 11.03 13.71 16.70
AlphaFold3 8.21 19.29 7.29 8.84
PDB 3.39 3.47 3.50 3.67
500
Fold’EM 3.23 3.26 3.39 3.39 3.70 3.70 3.96 3.93
cryoDRGN 3.32 3.35 3.55 3.59 5.99 6.88 6.77 7.40
RELION 5.94 6.40 5.94 6.40 10.00 10.32 12.00 12.39
AlphaFold3 8.21 19.29 7.29 8.84
PDB 3.39 3.47 3.50 3.67
1000
Fold’EM 3.22 3.22 3.38 3.43 3.69 3.72 3.91 4.00
cryoDRGN 3.25 3.32 3.55 3.55 5.81 5.91 6.06 6.95
RELION 5.04 5.74 5.04 6.16 8.65 10.00 10.00 10.53
AlphaFold3 8.21 19.29 7.29 8.84
PDB 3.39 3.47 3.50 3.67
Table A6: Quantitative evaluation of Cα RMSD (↓, Å) and TM-score (↑) on the synthetic cryo-EM datasets from
Table A2.Fold’EM structures are obtained using 100,250,500,& 1000 particles with known poses at SNR 0.01 and
0.005; AlphaFold3 is the unguided baseline. Scores are computed with respect to the experimentally resolved structures
deposited in the PDB. Entries highlighted inboldindicate the best result.
9UGB 9UGC 8U4B 8U4E
Metric # particles SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
CαRMSD
(↓, Å)
100 1.05 1.01 2.78 1.45 1.681 1.907 1.769 2.116
250 0.88 0.88 1.341.37 1.362 1.350 1.798 1.512
500 0.811.12 1.44 1.41 1.2481.227 1.503 1.479
1000 0.840.86 1.331.44 1.1321.228 1.686 1.711
AlphaFold3 8.96 11.22 7.780 26.670
TM-score
(↑)
100 0.964 0.965 0.939 0.983 0.9832 0.9785 0.9810 0.9731
250 0.9670.967 0.987 0.984 0.9887 0.9890 0.9807 0.9861
500 0.9680.962 0.9850.984 0.9906 0.9908 0.9862 0.9866
1000 0.9670.967 0.9870.983 0.9923 0.9909 0.9828 0.9822
AlphaFold3 0.699 0.661 0.7981 0.4772
28

Table A7: MolProbity evaluation of Fold’EM structures over synthetic targets with known poses. We re-
port median MolProbity score (↓), clash score ( ↓), and Ramachandran outlier percentage ( ↓), computed using
phenix.molprobity(Williams et al., 2018) over all relaxed structures in Table A6.
9UGB 9UGC 8U4B 8U4E
MolProbity statistic SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
MolProbity score1.01 1.05 1.36 1.44 1.35 1.35 1.56 1.54
Clashscore2.29 2.61 3.38 2.85 1.59 1.49 3.01 3.02
Ramachandran outliers0.00 0.00 0.28 0.55 1.49 1.40 1.72 1.26
Table A8: MolProbity evaluation of Fold’EM structures over real targets with known poses. We report median Mol-
Probity score (↓), clash score (↓), and Ramachandran outlier percentage (↓), computed using phenix.molprobity
(Williams et al., 2018) over all structures in Table A4.
MolProbity statistic9B9J 9B77 8PWH 9GXQ 9GXR
MolProbity score0.84 0.81 1.71 1.08 1.07
Clashscore0.38 0.60 5.42 1.21 0.99
Ramachandran outliers0.10 0.24 0.43 0.16 0.40
B.3 Homogeneousab initioreconstruction
Table A9: Resolution at Fourier shell correlation (FSC)= 0.143 (↓) on the experimental cryo-EM datasets from
Table A1, with poses inferredab initio.For Fold’EMab initio, AlphaFold3 and PDB structures, FSC is computed
using phenix.model_map. The number of particles used for the experiment is given below each identifier. Entries
highlighted inboldindicate the best result.

## Method

# particles
9B9J
1000
9B77
1000
8PWH
5000
9GXQ
5000
9GXR
5000
Fold’EM3.52 2.8510.834.48 3.22
cryoDRGN-AI35.90 31.01 32.80 24.44 26.88
RELION (ab initio)11.62 7.959.846.25 4.98
AlphaFold321.90 4.40 64.96 11.70 3.50
PDB2.38 2.49 3.06 2.64 2.89
Table A10: Quantitative evaluation of TM-score (↑) andCα-RMSD (↓) on the experimental cryo-EM datasets
from Table A1, with poses inferredab initio.The number of particles used is given below each identifier, and scores
are computed with respect to the experimentally resolved structures deposited in the PDB. Entries highlighted inbold
indicate the best result.
CαRMSD (↓, Å) TM-score (↑)

## Method

# particles
9B9J
1000
9B77
1000
8PWH
5000
9GXQ
5000
9GXR
5000
9B9J
1000
9B77
1000
8PWH
5000
9GXQ
5000
9GXR
5000
Fold’EM 2.49 2.25 18.91 2.87 1.54 0.956 0.967 0.602 0.857 0.898
AlphaFold3 21.90 3.87 33.16 5.96 2.01 0.776 0.916 0.397 0.734 0.886
29

Table A11: Resolution at Fourier shell correlation (FSC)= 0.143 (↓) on the synthetic cryo-EM datasets from
Table A2, with poses inferredab initio.For Fold’EMab initio, AlphaFold3 and PDB structures, FSC is computed
using phenix.model_map. All methods use 500 particles at SNR 0.01 and 0.005. Entries highlighted inbold
indicate the best result (excluding PDB).
9UGB 9UGC 8U4B 8U4E
# particles Method SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
500
Fold’EM 3.47 3.25 3.59 3.91 5.87 7.23 11.38 11.53
cryoDRGN-AI 12.80 27.70 33.30 33.20 22.59 38.40 38.40 38.40
RELION (ab initio) 7.23 8.93 6.93 7.56 10.97 16.00 11.64 15.36
AlphaFold3 8.21 19.29 7.29 8.84
PDB 3.39 3.47 3.5 3.67
Table A12: Quantitative evaluation of TM-score (↑) andCα-RMSD (↓,Å ) on the synthetic cryo-EM datasets
from Table A2, with poses inferredab initio.Fold’EMab initioresults are obtained using 500 particles at SNR 0.01
and 0.005, and scores are computed with respect to the experimentally resolved structures deposited in the PDB. Entries
highlighted inboldindicate the best result.
9UGB 9UGC 8U4B 8U4E
Metric Method SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
CαRMSD
(↓, Å)
Fold’EM 1.78 1.57 2.35 3.07 3.948 3.941 7.684 6.885
AlphaFold3 8.96 11.22 7.780 26.670
TM-score
(↑)
Fold’EM 0.969 0.976 0.948 0.917 0.9174 0.9182 0.810 0.809
AlphaFold3 0.699 0.661 0.7981 0.4772
Table A13: MolProbity evaluation of theab initioFold’EM structures in Table A12. For each relaxed struc-
ture, we report MolProbity score (↓), clash score (↓), and Ramachandran outlier percentage (↓), computed using
phenix.molprobity(Williams et al., 2018).
9UGB 9UGC 8U4B 8U4E
Statistic SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
MolProbity score 1.18 1.15 1.25 1.15 1.50 1.53 1.58 1.79
Clashscore 3.72 3.64 4.83 3.56 1.21 2.35 1.56 2.21
Ramachandran outliers 0.00 0.25 0.12 0.00 1.26 0.71 0.98 0.66
30

Table A14: MolProbity evaluation of theab initioFold’EM structures in Table A10. For each relaxed struc-
ture, we report MolProbity score (↓), clash score (↓), and Ramachandran outlier percentage (↓), computed using
phenix.molprobity(Williams et al., 2018). Particle counts are as in Table A9.
Statistic9B9J 9B77 8PWH 9GXQ 9GXR
MolProbity score0.93 0.80 1.48 1.22 1.11
Clashscore0.82 1.04 4.01 2.52 1.57
Ramachandran outliers0.19 0.00 0.27 0.16 0.24
B.4 Heterogeneous reconstruction
Table A15: Resolution at Fourier shell correlation (FSC)= 0.143 (↓) on the heterogeneous experimental dataset
EMPIAR-13396, with known poses.The two conformational states 9GXQ and 9GXR are resolved from the same
mixed particle stack, and the sweep is over the number of particles per state. For Fold’EM, AlphaFold3 and PDB
structures, FSC is computed usingphenix.model_map. Entries highlighted inboldindicate the best result.
# particles
per conf. Method9GXQ 9GXR
500
Fold’EM 6.253.02
RELION 8.67 8.40
cryoDRGN 5.604.89
1000
Fold’EM 3.09 2.95
RELION 6.89 10.75
cryoDRGN 4.34 4.41
2000
Fold’EM 3.16 3.01
RELION 5.97 4.80
cryoDRGN 4.27 4.10
5000
Fold’EM 3.13 2.99
RELION 7.47 7.07
cryoDRGN 4.10 4.03
10000
Fold’EM 3.16 2.99
RELION 6.56 6.40
cryoDRGN 4.00 3.99
AlphaFold3 11.69 3.54
PDB 2.64 2.89
31

Table A16: Quantitative evaluation of Cα RMSD (↓, Å) and TM-score (↑) on the heterogeneous experimental
dataset EMPIAR-13396, with known poses.Fold’EM resolves the two conformational states 9GXQ and 9GXR from
the same mixed particle stack, and the sweep is over the number of particles per state. Entries highlighted inbold
indicate the best result.
CαRMSD (↓, Å) TM-score (↑)
# particles
per conf. 9GXQ 9GXR 9GXQ 9GXR
500 3.30 1.85 0.840 0.890
1000 1.631.45 0.891 0.899
2000 1.76 1.71 0.886 0.894
5000 1.48 1.45 0.893 0.900
10000 1.82 1.73 0.885 0.894
AlphaFold3 5.96 2.01 0.734 0.886
Table A17: Resolution at Fourier shell correlation (FSC)= 0.143 (↓) on the heterogeneous experimental dataset
EMPIAR-13396, with poses inferredab initio.The two conformational states 9GXQ and 9GXR are resolved from the
same mixed particle stack, and the sweep is over the number of particles per state. For Fold’EMab initio, AlphaFold3
and PDB structures, FSC is computed using phenix.model_map. Entries highlighted inboldindicate the best
result (excluding PDB).
# particles
per conf. Method9GXQ 9GXR
500
Fold’EM 8.673.58
RELION (ab initio) 22.40 12.80
cryoDRGN-AI 38.40 26.90
1000
Fold’EM 7.474.20
RELION (ab initio) 38.40 10.75
cryoDRGN-AI 26.90 22.40
2000
Fold’EM 11.69 3.24
RELION (ab initio) 19.20 10.34
cryoDRGN-AI 24.40 26.90
5000
Fold’EM 8.67 3.02
RELION (ab initio) 13.44 11.20
cryoDRGN-AI 20.68 22.40
10000
Fold’EM 4.63 3.09
RELION (ab initio) 26.88 8.40
cryoDRGN-AI 17.92 16.80
AlphaFold3 11.693.54
PDB 2.64 2.89
32

Table A18: Quantitative evaluation of Cα RMSD (↓, Å) and TM-score (↑) on the heterogeneous experimental
dataset EMPIAR-13396, with poses inferredab initio.Fold’EMab initioresolves the two conformational states
9GXQ and 9GXR from the same mixed particle stack, and the sweep is over the number of particles per state. Entries
highlighted inboldindicate the best result.
CαRMSD (↓, Å) TM-score (↑)
# particles
per conf. 9GXQ 9GXR 9GXQ 9GXR
500 4.54 2.61 0.799 0.874
1000 5.48 2.80 0.781 0.868
2000 5.84 2.39 0.737 0.880
5000 5.061.63 0.776 0.895
10000 3.721.66 0.836 0.896
AlphaFold3 5.96 2.01 0.734 0.886
Table A19: Resolution at Fourier shell correlation (FSC)= 0.143 (↓) on the heterogeneous synthetic 9UGB/9UGC
mixture, with known poses.The two conformational states are resolved from the same mixed particle stack at SNR
0.01 and 0.005, and the sweep is over the number of particles per state. Entries highlighted inboldindicate the best
result.
9UGB 9UGC
# particles
per conf. Method SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
250
Fold’EM 3.25 3.28 3.43 3.47
RELION 9.24 10.40 9.24 11.09
cryoDRGN 4.38 6.16 6.40 8.76
500
Fold’EM 3.24 3.25 3.39 3.43
RELION 7.92 8.76 8.32 9.24
cryoDRGN 3.62 4.50 4.75 6.16
1000
Fold’EM 3.22 3.25 3.43 3.39
RELION 6.93 7.93 7.23 7.92
cryoDRGN 3.70 3.62 4.38 4.75
AlphaFold3 8.21 19.29
PDB 3.39 3.47
33

Table A20: Quantitative evaluation of C α RMSD (↓, Å) and TM-score (↑) on the heterogeneous synthetic
9UGB/9UGC mixture, with known poses.Fold’EM resolves the two conformational states from the same mixed
particle stack at SNR 0.01 and 0.005, and the sweep is over the number of particles per state. Entries highlighted in
boldindicate the best result.
CαRMSD (↓, Å) TM-score (↑)
9UGB 9UGC 9UGB 9UGC
# particles
per conf.
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
2500.760.99 1.55 1.38 0.9640.9600.9870.982
500 0.99 0.89 1.361.28 0.960 0.962 0.982 0.983
1000 0.930.81 1.181.59 0.9610.9630.9860.985
AlphaFold38.96 11.22 0.699 0.661
Table A21: Resolution at Fourier shell correlation (FSC)= 0.143 (↓) on the heterogeneous synthetic 9UGB/9UGC
mixture, with poses inferredab initio.The two conformational states are resolved from the same mixed particle stack
at SNR 0.01 and 0.005, and the sweep is over the number of particles per state. Entries highlighted inboldindicate the
best result.
9UGB 9UGC
# particles
per conf. Method SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
250
Fold’EM 3.22 7.61 3.63 4.81
RELION (ab initio) 8.32 8.32 23.77 8.76
cryoDRGN-AI 33.28 33.28 41.60 18.49
500
Fold’EM 3.25 3.35 3.51 3.55
RELION (ab initio) 6.93 7.92 7.23 8.32
cryoDRGN-AI 27.73 20.80 33.28 27.73
1000
Fold’EM 3.22 3.25 3.51 3.51
RELION (ab initio) 6.93 7.92 7.23 7.92
cryoDRGN-AI 28.81 16.64 27.73 27.73
AlphaFold3 8.21 19.29
PDB 3.39 3.47
34

Table A22: Quantitative evaluation of C α RMSD (↓, Å) and TM-score (↑) on the heterogeneous synthetic
9UGB/9UGC mixture, with poses inferredab initio.Fold’EM resolves the two conformational states from the same
mixed particle stack at SNR 0.01 and 0.005, and the sweep is over the number of particles per state. Entries highlighted
inboldindicate the best result.
CαRMSD (↓, Å) TM-score (↑)
9UGB 9UGC 9UGB 9UGC
# particles
per conf.
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
250 1.52 4.13 2.84 5.09 0.967 0.862 0.929 0.876
5001.501.95 2.71 2.61 0.968 0.9530.936 0.939
1000 1.971.71 2.42 2.17 0.952 0.9510.948 0.957
AlphaFold38.96 11.22 0.699 0.661
Table A23: MolProbity evaluation of Fold’EM structures on the heterogeneous synthetic9UGB/9UGC mixture.
We report median MolProbity score (↓), clash score (↓), and Ramachandran outlier percentage (↓), computed using
phenix.molprobity(Williams et al., 2018) over all structures in Tables A20 and A22.
9UGB 9UGC
Poses MolProbity statistic SNR
0.01
SNR
0.005
SNR
0.01
SNR
0.005
Known
MolProbity score 1.16 1.13 1.09 1.11
Clashscore 3.72 3.40 3.01 3.16
Ramachandran outliers 0.00 0.00 0.12 0.00
Ab initio
MolProbity score 1.39 1.48 1.44 1.46
Clashscore 5.85 7.28 6.65 6.72
Ramachandran outliers 0.12 0.12 0.12 0.25
Table A24: MolProbity evaluation of Fold’EM structures on the heterogeneous experimental dataset EMPIAR-
13396. We report median MolProbity score (↓), clash score (↓), and Ramachandran outlier percentage (↓), computed
usingphenix.molprobity(Williams et al., 2018) over all structures in Tables A16 and A18.
Poses MolProbity statistic9GXQ 9GXR
Known
MolProbity score 1.16 1.20
Clashscore 1.48 1.66
Ramachandran outliers 0.16 0.16
Ab initio
MolProbity score 1.32 1.38
Clashscore 2.74 2.61
Ramachandran outliers 0.16 0.08
35

B.5 Continuous heterogeneity on IgG-1D
Table A25: MolProbity evaluation of Fold’EM structures on IgG-1D. For each arm of the experiment, we report
MolProbity score (↓), clash score (↓), and Ramachandran outlier percentage (↓) of the relaxed structures, computed
using phenix.molprobity (Williams et al., 2018), averaged over the eight anchors and over the100 interpolated
states.
cryoDRGN RECOV AR B-RECOV AR
MolProbity statistic Anchors
(n= 8)
Interpolated
(n= 100)
Anchors
(n= 8)
Interpolated
(n= 100)
Anchors
(n= 8)
Interpolated
(n= 100)
MolProbity score0.72 0.71 0.70 0.72 0.74 0.72
Clashscore0.59 0.59 0.59 0.66 0.66 0.54
Ramachandran outliers0.15 0.15 0.15 0.15 0.15 0.15
B.6 Confidence-based particle selection
Table A26: Confidence-based particle selection described in Section D.4 prevents mode collapse in the ensemble.
On the heterogeneous experimental dataset EMPIAR-13396, embeddings optimized using high-confidence particles
typically yield better-separated conformations, accompanied by higher TM-scores to the corresponding conformations.
The “separation” column reports the difference between the RMSD of the true conformations 9GXQ and 9GXR and that
of the predicted conformations; smaller values indicate closer agreement with the true conformational separation.Bold
entries indicate the best result.
TM-score (↑)
# particles
per conf.
Confidence
method 9GXQ 9GXRSeparation (↓)
7.5k Cut by confidence0.835 0.894 0.58
No confidence0.822 0.888 1.35
10k Cut by confidence0.832 0.894 0.47
No confidence0.823 0.888 1.48
C Algorithms
Algorithm 1 gives the full Fold’EM procedure described in Section 3: the coordinate ascent that alternates
structure inference by guided reverse diffusion with the refinement of the nuisance variables. Algorithm 2
gives a single replicate of the residual-subspace estimator of B-RECOV AR (Appendix D.4), which provides
the initial class assignment in theab initioheterogeneous setting.
36

Algorithm 1Fold’EM
1: Input:Initial trunk embeddings H; particle images Y; initial nuisance variablesη(0); noise schedule
[σT,...,σ 0]; learning rateγh; ensemble sizen; coordinate iterationsR; diffusion runsQ; prior weight
λp
2: Output:Structural ensemble X={X 1,...,X n} decoded from the optimized Pairformer statesg(H)
3:forr= 0toR−1do▷Coordinate ascent
4:forq= 1toQdo▷Step 1: structure inference, Equation 3
5:X∼σ T·[N 1,...,N n]T ▷Ni∼N(0,I)
6:fort∈[T−1,...,0]do
7:H←H+γ h∇H

logp
 
Y|D θ(X;g(H),t),η (r)
+λ p logp(H|a)

▷Equation 5
8:X←ReverseSDE(X;g(H),t,σ t)▷Equation 4
9:end for
10:end for
11:η (r+1)←arg maxη

logp(Y|X,η) + logp(η)

▷Step 2: pose and class refinement, Equation 6
12:end for
13:Z←g(H)▷Optimized conditioning variables
14:X∼p(X|Z)▷Decode ensemble: unguided reverse diffusion, Equation 4
15:returnX▷Ensemble from the final reverse-diffusion run, conditioned ong(H)
Algorithm 2B-RECOV AR residual-subspace estimator for one replicate
1: Input:particles with poses and CTFs; band Ωa; number of classesn and of modesq; fitting subsetI;
mask fractionf;Talternating updates;Lrefinement iterations
2:Reconstruct the consensusˆρfrom all particles and derive the solvent maskMfrom it
3:Scale every particle to the consensus and subtract its projection▷residualsr k
4:form= 1,...,qdo
5: From a random start, alternateT times between back-projecting the residuals ofI into a masked mode
Wm and projecting them onto it▷alternating least squares
6:Remove the fitted mode from the residuals▷deflation
7:end for
8:Fit the coefficients ˆbk of every particle on all modes jointly▷joint coefficients
9:Cluster{ ˆbk}intonclasses byk-means▷initial labels
10:Refine the labels byLcross-validated updates of Equation 15▷two folds, centered rule
11:returnlabels{ˆc k}K
k=1
37

D Additional details
D.1 Pre-processing
Synthetic datasets.All synthetic datasets were prepared using the PDB deposited structure (Burley et al.,
2017). First, noiseless particles y were rendered by projecting the experimental PDB structure Xexpt using
the image formation model in Section D.3.3. White Gaussian noise was added to the noiseless particles in the
Fourier domain to match a specific signal to noise ratio (SNR).
ˆynoisy = ˆy+σ noise ˆN,N∼N(0,I),
The noise scaleσ noise was set using,
σnoise = std(ˆy)√
SNR
.
WhereSNRis the desired SNR for the dataset. Thus, the resulting particle satisfies
SNR = Var[ˆy]
Var[σnoise ˆN]
.
In all our synthetic experiments, we setSNR = 0.01or0.005.
Real datasets.All experimental datasets were downloaded from EMPIAR (Iudin et al., 2016). We
preprocess the deposited particle ensemble generation. We only retain the particles listed in the depositors’
final STAR files, and exclude particles identified as junk. The particles are then centered and Fourier-cropped
to 128×128 pixels, followed by phase flipping. We then apply a soft circular mask with a radius equal to0.4
times the box size.
D.2 Baselines
Known poses.We primarily compare against RELION (Zivanov et al., 2018) and CryoDRGN (Zhong
et al., 2021). Both methods reconstruct 3D density from particle images. In the commands below, angle
brackets denote dataset-specific inputs.
• CryoDRGN.With known poses, CryoDRGN (Zhong et al., 2021) volumes were trained using the
following command:
cryodrgn train_vae <particles.mrcs>
--poses <poses.pkl> --ctf <ctf.pkl> [--ind <ind.pkl>]
--zdim 8 -n 50 --no-amp
• RELION.With known poses, RELION (Zivanov et al., 2018) volumes were generated using the
following command:
relion_refine --ctf --skip_align --iter 5
--particle_diameter <diameter> --tau2_fudge 1
--split_random_halves --flatten_solvent
--solvent_mask <mask.mrc>
Here, <mask.mrc> is a low-pass reference generated from the EMD map with a 60 Å blob mask,
and the particle diameter<diameter>depends on the protein.
38

Ab initio.We primarily compare against RELION (ab initio) and CryoDRGN-AI (Levy et al., 2025). These
methods jointly estimate particle poses and 3D structure from the particle images without externally supplied
orientations.
•CryoDRGN-AI.CryoDRGN-AI volumes were trained using the following command:
cryodrgn abinit <particles.mrcs> --ctf <ctf.pkl> --o <outdir>
--zdim 8 --num-epochs 50 --no-amp --seed 0
--num-workers 0 --lazy --checkpoint 50
• RELION (ab initio).Without poses, RELION volumes were generated in two stages. First, an initial
model was constructed using VDAM without externally provided poses:
relion_refine --grad --denovo_3dref
--i <particles.star> --o <init_dir>/run --iter 200 --K 1
--sym <sym> --random_seed <seed> --particle_diameter <diameter>
--flatten_solvent --zero_mask --ctf
--ini_high 40 --oversampling 1 --healpix_order 1
--offset_range 6 --offset_step 2 --pool 30 --pad 1
--skip_gridding --dont_combine_weights_via_disc --gpu --j <threads>
We then performed 3D auto-refinement from the resulting initial model:
mpirun --oversubscribe --bind-to none -n 3 relion_refine_mpi
--auto_refine --split_random_halves
--i <particles.star> --ref <initial_model.mrc> --o <refine_dir>/run
--ini_high 30 --random_seed <seed> --ctf --sym <sym>
--particle_diameter <diameter> --flatten_solvent --zero_mask
--oversampling 1 --healpix_order 2 --auto_local_healpix_order 4
--offset_range 5 --offset_step 2 --low_resol_join_halves 40
--norm --scale --pool 30 --pad 2
--dont_combine_weights_via_disc --gpu --j <threads>
In all Fold’EMab initioexperiments, we use the poses and initial map generated in the first stage for
the subsequent refinement.
Heterogeneous reconstruction.For heterogeneous datasets, we first clustered the particles into structural
groups and then reconstructed each density separately using the corresponding particle subset. This provides
a density estimate for each discrete structural class without introducing additional heterogeneity modelling
assumptions.
D.2.1 AlphaFold3 and hardware resources
For all our experiments, we used Protenix v1.0.4 (Zhang et al., 2026) – a PyTorch reimplementation of
AlphaFold3 (Abramson et al., 2024). For map and pose estimation, we used RELION 5.0.0 (Zivanov et al.,
2018). For structural validation, we used Phenix (Liebschner et al., 2019) v1.21.2−5419 . All experiments
were carried out on NVIDIA H100 and L40S GPUs running Debian GNU/Linux 12.
39

D.2.2 Collision and bond length loss
To prevent the embedding optimization from generating physically invalid protein structures, we incorporate
numerous stereochemical regularizers. Given an ensemble of conformations X={X 1,...,X n} corre-
sponding to amino acid sequence a, we minimize three loss functions that avoid elongated bonds and steric
clashes.
Bond length loss.The bond-length loss for a structure withmatoms is given by,
Lbond(X;a) =
mX
i=1
mX
j=i+1
Bij·(max(0,|d ij−d ideal
ij |−δ bond))2
Here, B∈Z m×m is a mask with every elementbij∈{0,1} . If atomsi andj are covalently bonded,bij = 1,
otherwisebij = 0.dideal
ij is the sum of covalent radii of atomsi,j, anddij =∥x i−xj∥2.δbond = 0.2Å is a
tolerance margin.
Collision loss.Collisions are caused when any two non-bonded atoms are close in space. To prevent this,
we minimize:
Lcollision(X;a) =
mX
i=1
max
j̸=i,Bij=0
(max(0,(d ideal
ij +p collision)−d ij))(7)
Here,pcollision = 0.4Å is a padding distance to prevent over-penalization of near-contact atoms. Together,
the resulting validity log-likelihood of an ensemble of conformations is given by
logp(B|X,a) =−
nX
k=1
(λbondLbond(Xk;a) +λ collisionLcollision(Xk;a))(8)
D.2.3 Relaxation
Despite being regularized with loss functions that prevent collision and bond-violation, some minor clashes
can still persist. Hence, all outputs of Fold’EM are relaxed using AMBER14 force field (Hornak et al., 2006)
in vacuum, in order to relax nucleic acids too. The energy of the structures is minimized for a maximum of
2000iterations with an energy tolerance threshold of2.39 kcal/moland stiffness of10.0 kcal/mol/Å
2
D.2.4 Metrics
Cα Root mean square deviation (Cα RMSD).Given a structure X generated by Fold’EM, we measure
its structural accuracy relative to the experimentally resolved structure Xexpt using the RMSD over matched
Cα atoms. We first align X to Xexpt using the optimal rotation Rkabsch and translation tkabsch obtained by
Kabsch rigid-body alignment (Kabsch, 1976). We then compute,
RMSDCα =
vuut 1
NCα
mX
i∈ICα
·|Rkabschxi +t kabsch−x expt
i |2
2
whereI Cα denotes the set of matchedCαatoms andN Cα =|I Cα|.
40

Template Modeling score (TM-score).For a Fold’EM generated structureXand experimental structure
Xexpt, the Template Modeling score (TM-score) measures the global structural similarity (Zhang and
Skolnick, 2004). In contrast to RMSD, the TM-score is less sensitive to a small number of large local
deviations. It is defined as
TMScore = max
R,t
1
Lref
LaliX
i=1
1
1 +

di(R,t)
d0(Lref)
2,(9)
where Lref is the number of residues in the reference structure, Lali is the number of aligned residues
anddi(R,t) is the distance between theith pair of aligned Cα atoms after rigid-body superposition. The
length-dependent normalization is given by
d0(Lref) = 1.24(Lref−15) 1/3−1.8Å.(10)
TM-scores lie in(0,1]. Larger values indicate greater structural similarity.
MolProbity scores.We assess stereochemical quality using phenix.molprobity (Williams et al.,
2018). We report the MolProbity score, clashscore and percentage of Ramachandran outliers. The clashscore
is the number of serious all-atom steric overlaps per 1000 atoms. The Ramachandran outlier percentage is
the fraction of residues whose backbone ϕ andψ angles fall outside the allowed regions of the reference
Ramachandran distributions. The MolProbity score is a composite measure combining all-atom clashes,
side-chain rotamer outliers and Ramachandran statistics. Lower scores indicate better stereochemical quality.
Fourier shell correlation= 0.143 .For atomic models generated by Fold’EM, Fold’EMab initio, Al-
phaFold3, and obtained from the PDB, we report the resolution (Å) at which the Fourier shell correlation (FSC)
curve wrt the experimental mapρ from EMD crosses the 0.143 threshold, following the commonly used FSC
criterion for cryo-EM resolution assessment (Rosenthal and Henderson, 2003). We use phenix.map_box
to compute the FSC curve and determine the corresponding resolution at the0.143threshold.
D.3 Cryo-EM image formation model and likelihood function
Given a particle image y, its log-likelihood given a conformation X and poseϕ can be written as logp(y|
X,ϕ) = logp(y|y c(X,ϕ)) , where yc is the simulated noiseless particle image and logp(y|y c) is the
noise log-likelihood.
D.3.1 Image formation model
Given an atomic structure X={(x i,ei)}m
i=1, where xi∈R 3 is the position and ei the chemical element
of atom i, we approximate its electrostatic potential as a superposition of atomic potentials, ρX(r) =Pm
i=1ρei(r−x i). Each atomic potential is specified by its electron scattering factorfe, which we identify,
up to the conventional proportionality constant, with its Fourier transform,bρe(ξ) =f e(∥ξ∥). The Fourier
representation of the molecular potential is therefore
bρX(ξ) =
mX
i=1
fei(∥ξ∥) exp

−2πiξ⊤xi

,(11)
withξ denoting the 3D spatial frequency. For a poseϕ= (R,t) , with R∈SO(3) and in-plane translation
t∈R 2, we define the projection operatorPϕ projecting the density onto a plane oriented atϕ. We express the
41

projection in the Fourier domain through the slice theorem: projection of a rotated 3D potential corresponds
to sampling a central plane of its 3D Fourier transform. Letω= (ω 1,ω 2)⊤ denote a 2D spatial frequency.
We define the pose-dependent slice operator
(Sϕbρ)(ω) =e−2πiω⊤tbρ

R⊤
ω
0

,(12)
where the rotation selects the corresponding central Fourier plane and the translation appears as a phase ramp.
The noiseless particle image is formed by further applying the known contrast transfer function (CTF),G(ω),
in the Fourier domainbyc(X,ϕ)(ω) =G(ω) (S ϕbρX) (ω), or in the real space yc(X,ϕ) =F −1 [GSϕbρX].
Known particle-specific imaging parameters, including the CTF, are suppressed fromϕ throughout the paper;
they can equivalently be included among the nuisance variables introduced above.
D.3.2 Noise model and likelihood function
The fundamental electron-detection noise is shot noise and is therefore Poisson at the level of individual
electron counts. The particle images used for reconstruction, however, are processed rather than raw counting
measurements: detector response, frame integration, motion correction, dose weighting, gain correction,
background subtraction, normalization, and other sources of experimental uncertainty make a simple pixelwise
Poisson model inappropriate for the resulting images. As is standard in likelihood-based single-particle
cryo-EM reconstruction (Scheres, 2012), we therefore model the residual image noise as additive Gaussian
noise, allowing its variance to depend on spatial frequency.
Specifically, let yc denote a candidate noiseless particle image and assume additive Gaussian noise in the
Fourier domain,by= byc +bN. We follow the community practice and model each Fourier coefficient ofbN as
an independent zero-mean complex Gaussian with frequency-dependent varianceσ2(ω). The corresponding
noise log-likelihood is, up to an additive constant,
logp(y|y c) =− 1
2
X
ω∈Ω
|by(ω)− byc(ω)|2
σ2(ω) .(13)
The Gaussian model should be understood as an effective likelihood for processed cryo-EM particle images
rather than as a model of the underlying electron-arrival process. In practice, we do not optimize this Gaussian
log-likelihood directly. Instead, we use a band-limited normalized correlation between the observed and
simulated particle images in Fourier space,
Lcorr(y,yc) = Re
P
ω∈Ωby(ω)byc(ω)∗
pP
ω∈Ω|by(ω)|2pP
ω∈Ω|byc(ω)|2 +ϵ ,
where Ω ={ω:k min≤∥ω∥ 2 < kmax + 1} is the frequency band used for guidance and ϵ is a small
numerical stabilizer. Maximizing this objective is equivalent to minimizing squared error between the
observed and simulated Fourier images after normalizing both to unit norm. It can therefore be viewed as a
scale-invariant surrogate for the Gaussian image log-likelihood.
We use this surrogate because the overall amplitude and contrast of experimental cryo-EM particles can
vary for reasons that are not informative about molecular structure. The normalization removes sensitivity
to such global scale differences and makes the guidance depend primarily on agreement in the spatial-
frequency content and phase structure of the particle. Restricting the comparison to Ω further excludes
very low frequencies dominated by background and normalization effects, as well as high frequencies
with little reliable signal. Compared with the full Gaussian likelihood, this objective discards explicit
frequency-dependent noise weighting in favor of a simpler and empirically more robust similarity measure
for inference-time optimization.
42

D.3.3 Particle image rendering from atomic structure
We implement the image-formation model of Section D.3.1 directly from the atomic structure X=
{(xi,ei)}m
i=1, approximating the atomic potentialρ ei of atomiby an isotropic Gaussian with amplitudeZ i,
the atomic number of elementei. Witha the pixel size in Å/pixel, the Gaussian width is set by the Nyquist
resolution2a,σ= 2a/(
√
2π), that is,σ px =σ/a=
√
2/π≈0.45pixels.
Because integrating an isotropic 3D Gaussian along the viewing axis yields a 2D Gaussian of the same
width, the projection can be evaluated analytically without constructing an intermediate 3D voxel grid. For a
poseϕ= (R,t) , with R∈SO(3) and in-plane translation t∈R 2 measured in pixels, atomi is rotated into
the camera frame, ˜xi =R⊤xi, and its projected center, in pixel coordinates relative to the image center, is
ci =a−1(˜xi,1,˜xi,2)⊤ +t. The projected atomic centers define the continuous 2D projection
Pϕ(X)(r) =
mX
i=1
Zi exp

−∥r−c i∥2
2
2σ2px

,
wherer= (u,v) ⊤ denotes image-plane coordinates in pixels.
Each Gaussian is integrated over the finite pixel area. Since the isotropic 2D Gaussian is separable, the
integral factorizes into two one-dimensional Gaussian integrals, and for a pixel centered at coordinatep and a
Gaussian centered atcthe one-dimensional integral has the closed form
g(p;c) =
Z p+ 1
2
p− 1
2
exp

−(u−c) 2
2σ2px

du=σ px
rπ
2
"
erf
 
p+ 1
2−c√
2σpx
!
−erf
 
p− 1
2−c√
2σpx
!#
,
witherf(x) = 2√π
Rx
0 e−t2
dtthe error function. The rendered value at pixel(p,q)is therefore
Iϕ[p,q] =
mX
i=1
Zig(p;ci,1)g(q;c i,2).
D.3.4 Contrast transfer function
We assume the CTF parameters of each particle to be known, model contrast transfer under the weak-phase
approximation (Wade, 1992), and use the CTF parameterization of Rohou and Grigorieff (2015). For a
two-dimensional spatial frequencyω= (ω x,ωy)⊤, lets=∥ω∥ 2, measured in Å−1, andθ= atan2(ω y,ωx).
To account for astigmatism, the defocus is parameterized by two principal defocus valuesdu anddv and their
orientationθd, so that the effective defocus at Fourier-space angleθis
df(θ) = 1
2 [du +dv + (du−dv) cos (2(θ−θ d))],
which reduces to a rotationally symmetric CTF with a single defocus value whendu =d v.
The CTF phase is
γ(ω) = 2π

−1
2df(θ)λs2 + 1
4Csλ3s4

−φ,
whereλ is the electron wavelength,Cs the spherical aberration coefficient andφ the phase shift, and the CTF
is
G(ω) =
p
1−w 2 sin (γ(ω))−wcos (γ(ω)),
withw the amplitude-contrast fraction. The electron wavelength is determined by the accelerating voltageV
through the relativistic de Broglie relationλ(V) =hc/
p
eV(eV+ 2m ec2), whereh is Planck’s constant,e
43

the elementary charge,me the electron rest mass andc the speed of light. WithV in volts andλ in Å, this is
λ(V) = 12.2642598/
p
V(1 + 9.78475598×10 −7V).
Following the image-formation model of Section D.3, the CTF is applied in the Fourier domain. With
bIϕ(ω) the Fourier transform of the rendered projection of the previous section, the simulated noiseless particle
isbyc(X,ϕ)(ω) =G(ω) bIϕ(ω), and the real-space image is obtained by inverse Fourier transformation. For
phase-flipped experimental particle stacks, we apply the magnitude|G(ω)| rather than the signed CTFG(ω),
to match the preprocessing of the observed images.
D.4 B-RECOV AR: bootstrap-aggregated RECOV AR class assignment
In theab initioheterogeneous setting, Algorithm 1 requires an initial class assignment c(0) = (c (0)
k )K
k=1
forη(0), inferred directly from the particle images (Section 3.1). Standard low-dimensional embeddings,
including cryoDRGN latent coordinates and principal components of the RECOV AR volume covariance,
can be unreliable when few particles are available per class. Nuisance variation, such as continuous motion,
defocus variation, and specimen-preparation effects, can have variance comparable to the structural signal of
interest, and the leading covariance directions may therefore depend strongly on the sampled particles.
We therefore use B-RECOV AR, a bootstrap-style, subsampled ensemble for class initialization. Each
replicate estimates a low-dimensional residual subspace by pose-aware regularized back-projection, clusters
the resulting particle coefficients, and refines the labels by cross-validated comparison with class recon-
structions. Replicate labelings are then aggregated by spectral voting, and the normalized voting margin is
reported as a particle-level confidence score.
Model and notation.Let Y={y k}K
k=1 denoteK particle images drawn from a mixture of n discrete
conformations with densitiesρ1,...,ρ n, mixing proportionsπ1,...,π n>0 ,Pn
j=1πj = 1, and class labels
ck∈{1,...,n} . Posesϕk and CTFsGk are obtained from a preceding consensus refinement and registered
to a common coordinate system. The labels are unknown, and the procedure uses no reference structures or
atomic models.
We restrict volumes to the Fourier shells Ωa ={ξ:k min ≤ ∥ξ∥2 < kmax} and images to the
corresponding central-plane coefficients: the lowest-frequency shells are dominated by global contrast and
normalization, whereas the highest-frequency shells are noise-dominated. On this band, the imaging operator
for particle k is Ak =G kSϕk, whereSϕ is the central-slice operator of Equation 12, and we assume
yk =α ⋆
kAkρck +εk, withα⋆
k >0 a particle-specific intensity scale andεk zero-mean noise, independent
across particles and approximately white onΩ a.
Residual subspace.Define the mixture mean ¯ρ=Pn
j=1πjρj and the class deviationsδj =ρ j−¯ρ. SincePn
j=1πjδj = 0, the class deviations span a space of dimension q= dim span{δ 1,...,δ n}≤n−1 . Let
U1,...,U q be a basis of this space and writeδj =Pq
m=1bjmUm. After relative intensity normalization and
consensus subtraction, the residual of particleksatisfies
rk≈
qX
m=1
bckmAkUm +ε′
k,(14)
where any common scale is absorbed into the modes Um, andε′
k includes measurement noise and scale-
estimation error. Thus, particles from class j have a common mean coefficient vector bj ∈R q, and if
q=n−1 , these vectors form the vertices of an (n−1) -simplex. For n= 2 , the subspace is spanned by
∆ρ=ρ 1−ρ 2, withδ1 =π 2∆ρ andδ2 =−π 1∆ρ, and the coefficient sign distinguishes the two classes
up to a global label exchange. For a balanced two-state mixture,∥δ1∥=∥δ 2∥, so the residual energy alone
carries no class information.
44

For a particle subsetK, define the regularized back-projection
R
 
{(νk,dk)}k∈K

=
X
k∈K
νkA∗
kAk +λ wI
−1X
k∈K
A∗
kdk,
and let M denote multiplication in real space by a smooth solvent mask derived from the consensus
reconstruction. Using all particles, we form the consensus ˜ρ=R({(1,y k)}K
k=1), the scales ˜αk =
Re⟨yk,Ak ˜ρ⟩/∥Ak ˜ρ∥2, the normalized images ˇyk = ˜α−1
k yk, and the residuals rk = ˇyk−A k ˜ρ. The
scale normalization makes the class coefficients comparable across particles.
We seek masked modesW1,...,W q and coefficient vectors˜bk∈R q through the constrained factorization
minimize
{Wm},{˜bk}
∥˜b·m∥2=1,m=1,...,q
KX
k=1

rk−
qX
m=1
˜bkmAkWm

2
+λ w
qX
m=1
∥Wm∥2.
The normalization removes the scale ambiguity between a mode and its coefficients. The modes are
identifiable only up to a change of basis of the subspace, and the class labels only up to a permutation. For
n= 2 , omitting the mask yields a rank-one, one-dimensional RECOV AR fit without noise correction (Gilles
and Singer, 2025). The smooth mask allows for variance reduction, as it suppresses solvent-dominated
contributions, provided that it contains the class-specific density.
We estimate the factorization by greedy masked alternating least squares with deflation. LetI be the
particle subset used to fit one replicate; for a single full-data fit, I={1,...,K} . Set r(0)
k =r k. For
m= 1,...,q, we initializea Im = (akm)k∈I as a random unit vector and iterate
Wm←MR
 
{(a2
km,akmr(m−1)
k )}k∈I

,
akm←⟨r(m−1)
k ,AkWm⟩
∥AkWm∥2 ,a Im← aIm
∥aIm∥2
, k∈I.
After the final update, we recompute the unnormalized coefficients ˇakm =⟨r (m−1)
k ,AkWm⟩/∥AkWm∥2
and deflate, r(m)
k =r (m−1)
k −ˇakmAkWm, fork∈I . Once all modes are fitted, the coefficients of every
particle are estimated jointly from the original residual, ˜bk = arg minb∈Rq∥r(0)
k −Pq
m=1bmAkWm∥2,
k= 1,...,K . Under Equation 14, the expected coefficient vector depends on the class but not on the pose,
up to the fitted change of basis. We cluster{˜bk}K
k=1 byk-means withn clusters and multiple initializations.
Forn= 2 , we cluster the standardized scalar ˜bk1∥AkW1∥, whose noise variance is approximately constant
across particles.
Cross-validated refinement.At each refinement iteration, we partition the particles into two folds J
andJ′ and, given the current labels{˜ck}, reconstruct one masked volume per class from each fold, ˜ρF
j =
MR({(1, ˇyk)}k∈F,˜ck=j) forF∈{J,J ′}. For k∈F , we score classj against the reconstruction from
the opposite foldFc,skj =L corr(ˇyk,Ak ˜ρF c
j ), whereLcorr is the band-limited normalized correlation of
Section D.3 evaluated on Ωa, and center the scores of each class within the fold, ¯sF
j =|F| −1P
k′∈Fsk′j.
We then update
˜ck←arg max
j∈{1,...,n}
 
skj−¯sF
j

, k∈F.(15)
Cross-validation avoids direct self-correlation between a particle and a reconstruction containing its noise, and
the fold-specific centering compensates for class-dependent score offsets caused by unequal reconstruction
precision. The refinement requires sufficient particles from every current class in both folds.
45

Ensemble voting.With few particles per conformation, a single residual-subspace fit can be unstable even
forn= 2 : different initializations and particle samples may recover a nuisance direction with explained
energy comparable to that of the class mode. The class subspace, however, should recur across particle
subsamples and frequency bands containing structural signal, whereas sample-specific nuisance directions
are less stable. We therefore fitB randomized replicates of Algorithm 2, each with a particle subsetIb, a
selected frequency band, and an independent initialization. Modes are fitted onIb, but coefficients, clustering,
and refinement are evaluated for all particles. Each replicate produces labels {˜c(b)
k }, defined only up to
permutation.
To align the labelings, we select as reference the replicate with the highest mean pairwise agreement and,
for every replicateb, choose the permutationPb that maximizes the trace of its contingency matrix with the
reference, using the Hungarian algorithm (Kuhn, 1955); the aligned labels areˇc(b)
k =P b(˜c(b)
k ).
Forn= 2 , letv(b)
k ∈{−1,+1} encode the aligned vote of replicate b, and let ψb denote its balanced
accuracy relative to the unknown labels. Under conditional independence of replicate errors given the class,
Cov
 
v(b),v (b′)
= (1−β 2)(2ψb−1)(2ψb′−1), b̸=b ′,(16)
whereβ=π 1−π 2. Thus, the off-diagonal covariance entries admit a rank-one factorization. Following
the spectral meta-learner of Parisi et al. (2014), we obtain u∈R B from a spectral rank-one fit to these
entries, orienting it relative to the reference replicate. The weighted vote˜vk =PB
b=1ubv(b)
k defines the binary
assignment by its sign, and κk =|˜vk|/PB
b=1|ub| is the confidence score. A reversed replicate receives a
negative weight, and a chance-level replicate is downweighted. The relative gap between the two leading
eigenvalues of the vote covariance indicates whether the replicates agree on a common split.
Forn>2 , we apply the same meta-learner separately to the aligned one-versus-rest indicatorsv(b)
kj = +1
if ˇc(b)
k =j and−1 otherwise. Let u(j) denote the resulting class-specific weights and define the class scores
¯vkj =PB
b=1u(j)
b v(b)
kj
PB
b=1|u(j)
b |. We assign ˜ck = arg maxj ¯vkj and reportκk = 1
2(¯vk,(1)−¯vk,(2)), where
¯vk,(1)≥¯vk,(2) are the two largest class scores. Class-specific weights allow a replicate that resolves only a
subset of classes to contribute to those classes. Because replicates share particles, consensus maps, and masks,
conditional independence is a working approximation; the margins and eigengaps are therefore diagnostic
confidence measures rather than calibrated probabilities.
Comparison with RECOV AR.RECOV AR and B-RECOV AR both use consensus poses and CTFs, require
no learned network, and infer structural variability from pose-aware volume statistics. RECOV AR estimates
a regularized, noise-whitened volume covariance and embeds particles in a high-dimensional PCA space;
B-RECOV AR instead estimates only then−1 masked, band-limited class-deviation modes from consensus-
subtracted residuals. For n= 2 , this is a rank-one, uncorrected analogue of one-dimensional RECOV AR.
Restricting the fit to the class subspace avoids relying on the leading direction of the full covariance, which
can be dominated by sample-dependent nuisance variation at low particle counts.
B-RECOV AR further stabilizes the assignment by aggregating fits over particle subsamples, frequency
bands, and initializations with the spectral meta-learner of Equation 16; the normalized marginκk provides a
particle-level confidence score. It then applies the cross-fitted refinement of Equation 15, avoiding direct
self-correlation between a particle and its comparison volume. For a matched comparison, both methods
use the same label-free readout and spectral aggregation; only B-RECOV AR uses cross-fitted refinement.
RECOV AR randomizes its half-set split and downsampled box, whereas B-RECOV AR randomizes the
particle subset, frequency band, and initialization.
Implementation details.We use kmin = 3 and kmax∈{24,32,40} Fourier pixels, with q=n−1 .
Although the shells below 16 pixels contribute little directly to class discrimination in our data, they are
46

retained to stabilize the reconstructions. The regularization is λw = 0.1 times the mean diagonal entry ofP
k A∗
kAk. The solvent mask retains the 8% of voxels with the largest values of|F−1ˆρ|and is smoothed
with a Gaussian of standard deviation two voxels; mask fractions between 4% and 15% yield comparable
results.
We useT= 8 alternating updates,B= 24 replicates, and independent 80% particle subsamples; the
three frequency bands are allocated evenly among replicates. The consensus, normalized residuals, and
mask are computed once per band using all particles. Each replicate uses L= 4 refinement iterations.
In the experimental data, with fewer than approximately 5,000 particles per conformation, both the class
direction and competing nuisance directions account for about 1.5% of the residual energy, which motivates
the ensemble aggregation. The dominant computational cost is Bq single-mode fits, approximately 10
CPU-minutes for 104 particles on aD= 128 grid withn= 2 . Replicates can be evaluated in parallel; modes
within a replicate are fitted sequentially because of deflation.
D.5 Hyperparameters and implementation details
We use the following hyperparameters for all experiments.
•k min = 3andk max = 48.
•D= 128pixels.
• Due to memory constraints, at each optimization step, we guide usingmin(|Y|,128)particles.
• Optimizer: Adam (Kingma and Ba, 2015)
• Learning rate:0.06
• Max gradient norm:0.6
•λ bond = 10−3 andλ collision = 0.09
•R(number outer iterations) was3for real examples and5for synthetic examples.
• On the prior term.In the formulation from Maddipatla et al. (2026a), the prior logp(Z|a) was
essential: with Z treated as a free variable, nothing else prevented the optimization from drifting into
regions of embedding space that the Pairformer never produces. In the present parameterization this
role is partly assumed by the reparameterization itself, since displacements inH reach the conditioning
variable only throughg and are therefore expressed in the basis of directions the trunk natively realizes.
47
