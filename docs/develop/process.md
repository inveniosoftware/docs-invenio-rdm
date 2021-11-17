# Development process

The following page is an attempt to articulate the development process for
InvenioRDM. The application of this development process is meant to be
pragmatic - if something does not make sense don't do it. It's here more as
a checklist and collection of prior experience.

### Principles

The core foundational principles on which we build InvenioRDM is that we want

- an excellent user experience
- high scalability

These are the two principles that made the community come together in the first
place and kick-off the development of InvenioRDM.

Putting these two principles are the core of our development means among other
things that:

- We must make tough choices on which features to add or what not - building everything does not make for a good user experience.
- We should spend the time and dedication needed for creating mockups, talking to users
  and testing our assumptions.
- We must consider performance - an excellent UX is not enough if it does not scale.

### Design: Mockups, RFCs and UX

The most important about developing new features is to start communicating about
them early.

- Discuss with colleagues, ask on the chat, perhaps someone else has similar requirements or is already working on it.
- Identify users and feedback - understand their needs and worries (this later helps us validate if what we do makes sense).
- Design mockups in Balsamiq.
- Share and present in the bi-weekly InvenioRDM telecons to collect feedback.
- Collaboratively write RFCs - this helps articulate names, think through possible problems and keep a log of why certain decisions were taken.
- Match a coherent UX (e.g. know why you place a button a specific place, what's the text etc)

### Development

Before starting development, make sure that you've collected feedback, that there's consensus on what and how to build it. The goal is to avoid large changes late on in the development.

**Checklist**

The a working feature is only half of the work, remember also:

- Tests: performance, quality assurance, integration testing.
- Documentation (end-user, system administrators, developers).
- Migration/upgrade scripts
