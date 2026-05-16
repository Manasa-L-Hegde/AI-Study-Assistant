"""Configuration management for AI Study Assistant."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


GROQ_BASE_URL = "https://api.groq.com/openai/v1"


def _read_secret(section: str, key: str) -> Any:
	"""Read a Streamlit secret if available, otherwise return None."""
	try:
		import streamlit as st
		
		# Try to access nested secret (e.g., st.secrets["api"]["groq_api_key"])
		if section and hasattr(st.secrets, section):
			section_dict = st.secrets[section]
			if key in section_dict:
				return section_dict[key]
		
		# Fallback: try direct access (e.g., st.secrets["groq_api_key"])
		if key in st.secrets:
			return st.secrets[key]
		
		return None
	except Exception:
		return None


def _env_or_secret(env_name: str, secret_section: str, secret_key: str, default: str = "") -> str:
	"""Get value from environment variable or Streamlit secrets."""
	# First, try environment variable
	value = (os.getenv(env_name) or "").strip()
	if value:
		return value

	# Then try Streamlit secrets with section
	secret_value = _read_secret(secret_section, secret_key)
	if secret_value is not None:
		return str(secret_value).strip()

	return default


def _env_int(name: str, default: int) -> int:
	value = (os.getenv(name) or "").strip()
	if not value:
		return default

	try:
		return int(value)
	except ValueError:
		return default


@dataclass(frozen=True)
class APIConfig:
	"""API-related settings."""

	groq_api_key: str = field(default_factory=lambda: _env_or_secret("GROQ_API_KEY", "api", "groq_api_key"))
	groq_model: str = field(default_factory=lambda: _env_or_secret("GROQ_MODEL", "api", "groq_model", "llama-3.1-8b-instant"))
	base_url: str = GROQ_BASE_URL


@dataclass(frozen=True)
class AppConfig:
	"""Application-level settings."""

	app_name: str = "AI Study Assistant"
	app_env: str = field(default_factory=lambda: _env_or_secret("APP_ENV", "app", "environment", "development"))
	debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "").strip().lower() in {"1", "true", "yes", "on"})
	max_topic_length: int = field(default_factory=lambda: _env_int("MAX_TOPIC_LENGTH", 1000))


@dataclass(frozen=True)
class FeatureFlags:
	"""Feature toggles."""

	enable_analytics: bool = True
	enable_bookmarks: bool = True
	enable_history: bool = True
	enable_export: bool = True
	enable_dark_mode: bool = True


@dataclass(frozen=True)
class CacheConfig:
	"""Caching settings."""

	ttl: int = field(default_factory=lambda: _env_int("CACHE_TTL", 3600))


@dataclass(frozen=True)
class Settings:
	"""Top-level settings container used throughout the app."""

	api: APIConfig = field(default_factory=APIConfig)
	app: AppConfig = field(default_factory=AppConfig)
	features: FeatureFlags = field(default_factory=FeatureFlags)
	cache: CacheConfig = field(default_factory=CacheConfig)


settings = Settings()

