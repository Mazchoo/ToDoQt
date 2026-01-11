"""Level scaling configuration model for gamification system"""

import json
from typing import List, Optional, Tuple
from pathlib import Path


class LevelEntry:
    """Represents a single level in the scaling system"""

    def __init__(self, threat_level: str, points_required: int):
        self.threat_level = threat_level
        self.points_required = points_required

    def __repr__(self):
        return f"LevelEntry(threat_level='{self.threat_level}', points_required={self.points_required})"


class LevelScalingConfig:
    """Manages level scaling configuration and provides helper methods"""

    def __init__(self, config_path: str = "level_config.json"):
        """Load level configuration from JSON file"""
        self.levels: List[LevelEntry] = []
        self._load_config(config_path)

    def _load_config(self, config_path: str):
        """Load and parse the level configuration file"""
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Level config file not found: {config_path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.levels = [
            LevelEntry(entry["threat_level"], entry["points_required"])
            for entry in data
        ]

        # Ensure levels are sorted by points_required
        self.levels.sort(key=lambda x: x.points_required)

    def get_current_level(self, total_points: int) -> LevelEntry:
        """
        Get the current level based on total points.
        Returns the highest level that the user has reached.
        """
        current_level = self.levels[0]  # Start with the first level

        for level in self.levels:
            if total_points >= level.points_required:
                current_level = level
            else:
                break

        return current_level

    def get_next_level(self, total_points: int) -> Optional[LevelEntry]:
        """
        Get the next level to reach based on current total points.
        Returns None if already at max level.
        """
        for level in self.levels:
            if total_points < level.points_required:
                return level

        return None  # Already at max level

    def get_points_till_next_level(self, total_points: int) -> int:
        """
        Calculate points needed to reach the next level.
        Returns 0 if already at max level.
        """
        next_level = self.get_next_level(total_points)

        if next_level is None:
            return 0  # Already at max level

        return next_level.points_required - total_points

    def get_level_info(self, total_points: int) -> Tuple[str, int]:
        """
        Get current level threat_level string and points till next level.

        Returns:
            Tuple of (threat_level_string, points_till_next_level)
        """
        current_level = self.get_current_level(total_points)
        points_till_next = self.get_points_till_next_level(total_points)

        return (current_level.threat_level, points_till_next)

    def get_max_level(self) -> LevelEntry:
        """Get the maximum level available"""
        return self.levels[-1] if self.levels else None

    def get_total_levels(self) -> int:
        """Get the total number of levels"""
        return len(self.levels)
