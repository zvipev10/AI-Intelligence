# Model Prompt

You are given a compact, pre-processed evidence package from several fictional data sources.

Your task is to test cross-reference reasoning. Do not assume facts outside the evidence.

## Questions

1. What is the strongest cross-source hypothesis suggested by the evidence?
2. Which specific evidence points support it?
3. Which entity aliases or identity links matter?
4. Which events are likely distractors or alternative explanations?
5. What confidence level would you assign: low, medium, or high?
6. What additional data would most improve or disprove the hypothesis?

## Required Answer Format

Return:

- A one-paragraph bottom line.
- A bullet list of supporting evidence.
- A bullet list of caveats and alternative explanations.
- A short confidence assessment.
- A short list of recommended next checks.

Do not claim certainty. Distinguish direct evidence from inference.

