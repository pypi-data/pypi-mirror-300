#!/usr/bin/env python3
# =============================================================================
"""!Code Information:
    Package settings, includes static urls that may change over time

    WARNING: This is not a module, make sure that the directory where
    this file is included do NOT count with an __init__.py
"""
# =============================================================================


class Settings:

    balena_api_key_env_name = "BALENA_API_KEY"
    balena_api_url = "https://api.balena-cloud.com/v6/"

    protected_resources = ["device", "application"]
