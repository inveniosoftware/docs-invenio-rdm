# Preface

The following chapters describe the architecture of InvenioRDM and Invenio
Framework from a high-level point of view. It's meant to describe and expose
the higher-level structure, and help guide how code should be organized.

### How did we arrive to the current architecture?

**The perfect architecture**

The overarching goal of the architecture is similar to any other software
system. We want a software system that's easily maintainable, scalable,
extendable, adaptable, resilient, and *...insert your favorite other buzz words*.

**Reality**

The reality is there's a lot of methodologies and patterns on how to build and architect
software systems. However, in practice, while methodologies are useful
it's often as much about tradeoffs and finding the right balance rather than
strict application of a specific methodology. Most of the time you have to deal
with deadlines, requirements, design patterns, costs, legacy code, people,
projects, prior history and practices.

**Evolving**

InvenioRDM is no different. The architecture is largely a byproduct of our past
experiences and challenges we've faced. The architecture as described here is
not meant to be final answer, but rather an evolving architecture that adapts
and improve over time. You also won't find the answer to all your questions. As
we work with the architecture, we identify shortcomings, missing things and concepts
that could be better defined.

**Past experiences and challenges**

Some of the experiences and challenges we faced:

- **High developer turn-over and many juniors**: Because of the organisational framework and contract policies we've often had a high turn-over of developers and juniors. This means we must focus on good onboarding and great documentation to get developers to a level where they can efficiently contribute and develop high quality software.
- **Spaghetti code**: We have had our share of "data massaging", type conversions and fluffy requirements which all leads to a big ball of mud and interdependency hell.
- **Bad design choices**: We've obviously sometimes made bad design choices and learned from our mistakes.
- **Recovering from failures**: We've had to recover from some spectacular database crashes and file loss incidents on big distributed storage clusters that helped us understand which features were helpful and which features you wish you would've had.

By no means have we solved all of these, and any software project out there is likely facing the same issues.

### Why not X?

InvenioRDM is a monolithic application using something as old as a relational
database system, thus we sometimes get asked questions like why not use microservices, why not serverless
and why not use NoSQL, so here's an attempt to give some vague answers.

First, nothing ever rarely starts from scratch, even when you start a new project
the people and organizations involved bring a long history.

**Microservices**

Microservices themselves are not a substitute for an architecture, it's simply another way of tying different systems together. Part of the complexity at the software level is moved to the infrastructure level, but independently of where components of the system reside they still have to communicate and have clear boundaries. You can do good and bad architectures with both monoliths and microservices (e.g., Google "microservices death star" for some examples.)

**NoSQL**

SQL database have been around for the past 40 years and are often highly reliable systems. Most NoSQL systems on the otherhand have only been around for a much shorter period and do not provide the same reliability. On top of that, InvenioRDM uses a hybrid approach of performing mainly writes of the primary data to the relational database, but keeping a secondary copy indexed in NoSQL system for faster reads.
