# Agent Internet Allowlist

Codex Cloud setup scripts can use the default dependency access needed for `pip`.

For the agent phase, enable internet access only if the task needs live source scouting. Prefer `GET`, `HEAD`, and `OPTIONS` methods only.

## Minimum For Dry Run

No external domains are required for fixture-only dry runs.

## Recommended 1.0 Source Domains

Use these domains for live scouting:

```text
kickstarter.com
www.kickstarter.com
indiegogo.com
www.indiegogo.com
crowdsupply.com
www.crowdsupply.com
producthunt.com
www.producthunt.com
api.producthunt.com
hackaday.com
hackaday.io
techcrunch.com
www.techcrunch.com
wired.com
www.wired.com
theverge.com
www.theverge.com
engadget.com
www.engadget.com
newatlas.com
www.newatlas.com
yankodesign.com
www.yankodesign.com
designboom.com
www.designboom.com
36kr.com
www.36kr.com
geekpark.net
www.geekpark.net
ifanr.com
www.ifanr.com
sspai.com
www.sspai.com
ithome.com
www.ithome.com
mydrivers.com
www.mydrivers.com
leikeji.com
www.leikeji.com
pingwest.com
www.pingwest.com
jiqizhixin.com
www.jiqizhixin.com
qbitai.com
www.qbitai.com
zealer.com
www.zealer.com
```

## WeCom Later

Add WeCom/document domains only after live output is ready and reviewed. Keep write-capable network access separate from source-reading access.
