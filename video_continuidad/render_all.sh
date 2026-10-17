#!/bin/bash
set -e
cd "$(dirname "$0")"
for s in scene1_intro scene2_concepto scene3_evitable scene4_salto scene5_infinita scene6_repaso; do
  (python3 "$s.py" > "logs/$s.log" 2>&1; echo "EXIT $? for $s" >> "logs/$s.log") &
done
wait
echo "ALL DONE"
