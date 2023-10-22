from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin, dataclass_json


@dataclass_json
@dataclass
class ProjectManifestAssetAnalysis(DataClassJsonMixin):
    title: str
    tags: list[str]
    description: str


@dataclass_json
@dataclass
class ProjectManifestAsset(DataClassJsonMixin):
    elapsedMs: int
    durationMs: int
    analysis: ProjectManifestAssetAnalysis | None


@dataclass_json
@dataclass
class ProjectManifest(DataClassJsonMixin):
    name: str
    description: str
    version: str
    startWith: int
    assets: list[ProjectManifestAsset]
