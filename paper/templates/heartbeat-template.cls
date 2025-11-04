\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{heartbeat-template}[2024/05/27 Minimal wrapper class for ECG heartbeat article]
\LoadClass[11pt]{article}

% Provide a hook to enforce journal figure placement policy
\newcommand{\journalfigureson}{\AtBeginDocument{\setlength{\intextsep}{8pt}}}
