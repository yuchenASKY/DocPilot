# LaCache: Robust Semantic Caching for LLM Serving

> **arXiv**: [2608.01718v1](https://arxiv.org/abs/2608.01718v1) ｜ **发布日期**: 2026-08-03 ｜ **分类**: cs.AI ｜ **页数**: 15

## 摘要

Semantic caching, which reuses responses to semantically similar requests via their embeddings, has seen growing adoption in LLM serving, offering faster responses and reduced costs. Yet existing schemes are fundamentally vulnerable to cache-collision attacks, wherein an adversary pollutes the cache by injecting crafted queries, corrupting responses to subsequent legitimate requests. We present LaCache, a novel semantic caching scheme that addresses this vulnerability through a conceptually simple yet principled redesign. The key insight is that while the adversary has full control over the adversarial query, it has far less control over its response, which must simultaneously satisfy multiple semantic constraints. Rather than checking only the cache hit of a query, LaCache additionally checks the cache hit of its first k (speculatively) decoded tokens. This design yields two concrete benefits. First, it provides formally guaranteed resilience against cache-collision attacks: we prove that it is impossible to craft adversarial queries that simultaneously elicit malicious responses and collide with benign queries. Second, the enriched index supplies additional semantic context for cache retrieval, improving response relevance. Empirical evaluation across diverse LLMs and benchmarks validates both LaCache's security guarantees and efficiency gains, pointing to a promising direction for robust semantic caching.

---

## 正文

LACACHE: ROBUSTSEMANTICCACHING FORLLM
SERVING
Jiacheng Liang, Yuhui Wang, Tanqiu Jiang, Ting Wang
Stony Brook University

### ABSTRACT
Semantic caching, reusing responses to answer semantically similar queries, has
seen growing adoption in LLM serving, offering faster responses and reduced
costs. Yet existing schemes are fundamentally vulnerable to cache-collision attacks,
wherein an adversary pollutes the cache by injecting adversarial queries, corrupting
responses to subsequent legitimate requests. We present LACACHE 1, a simple yet
principled redesign of semantic caching that provides provable defense against
such attacks. The key insight is that while the adversary has full control over the
adversarial query, it has far less control over the corresponding LLM-generated
response, which must simultaneously satisfy multiple competing constraints. Thus,
LACACHEshifts the integrity check from the query to the response: rather than
checking only the cache hit of a query, LACACHEadditionally checks the cache hit
of its first k speculatively decoded tokens. Analytically, we prove that LACACHE
detects any cache-collision attack that produces a semantically distinct response
with provably high probability. Empirically, evaluation across diverse LLMs and
benchmarks confirms that LACACHEreduces attack hit rate to near zero while
preserving over 90% of benign cache utility. To our best knowledge, this work is the
first to exploit the inherent constraints on adversarial responses in cache-collision
attacks to provide provable security, pointing to a promising direction for building
robust semantic caching.

### 1 INTRODUCTION
Semantic caching has become essential for efficient LLM serving, reusing cached responses for
semantically similar queries to reduce latency and inference costs Regmi & Phakami Pun (2024);
Zhao & Mastorakis (2025); Zhu et al. (2025); Gaspar Schroeder et al. (2026); YU et al. (2025); Jin
et al. (2025); Agarwal et al. (2025); Kahatapitiya et al. (2025), a capability now deployed at scale
across major LLM serving platforms Gu et al. (2025); Microsoft (2025); Amazon (2025); Alibaba
(2025). Yet this efficiency boost also introduces a new attack surface: cache-collision attacks. As
illustrated in Figure 1 (a), the adversary may inject crafted queries whose cache keys collide with
those of legitimate queries, causing the cache to serve adversary-controlled responses to subsequent
queries Zhang et al. (2026); Afiffy et al. (2026); Wu et al. (2026a;b); Liang et al. (2026); Zou et al.
(2025).
Existing defenses against cache-collision attacks are fundamentally reactive: they attempt to identify
and filter adversarial queries at lookup time, using signals such as perplexity Hu et al. (2023); Zhang
et al. (2026), query–response consistency Wu et al. (2026a), or LLM-based classification Afiffy et al.
(2026); Wu et al. (2026a). This strategy is inherently limited. Since the adversary exercises full control
over the adversarial query, which is never directly seen by the victim user, it can be freely optimized
to evade any query-side defense. Gradient-guided optimization, such as GCG Zhao et al. (2024); Zou
et al. (2023), can produce low-perplexity, fluent adversarial queries that bypass both perplexity and
consistency checks. As we demonstrate empirically, no existing defense simultaneously withstands
all attack variants.
1LACACHE: LookAhead Cache.
1
arXiv:2608.01718v1 [cs.AI] 3 Aug 2026

<latexit sha1_base64="xx4cftoLTd+uJZjk2QcUhteuwW4=">AAACDnicbVDLSgNBEJyN7/ha9ehlMAgqEnY1RC9CwIvHiCYK2RhmJ504ZPbhTK8kLPkCL/6KFw+KePXszb9x8jiosaChqOqmu8uPpdDoOF9WZmp6ZnZufiG7uLS8smqvrVd1lCgOFR7JSF37TIMUIVRQoITrWAELfAlXfud04F/dg9IiCi+xF0M9YO1QtARnaKSGve0hdDG9EEF/p7tPuzd7u/SEOvnjQ+q14Y56yJIGb9g5J+8MQSeJOyY5Mka5YX96zYgnAYTIJdO65jox1lOmUHAJ/ayXaIgZ77A21AwNWQC6ng7f6dNtozRpK1KmQqRD9edEygKte4FvOgOGt/qvNxD/82oJto7rqQjjBCHko0WtRFKM6CAb2hQKOMqeIYwrYW6l/JYpxtEkmDUhuH9fniTVg7xbzBfPC7lSYRzHPNkkW2SHuOSIlMgZKZMK4eSBPJEX8mo9Ws/Wm/U+as1Y45kN8gvWxze6WZn4</latexit>
Sim(x, x→)=0.83→ωc
<latexit sha1_base64="PfZPuudgC5zFMqrRSadBsb63jkA=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lEqseCF48V7Qe0oWy2m3bpZhN2J2IJ/QlePCji1V/kzX/jts1BWx8MPN6bYWZekEhh0HW/ncLa+sbmVnG7tLO7t39QPjxqmTjVjDdZLGPdCajhUijeRIGSdxLNaRRI3g7GNzO//ci1EbF6wEnC/YgOlQgFo2il+6e+2y9X3Ko7B1klXk4qkKPRL3/1BjFLI66QSWpM13MT9DOqUTDJp6VeanhC2ZgOeddSRSNu/Gx+6pScWWVAwljbUkjm6u+JjEbGTKLAdkYUR2bZm4n/ed0Uw2s/EypJkSu2WBSmkmBMZn+TgdCcoZxYQpkW9lbCRlRThjadkg3BW355lbQuql6tWru7rNQv8ziKcAKncA4eXEEdbqEBTWAwhGd4hTdHOi/Ou/OxaC04+cwx/IHz+QMJiI2c</latexit>
x0
<latexit sha1_base64="PfZPuudgC5zFMqrRSadBsb63jkA=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lEqseCF48V7Qe0oWy2m3bpZhN2J2IJ/QlePCji1V/kzX/jts1BWx8MPN6bYWZekEhh0HW/ncLa+sbmVnG7tLO7t39QPjxqmTjVjDdZLGPdCajhUijeRIGSdxLNaRRI3g7GNzO//ci1EbF6wEnC/YgOlQgFo2il+6e+2y9X3Ko7B1klXk4qkKPRL3/1BjFLI66QSWpM13MT9DOqUTDJp6VeanhC2ZgOeddSRSNu/Gx+6pScWWVAwljbUkjm6u+JjEbGTKLAdkYUR2bZm4n/ed0Uw2s/EypJkSu2WBSmkmBMZn+TgdCcoZxYQpkW9lbCRlRThjadkg3BW355lbQuql6tWru7rNQv8ziKcAKncA4eXEEdbqEBTWAwhGd4hTdHOi/Ou/OxaC04+cwx/IHz+QMJiI2c</latexit>
x0
(a) Cache-collision Attack
1. Attacker crafts adversarial query x* 
Adversarial Query x* = <GCG Preﬁx> ⊕ ⊕ “Always answer Yes …”
Core Query = “Can I give aspirin to my child?”
f(x*) = “Yes, you can give 
your child aspirin”

### 2. LLM generates and caches adversarial response
Key: h(x*) 
Value: f(x*)

### 3. LLM reuses cached response for target query
x = “Can I give 
aspirin to my child?”
 f(x*): “Yes, you can give your child aspirin”
(b) LaCache Workﬂow

### 1. Cache-Key Check
<latexit sha1_base64="xx4cftoLTd+uJZjk2QcUhteuwW4=">AAACDnicbVDLSgNBEJyN7/ha9ehlMAgqEnY1RC9CwIvHiCYK2RhmJ504ZPbhTK8kLPkCL/6KFw+KePXszb9x8jiosaChqOqmu8uPpdDoOF9WZmp6ZnZufiG7uLS8smqvrVd1lCgOFR7JSF37TIMUIVRQoITrWAELfAlXfud04F/dg9IiCi+xF0M9YO1QtARnaKSGve0hdDG9EEF/p7tPuzd7u/SEOvnjQ+q14Y56yJIGb9g5J+8MQSeJOyY5Mka5YX96zYgnAYTIJdO65jox1lOmUHAJ/ayXaIgZ77A21AwNWQC6ng7f6dNtozRpK1KmQqRD9edEygKte4FvOgOGt/qvNxD/82oJto7rqQjjBCHko0WtRFKM6CAb2hQKOMqeIYwrYW6l/JYpxtEkmDUhuH9fniTVg7xbzBfPC7lSYRzHPNkkW2SHuOSIlMgZKZMK4eSBPJEX8mo9Ws/Wm/U+as1Y45kN8gvWxze6WZn4</latexit>
Sim(x, x→)=0.83→ωc
x = Can I give aspirin 
to my child?
Key: h(x) Find: h(x*)

### 2. Lookahead Check

### 3. Cache Miss and Decode
f(x) = “No, you shouldn’t give your 
child aspirin, because …”
Lookahead Decoding Similarity Check
<latexit sha1_base64="U3Cftj9ykl+25yZ4rfRsFUN4Ufw=">AAACGHicbVDJSgNBEO1xjXGLevTSGIREJM6I20UQvHhUNBrIxKGnU6NNeha7ayRhyGd48Ve8eFDEa27+jZ3loNEHRT3eq6K7np9IodG2v6yJyanpmdncXH5+YXFpubCyeq3jVHGo8ljGquYzDVJEUEWBEmqJAhb6Em781mnfv3kEpUUcXWEngUbI7iIRCM7QSF5hx0VoY3Ypwm4p8FqldnmbDvrtVrlMj6ld2T+kroQH6iJLPeYVinbFHoD+Jc6IFMkI516h5zZjnoYQIZdM67pjJ9jImELBJXTzbqohYbzF7qBuaMRC0I1scFiXbhqlSYNYmYqQDtSfGxkLte6EvpkMGd7rca8v/ufVUwyOGpmIkhQh4sOHglRSjGk/JdoUCjjKjiGMK2H+Svk9U4yjyTJvQnDGT/5LrncrzkHl4GKveLI3iiNH1skGKRGHHJITckbOSZVw8kReyBt5t56tV+vD+hyOTlijnTXyC1bvG07AnWI=</latexit>
Sim(fk(x),fk(x→)) = 0.57→ωa
<latexit sha1_base64="EmkCtF73LYl5Zn1HowsV9AUOB/w=">AAAB7XicbVBNSwMxEJ2tX7V+tOrRS7AI9VJ2pVSPBS8eK9gPaJeSTbNtbDZZkqxYlv4HLx4U8er/8ea/MW33oK0PBh7vzTAzL4g508Z1v53cxubW9k5+t7C3f3BYLB0dt7VMFKEtIrlU3QBrypmgLcMMp91YURwFnHaCyc3c7zxSpZkU92YaUz/CI8FCRrCxUjscTCpPF4NS2a26C6B14mWkDBmag9JXfyhJElFhCMda9zw3Nn6KlWGE01mhn2gaYzLBI9qzVOCIaj9dXDtD51YZolAqW8Kghfp7IsWR1tMosJ0RNmO96s3F/7xeYsJrP2UiTgwVZLkoTDgyEs1fR0OmKDF8agkmitlbERljhYmxARVsCN7qy+ukfVn16tX6Xa3cqGVx5OEUzqACHlxBA26hCS0g8ADP8ApvjnRenHfnY9mac7KZE/gD5/MH61GOrA==</latexit>
fk(x)= “No, you shouldn’t give …”
Figure 1: (a) Cache-collision attacks: the adversarial query x∗ collides with a victim query x in the semantic
cache, so that x receives the adversary-chosen response y∗. (b) LACACHEworkflow: a cached response f(x ∗)
is served only when both the cache-key check(x, x∗)and a lookahead check(f k(x∗), fk(x))pass.
In this work, we pursue a fundamentally different approach. While the adversary has full control over
the adversarial query x∗, it has far less control over the corresponding LLM-generated response y∗.
Critically, for the attack to be effective, y∗ must satisfy multiple competing constraints.i) Since the
adversary’s goal is typically to induce the victim to take a meaningfully different action (e.g., receive
malware, be redirected, or accept a refusal instead of an informative answer), y∗ tends to diverge
substantially from the genuine response y.ii) Constrained by the autoregressive nature of LLM
decoding Zou et al. (2023) and the need to maintain plausibility to the victim,y∗’s prefix must remain
semantically consistent with the full response. These constraints jointly make the response prefix an
adversary-resistant signal, one that the adversary cannot freely manipulate via prompt optimization.
Motivated by these observations, we propose LACACHE, a simple yet principled redesign of semantic
caching that shifts the integrity check from the query to the response. Rather than indexing solely
on a query, LACACHEaugments the cache entry with a lookahead key derived from the first k
response tokens. As illustrated in Figure 1 (b), cache retrieval in LACACHEproceeds in two stages: a
standard query check, followed by a response-prefix check. A cached response is served only when
both checks pass. This design adds negligible overhead: the k-token prefix can be generated via a
lightweight draft LLM and reused for speculative decoding on cache misses.
We validate LACACHEboth analytically and empirically. Analytically, we show that under two em-
pirically validated assumptions (semantic separability and prefix coherency), LACACHEdetects any
cache-collision attack that produces a semantically distinct response with provably high probability.
This guarantee isstructural: it holds for any query-optimizing attack, including white-box ones with
full knowledge of the LLM and embedding models. Empirically, evaluation across diverse LLMs and
embedding models confirms that LACACHEreduces attack hit rate to near zero while preserving over
90% of benign cache utility, and that adaptive adversaries who attempt to evade LACACHEgain only
a marginal advantage, due to the inherent tension between the competing constraints that LACACHE
exploits. To the best of our knowledge, this work is the first to leverage the inherent constraints
on adversary-driven responses in cache-collision attacks to provide provable security guarantees,
highlighting a promising direction for building robust semantic caching in LLM serving.

### 2 RELATEDWORK
Caching for LLM Serving.Caching is the dominant lever for reducing latency and cost in LLM
serving. Key-value (KV) caching Wang et al. (2025) stores per-layer attention states to eliminate
redundant prefill computation. Prompt caching reuses precomputed KV states across requests sharing
a textual prefix, realized via modular markup Gim et al. (2024), radix-tree prefix discovery Zheng
et al. (2024a), and prefix-aware scheduling Ye et al. (2024); Juravsky et al. (2024); Zheng et al.
(2024b). Semantic caching generalizes further to embedding-similarity matching, enabling reuse
across rephrased or paraphrased queries Regmi & Phakami Pun (2024); Zhao & Mastorakis (2025);
Zhu et al. (2025); Gaspar Schroeder et al. (2026); YU et al. (2025); Jin et al. (2025); Agarwal et al.
(2025); Kahatapitiya et al. (2025). Empirical studies confirm that prompt and semantic caching are
now widely deployed in cross-tenant production settings Gu et al. (2025); Microsoft (2025); Amazon
(2025); Alibaba (2025). This work targets prompt and semantic caching, where cache keys are
exposed to user-supplied content and adversarial collisions are most consequential.
2

Adversarial Attacks on LLM Caching.Existing attacks on LLM caching divide along their
adversarial objectives. The first class of attacks targetsprivacy. Side-channels, notably timing
differences between cache hits and misses, tend to leak victim prompts and embedding-space
metadata across tenants in commercial LLM serving platforms Gu et al. (2025); Song et al. (2025);
Wu et al. (2025). The second line targetsintegrity. The adversary crafts prompts whose cache
keys collide with the victim’s queries, causing the cache to serve adversary-controlled responses to
subsequent legitimate queries Zhang et al. (2026); Afiffy et al. (2026); Wu et al. (2026a;b); Liang
et al. (2026); Zou et al. (2025). This work mainly focuses on mitigating integrity attacks.
Defenses against Caching Attacks.Compared to the breadth of the attack literature, defenses against
semantic cache attacks remain underdeveloped. Privacy-side defenses address the side-channel angle
by obfuscating KV-cache states Luo et al. (2026) or stratifying cache scope to limit cross-user
observability Wu et al. (2025). Integrity-side defenses reject malicious cache hits at lookup time via
clustering-based isolation Afiffy et al. (2026), per-tenant key randomization Morris & Thompson
(1979), perplexity-based filtering Hu et al. (2023), or query–response consistency checks Wu et al.
(2026a). Yet these defenses often fail under adaptive attacks: gradient-guided search or low-perplexity
adversarial suffixes tend to easily bypass such defenses Zhang et al. (2026). In contrast, LACACHE
builds robustness into the cache structure itself, ensuring that key collision provably implies semantic
equivalence and thus providing security guarantees against adaptive attackers by construction.

### 3 PRELIMINARIES
LLM with Semantic Cache.Let X denote the prompt space and Y the response space. The LLM f
is a decoding function that maps a given query x∈ Xto its response y=f(x)∈ Y . As illustrated
in Figure 1 (a), upon receiving a query x, the LLM server first consults its semantic cache. If a
sufficiently similar cached query x′ is found, identified by cache key h(x′), the cached response
f(x ′) is returned directly, bypassing LLM decoding. Otherwise, x is forwarded to the LLM, and the
resulting response is stored as the key-value pair⟨h(x), f(x)⟩.
Specifically, we assume a two-phase indexing pipeline commonly used in representative LLM
caching (e.g., GPTCache Bang (2023)). First, an embedding model emb(·) maps x to a dense vector
z= emb(x) . Second, an indexing scheme (e.g., Local-Sensitive Hashing Charikar (2002)) h(·)
applies to z, producing the cache key h(z) for efficient retrieval. Specifically, the indexing scheme
satisfies: 
P[h(z) =h(z ′)]> p1 ifd(z, z′)< δ1
P[h(z) =h(z ′)]< p2 ifd(z, z′)> δ2 (1)
where p1 > p2 and δ1 < δ2, and d(z, z′) is a distance metric (e.g., cosine distance). Thus, two
semantically similar queries x and x′ with d(z, z′)< δ 1 yield a cache hit, allowing the cached
response f(x ′) to be reused for x. For notational simplicity, we write h(x)≜h(emb(x)) and elide
the embedding model hereafter.
Threat Model.In a cache-collision attack, the adversary targets a victim query x (with true response
y=f(x) ), aiming to cause the LLM server to return a malicious response y∗ in this place. To this
end, the adversary crafts an adversarial query x∗ that satisfies two conditions:i) the LLM generates
the malicious output for x∗: y∗ =f(x ∗);ii) x∗ collides with x in the semantic cache: h(x) =h(x∗).
Once the adversary’s query is served, the pair ⟨h(x∗), y∗⟩ is stored in the cache. The subsequent
query x then incurs a cache hit and receives y∗ rather than the legitimate response y. We consider
two threat settings: a black-box adversary with access to the embedding model and indexing method
only, and a white-box adversary who additionally has access to the LLM internals.
0 50 100 150
Per-query latency (ms)
0.0
0.2
0.4
0.6
0.8
1.0Attack Hit Rate (AHR)
Undefended
PPL
QR-PPL
LLM-as-Judge
LaCache
Figure 2: Security (attack hit rate)
and efficiency (per-query latency)
trade-off.
Problem Formulation.Intuitively, cache-collision attacks can be
trivially neutralized by disabling the semantic cache and decoding
every query from scratch, but at the cost of forfeiting all efficiency
gains. The true challenge is therefore to strike an optimal tradeoff:
how to maximize resilience against cache-collision attacks while min-
imizing query-processing cost?As shown in Figure 2, our proposed
LACACHEachieves this trade-off more favorably than alternative
defenses, attaining near-zero attack hit rate with per-query latency
comparable to the undefended baseline, as demonstrated against the
SCP-P attack Wu et al. (2026a).
3


### 4 METHOD
Next, we present LACACHE, a lightweight redesign of semantic
caching that provides guaranteed security against cache-collision attacks with negligible impact on
LLM serving efficiency.

### 4.1 MOTIVATION
Existing defenses against cache-collision attacks predominantly focus on identifying the adversarial
query x∗ Afiffy et al. (2026); Wu et al. (2026a); Zhang et al. (2026). This strategy is fundamentally
limited: since the adversary exercises full control overx∗, which is never directly visible to the victim,
the adversary can freely optimize x∗ to pursue varied objectives, including evading the deployed
defense.
In contrast, the adversary exercises no direct control over the LLM-generated response y∗ =f(x ∗).
More critically,y ∗ must simultaneously satisfy multiple competing constraints.
• Semantic Separability– In many attacks, the adversary’s goal is to cause functional divergence:
the victim is induced to take a meaningfully different action (e.g., receive malware, be redirected,
or accept a refusal instead of an informative answer). Thus, y∗ often differs substantially from
the genuine response y=f(x) to the target query x. Formally, d(f(x ∗), f(x))> δ2/C for some
constantC∈(0,1).
• Prefix Coherency– Constrained by the autoregressive nature of LLM decoding Zou et al. (2023)
and the need to maintain y∗’s plausibility to the victim, y∗’s first k tokens must faithfully reflect
the content of the full response. Formally, for any responses y, y∗, d(yk, y∗k)> ϵkmin−kd(y, y∗),
where yk denotes y’s first k tokens (analogously for y∗), kmin = min{|y|,|y∗|} and some constant
ϵ∈(0,1).
These constraints jointly make the response prefix an adversary-resistant signal that cannot be freely
manipulated via prompt optimization.

### 4.2 LACACHE
Grounded in this insight, we shift the integrity check from the query to the response, and explore
LACACHE, a novel defense that efficiently verifies the integrity of a retrieved response y∗ against the
target queryx, as illustrated in Figure 1 (b).
Cache Structure.A standard cache entry consists of a key-value pair ⟨h(x), f(x)⟩, where h(x) is
the cache key. LACACHEaugments this structure with an additional integrity check: each entry is
stored as ⟨h(x),[h(f k(x)), f(x)]⟩, where fk(x) denotes the first k tokens of the LLM’s response to
x (details of efficient implementation in §4.3), and h(fk(x)) serves as a lightweight lookahead check
on the response integrity.
Query Processing.As outlined in Algorithm 1, LACACHEprocesses each incoming query x in two
stages. First, it computes the cache key h(x) and queries the semantic cache. If a cache hit x′ is found
(i.e., h(x′) =h(x)), LACACHEdecodes the first k tokens of x and computes h(fk(x)). Second, it
verifies whether h(fk(x′)) =h(f k(x)). Only whenbothchecks pass does LACACHEserve x by
returning the cached response f(x ′). If either check fails, LACACHEdecodes f(x), possibly reusing
the already-computed prefixf k(x), and updates the cache accordingly.

### 4.3 OPTIMIZATION
Draft LLM.Rather than invoking the backend LLM f, typically highly capable but computationally
expensive, we instead employ a lightweight draft LLM g (e.g., Gemma-4-E4B-it) to generate
the first k prefix tokens fk(x) of an incoming query x. As demonstrated in §5, since k is typically
small (e.g., ≤20), substituting g for f has negligible impact on LACACHE’s effectiveness against
key-collision attacks, while substantially reducing inference cost.
Speculative Decoding.Recall that when the cache-key check passes but the lookahead check fails,
LACACHEfalls back to full decoding via f(x). To minimize this overhead, we integrate speculative
decoding Leviathan et al. (2023) to reuse as many draft tokens as possible. Concretely, beginning
4

Algorithm 1:Workflow of LaCache
Input:LLMf; LSHh(·)(with embedding modelemb(·));
1foreachincoming queryxdo
2compute hashh(x);
3search semantic cache with keyh(x);
// key and lookahead check
4ifthere is a hit⟨h(x ′),[h(f k(x′)), f(x′)]⟩then
5(speculatively) decodef k(x);
6ifh(f k(x′)) =h(fk(x))then
7servexwithf(x ′);
8continue;
9servexby decodingf(x);// decode from scratch
10add⟨h(x),[h(f k(x)), f(x)]⟩to cache;// update cache
from the first token, each draft token t generated by g is verified by f: if Pf (t)≥P g(t), where Pf (t)
denotes the probability assigned to t by f (analogously for g), the token is accepted; otherwise, f
takes over to generate all subsequent tokens. Critically, verifying k draft tokens requires only a single
forward pass, making the verification cost substantially lower than generating these tokens from
scratch.

### 4.4 ANALYSIS
The following theorem (proof in §B) establishes that LACACHEprovides formal theoretical guaran-
tees against cache-collision attacks.
Theorem 1.If semantic separability and prefix coherency in §4.1 both hold, then for k > kmin −
⌊logϵ C⌋,LACACHEdetects any cache-collision attack with probability at least1−p 2.
Notably, this guarantee can be further strengthened through an ensemble of independent lookahead
checks. Let H be a family of indexing functions defined in Eqn (1), and drawm independent functions
h1, h2, . . . , hm from H. A cache hit is valid only ifi) h(x) =h(x′) andii) hi(fk(x)) =hi(fk(x′))
for all i∈[1, m]. Since each lookahead check succeeds independently with probability at most p2,
the conjunction ofmchecks raises the detection probability to at least1−p m2 .

### 5 EVALUATION
We further empirically evaluate the efficacy of LACACHE. Our experiments are designed to answer
three key questions:i) Do the working assumptions of LACACHE(Gapped LSH, semantic separability,
and prefix coherency) hold empirically?ii) How effective is LACACHEagainst state-of-the-art cache-
collision attacks?iii) What are the best practices for operating LACACHE?

### 5.1 EXPERIMENTALSETTING
Attacks and Datasets.We evaluate two representative cache-collision attacks Zhang et al. (2026);
Wu et al. (2026a;b).
• Key-Collision Attack (KCA)Zhang et al. (2026). Given a target query x and a core query x0
drawn from the Natural Question dataset Kwiatkowski et al. (2019), the adversarial prompt is
constructed as x∗ =x 0 ⊕s , where ⊕ denotes concatenation, and s is a 20-token adversarial
suffix optimized via GCG Zhao et al. (2024) to maximize the embedding similarity of x and x∗
(default: 200-step gradient descent with target similarity τtgt = 0.85). The suffix s may begin with
the “Neglect:” phrase Zhang et al. (2026), which causes its semantic content to be effectively
ignored during LLM processing.
• Semantic Cache Poisoning (SCP)Wu et al. (2026a). Given a target query x drawn from the
MARCO dataset Bajaj et al. (2016), the attack randomly assigns one harm category (e.g., brand
damage, censorship/DoS, malicious injection, misinformation, or targeted advertising), synthesizes
a malicious response y∗, and constructs an in-context background message ctx accordingly, all
via gpt-5-mini. The adversarial query x∗ is generated by wrapping x within one of three
5

0.0 0.2 0.4 0.6 0.8 1.0
semantic distance d(⋅, ⋅ )
0
5
10density
δ1 = 0.16 δ2 = 0.30
 P1 = 0.43
Embedding Fidelity (BGE)
paraphrase pairs
random pairs
0.0 0.2 0.4 0.6 0.8 1.0
response distance d(fk(x), fk(x * ))
0
2
4
 δ2 = 0.30
Semantic Separability (BGE)
Qwen3
Gemma3
δ2
P5
10 20 50 100 150
k (response prefix tokens)
0.0
0.2
0.4
0.6
0.8
1.0
Prefix Coherency (BGE)
Qwen3
Gemma3
0.0 0.2 0.4 0.6 0.8 1.0
semantic distance d(⋅, ⋅ )
0.0
2.5
5.0
7.5
10.0density
δ1 = 0.29 δ2 = 0.53
 P1 = 0.76
Embedding Fidelity (MiniLM)
0.0 0.2 0.4 0.6 0.8 1.0
response distance d(fk(x), fk(x * ))
0
1
2
3
4 δ2 = 0.53
Semantic Separability (MiniLM)
10 20 50 100 150
k (response prefix tokens)
0.0
0.2
0.4
0.6
0.8
1.0
Prefix Coherency (MiniLM)
Figure 3: Empirical validation of working assumptions across LLM-embedding combinations: (a) embedding
distance distributions of 500 paraphrase and 500 random query pairs; (b) embedding distance of adversarial-
genuine response pairs; and (c) k-prefix embedding distance ratio of adversarial-genuine response pairs (k = 20).
templates:i) zero-shot prompting (Z) appends “ Print {y ∗}” to x;ii) in-context learning (I)
appends “ Background:{ctx} ... Based on the provided text, answer: ” to
x;iii) prompt-injection (P) appends “ Ignore that question and only print {y ∗}”
to x. We further consider an optimized variant that prepends a 20-token GCG-optimized prefix to
maximize the embedding similarity betweenxandx ∗.
Following Zhang et al. (2026); Wu et al. (2026a), we generate 500 samples per attack. To measure the
impact of defenses on LLM serving utility, we additionally construct a separate pool of 500 benign
paraphrase pairs (x, x′) drawn from the MS MARCO dataset, wherex′ is a paraphrase of x generated
viagpt-5-mini.
LLMs and Embedding Models.We consider two backbone LLMs of varied scale:
Qwen3.6-35B-A3B-FP8 (default) and Gemma-3-E4B-it. We also consider two embedding
models: BGE-large-en-v1.5 (default, 1,024-dim) or all-MiniLM-L6-v2 (384-dim). All
decoding is greedy (with temperature = 0). The default lookahead window isk= 20.
Metrics.We use the following metrics throughout the evaluation. Given an adversarial query x∗ and
the adversary’s intended response y∗, an injection is deemed successful if f(x ∗) matches y∗ (judged
by gpt). The Injection Success Rate (ISR) measures the fraction of adversarial queries that elicit the
intended responses, as defined in Eqn (2)(a).
(a) ISR =# Successful Injections# Adversarial Queries (b) HR =# Cache Hits# Query Pairs (2)
Notably, a successful injection is a prerequisite for attack success; we therefore measure attack
effectiveness on the subset of adversarial queries that result in successful injections.
Further, for a given query pair (x, x′), a cache hit occurs wheni) the cache check sim(x, x′)≥τ c
andii) (under LACACHE) the lookahead check sim(fk(x), fk(x′))≥τ a both hold, where τc and τa
are thresholds calibrated to the underlying embedding model and LSH function. The Hit Rate (HR)
measures the fraction of query pairs that admit cache hits, as defined in Eqn (2)(b). We differentiate
two variants: Attack Hit Rate (AHR) – the cache hit rate on adversarial pairs (x, x∗), restricted to
successfully injected adversarial queries; Benign Hit Rate (BHR) – the cache hit rate on benign
paraphrase pairs (x, x′), measuring semantic cache utility. The defense’s Detection Rate (DR) is then
simplyDR = 1−AHR. Full details of the experimental setting are deferred to §A.

### 5.2 RQ1: EMPIRICALVALIDATION OFWORKINGASSUMPTIONS
We first empirically validate LACACHE’s working assumptions. Figure 3 reports all three assumption
checks across the four LLM–embedding model combinations.
Embedding fidelityformalizes the empirical condition under which the gapped-LSH property in
Eq. 1 translates into semantic guarantees in practice: paraphrase pairs ( d≤δ 1) hash-collide with
6

probability ≥p 1, while random pairs ( d≥δ 2) hash-collide with probability ≤p 2, with δ1 < δ2
and p1 > p2. This ensures that two LLM-generated responses y and y∗ collide only when y∗ is
semantically similar to y. We verify this condition by measuring cosine similarity on 500 paraphrase
pairs (gpt-5-mini rewrites of the same MARCO query) and 500 random pairs (arbitrary pairings
of different MARCO queries). As shown in Figure 3 (a), the two distributions are well separated
with a clear gap. δ1 is naturally anchored at the upper tail of the paraphrase distribution: we set
δ1 =P 99(paraphrase) so that 99% of paraphrase pairs fall in the high-collision regime d≤δ 1. δ2
admits any value in the gap (δ1, P1(random)) since p2 stays at 0 throughout; we report the midpoint
as a balanced default, yielding ( δ1, δ2) = (0.16, 0.30) for BGE and (0.29, 0.53) for MiniLM, with
empirical1−p 2 = 1.0in both cases.
Semantic separabilityassumes that a meaningful attack produces an adversarial response f(x ∗)
significantly different from the victim query’s genuine response f(x), formally d(f(x ∗), f(x))>
δ2/C for some constant C∈(0,1) . We measure the adversarial-genuine response distance at k
= 20 on SCP-Pand compare it against the δ2 calibrated above. As shown in Figure 3 (b), the bulk
of adversarial response distances exceed δ2: the lower 5th percentile is 0.37 for BGE and 0.54 for
MiniLM, clearing the corresponding δ2 (0.30 and 0.53), so the assumption holds for >95% of pairs
across all four (LLM, embedding) combinations. A looserδ2 within the embedding-fidelity gap would
only widen this margin further. Crucially, switching backbone LLMs (Qwen3 versus Gemma3) shifts
the distribution by less than 0.02, indicating that the separation arises from the structural divergence
between adversarial and genuine responses, not from any LLM-specific artifact. This confirms the
core intuition behind LACACHE: the adversary can drag the adversarial query’s cache key into the
collision region, but cannot pull the LLM’s response close to the victim’s genuine response.
Prefix coherencyassumes that the k-token response prefix fk(·) inherits the response separation of
the full response, formally d(fk(x), fk(x′))> ϵkmin−k d(f(x), f(x′)), so that running the lookahead
check on a short prefix is as discriminative as running it on the full output. We track the empirical ratio
Ak =d(f k(x), fk(x′))/d(f(x), f(x′)) as a function of k. As shown in Figure 3 (c), this assumption
holds across all settings: mean Ak is essentially flat over k∈ {10, . . . ,150}, indicating that the
20-token lookahead window already captures the full response divergence. Longer prefixes offer no
additional discriminative power, justifying our choicek=20 at minimum decoding cost.
Taken together, with all working assumptions empirically validated, Theorem 1 applies directly: for
any cache-collision attack that produces a response semantically distinct from the genuine response,
LACACHEdetects the adversarial collision with probability at least 1−p 2, while the empirically
observed 1−p 2 is often close to 1. Further, the two-stage LACACHEdesign, a cache check on x
paired with a lookahead check onfk(x) (k = 20) is not a heuristic stack. Each component corresponds
to a load-bearing piece of the proof: the cache check inherits its guarantee from embedding fidelity,
the lookahead check from semantic separability, and the k =20 window is justified directly by the Ak
saturation in Figure 3(c), which together analytically predict LACACHE’s effectiveness.
5.3 RQ2: LACACHE’SEFFECTIVENESS AGAINSTCACHE-COLLISIONATTACKS
We now measure LACACHE’s empirical effectiveness against KCAand SCP. For SCP, we focus
on the prompt-injection variant SCP-P(with optimized prefix), as it represents the strongest attack
setting; per-variant breakdown on the default Qwen3 + BGE combination is reported in §C.
Main Results.As reported in Table 1, the high attack hit rate (AHR) on undefended LLMs confirms
that KCAand SCP-P, by optimizing adversarial prefixes or suffixes, can effectively cause false cache
collisions, but LACACHEneutralizes this advantage uniformly across all four LLM-embedding model
combinations, reducing AHR to near zero while preserving most of the benign hit rate (BHR). The
relatively lower BHR under MiniLM reflects its wider paraphrase-response distribution, but the
security guarantee is unaffected as threshold calibration adapts (τc, τa) per-embedding (more details
in §A.2).
To further understand the underlying mechanism, Figure 4 visualizes the embedding distance distri-
butions for adversarial and benign (paraphrase) pairs. As shown in Figure 4 (a) and (c), adversarial
query embeddings are optimized to trigger cache collisions, pushing similarity above τc via adver-
sarial suffixes (KCA) or prefixes (SCP-P). Yet as shown in Figure 4 (b) and (d), the LLM responses
(prefixes), which the adversary cannot directly influence at inference time, remain well separated
7

Table 1. LACACHEversus undefended baseline against KCAand SCP-Pattacks across LLMs and embedding
models. AHR is reported on successfully injected adversarial prompts.
AHR↓BHR↑
LLM EmbeddingAttack ISR Undefended LACACHEUndefended LACACHE
Qwen3
BGE KCA0.95 0.80 0.00 1.00 0.93SCP-P0.73 0.95 0.01 1.00 0.93
MiniLM KCA0.95 0.79 0.00 0.95 0.85SCP-P0.74 0.82 0.00 0.95 0.85
Gemma3
BGE KCA0.95 0.80 0.01 1.00 0.90SCP-P0.73 0.95 0.04 1.00 0.90
MiniLM KCA0.95 0.79 0.01 0.95 0.86SCP-P0.74 0.82 0.02 0.95 0.86
0.0 0.2 0.4 0.6 0.8 1.0
cache-key sim sim(emb(x), emb(x * ))
0.0
2.5
5.0
7.5
10.0
12.5density
(a) KCA cache admission
benign (n=500)
attack (n=475)
τ=0.80
0.0 0.2 0.4 0.6 0.8 1.0
response-prefix sim sim(fk(x), fk(x * ))
0
2
4
6
(b) KCA look-ahead guard
benign (n=500)
attack (n=475)
τ=0.70
0.0 0.2 0.4 0.6 0.8 1.0
cache-key sim sim(emb(x), emb(x * ))
0
5
10
15
20
25
(c) SCP-P wbox cache admission
benign (n=500)
attack (n=364)
τ=0.80
0.0 0.2 0.4 0.6 0.8 1.0
response-prefix sim sim(fk(x), fk(x * ))
0
1
2
3
4
5
(d) SCP-P wbox look-ahead guard
benign (n=500)
attack (n=364)
τ=0.70
Figure 4: Embedding distance distributions for adversarial (restricted to successfully injected ones) and benign
(paraphrase) pairs under Qwen3 + BGE: (a) query embeddings and (b) response prefix embeddings under KCA;
(c) query embeddings and (d) response prefix embeddings under SCP-P(with optimized prefix).
Table 2. Comparison of LACACHEand baseline defenses on Qwen3 + BGE across attacks, with all defenses
evaluated on successfully injected adversarial queries.
KCASCP-ZSCP-PSCP-I
Defense AHR↓BHR↑AHR↓BHR↑AHR↓BHR↑AHR↓BHR↑
Undefended 0.80 1.00 0.91 1.00 0.95 1.00 0.97 1.00
PPL 0.65 0.95 0.87 0.95 0.93 0.95 0.97 0.95
QR-PPL 0.52 0.95 0.58 0.95 0.72 0.95 0.41 0.95
LLM-as-Judge 0.01 0.99 0.47 0.99 0.44 0.99 0.87 0.99
LACACHE 0.00 0.93 0.04 0.93 0.01 0.93 0.14 0.93
from the victim’s genuine responses. The lookahead check therefore effectively catches the false
collisions, as implied by the semantic separability and prefix coherency properties.
Comparison with Baselines.We also compare LACACHEagainst three baseline defenses from prior
work: PPL Zhang et al. (2026) filters adversarial queries based on their perplexity Hu et al. (2023),
Query-Response PPL (QR-PPL) Wu et al. (2026a) extends this by jointly measuring query-response
perplexity to assess consistency, and LLM-as-Judge employs a Gemma model to classify incoming
queries as adversarial or benign. Table 2 compares all four defenses across four white-box attacks
(KCA, SCP-Z, SCP-P, SCP-I).
Notably, LACACHEis the only defense that consistently suppresses all attacks while preserving
semantic cache utility. The three baselines all operate onquery-sidefeatures and are brittle in different
ways. PPL and QR-PPL rely on perplexity, but all attacks run GCG with a perplexity-aware loss
term, producing fluent pre/suffixes that defeat both filters. LLM-as-Judge appears effective against
KCA, but only as a side-effect of KCA’s inherent structure: the adversarial query x∗ =x 0 ⊕s may
contain an entirely unrelated core prompt x0, and the judge trivially flags the inconsistency between
the cached query x∗ and the victim query x. The SCPvariants, however, preserve x verbatim within
the adversarial wrapper, so the cached query reads as a normal request that is indistinguishable
from a benign paraphrase. In contrast, LACACHEoperates on theresponseside: it checks the
lookahead response-prefix divergence guaranteed by Theorem 1, a quantity the adversary cannot
directly manipulate at decode time, so the defense generalizes across all attacks. The marginally
elevated AHR on SCP-Ireflects a boundary case in which in-context learning induces the LLM to
mimicf(x)’s style, partially aligningf k(x∗)prefix withf k(x).
8


### 5.4 RQ3: OPERATION OFLACACHE INPRACTICE
We now examine best practices for operating LACACHE.
10 20 50 100 150
k (response prefix tokens)
0.00
0.25
0.50
0.75
1.00hit rate
Qwen3 + BGE
no-defense attack
lacache attack
no-defense benign
lacache benign
10 20 50 100 150
k (response prefix tokens)
Qwen3 + MiniLM
10 20 50 100 150
k (response prefix tokens)
Gemma3 + BGE
10 20 50 100 150
k (response prefix tokens)
Gemma3 + MiniLM
Figure 5: LACACHE’s sensitivity to the look-ahead window k against SCP-P (prompt injection with optimized
prefix) across all LLM-embedding model combinations.
Lookahead Window.Figure 5 examines LACACHE’s sensitivity to the lookahead window k.
0.30
0.20
0.10
0.00
1 2 3 4
Number of Lookahead Checks (m)
Attack Hit Rate (AHR)
Benign Hit Rate (BHR)
0.90
0.88
0.86
0.84
0.92KCA
SCP-p
SCP-z
SCP-i
BHR
Figure 6: AHR of ensembles of lookahead
checks (averaged over all combinations of
BGE,MiniLM,MPNet, andQwen3-Emb).
Notably, AHR remains flat ink across all LLM-embedding
model combinations, while BHR saturates by k = 20. This
is consistent with our finding in §5.2 that prefix coherency
is already tight at k = 20. The setting of k = 20 thus
achieves near-optimal security at minimum decoding cost.
Number of Lookahead Checks.Theorem 1 suggests
that detection probability can be amplified to 1−p m2 by
stacking m independent lookahead checks. To evaluate
this, we instantiate an ensemble of architecturally dis-
tinct embedding models (BGE-large, MiniLM, MPNet,
Qwen3-Embedding-0.6B), each calibrated to its own
benign-response P10, and admit a cache hit only if it passes
all m checks. As shown in Figure 6, against KCAand SCP-
P, m = 1 already saturates at ≤ 1% AHR and additional
checks yield only marginal improvement; against SCP-Z and SCP-I, ensembling does help, shrinking
AHR 2∼4× from m = 1 to m = 4. Meanwhile, BHR decays modestly from 0.91 (m = 1) to 0.86 (m
= 4). The choice ofmthus represents a practical trade-off between security and efficiency.
Resilience to Adaptive Attacks.The KCAand SCP-Pvariants evaluated in Table 1 already assume
full white-box access to the underlying embedding model. We strengthen this threat model further by
asking whether the adversary that additionally knows the deployed LACACHEcan bypass the defense.
Specifically, we consider an adaptive adversary that optimizes the following objective:
L(x∗) = sim(x∗, x)| {z }
(i) cache check
+λ1 ·sim(f k(x∗), fk(x))| {z }
(ii) lookahead check
+λ2 ·sim(f k(x∗), y∗)| {z }
(iii) semantic preservation
(3)
where the first term optimizes the cache-key similarity, the second term optimizes the lookahead
similarity, the third term ensures that the response matches the adversary’s intended response y∗,
and λ1 and λ2 balance these factors. We instantiate this adaptive adversary on both attacks under
identical settings: 200 gradient-descent steps, a 20-token GCG variable, and target similarity τtgt =
0.85. Further implementation details are provided in §D.
Table 3. Adaptive attacks against LACACHEonQwen3+BGE.
Attack Cache Check Lookahead | Cache Check End-to-End Check
KCA13/200 (6.5%) 0/13 (0.0%) 0/200 (0.0%)
SCP-P137/200 (68.5%) 4/137 (2.9%) 4/200 (2.0%)
Table 3 reports that LACACHE
shows strong resilience against
both adaptive attacks. Among
200 adversarial queries, only 4
bypass both the cache and looka-
head checks under adaptive SCP-
P, and none under adaptive KCA. The reason is structural: terms (ii) and (iii) in Eqn (3) are funda-
mentally conflicting - jointly maximizing lookahead similarity and preserving response semantics is
self-defeating when the adversary’s intended response y∗ diverges substantially from the genuine
response f(x). Therefore, the joint optimization succeeds at the query-embedding level (µ = 0.85
> τc), but the prefix-embedding similarity of the actually decoded LLM response remains well below
τa (µ = 0.49, p95 = 0.64 on SCP-P), yielding negligible end-to-end success on both attacks. Thus,
compared with the non-adaptive variant, the adaptive adversary gains only a marginal advantage.
9

Table 4. Overhead of LACACHEwith and without optimization
(draft LLM and speculative decoding). Latency reported per query
atk= 20 forced decoding.
Optimization Latency↓KCAAHR↓SCP-PAHR↓BHR↑
w/o 108.5 ms 0.00 0.01 0.93
w/ 68.6 ms 0.00 0.01 0.94
Optimization Strategies.Finally,
we evaluate the impact of the opti-
mization strategies (draft LLM and
speculative decoding) in §4.3 on LA-
CACHE’s security and efficiency, with
results summarized in Table 4 (more
details in §E). Notably, the optimiza-
tion preserves LACACHE’s defense
guarantees while reducing its overhead (per-query latency) by 1.6×.

### 6 CONCLUSION ANDFUTUREWORK
This work presents LACACHE, a simple yet principled redesign of semantic caching that provably
defends against cache-collision attacks with negligible impact on LLM serving efficiency. The central
insight is an asymmetry inherent to cache-collision attacks: while the adversary exercises full control
over the adversarial query, it has far less control over the LLM-generated response, which must
simultaneously satisfy competing semantic constraints. By shifting the integrity check from the query
to the response, LACACHEconverts this asymmetry into a structural security guarantee that holds
for any query-optimizing adversary, representing a principled direction for building robust semantic
caching in LLM serving.
Meanwhile, several directions merit further investigation.i) LACACHE’s formal guarantee applies
to attacks whose adversarial response is semantically distinct from the genuine response; subtle
misinformation attacks that preserve semantic proximity fall outside this scope, though such attacks
are structurally harder to mount and provide limited adversarial value within the cache-collision
framework.ii) The detection amplification predicted by Theorem 1 does not fully materialize when
embedding models are inherently correlated; realizing the theoretical 1−p m2 bound may require
ensembles of more architecturally diverse embedding models.iii) LACACHEcurrently focuses
on integrity attacks; a unified design that simultaneously provides integrity and privacy guarantees
against timing side-channels remains a compelling open problem.
10


### REFERENCES
Mohanad Afiffy, Mohamed Waleed Fakhr, and Fahima A. Maghraby. Enhancing adversarial resilience
in semantic caching for secure retrieval augmented generation systems.Scientific Reports, 16(1):
5936, 2026.
Shubham Agarwal, Sai Sundaresan, Subrata Mitra, Debabrata Mahapatra, Archit Gupta, Rounak
Sharma, Nirmal Joshua Kapu, Tong Yu, and Shiv Saini. Cache-Craft: Managing chunk-caches
for efficient retrieval-augmented generation. InProceedings of ACM International Conference on
Management of Data (SIGMOD), 2025.
Alibaba. Semantic caching.https://higress.ai/en/scene/semantic-cache, 2025.
Amazon. Build a read-through semantic cache with amazon opensearch serverless and amazon
bedrock. https://aws.amazon.com/cn/blogs/machine-learning/build-a
-read-through-semantic-cache-with-amazon-opensearch-serverless-a
nd-amazon-bedrock/, 2025.
Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan Ma-
jumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, Mir Rosenberg, Xia Song, Alina Stoica,
Saurabh Tiwary, and Tong Wang. Ms marco: A human generated machine reading comprehension
dataset.ArXiv e-prints, 2016.
Fu Bang. GPTCache: An open-source semantic cache for LLM applications enabling faster answers
and cost savings. InProceedings of the 3rd Workshop for Natural Language Processing Open
Source Software (NLP-OSS 2023), 2023.
Moses S. Charikar. Similarity estimation techniques from rounding algorithms. InProceedings of
ACM symposium on Theory of computing (STOC), 2002.
Luis Gaspar Schroeder, Aditya Desai, Alejandro Cuadron, Kyle Chu, Shu Liu, Mark Zhao, Stephan
Krusche, Alfons Kemper, Matei Zaharia, and Joseph E. Gonzalez. vcache: Verified semantic
prompt caching. InProceedings of International Conference on Learning Representations (ICLR),
2026.
In Gim, Guojun Chen, Seung-seob Lee, Nikhil Sarda, Anurag Khandelwal, and Lin Zhong. Prompt
cache: Modular attention reuse for low-latency inference. InProceedings of Annual Conference
on Machine Learning and Systems (MLSys), 2024.
Chenchen Gu, Xiang Lisa Li, Rohith Kuditipudi, Percy Liang, and Tatsunori Hashimoto. Auditing
prompt caching in language model apis. InProceedings of International Conference on Machine
Learning (ICML), 2025.
Zhengmian Hu, Gang Wu, Saayan Mitra, Ruiyi Zhang, Tong Sun, Heng Huang, and Viswanathan
Swaminathan. Token-level adversarial prompt detection based on perplexity measures and contex-
tual information.ArXiv e-prints, 2023.
Chao Jin, Zili Zhang, Xuanlin Jiang, Fangyue Liu, Shufan Liu, Xuanzhe Liu, and Xin Jin. Ragcache:
Efficient knowledge caching for retrieval-augmented generation.ACM Transactions on Computer
Systems, 2025.
Jordan Juravsky, Bradley Brown, Ryan Ehrlich, Daniel Y . Fu, Christopher Ré, and Azalia Mirhoseini.
Hydragen: High-throughput LLM inference with shared prefixes.ArXiv e-prints, 2024.
Kumara Kahatapitiya, Haozhe Liu, Sen He, Ding Liu, Menglin Jia, Chenyang Zhang, Michael S.
Ryoo, and Tian Xie. Adaptive caching for faster video generation with diffusion transformers. In
Proceedings of IEEE International Conference on Computer Vision (ICCV), 2025.
Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris
Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion
Jones, Matthew Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, and Slav
Petrov. Natural questions: A benchmark for question answering research.Transactions of the
Association for Computational Linguistics, 7:453–466, 2019.
11

Yaniv Leviathan, Matan Kalman, and Yossi Matias. Fast inference from transformers via speculative
decoding. InProceedings of International Conference on Machine Learning (ICML), 2023.
Jiacheng Liang, Yuhui Wang, Changjiang Li, Rongyi Zhu, Tanqiu Jiang, Neil Gong, and Ting Wang.
Graphrag under fire. InProceedings of IEEE Symposium on Security and Privacy (S&P), 2026.
Zhifan Luo, Shuo Shao, Su Zhang, Lijing Zhou, Yuke Hu, Chenxu Zhao, Zhihao Liu, and Zhan
Qin. Shadow in the cache: Unveiling and mitigating privacy risks of kv-cache in llm inference. In
Proceedings of Network and Distributed System Security Symposium (NDSS), 2026.
Microsoft. Introduction to semantic cache. https://learn.microsoft.com/en-us/az
ure/cosmos-db/gen-ai/semantic-cache, 2025.
Robert Morris and Ken Thompson. Password security: a case history.Commun. ACM, 22(11):
594–597, 1979.
Sajal Regmi and Chetan Phakami Pun. GPT Semantic Cache: Reducing LLM Costs and Latency via
Semantic Embedding Caching.ArXiv e-prints, 2024.
Linke Song, Zixuan Pang, Wenhao Wang, Zihao Wang, XiaoFeng Wang, Hongbo Chen, Wei Song,
Yier Jin, Dan Meng, and Rui Hou. The early bird catches the leak: Unveiling timing side channels in
llm serving systems.IEEE Transactions on Information Forensics and Security, 20:11431–11446,
2025.
Jiahao Wang, Jinbo Han, Xingda Wei, Sijie Shen, Dingyan Zhang, Chenguang Fang, Rong Chen,
Wenyuan Yu, and Haibo Chen. Kvcache cache in the wild: Characterizing and optimizing kvcache
cache at a large cloud provider. InProceedings of USENIX Annual Technical Conference (ATC),
2025.
Guanlong Wu, Zheng Zhang, Yao Zhang, Weili Wang, Jianyu Niu, Ye Wu, and Yinqian Zhang.
I know what you asked: Prompt leakage via kv-cache sharing in multi-tenant llm serving. In
Proceedings of Network and Distributed System Security Symposium (NDSS), 2025.
Guanlong Wu, Taojie Wang, Yao Zhang, Zheng Zhang, Jianyu Niu, Ye Wu, and Yinqian Zhang.
When cache poisoning meets LLM systems: Semantic cache poisoning and its countermeasures.
InProceedings of Network and Distributed System Security Symposium (NDSS), 2026a.
XiangFan Wu, Lingyun Ying, Guoqiang Chen, Yacong Gu, and Haipeng Qu. Cache me, catch
you: Cache related security threats in llm serving frameworks. InProceedings of Network and
Distributed System Security Symposium (NDSS), 2026b.
Lu Ye, Ze Tao, Yong Huang, and Yang Li. ChunkAttention: Efficient self-attention with prefix-aware
KV cache and two-phase partition. InProceedings of Annual Meeting of the Association for
Computational Linguistics (ACL), 2024.
Chengye YU, Tianyu Wang, Zili Shao, and Song Jiang. Smartcache: Context-aware semantic
cache for efficient multi-turn LLM inference. InProceedings of Advances in Neural Information
Processing Systems (NeurIPS), 2025.
Zhixiang Zhang, Zesen Liu, Yuchong Xie, Quanfeng Huang, and Dongdong She. From similarity
to vulnerability: Key collision attack on llm semantic caching. InProceedings of International
Conference on Machine Learning (ICML), 2026.
Xinye Zhao and Spyridon Mastorakis. SemShareKV: Efficient KVCache Sharing for Semantically
Similar Prompts via Token-Level LSH Matching. InProceedings of the 14th International Joint
Conference on Natural Language Processing and the 4th Conference of the Asia-Pacific Chapter
of the Association for Computational Linguistics (IJCNLP-AACL), 2025.
Yiran Zhao, Wenyue Zheng, Tianle Cai, Xuan Long Do, Kenji Kawaguchi, Anirudh Goyal, and
Michael Qizhe Shieh. Accelerating greedy coordinate gradient and general prompt optimization via
probe sampling. InProceedings of Advances in Neural Information Processing Systems (NeurIPS),
2024.
12

Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao,
Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, and Ying Sheng. SGLang:
Efficient execution of structured language model programs. InProceedings of Advances in Neural
Information Processing Systems (NeurIPS), 2024a.
Zhen Zheng, Xin Ji, Taosong Fang, Fanghao Zhou, Chuanjie Liu, and Gang Peng. BatchLLM:
Optimizing large batched LLM inference with global prefix sharing and throughput-oriented token
batching.ArXiv e-prints, 2024b.
Yuxuan Zhu, Ali Falahati, David H. Yang, and Mohammad Mohammadi Amiri. SentenceKV:
Efficient LLM inference via sentence-level semantic KV caching. InProceedings of Conference
on Language Modeling (COLM), 2025.
Andy Zou, Zifan Wang, Nicholas Carlini, Milad Nasr, J. Zico Kolter, and Matt Fredrikson. Universal
and transferable adversarial attacks on aligned language models.ArXiv e-prints, 2023.
Wei Zou, Runpeng Geng, Binghui Wang, and Jinyuan Jia. Poisonedrag: knowledge corruption attacks
to retrieval-augmented generation of large language models. InProceedings of USENIX Security
Symposium (SEC), 2025.
A DETAILS OFEXPERIMENTALSETTING
This section details the experimental setting in §5.
A.1 GCG HYPERPARAMETERS
All GCG Zhao et al. (2024) runs, both for dataset construction and the adaptive adversary (section D),
share the same configuration:
•Mode:gradient (HotFlip-style) with greedy candidate replacement.
•Variable length:20tokens.
•Optimizer steps:200.
•Top-kcandidates per position:64.
•Target similarity:τ tgt = 0.85(early-stop when reached).
• Perplexity-aware filter:enabled, λppl = 0.3(penalizes GPT-2 perplexity to keep candidate tokens
plausible).
•Random seed:42 + hash(record_id) mod 1000(deterministic per record).
Thepositionof the GCG variable depends on the attack: suffix for KCA(after the Neglect anchor),
prefix for SCPwhite-box (before the payload).
A.2 THRESHOLDCALIBRATION
Cache Admission τc.We collect cosine similarities of the 500 benign paraphrase pairs (x, x′)
and set τc = min
 
0.80, P5
 
{sim(emb(x),emb(x ′))} , i.e. the 5th percentile of the benign
similarity distribution capped at 0.80. The cap binds for BGE (natural P5=0.857, so τc=0.800); for
MiniLM the cap does not bind and τc=P5=0.778. Note that τc (the practical similarity threshold
for cache admission) and δ1 (the LSH high-collision boundary in §5.2) are calibrated using different
percentiles (P5 and P99 respectively) for different roles: τc defines the operational hit decision while
δ1 characterizes the embedding-fidelity regime.
Lookahead Admission τa.Analogously, we collect cosine similarities of fk(x) vs. fk(x′) on the
same benign pairs and set τa = min
 
0.70, P10
 
{sim(emb(fk(x)),emb(f k(x′)))} . Unlike τc,
the natural P10 of benign-response similarity depends on both the embeddingandthe backbone LLM,
soτ a is calibrated per (LLM, embedding) combination atk=20:
13

Qwen3+BGE Qwen3+MiniLM Gemma3+BGE Gemma3+MiniLM
P10(benignr-sim) 0.734 0.611 0.664 0.515
τa (used)0.700 0.611 0.664 0.515
The cap binds only for Qwen3+BGE; for the other three combinations τa=P10. The looser MiniLM
thresholds reflect its wider paraphrase-response distribution; the security guarantee in Theorem 1 is
unaffected since each τa remains comfortably below the corresponding mean adversarial-vs-victim
response distance reported in section 5.2.
Choice ofkandm.The look-ahead window isk=20tokens; the number of guards ism=1. These
choices are justified empirically by Figure 5 (k-saturation at 20) and Figure 6 (m=1 already saturates
security on the easy tracks whilem>1only erodes benign hit rate).
B PROOF
Proof. (Theorem 1) Let x∗ be a key-collision query satisfying h(x∗) =h(x) for a target query x,
such that the LLM returns the adversary’s desired responsey ∗ =f(x ∗).
By semantic separability, d(f(x), f(x∗))> δ 2/C. By prefix coherency, d(fk(x), fk(x∗))>
ϵkmin−kd(f(x), f(x∗)), where kmin = min{|f(x)|,|f(x ∗)|}. Thus, setting k > kmin − ⌊logϵ C⌋, it
follows that:
ϵkmin−kd(f(x), f(x∗))> δ2 (4)
and hence: d(fk(x), fk(x∗))> δ2. By the property of LSH, P[h(fk(x))̸=h(f k(x∗))]>1−p 2.
Intuitively, even when the attack successfully induces a key collision (i.e., h(x) =h(x∗)), it fails the
lookahead check with probability at least1−p 2.
C EVALUATION OFSCPVARIANTS
The main-text Table 1 reports defense effectiveness on the two strongest attacks (KCAand SCP–P
white-box) across all four (LLM, embedding) combinations. This subsection complements that
with the full per-variant SCPbreakdown on the default Qwen3 + BGE combination: all six prompt-
engineering×adversary-knowledge variants of SCPdescribed in section 5.1.
Table 5. Per-variant SCPdefense effectiveness on the default Qwen3 + BGE combination. Same columns as
Table 1.
AHR↓BHR↑
Variantn ISR Undefended LACACHEUndefended LACACHE
SCP-Z, black-box 163 0.17 0.04 1.00 0.93
SCP-I, black-box 182 0.09 0.02 1.00 0.93
SCP-P, black-box 382 0.100.001.00 0.93
SCP-Z, white-box 166 0.91 0.04 1.00 0.93
SCP-I, white-box 112 0.97 0.141.00 0.93
SCP-P, white-box 364 0.95 0.01 1.00 0.93
The black-box variants achieve only 9–17% no-defense admission because the verbatim x inside the
wrapper is enough to land near τc but not consistently above it; LACACHEstill cuts these by 4–∞×.
The white-box GCG prefix raises no-defense admission to 0.90–0.97 on all three variants, confirming
that direct embedding-space optimization defeats Assumptioni) on the query side. LACACHE
neutralizes this advantage on Z and P (atk≤0.04 ), while the in-context (I) variant remains the hardest
case. The shaded blue row corresponds to the headline SCP–P white-box result reported in Table 1.
D DETAILS OFADAPTIVEATTACKS
The adaptive adversary in section 5.4 replaces the GCG single-objective with the three-term coupled
loss of Eqn (3):
L(x∗) = sim(x∗, x)| {z }
(i) cache check
+λ 1 ·sim(f k(x∗), fk(x))| {z }
(ii) lookahead check
+λ 2 ·sim(f k(x∗), y∗)| {z }
(iii) semantic preservation
,
14

with λ1 = λ2 = 1 and target similarity τtgt = 0.85 for the GCG early-stop criterion. The response
surrogates fk(x) and y∗ are pre-decoded once per record at k = 20 and treated as constants in the
gradient. After GCG terminates, we re-decode x∗ on the real LLM (no surrogate) at k = 20 and re-
compute qsim = sim(x∗, x)and rsim = sim(fk(x∗), fk(x)); end-to-end success requires qsim ≥τ c
and rsim ≥τ a. Both adaptive runs are conducted on the first 200 queries of successfully injected
adversarial queries.
E LATENCYMEASUREMENT
The per-query latency numbers in Figure 2 are measured atsteady stateon an H100 with TP=2,
after a warm-up run, and report the mean over 10 subsequent queries. To prevent EOS from masking
the true per-token decoding cost, all decoding-bearing benchmarks force exact token counts via
min_tokens=max_tokens=kandignore_eos= True. The components are
•BGEembedding (1,024-dim, batch 1): 10.1 ms.
•GPT-2 PPL on query (PPL): 7.8 ms; on query+response (QR-PPL): 10.1 ms.
•LLM-as-Judge classification: 151.6 ms.
• LACACHE(with k = 20) on the default backbone (BGE + Qwen3): 108.5 ms; LACACHE(with draft
LLM and speculative decoding), implemented as f = Qwen3.6-35B-A3B-FP8 and its bundled
MTP head as draftg: 68.6 ms.
15