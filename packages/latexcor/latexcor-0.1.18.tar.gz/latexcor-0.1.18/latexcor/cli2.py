import argparse
from pathlib import Path
from .latex_compiler import LatexCompiler
from .encoding_converter import EncodingConverter
from .file_manager import FileManager
from .mermaid_processor import MermaidProcessor


def main() -> None:
    parser = argparse.ArgumentParser(description="LaTeX Compiler and File Manager")
    parser.add_argument("--clean", action="store_true", help="Clean auxiliary files")
    parser.add_argument("--recompile", action="store_true", help="Recompile all files")
    parser.add_argument(
        "--engine",
        choices=["xelatex", "lualatex"],
        default="xelatex",
        help="LaTeX engine to use",
    )
    parser.add_argument(
        "--utf8", action="store_true", help="Convert .tex files to UTF-8"
    )
    parser.add_argument(
        "--slugify", action="store_true", help="Slugify file and directory names"
    )
    parser.add_argument(
        "--mermaid", action="store_true", help="Process Mermaid diagrams in LaTeX files"
    )
    args = parser.parse_args()

    path_to_watch = Path.cwd()

    if args.clean:
        LatexCompiler.clean_aux(path_to_watch, paths=True)
    elif args.recompile:
        for file in path_to_watch.rglob("*.tex"):
            LatexCompiler.compile_latex(file, args.engine)
        LatexCompiler.clean_aux(path_to_watch)
    elif args.utf8:
        EncodingConverter.convert_utf8(path_to_watch)
    elif args.slugify:
        FileManager.slugify_files(path_to_watch)
    elif args.mermaid:
        MermaidProcessor.process_all_mermaid(path_to_watch)
    else:
        LatexCompiler.watch(path_to_watch, args.engine)


if __name__ == "__main__":
    main()
