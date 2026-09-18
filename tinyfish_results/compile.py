import json

with open("all_company_jobs.json") as f:
    data = json.load(f)

# Collect all real job postings (exclude generic "Job search" homepages/aggregators noise)
skip_phrases = ["job search", "careers at", "search our job", "apple roles and opportunities"]
good = []
for comp, d in data.items():
    for j in d.get("results", []):
        title = (j.get("title") or "").lower()
        url = j.get("url","")
        if not title: continue
        # skip generic search-homepage entries that aren't specific roles
        if any(p in title for p in skip_phrases): continue
        good.append({"company": comp, "title": j.get("title"),
                     "url": url, "site": j.get("site")})

# Filter to roles that match QA / Test / Automation / SDET profile
match_kw = ["qa","test","automation","quality","sdet","validation"]
matched = [g for g in good if any(k in (g["title"].lower()) for k in match_kw)]

# Save
with open("matched_jobs.json","w") as f:
    json.dump({"total_real_postings": len(good), "matched_to_profile": matched}, f, indent=2)

print(f"\nTotal real postings: {len(good)}")
print(f"Matched to QA/Automation profile: {len(matched)}\n")

# Show top 20 best matches
print("TOP MATCHING JOBS:")
for i, g in enumerate(matched[:20], 1):
    print(f"{i:2}. [{g['company'].upper()}] {g['title']}")
    print(f"     -> {g['url']}")
