import sys
sys.path.insert(0, '.')

from filepulse.config import Config

config = Config()
print(f"Include patterns: {config.include_patterns}")
print(f"Exclude patterns: {config.exclude_patterns}")
print(f"Monitoring events: {config.monitoring_events}")
print(f"Ignore directories: {config.ignore_directories}")
