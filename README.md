# bachelor-thesis
Code for my bachelor's thesis.

Performs an NLP analysis over wikipedia pages of persecuted composers in the period of National Socialism in germany.


# How-to's

### setup
``` shell
conda env create --file environment.yml && \
conda activate jessica-thesis && \
jupyter trust bachelor_thesis.ipynb && \
python -m ipykernel install --user --name jessica-thesis --display-name "Jessica's kernel for her thesis"

```

### install dependencies
``` shell
conda env update
```

### clean
``` shell
conda deactivate && \
conda env remove --name jessica-thesis
```

---

*if pip is needed refer to https://stackoverflow.com/a/71548453/11203062*
