#!/usr/bin/env bash
# Play exported QA clips in order, printing each subtitle before its clip.
#
#   ./pipeline/listen_qa.sh 2023-06-set2              # whole exam
#   ./pipeline/listen_qa.sh 2023-06-set2 conv-1       # one subpart
#
# Press Ctrl-C to stop. Uses mpv if available, otherwise ffplay.

set -euo pipefail

EXAM="${1:?usage: listen_qa.sh <exam_id> [subpart_code]}"
SUB="${2:-}"
DIR="data/qa_clips/${EXAM}"
MANIFEST="${DIR}/manifest.txt"

if [[ ! -f "$MANIFEST" ]]; then
  echo "no clips for ${EXAM}. run:"
  echo "  python3 pipeline/export_check_clips.py ${EXAM} ${SUB:+--subpart $SUB}"
  exit 1
fi

cd "$DIR"
PATTERN="${SUB:-*}"
count=$(ls ${PATTERN}-*.mp3 2>/dev/null | wc -l)
echo "=============================================================="
echo " ${EXAM}  ${SUB:-all subparts}  —  ${count} clips"
echo " Compare what you HEAR against the EN line printed before it."
echo " If they disagree, the timestamp is wrong, not your hearing."
echo "=============================================================="

for f in $(ls ${PATTERN}-*.mp3 | sort); do
  python3 - "$f" <<'PY'
import sys
lines = open("manifest.txt", encoding="utf-8").read().split("\n")
clip = sys.argv[1]
for i, l in enumerate(lines):
    if l.startswith(f"[{clip}]"):
        print("\n" + l)
        for nxt in lines[i + 1:i + 3]:
            if nxt.startswith("["):
                break
            print(nxt)
        break
PY
  if command -v mpv >/dev/null 2>&1; then
    mpv --really-quiet --no-video "$f"
  else
    ffplay -autoexit -nodisp -v error "$f"
  fi
done

echo
echo "done: ${count} clips"
