from dataclasses import dataclass, field


@dataclass
class Task:

    description: str

    metadata: dict = field(
        default_factory=dict
    )

    task_id: str | None = None