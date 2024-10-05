import argparse
import os
import shutil
import subprocess
import time

import chardet
from slugify import slugify

clean_up = [
    ".bbl",
    ".blg",
    ".synctex",
    ".bar",
    ".cor",
    ".lua",
    ".lub",
    ".tab",
    ".log",
    ".gz",
    ".aux",
    ".out",
    ".fdb_latexmk",
    ".fls",
    ".xdv",
    ".dvi",
]

clean_path = ["minted"]


def predict_encoding(file_path: str, n_lines: int = 20) -> str:
    """Predict a file's encoding using chardet

    Args:
        file_path (str): _description_
        n_lines (int, optional): _description_. Defaults to 20.

    Returns:
        str: _description_
    """

    # Open the file as binary data
    with open(file_path, "rb") as f:
        # Join binary lines for specified number of lines
        rawdata = b"".join([f.readline() for _ in range(n_lines)])

    return chardet.detect(rawdata)["encoding"]


def convert_utf8(path_to_watch: str) -> None:
    """convertit tous les fichiers qui ne sont pas encodés en UTF-8.


    Args:
        path_to_watch (str): _description_
    """
    # https://stackoverflow.com/questions/1728376/get-a-list-of-all-the-encodings-python-can-encode-to
    paths = initilisation(path_to_watch)
    files = get_files(paths)
    for file in files:
        encoding = predict_encoding(file["name"])

        if encoding != "utf-8":
            print(file["name"], encoding)
            if encoding == "Windows-1252":
                print("Windows-1252 -> cp1252 -> utf-8")

                with open(file["name"], "r", encoding="cp1252") as f:
                    contenu = f.read()
                # print(contenu)
                with open(file["name"], "w", encoding="utf_8") as f:
                    f.write(contenu)

            elif encoding == "ISO-8859-1":
                print("ISO-8859-1-> latin_1 -> utf-8")
                with open(file["name"], "r", encoding="latin_1") as f:
                    contenu = f.read()
                # print(contenu)
                with open(file["name"], "w", encoding="utf_8") as f:
                    f.write(contenu)

            elif encoding == "MacRoman":
                print("MacRoman: no need to convert")

            elif encoding == "ascii":
                print("ascii -> utf-8: don't work. Try manualy")

            # for _ in range(2):
            #     with open(file["name"], "r", encoding=encoding) as f:
            #         contenu = f.read()
            #     with open(file["name"], "w", encoding="utf-8") as f:
            #         f.write(contenu)
            # print(file["name"], "conversion utf-8 réussie")


def initilisation(path_to_watch: str) -> list:
    """Initialisation: récupère les répertoires dans un chemin donné.
    Args:
        path_to_watch (str): path to watch

    Returns:
        list: _description_
    """
    paths = [path_to_watch]
    for root, dirs, files in os.walk(path_to_watch):
        for dir in dirs:
            paths.append(os.path.join(path_to_watch, dir))
    return paths


def get_files(paths: list) -> list[dict]:
    """récupère tous les fichiers .tex dans les répertoires donnés.

    Args:
        paths (list): _description_

    Returns:
        list[dict]: _description_
    """
    files = []
    for path in paths:
        try:
            temp_list = [
                {
                    "name": os.path.join(path, file),
                    "time_modification": os.path.getmtime(os.path.join(path, file)),
                    "path": path,
                }
                for file in os.listdir(path)
                if ".tex" in file
            ]
            files = files + temp_list
        except:
            pass
    return files


def clean_aux(paths: list) -> None:
    """nettoie les fichiers auxiliaires produits par le compilateur LaTeX.

    Args:
        paths (list): _description_
    """
    print(paths)
    for path in paths:
        try:
            print(path)

            for file in os.listdir(path):
                if True in [term in file for term in clean_path]:
                    print(file)
                    if os.path.isdir(file):
                        shutil.rmtree(file, ignore_errors=True)
                else:
                    ext = os.path.splitext((file))[1]
                    if ext in clean_up:
                        os.remove(os.path.join(path, file))

        except:
            pass


def recompile_all(path_to_watch: str, latex_engine: str) -> None:
    """Recomplie all .tex files in path_to_watch folder with latex_engine

    Args:
        path_to_watch (str): _description_
        latex_engine (str): _description_
    """

    cmd = f"latexmk -interaction=nonstopmode -{latex_engine}"
    print(cmd)
    subprocess.call(cmd, shell=True)
    subprocess.call(cmd, shell=True)
    clean_aux([path_to_watch])


def watch(path_to_watch: str, latex_engine: str) -> None:
    """Watch path_to_watch folder

    Args:
        path_to_watch (str): _description_
        latex_engine (str): _description_
    """
    print("Démarrage de la surveillance.")
    print(f"Dossier: {path_to_watch}")
    paths = initilisation(path_to_watch)
    before = get_files(paths)
    while 1:
        time.sleep(10)
        after = get_files(paths)
        added = [f for f in after if not f in before]
        if added:
            print("Fichier ajouté ou modifié")
            for file in added:
                if " " in file["path"]:
                    output = paths[0]
                else:
                    output = file["path"]
                print(output)
                cmd = f"latexmk \"{file['name']}\" -interaction=nonstopmode -{latex_engine} -output-directory=\"{os.path.join(file['path'])}\""
                print(cmd)
                subprocess.call(cmd, shell=True)
            before = after
            clean_aux(paths)


def define_latex_engine(args: argparse) -> str:
    """Process latex engine argument

    Args:
        args (argparse): _description_

    Returns:
        str: _description_
    """
    if args.lualatex:
        print("lualatex")
        return "lualatex"
    else:
        print("xelatex")
        return "xelatex"


def slugify_files(path_to_watch: str, automatique=False):
    """_summary_

    Args:
        path_to_watch (str): _description_
    """
    rename = False
    if not automatique:
        print("Renommage automatique ?")
        entree = input("[O]ui, non par defaut: ")
        if entree.upper() == "O":
            automatique = True
            entree = "O"
        else:
            automatique = False
    for root, dirs, file in os.walk(path_to_watch):
        for dir in dirs:
            if (
                ".git" not in root
                and ".venv" not in root
                and ".venv" not in dir
                and ".git" not in dir
                and "dist" not in dir
                and "dist" not in root
                and "latexcor" not in root
                and "latexcor" not in dir
                and "site" not in root
                and "site" not in dir
            ):
                # print(root, dir, slugify(dir))
                # print(os.path.join(root, dir))
                # print(os.path.join(root, slugify(dir)))
                if os.path.join(root, dir) != os.path.join(root, slugify(dir)):
                    if not automatique:
                        print(f"Renommage de {dir} en {slugify(dir)} ?")
                        entree = input("[O]ui, non par défaut: ")
                    if automatique or entree.upper() == "O":
                        print(f"Renommage de {dir} en {slugify(dir)}")
                        rename = True
                        os.rename(
                            os.path.join(root, dir), os.path.join(root, slugify(dir))
                        )
    if rename:
        if not automatique:
            print("Un ou plusieurs renommages de dossiers ont été effectués.")
            print("Il est nécessaire de relancer le script pour terminer le renommage.")
            print("Voulez-vous le relancer maintenant ?")
            entree = input("[O]ui, non par défaut: ")
        if automatique or entree.upper() == "O":
            slugify_files(path_to_watch, automatique)
    else:
        print("Renommage des dossiers terminé.")

    for root, dirs, files in os.walk(path_to_watch):
        for file in files:
            if ".tex" in file or ".pdf" in file or ".ipynb" in file:
                filename, file_extension = os.path.splitext(file)
                if filename != slugify(filename):
                    if not automatique:
                        print(
                            f"Renommer {file} en {slugify(filename) + file_extension} ?"
                        )

                        # print(filename)
                        # print(file_extension)
                        # print(os.path.join(root, file))
                        # print(os.path.join(root, slugify(filename) + file_extension))
                        entree = input("[O]ui, non par défaut: ")
                    if automatique or entree.upper() == "O":
                        print(f"{file} en {slugify(filename) + file_extension}")
                        rename = True
                        os.rename(
                            os.path.join(root, file),
                            os.path.join(root, slugify(filename) + file_extension),
                        )

    #             else:
    #                 print("Pas renommage")

    # path = path_to_watch + "//**//*.tex"
    # print(path)

    # for file in glob.iglob(path, recursive=True):
    #     print(file)


def main() -> None:
    path_to_watch = os.getcwd()
    parser = argparse.ArgumentParser(description="""Basic usage: latexcor""")
    parser.add_argument(
        "--clean",
        action="store_true",
        default=False,
        help="clean all aux files in current directory",
    )
    parser.add_argument(
        "--recompile",
        action="store_true",
        default=False,
        help="recompile all files in current directory",
    )
    parser.add_argument(
        "--xelatex", action="store_true", default=True, help="xelatex default True"
    )
    parser.add_argument(
        "--lualatex", action="store_true", default=False, help="lualatex default False"
    )
    parser.add_argument(
        "--utf8",
        action="store_true",
        default=False,
        help="convert .tex files to utf-8 encoding",
    )
    parser.add_argument(
        "--slugify",
        action="store_true",
        default=False,
        help="slugify .tex files",
    )
    args = parser.parse_args()
    if args.clean:
        print(f"Nettoyage du dossier: {path_to_watch}")
        clean_aux([path_to_watch])
        print("Fait")
    elif args.recompile:
        latex_engine = define_latex_engine(args)
        print("Recompile tout")
        recompile_all(path_to_watch, latex_engine)
        print("Fait")
    elif args.utf8:
        print("Conversion utf-8")
        convert_utf8(path_to_watch)
    elif args.slugify:
        slugify_files(path_to_watch)
    else:
        latex_engine = define_latex_engine(args)
        watch(path_to_watch, latex_engine)


if __name__ == "__main__":
    main()
