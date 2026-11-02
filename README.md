# Gemstone Recognition from Photos

Identify a gemstone from a single photo, out of 87 classes, using classical features, a CNN trained from scratch, and transfer learning from an ImageNet-pretrained ResNet-50.

Course project for CSCI 467 (Introduction to Machine Learning), University of Southern California, Fall 2026. Author: Cindy Chen.

## Results so far (midterm)

Test set: Kaggle's provided test folder (363 images, 4 to 5 per class). Hyperparameters were chosen on a held-out dev set.

| Method | Top-1 | Top-5 | Macro F1 |
|---|---:|---:|---:|
| Majority class | 1.4 | 6.9 | 0.0 |
| Logistic regression (color histogram) | 61.2 | 90.1 | 59.1 |
| Random Forest (color + texture features) | 69.7 | 95.0 | 68.1 |
| Small CNN trained from scratch | 69.7 | 95.3 | 69.0 |
| ResNet-50, linear probe (frozen) | 65.3 | 90.1 | 63.6 |
| **ResNet-50, fine-tuned last two stages** | **79.6** | **96.1** | **79.4** |

All numbers are percentages. Full tables, tuning runs, and figures are in `results/midterm/`, and the write-up is in `report/midterm/`.

Main findings:

* Fine-tuning a pretrained network beats every other method by about 10 points.
* Frozen ImageNet features alone do worse than hand-made color and texture features. Retraining the later layers is what makes transfer learning work here.
* The most common mistakes are look-alike stones of the same color, and stones within the garnet family.

## Repository layout

```
gemstone-recognition/
├── README.md
├── requirements.txt
├── notebooks/
│   └── gemstone_midterm.ipynb   full pipeline: data, baselines, CNN, ResNet-50, error analysis
├── scripts/
│   └── make_splits.py           recreates the train/dev/test split without training
├── data/
│   ├── raw/                     Kaggle download (not committed)
│   ├── splits/                  train.csv, dev.csv, test.csv
│   └── museum/                  my own photos, a real-world test set (in progress)
├── results/
│   └── midterm/                 metrics, LaTeX tables, figures
└── report/
    └── midterm/                 LaTeX source of the midterm report
```

Model weights are not in the repo because of their size.

## Data

* **Kaggle Gemstones Images** by Daria Chemkaeva: https://www.kaggle.com/datasets/lsind18/gemstones-images
  About 3,200 images in 87 classes, with a provided train and test folder.
* **Split.** The provided test folder is the test set. A stratified 15% of the training folder (random seed 467) is the dev set. This gives 2,427 train, 429 dev, and 363 test images. The exact file lists are in `data/splits/`.
* **Museum test set (in progress).** Photos I took of stones on display in the Robert Procop Gem and Mineral Hall at the Natural History Museum of Los Angeles County, and of stones in my personal collection. Labels come from the museum's display cards. See `data/museum/README.md`.

## How to reproduce

The pipeline runs in Google Colab on a free T4 GPU and takes about 40 to 60 minutes.

1. Open `notebooks/gemstone_midterm.ipynb` in Google Colab.
2. Choose Runtime > Change runtime type > T4 GPU.
3. Choose Runtime > Run all. The notebook downloads the Kaggle dataset itself.
4. At the end it downloads `results.zip`. Its contents match `results/midterm/`.

To recreate only the data split (a few seconds, no GPU needed):

```
pip install -r requirements.txt
python scripts/make_splits.py
```

To build the report, compile `report/midterm/main.tex` with pdflatex and bibtex. It reads the numbers, tables, and figures from `results/midterm/`.

## Status

* [x] Proposal
* [x] Midterm report: baselines, scratch CNN, and ResNet-50 transfer learning
* [ ] Final report: full fine-tuning with stronger regularization, cropping to the stone, test-time augmentation, ablations, results over 3 seeds, and the museum test set
