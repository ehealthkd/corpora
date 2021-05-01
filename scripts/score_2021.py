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
score_main(gold, Path(__file__).parent.parent / "2021" / "submissions" / "Maoqin" / "872627" / "testing", verbose=False, runs=[1,2,3], scenarios=[1,2,3], prefix="")

# %%
