# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b145-numbers-led/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b145-numbers-led/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-image front page summing up 23 November 2026's world news — numbers-led:
a big number grid first (−3.3% Kospi, 5.3 US–China power gap, 11,762 Ebola cases
in the DRC, 10T-won Seoul fund, 2% billionaire tax, $450M Skubal deal, 165 Russian
missiles a week, 12,000 cleared in Manchester, 264 kg explosives seized, $107.3B
Anthropic IPO), then the three heroes of the day — the AI rout that hit Asian
markets, Guterres calling for AI rules before it is too late, and the US lead over
China at its record low — plus 10 more stories, a map with numbered pins, an
18-item ALSO list, and a DATE CHECK box that keeps out stories dated other days.

## Stories (31)

**Heroes:** AI rout hits Asia (Kospi −3.3% to 4,708.54) · Guterres: regulate AI
before it's too late (Bridgetown summit, 150 delegates back a risk framework) ·
US lead over China at record low (Asia Power Index 2026: US 78.9, China 73.6, gap 5.3).

**More of the day (10):** Bessent demands Nvidia answers · FBI probes NCIC hack ·
Trump: Iran strikes may resume in New Year · Nasdaq futures +3% · Skubal's $450M
Mets deal · Tom Jackson dies at 75 · States sue SpaceX · Anthropic IPO $107.3B
(raised at $83/share) · Poland: 3 Russian Kh-101 missiles crossed airspace (CLAIM) ·
Intel warns of Russian nuclear satellite (CLAIM).

**Also on Monday (18):** Paris 100+ back 2% billionaire tax · Manchester 12,000
cleared · Zelenskyy: 165 Russian missiles in a week · COP31: the day after (194
nations reject the Antalya pact) · Israel unity talks resume · Gaza: two killed in
Israeli strike · West Bank settler attacks · Iran war: no deal in sight · Lebanon
seizes 264 kg explosives · Bahrain: strike hits plant, 2 hurt · Benghazi: UN
demands probe of port attacks (CLAIM) · Sudan: defences down drones over Khartoum
(CLAIM) · DRC: fighting traps Ebola teams · Bangladesh: Hasina jailed if she
returns · Seoul minister quits over AI exam row · SK Telecom −7.3% · China eases
margin rules · Seoul readies 10T-won fund.

**Date check — left out (not 23 Nov):** Democrats reach 258 (22 Nov) · Sparta II
fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia pact (21 Nov) ·
Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov). **Not yet:** Dymer search
continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO
evacuating trapped Ebola staff.

## Build

- `draw.py` — draws `entry.png` (1024×1024, PIL). Run `python3 draw.py`.
- `main.py` — stdlib-only entrypoint: validates the PNG header (signature, IHDR
  1024×1024, CRCs, IEND) and copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`. Run `python3 main.py`.
- `entry.png` — the finished front page (180,943 bytes).

Sources: Reuters, AP, Bloomberg, AFP, Yonhap, BBC, WSJ, ESPN, Lowy Institute
(Asia Power Index 2026). Chips: REPORTED = confirmed by wires; CLAIM = one side's
claim, independently unconfirmed; ONGOING = still developing. All times UTC.
Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.
