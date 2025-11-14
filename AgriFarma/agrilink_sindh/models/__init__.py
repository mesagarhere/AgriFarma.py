"""
Package initializer for agrilink_sindh.models

This file makes `agrilink_sindh.models` a regular package so imports
like `agrilink_sindh.models.user_model` work reliably.
"""

from . import user_model

__all__ = ["user_model"]
