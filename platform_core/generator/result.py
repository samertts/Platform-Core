from dataclasses import dataclass


@dataclass(slots=True)
class GeneratorResult:
    files_created: list[str]
    directories_created: list[str]
    success: bool

    @property
    def created_files(self) -> int:
        return len(self.files_created)

    @property
    def created_directories(self) -> int:
        return len(self.directories_created)
