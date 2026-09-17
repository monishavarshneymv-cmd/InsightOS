"""
InsightOS - Configuration Module
Defines system paths, database connection parameters, UI design tokens, and analytical thresholds.
"""

from pathlib import Path
import os

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DATA_DIR.mkdir(exist_ok=True)

# Database Configuration
# Default is local SQLite for instant zero-dependency execution.
# Can be overridden via DATABASE_URL environment variable for PostgreSQL.
SQLITE_DB_PATH = DATA_DIR / "insight_os.db"
DEFAULT_DB_URL = f"sqlite:///{SQLITE_DB_PATH}"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# Aesthetic / Design System Tokens (Executive Editorial Slate)
# Explicitly avoiding generic neon/glowing AI palettes.
THEME = {
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F8FAFC",
    "bg_tertiary": "#F1F5F9",
    "border_subtle": "#E2E8F0",
    "border_strong": "#CBD5E1",
    "text_primary": "#0F172A",
    "text_secondary": "#475569",
    "text_muted": "#94A3B8",
    "accent_primary": "#1E293B",  # Deep Slate
    "accent_brand": "#2563EB",    # Precision Cobalt Blue
    "status_success": "#059669",  # Emerald (Retention, Growth)
    "status_warning": "#D97706",  # Amber (Attention, Moderate Risk)
    "status_danger": "#BE123C",   # Crimson (Churn, Anomaly, Loss)
    "status_info": "#0284C7",     # Sky (Information)
    "font_family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
}

# Analytical & Machine Learning Defaults
RANDOM_SEED = 42
CHURN_THRESHOLD = 0.50
ANOMALY_CONTAMINATION = 0.03  # Expect ~3% anomalous transactions
FORECAST_HORIZON_DAYS = 60
RFM_CLUSTERS = 4

# API Keys (Optional - System works 100% offline with smart local fallback)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
