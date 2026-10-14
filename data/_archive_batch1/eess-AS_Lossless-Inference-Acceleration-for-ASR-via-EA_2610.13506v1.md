# Lossless Inference Acceleration for ASR via EAGLE-Style Speculative Decoding

> **领域**：`eess.AS`　**发布**：2026-10-09　**arXiv**：[2610.13506v1](https://arxiv.org/abs/2610.13506v1)
>
> **作者**：Sen Zhang, Xianghu Yue, Yiming Chen, Wenhuan Lu 等 6 人
>
> **来源**：arXiv 预印本（开放获取）　**页数**：12

---

## Abstract

Autoregressive Transformer and Conformer models have achieved state-of-the-art performance in automatic speech recognition (ASR). However, their sequential token generation mechanism imposes a significant bottleneck during decoding, resulting in substantial inference latency. While speculative decoding has emerged as a promising lossless acceleration technique, existing ASR-oriented approaches either suffer from low draft acceptance rates due to suboptimal draft quality or rely on specially designed external draft models, which limit their generality and practicality. To overcome these limitations, we propose EAGLE-ASR, a novel framework that accelerates ASR inference via EAGLE-style speculative decoding while strictly preserving lossless output quality. Specifically, we introduce Speech-Draft, a lightweight autoregressive module that serves as a universal draft model by jointly leveraging encoder acoustic features and hierarchical decoder representations from the target ASR model. Furthermore, we adopt a multi-step generation strategy with self-distilled data to train the Speech-Draft, enabling it to better approximate the target model's output distribution and maintain causal consistency during multi-token generation. Extensive experiments on representative Whisper and Conformer AED models demonstrate that EAGLE-ASR achieves significant lossless speedups of up to $1.9\times$ and $2.4\times$, respectively, consistently outperforming existing speculative decoding baselines for ASR. Our proposed framework further generalizes effectively to multilingual ASR and speech translation tasks, establishing EAGLE-ASR as a practical and universally applicable solution for accelerating modern ASR systems without compromising recognition accuracy.

---

## 正文（由 PDF 提取）

1
Lossless Inference Acceleration for ASR via EAGLE-Style
Speculative Decoding
Sen Zhang, Xianghu Yue, Yiming Chen, Wenhuan Lu, Jianguo Wei,Senior Member, IEEE,
Haizhou Li,Fellow, IEEE
Abstract—Autoregressive Transformer and Conformer models
have achieved state-of-the-art performance in automatic speech
recognition (ASR). However, their sequential token generation
mechanism imposes a significant bottleneck during decoding,
resulting in substantial inference latency. While speculative de-
coding has emerged as a promising lossless acceleration tech-
nique, existing ASR-oriented approaches either suffer from low
draft acceptance rates due to suboptimal draft quality or rely on
specially designed external draft models, which limit their gener-
ality and practicality. To overcome these limitations, we propose
EAGLE-ASR, a novel framework that accelerates ASR inference
via EAGLE-style speculative decoding while strictly preserving
lossless output quality. Specifically, we introduce Speech-Draft,
a lightweight autoregressive module that serves as a universal
draft model by jointly leveraging encoder acoustic features
and hierarchical decoder representations from the target ASR
model. Furthermore, we adopt a multi-step generation strategy
with self-distilled data to train the Speech-Draft, enabling it
to better approximate the target model’s output distribution
and maintain causal consistency during multi-token generation.
Extensive experiments on representative Whisper and Conformer
AED models demonstrate that EAGLE-ASR achieves significant
lossless speedups of up to 1.9×and 2.4×, respectively, consistently
outperforming existing speculative decoding baselines for ASR.
Our proposed framework further generalizes effectively to mul-
tilingual ASR and speech translation tasks, establishing EAGLE-
ASR as a practical and universally applicable solution for acceler-
ating modern ASR systems without compromising recognition ac-
curacy. Our code is publicly available at https://github.com/ssss-
sen/eagle-asr.
Index Terms—Automatic speech recognition, inference accel-
eration, speculative decoding, EAGLE
I. INTRODUCTION
N
EURAL network models based on Transformer or Con-
former architectures have recently achieved state-of-the-
art performance in automatic speech recognition (ASR) [1]–
[4]. However, these accuracy improvements in transcription
are often accompanied by increasingly large model sizes and
more complex decoding procedures. In particular, autoregres-
sive ASR models generate output tokens sequentially, which
bottlenecks the decoding stage and introduces substantial
inference latency. As ASR systems are increasingly deployed
on resource-constrained edge devices and in high-throughput
Sen Zhang, Xianghu Yue, Wenhuan Lu, and Jianguo Wei are with the Col-
lege of Intelligence and Computing, Tianjin University, Tianjin 300350, China
(email: zhangsen@tju.edu.cn; yuexianghu@tju.edu.cn; wenhuan@tju.edu.cn;
jianguo@tju.edu.cn)
Yiming Chen is with ASUS Intelligent Cloud Services, Singapore 486030
(email: mattymchen@gmail.com).
Haizhou Li is with the School of Artificial Intelligence, The Chinese
University of Hong Kong, Shenzhen, Guangdong 518172, China, also with
the Department of Electrical and Computer Engineering, National University
of Singapore, Singapore 117583 (email: haizhouli@cuhk.edu.cn).
server environments, reducing per-utterance decoding latency
without sacrificing recognition accuracy has become a critical
challenge for the speech processing community [5], [6], [7].
Streaming ASR techniques have demonstrated effectiveness
in reducing end-to-end latency by emitting partial results
before processing the entire audio utterance [8]–[11]. In
this work, however, we focus on accelerating the decoding
stage of autoregressive ASR models under the standard full-
utterance inference setting, which remains crucial for offline
transcription. To improve decoding efficiency in this setting,
various acceleration strategies have been explored, including
model compression [12]–[15] and non-autoregressive (NAR)
decoding [16]–[20]. Model compression techniques aim to
reduce computational cost and memory footprint by construct-
ing smaller or more efficient variants of large-scale models.
On the other hand, NAR decoding attempts to mitigate the
latency of sequential generation by predicting multiple tokens
in parallel. Although these methods can reduce inference cost,
they often require architectural modification or may sacrifice
recognition accuracy for decoding speed. Therefore, lossless
acceleration techniques for autoregressive ASR models remain
highly desirable.
Speculative decoding has recently emerged as an effective
inference acceleration technique for autoregressive models in
natural language processing (NLP) [21], [22], [23]. It typically
uses a lightweight draft model to generate multiple candidate
tokens, which are then verified in parallel by the target
model. By reducing the number of expensive target-model
decoding steps, speculative decoding can substantially improve
inference speed while preserving the output distribution of the
original model.
Recent studies have explored speculative decoding for
ASR acceleration, but face critical limitations. Some ap-
proaches [12], [24] rely on specially designed external draft
models that must be well aligned with the target ASR model,
increasing implementation complexity and limiting generaliz-
ability. Others [25], [26] generate low-quality drafts, resulting
in poor acceptance rates that constrain achievable speedups.
These limitations motivate the need for an ASR-oriented
speculative decoding framework that generates high-quality
drafts while remaining lightweight and adaptable. EAGLE-
style speculative decoding constructs lightweight draft mod-
ules by leveraging the target model’s internal representations,
thereby eliminating the need for external models [27]–[30].
While this design is highly attractive for ASR, its direct appli-
cation poses non-trivial challenges. Unlike pure text generation
tasks, ASR involves cross-modal conditioning on continuous
acoustic features, where the decoder’s behavior is inherently
arXiv:2610.13506v1 [cs.SD] 9 Oct 2026

2
coupled with encoder representations. A naive adaptation that
ignores acoustic context or decoder–encoder interactions can
result in poor draft quality and reduced acceptance rates,
ultimately undermining the efficiency gains of speculative
decoding [31], [32], [33].
To address these challenges, we propose EAGLE-ASR,
a speculative decoding framework tailored to autoregressive
ASR models. The key component of EAGLE-ASR is Speech-
Draft, a lightweight autoregressive draft module that leverages
both encoder-side acoustic features and hierarchical decoder
representations from the target ASR model. By incorporating
acoustic and decoder-context information, Speech-Draft better
approximates the target model’s token prediction behavior
while maintaining low computational cost, thereby improving
draft acceptance and inference efficiency. Furthermore, we
design a self-distillation and multi-step generation strategy to
train Speech-Draft. This training strategy enables the draft
module to model dependencies among consecutive future
tokens and maintain causal consistency during multi-token
drafting. As a result, EAGLE-ASR can generate multiple
high-quality draft tokens at each decoding step and ver-
ify them efficiently with the target ASR model. We evalu-
ate EAGLE-ASR on representative Whisper and Conformer
attention-based encoder-decoder (AED) models. Experimental
results show that EAGLE-ASR achieves average accepted
draft lengths of 3.67 on Whisper and 4.74 on the Conformer
AED model, demonstrating effective draft generation. It fur-
ther achieves lossless inference speedups of up to 1.9×and
2.4×, respectively, outperforming existing ASR speculative
decoding baselines. Additional experiments also demonstrate
the effectiveness of the proposed framework on multilingual
ASR and speech translation tasks.
The main contribution of this paper can be summarized as
follows.
•We propose EAGLE-ASR, an EAGLE-style speculative
decoding framework for accelerating autoregressive ASR
inference while preserving recognition accuracy.
•We introduce Speech-Draft, a lightweight autoregressive
draft module that leverages encoder acoustic features
and hierarchical decoder representations to generate high-
quality draft tokens for attention-based encoder-decoder
ASR models.
•We develop a self-distillation and multi-step generation
training strategy that improves draft quality and maintains
causal consistency during multi-token speculative decod-
ing.
•Extensive experiments on Whisper and Conformer AED
models demonstrate that EAGLE-ASR achieves signifi-
cant lossless speedups of up to 1.9×and 2.4×, respec-
tively, consistently outperforming existing ASR specula-
tive decoding baselines.
The remainder of this paper is organized as follows: Sec-
tion II summarizes related work. Section III presents the
architecture of Speech-Draft, along with the training and
inference framework of EAGLE-ASR. Section IV describes
the experimental setup, with results provided in Section V.
The paper concludes in Section VI.
II. RELATEDWORK
A. Traditional Inference Acceleration Techniques in ASR
Traditional approaches for accelerating ASR inference
mainly focus on model compression and non-autoregressive
ASR (NAR-ASR). Model compression techniques, such as
knowledge distillation [34], quantization [35], and pruning
[36], reduce computational overhead by decreasing model
size and complexity. Representative works, including Distil-
Whisper [12] and DQ-Whisper [13] achieve faster inference
by using compressed model variants of large ASR models.
However, these approaches often introduce some degree of
information loss, which may lead to degradation in Word Error
Rate (WER). Concurrently, NAR-ASR models [37] attempt
to eliminate the latency inherent in autoregressive decoding
by generating multiple tokens in parallel. Notable approaches
include Mask-CTC [16], Paraformer [17], [18], Align-refine
[19] and A-CMLM [20] models. Despite their improved
decoding efficiency, NAR-ASR approaches generally exhibit
a performance gap compared to autoregressive models in
terms of recognition accuracy. Overall, while these strategies
demonstrate effectiveness in reducing inference latency, they
typically sacrifice recognition performance for speed. This
limitation highlights the need for lossless acceleration methods
that are specifically tailored to autoregressive ASR models.
B. Speculative Decoding
Speculative decoding is a lossless acceleration technique
for large language models that employs a “draft-then-verify”
paradigm. Early speculative decoding methods [38], [39] ac-
celerated generation in greedy settings, while recent advances
[21], [22] introduced speculative sampling to extend this
framework to non-greedy generation. In this paradigm, the
drafting phase incurs minimal computational overhead, while
the verification phase is executed in parallel, corresponding to
draft generation and validation, respectively. In the drafting
phase, a lightweight draft model is employed to autore-
gressively generate tokens, forming a draft sequence while
recording the probabilityˆpfor each token. In the verification
phase, the target model is invoked to evaluate the draft and
record the probabilitypfor each drafted token. Speculative
decoding then sequentially determines the acceptance of each
drafted token with an acceptance probability ofmin(1,p/ˆp).
If the current token is accepted, the process proceeds to the
next token; otherwise, a replacement token is sampled from
the distribution norm(max(0,p−ˆp)), and subsequent tokens
in the draft are discarded [40], [41]. Crucially, Leviathan et
al. [21] proved that speculative decoding is consistent with the
distribution of vanilla autoregressive decoding. Building upon
this foundation, numerous variants have emerged in the NLP
domain, including CS Drafting [42], BiLD [43], LLMA [44],
and REST [45], each exploring different strategies for draft
generation and verification.
Unlike conventional speculative decoding approaches that
rely on separate, independent draft models, Medusa [46]
and EAGLE [27], [28], [29] adopt an internally integrated
speculative decoding strategy, which aims to directly leverage

3
the feature extraction capability of the target model itself for
draft generation.
Specifically, Medusa attaches multiple lightweight MLP
heads on top of the frozen target model, utilizing the hidden
states at the current time step to predict candidate tokens
for the subsequentkpositions in parallel. However, because
these heads predict each position independently, the approach
fails to capture the sequential dependencies among the drafted
tokens. Consequently, each later token is generated without
conditioning on its immediate predecessor, resulting in less
coherent draft sequences and a diminished acceptance rate
during the verification phase.
In contrast to Medusa’s multi-head design, EAGLE attaches
only a single lightweight autoregressive module to the frozen
target model, leveraging semantic information from different
layers of the target model for prediction. By maintaining an
explicit autoregressive structure, this design preserves tempo-
ral dependencies during draft generation while more effec-
tively leveraging the target model’s learned representations.
Empirically, EAGLE has been reported to achieve state-of-
the-art decoding speed among existing speculative decoding
approaches.
C. Speculative Decoding in ASR
Current research on accelerating ASR models through spec-
ulative decoding still largely focuses on selecting or training
a separate draft model. For instance, the Hugging Face team
employs Distil-Whisper and Whisper-tiny as draft models to
accelerate the inference of the Whisper-large target model [12].
However, such approaches rely heavily on strict distribution
alignment between the draft and target models, typically
requiring them to belong to the same model family or the
draft model to be a distilled variant of the target. This con-
straint significantly limits architectural flexibility and practical
deployment. When this assumption is violated, such as when
pairing a Distil-Whisper draft model with a Conformer-based
target model, the token acceptance rate can degrade substan-
tially, thereby diminishing or even negating the anticipated
speedup.
Whisper-Medusa partially alleviates the cost of obtaining a
well-aligned draft model by appending multiple MLP heads
on top of a Whisper model [25]. However, constrained by the
inherent limitations of the Medusa framework, this approach
similarly neglects temporal dependencies and underutilizes the
rich intermediate representations extracted by the target model,
particularly the acoustic features derived from the encoder.
Consequently, its overall acceleration ratio remains limited.
Moreover, since Whisper-Medusa fine-tunes the final decoder
layer during training rather than freezing all parameters of the
target model, its WER exhibits noticeable degradation, thus
failing to achieve lossless acceleration.
To address these limitations, we propose EAGLE-ASR,
an EAGLE-style speculative decoding framework tailored for
accelerating the inference of the ASR model. Unlike existing
approaches, EAGLE-ASR eliminates the need for an indepen-
dently trained draft model while delivering superior decoding
speedups and strictly preserving lossless output quality.
III. METHODOLOGY
A. Overview
In this work, we propose EAGLE-ASR, an EAGLE-style
speculative decoding framework designed to accelerate autore-
gressive ASR inference while maintaining lossless recognition
accuracy. As illustrated in Figure 1, EAGLE-ASR is built upon
a frozen target ASR model consisting of an encoder and an au-
toregressive decoder, augmented with a lightweight autoregres-
sive module termed Speech-Draft and a dedicated speculative
decoding pipeline. Unlike conventional speculative decoding
methods that rely on standalone external draft models, Speech-
Draft directly leverages the internal representations of the
target ASR model for draft generation, thereby improving
target-draft consistency while maintaining low computational
overhead. Similar to standard speculative decoding, EAGLE-
ASR alternates between a drafting stage and a verification
stage during inference. Specifically, given the input audio and
the sequence prefixt 1:t−1, to generate multiple tokens in
parallel, the inference process of EAGLE-ASR proceeds as
follows, as depicted in the lower part of Figure 1.
Drafting stage:During draft generation, the target ASR
model first processes the input audio to predict the next
token ˆtt. Meanwhile, the encoder featuresf encoder are cached,
and decoder representations at different levels, denoted as
flow,f middle, andf high, are extracted from the target decoder.
These multi-granularity features, together with the predicted
token ˆtt and the sequence prefixt 1:t−1, are then fed into the
Speech-Draft, which autoregressively generatesKdraft tokens
following the EAGLE framework [27].
•In the initial draft stepk= 1, the Speech-Draft takes as
inputf encoder,f low,f middle,f high, and the concatenated se-
quence[t 2:t−1, ˆtt], where the newly predicted token from
the target model is appended to the input sequence shifted
one step ahead. Based on this information, Speech-Draft
generates the first draft token ˆtt+1.
•In the subsequent draft stepk >1, the Speech-Draft
operates in an autoregressive manner. Specifically, it
predicts thek-th draft token conditioned on the encoder
representationsf encoder, the hidden state output from the
previous drafting step ˆht+k−2, and the previously gener-
ated drafted token ˆtt+k−1.
AfterKrecursive steps, a complete draft sequence ˆtt+1:t+K
is obtained.
Verification stage:During verification, all drafted tokens
are fed into the target decoder in parallel, which simultane-
ously computes the logits for positionst+1throught+K. We
adopt the standard speculative decoding acceptance criterion
to determine the accepted draft tokens, where drafted tokens
are accepted sequentially until the first position at which the
draft token differs from what the target model would have
sampled. Through this parallel verification without approxi-
mate strategies, Eagle-ASR ensures that the output distribution
remains identical to that of the target model, thereby achieving
acceleration in a lossless manner. In subsection V-D, we
further investigate the impact of different verification strategies
on acceleration performance. Experimental results show that

4
Encoder
encoder
Inference
...1t 1-tt2t
Decoder
tˆt
Target
Model
Speech-
Draft
...2t 3t
high
middle
low
Speech-
Draft ...
Shared 
Weight
tˆt
1tˆ t
1tˆ t
2tˆ t
Verify in parallel
...
t
ˆh
Encoder
encoder
Training
...1t Tt2t
Decoder
... 1Tˆ t
Target
Model
... Tt2t
2ˆt Tˆt
Labels
Speech-
Draft
shift ...2t Tt3t
high
middle
low
shift
... 1Tˆ t3ˆt Tˆt
1Tt ... Tt3t 1Tt
1
mtpL
Speech-
Draft
...3t Tt4t
... 1Tˆ t4ˆt Tˆt
... Tt4t 1Tt
2
mtpL
shift
shift
...
Shared 
Weight
t:2h
Fig. 1. Pipeline of EAGLE-ASR.Training phase (upper):The Speech-Draft model is trained using a multi-token generation strategy together with a weighted
cross-entropy loss with exponential decay. During training, only the FC layers and the Transformer decoder block of the Speech-Draft are fine-tuned, while
remaining parameters of the Speech-Draft, as well as all parameters of the target model, are kept frozen.Inference phase (lower):The target model predicts
the next token, which feeds into the Speech-Draft serving as the draft model, thereby recursively generating draft tokens for subsequent parallel verification.
linear verification yields a better speedup than tree-based
verification in the ASR setting.
B. Speech-Draft Module
Unlike standard language models, the autoregressive de-
coding in ASR exhibits a dual dependency, requiring both
historical text context and acoustic representations produced
by the encoder. Motivated by this observation, we propose
Speech-Draft, a lightweight autoregressive module that ef-
fectively integrates acoustic and textual information to serve
as the draft model in EAGLE-ASR. The overall architecture
of the Speech-Draft is illustrated in Figure 2. The Speech-
Draft module consists of two fully connected (FC) layers, an
embedding layer, a single Transformer decoder block, and an
LM head. Notably, the embedding layer and the LM head
directly reuse the corresponding parameters of the target model
and require no additional training.
The first FC layer is activated only at the first decoding
step (step= 1), where it fuses the multi-level decoder rep-
resentations (f low,f middle, andf high) extracted from the target
model into a unified representationf mixed, thereby aggregating
hierarchical information from different depths. The second
FC layer then combinesf mixed (or the hidden states from
the preceding step when step>1) with the embeddings of
previously generated tokens, producing the input represen-
tation for the Transformer decoder block. To maintain strict
alignment with the input speech signal, the encoder acoustic
...
 FC Layer
tˆt1t 1-tt
 Embedding
mixed 1:t
FC Layer
concat
LM Head
1tˆ t
high
middle
low
concat
Transformer Decoder Block
encoder
self attention
cross attention
MLP
Speech-Draft
step 1
 Embedding
t+1
FC Layer
LM Head
Transformer Decoder Block
self attention
cross attention
MLP
concat
...
step 2
Shared
Weight
2t 1tˆ t
2tˆ t
t
ˆh 1t
ˆ
h
Speech-Draft
Fig. 2. The overall architecture of the Speech-Draft, which consists of two
fully connected (FC) layers, an embedding layer, a Transformer decoder block,
and an LM head.
representationf encoder is incorporated into the drafting process
through the cross-attention mechanism of the Transformer
decoder block. This design enables Speech-Draft to jointly
leverage rich decoder-side semantic representations and fine-

5
Audio:
Text: percy my husband for 
god's sake fly armand 
armand why don't you fire
Audio:
Text: <|en|><|transcribe|> 
<|notimestamps|> Percy, my 
husband, for God's sake, fly! 
Armin, Armin, why don't 
you fire?
Self-Distillation 
via Rewriting
Target
Model
Original Dataset
 Distilled Dataset
Fig. 3. An illustration of self-distilled training data generation, designed to
mitigate the distributional discrepancy between the original transcripts and the
target model outputs.
grained encoder-side acoustic information, thereby improving
draft quality for subsequent verification. It is worth noting that,
owing to its lightweight and model-agnostic architecture, the
Speech-Draft module can be seamlessly integrated into any
autoregressive ASR system that employs a Transformer-based
decoder, including state-of-the-art models such as Whisper and
Conformer AED models.
C. Self-Distilled Training Data
As illustrated in Figure 3, there is a distribution discrepancy
between the output distribution of the target ASR model and
the original distribution of the training data transcriptions.
This discrepancy arises from factors such as prediction errors,
inaccurate annotations, and inconsistencies in transcription
conventions. Training Speech-Draft directly on the original
transcriptions may therefore lead to suboptimal target-draft
alignment, ultimately limiting speculative decoding perfor-
mance.
To address the above issue, we adopt a self-distillation
approach for training data generation [47]. Specifically, the
target ASR model is first used to generate transcriptions for
all training audio samples, and these generated transcriptions
are subsequently used as the training targets for Speech-
Draft. For the Whisper model, we explicitly preserve its
special tokens, such as<|en|>,<|transcribe|>, and
<|notimestamps|>. The resulting self-distilled training
data effectively captures the generation patterns and prefer-
ences of the target model. By training Speech-Draft on these
self-distilled transcriptions rather than on the original annota-
tions, the draft module learns to produce draft tokens that are
consistent with the behavior of the target model, instead of
attempting to imitate transcriptions from external sources that
may exhibit a different distribution. As a result, Speech-Draft
can better match the target model during speculative decoding,
leading to a higher token acceptance rate and a more effective
drafting process.
D. Training Strategy
During training, EAGLE-ASR updates only the trainable
components of Speech-Draft, namely the FC layers and the
Transformer decoder block. The remaining parameters of
Speech-Draft, including the reused embedding layer and LM
head, as well as all parameters of the target ASR model, are
kept frozen. This strategy ensures computational efficiency
during training while fully preserving the capabilities of the
target model.
During actual speculative decoding, however, Speech-Draft
faces a training–inference mismatch. Specifically, at the second
and subsequent drafting steps, Speech-Draft must rely on
its own predicted hidden states rather than the ground-truth
hidden states produced by the target model. This discrepancy
can lead to error accumulation during recursive drafting,
resulting in a degradation in acceptance rate. To alleviate this
issue, EAGLE-ASR adopts a multi-step generation strategy
for training Speech-Draft, as illustrated in the upper part of
Figure 1. Specifically, suppose that EAGLE-ASR employs
Speech-Draft to performK-step generation during training.
Given an input speech audio and its corresponding transcrip-
tion token sequencet 1:T (whereTdenotes the sequence
length), the training procedure of EAGLE-ASR is illustrated
as follows.
•At stepk= 1, the Speech-Draft leveragesf encoder,f low,
fmiddle, andf high from the target model, along with the
shifted token sequencet 2:T (shifted by one position), to
predict ˆt3:(T+1) .
•At stepk >1, the Speech-Draft utilizesf encoder and
the output hidden states ˆhk:T from the preceding step,
together with the shifted token sequencet (k+1):T (shifted
bykpositions), to predict ˆt(k+2):(T+1) .
As the generation depth increases, distant tokens condition
on a growing number of intermediate decisions, resulting in
progressively higher prediction difficulty. Consequently, the
prediction uncertainty accumulates with each successive step.
To mitigate this issue, we optimize the Speech-Draft using a
weighted cross-entropy loss with exponential decay:
Lmtp =
KX
k=1
αk ·Lk
mtp =
KX
k=1
αk ·CE
 ˆtk
1+k:T+1, t1+k:T+1

(1)
whereL mtp
k represents the loss at thek-th step, and CE(·,·)
denotes the cross-entropy loss between the predicted token
and the ground-truth label. The position-dependent weightα k
follows an exponential decay, formulated as:
αk = βk−1
PK
j=1βj−1
(2)
whereβdenotes the decay factor. Through this loss formula-
tion, EAGLE-ASR prioritizes the accuracy of near-term pre-
dictions while simultaneously enhancing its ability to generate
multiple consecutive future tokens.
IV. EXPERIMENTALSETUP
A. Datasets
We use two datasets to train and evaluate the proposed
EAGLE-ASR framework. First, we adopt LibriSpeech, a
widely used benchmark in ASR research [48]. LibriSpeech
contains approximately 1,000 hours of read English speech
derived from audiobooks in the public domain. In this work,
we use the full 960-hour LibriSpeech training split to train

6
the Speech-Draft module and report evaluation results on the
standard test-clean and test-other subsets. Moreover, to further
evaluate the generalizability of EAGLE-ASR on both multi-
lingual ASR and speech translation (ST) tasks, we conduct
additional experiments on the V oxPopuli dataset [49]. V ox-
Populi is a large-scale multilingual speech corpus derived from
European Parliament event recordings between 2009 and 2020.
It comprises approximately 400,000 hours of unlabeled speech
data covering 23 languages, as well as around 1,800 hours
of transcribed speech data in 16 languages. For multilingual
ASR evaluation, we use the English, German, Spanish, French,
and Italian subsets. For the ST task, we conduct experiments
on four translation directions: German-to-English, Spanish-to-
English, French-to-English, and Italian-to-English.
It is worth noting that, although both LibriSpeech and
V oxPopuli subsets used in our experiments provide paired
reference transcripts for all audio samples, we do not directly
use these human-annotated transcriptions for training. Instead,
we train the Speech-Draft exclusively on self-distilled data
generated by the target model, as described in subsection III-C.
B. Model Configurations
To validate the effectiveness and generality of EAGLE-
ASR, we adopt two representative autoregressive ASR models,
Whisper and Conformer AED, as our target models [1], [2].
Whisper is a Transformer-based ASR model developed by
OpenAI, trained on approximately 680,000 hours of audio
data. Owing to its strong robustness and competitive recog-
nition performance across diverse speech conditions, Whisper
has become a widely adopted backbone for ASR research.
In this work, we adopt Whisper-large-v3 as the target model
for EAGLE-ASR. This model consists of a 32-layer Trans-
former encoder and a 32-layer Transformer decoder, with
approximately 1550M parameters in total. Conformer AED is
a hybrid encoder-decoder model based on the CTC/attention
architecture. In this work, we adopt the Conformer AED
implementation provided by the FunASR toolkit [50] as the
target model for EAGLE-ASR. This model is trained on ap-
proximately 50,000 hours of English audio data and comprises
a 32-layer Conformer encoder and a 16-layer Transformer
decoder, with approximately 220M parameters in total. Since
our study focuses on autoregressive decoding, the CTC branch
is not used in inference.
C. Training Details
For the Whisper model, Speech-Draft is trained for 200K
and 400K steps on the LibriSpeech and V oxPopuli datasets,
respectively. For the Conformer AED model, Speech-Draft is
trained for 150K steps on LibriSpeech and 300K steps on
V oxPopuli. Across all experiments, we employed the AdamW
optimizer [51] with beta values(β 1,β 2) = (0.9,0.95), to-
gether with a gradient clipping of0.5. A cosine learning rate
schedule is adopted with a peak learning rate of5×10 −5 and
a warmup ratio of0.05[52]. The batch size is set to2with4
gradient accumulation steps, yielding an effective batch size of
8. For the multi-step generation training strategy, we adopt a
weight decay factorβ= 0.8and prediction depthK= 7. All
evaluations were conducted on a single NVIDIA RTX 4090
GPU with 24 GB of memory.
D. Evaluation Metrics
Since EAGLE-ASR does not modify the parameters of the
target model and adopts strict speculative decoding acceptance
conditions [23], [53], its decoded outputs are theoretically
identical to those produced by the original target model. To
empirically verify this lossless property in practice, we report
∆WER, which measures the change in WER of EAGLE-ASR
relative to the original target model. A∆WER greater than
0indicates that the decoding method incurs a degradation in
recognition accuracy. Similarly, for ST tasks, we report the
change in BLEU score [54], denoted as∆BLEU, to measure
the change in translation quality relative to the original model.
In addition to∆WER, we further adopt the following
metrics to evaluate the acceleration performance:
(1) Speedup ratio: The relative inference speedup compared
to the baseline (vanilla autoregressive decoding).
(2) Mean accepted length (τ): The average number of draft
tokens accepted during each verification step, which reflects
the effectiveness of the draft generation process and is directly
related to the achievable acceleration.
V. RESULTS ANDANALYSIS
A. Main Results
In this section, we evaluate the performance of EAGLE-
ASR and other speculative decoding methods on the Lib-
riSpeech benchmark using both Whisper and Conformer AED
models. To ensure a fair comparison, all methods are re-
implemented and evaluated under the same hardware con-
figuration and experimental environment. Unless otherwise
specified, the decoding hyperparameters for evaluation are set
to a draft length ofK= 5and top-k= 1. For the standard
Speculative Decoding (SpD) baselines with Whisper-large-v3,
we employ Distil-large-v3 and Whisper-tiny as draft models.
For the Conformer AED model, we use Distil-small and
Whisper-tiny to ensure the draft model remains substantially
smaller than the target. 1 Regarding the Medusa baseline,
we evaluate two implementations from Whisper-Medusa on
the Whisper model: Medusa-Linear and Medusa-Block. It
is crucial to note that neither of these approaches achieves
lossless acceleration, as they modify the original parameters
of the target model and do not adhere to strict speculative
decoding acceptance criteria. In addition, we do not report
Medusa’s acceleration results on the Conformer AED model
as no public implementation is currently available.
We present the results in Table I and Figure 4. For the
Whisper-large-v3 target model, EAGLE-ASR achieves the
highest speedup, reaching 1.91×on test-clean and 1.79×
on test-other, outperforming all baselines while maintaining
strictly lossless decoding (∆WER= 0.00). Notably, SpD with
Distil-large-v3 attains the highest acceptance length, yet its
1Due to the discrepancy between the tokenizers of Conformer AED and
Whisper, direct token verification is infeasible. We address this vocabulary
mismatch by decoding the Whisper draft tokens into text and then re-encoding
them using the Conformer tokenizer before verification.

7
TABLE I
COMPARISON OF ACCELERATION PERFORMANCE ACROSS DIFFERENT SPECULATIVE DECODING APPROACHES ON THELIBRISPEECH DATASET.
Target model Method Draft Model Draft Params Test Clean Test Other
Speedupτ∆WER Speedupτ∆WER
Whisper
(1550 M)
SpD [12] Distil-large-v3 756 M 1.72×4.140.00 1.52×3.760.00
SpD [12] Whisper-tiny 39 M 1.76×3.04 0.00 1.58×2.56 0.00
Medusa [25] Medusa-Linear 68 M 1.67×3.51 +1.88 1.59×3.32 +3.61
Medusa [25] Medusa-Block 92 M 1.65×3.16 +1.17 1.54×3.01 +1.50
EAGLE-ASR Speech-Draft 117 M1.91×3.79 0.001.79×3.55 0.00
Conformer
(220 M)
SpD [12] Distil-small 166 M 1.18×2.85 0.00 0.90×2.35 0.00
SpD [12] Whisper-tiny 39 M 1.13×2.56 0.00 0.88×1.97 0.00
EAGLE-ASR Speech-Draft 10 M2.43×4.980.002.30×4.500.00
Whisper Conformer
0
0.5
1
1.5
2
2.5
1.0×
1.6×
1.7×
1.6× 1.6×
1.9×
1.0× 1.0× 1.0×
2.4×
Speedup
Vanilla SpD w/ Distil-large-v3
SpD w/ Distil-small SpD w/ Whisper-tiny
Medusa w/ Medusa-Linear Medusa w/ Medusa-Block
EAGLE-ASR
Fig. 4. Speedup comparison across different decoding methods. EAGLE-
ASR consistently outperforms all baseline methods for both target models
while guaranteeing lossless decoding.
speedup ratio is lower than that of our EAGLE-ASR. This is
due to the fact that the Distil-large-v3 draft model contains
756M parameters, comprising nearly half the size of the
target model, which incurs substantial computational overhead
during the drafting stage and consequently offsets the benefits
gained from its high acceptance rate. In contrast, while other
speculative decoding methods employ more lightweight draft
models compared to EAGLE-ASR, the mean accepted lengths
τvalues are significantly lower than those of EAGLE-ASR,
thus resulting in lower speedup ratios. These results suggest
that EAGLE-ASR achieves a more effective balance between
draft quality and computational efficiency.
The advantage of EAGLE-ASR is more pronounced on
the Conformer AED model. EAGLE-ASR achieves a remark-
able 2.43×speedup on test-clean and 2.30×on test-other,
substantially outperforming SpD with Distil-small and SpD
with Whisper-tiny. In fact, both SpD baselines fail to acceler-
ate, even resulting in a slowdown on the more challenging
test-other set. This poor performance can be attributed to
a combination of factors. First, the Conformer AED target
model is relatively small (220M parameters), which makes
the computational overhead of executing a separate draft
model comparatively high. Second, a significant distributional
mismatch exists between the Conformer AED target and the
Whisper-based draft models. This includes discrepancies in
transcription style, leading to low acceptance rates for the draft
sequences (evidenced by lowτvalues for both SpD methods).
Finally, due to the tokenizer mismatch between Conformer
AED and Whisper models, we are compelled to perform
token mapping through ground-truth text during the verifi-
cation phase, which further exacerbates the time overhead.
These results highlight the practical challenges of applying
conventional speculative decoding across heterogeneous ASR
model families.
Across both target models and evaluation sets, EAGLE-ASR
consistently achieves the highest speedup while maintaining
lossless transcription quality. These results highlight two key
strengths of our proposed framework. First, our proposed
Speech-Draft module effectively leverages the hidden features
of the target model to generate high-quality draft tokens
while maintaining a lightweight architecture. This design
achieves an effective trade-off between generation quality and
computational cost, ultimately leading to superior accelera-
tion performance. Second, EAGLE-ASR demonstrates strong
generalizability across target models with different architec-
tures and parameter scales without requiring architecture-
specific modifications or same-family distilled draft models.
This makes EAGLE-ASR a practical and flexible acceleration
solution for a broad range of autoregressive attention-based
ASR systems, particularly for models that lack the same-
family smaller variants or distilled lightweight variants.
B. Performance on Multilingual Speech Recognition
To further evaluate the generalizability of EAGLE-ASR
across diverse languages, we report the acceleration perfor-
mance of EAGLE-ASR on the V oxPopuli multilingual ASR

8
benchmark using Whisper as the target model. Specifically, the
evaluation covers five languages: English, German, Spanish,
French, and Italian. The decoding hyperparameters for the
multilingual ASR task remain identical to those used in the
monolingual ASR experiments as described above.
TABLE II
ACCELERATION PERFORMANCE OFEAGLE-ASRACROSS DIVERSE
LANGUAGES FORASR.
Subset Speedupτ∆WER
V oxPopuli English 1.96×4.06 0.00
V oxPopuli German 2.14×4.50 0.00
V oxPopuli Spanish 2.10×4.46 0.00
V oxPopuli French 2.15×4.64 0.00
V oxPopuli Italian 2.10×4.46 0.00
Average 2.09×4.42 0.00
As shown in Table II, EAGLE-ASR delivers consistent and
substantial acceleration across all five languages, achieving a
2.09×average acceleration while remaining strictly lossless
(∆WER= 0.00for every subset). This performance is un-
derpinned by the high quality of the generated draft tokens,
as evidenced by the consistently high average acceptance
lengths (τ), which average 4.41 across the languages. No-
tably, EAGLE-ASR exhibits highly consistent performance
across different languages, with speedup ratios ranging from
1.96×to 2.15×. The relatively small performance variation
suggests that the Speech-Draft module effectively captures
language-agnostic patterns from the target model’s hidden
representations, enabling it to generalize well across diverse
languages. Overall, these multilingual evaluations confirm that
the acceleration benefits of EAGLE-ASR extend well beyond
English, confirming its strong generalizability across diverse
languages while strictly preserving lossless decoding accuracy.
C. Performance on Speech Translation
To further evaluate the generalization ability and robustness
of EAGLE-ASR beyond ASR, we extend our investigation to
the speech translation (ST) task. Specifically, by leveraging
Whisper’s inherent capability to directly translate non-English
speech into English text, we conduct additional experiments
on the V oxPopuli dataset. Unlike its earlier use in multilingual
ASR, V oxPopuli is repurposed in this section to benchmark
the acceleration performance of EAGLE-ASR across four
diverse X-to-English translation directions. For the ST task,
we report the acceleration results with a draft length of
K= 5and a sampling size of top-k= 2, which helps
accommodate the increased output uncertainty compared with
standard transcription task.
As shown in Table III, EAGLE-ASR consistently improves
inference efficiency across all four translation tasks, achieving
an average speedup of 1.62×and a mean acceptance lengthτ
of 3.57. Importantly, this acceleration remains strictly lossless,
with a∆BLEU score of 0.00 for every task, confirming
that EAGLE-ASR fully preserves the translation quality of
the original Whisper model. A notable observation is that,
despite using a larger top-kvalue, EAGLE-ASR achieves a
lower mean accepted length on speech translation (τ= 3.57)
TABLE III
ACCELERATION PERFORMANCE OFEAGLE-ASRACROSS VARIOUS
SPEECH TRANSLATION TASKS.
ST task Speedupτ∆BLEU
German-to-English 1.49×3.44 0.00
Spanish-to-English 1.73×3.75 0.00
French-to-English 1.66×3.60 0.00
Italian-to-English 1.59×3.49 0.00
Average 1.62×3.57 0.00
2 3 4 5 6 7 81.5
1.6
1.7
1.8
1.9
2
Draft LengthK
Speedup (×)
2 3 4 5 6 7 81
2
3
4
5
Draft LengthK
τ
Fig. 5. Effect of the draft lengthKon the acceleration performance of
EAGLE-ASR. Left: Speedup ratio. Right: Mean accepted lengthτ.
than on multilingual ASR task (τ= 4.42). This behavior is
expected due to the inherently higher complexity of the ST
task. Unlike ASR, ST involves a more intricate cross-lingual
mapping from source speech to target text, where the increased
output uncertainty poses greater challenges for draft model
predictions to be accepted. As a result, fewer draft tokens
are accepted during verification. Together with the additional
computational overhead introduced by the larger top-k setting,
this explains the relatively lower speedup observed for the ST
task (1.62×) compared with multilingual ASR task (2.09×).
Nevertheless, despite the increased task difficulty, EAGLE-
ASR demonstrates remarkable robustness and effectiveness by
delivering substantial, lossless acceleration for speech transla-
tion. These results indicate that the benefits of EAGLE-ASR
extend beyond monolingual and multilingual ASR and transfer
effectively to challenging speech translation scenarios. This
consistent acceleration across diverse cross-lingual generation
tasks further underscores the strong generalization ability and
robustness of our proposed framework.
D. Impact of Decoding Hyperparameters
In this section, we investigate the impact of decoding
hyperparameters on the acceleration performance of EAGLE-
ASR. Specifically, we focus on two key parameters: the draft
lengthK, which controls the number of tokens generated
by the draft model at each speculative step, and the top-k
sampling size, which determines the number of candidate
tokens considered during the sampling process.
Figure 5 illustrates how the draft lengthKaffects both the
speedup ratio and the mean accepted lengthτwhen top-kis
fixed to 1. As shown in the right panel, the mean accepted
lengthτincreases monotonically asKincreases, rising from
1.82 atK=2to 4.57 atK=8. This is expected, since a longer

9
1 2 3 41.5
1.6
1.7
1.8
1.9
top-k
Speedup (×)
1 2 3 43
3.5
4
4.5
5
top-k
τ
Fig. 6. Effect of top-kon the acceleration performance of EAGLE-ASR.
Left: Speedup ratio. Right: Mean accepted lengthτ.
draft sequence provides more candidate tokens for verification,
and thus more tokens can be accepted on average in a single
forward pass.
However, the speedup ratio does not exhibit the same
monotonic trend. As shown in the left panel, the speedup first
increases withK, reaches a peak of approximately 1.85×at
K=5, and then gradually declines asK=5increases further.
This discrepancy can be explained by the trade-off between
two competing factors: the number of accepted tokens and
the computational cost of drafting. On the one hand, a larger
Kleads to a higherτ, meaning that fewer verification steps
are needed to generate a complete sequence, thereby reducing
the number of expensive forward passes through the target
model. On the other hand, each draft step requires the draft
model to runKautoregressive iterations, and the subsequent
verification pass must process the entire draft sequence, both
of which incur additional computational overhead that scales
roughly withK. WhenKis small, the gain from accepting
more tokens per step outweighs the extra drafting cost, leading
to improved acceleration. However, the marginal gain in ac-
cepted tokens gradually diminishes asKgrows. For example,
τincreases by 0.84 whenKgoes from 2 to 3, but only by
0.22 whenKincreases from 7 to 8. This sublinear growth of
τsuggests that draft tokens predicted further are more likely
to be rejected due to error accumulation. Beyond the optimal
point (K= 5), the additional drafting overhead outweighs
the modest gain in accepted length, leading to reduced overall
speedup.
Figure 6 further presents the impact of the draft top-kwhen
the draft length is fixed atK=5. As shown in the right
panel, the mean accepted lengthτincreases monotonically
as top-kincreases, rising from 3.67 at top-k=1to 4.56 at
top-k=4. This trend is expected, since enlarging the candidate
set at each drafting step increases the likelihood that the target
token is included among the proposed candidates, thereby
improving the acceptance rate during verification. However,
the speedup ratio exhibits the opposite trend. As shown in the
left panel, the speedup decreases monotonically from 1.85×
at top-k=1to 1.54×at top-k=4. This indicates that, for
ASR tasks, EAGLE-ASR achieves greater acceleration when
adopting linear verification (top-k= 1) compared to tree-based
verification (top-k >1). Notably, this finding contrasts with
prior empirical observations in natural language processing,
1 2 3 41.3
1.4
1.5
1.6
top-k
Speedup (×)
1 2 3 42
2.5
3
3.5
4
4.5
top-k
τ
Fig. 7. Effect of top-kon the acceleration performance of EAGLE-ASR on
the ST (German-to-English) task. Left: Speedup ratio. Right: Mean accepted
lengthτ.
where speculative decoding typically benefits more from tree-
based verification strategies. We attribute this phenomenon to
the simplicity and deterministic nature of ASR tasks. As top-k
increases, the gain in the accepted token lengthτis marginal.
For example, when top-kincreases from 1 to 2,τimproves
by only 0.46. Concurrently, a larger top-kleads the draft
model to generate more candidate tokens at each step, thereby
increasing the number of tokens that must be verified by the
target model and consequently raising the computational cost
per verification step. The modest improvement inτbrought
by increasing top-kis insufficient to offset the steadily grow-
ing verification overhead, ultimately resulting in a consistent
decline in the overall speedup ratio.
To validate this hypothesis, we further investigate the impact
of top-kon the acceleration performance of EAGLE-ASR in
the ST task. Compared with ASR, ST is inherently more com-
plex and exhibits greater output diversity, as a single source
utterance can have multiple valid translations. We present
the results for the German-to-English task as a representative
example.
Figure 7 shows the effect of top-kon EAGLE-ASR for the
ST task. In contrast to the ASR results, the speedup on ST
does not decrease monotonically as top-kincreases. Instead,
the speedup first improves from 1.44×at top-k=1to 1.48×
at top-k=2, and then gradually declines to 1.38×at top-k=4.
Meanwhile, the mean accepted lengthτincreases steadily
from 2.70 to 3.90. This result supports our hypothesis that the
effectiveness of tree-based verification is task dependent. For
the ST task, increasing the top-kvalue enables the draft model
to explore a broader range of translation hypotheses, thereby
increasing the likelihood that the target model accepts at least
one branch within the expanded tree. Consequently, the growth
inτinduced by larger top-kis substantially more pronounced
in ST than in ASR. In particular, when top-kincreases
from 1 to 2,τrises by 0.74, which is substantially higher
than the corresponding gain of 0.46 observed in the ASR
task. This improvement is sufficient to offset the additional
verification overhead, thereby yielding a speedup. However,
the benefit quickly saturates when top-kbecomes larger. When
top-kexceeds 2, the verification overhead begins to dominate:
the marginal increase inτdiminishes, while the number of
candidates requiring verification continues to grow, leading

10
to degraded speedup. We conjecture that this is because
ST tasks, despite being more complex than ASR, remain
relatively simple and deterministic compared to dialogue or
comprehension tasks, which typically employ top-k= 4or8
in speculative decoding settings [28], [46].
E. Ablation Studies
In this section, we conduct a comprehensive ablation study
to systematically evaluate the contribution of each component
in EAGLE-ASR. Our analysis focuses on three primary as-
pects: the architecture of the Speech-Draft module, the training
data, and the employed training strategies.
TABLE IV
ABLATION STUDY RESULTS OFEAGLE-ASRON THEWHISPER MODEL.
Method Speedupτ∆WER
w/o encoder feature 0.89×0.08 0.00
w/o fused decoder features 1.35×1.84 0.00
w/o self-distilled data 1.43×2.02 0.00
w/o multi-step generation 1.17×1.00 0.00
w/oL mtp 1.66×3.28 0.00
EAGLE-ASR 1.85×3.67 0.00
We first investigate the impact of different architectural
components within the Speech-Draft module. As shown in
the first two rows of Table IV, both encoder features and
fused decoder features play critical roles in achieving ef-
fective speculative decoding. When the encoder features are
removed by replacing the cross-attention mechanism with self-
attention, the model suffers from catastrophic performance
degradation. Instead of achieving acceleration, the system
exhibits a slowdown (0.89×) and a drastically reduced mean
accepted length (τ= 0.08). This indicates that the acoustic
information from the encoder is indispensable for the Speech-
Draft module to generate plausible draft tokens that align with
the target ASR model’s predictions. Without direct access
to encoder representations, the draft model lacks sufficient
acoustic grounding, leading to poor-quality predictions that
are rarely accepted by the target model.
Next, when replacing the fused decoder features with only
the second-top-layer decoder features, the model still achieves
acceleration (1.35×speedup), but the improvement is substan-
tially lower than that of the full EAGLE-ASR framework. The
results demonstrate that the fusion of multi-layer decoder fea-
tures provides richer contextual representations. By integrating
information from different levels of the decoding process,
the fused features enable the Speech-Draft module to more
accurately approximate the behavior of the target model and
to generate higher-quality draft tokens, thereby improving the
overall acceleration performance.
Then we analyze the effect of the training data. The third
row of Table IV presents the results when the Speech-Draft
module is trained on the original ground-truth transcripts
rather than on self-distilled data generated by the target ASR
model. This change leads to a noticeable degradation in
acceleration performance, with the speedup dropping to 1.43×
and the mean accepted lengthτfalling to 2.02. This result
highlights a fundamental principle of speculative decoding:
the draft model’s primary goal is to predict the target model’s
output, not necessarily the ground truth. When trained on
self-distilled data, the Speech-Draft module directly learns
to approximate the token distribution produced by the target
ASR model, including transcription style characteristics such
as punctuation and capitalization. Such distributional align-
ment increases the likelihood that the drafted tokens will be
accepted during the verification stage. In contrast, training
on ground-truth transcripts forces the draft model to learn
an “ideal” distribution, which may diverge from the target
model’s. This distributional mismatch causes more rejections,
as predictions that are correct with respect to the ground truth
may nonetheless differ from the tokens that the target model
would generate. Moreover, in the case of the Whisper model,
the original transcriptions lack special token prefixes, which
further constrains the acceptance rate of draft tokens generated
by the Speech-Draft at the initial decoding step.
Finally, we examine the impact of our proposed training
strategies. The fourth and fifth rows of Table IV show the
results of ablating the multi-step generation training and the
weighted cross-entropy loss with exponential decayL mtp.
When the number of iterative generation steps during training
is set to one, a dramatic performance collapse is observed,
with the speedup plummeting to1.17×and the mean accepted
lengthτreducing to 1.00. The result ofτ= 1.00indicates
that, on average, only the first token of each drafted sequence
is accepted. This outcome aligns with our expectations: dur-
ing training, Speech-Draft is optimized solely to generate
predictions conditioned on the hidden representations of the
target model, rather than on its own previously predicted
hidden states. Consequently, this module is only capable of
predicting the immediate next token and lacks the ability to
autoregressively generate subsequent tokens. This observation
highlights that a multi-step generation training strategy is es-
sential for enabling Speech-Draft to produce multiple plausible
tokens simultaneously, thereby enhancing its effectiveness in
speculative decoding. When the exponential decay weighting
inL mtp is removed (settingβ= 1), the model achieves a
speedup of 1.66×withτ= 3.28. Although this still pro-
vides a noticeable acceleration, it remains inferior to the full
EAGLE-ASR configuration. This degradation occurs because
predicting tokens further into the future is inherently more
challenging due to increased uncertainty. The exponential
decay mechanism inL mtp strategically prioritizes the accuracy
of the initial tokens in the drafted sequence, which are more
critical for the acceptance of the entire sequence. By assigning
equal weights across all positions, the model is forced to
allocate its capacity to optimizing for harder, more distant
predictions, potentially at the cost of accuracy on the more
crucial initial tokens. Since an incorrect early token leads to
the rejection of the entire draft, this targeted optimization leads
to improved draft quality and higher acceptance rates during
verification. Since an error early token leads to the rejection
of the entire draft sequence, uniform weighting can ultimately
lead to a lower overall acceptance rate.

11
VI. CONCLUSION
In this paper, we propose EAGLE-ASR, a novel and general
framework for lossless inference acceleration of autoregressive
ASR models through EAGLE-style speculative decoding. By
introducing a lightweight and model-agnostic Speech-Draft
module that jointly leverages hierarchical decoder representa-
tions and encoder acoustic features, the proposed framework
effectively balances draft quality and computational overhead.
Through self-distilled training data and a multi-step generation
strategy, Speech-Draft is optimized to closely approximate
the output distribution of the target model while maintaining
stable and reliable multi-token prediction capability. Exten-
sive experiments conducted on Whisper and Conformer-based
AED models demonstrate that EAGLE-ASR achieves substan-
tial inference speedups. It consistently outperforms existing
speculative decoding baselines, while strictly preserving out-
put quality without any degradation. Furthermore, additional
experiments on multilingual ASR and speech translation tasks
confirm the robustness and generalizability of EAGLE-ASR
across diverse languages and cross-lingual generation settings.
Overall, EAGLE-ASR provides a practical and universally
applicable solution for accelerating modern ASR systems
without sacrificing accuracy.
REFERENCES
[1] A. Radford, J. W. Kim, T. Xu, G. Brockman, C. McLeavey, and
I. Sutskever, “Robust speech recognition via large-scale weak supervi-
sion,” inInternational conference on machine learning. PMLR, 2023,
pp. 28 492–28 518.
[2] A. Gulati, J. Qin, C.-C. Chiu, N. Parmar, Y . Zhang, J. Yu, W. Han,
S. Wang, Z. Zhang, Y . Wuet al., “Conformer: Convolution-augmented
transformer for speech recognition,” inProc. Interspeech 2020, 2020,
pp. 5036–5040.
[3] A. Baevski, Y . Zhou, A. Mohamed, and M. Auli, “wav2vec 2.0:
A framework for self-supervised learning of speech representations,”
Advances in neural information processing systems, vol. 33, pp. 12 449–
12 460, 2020.
[4] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,
Ł. Kaiser, and I. Polosukhin, “Attention is all you need,”Advances in
neural information processing systems, vol. 30, 2017.
[5] R. Prabhavalkar, T. Hori, T. N. Sainath, R. Schl ¨uter, and S. Watanabe,
“End-to-end speech recognition: A survey,”IEEE/ACM Transactions on
Audio, Speech, and Language Processing, vol. 32, pp. 325–351, 2023.
[6] S. Gondi and V . Pratap, “Performance and efficiency evaluation of asr
inference on the edge,”Sustainability, vol. 13, no. 22, p. 12392, 2021.
[7] M. Nayeem, M. S. Tabrej, K. J. Deb, S. Goswami, and M. A. Hakim,
“Automatic speech recognition in the modern era: Architectures, train-
ing, and evaluation,”arXiv preprint arXiv:2510.12827, 2025.
[8] A. Graves, “Sequence transduction with recurrent neural networks,”
arXiv preprint arXiv:1211.3711, 2012.
[9] Y . He, T. N. Sainath, R. Prabhavalkar, I. McGraw, R. Alvarez, D. Zhao,
D. Rybach, A. Kannan, Y . Wu, R. Panget al., “Streaming end-to-end
speech recognition for mobile devices,” inICASSP 2019-2019 IEEE
International Conference on Acoustics, Speech and Signal Processing
(ICASSP). IEEE, 2019, pp. 6381–6385.
[10] Y . Shi, Y . Wang, C. Wu, C.-F. Yeh, J. Chan, F. Zhang, D. Le, and
M. Seltzer, “Emformer: Efficient memory transformer based acoustic
model for low latency streaming speech recognition,” inICASSP 2021-
2021 IEEE International Conference on Acoustics, Speech and Signal
Processing (ICASSP). IEEE, 2021, pp. 6783–6787.
[11] Q. Zhang, H. Lu, H. Sak, A. Tripathi, E. McDermott, S. Koo, and
S. Kumar, “Transformer transducer: A streamable speech recognition
model with transformer encoders and rnn-t loss,” inICASSP 2020-
2020 IEEE International Conference on Acoustics, Speech and Signal
Processing (ICASSP). IEEE, 2020, pp. 7829–7833.
[12] S. Gandhi, P. V on Platen, and A. M. Rush, “Distil-whisper: Robust
knowledge distillation via large-scale pseudo labelling,”arXiv preprint
arXiv:2311.00430, 2023.
[13] H. Shao, B. Liu, W. Wang, X. Gong, and Y . Qian, “Dq-whisper: Joint
distillation and quantization for efficient multilingual speech recogni-
tion,” in2024 IEEE Spoken Language Technology Workshop (SLT).
IEEE, 2024, pp. 240–246.
[14] T. Gu, B. Liu, and Y . Qian, “Efficient pruning for large-scale seq2seq
speech models without back-propagation,” inICASSP 2025-2025 IEEE
International Conference on Acoustics, Speech and Signal Processing
(ICASSP). IEEE, 2025, pp. 1–5.
[15] K. Kamahori, J. Kasai, N. Kojima, and B. Kasikci, “Liteasr: Efficient
automatic speech recognition with low-rank approximation,” inProceed-
ings of the 2025 Conference on Empirical Methods in Natural Language
Processing, 2025, pp. 3430–3442.
[16] Y . Higuchi, S. Watanabe, N. Chen, T. Ogawa, and T. Kobayashi, “Mask
ctc: Non-autoregressive end-to-end asr with ctc and mask predict,” in
21st Annual Conference of the International Speech Communication As-
sociation, INTERSPEECH 2020. International Speech Communication
Association, 2020, pp. 3655–3659.
[17] Z. Gao, S. Zhang, I. McLoughlin, and Z. Yan, “Paraformer: Fast and
accurate parallel transformer for non-autoregressive end-to-end speech
recognition,”arXiv preprint arXiv:2206.08317, 2022.
[18] K. An, Z. Li, Z. Gao, and S. Zhang, “Paraformer-v2: An improved non-
autoregressive transformer for noise-robust speech recognition,”arXiv
preprint arXiv:2409.17746, 2024.
[19] E. A. Chi, J. Salazar, and K. Kirchhoff, “Align-refine: Non-
autoregressive speech recognition via iterative realignment,” inPro-
ceedings of the 2021 Conference of the North American Chapter
of the Association for Computational Linguistics: Human Language
Technologies, 2021, pp. 1920–1927.
[20] N. Chen, S. Watanabe, J. Villalba, P. ˙Zelasko, and N. Dehak, “Non-
autoregressive transformer for speech recognition,”IEEE Signal Pro-
cessing Letters, vol. 28, pp. 121–125, 2020.
[21] Y . Leviathan, M. Kalman, and Y . Matias, “Fast inference from transform-
ers via speculative decoding,” inInternational Conference on Machine
Learning. PMLR, 2023, pp. 19 274–19 286.
[22] C. Chen, S. Borgeaud, G. Irving, J.-B. Lespiau, L. Sifre, and J. Jumper,
“Accelerating large language model decoding with speculative sam-
pling,”arXiv preprint arXiv:2302.01318, 2023.
[23] H. Xia, Z. Yang, Q. Dong, P. Wang, Y . Li, T. Ge, T. Liu, W. Li,
and Z. Sui, “Unlocking efficiency in large language model inference:
A comprehensive survey of speculative decoding,”Findings of the
Association for Computational Linguistics: ACL 2024, pp. 7655–7671,
2024.
[24] L. Wei, S. Zhong, S. Xu, R. Wang, R. Huang, and M. Li, “Specasr:
Accelerating llm-based automatic speech recognition via speculative
decoding,” in2025 62nd ACM/IEEE Design Automation Conference
(DAC). IEEE, 2025, pp. 1–7.
[25] Y . Segal-Feldman, A. Shamsian, A. Navon, G. Hetz, and J. Keshet,
“Whisper in medusa’s ear: Multi-head efficient decoding for transformer-
based asr,” inICASSP 2025-2025 IEEE International Conference on
Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2025, pp.
1–5.
[26] T. V . Ho, H. Kokubo, M. Yamamoto, and Y . Kawaguchi, “Model-free
speculative decoding for transformer-based asr with token map drafting,”
in2025 33rd European Signal Processing Conference (EUSIPCO).
IEEE, 2025, pp. 361–365.
[27] Y . Li, F. Wei, C. Zhang, and H. Zhang, “Eagle: speculative sampling
requires rethinking feature uncertainty,” inProceedings of the 41st
International Conference on Machine Learning, 2024, pp. 28 935–
28 948.
[28] Li, Yuhui and Wei, Fangyun and Zhang, Chao and Zhang, Hongyang,
“Eagle-2: Faster inference of language models with dynamic draft trees,”
inProceedings of the 2024 conference on empirical methods in natural
language processing, 2024, pp. 7421–7432.
[29] Li, Yuhui and Wei, Fangyun and Zhang, Chao and Zhang, Hongyang,
“Eagle-3: Scaling up inference acceleration of large language models
via training-time test,”arXiv preprint arXiv:2503.01840, 2025.
[30] Y . Cai, X. Liang, X. Wang, J. Ma, H. Liang, J. Luo, X. Zuo, L. Duan,
Y . Yin, and X. Chen, “Fastmtp: Accelerating llm inference with en-
hanced multi-token prediction,”arXiv preprint arXiv:2509.18362, 2025.
[31] G. Saon, S. Thomas, T. Fukuda, T. Nagano, A. Dekel, and L. Lastras,
“Self-speculative decoding for llm-based asr with ctc encoder drafts,”
arXiv preprint arXiv:2603.11243, 2026.
[32] H. Huang, F. Yang, Z. Liu, X. Yin, D. Li, P. Ren, and E. Barsoum,
“Specvlm: Fast speculative decoding in vision-language models,”arXiv
preprint arXiv:2509.11815, 2025.
[33] J. Kang, H. Shu, W. Li, Y . Zhai, and X. Chen, “Vispec: Accelerating
vision-language models with vision-aware speculative decoding,”Ad-

12
vances in Neural Information Processing Systems, vol. 38, pp. 115 511–
115 532, 2026.
[34] G. Hinton, O. Vinyals, and J. Dean, “Distilling the knowledge in a neural
network,”arXiv preprint arXiv:1503.02531, 2015.
[35] A. Gholami, S. Kim, Z. Dong, Z. Yao, M. W. Mahoney, and K. Keutzer,
“A survey of quantization methods for efficient neural network infer-
ence,” inLow-power computer vision. Chapman and Hall/CRC, 2022,
pp. 291–326.
[36] S. Han, J. Pool, J. Tran, and W. Dally, “Learning both weights and con-
nections for efficient neural network,”Advances in neural information
processing systems, vol. 28, 2015.
[37] J. Gu, J. Bradbury, C. Xiong, V . O. Li, and R. Socher, “Non-
autoregressive neural machine translation,” inInternational Conference
on Learning Representations, 2018.
[38] M. Stern, N. Shazeer, and J. Uszkoreit, “Blockwise parallel decoding
for deep autoregressive models,”Advances in Neural Information Pro-
cessing Systems, vol. 31, 2018.
[39] X. Sun, T. Ge, F. Wei, and H. Wang, “Instantaneous grammatical error
correction with shallow aggressive decoding,” inProceedings of the 59th
Annual Meeting of the Association for Computational Linguistics and
the 11th International Joint Conference on Natural Language Processing
(Volume 1: Long Papers), 2021, pp. 5937–5947.
[40] X. Miao, G. Oliaro, Z. Zhang, X. Cheng, Z. Wang, Z. Zhang, R. Y . Y .
Wong, A. Zhu, L. Yang, X. Shiet al., “Specinfer: Accelerating large
language model serving with tree-based speculative inference and ver-
ification,” inProceedings of the 29th ACM International Conference
on Architectural Support for Programming Languages and Operating
Systems, Volume 3, 2024, pp. 932–949.
[41] B. Spector and C. Re, “Accelerating llm inference with staged specula-
tive decoding,”arXiv preprint arXiv:2308.04623, 2023.
[42] Z. Chen, X. Yang, J. Lin, C. Sun, K. C. Chang, and J. Huang, “Cascade
speculative drafting for even faster llm inference,”Advances in Neural
Information Processing Systems, vol. 37, pp. 86 226–86 242, 2024.
[43] S. Kim, K. Mangalam, S. Moon, J. Malik, M. W. Mahoney, A. Gholami,
and K. Keutzer, “Speculative decoding with big little decoder,”Advances
in Neural Information Processing Systems, vol. 36, pp. 39 236–39 256,
2023.
[44] N. Yang, T. Ge, L. Wang, B. Jiao, D. Jiang, L. Yang, R. Majumder,
and F. Wei, “Inference with reference: Lossless acceleration of large
language models,”arXiv preprint arXiv:2304.04487, 2023.
[45] Z. He, Z. Zhong, T. Cai, J. Lee, and D. He, “Rest: Retrieval-based
speculative decoding,” inProceedings of the 2024 Conference of the
North American Chapter of the Association for Computational Linguis-
tics: Human Language Technologies (Volume 1: Long Papers), 2024,
pp. 1582–1595.
[46] T. Cai, Y . Li, Z. Geng, H. Peng, J. D. Lee, D. Chen, and T. Dao,
“Medusa: Simple llm inference acceleration framework with multiple
decoding heads,”Proceedings of Machine Learning Research, vol. 235,
pp. 5209–5235, 2024.
[47] Z. Yang, T. Pang, H. Feng, H. Wang, W. Chen, M. Zhu, and Q. Liu,
“Self-distillation bridges distribution gap in language model fine-tuning,”
inProceedings of the 62nd Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers), 2024, pp. 1028–
1043.
[48] V . Panayotov, G. Chen, D. Povey, and S. Khudanpur, “Librispeech: an asr
corpus based on public domain audio books,” in2015 IEEE international
conference on acoustics, speech and signal processing (ICASSP). IEEE,
2015, pp. 5206–5210.
[49] C. Wang, M. Riviere, A. Lee, A. Wu, C. Talnikar, D. Haziza,
M. Williamson, J. Pino, and E. Dupoux, “V oxpopuli: A large-scale
multilingual speech corpus for representation learning, semi-supervised
learning and interpretation,” inProceedings of the 59th Annual Meeting
of the Association for Computational Linguistics and the 11th Interna-
tional Joint Conference on Natural Language Processing (Volume 1:
Long Papers), 2021, pp. 993–1003.
[50] Z. Gao, Z. Li, J. Wang, H. Luo, X. Shi, M. Chen, Y . Li, L. Zuo,
Z. Du, Z. Xiao, and S. Zhang, “Funasr: A fundamental end-to-end speech
recognition toolkit,” inINTERSPEECH, 2023.
[51] I. Loshchilov and F. Hutter, “Decoupled weight decay regularization,”
arXiv preprint arXiv:1711.05101, 2017.
[52] Loshchilov, Ilya and Hutter, Frank, “Sgdr: Stochastic gradient descent
with warm restarts,”arXiv preprint arXiv:1608.03983, 2016.
[53] H. Xia, T. Ge, P. Wang, S.-Q. Chen, F. Wei, and Z. Sui, “Speculative
decoding: Exploiting speculative execution for accelerating seq2seq gen-
eration,” inFindings of the Association for Computational Linguistics:
EMNLP 2023, 2023, pp. 3909–3925.
[54] K. Papineni, S. Roukos, T. Ward, and W.-J. Zhu, “Bleu: a method for
automatic evaluation of machine translation,” inProceedings of the 40th
annual meeting of the Association for Computational Linguistics, 2002,
pp. 311–318.
