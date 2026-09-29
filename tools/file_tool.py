from pathlib import Path


class FileTool:

    name = "file"

    permission = "tool.file"

    risk = "medium"

    description = (
        "Reads and writes files inside "
        "the configured KRISH workspace."
    )

    def __init__(
        self,
        root,
    ):

        self.root = Path(
            root
        ).resolve()

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _safe_path(
        self,
        path,
    ):

        if not isinstance(
            path,
            str,
        ):
            raise TypeError(
                "Path must be text."
            )

        target = (
            self.root / path
        ).resolve()

        try:

            target.relative_to(
                self.root
            )

        except ValueError as error:

            raise PermissionError(
                "Path escapes allowed "
                "directory."
            ) from error

        return target

    def read(
        self,
        path,
    ):

        target = self._safe_path(
            path
        )

        if not target.is_file():

            raise FileNotFoundError(
                str(path)
            )

        if target.stat().st_size > 5_000_000:

            raise ValueError(
                "File exceeds 5 MB limit."
            )

        return target.read_text(
            encoding="utf-8"
        )

    def write(
        self,
        path,
        content,
    ):

        if len(content) > 5_000_000:

            raise ValueError(
                "Content exceeds 5 MB limit."
            )

        target = self._safe_path(
            path
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        target.write_text(
            content,
            encoding="utf-8",
        )

        return str(target)