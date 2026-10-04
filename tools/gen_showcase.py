"""產生作品展示用的 SVG 示範圖（每件作品 5 張，800x500），輸出至 images/showcase/<作品代碼>/<序號>.svg。

用法：
    python tools/gen_showcase.py              產生全部作品
    python tools/gen_showcase.py web-cafe     只產生指定作品（可列多個）
僅使用 Python 標準函式庫，無需額外安裝。
"""
import importlib
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
OUT_DIR = TOOLS_DIR.parent / "images" / "showcase"
sys.path.insert(0, str(TOOLS_DIR))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows 主控台預設 cp950，避免中文輸出錯誤

# 各模組皆提供 SCREENS = {作品代碼: [畫面函式, ...]}
MODULE_NAMES = ["web_pages", "platforms", "automation_pages", "bot_pages", "games_casual_pages", "games_advanced"]


def collect_screens() -> dict:
    """彙整所有模組的畫面設定，並檢查作品代碼不可重複。"""
    merged = {}
    for name in MODULE_NAMES:
        module = importlib.import_module(f"showcase.{name}")
        for item_id, scenes in module.SCREENS.items():
            if item_id in merged:
                raise ValueError(f"作品代碼重複：{item_id}（模組 {name}）")
            merged[item_id] = scenes
    return merged


def render_item(item_id: str, scenes: list) -> None:
    item_dir = OUT_DIR / item_id
    item_dir.mkdir(parents=True, exist_ok=True)
    for index, scene in enumerate(scenes, start=1):
        try:
            (item_dir / f"{index}.svg").write_text(scene(), encoding="utf-8")
        except Exception as exc:
            raise RuntimeError(f"產生 {item_id}/{index}.svg 失敗（{scene.__name__}）：{exc}") from exc
    print(f"✓ {item_id}：{len(scenes)} 張")


def main(argv: list) -> None:
    screens = collect_screens()
    targets = argv or list(screens)
    unknown = [t for t in targets if t not in screens]
    if unknown:
        raise SystemExit(f"找不到作品代碼：{', '.join(unknown)}")
    for item_id in targets:
        render_item(item_id, screens[item_id])


if __name__ == "__main__":
    main(sys.argv[1:])
