# eHealth-KD Corpora - Scripts

This folder contains scripts and tools to aid in the loading, manipulation, and writing of BRAT .ann files.

## Loading the training collection

The `anntools.py` contains a set of classes to load and manipulate BRAT files (Python 3.7 or higher is required).

Start by creating an empty collection:

```python
from anntools import Collection
from pathlib import Path

c = Collection()
```

You can load specific files (note that we pass the path of the `.txt` file):

```python
c.load(Path("/path/to/corpus/2021/training/medline.es.1200.txt"))
```

Or you can load all files at once:

```python
for fname in Path("/path/to/corpus/2021/training/").rglob("*.txt"):
    c.load(fname)
```

Now, you can inspect the contents of the collection. It contains a `sentence` list with `Sentence` objects.
These objects in turn contain the `Keyphrase`s and `Relation`s annotated in each sentence along with their metadata:

```python
>>> len(c.sentences)
1500
>>> c.sentences[0]
Sentence(text='La presencia del gen de células falciformes y otro normal se denomina rasgo drepanocítico.', keyphrases=[Keyphrase(text='presencia', label='Action', id=1, attr=[]), Keyphrase(text='gen', label='Concept', id=2, attr=[]), Keyphrase(text='gen de células falciformes', label='Concept', id=3, attr=[]), Keyphrase(text='normal', label='Concept', id=4, attr=[]), Keyphrase(text='rasgo drepanocítico', label='Concept', id=5, attr=[])], relations=[Relation(from='gen', to='normal', label='in-context'), Relation(from='presencia', to='gen de células falciformes', label='subject'), Relation(from='presencia', to='rasgo drepanocítico', label='same-as'), Relation(from='presencia', to='gen', label='subject')])
>>> c.sentences[100].keyphrases[2]
Keyphrase(text='bombear', label='Action', id=612, attr=[Attribute(label='Negated')])
>>> c.sentences[1000].relations[-1]
Relation(from='bebe', to='obtiene', label='causes')
```

You can also create a `Collection` manually (e.g., from the output of your entity recognition system) and produce an annotated file:

```python
c.dump(Path("output.txt"))
```

This will produce the `.txt` file and the corresponding `.ann` file with all relevant annotations, along with normalized IDs.
