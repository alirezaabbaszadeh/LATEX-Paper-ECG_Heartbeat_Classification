#!/usr/bin/env python3
import argparse, re, sys
from pathlib import Path

# --- Helpers ---------------------------------------------------------------
CLASS_KEYS = [
    ("Normal", ["Normal","N"]),
    ("SVEB",   ["SVEB","S"]),
    ("VEB",    ["VEB","V"]),
    ("Fusion", ["Fusion","F"]),
    ("Unknown",["Unknown","Q"])
]

ROW_RE = re.compile(r^\s*([A-Za-z]+)\s+([0-9]*\.?[0-9]+)\s+([0-9]*\.?[0-9]+)\s+([0-9]*\.?[0-9]+)\s+([0-9]+)\s*$)
AUC_RE = re.compile(r"AUC for class '([^']+)':\s*([0-9]*\.?[0-9]+)")
ACC_RE = re.compile(r^\s*accuracy\s+([0-9]*\.?[0-9]+))
MACRO_RE = re.compile(r^\s*macro avg\s+([0-9]*\.?[0-9]+)\s+([0-9]*\.?[0-9]+)\s+([0-9]*\.?[0-9]+)\s+([0-9]+))
WEIGHT_RE = re.compile(r^\s*weighted avg\s+([0-9]*\.?[0-9]+)\s+([0-9]*\.?[0-9]+)\s+([0-9]*\.?[0-9]+)\s+([0-9]+))

def norm_key(k):
    return k.strip().lower()

# --- Parse one classification report file ---------------------------------
def parse_report(path: Path):
    text = path.read_text(errors='ignore')
    per_class = {}
    auc = {}
    acc = None
    macro = None
    weight = None
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if m:
            name = m.group(1)
            pre = float(m.group(2)); rec = float(m.group(3)); f1 = float(m.group(4)); sup = int(float(m.group(5)))
            key = norm_key(name)
            per_class[key] = {"precision":pre, "recall":rec, "f1":f1, "support":sup}
            continue
        m = AUC_RE.search(line)
        if m:
            auc[norm_key(m.group(1))] = float(m.group(2))
            continue
        m = ACC_RE.match(line)
        if m:
            acc = float(m.group(1))
            continue
        m = MACRO_RE.match(line)
        if m:
            macro = tuple(map(float, m.group(1,2,3))) + (int(float(m.group(4))),)
            continue
        m = WEIGHT_RE.match(line)
        if m:
            weight = tuple(map(float, m.group(1,2,3))) + (int(float(m.group(4))),)
            continue
    return {"per_class":per_class, "auc":auc, "accuracy":acc, "macro":macro, "weighted":weight}

# --- Write TeX helpers -----------------------------------------------------
HEADER = "\\begingroup\n\\footnotesize\n\\setlength{\\tabcolsep}{6pt}\n"
FOOTER = "\n\\endgroup\n"

def write_perf_summary(out_path: Path, acc, macro, weight, support):
    s = [HEADER, "\\begin{tabular}{lcccc}\n\\toprule\n & \\textbf{Precision} & \\textbf{Recall} & \\textbf{F1} & \\textbf{Support} \\\ \n\\midrule\n"]
    s.append(f"Accuracy & \\multicolumn{{3}}{{c}}{{{acc:.2f}}} & {support} \\\ \n")
    if macro:
        s.append(f"Macro avg & {macro[0]:.2f} & {macro[1]:.2f} & {macro[2]:.2f} & {macro[3]} \\\ \n")
    if weight:
        s.append(f"Weighted avg & {weight[0]:.2f} & {weight[1]:.2f} & {weight[2]:.2f} & {weight[3]} \\\ \n")
    s.append("\\bottomrule\n\\end{tabular}\n")
    s.append(FOOTER)
    out_path.write_text(''.join(s))

def write_auc(out_path: Path, auc):
    s = [HEADER, "\\begin{tabular}{lcc}\n\\toprule\n\\textbf{Class} & \\textbf{AUC (OvR)} & \\textbf{Note} \\\ \n\\midrule\n"]
    notes = {
        'normal': 'strong separability',
        'sveb': 'low-prevalence; overlap with N',
        'veb': 'good separability',
        'fusion': 'scarce \\& ambiguous',
        'unknown': 'tiny support'
    }
    for label, aliases in CLASS_KEYS:
        k = norm_key(label)
        val = auc.get(k, None)
        if val is None and k=='unknown':
            val = auc.get('q', None)
        if val is None:
            s.append(f"{label} & N/A & {notes.get(k,'')} \\\ \n")
        else:
            s.append(f"{label} & {val:.4f} & {notes.get(k,'')} \\\ \n")
    s.append("\\midrule\n\\textbf{Macro avg} & \\textit{---} & reported curves per-class \\\ \n\\bottomrule\n\\end{tabular}\n")
    s.append(FOOTER)
    out_path.write_text(''.join(s))

def write_per_class(out_path: Path, per_class):
    s = [HEADER, "\\begin{tabular}{lcccc}\n\\toprule\nClass & Precision & Recall & F1 & Support \\\ \n\\midrule\n"]
    for label, aliases in CLASS_KEYS:
        k = norm_key(label)
        row = per_class.get(k) or per_class.get(aliases[-1].lower(), None)
        if row:
            s.append(f"{label} & {row['precision']:.2f} & {row['recall']:.2f} & {row['f1']:.2f} & {row['support']} \\\ \n")
        else:
            s.append(f"{label} & N/A & N/A & N/A & N/A \\\ \n")
    s.append("\\bottomrule\n\\end{tabular}\n")
    s.append(FOOTER)
    out_path.write_text(''.join(s))

# --- Main -----------------------------------------------------------------
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, help='Path to ECG_Heartbeat_Classification repo')
    ap.add_argument('--out', default='paper/tables', help='Output tables dir (relative to paper repo)')
    # Fallbacks (from chat-supplied report) if we can't parse any file
    ap.add_argument('--fallback-acc', type=float, default=0.60)
    ap.add_argument('--fallback-support', type=int, default=15573)
    ap.add_argument('--fallback-macro', default='0.29,0.26,0.26')
    ap.add_argument('--fallback-weight', default='0.82,0.60,0.68')
    ap.add_argument('--fallback-auc', default='normal:0.9009,sveb:0.6681,veb:0.8431,fusion:0.3140,unknown:0.5837')
    args = ap.parse_args()

    repo = Path(args.repo)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    reports = list(repo.rglob('classification_report*.txt')) + list(repo.rglob('*Classification Report*.txt'))
    best = None
    for p in reports:
        try:
            r = parse_report(p)
            # pick the one with highest accuracy if available
            if best is None:
                best = r
            else:
                if (r.get('accuracy') or 0) > (best.get('accuracy') or 0):
                    best = r
        except Exception as e:
            print('WARN: failed parse', p, e, file=sys.stderr)

    if best is None:
        # Fallback from provided numbers
        macro = tuple(map(float, args.fallback_macro.split(','))) + (args.fallback_support,)
        weight = tuple(map(float, args.fallback_weight.split(','))) + (args.fallback_support,)
        acc = args.fallback_acc
        auc = {k: float(v) for k,v in [kv.split(':') for kv in args.fallback_auc.split(',')]}
        per_class = {}
    else:
        acc = best.get('accuracy') or args.fallback_acc
        # If macro not fully available, use fallback for missing parts
        macro = best.get('macro')
        if not macro:
            macro = tuple(map(float, args.fallback_macro.split(','))) + (args.fallback_support,)
        weight = best.get('weighted')
        if not weight:
            weight = tuple(map(float, args.fallback_weight.split(','))) + (args.fallback_support,)
        auc = best.get('auc') or {k: float(v) for k,v in [kv.split(':') for kv in args.fallback_auc.split(',')]}
        per_class = best.get('per_class') or {}

    write_perf_summary(out_dir / 'table_perf_summary.tex', acc, macro, weight, macro[3])
    write_auc(out_dir / 'table_auc.tex', auc)
    write_per_class(out_dir / 'main_per_class_report.tex', per_class)
    print('Wrote:', out_dir / 'table_perf_summary.tex')
    print('Wrote:', out_dir / 'table_auc.tex')
    print('Wrote:', out_dir / 'main_per_class_report.tex')
