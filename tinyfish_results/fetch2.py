import json, subprocess, os

# Career pages likely to return real job listings (not expired roles)
urls = {
    "amazon":  ["https://www.amazon.jobs/en/search?base_query=Quality+Assurance&loc_query=California"],
    "apple":   ["https://jobs.apple.com/en-us/search?location=united-states-USA&team=software-quality-automation-tools-and-validation-SFTWR-SQAT"],
    "google":  ["https://landing.google.com/engprod/careers/",
                "https://careers.google.com/jobs/results/?q=Test+Engineer"],
    "meta":    ["https://www.metacareers.com/jobsearch/?query=QA+Automation"],
}

key = os.environ["TINYFISH_API_KEY"]
for comp, url_list in urls.items():
    body = json.dumps({"urls": url_list, "format": "markdown"})
    out = subprocess.run(
        ["curl","-s","https://api.fetch.tinyfish.ai",
         "-H",f"X-API-Key: {key}","-H","Content-Type: application/json"],
        capture_output=True, text=True)
    try:
        data = json.loads(out.stdout)
    except Exception as e:
        print(f"{comp}: parse error")
        continue
    print("="*90); print(f"{comp.upper()} — {len(url_list)} url(s)")
    for res in data.get("results", []):
        title = res.get("title") or "(no title)"
        furl = res.get("final_url","")
        text = (res.get("text") or "").replace("\n","\n  ")[:900]
        print(f"\n### {title}")
        print(f"    URL: {furl}")
        # Print lines that look like job titles / locations
        for line in text.split("\n"):
            s = line.strip()
            if not s: continue
            low = s.lower()
            if any(k in low for k in ["engineer","test","automation","quality","qa "]):
                print("     -", s)
