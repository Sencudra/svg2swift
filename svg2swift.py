"""

    Main file

"""

import re
import argparse

from pathlib import Path


from source.ui_bezier_path_generator import UIBezierPathGenerator


def parse_command_arguments():
    """Returns parsed command arguments"""
    parser = argparse.ArgumentParser(description="svg-to-swift converter")
    parser.add_argument("--input_file", required=True, help="SVG file to convert.")
    parser.add_argument("--output_file", default="svg.swift", help="File to save in swift code.")
    return parser.parse_args()


def check_input_file(input_file_path: str):
    """Raises ValueException if file does not exist or has incorrect extension"""
    path2file = Path(input_file_path)

    if not path2file.is_file():
        raise ValueError("File {input} not found!".format(input=input_file_path))
    if not input_file_path.endswith(".svg"):
        raise ValueError("File should have .svg extension")


def get_svg_file_d_attribute(path2file: str):
    """Returns d attribute content"""

    def find_d_attribute(text):
        return re.findall(r'<path d=\"(.*?)\"', text)

    with open(path2file, "r") as input_file:
        content = "".join(input_file.readlines())

        d_contents = find_d_attribute(content)

        if len(d_contents) != 1:
            raise ValueError("For now it should be one d attribute in svg.")
        return d_contents


if __name__ == "__main__":

    GENERATOR = UIBezierPathGenerator()

    # Extracting script arguments
    ARGUMENTS = parse_command_arguments()
    INPUT_FILE = ARGUMENTS.input_file
    OUTPUT_FILE = ARGUMENTS.output_file
    check_input_file(INPUT_FILE)

    RESULT = GENERATOR.generate(get_svg_file_d_attribute(INPUT_FILE))

    with open(OUTPUT_FILE, "w") as file:
        for line in RESULT:
            file.write(line+"\n")

    print("Done. Result stored in {out}".format(out=OUTPUT_FILE))
