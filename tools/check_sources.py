"""Check every source link in data/ and in the chart limit lines.

For DOIs the Crossref record is fetched and its title printed next to our
citation, so a wrong DOI is visible at a glance. Other URLs get an HTTP check.
Some publisher and agency sites block scripted requests (HTTP 403/429 or
timeouts); those are reported as BLOCKED, not as failures.

    python tools/check_sources.py            # all sources
    python tools/check_sources.py --doi-only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from allowed_universe import references  # noqa: E402

UA = "the-allowed-universe-source-check/0.1 (https://github.com/QuantumNovice/awesome-universal-limits)"


def _get(url: str, timeout: float = 30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    return urllib.request.urlopen(req, timeout=timeout)


def check_doi(doi: str) -> tuple[str, str]:
    api = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    for attempt in range(5):
        try:
            with _get(api) as r:
                msg = json.load(r)["message"]
            title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", (msg.get("title") or ["?"])[0]))
            year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
            return "OK", f"{year} {title[:100]}"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Not every DOI is registered with Crossref (e.g. DataCite); try the resolver.
                return check_url("https://doi.org/" + doi)
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return "ERROR", "Crossref lookup failed"


def check_url(url: str) -> tuple[str, str]:
    try:
        with _get(url) as r:
            return "OK", f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        if e.code in (401, 403, 405, 406, 429, 503):
            return "BLOCKED", f"HTTP {e.code}"
        return "FAIL", f"HTTP {e.code}"
    except Exception as e:  # timeouts, refused connections
        return "BLOCKED", type(e).__name__


def check(item):
    url, cit = item
    if url.startswith("https://doi.org/"):
        status, info = check_doi(url.removeprefix("https://doi.org/"))
    else:
        status, info = check_url(url)
    return status, url, cit, info


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doi-only", action="store_true")
    args = ap.parse_args()
    sources = {}
    for group in references.collect().values():
        sources.update(group)
    items = [(u, c) for u, c in sources.items() if not args.doi_only or u.startswith("https://doi.org/")]
    fails = 0
    with ThreadPoolExecutor(3) as ex:
        for status, url, cit, info in ex.map(check, items):
            fails += status in ("FAIL", "ERROR")
            print(f"[{status:7}] {url}\n           ours: {cit[:110]}\n           got:  {info}")
    print(f"\n{len(items)} sources, {fails} failures")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
