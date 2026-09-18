import urllib.parse, json, subprocess, os, time

# Targeted queries for each of the 20 companies -> real job postings
queries = [
    ("amazon",        "Quality Assurance Automation Engineer jobs at Amazon California United States"),
    ("microsoft",     "Software Test Automation QA Engineer job at Microsoft Washington United States"),
    ("google",        "SWE and Test Engineer TE job at Google California United States"),
    ("meta",          "QA SDET Quality Assurance Engineer job at Meta California United States"),
    ("apple",         "Software QA Automation Test Engineer job at Apple California United States"),
    ("tcs",           "Quality Assurance Validation Automation Engineer jobs at TCS United States"),
    ("infosys",       "QA Test Automation Validation Consultant job at Infosys United States"),
    ("cognizant",     "QA Automation Test Engineer job at Cognizant United States"),
    ("wipro",         "Quality Assurance Automation Test Engineer job at Wipro United States"),
    ("hcltech",       "QA Validation Automation Test Engineer job at HCL Technologies United States"),
    ("ey",            "Quality Assurance QA Analyst jobs at EY Deloitte United States"),
    ("deloitte",      "Senior Associate QA Quality Assurance job at Deloitte United States"),
    ("pwc",           "Quality Assurance QA Analyst jobs at PwC United States"),
    ("goldmansachs",  "Software Test QA Automation job at Goldman Sachs New York United States"),
    ("jpmc",          "Software QA Automation Test Engineer job at J.P. Morgan United States"),
    ("bankofamerica", "Software Test QA Automation job at Bank of America United States"),
    ("capitalone",    "QA Software Test Automation Engineer job at Capital One Virginia United States"),
    ("qualcomm",      "Senior QA Test Automation Engineer job at Qualcomm San Diego California United States"),
    ("ltmindtree",    "QA Test Validation Automation Engineer job at LTIMindtree United States"),
    ("walmart",       "Software Test QA Automation Engineer job at Walmart Arkansas United States"),
]

key = os.environ["TINYFISH_API_KEY"]
all_results = {}
for comp, q in queries:
    url = "https://api.search.tinyfish.ai?query=" + urllib.parse.quote(q)
    out = subprocess.run(["curl","-s",url,"-H",f"X-API-Key: {key}"], capture_output=True, text=True)
    try:
        data = json.loads(out.stdout)
        jobs = []
        for r in (data.get("results") or [])[:10]:
            jobs.append({"position": r.get("position"), "site": r.get("site_name"),
                          "title": r.get("title"), "url": r.get("url")})
        all_results[comp] = {"query": q, "results": jobs}
    except Exception:
        all_results[comp] = {"query": q, "results": [], "error": out.stdout[:100]}
    time.sleep(2)

with open("all_company_jobs.json","w") as f:
    json.dump(all_results, f, indent=2)

print("Completed searches for", len(all_results), "companies\n")
for comp, d in all_results.items():
    jobs = d.get("results", [])
    titles = [j["title"] for j in jobs if j.get("title")]
    print(f"{comp} ({len(jobs)} results): {titles[:3]}")
