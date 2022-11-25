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
<b>Can we train a classification model that is able to correctly classify a composer by his biography on wikipedia?</b>

## How-to's

Run project by executing the jupyter notebooks in ascending order:
* 0_data_scraping.ipynb
* 1_data_analysis.ipynb
* 2_data_preparation.ipynb
etc.


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

# Using Docker
Start docker container for the first time:
```shell
docker run -it \
    --volume $(pwd):/home/Bachelor-Thesis \
    --workdir /home/Bachelor-Thesis \
    --publish 8888:8888 \
    --name bachelor-thesis \
    continuumio/miniconda3 /bin/bash
```
You should be in the container shell now.

Run setup scripts within container shell: 
```shell
apt update \
&& apt install -y gcc vim \
&& conda env create --file environment.yml \
&& conda activate thesis \
&& echo 'conda activate thesis' >> ~/.bashrc \
&& python -m spacy download 'en_core_web_sm' \
&& python -m spacy download 'de_core_news_sm' \
&& python -m spacy download 'fr_core_news_sm' \
&& python -m spacy download 'xx_ent_wiki_sm' \
&& python -m ipykernel install --user --name thesis --display-name "thesis kernel"
```

To go into container shell and environment
```shell
docker exec -it bachelor-thesis bash
conda activate thesis 
```

To start container
```shell
docker start bachelor-thesis
```

When installations are done run jupyter notebook in container.
```shell
jupyter notebook --port=8888 --no-browser --allow-root --ip='*' --NotebookApp.token='' --NotebookApp.password=''
```

Jupyter notebook are under [http://localhost:8888](http://localhost:8888)

### download pretrained word vectors

We use the Glove vectors trained on Wikipedia 2014 and Gigaword 5.\
[Get them here](https://nlp.stanford.edu/projects/glove/) and place to models/word_vectors.


