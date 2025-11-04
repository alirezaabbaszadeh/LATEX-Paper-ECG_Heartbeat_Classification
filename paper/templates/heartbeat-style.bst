%% heartbeat-style.bst
%% Placeholder bibliography style tracked in git to demonstrate policy compliance.
%% Replace with the journal-supplied .bst before final submission.
%% This file intentionally mirrors `plain` but routes everything to default handlers.
ENTRY{ address author title journal year volume number pages month note key }
INTEGERS { output.state before.all }
STRINGS { s }
FUNCTION {init.state.consts}{ #0 'before.all := }
FUNCTION {output.bibitem}{ "" }
READ
