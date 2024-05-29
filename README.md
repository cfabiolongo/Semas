# SEMAS

This is the repository of the Python (3.7+) implementation of SEMAS (**SE**mantic **M**ulti-**A**gent **S**ystem), which integrates 
Multi-Agent systems with the Semantic Web. SEMAS is built on top of the framework [PHIDIAS](https://ceur-ws.org/Vol-2502/paper5.pdf).

![Image 1](images/schema.jpg)

# Installation

---------------

This repository has been tested on Python 3.7.3 64bit (Windows 10/PopOs linux), with the following packages versions:

* [PHIDIAS](https://github.com/corradosantoro/phidias) (release 1.3.4.alpha) 
* [Owlready2](https://pypi.org/project/Owlready2/) (ver. 0.26)


### PHIDIAS

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

* Choose the owl file name, by setting the variable FILE_NAME (ONTOLOGY Section) in the config.ini (test.owl for instance)
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

### Ontology initialization

---------------
The current version runs on a toy domain defined in config.ini, which must be initialised as it follows:


```sh
eShell: main > init()
```

## SEMAS agent's **mental attitudes**

---------------
The *mental attitudes* (Beliefs, Desire and Intentions) represent respectively the **information**, **motivational** and **deliberative**
states of the agent. SEMAS aim to integrate distinct models about agent's mental attitudes, in order to leverage all their features, by considering the following schema:


| BDI-Model  | OWL 2      | PHIDIAS    |
|------------|------------|------------|
| Beliefs    | Properties | Beliefs    |
| Desires    | Properties | Procedures |
| Intentions | Properties | Reactors   |

PHIDIAS mental attitudes are built starting from [this](https://cdn.aaai.org/ICMAS/1995/ICMAS95-042.pdf) paper, by considering the following assumptions:

1. We esplicitly represent only beliefs about *current* state of the world.
2. We represent the information about means of achieving certain future world states amd the option available to the agent as *plans*, which can be viewed as a special form of beliefs.
Each plan has a *body* describing the primitive actions os subgoal that have to be achieved for plan execution to be successful. The conditions under which a plan can be chosen as an option
are specified by an *invocation condition* and (possibly) one (or more) *pre-conditions*. The invocation condition specifies the "triggering" event that is necessary for invocation of the plan,
and the pre-conditions specifies the situation thst must hold for the plan to be executable.
3. Each intention tht the system forms by adopting certain plans is represented implicitly using a conventional run-time stack of hierarchically related plans (similar to how Prolog interpreter
handles clauses). Multiple intentions stacks can coexist, either running in parallel, suspended until some conditions occurs, or ordered for execution in some way.

Each plan is invoked within a production rule which follows the sintax: <BR><CENTER>**[TRIGGERING EVENT] / [CONDITIONS] >> [PLAN]**</CENTER>

* **[TRIGGERING EVENT]**: the triggering event can be a **Belief**, a **Reactor** (a special belief which interact with production rule but without residing in the Knowledge base), or a **Procedure**
which is a way for manually trigger a corresponding rule.
* **[CONDITIONS]**: (optional) one or more **Belief**, or **Active Belief** (a special belief which returon *True*/*False* on the basis of Python code)

### OWL Beliefs, Desires, Intentions

---------------

All OWL Semantic mental attitudes are represented by classes, subclasses, individuals and their properties, under the shape of triples. All involved entities ust be specified in config.ini
(which by default they describe a toy domain), in Section [CLASSES] with the variable **Entities**. All individuals under the Section [INDIVIDUALS]. Beliefs, Desires and Intentions are
represented with individuals properties defined in [CLASSES] and grounded as triples with variables having the same name in Section [INDIVIDUALS].

### PHIDIAS correspondence for Beliefs, Desires, Intentions

---------------

As highlighted above in PHIDIAS (thus also in SEMAS) some of typical BDI features are implicitly defined. In order to create a bridge between the two models, by considering the above schema, we employ the following
heuristic:

1. **Knowledge Base**: The Knowledge Base (KB) can be inspected with the following command:
```sh
> kb
```

2. **Beliefs**: Each belief can be asserted in the KB as follows (in this case the belief *SALUTO* contains the string *Hello*), by PHIDIAS shell of inside a production rule:
```sh
> +SALUTO("Hello")
```
Similarly, the belief can be retracted from the KB:
```sh
> -SALUTO("Hello")
```

3. **Desires**: by convention we have chosen to represent Desires with Procedures, which can be used to trigger manually part of the productions rules stack, taking in account (or not)
of one or more arguments.

4. **Intentions**: since in PHIDIAS Intentions are implicitly represented by one or more productions rules, by convention we have chosen to represent them with the PHIDIAS **Reactor**
which does not pass through the knowledge base but can (as like as beliefs) interact with the production rules, thus executed their plan.

5. **Data linking**: all OWL-PHIDIAS linking must be defined in Section [CLASSES] of config.ini.








