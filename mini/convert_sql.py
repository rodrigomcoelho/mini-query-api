from os.path import join, split
from re import sub


def add_prefix_to_filename(file_path: str, prefix: str) -> str:
    dir_name, base_name = split(file_path)
    new_base_name = prefix + base_name
    new_file_path = join(dir_name, new_base_name)

    return new_file_path


def convert(path: str) -> None:
    lines = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file.readlines():
            parsed_line = sub(r"\s+", " ", line.replace("\n", " ")).strip()
            if parsed_line:
                lines.append(parsed_line)

    new_path = add_prefix_to_filename(path, "converted_")
    with open(new_path, "w", encoding="utf-8") as file:
        file.write(" ".join(lines))


if __name__ == "__main__":
    convert("mini/query.sql")
