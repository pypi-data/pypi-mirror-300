import glob, os
import subprocess

ipynb2qmd = True
subdirectory: str | None = "./docs/tutorials"


if __name__ == "__main__":
    if subdirectory:
        os.chdir(subdirectory)
    print(f"current working directory: {os.getcwd()}")
    if ipynb2qmd:
        file_type = "*.ipynb"
    else:
        file_type = "*.qmd"
    for file in glob.glob(file_type):
        subprocess.run(f"quarto convert {file}".split(" "))
