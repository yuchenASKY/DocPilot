# The Effect of Text Chunk Size on Retrieval-Augmented Generation Performance

> **arXiv**: [2607.24767v1](https://arxiv.org/abs/2607.24767v1) ｜ **发布日期**: 2026-06-08 ｜ **分类**: cs.IR ｜ **页数**: 10

## 摘要

Retrieval-Augmented Generation (RAG) systems have emerged as a powerful process for allowing large language models (LLMs) to retrieve relevant information to use as source material during text generation. A critical yet under-explored component of these systems is the granularity at which source documents are segmented into retrievable chunks. The size of these chunks has the potential to significantly influence generation quality, contextual correctness, retrieval precision, and computational efficiency. Despite its importance, chunk size is often selected without proper evaluation of its impact on generation quality. Smaller chunks, such as individual sentences, may allow for precise retrieval by narrowing the focus of each chunk. However, they contain less information, which may limit the model's ability to generate coherent responses. Larger chunks, such as entire chapters, contain lots of broad information that may improve correctness, but also introduce additional noise and increase computational cost. Because larger chunks contain more information, the number of chunks returned to the model must also be considered. This paper evaluates how chunk size, along with the number of retrieved segments, influences generation quality and retrieval effectiveness. By comparing these configurations, this study seeks to better understand how document segmentation affects the performance and efficiency of Retrieval-Augmented Generation systems. segmentation affects the performance and efficiency of Retrieval-Augmented Generation systems.

---

## 正文

The Effect of Text Chunk Size on Retrieval-Augmented
Generation Performance
German Garrido-Lestache Belinchon , Hugo Garrido-Lestache Belinchon
Department of Computer Science and Software Engineering
Milwaukee School of Engineering
Milwaukee, WI US
garrido-lestachebeli@msoe.edu
arXiv:2607.24767v1 [cs.IR] 8 Jun 2026

Abstract
Retrieval-Augmented Generation (RAG) systems have emerged as a powerful process for
allowing large language models (LLMs) to retrieve relevant information to use as source
materialduringtextgeneration. Acriticalyetunder-exploredcomponentofthesesystemsis
thegranularityatwhichsourcedocumentsaresegmentedintoretrievablechunks. Thesize
of these chunks has the potential to significantly influence generation quality, contextual
correctness,retrievalprecision,andcomputationalefficiency. Despiteitsimportance,chunk
size is often selected without proper evaluation of its impact on generation quality.
Thispaperaimstoexploretheeffectthattextsizehasongenerationqualitybyusingmultiple
representations of identical full-length undergraduate textbooks, each split into different
sized chunks, such as sentences, paragraphs, or chapters. As the same source material is
used for all the chunks, it isolates chunk granularity as the primary variable. These chunks
areembeddedusingadenseembeddingmodelandindexedinavectordatabaseforsemantic
retrieval. Relevanceisdeterminedthroughcosinesimilaritysearch,wherethemostsimilar
text chunks to a user’s prompt are retrieved and supplied as contextual input to the LLM in
order to produce a response.
Smaller chunks, such as individual sentences, may allow for precise retrieval by narrowing
the focus of each chunk. However, they contain less information, which may limit the
model’s ability to generate coherent responses. Larger chunks, such as entire chapters,
containlotsofbroadinformationthatmayimprovecorrectness,butalsointroduceadditional
noise and increase computational cost. Because larger chunks contain more information,
the number of chunks returned to the model must also be considered.
This paper evaluates how chunk size, along with the number of retrieved segments, influ-
ences generation quality and retrieval effectiveness. By comparing these configurations,
this study seeks to better understand how document segmentation affects the performance
and efficiency of Retrieval-Augmented Generation systems.
Intro
LLMs are incredibly effective at generating coherent, relevant text in a number of different
formats and contexts. Though the text they generate may seem to fit at first glance, upon
closer inspection its often riddled with outdated, made up, and often incorrect information.
This is a well known issue of LLMs, but it would be incredibly time consuming and
computationally expensive to train them on every conceivable topic, so how do we make
these models produce factual, intelligent responses.
Retrieval Augmented Generation (RAG) systems address this limitation by combining
external knowledge retrieval with text generation. These models will use a large database
2

to store chunks of informational text, and a RAG model will then, given a prompt, find
relevant source information and supply them during text generation to produce accurate
factual responses. This pipeline of course relies heavily on the model’s ability to retrieve
relevant information.
Beforedocumentsareembeddedandindexedintoavectordatabase,theymustbesegmented
intoretrievablechunks. Thegranularityofthesechunkspresentsatradeoff. Smallerchunks
increaseretrievalspeed,andcomputationalpower,butlackthecontextualdepthforcoherent
responses. LargerchunksmaycontainmorecontextfortheLLMtoreference,butintroduce
noise,decreaseretrievalefficiency,andincreasescomputationaloverhead. Thesizeofthese
chunks,betheysentencesorparagraphs,isoftenselectedwithoutproperevaluationofhow
this decision impacts overall generation quality.
Chunk size has a clear impact on context retrieval, and coherent text generation. Despite
this, few studies isolate chunk size as a variable. This paper aims to address that by
evaluating how text chunk granularity affects retrieval effectiveness and generation quality
in a RAG framework. By comparing multiple chunk sizes with a single identical source
material,thisworkaimstoprovideinsightonanimportant,yetoftenoverlookedcomponent
of Retrieval Augmented Generation systems.
Related Work
Retrieval-Augmented Generation has become a foundational approach for improving re-
sponse accuracy in large language models by using external sources during generation.
Early RAG solutions focus on retrieval architectures and embedding quality, while keep-
ing a fixed document segmentation strategy (Lewis, et al., 2020) [6]. Retrieval-focused
generationmodelssuchasFusion-in-Decoderfurtherdemonstratethatintegrationbetween
retrieval and generation can significantly enhance response quality, yet continue to treat
document chunking as a static preprocessing step (Izacard et al., 2021) [4].
More recent work has improved how retrieved information is structured and utilized. The
RAPTOR framework (Sarthi et al., 2024) [7] introduces a hierarchical retrieval, based on
recursive summarization over large document collections. Similarly, Self-RAG (Asai et
al., 2023) [1] enables an iterative generation-critique loop, allowing models to refine both
retrieval decisions and generated outputs. These approaches highlight that improvements
to retrieval and generation pipelines can substantially enhance RAG system performance.
Otherresearchaddressesretrievalnoiseandcontextrelevancethroughpost-retrievalrefine-
ment. CorrectiveRAG(Yanetal.,2024)[9]introducesfilteringandcorrectionmechanisms
tomitigatetheimpactofirrelevantretrievedcontent,whileChunkRAG(Singhetal.,2024)
[8] applies LLM-based relevance filtering prior to generation. Although effective, these
approacheslargelyoperateafterretrievalandassumeafixedsegmentationofsources,focus-
ing on refining retrieved content rather than examining how document structure influences
performance.
3

More closely related to this work are studies that examine document chunking within RAG
pipelines. (Hladena et al., 2025) [3] demonstrate that chunk size significantly impacts
retrieval efficiency, generation quality, and computational cost. Additional studies analyse
chunk size across datasets and embeddings (Bhat et al., 2025) [2] or leverage document
structureindomain-specificcontexts(Yepesetal.,2025)[5],thoughtheseworksprimarily
emphasize retrieval effectiveness. In contrast, my work isolates chunk size as the primary
variable using meaningful boundaries (sentences, paragraphs, pages, and chapters) from
identical source content and evaluated under controlled embedding, retrieval, and gener-
ation conditions. This allows us to examine both retrieval effectiveness and downstream
generation quality, providing a view of how document chunking influences RAG system
performance.
Implementation
The RAG pipeline begins by loading and extracting the text, page by page, from the source
document. It extracts the raw text and removes artifacts such as, excessive line breaks,
page numbers, and hyphenated word splits. This produces a clean continuous body of text
suitable for chunking.
The document is then segmented using different levels of granularity, including chapter-
level splitting using regex, as well as agentic paragraph and sentence level segmentation,
in which an LLM iteratively extracts the first segment from a sliding window of text. This
allowsformorenaturalsegmentationratherthanrelyingpurelyonformattingwhichallowed
the chunking to work on any medium of source document.
Once segmented, each chunk is embedded into a vector representation, using a pre-trained
embedding model, and stored into a separate vector database for each chunk granularity.
Duringretrieval,auser’spromptisembeddedwiththesamemodel,andacosinesimilarity
search is used to find the n most similar text chunks.
Thesystemthenconcatenatestheretrievedchunks,tobeusedassourceinformation,along
with the user’s query. This augmented prompt is then passed onto an LLM to generate a
factual, grounded response.
Overall,thisimplementationenablescontrolledexperimentationacrossdifferentchunksizes
and retrieval configurations, allowing for direct comparison of their impact on generation
quality, relevance, and efficiency.
4

Figure 1: Flowchart Depicting the Source Document Pipeline
Figure 2: Flowchart Depicting the RAG Pipeline
Experimentation
5

To first ensure the program could effectively retrieve relevant source chunks, I produced
a set of 100 prompts, generated by ChatGPT, that were intended to simulate realistic
prompts,varyinginscopespecificityandcomplexity. Foreachprompt,Itestedtheretrieval
across all chunking strategies. The retrieval effectiveness was evaluated using Reciprocal
Rank, which measures how high the first relevant result appears within a ranked list of
retrievedchunks. Aretrievedchunkwasconsideredrelevantifitcontainedtheinformation
necessary to correctly answer the prompt. Relevance was determined agentically, using
an LLM to verifying whether the answer could be found within the retrieved text. This
ensuredconsistencyacrossallchunkingstrategies. Byaveragingthereciprocalrankscores
across all the prompts, I obtained a retrieval score that I could compare for each chunking
method. Additionally, I graphed the score of each chunking strategy for each prompt to
analyse which specific prompts the model struggles to retrieve.
Results and Analysis
Figure 3: Results from Chunking a Mathematics Textbook
6

Figure 4: Results from Chunking a Mathematics Textbook
The results demonstrate that chunking strategy has a significant impact on retrieval perfor-
mance, though this varies depending on the structure of the underlying text. For a math-
ematics textbook, paragraph-level chunking achieved the highest average retrieval score,
followedcloselybysentence-levelchunking. Thissuggeststhatforstructured,information-
dense content, medium-sized chunks such as paragraphs provide the best balance between
precision and contextual completeness. Sentence-level chunks, while precise, occasionally
lacked sufficient context, whereas chapter-level chunks were too broad, introducing noise
and reducing retrieval accuracy.
Figure 5: Results from Chunking a Narrative Text
7

Figure 6: Results from Chunking a Narrative Text
The results for the narrative text show a very different pattern. Sentence-level chunking
significantlyoutperformedallothermethods,achievinganaverageretrievalscoreof0.294,
while chapter, page, and paragraph-level chunking all performed extremely poorly. This
indicates that for narrative-driven content, where relevant details are often localized to
specific lines of dialogue or description, smaller chunks are far more effective. Larger
chunksinthiscontextappeartodiluterelevantinformation,makingitmoredifficultforthe
retrievalsystemtoisolateusefulcontent. Theseresultsreinforcetheconclusionthatoptimal
chunk size is highly dependent on the structure and writing style of the source material.
Despite these findings, several limitations must be considered. While smaller chunk sizes
often improve retrieval precision, they result in a significantly larger number of stored
embeddings, increasing both storage requirements and indexing time. On the other hand,
larger chunks reduce storage overhead but may introduce irrelevant context, negatively
impactingretrievalqualityandintroducingunwantednoiseduringgeneration. Furthermore,
the use of agentic chunking introduces additional computational cost, as it requires a large
language model during preprocessing. This makes it less practical for large-scale systems
despite its potential to produce more meaningful text chunks.
Conclusion
Thisstudysetouttoinvestigatehowdocumentsegmentationchunksizeinfluencestheper-
formanceofRAGsystems. Theresultsdemonstratethatchunkystrategyplaysameaningful
role in retrieval and generation. However, no single chunk size consistently outperforms
others across all mediums. Instead, the effectiveness of a given chunk size is tied to the
structure of the text.
Onekeyfindingisthatdifferenttextmediumsexhibitdifferentoptimalchunkingbehaviours.
More structured or narrative-driven documents tend to benefit from larger chunks, where
8

broader context improves the model’s ability to generate coherent and accurate responses.
In contrast, more fragmented or information-dense texts may benefit from smaller chunks,
whichallowformorepreciseretrievalatthecostofreducedcontextualcompleteness. This
highlightsanimportanttrade-offbetweenprecisionandcontext,suggestingthatchunksize
should not be treated as a fixed parameter, but rather as a configurable aspect of system
design.
These results point to several promising avenues for future research. One particularly
compelling direction is the further exploration of agentic or adaptive chunking, where the
chunks are dynamically segmented based on document structure, query intent, or retrieval
feedback. Such systems could adjust chunk granularity at indexing time or retrieval time,
selecting smaller chunks for fact-based queries and larger, more contextual segments for
reasoning-heavy prompts. Additionally, hybrid approaches that combine multiple chunk
sizes or assemble context dynamically from atomic units may further mitigate the preci-
sion–context trade-off observed in static chunking schemes.
Overall, this work reinforces the idea that effective RAG systems require careful consid-
eration of how source documents are segmented, rather than relying on a one-size-fits-all
approach. Bybetteraligningchunkingmethodswiththestructureofthesourcematerial,it
ispossibletoimprovebothretrievalqualityandgenerationperformanceinamoreconsistent
and efficient manner.
9

References
[1] Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-
rag: Learning to retrieve, generate, and critique through self-reflection, 2023. URL
https://arxiv.org/abs/2310.11511.
[2] SinchanaRamakanthBhatetal. Rethinkingchunksizeforlong-documentretrieval: A
multi-dataset analysis.arXiv preprint arXiv:2505.21700, 2025.
[3] Jan Hladěna, Kirsten Šteflovič, Pavel Čech, Kamila Štekerová, and Andrea Žváčková.
The effect of chunk size on the rag performance, 2025.
[4] Gautier Izacard and Edouard Grave. Leveraging passage retrieval with generative
models for open domain question answering. InACL, 2021.
[5] AntonioJimenoYepesetal. Financialreportchunkingforeffectiveretrievalaugmented
generation.arXiv preprint arXiv:2402.05131, 2024.
[6] Patrick Lewis, Ethan Perez, Aleksandra Piktus, et al. Retrieval-augmented generation
forknowledge-intensivenlptasks.Advances in Neural Information Processing Systems,
2020.
[7] Parth Sarthi, Salman Abdullah, Aditi Tuli, Shubh Khanna, Anna Goldie, and Christo-
pherD.Manning. Raptor: Recursiveabstractiveprocessingfortree-organizedretrieval,
2024. URLhttps://arxiv.org/abs/2401.18059.
[8] Ishneet Sukhvinder Singh et al. Chunkrag: Novel llm-chunk filtering method for rag
systems.arXiv preprint arXiv:2410.19572, 2024.
[9] Shi-QiYan,Jia-ChenGu,YunZhu,andZhen-HuaLing.Correctiveretrievalaugmented
generation, 2024. URLhttps://arxiv.org/abs/2401.15884.
10