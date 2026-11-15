"""Build the museum test set from a hand-filled manifest.

Usage:
    python scripts/build_museum_set.py --raw data/museum/raw --manifest data/museum/manifest.csv

manifest.csv columns (one row per photo you want to keep, in angle order):
    original       file name in the raw folder, e.g. IMG_9005.jpeg
    object_id      one ID per physical stone, e.g. amethyst_museum02
    display_label  card text, e.g. "254 carat amethyst (purple quartz) gemstone"
    kaggle_class   exact Kaggle class name, or blank if no match
    type           faceted / cabochon / rough
    source         museum / own
    notes          free text (LACM number, soft focus, glare, looks purple...)

What it does:
    * fixes rotation, strips EXIF (removes GPS and phone info)
    * resizes so the longer side is 1024 px
    * names files <object_id>_<type>_a<NN>.jpg, numbering angles per stone
    * writes data/museum/photos/ and data/museum/labels.csv
    * warns about kaggle_class names that are not in data/splits/train.csv
"""
import argparse
import csv
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageOps

try:  # iPhone HEIC support, optional
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

MAX_SIDE = 1024
FIELDS = ["file", "object_id", "display_label", "kaggle_class", "type", "source", "notes"]


def known_classes(repo: Path):
    train = repo / "data" / "splits" / "train.csv"
    if not train.exists():
        return None
    with open(train, newline="") as f:
        rows = list(csv.DictReader(f))
    for key in ("label", "class", "kaggle_class"):
        if rows and key in rows[0]:
            return {r[key] for r in rows}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default="data/museum/raw")
    ap.add_argument("--manifest", default="data/museum/manifest.csv")
    ap.add_argument("--out", default="data/museum")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parents[1]
    raw, out = Path(args.raw), Path(args.out)
    photos = out / "photos"
    photos.mkdir(parents=True, exist_ok=True)

    classes = known_classes(repo)
    angle = defaultdict(int)
    rows, problems = [], []

    with open(args.manifest, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            r = {k: (v or "").strip() for k, v in r.items()}
            if not r.get("original"):
                continue
            src = raw / r["original"]
            if not src.exists():
                problems.append(f"missing file: {src}")
                continue
            oid, typ = r["object_id"], r.get("type") or "faceted"
            angle[oid] += 1
            name = f"{oid}_{typ}_a{angle[oid]:02d}.jpg"

            im = Image.open(src)
            try:
                im = ImageOps.exif_transpose(im)
            except Exception:
                pass
            im = im.convert("RGB")
            im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            im.save(photos / name, "JPEG", quality=92)  # saved without EXIF

            kc = r.get("kaggle_class", "")
            if kc and classes is not None and kc not in classes:
                problems.append(f"{r['original']}: kaggle_class '{kc}' not in train.csv")

            rows.append({
                "file": name, "object_id": oid,
                "display_label": r.get("display_label", ""), "kaggle_class": kc,
                "type": typ, "source": r.get("source") or "museum",
                "notes": r.get("notes", ""),
            })

    with open(out / "labels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    stones = {r["object_id"] for r in rows}
    scored = {r["object_id"] for r in rows if r["kaggle_class"]}
    print(f"{len(rows)} photos, {len(stones)} stones ({len(scored)} with a Kaggle class)")
    for p in problems:
        print("WARNING:", p)


if __name__ == "__main__":
    main()
