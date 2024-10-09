import chardet
from pathlib import Path


class EncodingConverter:
    @staticmethod
    def predict_encoding(file_path: Path, n_lines: int = 20) -> str:
        with file_path.open("rb") as f:
            rawdata = b"".join([f.readline() for _ in range(n_lines)])
        return chardet.detect(rawdata)["encoding"]

    @classmethod
    def convert_utf8(cls, path_to_watch: Path) -> None:
        for file in path_to_watch.rglob("*.tex"):
            encoding = cls.predict_encoding(file)
            print(encoding)
            if encoding != "utf-8":
                print(f"Converting {file} from {encoding} to UTF-8")
                content = file.read_text(encoding=encoding)
                file.write_text(content, encoding="utf-8")
