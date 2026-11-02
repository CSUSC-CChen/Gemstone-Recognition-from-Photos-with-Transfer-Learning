"""Recreate the train/dev/test split used in the reports, without training anything.

The split is the one the notebook makes: Kaggle's provided test folder is the test
set, and a stratified 15% of the training folder (seed 467) is the dev set.

Usage:
    python scripts/make_splits.py                      # downloads the data with kagglehub
    python scripts/make_splits.py --data-dir path/to/gemstones-images
"""
import argparse
import glob
import os

import pandas as pd
from sklearn.model_selection import train_test_split

EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")


def find_split_dir(root, name):
    """Find the folder called `name` that holds one subfolder per class."""
    hits = [d for d in glob.glob(os.path.join(root, "**", name), recursive=True)
            if os.path.isdir(d) and any(os.path.isdir(os.path.join(d, c)) for c in os.listdir(d))]
    if not hits:
        raise FileNotFoundError(f"No '{name}' folder with class subfolders under {root}")
    return sorted(hits, key=len)[0]


def list_images(split_dir):
    rows = []
    for cls in sorted(os.listdir(split_dir)):
        d = os.path.join(split_dir, cls)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.lower().endswith(EXTS):
                rows.append((os.path.join(d, f), cls))
    return pd.DataFrame(rows, columns=["path", "label"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", default=None, help="unzipped Kaggle dataset; downloaded if omitted")
    ap.add_argument("--out", default="data/splits", help="output folder for train.csv, dev.csv, test.csv")
    ap.add_argument("--seed", type=int, default=467)
    ap.add_argument("--dev-frac", type=float, default=0.15)
    args = ap.parse_args()

    data_dir = args.data_dir
    if data_dir is None:
        import kagglehub
        data_dir = kagglehub.dataset_download("lsind18/gemstones-images")

    train_dir, test_dir = find_split_dir(data_dir, "train"), find_split_dir(data_dir, "test")
    full_train, test_df = list_images(train_dir), list_images(test_dir)
    test_df = test_df[test_df.label.isin(set(full_train.label))].reset_index(drop=True)
    train_df, dev_df = train_test_split(full_train, test_size=args.dev_frac,
                                        stratify=full_train.label, random_state=args.seed)

    root = os.path.commonpath([train_dir, test_dir])
    os.makedirs(args.out, exist_ok=True)
    for name, df in (("train", train_df), ("dev", dev_df), ("test", test_df)):
        out = df[["path", "label"]].copy()
        out["path"] = out.path.map(lambda p: os.path.relpath(p, root).replace(os.sep, "/"))
        out.to_csv(os.path.join(args.out, f"{name}.csv"), index=False)
        print(f"{name:5s} {len(out):5d} images -> {os.path.join(args.out, name + '.csv')}")


if __name__ == "__main__":
    main()
