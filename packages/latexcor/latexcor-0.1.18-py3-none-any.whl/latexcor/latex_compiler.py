import subprocess
import time
from pathlib import Path
from .utils import TexFile
from .config import CLEAN_UP_EXTENSIONS, CLEAN_PATHS
from .mermaid_processor import MermaidProcessor
import shutil


class LatexCompiler:
    @staticmethod
    def get_tex_files(path: Path) -> list[TexFile]:
        return [
            TexFile(name=file, time_modification=file.stat().st_mtime, path=file.parent)
            for file in path.rglob("*.tex")
        ]

    @staticmethod
    def clean_aux(path: Path, paths=False) -> None:
        for item in path.rglob("*"):
            if paths and item.is_dir() and item.name in CLEAN_PATHS:
                shutil.rmtree(item, ignore_errors=True)
            elif item.is_file() and item.suffix in CLEAN_UP_EXTENSIONS:
                item.unlink()

    @staticmethod
    def compile_latex(file: Path, latex_engine: str) -> None:
        try:
            with file.open("r", encoding="utf-8") as f:
                content = f.read()
            if (
                "documentclass" not in content
                or "begin{document}" not in content
                or "end{document}" not in content
            ):
                print(f"Skipping {file}: incomplete LaTeX structure")
                return
            if "begin{mermaid}" in content:
                print(f"{file}: Mermaid diagrams found")
                MermaidProcessor.process_mermaid(file)
            cmd = f'latexmk "{file}" -interaction=nonstopmode -{latex_engine} -output-directory="{file.parent}"'
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            print(f"Error compiling {file}: {str(e)}")

    @classmethod
    def watch(cls, path_to_watch: Path, latex_engine: str) -> None:
        print(f"Watching folder: {path_to_watch}")
        before = cls.get_tex_files(path_to_watch)
        while True:
            time.sleep(10)
            after = cls.get_tex_files(path_to_watch)
            added = [f for f in after if f not in before]
            if added:
                print("File added or modified")
                for file in added:
                    cls.compile_latex(file.name, latex_engine)
                before = after
                cls.clean_aux(path_to_watch)
