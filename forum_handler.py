import json
import os
import subprocess
import sys

if "-h" in sys.argv or "--help" in sys.argv:
    print(
        "Usage: python forum_handler.py [start_from] [end_at]\n"
        "start_from: The index of the first forum to scrape.\n"
        "end_at: The index of the last forum to scrape."
    )
    sys.exit(0)
start_from = (
    int(sys.argv[1])
    if len(sys.argv) > 1
    else sys.exit("Error: Please provide a start_from index.")
)
end_at = (
    int(sys.argv[2])
    if len(sys.argv) > 2
    else sys.exit("Error: Please provide an end_at index.")
)



root_folder = "forum_backup"
max_processes = 5

scrape_command: str = (
    "uv run forumscraper "
    + "--html --boards --tags --forums --users "
    + "--retry 5 --retry-delay 40 --wait 0.2 --wait-random 0.2 "
    # + "--thread-pages-max 3 --pages-max 3 --pages-forums-max 3 --pages-threads-max 3 "
)


# Make sure we don't have anything that will mess up a folder name.
def clean_string(s):
    clean_string: str = (
        s.replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("*", "_")
        .replace("?", "_")
        .replace('"', "_")
        .replace("<", "_")
        .replace(">", "_")
        .replace("|", "_")
        .replace("...", "_")
        .replace("Æ", "AE")
        .replace("æ", "ae")
    )

    clean_string = clean_string.strip("_")
    # Convert non-ASCII characters to their closest ASCII representation
    clean_string = clean_string.encode("ascii", "ignore").decode("ascii")
    return clean_string


with open(
    os.path.join(
        root_folder,
        "b-ea846e21764cf4b7b00b57368ab7b038b424a2e9e70302dffe2346d8afe6e6d8",
    ),
    "r",
) as f:
    s = f.read()

forum_structure = json.loads(s)

category = ""
forum = ""
subforum = ""
prev_forum_name = ""
postable_forums = []
count = 0

for i, x in enumerate(forum_structure["categories"]):
    if x["name"] != "":
        category: str = clean_string(x["name"])
    if i % 2 == 0:
        continue
    # print(f"{i} {category}")

    for j, y in enumerate(x["forums"]):
        forum: str = clean_string(y["title"])
        if y["childboards"]:
            forum = prev_forum_name
            # print(f"{i} {category} {j} {forum}")
        else:
            postable_forums.append(
                {
                    "path": os.path.join(root_folder, category, forum),
                    "url": y["link"],
                    "count": count,
                }
            )
            count += 1
        prev_forum_name = forum

        for k, z in enumerate(y["childboards"]):
            subforum: str = clean_string(z["name"])
            # print(f"{i} {category} {j} {forum} {k} {subforum}")
            postable_forums.append(
                {
                    "path": os.path.join(root_folder, category, forum, subforum),
                    "url": z["link"],
                    "count": count,
                }
            )
            count += 1

# print(json.dumps(postable_forums, indent=2))
all_processes = []
for forum_name in postable_forums:
    if int(forum_name["count"]) >= start_from and int(forum_name["count"]) <= end_at:
        os.makedirs(str(forum_name["path"]), exist_ok=True)
        command = (
            scrape_command
            + " --directory "
            + str(forum_name["path"])
            + " vbulletin.forum "
            + str(forum_name["url"])
        )
        all_processes.append(command)


# Runs multiple scraping processes in batches to speed things up but not overload the forum.
while all_processes:
    batch = all_processes[:max_processes]
    all_processes = all_processes[max_processes:]
    procs = [subprocess.Popen(i, shell=True) for i in batch]
    for p in procs:
        p.wait()
