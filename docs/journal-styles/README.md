# Official journal class and bibliography styles

This directory mirrors the official LaTeX class and bibliography style files distributed by each target journal's publisher. They are provided so that local `latexmk` builds match the versions used by the journal submission portals and Overleaf templates.

## Contents

- `journal-of-electrocardiology/`
  - `elsarticle.cls` and `elsarticle-num.bst` retrieved from the [Elsevier CTAN package](https://ctan.org/pkg/elsarticle).
- `biomedical-engineering-online/`
  - `sn-jnl.cls` and `sn-basic.bst` copied from the public Springer Nature Overleaf template mirror ([godkingjay/springer-nature-latex-template](https://github.com/godkingjay/springer-nature-latex-template)).

When compiling offline, copy these files next to the manuscript sources or add the directories to your TeX input path so the templates resolve the publisher-specific classes without relying on a system-wide TeX distribution.
