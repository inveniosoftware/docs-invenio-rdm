# Development process

The following page is an attempt to articulate the development process for
InvenioRDM. The application of this development process is meant to be
pragmatic - if something does not make sense don't do it. It's here more as
a checklist and collection of prior experience.

### Code of conduct

!!! warning "Don't skip!"

We expect every community member to adhere to our
[code of conduct](../contribute/code-of-conduct.md), and we thus expect
that you have read it! Overall, the code of conduct says that we're:

- Open
- Inclusive
- Considerate
- Respectful

You're part of a global diverse community where people have a wide variety of
backgrounds and a lot of our communication is text-based. This creates a lot of
room for misinterpretation for both senders and receivers of messages (the
text/words used only account for about 10% of a message, the nonverbal and
paraverbal part of message accounts for the remaining 90% of a message).

!!! tip "Communication tips"

    - Always assume best intentions of your counterpart both as sender and receiver.
    - Always use video meetings instead of text, if you feel a conflict is starting
      to develop (lowering the risk of misinterpretation).
    - Ask for help early to mediate from the senior leadership (conflicts only gets
      worse if left unaddressed).
    - Provide and receive feedback: Feedback is like a gift. You give it with best
      intentions to help another person. When you receive it, you say thank you and
      it's fully up to you what you do with that gift afterwards.



### Principles

The core foundational principles on which we build InvenioRDM is that we want

- an excellent user experience
- high scalability

These are the two principles that made the community come together in the first
place and kick-off the development of InvenioRDM.

Putting these two principles at the core of our development means among other
things that:

- We must make tough choices on which features to add or what not - building everything does not make for a good user experience.
- We should spend the time and dedication needed for creating mockups, talking to users
  and testing our assumptions.
- We must consider performance - an excellent UX is not enough if it does not scale.

### Vision

The vision of InvenioRDM is to build the repository world's "GitHub/GitLab" alike platform. We understand this as:

- **Empower users to self-organize** - Users must be empowered to get their job done without the platform or administrators getting in their way.
- **Provide a simple and powerful user experience** - Simple features can be very powerful and can accommodate a large number of use cases. Being able to do everything, often results in users not being able to do anything.
- **Distribute curation** - The repository platform should empower people with the skills and knowledge to curate the content, as our platforms starts accepting larger and larger quantities of content.
- **Enabling conversations** - A key part of the GitHub/GitLab like platforms is that they enable a conversations.

### Design: Mockups, RFCs and UX

The most important about developing new features is to start communicating about
them early.

- Discuss with colleagues, ask on the chat, perhaps someone else has similar requirements or is already working on it.
- Identify users and feedback - understand their needs and worries (this later helps us validate if what we do makes sense).
- Design mockups in Balsamiq.
- Share and present in the bi-weekly InvenioRDM telecons to collect feedback.
- Collaboratively write RFCs - this helps articulate names, think through possible problems and keep a log of why certain decisions were taken.
- Match a coherent UX (e.g. know why you place a button a specific place, what's the text etc.)

### Development

Before starting development, make sure that you've collected feedback, that there's consensus on what and how to build it. The goal is to avoid large changes later on in the development.

**Checklist**

A working feature is only half of the work, remember also:

- Tests: performance, quality assurance, integration testing.
- Translations
- Accessibility
- Documentation (end-user, system administrators, developers).
- Migration/upgrade scripts
