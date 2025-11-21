"""
Path utilities for PyInstaller compatibility
Handles relative paths correctly for both development and packaged executables
"""

import sys
import os
from pathlib import Path


def get_resource_path(relative_path: str) -> str:
    # If running as PyInstaller executable, use sys._MEIPASS
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, relative_path)


def get_save_path(relative_path: str = "") -> str:
    if getattr(sys, 'frozen', False):
        # Packaged executable: store saves in user's AppData folder
        save_dir = Path(os.getenv('APPDATA', os.path.expanduser('~'))) / 'LifeOfPy'
    else:
        # Development: store in project data/save/ folder
        save_dir = Path(__file__).resolve().parents[1] / 'data' / 'save'
    
    # Create directory if it doesn't exist
    save_dir.mkdir(parents=True, exist_ok=True)
    
    if relative_path:
        return str(save_dir / relative_path)
    else:
        return str(save_dir)
