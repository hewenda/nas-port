import os, json, threading, time, tempfile
from pathlib import Path
from typing import Any, Dict
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

_CONFIG_PATH = Path("config.yml")
_lock = threading.Lock()
_cache: Dict[str, Any] | None = None
_cache_mtime: float | None = None
_yaml = YAML()
_yaml.preserve_quotes = True
_yaml.indent(mapping=2, sequence=2, offset=2)

def _read_file() -> Dict[str, Any]:
    if not _CONFIG_PATH.exists():
        return {}
    with _CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = _yaml.load(f) or CommentedMap()
        if not isinstance(data, (dict, CommentedMap)):
            raise ValueError("config.yml 根节点必须为对象")
        return data

def _atomic_write(content: str) -> None:
    tmp_fd, tmp_path = tempfile.mkstemp(prefix="config_", suffix=".yml", dir=str(_CONFIG_PATH.parent))
    try:
        with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp_path, _CONFIG_PATH)  # 原子替换
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def _dump_yaml(data: Dict[str, Any]) -> str:
    # 使用 ruamel.yaml 序列化以保留注释/引号/顺序
    from io import StringIO
    buf = StringIO()
    _yaml.dump(data, buf)
    return buf.getvalue()

def get_config() -> Dict[str, Any]:
    global _cache, _cache_mtime
    with _lock:
        mtime = _CONFIG_PATH.stat().st_mtime if _CONFIG_PATH.exists() else -1
        if _cache is not None and _cache_mtime == mtime:
            return _cache
        data = _read_file()
        _cache, _cache_mtime = data, mtime
        return data

def update_config(patch: Dict[str, Any]) -> Dict[str, Any]:
    """浅合并 patch 到根；复杂合并可递归实现。"""
    global _cache, _cache_mtime
    with _lock:
        data = _read_file()
        data.update(patch)
        _atomic_write(_dump_yaml(data))
        # 刷新缓存与 mtime
        _cache = data
        _cache_mtime = _CONFIG_PATH.stat().st_mtime if _CONFIG_PATH.exists() else -1
        return data