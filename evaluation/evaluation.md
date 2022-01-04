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

We have also tested filtered versions of DyGIE++ and OpenTapioca.

| Metric          | Parmenides | DyGIE++ | OpenTapioca | D++ Clean | OT Clean |
|-----------------|------------|---------|-------------|-----------|----------|
| True Positives  | **455**    | 59      | 138         | 60        | 138      |
| False Positives | 53080      | 1264    | 1152        | **741**   | 761      |
| False Negatives | **1506**   | 1902    | 1823        | 1901      | 1823     |
| Precision       | 0.01       | 0.04    | **0.11**    | 0.07      | 0.15     |
| Recall          | **0.23**   | 0.03    | 0.07        | 0.03      | 0.07     |
| F1              | 0.02       | 0.04    | **0.08**    | 0.04      | 0.10     |

We also ran the same experiment with cleaned, normalized keywords.

| Metric          | Parmenides | DyGIE++ | OpenTapioca | D++ Clean | OT Clean |
|-----------------|------------|---------|-------------|-----------|----------|
| True Positives  | **771**    | 97      | 206         | 88        | 208      |
| False Positives | 52764      | 1226    | 1084        | 713       | **691**  |
| False Negatives | **1092**   | 1766    | 1657        | 1775      | 1655     |
| Precision       | 0.01       | 0.07    | 0.16        | 0.11      | **0.23** |
| Recall          | **0.41**   | 0.05    | 0.11        | 0.05      | 0.11     |
| F1              | 0.03       | 0.06    | 0.13        | 0.07      | **0.15** |

The results below are for Parmenides with a filter applied on the cleaned,
normalized keywords, for comparison and experimentation.

| Metric          | Parmenides |
|-----------------|------------|
| True Positives  | 766        |
| False Positives | 19646      |
| False Negatives | 1097       |
| Precision       | 0.04       |
| Recall          | 0.41       |
| F1              | 0.07       |

Compounds
---------

A similar experiment uses compounds extracted from the text by SpaCy. These are
all two-word phrases identified as compounds by the SpaCy dependency parser,
and then cleaned of LaTeX markup. Otherwise, the evaluation is the same as
before.

Only the filtered Parmenides is evaluated here.

| Metric          | Parmenides | DyGIE++ | OpenTapioca | D++ Clean | OT Clean |
|-----------------|------------|---------|-------------|-----------|----------|
| True Positives  | **825**    | 21      | 135         | 21        | 153      |
| False Positives | 19587      | 1302    | 1155        | 780       | **746**  |
| False Negatives | **904**    | 1708    | 1594        | 1708      | 1576     |
| Precision       | 0.04       | 0.02    | 0.10        | 0.03      | **0.17** |
| Recall          | **0.48**   | 0.01    | 0.08        | 0.02      | 0.09     |
| F1              | 0.07       | 0.01    | 0.09        | 0.02      | **0.12** |

Combining the author keywords and the compounds gives the following results:

| Metric          | Parmenides | DyGIE++ | OpenTapioca | D++ Clean | OT Clean |
|-----------------|------------|---------|-------------|-----------|----------|
| True Positives  | 1440       | 113     | 289         | 103       | 306      |
| False Positives | 18972      | 1210    | 1001        | 698       | 593      |
| False Negatives | 1942       | 3269    | 3093        | 3279      | 3076     |
| Precision       | 0.07       | 0.09    | 0.22        | 0.13      | 0.34     |
| Recall          | 0.43       | 0.03    | 0.09        | 0.03      | 0.09     |
| F1              | 0.12       | 0.05    | 0.12        | 0.05      | 0.14     |

Excluded Keywords
-----------------

By excluding author keywords that don't appear in the text, it is possible to
improve recall for some systems. In this case, all keywords have been
lemmatized before comparison.

| Metric          | Parmenides | DyGIE++ | OpenTapioca | D++ Clean | OT Clean |
|-----------------|------------|---------|-------------|-----------|----------|
| True Positives  | **936**    | 110     | 220         | 79        | 200      |
| False Positives | 17351      | 1199    | 808         | 722       | **699**  |
| False Negatives | **134**    | 960     | 850         | 991       | 870      |
| Precision       | 0.05       | 0.08    | 0.21        | 0.10      | **0.22** |
| Recall          | **0.87**   | 0.10    | 0.21        | 0.10      | 0.22     |
| F1              | 0.10       | 0.09    | **0.21**    | 0.08      | 0.20     |

Combining these with compounds:

| Metric          | Parmenides | DyGIE++ | OpenTapioca | D++ Clean | OT Clean |
|-----------------|------------|---------|-------------|-----------|----------|
| True Positives  | 1835       | 127     | 327         | 93        | 297      |
| False Positives | 16452      | 1182    | 701         | 708       | 602      |
| False Negatives | 745        | 2453    | 2253        | 2487      | 2283     |
| Precision       | 0.10       | 0.10    | 0.32        | 0.12      | 0.33     |
| Recall          | 0.71       | 0.05    | 0.13        | 0.04      | 0.12     |
| F1              | 0.18       | 0.07    | 0.18        | 0.06      | 0.17     |
