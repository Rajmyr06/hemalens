from fastapi import Request

from app.ml.artifacts import ArtifactBundle


def get_artifact_bundle(request: Request) -> ArtifactBundle:
    return request.app.state.artifact_bundle
