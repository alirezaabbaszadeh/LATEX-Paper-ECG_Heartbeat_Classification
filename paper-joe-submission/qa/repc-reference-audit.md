# Reference audit for REPC submission

Audit date: 2026-08-29

## Active manuscript bibliography

The current manuscript cites **24 unique bibliography keys**. Every cited key resolves to an entry in `bib/references.bib`, and every one of the 24 cited entries contains a DOI or DOI-like persistent identifier in the bibliography.

The active citation set is:

`he2009learning`, `saito2015precision`, `mantravadi2024clinet`, `petmezas2026optimizing`, `vainoryte2025diagnostic`, `dechazal2004automatic`, `herman2024validation`, `tuboly2026malignant`, `doggart2025singlelead`, `addison2005wavelet`, `torrence1998practical`, `mallat1989wavelet`, `wang2025mrsenet`, `pukkila2026chronic`, `gulati2020conformer`, `goldberger2000physiobank`, `moody2001impact`, `vaswani2017attention`, `he2016deep`, `ba2016layer`, `li2018hyperband`, `fawcett2006introduction`, `demolder2024certainty`, and `demolder2025digitization`.

## Repository hygiene finding

The bibliography file contains **66 entries total**, so 42 are not cited by the current manuscript. Among the uncited entries, the following 17 have no DOI or URL metadata and should **not** be promoted into the manuscript until individually verified against a primary bibliographic source:

- Gadaleta2023SingleLead
- Kim2024FortyFive
- Ozpolat2023Quantum
- Gliner2025Interpretability
- Czerwinski2025Interpretable
- Yoon2023Interpretable
- Jiang2025Hybrid
- Voss2023Multimodal
- Stern2024InBed
- Silva2023Infusion
- Chen2024SuperResolution
- Sugiarto2025GroundReaction
- Li2025Antioxidant
- Osullivan2024Pediatric
- Hsieh2025Economic
- Hempel2025ECGAging
- Aslan2025Poincare

These entries are currently harmless to the compiled article because BibTeX does not emit uncited entries, but they are a repository-quality risk if reused later without verification.

## Submission rule

Do not increase the reference count merely to make the bibliography longer. The REPC Original Article format allows substantially more references than the manuscript currently uses, but additions should be driven by a concrete claim or gap and verified at DOI/title/author/journal level before citation.

## Final preflight

Before submission:
- validate all 24 active DOIs resolve to the intended articles;
- check author names, journal, year, volume, pages/article number;
- preserve the current citation-to-claim mapping;
- add new literature only when it materially strengthens the manuscript and is cited in the text.
