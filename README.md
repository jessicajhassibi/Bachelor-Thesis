# bachelor-thesis

Code for my bachelor's thesis. 

Performs NLP analysis and binary classification over the wikipedia articles of two wikipedia lists. \
The code is generic! \
You can suit it to your problem by changing the groups.ini file and placing your lists urls and the wiki categories you are looking for there. 

My two lists/ classes are:
- [Gottbegnateden-Liste](https://de.wikipedia.org/wiki/Gottbegnadeten-Liste)
- [Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten](https://de.wikipedia.org/wiki/Liste_der_vom_NS-Regime_oder_seinen_Verb%C3%BCndeten_verfolgten_Komponisten)

## Background

In the period of National Socialism in Germany the Nazis basically classified composers into two groups:
- "Gifted" Composers which they admired and supported 
- "Degenerated" Composers which were persecuted or killed by them

Given the labels created by the Nazis: \
<b>Can we train a Machine Learning model that is able to correctly classify a composer by his biography on wikipedia?</b>

## How-to's

Run project by executing the jupyter notebooks in ascending order:
* 0_data_scraping.ipynb
* 1_data_analysis.ipynb
* 2_data_preparation.ipynb
* 3_topic_modeling.ipynb
* 4_word2vec_text_classification.ipynb


### setup
``` shell
conda env create --file environment.yml && \
conda activate thesis && \
python -m ipykernel install --user --name thesis --display-name "thesis kernel"

```

#### required for spacy:
Download Language models of languages you want to use. \
Note: There might be problems installing those on apple machine with M1 chip. \
Switching to another machine solved it for me... 
``` shell
python -m spacy download 'de_core_news_sm' # german model
python -m spacy download 'en_core_web_sm' # english model
python -m spacy download 'xx_ent_wiki_sm' # multilingual model
```

### update dependencies
``` shell
conda env update
```

### clean
``` shell
conda deactivate && \
conda env remove --name thesis
```

### download pretrained word vectors

We use the Glove vectors trained on Wikipedia 2014 and Gigaword 5.\
[Get them here](https://nlp.stanford.edu/projects/glove/) and place to models/word_vectors.


