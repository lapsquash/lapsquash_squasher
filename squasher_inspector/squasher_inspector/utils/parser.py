from squasher_inspector.utils.types.clipping import ClippingRange
from squasher_inspector.utils.types.manifest import Manifest


def parseManifest(filePath: str) -> Manifest:
    with open(filePath, "r") as file:
        manifestJson = file.read()
        return Manifest.from_json(manifestJson)  # type: ignore


def manifest2clippingRange(manifest: Manifest) -> list[ClippingRange]:
    return [
        ClippingRange(asset.elapsedMs, asset.elapsedMs + asset.durationMs)
        for asset in manifest.assets
    ]
