import os
import subprocess
import datetime
from collections import defaultdict


def is_valid_date(date_string):
    try:
        # Attempt to parse the date string
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def git_pull_and_log_changes():
    current_dir = os.getcwd()
    repos_dir = os.path.join(current_dir, "repos")
    changelog_dir = os.path.join(current_dir, "changelogs")

    # Loop through all folders in the "repos" directory
    for folder_name in os.listdir(repos_dir):
        folder_path = os.path.join(repos_dir, folder_name)

        # Check if it's a directory
        if os.path.isdir(folder_path):
            # Check if it's a git repository
            if os.path.isdir(os.path.join(folder_path, ".git")):
                os.chdir(folder_path)

                # Perform git pull
                subprocess.run(["git", "pull"])

                # Get the list of files changed in the last 30 days
                result = subprocess.run(
                    [
                        "git",
                        "log",
                        '--since="30 days ago"',
                        "--name-only",
                        "--pretty=format:%cd",
                        "--date=short",
                    ],
                    capture_output=True,
                    text=True,
                )

                # Group changes by date
                changes_by_date = defaultdict(list)
                lines = result.stdout.splitlines()
                for i in range(0, len(lines), 2):
                    date = lines[i]
                    filename = lines[i + 1] if i + 1 < len(lines) else None

                    # Validate the date before processing
                    if filename and is_valid_date(date):
                        changes_by_date[date].append(filename)

                # Write the changes to a changelog file
                if changes_by_date:
                    changelog_path = os.path.join(
                        changelog_dir, f"{folder_name}_changelog.md"
                    )
                    with open(changelog_path, "w") as changelog_file:
                        changelog_file.write(f"# Changelog for {folder_name}\n\n")
                        # Sort dates in reverse order to have newer dates first
                        for date, filenames in sorted(
                            changes_by_date.items(), reverse=True
                        ):
                            changelog_file.write(f"## {date}\n")
                            for filename in filenames:
                                changelog_file.write(f"- {filename}\n")
                            changelog_file.write("\n")

                # Return to the original directory
                os.chdir(current_dir)


if __name__ == "__main__":
    git_pull_and_log_changes()
