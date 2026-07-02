# Platform-Core Engineering Laws

Version: 1.0.0

Status: Official

---

# Introduction

These Engineering Laws are the permanent engineering principles that govern Platform-Core.

Every source file, module, builder, engine, service and contributor must comply with these laws.

---

# Law 1 — Knowledge Before Code

No code shall be written before its purpose, architecture and specification are documented.

---

# Law 2 — Architecture Before Implementation

Every implementation must follow an approved architecture.

No implementation may redefine the architecture.

---

# Law 3 — Contract Before Communication

All communication between components must occur through documented contracts.

Direct coupling is prohibited.

---

# Law 4 — Security By Design

Security is designed from the beginning.

It is never added later.

---

# Law 5 — Documentation Is Mandatory

Every component must include documentation.

Undocumented components are considered incomplete.

---

# Law 6 — Tests Are Mandatory

Every component must contain automated tests.

Untested components cannot enter production.

---

# Law 7 — Everything Has Identity

Every asset shall possess:

* Unique Identifier
* Version
* Owner
* Manifest
* Lifecycle

---

# Law 8 — Everything Is Versioned

No asset exists without version control.

---

# Law 9 — Everything Is Replaceable

No component may become irreplaceable.

Every dependency must have an exit strategy.

---

# Law 10 — Small Core

The Kernel shall remain minimal.

Optional functionality belongs to extensions.

---

# Law 11 — Automation Before Repetition

If a task is repeated more than once, evaluate automation.

---

# Law 12 — Measure Everything

Every engineering decision must be measurable.

---

# Law 13 — Evidence Before Opinion

Engineering decisions require evidence.

Opinions alone are insufficient.

---

# Law 14 — Simplicity Wins

When two solutions satisfy the same requirements, choose the simpler one.

---

# Law 15 — Backward Compatibility

Breaking compatibility requires formal approval.

---

# Law 16 — Human Oversight

Critical decisions always require human approval.

---

# Law 17 — Knowledge Never Dies

Knowledge shall never be deleted.

Deprecated knowledge is archived.

---

# Law 18 — Open Standards First

Open standards are preferred whenever practical.

---

# Law 19 — Continuous Improvement

Every release must improve at least one measurable aspect of the platform.

---

# Law 20 — Leave It Better

Every contribution should improve Platform-Core beyond its previous state.
