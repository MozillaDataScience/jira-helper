# class JiraTicket(models.Model):
#     summary = models.CharField(max_length=8192)
#     issue_key = models.CharField(max_length=16, primary_key=True)
#     resolution = models.CharField(max_length=16)
#     assignee = models.EmailField(max_length=255)
#     reporter = models.EmailField(max_length=255)
#     created = models.DateTimeField()
#     resolved = models.DateTimeField()
#     description = models.TextField()
#     last_comment = models.TextField()

import json
import subprocess
import sys

import dateutil.parser
import pandas as pd
import pytz

COLUMN_MAP = {
    "Summary": "summary",
    "Issue key": "issue_key",
    "Resolution": "resolution",
    "Assignee": "assignee",
    "Reporter": "reporter",
    "Created": "created",
    "Resolved": "resolved",
    "Description": "description",
    "Custom field (Last Comment)": "last_comment",
}


def translate(s):
    return subprocess.run(
        ["pandoc", "-f", "textile", "-t", "html"],
        input=s,
        capture_output=True,
        check=True,
        encoding="utf-8",
    ).stdout


df = pd.read_csv(sys.argv[1]).fillna("")
rows = []
for _, row in df.iterrows():
    d = {
        "model": "tickets.JiraTicket",
        "pk": row["Issue key"],
        "fields": {v: row[k] for k, v in COLUMN_MAP.items()},
    }
    d["fields"]["description"] = translate(d["fields"]["description"])
    for k in ("created", "resolved"):
        if not d["fields"][k]:
            del d["fields"][k]
            continue
        d["fields"][k] = (
            dateutil.parser.parse(d["fields"][k]).replace(tzinfo=pytz.UTC).isoformat()
        )
    rows.append(d)

print(json.dumps(rows, indent=2))
