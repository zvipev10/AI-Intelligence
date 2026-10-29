# mil-sym-ts browser renderer
Official package: `@armyc2.c5isr.renderer/mil-sym-ts-web` 2.10.8.
Upstream: https://github.com/missioncommand/mil-sym-ts, tag v2.10.8, commit 58cae590c7b1ddc4d762a8b00f59284f3122ef82.
License: Apache-2.0, retained in LICENSE. C5Ren.umd.js is the unmodified official browser bundle (7,367,121 bytes).
Tarball: https://registry.npmjs.org/@armyc2.c5isr.renderer/mil-sym-ts-web/-/mil-sym-ts-web-2.10.8.tgz
Verified tarball integrity: sha512-+xTP3ytzpu9J2JQ47tpeKBzWy4XXEQOUZRzdmR0txiPntrJuBcxduBMy7VL7D2voNPr1LtjSJt4t4+BTWB1dLg==
Reproduce: download that pinned tarball, verify SHA512, extract package/C5Ren.umd.js and package/LICENSE. No npm install, build, CDN or server renderer is required.
The application uses MIL-STD-2525E Change 1 (version digits 15). Mappings are in mil_sym_adapter.js; the library owns affiliation frames. This integration is not external standards certification.
Generic fallbacks: land convoy control measures require two points, so one-point observations use Vehicle plus Convoy label. Logistics truck uses generic utility vehicle plus its label (cross-country capacity is unknown). Aviation unit uses unspecified land unit plus Aviation label (rotary/fixed/composite subtype is not established). Missing mappings/library render failures use ordinary dots, never a fake military frame.
