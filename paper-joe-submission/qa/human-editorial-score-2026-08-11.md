# Human-editorial quality audit

Date: 2026-08-11

Scope: Abstract, Introduction, Materials and Methods, Results, Discussion, Conclusion, Highlights, and primary figure captions.

This score evaluates scholarly writing quality. It is not an estimate of whether a person or an AI wrote the text, and it is not based on an AI detector. Authorship provenance cannot be inferred reliably from prose alone.

| Criterion | Weight | Before strict pass | After strict pass |
|---|---:|---:|---:|
| Fidelity to evidence and restraint of claims | 15 | 15 | 15 |
| Argument architecture | 15 | 13 | 14 |
| Domain-specific authorial judgement | 15 | 12 | 14 |
| Cohesion and inferential continuity | 10 | 9 | 10 |
| Sentence and paragraph rhythm | 10 | 8 | 9 |
| Lexical naturalness and precision | 10 | 8 | 9 |
| Synthesis of cited literature | 10 | 9 | 10 |
| Control of repetition | 5 | 4 | 4 |
| Fit with journal conventions | 5 | 5 | 5 |
| Transparency and reproducibility | 5 | 5 | 5 |
| **Total** | **100** | **88** | **95** |

## Evidence for the change

- The principal narrative was reduced from approximately 3,488 to 3,175 source words without removing a quantitative result or citation key.
- Repeated explanations of the weighted-F1/macro-F1 difference were consolidated.
- Two engineered rhetorical questions were removed from the Discussion.
- The error interpretation now states which mechanism the authors consider more informative and identifies the ablation that could refute it.
- Future work is ordered by dependency: representation ablation, development-only minority-class selection, external validation, and only then prospective clinical assessment.
- The Methods section retains exact protocol information but contains less repository-documentation language.
- The Abstract contains 201 LaTeX-stripped words; all five Highlights remain below 85 characters.

## Why the score is not 100

The remaining five points are not safely recoverable through editorial automation alone. Final author review is needed to confirm that the prioritised mechanism and the stated experimental sequence reflect the investigators' own scientific judgement. Some procedural language is also unavoidable in a reproducible Methods section and in the required generative-AI declaration. A perfect score would falsely imply certainty about authorship and authorial intention that prose analysis cannot provide.
