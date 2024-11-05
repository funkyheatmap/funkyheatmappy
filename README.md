<img
  src="https://raw.githubusercontent.com/funkyheatmap/logo/refs/heads/main/src/attempt1/funkyheatmap_edited.svg"
  class="dark-light" align="right" width="150" alt="image"
/>


# Funkyheatmappy

Funkyheatmap in Python: Generating Funky Heatmaps for Data Frames

## Installation

You can install funkyheatmappy from GitHub using the following command:
```
pip install git+https://github.com/funkyheatmap/funkyheatmappy
```

## Usage

We use the `mtcars` dataset to demonstrate the usage of the `funkyheatmappy` package.

```python
import funkyheatmappy
import pandas as pd

mtcars = pd.read_csv("./test/data/mtcars.csv")
```

You can visualise the dataset as follows:

```python
funkyheatmappy.funkyheatmap(mtcars)
```
<img src="figures/mtcars_basic.png" width="75%" />

## Documentation

Reference documentation is available at [funkyheatmap.github.io/funkyheatmappy](https://funkyheatmap.github.io/funkyheatmappy/).

