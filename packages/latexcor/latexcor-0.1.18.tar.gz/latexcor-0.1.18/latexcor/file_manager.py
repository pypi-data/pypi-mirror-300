from pathlib import Path
from slugify import slugify


class FileManager:
    @staticmethod
    def slugify_files(path_to_watch: Path, automatic: bool = False) -> None:
        def confirm(prompt: str) -> bool:
            return automatic or input(f"{prompt} [y/N]: ").lower() == "y"

        for item in path_to_watch.rglob("*"):
            if item.is_dir() and item.name not in [
                ".git",
                ".venv",
                "dist",
                "latexcor",
                "site",
            ]:
                new_name = slugify(item.name)
                if item.name != new_name and confirm(
                    f"Rename directory {item.name} to {new_name}?"
                ):
                    item.rename(item.parent / new_name)
            elif item.is_file() and item.suffix in [".tex", ".pdf", ".ipynb"]:
                new_name = slugify(item.stem) + item.suffix
                if item.name != new_name and confirm(
                    f"Rename file {item.name} to {new_name}?"
                ):
                    item.rename(item.parent / new_name)
