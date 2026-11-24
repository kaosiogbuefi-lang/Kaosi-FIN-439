"""Generate Project 2's visible executed-output report.

Run from this folder: python build_output.py
"""

from app_logic import build_project2_results, render_report


def main():
    print(render_report(build_project2_results()))


if __name__ == "__main__":
    main()
