Methods
-------

Each experiment below compares the results of several keyphrase extraction
algorithms against a different gold/silver standard. For each evaluation, we
calculate the number true positives, false positives, and false negatives,
which allows us to calculate precision, recall, and F1. 

In all of these evaluations, keyphrases are identified at the corpus level, not
at the document or sentence level.

Author Keywords
---------------

The first experiment compares each algorithm against the set of keywords
selected by the authors that actually appear in the text of the corpus. 

| Metric          | Parmenides | DyGIE++ | OpenTapioca | TextRank |
|-----------------|------------|---------|-------------|----------|
| True Positives  | **940**    | 98      | 218         | 552      |
| False Positives | 18668      | 671     | **653**     | 10470    |
| False Negatives | **130**    | 972     | 852         | 518      |
| Precision       | 0.05       | 0.13    | **0.25**    | 0.05     |
| Recall          | **0.88**   | 0.09    | 0.20        | 0.52     |
| F1              | 0.09       | 0.11    | **0.22**    | 0.09     |

Compounds and Modified NPs
--------------------------

The second experiment compares each algorithm against the set of phrases
identified by spaCy using simple regular expressions over part-of-speech tags
and relation labels. Any sequence consiting of an adjective followed by a noun
or two nouns with a compound relation are included.

| Metric          | Parmenides | DyGIE++ | OpenTapioca | TextRank |
|-----------------|------------|---------|-------------|----------|
| True Positives  | **2226**   | 83      | 339         | 979      |
| False Positives | 17382      | 686     | **532**     | 10043    |
| False Negatives | **841**    | 2984    | 2728        | 2088     |
| Precision       | 0.11       | 0.11    | **0.39**    | 0.09     |
| Recall          | **0.73**   | 0.03    | 0.11        | 0.32     |
| F1              | **0.20**   | 0.04    | 0.17        | 0.14     |

Author Keywords + Compounds
---------------------------

Next we compare the union of author keywords, compounds, and modified noun
phrases.

| Metric          | Parmenides | DyGIE++ | OpenTapioca | TextRank |
|-----------------|------------|---------|-------------|----------|
| True Positives  | **2728**   | 159     | 442         | 1290     |
| False Positives | 16880      | 610     | **429**     | 97320    |
| False Negatives | **958**    | 3527    | 3244        | 2396     |
| Precision       | 0.14       | 0.21    | **0.51**    | 0.12     |
| Recall          | **0.74**   | 0.04    | 0.12        | 0.35     |
| F1              | **0.23**   | 0.07    | 0.19        | 0.18     |

OpenTapioca
-----------

Finally, we look at OpenTapioca as its own gold standard.

| Metric          | Parmenides | DyGIE++  | TextRank |
|-----------------|------------|----------|----------|
| True Positives  | **871**    | 95       | 462      |
| False Positives | 18737      | **674**  | 10560    |
| False Negatives | **157**    | 933      | 566      |
| Precision       | 0.04       | **0.12** | 0.04     |
| Recall          | **0.85**   | 0.09     | 0.45     |
| F1              | 0.08       | **0.11** | 0.08     |

Summary
-------

Below is a summary of all F1 scores.

| Evaluation | Parmenides | DyGIE++  | OpenTapioca | TextRank |
|------------|------------|----------|-------------|----------|
| K          | 0.09       | 0.11     | **0.22**    | 0.09     |
| C          | **0.20**   | 0.04     | 0.17        | 0.14     |
| KC         | **0.23**   | 0.07     | 0.19        | 0.18     |
| O          | 0.08       | **0.11** | 1           | 0.08     |
