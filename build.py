"""Builds the Shieldright report pages from the campaign-to-date GOAL exports (pulled 10/5/26)."""
import html

AGENCY = "Shieldright LLC"
WHO = 'Prepared for <b>DK Kumar</b><br>Kingwood, TX<br>Campaign to date &middot; through October 5, 2026'
PERIOD = "Campaign to date, through October 5, 2026"
FOOT = "GOAL Performance Marketing<br>Contact, quote and policy rates are calculated on submitted leads. Inbound calls are reported separately."

# source rows: name, impressions, clicks, leads, calls, contacted, quoted, bound, spend
CAMPAIGNS = {
    "auto": dict(
        title="Auto (TX)", slug="auto-tx-performance-review",
        searches=17465, impr=411, clicks=76, leads=62, calls=8, contacted=16, quoted=9, bound=0, spend=760.85,
        sources=[
            ("Premium Referral", 226, 22, 17, 1, 3, 1, 0, 231.83),
            ("Internal SEO 2", 28, 11, 11, 2, 2, 1, 0, 105.28),
            ("Premium Paid Search 2", 24, 11, 11, 3, 3, 3, 0, 103.40),
            ("Native/Display/Social 2", 51, 11, 7, 0, 1, 1, 0, 106.69),
            ("Premium Paid Search 6", 28, 6, 5, 1, 2, 1, 0, 70.50),
            ("Premium Email C", 19, 6, 4, 0, 1, 1, 0, 64.39),
            ("Premium Paid Search 5C", 3, 3, 3, 1, 1, 0, 0, 31.96),
            ("Paid Search", 4, 3, 2, 0, 1, 1, 0, 23.82),
            ("Email", 18, 2, 1, 0, 1, 0, 0, 13.81),
            ("Premium Paid Search 3", 2, 1, 1, 0, 1, 0, 0, 9.17),
        ],
        other=("Other sources", 8, 0, 0, 0, 0, 0, 0, 0.00), other_n=16,
    ),
    "home": dict(
        title="Home (TX)", slug="home-tx-performance-review",
        searches=9913, impr=415, clicks=78, leads=65, calls=3, contacted=15, quoted=7, bound=0, spend=718.38,
        sources=[
            ("Tier 1", 155, 29, 25, 0, 5, 2, 0, 267.09),
            ("Tier 3", 214, 28, 22, 2, 7, 4, 0, 257.88),
            ("Tier 2", 33, 20, 17, 1, 3, 1, 0, 184.20),
            ("Home Search B", 13, 1, 1, 0, 0, 0, 0, 9.21),
        ],
        other=("Other sources", 0, 0, 0, 0, 0, 0, 0, 0.00), other_n=6,
    ),
}

PALETTE = ["#057BE5", "#2D90EE", "#5BA7E6", "#8CC0EE", "#0A3A6B", "#0C5FB0", "#3A92E0", "#B5D5F3", "#6A7482", "#C5CFDC"]


def pct(a, b):
    return f"{(a / b * 100):.1f}%" if b else "0.0%"


def money(x):
    return f"${x:,.2f}"


def head(title, css_prefix):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_prefix}assets/report-dashboard.css">
</head>
"""


def report(c):
    t = c["title"]
    L, S = c["leads"], c["spend"]
    out = [head(f"{AGENCY} &middot; {t} Performance Review", "../")]
    out.append(f"""<body>
<div class="shell">
  <aside class="side">
    <a class="back" href="../index.html">&larr; All reports</a>
    <img class="logo" src="../assets/goal-wordmark-white.png" alt="GOAL">
    <div class="eb">Performance Review &middot; {t}</div>
    <h1>{AGENCY}</h1>
    <div class="who">{WHO}</div>
    <nav><a href="#s1"><span class="dot"></span>Key metrics</a><a href="#s2"><span class="dot"></span>Conversion funnel</a><a href="#s3"><span class="dot"></span>Performance by source</a><a href="#s4"><span class="dot"></span>Recommendations</a></nav>
    <div class="foot">{FOOT}</div>
  </aside>
  <main class="main">
<div class="exec"><p>{PERIOD}: {c['searches']:,} shopper searches, {c['impr']:,} ad displays, and {c['clicks']} clicks, producing <b>{L} leads</b> and {c['calls']} inbound calls. <b>{c['contacted']} contacted</b> ({pct(c['contacted'], L)}) and <b>{c['quoted']} quoted</b> ({pct(c['quoted'], L)}). {c['bound']} policies bound. Ad spend {money(S)}.</p></div>
""")
    # 01 KPIs
    out.append(f"""<section class="block" id="s1">
<div class="bhead"><span class="ix">01</span><div><h2>Key metrics</h2><p>{PERIOD}</p></div></div>
<div class="kgrid"><div class="kc"><div class="v">{pct(c['contacted'], L)}</div><div class="k">Contact rate</div><div class="d">{c['contacted']} of {L} leads</div></div>
<div class="kc"><div class="v">{pct(c['quoted'], L)}</div><div class="k">Quote rate</div><div class="d">{c['quoted']} of {L} leads &middot; {pct(c['quoted'], c['contacted'])} of contacted</div></div>
<div class="kc"><div class="v">{c['bound']}</div><div class="k">Policies bound</div><div class="d">{c['bound']} of {c['quoted']} quoted</div></div>
<div class="kc"><div class="v">{money(S)}</div><div class="k">Ad spend</div><div class="d">{c['clicks']} clicks &middot; {money(S / c['clicks'])} avg cost per click</div></div>
<div class="kc"><div class="v">{money(S / c['contacted'])}</div><div class="k">Cost per contact</div><div class="d">{c['contacted']} leads contacted</div></div>
<div class="kc"><div class="v">{money(S / c['quoted'])}</div><div class="k">Cost per quote</div><div class="d">{c['quoted']} leads quoted</div></div></div>
</section>
""")
    # 02 funnel
    steps = [
        ("Shopper searches", "auctions entered", c["searches"], None),
        ("Your ad shown", "impressions", c["impr"], c["searches"]),
        ("Ad clicked", "to your quote page", c["clicks"], c["impr"]),
        ("Leads", "submitted", L, c["clicks"]),
        ("Contacted", "reached", c["contacted"], L),
        ("Quoted", "presented", c["quoted"], c["contacted"]),
        ("Bound", "policies issued", c["bound"], c["quoted"]),
    ]
    widths = [100, 72, 62, 60, 42, 34, 6]
    colors = ["#9cc4ec", "#5ba7e6", "#3a92e0", "#057BE5", "#0c5fb0", "#0a3a6b", "#00172D"]
    out.append(f"""<section class="block" id="s2">
<div class="bhead"><span class="ix">02</span><div><h2>Conversion funnel</h2><p>{PERIOD}</p></div></div>
<div class="fpanel">
""")
    for (lab, sub, v, prev), w, col in zip(steps, widths, colors):
        p = "100%" if prev is None else pct(v, prev)
        out.append(f'<div class="fstep"><div class="lab">{lab}<small>{sub}</small></div>\n<div class="fbar"><i style="background:{col};width:{w}%">{v:,}</i></div>\n<div class="pct">{p}</div></div>\n')
    out.append(f"""<div class="fnote">The ad appeared on {c['impr']:,} of {c['searches']:,} searches ({pct(c['impr'], c['searches'])}) and was clicked {c['clicks']} times ({pct(c['clicks'], c['impr'])} of displays). {L} clicks became a lead ({pct(L, c['clicks'])}); {c['contacted']} were contacted ({pct(c['contacted'], L)} of leads); {c['quoted']} received quotes ({pct(c['quoted'], c['contacted'])} of contacted); {c['bound']} policies bound ({pct(c['bound'], c['quoted'])} of quotes). {c['calls']} inbound calls were attributed to the campaign in the same period. Percentages are stage to stage.</div></div>
</section>
""")
    # 03 sources
    srcs = c["sources"]
    off = 0.0
    circles, legend = [], []
    for i, s in enumerate(srcs):
        if s[3] == 0:
            continue
        d = s[3] / L * 100
        circles.append(f'<circle cx="21" cy="21" r="15.915" fill="none" stroke="{PALETTE[i]}" stroke-width="6" stroke-dasharray="{d:.2f} {100 - d:.2f}" stroke-dashoffset="{-off:.2f}" transform="rotate(-90 21 21)"></circle>')
        legend.append(f'<div class="li"><span class="sw" style="background:{PALETTE[i]}"></span><span class="nm">{s[0]}</span><span class="vl">{s[3]}</span></div>')
        off += d
    rows = []
    allrows = list(srcs) + ([c["other"]] if c["other_n"] else [])
    for s in allrows:
        name = s[0] if s is not c["other"] else f'{s[0]}<small>{c["other_n"]} sources</small>'
        rows.append(f'<tr><td class="nm">{name}</td><td>{s[1]}</td><td>{s[2]}</td><td><b>{s[3]}</b></td><td>{s[4]}</td><td>{s[5]}</td><td>{s[6]}</td><td>{s[7]}</td><td>{money(s[8])}</td></tr>')
    rows.append(f'<tr class="tot"><td class="nm">Total</td><td>{c["impr"]}</td><td>{c["clicks"]}</td><td><b>{L}</b></td><td>{c["calls"]}</td><td>{c["contacted"]}</td><td>{c["quoted"]}</td><td>{c["bound"]}</td><td>{money(S)}</td></tr>')
    # spend vs quote share
    pairs = []
    for s in srcs:
        if s[8] < 20:
            continue
        sp, qs = s[8] / S * 100, (s[6] / c["quoted"] * 100 if c["quoted"] else 0)
        pairs.append(f"""<div class="pair"><div class="pl">{s[0]}</div>
<div class="srow"><div class="lab">Spend</div><div class="tr"><i style="width:{sp:.1f}%;background:#0A3A6B"></i></div><div class="vl">{sp:.1f}% <small>{money(s[8])}</small></div></div>
<div class="srow"><div class="lab">Quote</div><div class="tr"><i style="width:{qs:.1f}%;background:#057BE5"></i></div><div class="vl">{qs:.1f}% <small>{s[6]} quote{'s' if s[6] != 1 else ''}</small></div></div></div>""")
    out.append(f"""<section class="block" id="s3">
<div class="bhead"><span class="ix">03</span><div><h2>Performance by source</h2><p>{PERIOD}</p></div></div>
<div class="stack"><div class="panel"><div class="pt">Leads by source</div>
<div class="mix"><div class="donut"><svg viewBox="0 0 42 42" width="180" height="180"><circle cx="21" cy="21" r="15.915" fill="none" stroke="#EFF2F7" stroke-width="6"></circle>
{chr(10).join(circles)}</svg>
<div class="center"><div class="n">{L}</div><div class="l">leads</div></div></div>
<div class="legend">{''.join(legend)}</div></div></div>
<div class="panel"><div class="pt">Source results</div><table class="ctab stable"><thead><tr><th>Source</th><th>Ad shown</th><th>Clicks</th><th>Leads</th><th>Calls</th><th>Contacted</th><th>Quoted</th><th>Bound</th><th>Spend</th></tr></thead><tbody>
{chr(10).join(rows)}</tbody>
</table></div>
<div class="panel"><div class="pt">Share of spend and share of quotes</div>
<div class="keyrow"><span><i class="sw" style="background:#0A3A6B"></i>Spend share</span><span><i class="sw" style="background:#057BE5"></i>Quote share</span></div>
{chr(10).join(pairs)}
<div class="pnote">Sources with $20 or more in spend. Quote share is each source's quotes as a share of all {c['quoted']} quotes.</div></div>
</div>
</section>
""")
    # 04 recommendations
    out.append(f"""<section class="block" id="s4">
<div class="bhead"><span class="ix">04</span><div><h2>Recommendations</h2><p>Before the next review</p></div></div>
<div class="plan"><div class="pstep"><div class="num">1</div>
<div><div class="h">Bind status on quoted leads</div>
<div class="b"><b>{c['quoted']} leads</b> are recorded as quoted and {c['bound']} as bound. An updated disposition export from Ricochet, including bound policies and premium, keeps cost per policy current in the next report.</div></div></div>
<div class="pstep"><div class="num">2</div>
<div><div class="h">Uncontacted leads</div>
<div class="b"><b>{L - c['contacted']} of {L} leads</b> ({pct(L - c['contacted'], L)}) have no recorded contact. Continued follow-up across phone, text and email applies to these leads.</div></div></div>
<div class="pstep"><div class="num">3</div>
<div><div class="h">Inbound calls</div>
<div class="b">{c['calls']} inbound calls were attributed to this campaign. Answer and quote results for calls will be reported separately.</div></div></div></div>
</section>
<div class="pnote" style="border-top:none;padding-top:10px;">Source: GOAL campaign and source-settings exports for {t}, campaign to date, pulled October 5, 2026. Lead outcomes reflect dispositions recorded in GOAL and cover web leads.</div>
  </main>
</div>
</body>
</html>
""")
    return "".join(out)


def hub():
    a, h = CAMPAIGNS["auto"], CAMPAIGNS["home"]
    return head(f"{AGENCY} &middot; Performance Reports", "") + f"""<style>
.main{{background:var(--gray);}}
.package{{background:var(--off);border:1px solid var(--line);border-radius:16px;padding:30px 34px;margin-bottom:30px;}}
.package .eb{{font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);}}
.package h2{{font-size:30px;font-weight:900;color:var(--ink);letter-spacing:-.02em;line-height:1.1;margin:12px 0 14px;}}
.package p{{font-size:14.5px;color:var(--body);line-height:1.62;max-width:760px;}}
.package p b{{color:var(--ink);font-weight:700;}}
.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;}}
.rcard{{position:relative;background:var(--white);border:1px solid var(--line);border-radius:16px;padding:28px 30px 26px;box-shadow:0 4px 16px rgba(0,23,45,.05);display:flex;flex-direction:column;overflow:hidden;transition:transform .2s,box-shadow .2s;}}
.rcard:hover{{transform:translateY(-3px);box-shadow:0 16px 38px rgba(0,23,45,.12);}}
.rcard::before{{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--blue);}}
.rcard .num{{display:inline-flex;align-items:center;justify-content:center;width:36px;height:30px;border-radius:8px;background:#E6F1FD;color:var(--blue);font-size:13px;font-weight:800;}}
.rcard .tag{{font-size:11px;font-weight:800;letter-spacing:.07em;text-transform:uppercase;color:var(--muted);margin-top:18px;}}
.rcard h3{{font-size:21px;font-weight:800;color:var(--ink);letter-spacing:-.01em;margin:7px 0 10px;}}
.rcard .desc{{font-size:13.5px;color:var(--muted);line-height:1.58;flex:1;}}
.rcard .pills{{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 22px;}}
.rcard .pills span{{font-size:11.5px;font-weight:600;color:var(--body);background:var(--gray);border-radius:999px;padding:6px 12px;}}
.rcard .open{{align-self:flex-start;font-size:14px;font-weight:700;color:var(--blue);text-decoration:none;}}
.botnote{{margin-top:30px;font-size:12.5px;color:var(--muted);border-top:1px solid var(--line);padding-top:20px;}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr;}}}}
</style>
<body>
<div class="shell">
  <aside class="side">
    <img class="logo" src="assets/goal-wordmark-white.png" alt="GOAL">
    <div class="eb">Performance Reports</div>
    <h1>{AGENCY}</h1>
    <div class="who">{WHO}</div>
    <nav><a href="#r1"><span class="dot"></span>Auto (TX) Performance Review</a><a href="#r2"><span class="dot"></span>Home (TX) Performance Review</a></nav>
    <div class="foot">{FOOT}</div>
  </aside>
  <main class="main">
    <div class="package">
      <div class="eb">Account Review &middot; October 5, 2026</div>
      <h2>October 5 review package</h2>
      <p>Campaign-to-date results for the <b>Auto (TX)</b> and <b>Home (TX)</b> campaigns through <b>October 5, 2026</b>. Combined: {a['leads'] + h['leads']} leads, {a['calls'] + h['calls']} inbound calls, {a['contacted'] + h['contacted']} contacted, {a['quoted'] + h['quoted']} quoted, {a['bound'] + h['bound']} policies bound, on {money(a['spend'] + h['spend'])} ad spend.</p>
    </div>
    <div class="grid">
      <div class="rcard" id="r1">
        <div class="num">01</div>
        <div class="tag">Auto (TX) &middot; Campaign to Date</div>
        <h3>Auto Performance Review</h3>
        <p class="desc">{a['searches']:,} shopper searches, {a['leads']} leads, {a['contacted']} contacted, {a['quoted']} quoted, and {a['bound']} policies bound on {money(a['spend'])} spend.</p>
        <div class="pills"><span>Key metrics</span><span>Funnel</span><span>Source results</span></div>
        <a class="open" href="reports/{a['slug']}.html">Open report &rarr;</a>
      </div>
      <div class="rcard" id="r2">
        <div class="num">02</div>
        <div class="tag">Home (TX) &middot; Campaign to Date</div>
        <h3>Home Performance Review</h3>
        <p class="desc">{h['searches']:,} shopper searches, {h['leads']} leads, {h['contacted']} contacted, {h['quoted']} quoted, and {h['bound']} policies bound on {money(h['spend'])} spend.</p>
        <div class="pills"><span>Key metrics</span><span>Funnel</span><span>Source results</span></div>
        <a class="open" href="reports/{h['slug']}.html">Open report &rarr;</a>
      </div>
    </div>
    <div class="botnote">Reports reflect GOAL Platform data and are updated before each review. Each report prints cleanly to PDF.</div>
  </main>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    for c in CAMPAIGNS.values():
        # integrity: source rows reconcile to the campaign totals
        tot = [sum(s[i] for s in c["sources"]) + c["other"][i] for i in range(1, 9)]
        exp = [c["impr"], c["clicks"], c["leads"], c["calls"], c["contacted"], c["quoted"], c["bound"], c["spend"]]
        assert all(abs(x - y) < 0.01 for x, y in zip(tot, exp)), (c["title"], tot, exp)
        open(f"reports/{c['slug']}.html", "w").write(report(c))
    open("index.html", "w").write(hub())
    print("ok")
