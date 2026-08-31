# Revista Portuguesa de Cardiologia submission package

This directory contains the submission-facing files for the Revista Portuguesa de Cardiologia (REPC) adaptation of the final scientific manuscript.

Canonical files:
- 01_Cover_Letter_Revista_Portuguesa_de_Cardiologia.pdf
- 02_Manuscript_Record_Level_ECG_Classification.pdf
- 03_Ethical_Statement.pdf
- 04_Graphical_Abstract.pdf / 04_Graphical_Abstract.png
- 05_Title_Page_with_Author_Details.pdf
- 06_Declaration_of_Interest_Statement.pdf
- 07_Portuguese_Title_Abstract_Keywords.pdf
- 08_Supplementary_Material.pdf

The primary manuscript is built from ../src/main.tex. Supplementary material is built separately from ../supplementary/supplementary.tex.

Reproducibility:
- public development repository: https://github.com/alirezaabbaszadeh/ECG_Heartbeat_Classification
- immutable experimental snapshot: v1.0-joe-submission

Important graphical-abstract gate:
The current 04_Graphical_Abstract TeX/PDF is an AI-assisted layout draft and data specification. Current Elsevier artwork policy does not permit a general-purpose generative-AI tool to create a submitted graphical abstract. Before portal upload, the same scientific content must be recreated or independently approved in a journal-permitted non-generative scientific/professional illustration workflow, and that compliant file must replace the draft at the canonical 04_Graphical_Abstract path.

See ../qa/repc-submission-readiness.md for the final pass/fail gate.
