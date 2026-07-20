from dataclasses import dataclass, field


@dataclass
class RepositoryKnowledge:

    summary: dict = field(default_factory=dict)

    files: list[dict] = field(default_factory=list)

    functions: list[dict] = field(default_factory=list)

    classes: list[dict] = field(default_factory=list)

    imports: list[dict] = field(default_factory=list)

    routes: list[dict] = field(default_factory=list)

    symbols: list[dict] = field(default_factory=list)

    routes: list[dict] = field(default_factory=list)