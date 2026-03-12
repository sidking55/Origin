import sys
from pathlib import Path

def analyze_file(file_path):
    """
    Analyze a single log file and return:
    - count of ERROR messages
    - list of ERROR lines
    """

    error_count = 0
    error_messages = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "ERROR" in line:
                error_count += 1
                error_messages.append(line.strip())

    return error_count, error_messages


def main(log_dir):

    log_path = Path(log_dir)

    total_errors = 0
    all_errors = []

    # recursively get all log files
    file_list = log_path.rglob("*.log")

    for file in file_list:
        count, errors = analyze_file(file)

        total_errors += count
        all_errors.extend(errors)

    print(f"Total number of errors: {total_errors}")
    print("Here are all the errors:")

    for error in all_errors:
        print(error)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 log_analyzer.py <log_directory>")
        sys.exit(1)

    log_directory = sys.argv[1]
    main(log_directory)