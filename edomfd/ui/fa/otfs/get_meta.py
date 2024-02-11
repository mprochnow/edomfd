# Copyright (C) Martin J. Prochnow
# Licensed under the GNU General Public License v3
# See LICENSE.MD

import json

meta = {}

with open('icons.json', 'r') as f:
    j = json.load(f)

    for key, value in j.items():
        meta[key] = {
            'styles': value['styles'],
            'unicode': chr(int(value['unicode'], 16))
        }

with open('meta.json', 'w') as f:
    json.dump(meta, f, indent=2, ensure_ascii=True)
