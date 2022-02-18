echo "Evaluating against K"
python evaluate.py -t ../dygiepp_keywords.txt ../ot_keywords.txt \
  ../randr_keywords.txt \
  ../dygiepp_keywords_cleaned.txt \
  ../ot_keywords_cleaned.txt \
  -r ../../articles.json \
  -T ../author_keywords.txt

echo "Evaluating against CN"
python evaluate.py -t ../dygiepp_keywords.txt ../ot_keywords.txt \
  ../randr_keywords.txt \
  ../dygiepp_keywords_cleaned.txt \
  ../ot_keywords_cleaned.txt \
  -r ../../articles.json -C ../tac_compounds_cleaned.csv \
  -T ../anp_clean_sorted.txt

echo "Evaluating against KCN"
python evaluate.py -t ../dygiepp_keywords.txt ../ot_keywords.txt \
  ../randr_keywords.txt \
  ../dygiepp_keywords_cleaned.txt \
  ../ot_keywords_normalized.txt \
  -r ../../articles.json -C ../tac_compounds_cleaned.csv \
  -T ../author_keywords.txt ../anp_clean_sorted.txt

echo "Evaluating against OT"
python evaluate.py -t ../dygiepp_keywords.txt ../ot_keywords.txt \
  ../randr_keywords.txt \
  ../dygiepp_keywords_cleaned.txt \
  ../ot_keywords_normalized.txt \
  -r ../../articles.json -T ../ot_keywords.txt
