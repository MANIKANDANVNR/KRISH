from pathlib import Path


class DocumentProcessor:

    SUPPORTED = {
        ".txt",
        ".md",
        ".csv",
        ".json",
    }

    def extract(self, path):

        path = Path(path)

        if path.suffix.lower() not in self.SUPPORTED:

            raise ValueError(
                f"Unsupported document: "
                f"{path.suffix}"
            )

        return path.read_text(
            encoding="utf-8"
        )