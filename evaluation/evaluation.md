Methods
-------

To evaluate Parmenides against another phrase extraction method, both
Parmenides and the point of comparison are used to generate the set of phrases
that are extracted for each document in the corpus. This results in two sets of
phrases for each document: the set of phrases that Parmenides retrieved, and
the set of phrases that are, for the purposes of this evaluation, considered
relevant. Each phrase that occurs in both sets is considered a true positive; a
phrase that occurs only in the retrieved set is a false negative, and a phrase
that occurs only in the relevant set is a false negative. The false positives,
false negatives, and true positives for each document and each point of
comparison can be found in `results.full.json`. 

To calculate the overall results, we sum the number of false negatives, false
positives, and true positives for the entire corpus, and use these to calculate
precision, recall, and F1. We also provide summaries for the frequency with
which particular phrases appear as false negatives, false positives, and true
positives. There is one summary file for each experiment:
`opentapioca.summary.json` and `dygiepp.summary.json`. For example, against
DyGIE++, "monoidal" was found as a true positive 20 times (identified by both
Parmenides and DyGIE++), "category" was found as a false positive 455 times
(identifier by Parmenides but not by DyGIE++), and "of" was found as a false
negative 14 times (found by DyGIE++ but not by Parmenides). 

Results
-------

The following results were obtained comparing Parmenides against OpenTapioca:

| Metric    | Score |
|-----------|-------|
| Precision | 0.08  |
| Recall    | 0.74  |
| F1        | 0.15  |

The following results were obtained comparing Parmenides against DyGIE++:

| Metric    | Score |
|-----------|-------|
| Precision | 0.01  |
| Recall    | 0.57  |
| F1        | 0.03  |

Author Keywords
---------------

We also ran similar experiments against author-selected keywords. These
experiments cover the whole corpus and are not evaluated against specific
documents. All three keyword extraction models are tested against the gold
standard of author-selected keywords.

| Metric          | Parmenides | DyGIE++ | OpenTapioca |
|-----------------|------------|---------|-------------|
| True Positives  | **455**    | 59      | 138         |
| False Positives | 53080      | 1264    | **1152**    |
| False Negatives | **1506**   | 1902    | 1823        |
| Precision       | 0.01       | 0.04    | **0.11**    |
| Recall          | **0.23**   | 0.03    | 0.07        |
| F1              | 0.02       | 0.04    | **0.08**    |

We also ran the same experiment with cleaned, normalized keywords.

| Metric          | Parmenides | DyGIE++ | OpenTapioca |
|-----------------|------------|---------|-------------|
| True Positives  | **771**    | 97      | 206         |
| False Positives | 52764      | 1226    | **1084**    |
| False Negatives | **1092**   | 1766    | 1657        |
| Precision       | 0.01       | 0.07    | **0.16**    |
| Recall          | **0.41**   | 0.05    | 0.11        |
| F1              | 0.03       | 0.06    | **0.13**    |
