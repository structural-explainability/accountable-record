# DECISIONS

<!-- markdownlint-disable MD024 -->

Architectural decisions for the Accountable Record contract.
Records rationale, not vocabulary.

This document records the load-bearing choices that drive the AR
specification. Each decision is numbered, dated, and stated with its
rationale and the alternatives considered. Other AR documents cite
decisions by number.

A decision recorded here is stable. Reversing a decision is a breaking
change to the contract. The document is append-only by convention: new
decisions are added at the bottom, and decision numbers are never
renumbered.

A decision records why a choice was made. It points to the data artifact
that holds the chosen values; it does not recreate that artifact. Where a
vocabulary, pattern, schema, or rule lives in `data/`, the decision cites
it rather than copying it, so the decision cannot drift from its source.

## Amendments to existing decisions

Refining or clarifying a decision is non-breaking and is recorded as an
amendment to that decision's entry, not as a new entry.

---

## AR-D-001: AR uses subject-oriented identity without owning domain ontology

### Date Recorded

2026-05

### Decision

The Accountable Record contract identifies the subject of a record through
AR subject elements, subject-kind declarations, and profile-specific mappings.
AR does not own a universal domain ontology and does not require adopters to
accept a single external kind vocabulary.

Profiles may map their own subject vocabularies, identity regimes, or domain
classifications into AR subject structure. Those mappings are explicit,
machine-readable, and citable.

### Rationale

AR must remain usable across systems that disagree about classification,
authority, domain meaning, and identity interpretation. A subject-oriented
model lets AR preserve what a record is about without requiring AR itself to
own every domain kind vocabulary.

### Consequences

- AR owns subject structure, not domain ontology.
- Profiles may declare and map subject-kind vocabularies.
- External vocabularies are referenced through mappings, not made canonical
  AR vocabulary by default.

---

## AR-D-002: Applicable claims have exactly one outcome from the closed vocabulary

### Date Recorded

2026-05

### Decision

When an applicable claim is run against a bundle, it produces exactly one
outcome from the closed vocabulary defined in the conformance contract
(`data/conformance/outcomes.toml`).

A claim that is not selected, is outside the requested maturity level, or
is not applicable to the bundle is not run and does not receive an
outcome.

### Rationale

Outcomes describe verification results for claims that were actually
examined. A closed vocabulary expresses every verification result without
introducing categories that overlap or require interpretation.

Categories such as `warning`, `skipped`, and `not-applicable` are
deliberately excluded from the outcome vocabulary. Warnings belong in
findings. Claims that are not run are listed separately as `not_run`
metadata, not as outcomes.

### Consequences

- The report schema constrains `outcome` to the vocabulary defined in the
  conformance contract.
- The outcome vocabulary is closed: adding, removing, renaming, or changing
  the meaning of an outcome is a breaking change.
- Report summaries count only claims that were run.
- Maturity levels select which claims are run; claims outside the selected
  level produce no outcome.

---

## AR-D-003: AR core claims use declarative shapes only

### Date Recorded

2026-05

### Decision

Claim definitions use one of the shapes defined in the claims contract.
The AR core uses only declarative shapes. The `custom` shape is reserved
for domain or profile claims that cannot be expressed with the
declarative shapes.

### Rationale

Declarative shapes are sufficient for AR core verification and keep the
core contract inspectable: an AR claim can be understood from its declared
shape, fields, and rules without reading verifier code.

The `custom` shape remains necessary for domain profiles, since some
domain-specific checks cannot be reduced cleanly to declarative
predicates. Keeping `custom` out of the AR core preserves analyzability
without preventing profiles from expressing domain-specific verification.

### Consequences

- AR core claim definitions use only declarative shapes.
- Domain profiles may use `custom` claims when declarative shapes are
  insufficient.
- Implementations must support `custom` for profiles but must not require
  it for AR core claims.

---

## AR-D-004: Namespace authorities own their project spaces

### Date Recorded

2026-05

### Decision

Identifier ownership is governed by namespace authority and project space.
Each authority owns the identifiers it publishes within its project spaces.
AR owns identifiers in the `structural-explainability.org/accountable-record`
project space. Domain systems, proprietary systems, and external publishers own
their own project spaces.

### Rationale

Identifier ownership determines who may publish, deprecate, supersede, or
withdraw an identifier and which change contract governs that action.

### Consequences

- AR identifiers are governed by the AR change contract.
- Domain and external identifiers are governed by their owning authorities.
- AR may reference external identifiers through mappings without owning them.

---

## AR-D-005: AR conformance is incremental

### Date Recorded

2026-05

### Decision

AR conformance is incremental. Bundles may declare a target maturity
level; the verifier reports the achieved level. Levels are nested: a
bundle achieves a level only if it satisfies that level's mandatory claims
and the mandatory claims of all lower levels.

### Rationale

Real systems often cannot move from no AR contract to full domain-profile
conformance in one step. Incremental levels let systems adopt AR in
stable, verifiable stages. A level represents a meaningful conformance
milestone, not an arbitrary group of claims.

### Alternatives Considered

- **Require full conformance only.** Rejected. Prevents incremental adoption
  and makes AR less useful during migration.
- **Per-claim opt-in only.** Rejected. Too granular for producers and
  consumers to compare across systems.

### Consequences

- Bundles may declare a target level.
- Reports include the achieved level.
- Changing the level structure requires updating the maturity-levels
  definition and any affected claim assignments.

---

## AR-D-006: AR exports bundles, profiles, and reports

### Date Recorded

2026-05

### Decision

The AR contract defines its exported artifact types in the export
contract: producers export bundles, profiles define claim sets, and
verifiers export reports.
Element, claim, trait, and package schemas define reusable contract structure;
they are not separate verifier input or output artifact types.

Storage formats, query interfaces, authentication, authorization, access
control, and cryptographic attestation are outside the AR contract.

### Rationale

This artifact set is sufficient to express the contract boundary. Keeping
storage, transport, access control, and attestation out of scope preserves
AR's neutrality across implementations and operational systems.

### Alternatives Considered

- **Add a live-query artifact.** Rejected. Query interfaces belong to
  operational systems, not to the AR export contract.
- **Inline profiles into bundles.** Rejected. Profiles are shared contract
  artifacts and remain independently citable.

### Consequences

- Verifier implementations consume bundles and profiles and emit reports.
- Operational systems may provide storage, query, access-control, or
  attestation features, but AR does not require them.

---

## AR-D-007: The specification is generated from data

### Date Recorded

2026-05

### Decision

The durable content of the AR specification lives in machine-readable TOML
and JSON artifacts under `data/`. Human-readable specification pages are
generated from those artifacts under `docs/en/`. The data artifacts are
authoritative; the generated pages are not.

### Rationale

A single machine-readable source keeps the specification internally
consistent and lets tooling validate, resolve, and render the contract
without parsing prose. Prose pages serve readers; they do not define the
contract.

### Consequences

- `data/` artifacts are the source of truth.
- `docs/en/` pages are generated and must not be edited as if
  authoritative.
- A change to the contract is a change to `data/`, not to the prose.

---

## AR-D-008: TOML is authored source and JSON is interchange/export/canonicalization target

### Date Recorded

2026-05

### Decision

AR uses TOML for human-authored source declarations and JSON for schemas,
examples, generated interchange artifacts, lock files, and canonical exports.

TOML source files are optimized for maintainers: they may contain comments,
human-oriented ordering, explanatory grouping, and formatting choices that do
not affect contract meaning.

JSON artifacts are optimized for tooling: they are used for schemas,
validator fixtures, exported records, generated registries, package locks,
and canonical generated forms used for digest computation.

When an AR package, element, schema, or export requires a digest, the digest
is computed from canonical generated JSON, not from the authored TOML source.

### Rationale

TOML is easier to author, review, and maintain for source declarations. JSON is
better for interchange, validation, canonicalization, and downstream toolchains.

Separating authored source from canonical export prevents non-semantic source
edits from changing package identity. A comment edit, formatting change, or
source key reordering should not invalidate downstream lock files.

This distinction also lets Python, Rust, docs, catalogs, validators, and
external systems consume the same normalized JSON exports without treating a
particular implementation language as the specification.

### Alternatives Considered

- **Use JSON for all source files.** Rejected. JSON is poor for authored
  specification work because it has no comments and is less suitable for
  rationale-bearing declarations.

- **Use TOML for interchange and digests.** Rejected. TOML does not provide a
  single canonical byte representation suitable for reproducible cross-tool
  digest computation.

- **Let implementation models define the canonical form.** Rejected. AR data
  artifacts define the contract; implementation models consume and validate
  them.

### Consequences

- Authored source declarations live primarily in TOML.
- JSON schemas, examples, generated exports, lock files, and canonical package
  exports are JSON.
- Digest computation uses canonical generated JSON.
- Non-semantic TOML edits do not change package identity.
- Generated JSON exports must be reproducible from the authored source.

---

## AR-D-009: The contract is expressed as verifiable elements

### Date Recorded

2026-05

### Decision

Claims, traits, verification semantics, maturity levels, identifiers,
export contracts, and conformance checks are represented as verifiable
elements and supporting data artifacts under `data/`, not as separate
prose source files.

### Rationale

Representing each concern as a verifiable element makes it independently
checkable, independently versionable, and composable into packages. The
contract becomes inspectable by tooling rather than only by readers.

### Consequences

- Each concern has a data representation under its component group.
- Prose documents explain elements; they do not define them.

---

## AR-D-010: AR preserves disagreement structure without resolving disagreement

### Date Recorded

2026-05

### Decision

AR preserves the identifiers, claims, traits, sources, references,
relations, provenance, verification, conformance, and status needed for
disagreement to remain inspectable. AR does not decide truth, correctness,
authority, legitimacy, obligation, enforcement, or domain meaning.

### Rationale

AR's neutrality is the property that lets parties who disagree still share
a record. The moment AR adjudicates, it stops being a neutral substrate and
becomes a party to the disagreement. Preserving structure without resolving
it is the boundary that keeps AR adoptable across adversarial parties.

### Consequences

- Verifiers report whether claims hold, not whether positions are correct.
- Domain meaning, authority, and enforcement live in domain profiles and
  operational systems, not in AR.

---

## AR-D-011: Component groups, verifiable elements, and element packages are distinct

### Date Recorded

2026-05

### Decision

AR separates three concepts:

- **component groups** organize related verifiable element types;
- **verifiable element types** define independently checkable record
  building blocks;
- **element packages** distribute one or more element types with their
  schemas, checks, examples, mappings, verifier expectations, and
  compatibility fixtures.

Profiles compose element packages or selected element types. Domain systems
such as JR and CIR may define their own element packages while depending on
AR core element packages.

### Rationale

Separating the unit of organization (group), the unit of verification
(element type), and the unit of distribution (package) lets each vary
independently. An element type can move between packages without changing
its identity; a package can evolve without redefining its element types.

### Consequences

- Element types are the unit of verification and identity.
- Packages are the unit of distribution and versioned dependency.
- Profiles compose at the package or element-type level.

---

## AR-D-012: Identifiers are authority-based

### Date Recorded

2026-05

### Decision

A verifiable element type is identified by a namespace authority, project
space, component group, and local element name. The identity contract
(`data/contracts/identity-contract.toml`) defines the canonical URI form, the
persistent-ID form, and the compact-ID form, along with the rule that none of
these forms includes a version.

Hosting metadata is recorded separately and is not part of identity. Domain
systems such as JR and CIR define their own project spaces and element types
while depending on AR core identifiers. Deprecated identifiers remain citable
and must not be reused.

### Rationale

Authority-based identifiers make provenance legible and let each authority
govern its own names. Excluding version from the identifier is what allows
a released identifier to remain stable across versions; version attaches
only through a versioned reference, also defined in the identity contract.

### Consequences

- Released identifiers are stable and are never renamed or repurposed.
- Versioning attaches through versioned references, not through the
  identifier.
- Hosting may change without changing identity.

---

## AR-D-013: Claims are verifier checks

### Date Recorded

2026-05

### Decision

AR treats claims as verifier checks with stable identifiers, declared
shapes, outcome semantics, applicability rules, and maturity or profile
assignments. Claim-related element types live under the claims component
group, and element packages compose claim sets together with traits, field
mappings, verifier expectations, fixtures, expected reports, and rationale.

Profiles may adopt AR claims by reference. Domain profiles may add their own
claims, but they do not redefine AR claim identifiers or outcome semantics.

### Rationale

Treating a claim as a check with a stable identity and declared shape keeps
verification inspectable and composable. Composing claims through packages
rather than embedding them in larger units lets claim sets be shared,
versioned, and reused across profiles.

### Consequences

- A claim is identified, shaped, and checkable on its own.
- Claim sets are distributed through packages.
- Domain profiles extend the claim set without altering AR claim semantics.

---

## AR-D-014: Package resolution uses pinned versions, canonical JSON digests, and hard-fail conflicts

### Date Recorded

2026-05

### Decision

AR packages are designed for cross-project composition. Authoring may use
compatible version ranges, but validation uses a resolved lock file with
exact versions and digests.

Package and element digests are computed over canonical generated JSON
exports, not authored TOML source. TOML is the human-authored format;
comments, formatting, and ordering are not part of package identity. The
authoritative digest is computed by the publisher at release and travels
with the package; resolution verifies it rather than originating it. The
digest target and canonicalization rules are defined in the package
contract (`data/contracts/package-contract.toml`).

Verifiable element identity is package-independent. Element packages
include element types by reference. Moving an element type between packages
is a package composition change, not an element rename.

A package's version reflects the most severe change among its manifest and
all included element exports; a breaking change in any included element is
a breaking change to the package.

### Rationale

Pinned versions with digests make a resolved graph reproducible and
verifiable across independently published authorities. Digesting the
canonical export rather than the source means non-semantic edits to the
authored TOML do not perturb identity, while adding an optional field stays
digest-neutral for content that does not set it, keeping additive changes
genuinely non-breaking.

### Consequences

- Authoring uses ranges; validation uses an exact, digested lock file.
- A package's version always corresponds to its current canonical export
  and digest.
- An element type can be repackaged without a rename, with membership
  resolved through the catalog.

---

## AR-D-015: Composite-claim outcomes resolve failure-first

### Date Recorded

2026-05

### Decision

A claim with multiple verifiable requirements resolves to a single outcome
from its per-requirement outcomes, failure-first: a determinate negative
result is never masked by missing evidence. The full precedence is defined
in the conformance contract's composite-claim rollup
(`data/conformance/outcomes.toml`).

### Rationale

For an accountability substrate, a known failure being hidden by an
unverifiable requirement is worse than the reverse: a `cannot-verify`
invites someone to supply the missing evidence, while a masked `fail`
invites nothing. Failure-first keeps confirmed problems visible.

This is a domain-keyed choice, not a universal one. A system whose purpose
is certification rather than accountability could justifiably resolve
missing-evidence-first. The conformance severity order is aligned with this
precedence; changing one without the other is a contract error.

### Alternatives Considered

- **Missing-evidence-first.** Rejected for AR. It would allow an
  unverifiable requirement to suppress a confirmed failure, defeating the
  substrate's purpose.

### Consequences

- Level achievement evaluates composite claims by this rule before
  checking whether a level is met.
- A confirmed failure always surfaces, regardless of unverifiable
  sibling requirements.

---

## AR-D-016: One major version per identity per resolved graph

### Date Recorded

2026-05

### Decision

A resolved dependency graph may contain only one major version for a given
package or element identity. If declared version ranges do not intersect,
resolution hard-fails. AR does not silently choose a version, override a
constraint, or admit multiple incompatible major versions of the same
identity in one graph.

### Rationale

Allowing two majors of the same identity to coexist would require
major-version-qualified identifiers, which contradicts AR-D-012: a released
identifier cannot both be stable and carry its major version. For a
substrate whose value is durable identity, stable identifiers win.

The cost is that AR major bumps are expensive for the whole ecosystem,
since consumers must converge on one major before validation. For a
substrate intended to outlive its consumers, that cost is appropriate: it
makes breaking the substrate suitably hard, which is what keeps it stable.

### Alternatives Considered

- **Allow coexisting majors.** Rejected. Forces version into the
  identifier and breaks identifier stability.
- **Silent newest-wins resolution.** Rejected. Hides incompatibility that
  the consumer needs to resolve deliberately.

### Consequences

- Incompatible major requirements must be reconciled by the consumer before
  validation, not papered over by the resolver.

---

<!-- markdownlint-enable MD024 -->
