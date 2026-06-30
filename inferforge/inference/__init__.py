"""Inference backends for InferForge."""

from inferforge.inference.base import InferenceBackend
from inferforge.inference.mock import MockInferenceBackend

__all__ = ["InferenceBackend", "MockInferenceBackend"]
