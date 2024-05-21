# SEMAS

This is the repository of the Python (3.7+) implementation of SEMAS (**SE**mantic **M**ulti-**A**gent **S**ystem), which integrates 
Multi-Agent systems with the Semantic Web. SEMAS is built on top of the framework [PHIDIAS](https://ceur-ws.org/Vol-2502/paper5.pdf).

![Image 1](images/QuLIO-XR.jpg)

# Installation

---------------

This repository has been tested on Python 3.7.3 64bit (Windows 10/PopOs linux), with the following packages versions:

* [Phidias](https://github.com/corradosantoro/phidias) (release 1.3.4.alpha) 
* [Owlready2](https://pypi.org/project/Owlready2/) (ver. 0.26)


### Phidias

---------------

```sh
> git clone https://github.com/corradosantoro/phidias
> cd phidias
> pip install -r requirements.txt
> pip install .
```


### Owlready2 

---------------

from prompt:
```sh
> pip install owlready2
```

### rdflib 

---------------

from prompt:
```sh
> pip install rdflib
```


### Starting agent

---------------

First of all, you must create the ontology. In order to do that, you must follow three preliminar steps:

* Choose the owl file name, by setting the variable FILE_NAME (within AGENT) in the config.ini (test.owl for instance)
* Execute semas.py

```sh
Creating new test.owl file...

Please Re-Run Semas.

Process finished with exit code 0
```

* Re-execute Semas

```sh
Loading existing test.owl file...

NLP engine initializing. Please wait...

	PHIDIAS Release 1.3.4.alpha (deepcopy-->clone,micropython,py3)
	Autonomous and Robotic Systems Laboratory
	Department of Mathematics and Informatics
	University of Catania, Italy (santoro@dmi.unict.it)
	
eShell: main > 
```

Now Semas is ready.
Unless you delete the owl file or choose to create another ontology, the agent will try to load every time the specified file in confi.ini.

### Ontology Learning

---------------

After having started Semas....

```sh
eShell: main > +FEED("sentence")
```

