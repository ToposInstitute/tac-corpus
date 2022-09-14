python scripts/get_keywords.py textrank parmenides opentapioca dygie author \
  nlab nps dygie_tac

python scripts/normalize_text.py

python scripts/normalize_keywords.py textrank parmenides opentapioca dygie \
  author nlab nps dygie_tac

python scripts/extract_keywords.py textrank parmenides opentapioca dygie \
  author nlab nps dygie_tac

echo "Evaluating against author keywords"
python scripts/evaluate.py -p textrank parmenides opentapioca dygie dygie_tac -- \
  author

echo "Evaluating against NLab titles"
python scripts/evaluate.py -p textrank parmenides opentapioca dygie dygie_tac -- \
  nlab

echo "Evaluating against NPs"
python scripts/evaluate.py -p textrank parmenides opentapioca dygie dygie_tac -- \
  nps

echo "Evaluating against combined keywords"
python scripts/evaluate.py -p textrank parmenides opentapioca dygie dygie_tac -- \
  author nlab nps

echo "Creating visualizations"
python scripts/venn.py -o visualizations/full_scaled.png -m 300 textrank parmenides \
  opentapioca dygie author nlab nps > results/counts.txt

python scripts/venn.py -o visualizations/full_clean.png -r 0.05 textrank parmenides \
  opentapioca dygie author nlab nps

python scripts/venn.py -o visualizations/textrank_scaled.png -m 300 textrank \
  author nlab nps

python scripts/venn.py -o visualizations/textrank_clean.png -r 0.05 textrank \
  author nlab nps

python scripts/venn.py -o visualizations/parmenides_scaled.png -m 300 parmenides \
  author nlab nps

python scripts/venn.py -o visualizations/parmenides_clean.png -r 0.05 \
  parmenides author nlab nps

python scripts/venn.py -o visualizations/opentapioca_scaled.png -m 300 opentapioca \
  author nlab nps

python scripts/venn.py -o visualizations/opentapioca_clean.png -r 0.05 \
  opentapioca author nlab nps

python scripts/venn.py -o visualizations/dygie_scaled.png -m 300 dygie \
  author nlab nps

python scripts/venn.py -o visualizations/dygie_clean.png -r 0.05 \
  dygie author nlab nps

python scripts/venn.py -o visualizations/standards_scaled.png -m 300 author \
  nlab nps

python scripts/venn.py -o visualizations/standards_clean.png -r 0.05 \
  author nlab nps

python scripts/venn.py -o visualizations/extractors_scaled.png -m 300 \
  textrank parmenides opentapioca dygie

python scripts/venn.py -o visualizations/extractors_clean.png -r 0.05 \
  textrank parmenides opentapioca dygie
