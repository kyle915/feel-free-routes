#!/usr/bin/env bash
# One command to regenerate every deliverable from build_data.py.
# Usage:  bash rebuild.sh
set -e
echo "→ Building schedule.json ..."
python3 build_data.py
echo "→ Building Excel workbook ..."
python3 build_xlsx.py
echo "→ Building client PDF ..."
python3 build_pdf.py
echo "→ Building interactive HTML + index.html ..."
python3 build_html.py
echo "→ Building Open Shifts page ..."
python3 build_open_shifts.py
echo "✓ Done. The live site is index.html; downloadables are the .xlsx and .pdf."
