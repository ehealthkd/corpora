#%%
from score import main as score_main
from pathlib import Path

# %%
submissions = Path(__file__).parent.parent / "2021" / "submissions"
submission_paths = []

for participant in submissions.iterdir():
    if not participant.is_dir():
        continue

    for submission in participant.iterdir():
        if not submission.is_dir():
            continue

        if not (submission / "testing").exists():
            continue

        submission_paths.append(submission)

# %%
gold = Path(__file__).parent.parent / "2021" / "eval" / "testing"
participants = {}

for submission in submission_paths:
    prefix = submission.parent.stem + "_" + submission.stem + ""
    print(prefix)
    participants[prefix] = score_main(gold, submission / "testing", verbose=False, runs=[1,2,3], scenarios=[1,2,3], prefix=prefix + "_")

# %%
import json

with open("scores_2021.json", "w") as fp:
    json.dump(participants, fp, indent=4)

# %%
import pandas as pd

rows = []

for k,v in participants.items():
    team, submit = k.split("_")

    for run in [1,2,3]:
        run_data = v.get("run%i" % run)

        if run_data is None:
            continue

        r = dict(team=team, submission=submit, run=run)

        for scenario in [1,2,3]:
            scenario_data = run_data["scenario%i" % scenario]
            for metric, value in scenario_data.items():
                r["scenario%i_%s" % (scenario, metric)] = value

        rows.append(r)

df = pd.DataFrame(rows).sort_values("submission", ascending=False).round(5)
df.to_csv("scores_2021.csv", index=False)

df1 = df[["team", "scenario1_f1", "scenario1_precision", "scenario1_recall"]].groupby("team").agg("max")
df1.sort_values("scenario1_f1", ascending=False).to_csv("scores_2021_scn1.csv")

df2 = df[["team", "scenario2_f1", "scenario2_precision", "scenario2_recall"]].groupby("team").agg("max")
df2.sort_values("scenario2_f1", ascending=False).to_csv("scores_2021_scn2.csv")

df3 = df[["team", "scenario3_f1", "scenario3_precision", "scenario3_recall"]].groupby("team").agg("max")
df3.sort_values("scenario3_f1", ascending=False).to_csv("scores_2021_scn3.csv")

 # %%
