import json
import re
from collections import defaultdict
from pathlib import Path

file = Path(".benchmarks/Darwin-CPython-3.12-64bit/0018_report.json")
data = json.loads(file.read_text())


grouped = defaultdict(lambda: defaultdict(list))
for bench in data["benchmarks"]:
    if "[" in bench["name"]:
        match re.split(string=bench["name"], pattern=r"[_\[\]]"):
            case (_, _, _, category, _):
                bench["category"] = category
        grouped[bench["group"]][category].append(bench)

columns = [
    ["ovld", "ovld", "https://github.com/breuleux/ovld"],
    ["beartype", "bear", "https://github.com/beartype/beartype"],
    ["strongtyping", "strong", "https://github.com"],
    ["typeguard", "guard", "https://github.com"],
]
bench_names = [
    "mul_normal",
    "add_ints",
    "add_lists",
    "urlregexp_normal",
    "positive_normal",
    "triple_normal",
    "firstelem_normal",
    "misc_normal",
]


template = "https://github.com/breuleux/ovld/tree/master/benchmarks/test_typechecking.py"

# print("| Benchmark | custom | ovld | md | plum | mm | runtype | sd |")
headers = [f"[{title}]({lnk})" if lnk else title for _, title, lnk in columns]

print(f"| Benchmark | {' | '.join(headers)} |")
print("| --- | ---: | ---: | ---: | ---: |")

for name in bench_names:
    group = grouped[name]
    best = min(
        min(bench["stats"]["median"] for bench in benches)
        for cat, benches in group.items()
    )
    loc = template.format(name)
    line = [f"[{name.replace('_normal', '')}]({loc})"]
    for column, *_ in columns:
        benches = group.get(column, None)
        if not benches:
            line.append("x")
        else:
            value = min(bench["stats"]["median"] for bench in benches) / best
            line.append(f"{value:.2f}")

    print("|".join(["", *line, ""]))
