from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin, dataclass_json


@dataclass_json
@dataclass
class ManifestAssetAnalysis(DataClassJsonMixin):
    title: str
    tags: list[str]
    description: str


@dataclass_json
@dataclass
class ManifestAsset(DataClassJsonMixin):
    elapsedMs: int
    durationMs: int
    analysis: ManifestAssetAnalysis | None


@dataclass_json
@dataclass
class Manifest(DataClassJsonMixin):
    name: str
    description: str
    version: str
    startWith: int
    assets: list[ManifestAsset]
