import argparse
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import List, Dict
import hashlib

import chardet
from slugify import slugify

CLEAN_UP_EXTENSIONS = [
    ".bbl", ".blg", ".synctex", ".bar", ".cor", ".lua", ".lub", ".tab",
    ".log", ".gz", ".aux", ".out", ".fdb_latexmk", ".fls", ".xdv", ".dvi"
]

CLEAN_PATHS = ["minted"]

def predict_encoding(file_path: Path, n_lines: int = 20) -> str:
    """Predict a file's encoding using chardet"""
    with file_path.open('rb') as f:
        rawdata = b"".join([f.readline() for _ in range(n_lines)])
    return chardet.detect(rawdata)["encoding"]

def convert_utf8(path_to_watch: Path) -> None:
    """Convert all files that are not encoded in UTF-8."""
    for file in path_to_watch.rglob('*.tex'):
        encoding = predict_encoding(file)
        if encoding != "utf-8":
            print(f"Converting {file} from {encoding} to UTF-8")
            content = file.read_text(encoding=encoding)
            file.write_text(content, encoding='utf-8')

def get_tex_files(path: Path) -> List[Dict[str, any]]:
    """Get all .tex files in the given path and subdirectories."""
    return [
        {
            "name": file,
            "time_modification": file.stat().st_mtime,
            "path": file.parent
        }
        for file in path.rglob('*.tex')
    ]

def clean_aux(path: Path) -> None:
    """Clean auxiliary files produced by the LaTeX compiler."""
    for item in path.rglob('*'):
        if item.is_dir() and item.name in CLEAN_PATHS:
            shutil.rmtree(item, ignore_errors=True)
        elif item.is_file() and item.suffix in CLEAN_UP_EXTENSIONS:
            item.unlink()

def compile_latex(file: Path, latex_engine: str) -> None:
    """Compile a LaTeX file using the specified engine."""
    with file.open('r', encoding='utf-8') as f:
        content = f.read()
    if 'documentclass'not in content:
            print(f"Skipping {file}: no document class found")
            return
    if 'begin{document}' not in content:
            print(f"Skipping {file}: no begin document found")
            return
    if 'end{document}' not in content:
            print(f"Skipping {file}: no end document found")
            return
    if 'begin{mermaid}' in content:
            print(f"{file}: Mermaid diagrams found")
            process_mermaid(file)
    cmd = f"latexmk \"{file}\" -interaction=nonstopmode -{latex_engine} -output-directory=\"{file.parent}\""
    subprocess.run(cmd, shell=True, check=True)

def watch(path_to_watch: Path, latex_engine: str) -> None:
    """Watch the given path for changes and compile modified .tex files."""
    print(f"Watching folder: {path_to_watch}")
    before = get_tex_files(path_to_watch)
    while True:
        time.sleep(10)
        after = get_tex_files(path_to_watch)
        added = [f for f in after if f not in before]
        if added:
            print("File added or modified")
            for file in added:
                compile_latex(file['name'], latex_engine)
            before = after
            clean_aux(path_to_watch)

def slugify_files(path_to_watch: Path, automatic: bool = False) -> None:
    """Rename files and directories to use slugified names."""
    def confirm(prompt: str) -> bool:
        return automatic or input(f"{prompt} [y/N]: ").lower() == 'y'

    for item in path_to_watch.rglob('*'):
        if item.is_dir() and item.name not in ['.git', '.venv', 'dist', 'latexcor', 'site']:
            new_name = slugify(item.name)
            if item.name != new_name:
                if confirm(f"Rename directory {item.name} to {new_name}?"):
                    item.rename(item.parent / new_name)
        elif item.is_file() and item.suffix in ['.tex', '.pdf', '.ipynb']:
            new_name = slugify(item.stem) + item.suffix
            if item.name != new_name:
                if confirm(f"Rename file {item.name} to {new_name}?"):
                    item.rename(item.parent / new_name)

def mermaid_to_image(mermaid_code: str, output_file: str) -> None:
    """Convert Mermaid code to an image using mermaid-cli."""
    subprocess.run(['mmdc', '-i', '-', '-o', output_file], input=mermaid_code, text=True, check=True)

def process_mermaid(file_path: Path) -> None:
    """Process Mermaid diagrams in LaTeX files."""
    try:
            Path.mkdir("mermaid")
    except FileExistsError:
            pass
    content = file_path.read_text(encoding='utf-8')
   
    hash_text = hashlib.md5(content.encode()).hexdigest()
    hash_file_path = Path(f"mermaid/{hash_text}.mermaid")
    if not hash_file_path.exists():
        
        hash_file_path.write_text("processed", encoding='utf-8')
    else:
        return


    def replace_mermaid(match):
        mermaid_block = match.group(0)
        mermaid_code = match.group(1).replace("%","")
        
        # Générer un hash unique pour le code Mermaid
        hash_object = hashlib.md5(mermaid_code.encode())
        unique_hash = hash_object.hexdigest()
        
        image_file = f"mermaid_diagram_{unique_hash}.png"
        
        # Vérifier si l'image existe déjà
        if not Path(image_file).exists():
            mermaid_to_image(mermaid_code, image_file)
            include = f"\n\\includegraphics{{{image_file}}}"
        else:
            include = ""
        
        # Commenter le bloc Mermaid original s'il n'est pas déjà commenté
        if not mermaid_block.strip().startswith('%'):
            commented_block = '\n'.join(f'{line}' for line in mermaid_block.split('\n'))
        else:
            commented_block = mermaid_block
        
        return f"{commented_block}{include}"

    # Remplacer les blocs Mermaid par des commentaires et des inclusions d'images
    pattern = r'(?<!%)\\begin\{mermaid\}(.*?)\\end\{mermaid\}'
    new_content = re.sub(pattern, replace_mermaid, content, flags=re.DOTALL)
    if "killmermaid" not in new_content:
        new_content = new_content.replace("\\begin{document}", 
                                          """\\usepackage{environ}\n\\NewEnviron{killmermaid}{}
\\let\mermaid\\killmermaid
\\let\endmermaid\\endmermaid
\\begin{document}""")
    file_path.write_text(new_content, encoding='utf-8')
    print(f"Processed Mermaid diagrams in {file_path}")

def process_all_mermaid(path_to_watch: Path) -> None:
    """Process Mermaid diagrams in all LaTeX files in the given directory."""
    for file in path_to_watch.rglob('*.tex'):
        process_mermaid(file)

def main() -> None:
    parser = argparse.ArgumentParser(description="LaTeX Compiler and File Manager")
    parser.add_argument("--clean", action="store_true", help="Clean auxiliary files")
    parser.add_argument("--recompile", action="store_true", help="Recompile all files")
    parser.add_argument("--engine", choices=['xelatex', 'lualatex'], default='xelatex', help="LaTeX engine to use")
    parser.add_argument("--utf8", action="store_true", help="Convert .tex files to UTF-8")
    parser.add_argument("--slugify", action="store_true", help="Slugify file and directory names")
    parser.add_argument("--mermaid", action="store_true", help="Process Mermaid diagrams in LaTeX files")
    args = parser.parse_args()

    path_to_watch = Path.cwd()

    if args.clean:
        print(f"Cleaning directory: {path_to_watch}")
        clean_aux(path_to_watch)
    elif args.recompile:
        print("Recompiling all files")
        for file in path_to_watch.rglob('*.tex'):
            compile_latex(file, args.engine)
        clean_aux(path_to_watch)
    elif args.utf8:
        print("Converting to UTF-8")
        convert_utf8(path_to_watch)
    elif args.slugify:
        slugify_files(path_to_watch)
    elif args.mermaid:
        print("Processing Mermaid diagrams")
        process_all_mermaid(path_to_watch)
    else:
        watch(path_to_watch, args.engine)

if __name__ == "__main__":
    main()