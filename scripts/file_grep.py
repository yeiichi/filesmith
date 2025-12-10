import re
from pathlib import Path

keywords = ["moldova", "luxembourg", "norway"]
pat = re.compile("|".join(re.escape(k) for k in keywords), re.I)

for f in Path.cwd().glob("*.json"):
    text = f.read_text()
    matches = {m.lower() for m in pat.findall(text)}
    if all(k in matches for k in keywords):
        print(f.name)
