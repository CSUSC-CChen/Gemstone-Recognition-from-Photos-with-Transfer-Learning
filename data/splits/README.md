# Data split

`train.csv`, `dev.csv`, and `test.csv` list every image in each split. Each row has:

* `path`: the image path relative to the Kaggle dataset folder, for example `train/Amethyst/amethyst_12.jpg`
* `label`: the class name

The test set is Kaggle's provided test folder. The dev set is a stratified 15% of the training folder, made with random seed 467.

To create or recreate the files, run either:

* `python scripts/make_splits.py` from the repo root, or
* the first three code cells of `notebooks/gemstone_midterm.ipynb` in Colab, then download `results/splits/`.

Both produce the same split the reports use: 2,427 train, 429 dev, and 363 test images.
