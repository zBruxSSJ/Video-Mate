#!/bin/bash
set -e
cd "$(dirname "$0")"
for s in scene1_intro scene2_condiciones scene3_planteo scene4_condicion_x1 scene5_condicion_x3 scene6_resolver_sistema scene7_verificacion scene8_cierre; do
  (python3 "$s.py" > "logs/$s.log" 2>&1; echo "EXIT $? for $s" >> "logs/$s.log") &
done
wait
echo "ALL DONE"
