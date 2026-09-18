import json, subprocess, os

# Single URL per request to avoid parse errors
single = {
    "apple_search":  ["https://jobs.apple.com/en-us/search?location=united-states-USA&team=software-quality-automation-tools-and-validation-SFTWR-SQAT"],
    "google_careers":["https://landing.google.com/engprod/careers/"],
    "meta_search":   ["https://www.metacareers.com/jobsearch/?query=QA+Automation"],
}

key = os.environ["TINYFISH_API_KEY"]
for comp, url_list in single.items():
    for u in url_list:
        body = json.dumps({"urls":[u],"format":"markdown"})
        out = subprocess.run(
            ["curl","-s","https://api.fetch.tinyfish.ai",
             "-H",f"X-API-Key: {key}","-H","Content-Type: application/json"],
            capture_output=True, text=True)
        print(f"\n===== {comp} =====")
        # Save raw for inspection
        with open(comp+".raw","w") as f: f.write(out.stdout[:200])
        print("RAW[:200]:", out.stdout[:200].replace("\n"," "))
        try:
            data = json.loads(out.stdout)
            for res in data.get("results", []):
                print(f"  TITLE: {res.get('title')}")
                text = (res.get("text") or "")[:1000]
                for line in text.split("\n"):
                    s=line.strip()
                    if any(k in s.lower() for k in ["engineer","test","automation","quality"]):
                        print("     -", s)
        except Exception as e:
            print("  PARSE ERR:", out.stdout[:150])
