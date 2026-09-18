import json, subprocess, os

urls = {
    "amazon": [
        "https://www.amazon.jobs/en/jobs/10414519/quality-assurance-engineer-ii-amazon-search-relevance-measurement",
        "https://www.amazon.jobs/en/search?base_query=QA+Automation&loc_query=California",
    ],
    "apple": [
        "https://jobs.apple.com/en-us/details/200615747/software-automation-qa-engineer-security",
        "https://jobs.apple.com/en-us/details/200679164-0836/quality-engineer-test-and-automation",
    ],
    "google": [
        "https://careers.google.com/jobs/results/127670839075054278-software-test-engineer/",
        "https://landing.google.com/engprod/careers/",
    ],
}

key = os.environ["TINYFISH_API_KEY"]
for comp, url_list in urls.items():
    body = json.dumps({"urls": url_list, "format": "markdown"})
    out = subprocess.run(
        ["curl","-s","-X POST","https://api.fetch.tinyfish.ai",
         "-H",f"X-API-Key: {key}","-H","Content-Type: application/json","--data-binary",body],
        capture_output=True, text=True)
    try:
        data = json.loads(out.stdout)
    except Exception as e:
        print(f"{comp}: fetch parse error -> {out.stdout[:200]}")
        continue
    print("="*80); print(f"{comp.upper()} ({len(url_list)} urls)")
    for res in data.get("results", []):
        print(f"\n--- {res.get('title')} | {res.get('final_url','')}")
        text = res.get("text","")[:1500]
        for line in text.split("\n"):
            s = line.strip()
            if not s: continue
            low = s.lower()
            if any(k in low for k in ["job","engineer","location","qa","test","automation"]):
                print("  ", s)
