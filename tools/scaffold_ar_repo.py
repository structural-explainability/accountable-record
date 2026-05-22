"""Scaffold an Accountable Record repository with initial files and directories."""

import json
from pathlib import Path

ROOT = Path.cwd()

CLAIM_OUTCOMES = [
    {
        "id": "pass",
        "label": "Pass",
        "description": "The required evidence is present and the claim is satisfied.",
        "is_pass": True,
        "is_failure": False,
        "evidence_sufficient": True,
        "blocks_mandatory_level": False,
    },
    {
        "id": "fail",
        "label": "Fail",
        "description": "The required evidence is present and the claim is not satisfied.",
        "is_pass": False,
        "is_failure": True,
        "evidence_sufficient": True,
        "blocks_mandatory_level": True,
    },
    {
        "id": "partial",
        "label": "Partial",
        "description": "The claim has multiple verifiable requirements; at least one is satisfied, at least one fails, and required evidence for checked requirements is present.",
        "is_pass": False,
        "is_failure": False,
        "evidence_sufficient": True,
        "blocks_mandatory_level": True,
    },
    {
        "id": "cannot-verify",
        "label": "Cannot Verify",
        "description": "The claim applies, but required evidence is missing.",
        "is_pass": False,
        "is_failure": False,
        "evidence_sufficient": False,  # the one outcome where evidence was absent
        "blocks_mandatory_level": True,
    },
]


NOT_RUN_REASONS = [
    "outside-selected-adoption-level",
    "outside-selected-profile",
    "optional-and-not-selected",
    "preconditions-absent",
    "not-applicable-to-bundle",
]


SUMMARY_SEVERITY_ORDER = [
    "fail",
    "partial",
    "cannot-verify",
    "pass",
]

# The closed vocabulary IS the set of outcome ids. Derived, not duplicated.
DEFINED_OUTCOMES = [outcome["id"] for outcome in CLAIM_OUTCOMES]

COMPONENT_GROUPS = [
    "identity",
    "subjects",
    "claims",
    "traits",
    "sources",
    "references",
    "relations",
    "provenance",
    "verification",
    "status",
    "disagreement",
    "conformance",
    "maturity",
    "mappings",
    "exports",
    "governance",
    "transformations",
    "failure-modes",
]


ELEMENTS_BY_GROUP = {
    "identity": [
        "identifier",
        "namespace",
        "version",
    ],
    "subjects": [
        "record-subject",
        "subject-kind",
        "subject-scope",
        "subject-classification",
        "subject-kind-declaration",
        "subject-kind-mapping",
        "record-type-subject-binding",
    ],
    "transformations": [
        "transformation",
        "transformation-kind",
        "transformation-behavior",
        "transformation-declaration",
        "transformation-admissibility",
        "transformation-lineage",
        "transformation-evidence",
        "transformation-profile-rule",
    ],
    "failure-modes": [
        "failure-mode",
        "structural-collapse",
        "collapse-pattern",
        "collapse-detection",
        "collapse-remediation",
        "profile-failure-mode",
    ],
    "claims": [
        "claim",
        "claim-kind",
        "claim-status",
        "claim-attachment",
        "claim-shape",
    ],
    "traits": [
        "trait",
        "trait-kind",
        "trait-value",
        "trait-declaration",
        "trait-requirement",
        "trait-conformance-binding",
        "trait-claim-binding",
    ],
    "sources": [
        "source",
        "source-kind",
        "source-role",
        "authority-source",
        "evidence-source",
        "normative-source",
    ],
    "references": [
        "source-reference",
        "citation",
        "locator",
        "source-span",
        "uri-reference",
        "hash-reference",
    ],
    "relations": [
        "relation",
        "relation-kind",
        "support",
        "contradiction",
        "dependency",
        "derivation",
        "satisfaction",
        "equivalence",
        "mapping-relation",
    ],
    "provenance": [
        "provenance-event",
        "generation-event",
        "derivation-event",
        "revision-event",
        "custody-event",
        "publication-event",
        "creator",
        "contributor",
        "tool-used",
    ],
    "verification": [
        "verifier",
        "verifier-identity",
        "verifier-operation",
        "verifier-error",
        "verifier-expectation",
        "verification-event",
        "verification-method",
        "evidence",
        "finding",
        "check",
        "review",
        "reviewer",
        "result",
        "sub-result",
        "confidence",
        "reproducibility",
        "report-production",
    ],
    "status": [
        "lifecycle-status",
        "review-status",
        "publication-status",
        "validity-status",
        "dispute-status",
        "deprecation-status",
    ],
    "disagreement": [
        "dispute",
        "objection",
        "alternative-claim",
        "interpretation",
        "contested-claim",
        "contested-relation",
        "resolution-status",
    ],
    "conformance": [
        "requirement",
        "rule",
        "conformance-check",
        "conformance-profile",
        "conformance-outcome",
        "claim-outcome",
        "not-run-metadata",
        "claim-selection",
        "conformance-declaration",
        "structural-non-conformance",
        "conformance-report",
        "expected-report",
        "compatibility-fixture",
    ],
    "maturity": [
        "maturity-level",
        "level-requirement",
        "level-check",
        "maturity-assessment",
        "progression-path",
    ],
    "mappings": [
        "external-standard",
        "mapping-guide",
        "mapping-question",
        "mapping-answer",
        "mapping-rule",
        "candidate-target",
        "mapping-warning",
        "mapping-example",
        "field-role",
        "field-mapping",
    ],
    "exports": [
        "export-artifact",
        "export-index",
        "export-bundle",
        "export-profile",
        "export-report",
        "export-envelope",
        "export-schema",
        "export-extension",
        "forbidden-extension",
        "release-contract",
        "compatibility-manifest",
        "lock-file",
    ],
    "governance": [
        "steward",
        "change-policy",
        "compatibility-policy",
        "deprecation-policy",
        "adoption-policy",
        "decision-record",
    ],
}


EXPORT_ARTIFACT_TYPES = [
    {
        "id": "bundle",
        "label": "Bundle",
        "schema": "accountable-record-bundle-1",
        "description": "What a conforming system exports for inspection.",
    },
    {
        "id": "profile",
        "label": "Profile",
        "schema": "accountable-record-profile-1",
        "description": "What a domain specification exports for verification composition.",
    },
    {
        "id": "report",
        "label": "Report",
        "schema": "accountable-record-report-1",
        "description": "What a verifier exports after checking a bundle.",
    },
]


EXPORT_OPERATIONS = [
    {
        "id": "inspect",
        "label": "Inspect",
        "produces_ar_report": False,
        "description": "Reads a bundle and summarizes declared conformance and structure.",
    },
    {
        "id": "validate",
        "label": "Validate",
        "produces_ar_report": True,
        "description": "Reads a bundle and profile, runs applicable claims, and emits a report.",
    },
    {
        "id": "compare",
        "label": "Compare",
        "produces_ar_report": False,
        "description": "Reads two bundles, profiles, or reports and produces an implementation-defined diff.",
    },
]


FAILURE_MODE_PATTERNS = [
    {
        "id": "source-vs-interpretation",
        "label": "Source vs. Interpretation",
        "collapse": "A record fuses source material with an interpretation of what the source means.",
    },
    {
        "id": "name-vs-identity",
        "label": "Name vs. Identity",
        "collapse": "A record ties identity to a name, title, address, designation, or other mutable label.",
    },
    {
        "id": "content-vs-status",
        "label": "Content vs. Status",
        "collapse": "A record mutates content to encode current status.",
    },
    {
        "id": "event-vs-record",
        "label": "Event vs. Record",
        "collapse": "A record treats a representation of an event as the event itself.",
    },
    {
        "id": "provenance-vs-authority",
        "label": "Provenance vs. Authority",
        "collapse": "A record treats provenance as conferring authority.",
    },
    {
        "id": "context-vs-claim",
        "label": "Context vs. Claim",
        "collapse": "A record folds contextual limits into the claim itself.",
    },
]

PACKAGES = {
    "core": {
        "label": "AR Core",
        "description": "Core Accountable Record element package.",
        "elements": [
            "se.accountable-record.identity.identifier",
            "se.accountable-record.subjects.record-subject",
            "se.accountable-record.claims.claim",
            "se.accountable-record.conformance.claim-outcome",
            "se.accountable-record.conformance.not-run-metadata",
            "se.accountable-record.conformance.claim-selection",
            "se.accountable-record.conformance.conformance-declaration",
            "se.accountable-record.conformance.structural-non-conformance",
            "se.accountable-record.traits.trait",
            "se.accountable-record.sources.source",
            "se.accountable-record.references.source-reference",
            "se.accountable-record.relations.relation",
            "se.accountable-record.provenance.provenance-event",
            "se.accountable-record.verification.verification-event",
            "se.accountable-record.conformance.conformance-check",
            "se.accountable-record.maturity.maturity-level",
            "se.accountable-record.traits.trait-declaration",
            "se.accountable-record.traits.trait-requirement",
            "se.accountable-record.traits.trait-conformance-binding",
            "se.accountable-record.verification.verifier",
            "se.accountable-record.verification.result",
            "se.accountable-record.verification.evidence",
            "se.accountable-record.exports.export-bundle",
            "se.accountable-record.exports.export-profile",
            "se.accountable-record.exports.export-report",
            "se.accountable-record.exports.export-envelope",
            "se.accountable-record.exports.export-schema",
            "se.accountable-record.subjects.record-subject",
            "se.accountable-record.subjects.subject-kind",
            "se.accountable-record.subjects.subject-scope",
            "se.accountable-record.subjects.subject-kind-declaration",
            "se.accountable-record.subjects.record-type-subject-binding",
            "se.accountable-record.transformations.transformation",
            "se.accountable-record.transformations.transformation-kind",
            "se.accountable-record.transformations.transformation-behavior",
            "se.accountable-record.transformations.transformation-declaration",
            "se.accountable-record.transformations.transformation-admissibility",
            "se.accountable-record.transformations.transformation-lineage",
            "se.accountable-record.failure-modes.failure-mode",
            "se.accountable-record.failure-modes.structural-collapse",
            "se.accountable-record.failure-modes.collapse-pattern",
            "se.accountable-record.failure-modes.collapse-detection",
            "se.accountable-record.failure-modes.collapse-remediation",
        ],
    },
    "source-traceability": {
        "label": "Source Traceability",
        "description": "Element package for source, reference, provenance, and traceability structures.",
        "elements": [
            "se.accountable-record.sources.source",
            "se.accountable-record.sources.source-kind",
            "se.accountable-record.sources.source-role",
            "se.accountable-record.references.source-reference",
            "se.accountable-record.references.citation",
            "se.accountable-record.references.locator",
            "se.accountable-record.references.source-span",
            "se.accountable-record.references.uri-reference",
            "se.accountable-record.references.hash-reference",
            "se.accountable-record.provenance.provenance-event",
            "se.accountable-record.provenance.derivation-event",
            "se.accountable-record.provenance.revision-event",
            "se.accountable-record.provenance.custody-event",
        ],
    },
    "verification-core": {
        "label": "Verification Core",
        "description": "Element package for verifier-facing checks, results, evidence, reports, and expectations.",
        "elements": [
            "se.accountable-record.verification.verification-event",
            "se.accountable-record.verification.verification-method",
            "se.accountable-record.verification.evidence",
            "se.accountable-record.verification.check",
            "se.accountable-record.verification.review",
            "se.accountable-record.verification.reviewer",
            "se.accountable-record.verification.result",
            "se.accountable-record.verification.confidence",
            "se.accountable-record.verification.reproducibility",
            "se.accountable-record.verification.verifier-expectation",
            "se.accountable-record.conformance.conformance-check",
            "se.accountable-record.conformance.conformance-outcome",
            "se.accountable-record.conformance.conformance-report",
            "se.accountable-record.conformance.expected-report",
            "se.accountable-record.conformance.claim-outcome",
            "se.accountable-record.conformance.not-run-metadata",
            "se.accountable-record.conformance.claim-selection",
            "se.accountable-record.conformance.conformance-declaration",
            "se.accountable-record.conformance.structural-non-conformance",
            "se.accountable-record.conformance.compatibility-fixture",
            "se.accountable-record.traits.trait-conformance-binding",
            "se.accountable-record.verification.verifier",
            "se.accountable-record.verification.verifier-identity",
            "se.accountable-record.verification.verifier-operation",
            "se.accountable-record.verification.verifier-error",
            "se.accountable-record.verification.finding",
            "se.accountable-record.verification.sub-result",
            "se.accountable-record.verification.report-production",
            "se.accountable-record.exports.export-report",
            "se.accountable-record.transformations.transformation-evidence",
            "se.accountable-record.transformations.transformation-profile-rule",
            "se.accountable-record.failure-modes.collapse-detection",
            "se.accountable-record.failure-modes.profile-failure-mode",
        ],
    },
}

ROOT_FILES = {
    "README.md": "# Accountable Record\n\nAccountable Records is a data-first specification for composing records from verifiable elements.\n",
    "DECISIONS.md": "# Decisions\n\n## Decision: Data-first verifiable element architecture\n\nAccountable Records is a data-first specification. An Accountable Record is composed of verifiable elements.\n",
    "AGENTS.md": "# Agents\n\nFollow the repository source-of-truth boundaries. Data files define the specification. Generated files must not be hand edited.\n",
    "AGENT_CONDUCT.md": "# Agent Conduct\n\nPreserve rationale-bearing comments and source-of-truth boundaries.\n",
    "CLAUDE.md": "# Claude\n\nRead README.md, DECISIONS.md, AGENTS.md, and MANIFEST.toml before making changes.\n",
}


SCHEMA_FILES = [
    "ar-term.schema.json",
    "ar-namespace-authority.schema.json",
    "ar-component-group.schema.json",
    "ar-element-type.schema.json",
    "ar-element-instance.schema.json",
    "ar-element-check.schema.json",
    "ar-element-catalog-entry.schema.json",
    "ar-element-lock.schema.json",
    "ar-element-package.schema.json",
    "ar-element-package-index.schema.json",
    "ar-mapping-guide.schema.json",
    "ar-record.schema.json",
    "ar-export-index.schema.json",
    "ar-claim-shape.schema.json",
    "ar-core-claim-set.schema.json",
    "ar-trait-library.schema.json",
    "ar-trait-library-index.schema.json",
    "ar-trait-declarations.schema.json",
    "ar-conformance-index.schema.json",
    "ar-conformance-outcomes.schema.json",
    "ar-claim-selection.schema.json",
    "ar-achieved-level-semantics.schema.json",
    "ar-conformance-report-semantics.schema.json",
    "ar-verifier-errors.schema.json",
    "ar-conformance-compatibility.schema.json",
    "ar-verification-index.schema.json",
    "ar-verifier-contract.schema.json",
    "ar-verifier-operations.schema.json",
    "ar-evidence-semantics.schema.json",
    "ar-verification-aggregation.schema.json",
    "ar-verifier-identity.schema.json",
    "ar-export-contract-index.schema.json",
    "ar-export-artifact-types.schema.json",
    "ar-bundle-envelope.schema.json",
    "ar-profile-envelope.schema.json",
    "ar-report-envelope.schema.json",
    "ar-export-schemas.schema.json",
    "ar-export-extensions.schema.json",
    "ar-export-operations.schema.json",
    "ar-identity-contract.schema.json",
    "ar-package-contract.schema.json",
    "ar-change-contract.schema.json",
    "ar-subject-mapping-index.schema.json",
    "ar-subject-mapping-guide.schema.json",
    "ar-subject-kind-map.schema.json",
    "ar-subject-mapping-questions.schema.json",
    "ar-transformations-index.schema.json",
    "ar-transformation-behaviors.schema.json",
    "ar-transformation-declarations.schema.json",
    "ar-transformation-admissibility.schema.json",
    "ar-transformation-lineage.schema.json",
    "ar-transformation-profile-responsibilities.schema.json",
    "ar-failure-modes-index.schema.json",
    "ar-failure-mode-patterns.schema.json",
    "ar-failure-mode-detection.schema.json",
    "ar-failure-mode-remediation.schema.json",
    "ar-profile-failure-mode-additions.schema.json",
    "ar-governance-index.schema.json",
    "ar-scope.schema.json",
    "ar-governance-boundaries.schema.json",
    "ar-non-goals.schema.json",
    "ar-adoption-index.schema.json",
    "ar-when-to-use-ar.schema.json",
    "ar-readiness-questions.schema.json",
    "ar-adoption-maturity-path.schema.json",
]

SUBJECT_MAPPING_SYSTEMS = [
    {
        "id": "identity-regimes",
        "label": "Identity Regimes",
        "description": "Mapping support for identity-regime vocabularies used by profiles.",
    },
    {
        "id": "accountable-entities",
        "label": "Accountable Entities",
        "description": "Mapping support for accountable-entity vocabularies used by profiles.",
    },
]


SUBJECT_MAPPING_GUIDES = [
    {
        "id": "identity-regimes",
        "label": "Identity Regimes Subject Mapping",
        "path": "data/subject-mappings/identity-regimes/mapping-guide.toml",
    },
    {
        "id": "accountable-entities",
        "label": "Accountable Entities Subject Mapping",
        "path": "data/subject-mappings/accountable-entities/mapping-guide.toml",
    },
]

TRAIT_LIBRARY = [
    {
        "legacy_id": "AR.TRAIT.SOURCE_TRACEABLE",
        "compact_id": "se.accountable-record.traits.source-traceable",
        "label": "Source Traceable",
        "applies_to": ["all"],
    },
    {
        "legacy_id": "AR.TRAIT.PROVENANCE_TRACEABLE",
        "compact_id": "se.accountable-record.traits.provenance-traceable",
        "label": "Provenance Traceable",
        "applies_to": ["all"],
    },
    {
        "legacy_id": "AR.TRAIT.CONTENT_STATUS_SEPARATED",
        "compact_id": "se.accountable-record.traits.content-status-separated",
        "label": "Content Status Separated",
        "applies_to": ["obligation", "rule-content", "rule-scope"],
    },
    {
        "legacy_id": "AR.TRAIT.AUTHORITY_NON_ASSERTED",
        "compact_id": "se.accountable-record.traits.authority-non-asserted",
        "label": "Authority Non-Asserted",
        "applies_to": ["obligation", "rule-content", "rule-scope", "source"],
    },
    {
        "legacy_id": "AR.TRAIT.SCOPE_DECLARED",
        "compact_id": "se.accountable-record.traits.scope-declared",
        "label": "Scope Declared",
        "applies_to": ["obligation", "rule-content"],
    },
    {
        "legacy_id": "AR.TRAIT.OBSERVATION_NON_AUTHORITATIVE",
        "compact_id": "se.accountable-record.traits.observation-non-authoritative",
        "label": "Observation Non-Authoritative",
        "applies_to": ["source", "domain-observation"],
    },
    {
        "legacy_id": "AR.TRAIT.LOCUS_STABLE",
        "compact_id": "se.accountable-record.traits.locus-stable",
        "label": "Locus Stable",
        "applies_to": ["place-or-asset"],
    },
    {
        "legacy_id": "AR.TRAIT.INSTRUMENT_NON_COLLAPSING",
        "compact_id": "se.accountable-record.traits.instrument-non-collapsing",
        "label": "Instrument Non-Collapsing",
        "applies_to": ["instrument"],
    },
    {
        "legacy_id": "AR.TRAIT.INTERPRETATION_NON_MUTATING",
        "compact_id": "se.accountable-record.traits.interpretation-non-mutating",
        "label": "Interpretation Non-Mutating",
        "applies_to": ["all"],
    },
]

TRANSFORMATION_BEHAVIORS = [
    {
        "id": "identity-preserving",
        "label": "Identity Preserving",
        "description": "The target record preserves the same subject identity as the source record.",
    },
    {
        "id": "identity-breaking",
        "label": "Identity Breaking",
        "description": "The target record represents a distinct subject identity from the source record.",
    },
    {
        "id": "identity-inheriting",
        "label": "Identity Inheriting",
        "description": "The target record represents a successor subject whose accountability lineage includes the source subject.",
    },
    {
        "id": "no-identity-question",
        "label": "No Identity Question",
        "description": "The operation does not raise an identity question for the represented subject.",
    },
]


TRANSFORMATION_PROFILE_RESPONSIBILITIES = [
    "declare recognized transformation kinds",
    "declare which record types or subject structures may be connected",
    "declare required evidence for each transformation kind",
    "declare which AR transformation behavior each transformation claims",
    "respect AR transformation behavior vocabulary",
    "respect subject-mapping-sensitive admissibility rules",
]


PY_PACKAGE_DIRS = [
    "vocabulary",
    "namespace",
    "contracts",
    "component_groups",
    "elements",
    "packages",
    "mappings",
    "records",
    "build",
    "render",
]

VERIFIER_CONTRACT_RULES = [
    {
        "id": "deterministic",
        "label": "Deterministic",
        "description": "The same inputs produce the same outputs. Outcome nondeterminism is a defect.",
    },
    {
        "id": "complete-over-claim-set",
        "label": "Complete Over Claim Set",
        "description": "Every selected applicable claim is run, regardless of whether earlier claims failed.",
    },
    {
        "id": "disciplined-explanation",
        "label": "Disciplined Explanation",
        "description": "The verifier reports outcomes, findings, identifiers, and structured evidence without uncited editorial conclusions.",
    },
]

VERIFIER_OPERATIONS = [
    {
        "id": "inspect",
        "label": "Inspect",
        "produces_report": False,
        "runs_claims": False,
        "description": "Summarizes bundle declarations and structure without running claims.",
    },
    {
        "id": "validate",
        "label": "Validate",
        "produces_report": True,
        "runs_claims": True,
        "description": "Runs applicable claims and produces an AR report.",
    },
]

GOVERNANCE_BOUNDARIES = [
    {
        "id": "truth",
        "label": "Truth",
        "description": "AR does not decide whether a statement is true.",
    },
    {
        "id": "authority",
        "label": "Authority",
        "description": "AR does not decide whether a record, source, claim, or institution is authoritative.",
    },
    {
        "id": "legal-effect",
        "label": "Legal Effect",
        "description": "AR does not decide legal effect, enforceability, or legal validity.",
    },
    {
        "id": "institutional-legitimacy",
        "label": "Institutional Legitimacy",
        "description": "AR does not decide whether an institution, process, decision, or actor is legitimate.",
    },
    {
        "id": "obligation-enforcement",
        "label": "Obligation Enforcement",
        "description": "AR does not enforce obligations, permissions, prohibitions, or duties.",
    },
    {
        "id": "causal-explanation",
        "label": "Causal Explanation",
        "description": "AR does not decide causal explanation.",
    },
    {
        "id": "epistemic-evaluation",
        "label": "Epistemic Evaluation",
        "description": "AR does not decide credibility, certainty, belief, knowledge, or epistemic warrant.",
    },
    {
        "id": "analytics",
        "label": "Analytics",
        "description": "AR does not define analytic models, optimization, prediction, recommendation, or scoring.",
    },
    {
        "id": "operational-deployment",
        "label": "Operational Deployment",
        "description": "AR does not define databases, APIs, authentication, authorization, access control, hosting, or runtime deployment.",
    },
    {
        "id": "cryptographic-attestation",
        "label": "Cryptographic Attestation",
        "description": "AR does not require cryptographic attestation. Attestation may be layered outside the core contract.",
    },
]


ADOPTION_FIT_SIGNALS = [
    {
        "id": "persistent-disagreement",
        "label": "Persistent Disagreement",
        "description": "Records may be questioned later by parties who disagree about meaning, source, scope, authority, status, or interpretation.",
    },
    {
        "id": "inspectable-exports",
        "label": "Inspectable Exports",
        "description": "The system needs exported records that can be inspected independently of the producing application.",
    },
    {
        "id": "source-traceability",
        "label": "Source Traceability",
        "description": "Readers need to inspect records against source material, citations, files, observations, or provenance.",
    },
    {
        "id": "cross-system-mapping",
        "label": "Cross-System Mapping",
        "description": "The system needs to map local, domain, institutional, or external vocabulary into a durable structure.",
    },
    {
        "id": "verification-reporting",
        "label": "Verification Reporting",
        "description": "The system needs reports showing what was checked, what passed, what failed, what was partial, and what could not be verified.",
    },
    {
        "id": "record-evolution",
        "label": "Record Evolution",
        "description": "The system needs to preserve corrections, transformations, reinterpretations, or successor relations over time.",
    },
]


ADOPTION_POOR_FIT_SIGNALS = [
    {
        "id": "ordinary-schema-validation-is-enough",
        "label": "Ordinary Schema Validation Is Enough",
        "description": "The system only needs to check shape and required fields, without preserving disagreement or verification context.",
    },
    {
        "id": "single-short-lived-authority",
        "label": "Single Short-Lived Authority",
        "description": "The records are short-lived and controlled by one trusted authority with no durable contestation burden.",
    },
    {
        "id": "workflow-platform-needed",
        "label": "Workflow Platform Needed",
        "description": "The team primarily needs forms, approvals, dashboards, APIs, authorization, or case management rather than export accountability.",
    },
    {
        "id": "no-independent-inspection-needed",
        "label": "No Independent Inspection Needed",
        "description": "No one needs to inspect the exported records outside the producing system.",
    },
]


READINESS_QUESTIONS = [
    {
        "id": "records-questioned-later",
        "question": "Will these records be questioned later by people or systems that may disagree?",
    },
    {
        "id": "source-inspection-needed",
        "question": "Does a reader need to inspect records against sources, citations, provenance, or evidence?",
    },
    {
        "id": "meaning-and-status-separable",
        "question": "Do content, status, interpretation, source, scope, or provenance need to remain separable?",
    },
    {
        "id": "exports-needed",
        "question": "Does the system need to export records for review outside the original application?",
    },
    {
        "id": "verification-report-needed",
        "question": "Would a verifier report showing pass, fail, partial, cannot-verify, and not-run information be useful?",
    },
    {
        "id": "incremental-adoption-needed",
        "question": "Does the system need a path that starts with bundle shape and grows toward stronger conformance?",
    },
]


def write_if_missing(path: Path, content: str) -> None:
    """Write content to path if the file does not already exist. Idempotent."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(content, encoding="utf-8")


def write_json_if_missing(path: Path, data: object) -> None:
    """Write JSON data to path if the file does not already exist. Idempotent."""
    content = json.dumps(data, indent=2) + "\n"
    write_if_missing(path, content)


def empty_schema(title: str) -> dict[str, object]:
    """Generate an empty JSON schema with the given title. Additional properties are allowed."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://structural-explainability.org/accountable-record/schemas/{title}.schema.json",
        "title": title,
        "type": "object",
        "additionalProperties": True,
    }


def element_manifest(group: str, element: str) -> str:
    """Generate a manifest for an accountable record element."""
    compact_id = f"se.accountable-record.{group}.{element}"
    canonical_uri = (
        "https://structural-explainability.org/"
        f"accountable-record/elements/{group}/{element}"
    )
    persistent_id = f"urn:ar:se:accountable-record:{group}:{element}"

    label = element.replace("-", " ").title()

    return f'''schema = "ar-element-type-1"

[identity]
canonical_uri = "{canonical_uri}"
persistent_id = "{persistent_id}"
compact_id = "{compact_id}"
local_name = "{element}"
label = "{label}"

[namespace]
authority = "structural-explainability.org"
authority_alias = "se"
project = "accountable-record"

[classification]
artifact_kind = "element-type"
component_group = "{group}"

[release]
version = "0.1.0"
status = "working-draft"
immutable = false

[definition]
description = """
TODO: Define this verifiable element type.
"""
plain_language = """
TODO: Explain this element in plain language.
"""

[identity_rules]
element_type_id_field = "element_type_id"
element_instance_id_field = "element_instance_id"

[structure]
schema = "schema.schema.json"
checks = "checks.toml"
examples = "examples/"

[compatibility]
breaking_changes_require_new_major = true
requires = []

[deprecation]
deprecated = false
successor = ""

[stewardship]
maintainer = "Structural Explainability"
status = "active"

[hosting]
provider = "github"
organization = "structural-explainability"
repository = "accountable-record"
url = "https://github.com/structural-explainability/accountable-record"
'''


def element_checks(group: str, element: str) -> str:
    """Generate a basic set of checks for an accountable record element."""
    compact_id = f"se.accountable-record.{group}.{element}"
    prefix = element.replace("-", "_")

    return f'''schema = "ar-element-checks-1"

element_type_id = "{compact_id}"

[[checks]]
id = "{prefix}.has-element-type-id"
label = "Has element type ID"
level = "required"
description = """
An element instance must identify the element type it conforms to.
"""

[[checks]]
id = "{prefix}.has-instance-id"
label = "Has instance ID"
level = "required"
description = """
An element instance must have a stable element instance identifier.
"""
'''


def element_schema(group: str, element: str) -> dict[str, object]:
    """Generate a JSON schema for an accountable record element.

    Args:
        group (str): The group to which the element belongs.
        element (str): The name of the element.

    Returns:
        dict[str, object]: The JSON schema for the element.
    """
    compact_id = f"se.accountable-record.{group}.{element}"
    schema_id = (
        "https://structural-explainability.org/accountable-record/"
        f"schemas/elements/{group}/{element}.schema.json"
    )

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": schema_id,
        "title": element.replace("-", " ").title(),
        "type": "object",
        "required": [
            "element_type_id",
            "element_instance_id",
        ],
        "properties": {
            "element_type_id": {
                "const": compact_id,
            },
            "element_instance_id": {
                "type": "string",
            },
        },
        "additionalProperties": True,
    }


def element_example(group: str, element: str) -> dict[str, str]:
    """Generate an example instance of an accountable record element.

    Args:
        group (str): The group to which the element belongs.
        element (str): The name of the element.

    Returns:
        dict[str, str]: An example instance of the element.
    """
    return {
        "element_type_id": f"se.accountable-record.{group}.{element}",
        "element_instance_id": f"{element}-001",
    }


def scaffold_root_files() -> None:
    """Scaffold root files."""
    for relative_path, content in ROOT_FILES.items():
        write_if_missing(ROOT / relative_path, content)


def scaffold_data_index() -> None:
    """Scaffold the data index file, which serves as the manifest for the repository and the source of truth for all paths and identifiers."""
    write_if_missing(
        ROOT / "data" / "index.toml",
        '''schema = "ar-data-index-1"

[repo]
id = "accountable-record"
label = "Accountable Record"
version = "0.1.0"
status = "working-draft"

[source]
vocabulary = "data/vocabulary/terms.toml"
namespace = "data/namespace/"
contracts = "data/contracts/"
governance = "data/governance/"
adoption = "data/adoption/"
component_groups = "data/component-groups/index.toml"
elements = "data/elements/"
packages = "data/packages/"
claims = "data/claims/"
traits = "data/traits/"
conformance = "data/conformance/"
verification = "data/verification/"
export_contract = "data/export-contract/"
mappings = "data/mappings/"
subject_mappings = "data/subject-mappings/"
transformations = "data/transformations/"
failure_modes = "data/failure-modes/"
records = "data/records/"

[export]
index = "data/export/index.json"
vocabulary = "data/export/vocabulary/"
component_groups = "data/export/component-groups/"
elements = "data/export/elements/"
mappings = "data/export/mappings/"
records = "data/export/records/"

[schemas]
directory = "data/schemas/"
''',
    )


def scaffold_export_contract() -> None:
    """Scaffold the exports contract files."""
    export_contract_dir = ROOT / "data" / "export-contract"

    write_if_missing(
        export_contract_dir / "index.toml",
        '''schema = "ar-export-contract-index-1"

artifact_types = "data/export-contract/artifact-types.toml"
bundle = "data/export-contract/bundle-envelope.toml"
profile = "data/export-contract/profile-envelope.toml"
report = "data/export-contract/report-envelope.toml"
schemas = "data/export-contract/schemas.toml"
extensions = "data/export-contract/extensions.toml"
operations = "data/export-contract/operations.toml"
''',
    )

    artifact_entries = []
    for artifact in EXPORT_ARTIFACT_TYPES:
        artifact_entries.append(
            f'''[[artifact_types]]
id = "{artifact["id"]}"
label = "{artifact["label"]}"
schema = "{artifact["schema"]}"
description = """
{artifact["description"]}
"""
'''
        )

    write_if_missing(
        export_contract_dir / "artifact-types.toml",
        'schema = "ar-export-artifact-types-1"\n\n'
        + "\n".join(artifact_entries)
        + '''
[semantics]
exported_artifact_types = [
  "bundle",
  "profile",
  "report",
]
composition_units_are_not_verification_artifact_types = true
''',
    )

    write_if_missing(
        export_contract_dir / "bundle-envelope.toml",
        '''schema = "ar-bundle-envelope-1"

[artifact]
id = "bundle"
schema_identifier = "accountable-record-bundle-1"

[required_top_level_fields]
fields = [
  "schema",
  "bundle_id",
  "versions",
  "conformance",
  "manifest",
  "records",
]

[recommended_top_level_fields]
fields = [
  "generated_at",
]

[records]
required_fields = [
  "id",
  "record_type",
]

[level_1_fields]
where_applicable = [
  "source_reference",
  "provenance",
]

[level_2_fields]
fields = [
  "subject_kind",
]

[reserved_conformance_keys]
keys = [
  "ar",
  "se",
  "ar_level",
  "ar_profile",
]
''',
    )

    write_if_missing(
        export_contract_dir / "profile-envelope.toml",
        '''schema = "ar-profile-envelope-1"

[artifact]
id = "profile"
schema_identifier = "accountable-record-profile-1"

[required_top_level_fields]
fields = [
  "schema",
  "profile_id",
  "ar_version",
]

[composition]
preferred_model = "element-packages"
may_select = [
  "ar element packages",
  "domain element packages",
  "local element packages",
  "proprietary element packages",
  "selected element types",
]

[profile_contents]
may_define = [
  "record types",
  "traits",
  "field mappings",
  "transformations",
  "claims",
  "acceptance rules",
  "verifier expectations",
]

[constraints]
may_not_redefine_ar_outcomes = true
may_not_redefine_ar_transformation_behaviors = true
may_not_redefine_ar_element_identity = true
''',
    )

    write_if_missing(
        export_contract_dir / "report-envelope.toml",
        '''schema = "ar-report-envelope-1"

[artifact]
id = "report"
schema_identifier = "accountable-record-report-1"

[required_top_level_fields]
fields = [
  "schema",
  "report_id",
  "verifier",
  "bundle",
  "declared_level",
  "achieved_level",
  "summary",
  "results",
]

[recommended_top_level_fields]
fields = [
  "generated_at",
  "profile",
  "element_packages",
]

[results]
required_fields = [
  "claim_id",
  "outcome",
]
optional_fields = [
  "evidence",
  "sub_results",
]

[semantics]
report_is_inspectable = true
cites_by_identifier = true
does_not_summarize_away_evidence = true
''',
    )

    write_if_missing(
        export_contract_dir / "schemas.toml",
        '''schema = "ar-export-schemas-1"

[schemas]
directory = "data/schemas"

required = [
  "ar-record.schema.json",
  "ar-export-index.schema.json",
  "ar-element-type.schema.json",
  "ar-element-instance.schema.json",
]

[legacy_schema_names]
names = [
  "bundle-1.json",
  "profile-1.json",
  "report-1.json",
  "claim-1.json",
  "trait-1.json",
  "component-1.json",
]

[versioning]
schema_changes_follow_contract_versioning = true
breaking_schema_changes_require_major_version = true
''',
    )

    write_if_missing(
        export_contract_dir / "extensions.toml",
        '''schema = "ar-export-extensions-1"

[extension_model]
profiles_may_add_fields = true
domain_schemas_may_extend_ar_envelope = true
domain_schemas_must_not_replace_ar_envelope = true

[forbidden_extensions]
rules = [
  "must not override or redefine required fields",
  "must not use keys beginning with _ar_",
  "must not omit required fields because they are outside a package concern",
]

[missing_required_evidence]
claim_outcome = "cannot-verify"
description = """
If a selected element package or profile requires evidence and that evidence is
absent, the corresponding claim result is cannot-verify.
"""
''',
    )

    operation_entries = []
    for operation in EXPORT_OPERATIONS:
        operation_entries.append(
            f'''[[operations]]
id = "{operation["id"]}"
label = "{operation["label"]}"
produces_ar_report = {str(operation["produces_ar_report"]).lower()}
description = """
{operation["description"]}
"""
'''
        )

    write_if_missing(
        export_contract_dir / "operations.toml",
        'schema = "ar-export-operations-1"\n\n' + "\n".join(operation_entries),
    )


def scaffold_vocabulary() -> None:
    """Scaffold the vocabulary files."""
    write_if_missing(
        ROOT / "data" / "vocabulary" / "terms.toml",
        '''schema = "ar-vocabulary-terms-1"

[[terms]]
id = "accountable-record"
label = "Accountable Record"
status = "stable-draft"
definition = """
A structured record composed of verifiable elements.
"""
plain_language = """
A record made of parts that can be checked, traced, related, and reviewed.
"""
related_terms = [
  "verifiable-element",
  "element-type",
  "element-instance",
  "component-group",
]

[[terms]]
id = "verifiable-element"
label = "Verifiable Element"
status = "stable-draft"
definition = """
An independently identifiable part of an Accountable Record that can be
claimed about, sourced, related, verified, exported, and reviewed.
"""
plain_language = """
A part of an Accountable Record that can be checked on its own.
"""
aliases = [
  "element",
]
deprecated_aliases = [
  "verifiable-unit",
]
related_terms = [
  "accountable-record",
  "element-type",
  "element-instance",
  "component-group",
]
''',
    )
    write_if_missing(
        ROOT / "data" / "vocabulary" / "aliases.toml",
        'schema = "ar-vocabulary-aliases-1"\n',
    )
    write_if_missing(
        ROOT / "data" / "vocabulary" / "deprecated-terms.toml",
        'schema = "ar-deprecated-terms-1"\n',
    )


def scaffold_namespace() -> None:
    """Scaffold the namespace files, which define the authorities, projects, and identifier rules for the accountable record ecosystem."""
    namespace_dir = ROOT / "data" / "namespace"
    write_if_missing(
        namespace_dir / "authorities.toml",
        '''schema = "ar-namespace-authorities-1"

[[authorities]]
authority = "structural-explainability.org"
authority_alias = "se"
status = "active"
label = "Structural Explainability"
canonical_url = "https://structural-explainability.org"

[[authorities.projects]]
project = "accountable-record"
label = "Accountable Record"
canonical_uri_base = "https://structural-explainability.org/accountable-record"
compact_id_base = "se.accountable-record"

[authorities.projects.hosting]
provider = "github"
organization = "structural-explainability"
repository = "accountable-record"
url = "https://github.com/structural-explainability/accountable-record"
''',
    )
    write_if_missing(
        namespace_dir / "authority-aliases.toml", 'schema = "ar-authority-aliases-1"\n'
    )
    write_if_missing(
        namespace_dir / "projects.toml", 'schema = "ar-namespace-projects-1"\n'
    )
    write_if_missing(
        namespace_dir / "identifier-rules.toml",
        '''schema = "ar-identifier-rules-1"

[canonical_uri]
pattern = "https://<authority>/<project>/elements/<component-group>/<element-type>"
preferred = true
version_included = false

[persistent_id]
pattern = "urn:ar:<authority-alias>:<project>:<component-group>:<element-type>"
required = false
version_included = false

[compact_id]
pattern = "<authority-alias>.<project>.<component-group>.<element-type>"
required = true
version_included = false

[versioned_reference]
pattern = "<compact-id>@<version>"

[segments]
case = "lowercase"
character_set = "ascii"
word_separator = "hyphen"
segment_separator = "dot"
element_type_number = "singular"
component_group_number = "plural"

[stability]
published_element_ids_are_immutable = true
breaking_changes_require_new_major = true
deprecated_ids_must_not_be_reused = true
''',
    )


def scaffold_component_groups() -> None:
    """Scaffold the component group files."""
    groups_as_toml = "\n".join(f'  "{group}",' for group in COMPONENT_GROUPS)
    write_if_missing(
        ROOT / "data" / "component-groups" / "index.toml",
        f'''schema = "ar-component-group-index-1"

groups = [
{groups_as_toml}
]
''',
    )

    for group in COMPONENT_GROUPS:
        group_dir = ROOT / "data" / "component-groups" / group
        write_if_missing(
            group_dir / "group.toml",
            f'''schema = "ar-component-group-1"

id = "{group}"
label = "{group.replace("-", " ").title()}"
status = "working-draft"

definition = """
TODO: Define the {group} component group.
"""

plain_language = """
TODO: Explain this component group in plain language.
"""

element_directory = "data/elements/{group}"
''',
        )


def _validate_outcomes() -> None:
    ids = [o["id"] for o in CLAIM_OUTCOMES]
    assert len(set(ids)) == len(ids), "duplicate outcome id"
    # the two semantic orderings must cover exactly the defined set
    assert set(DEFINED_OUTCOMES) == set(ids), "closed vocab drift"
    assert set(SUMMARY_SEVERITY_ORDER) == set(ids), "severity order drift"
    # exactly one pass, exactly one failure
    assert sum(o["is_pass"] for o in CLAIM_OUTCOMES) == 1
    assert sum(o["is_failure"] for o in CLAIM_OUTCOMES) == 1
    # cannot-verify is the unique evidence_sufficient == False
    assert [o["id"] for o in CLAIM_OUTCOMES if not o["evidence_sufficient"]] == [
        "cannot-verify"
    ]


def scaffold_conformance() -> None:
    """Scaffold the conformance files."""
    _validate_outcomes()  # fail before emitting anything inconsistent
    conformance_dir = ROOT / "data" / "conformance"

    write_if_missing(
        conformance_dir / "index.toml",
        '''schema = "ar-conformance-index-1"

outcomes = "data/conformance/outcomes.toml"
selection = "data/conformance/claim-selection.toml"
levels = "data/conformance/achieved-level-semantics.toml"
reports = "data/conformance/report-semantics.toml"
errors = "data/conformance/verifier-errors.toml"
compatibility = "data/conformance/compatibility.toml"
''',
    )

    outcome_entries = []
    for outcome in CLAIM_OUTCOMES:
        outcome_entries.append(
            f'''[[outcomes]]
id = "{outcome["id"]}"
label = "{outcome["label"]}"
description = """
{outcome["description"]}
"""
is_pass = {str(outcome["is_pass"]).lower()}
is_failure = {str(outcome["is_failure"]).lower()}
evidence_sufficient = {str(outcome["evidence_sufficient"]).lower()}
blocks_mandatory_level = {str(outcome["blocks_mandatory_level"]).lower()}
'''
        )

    defined_lines = "\n".join(f'  "{item}",' for item in DEFINED_OUTCOMES)
    severity_lines = "\n".join(f'  "{item}",' for item in SUMMARY_SEVERITY_ORDER)

    write_if_missing(
        conformance_dir / "outcomes.toml",
        'schema = "ar-conformance-outcomes-1"\n\n'
        + "\n".join(outcome_entries)
        + f'''
[closed_vocabulary]
only_defined_outcomes_allowed = true
defined_outcomes = [
{defined_lines}
]

[summary_aggregation]
severity_order = [
{severity_lines}
]
description = """
The severity order is for reporting and aggregation. It does not change the
meaning of individual outcomes. It is intentionally aligned with the
composite_claim_rollup precedence: a determinate failure outranks missing
evidence in both. Changing one without the other is a contract error.
"""

[composite_claim_rollup]
rollup_defined_over_required_requirements_only = true
unknown_requirement_outcome_is_an_error = true
description = """
A claim with multiple verifiable requirements derives its outcome from its
per-requirement outcomes, each itself one of the four defined outcomes.
Precedence:

1. If any required requirement is fail or partial, the claim outcome is fail or
   partial. A determinate negative result is not masked by missing evidence.
2. Otherwise, if any required requirement is cannot-verify, the claim is
   cannot-verify.
3. Otherwise, if every required requirement is pass, the claim is pass.

Within rule 1, a mix of pass and fail (with evidence present throughout) is
partial; an all-fail set is fail. Rollup is evaluated only over required
requirements for the selected level. An unrecognized per-requirement outcome is
a verifier error, not a claim outcome.
"""
''',
    )

    not_run_lines = "\n".join(f'  "{item}",' for item in NOT_RUN_REASONS)

    write_if_missing(
        conformance_dir / "claim-selection.toml",
        f'''schema = "ar-claim-selection-1"

[selection_inputs]
inputs = [
  "declared AR contract version",
  "declared target adoption level",
  "selected profile",
  "profile adopted AR claims",
  "profile-defined claims",
  "verifier configuration for optional claims",
]

[mandatory_claims]
declared_level_and_lower_are_selected = true

[optional_claims]
selected_only_when_included_by_profile_bundle_or_verifier = true

[not_run]
claims_not_run_do_not_receive_outcomes = true
claims_not_run_may_be_listed_as_metadata = true
reasons = [
{not_run_lines}
]
''',
    )

    write_if_missing(
        conformance_dir / "achieved-level-semantics.toml",
        '''schema = "ar-achieved-level-semantics-1"

[adoption_levels]
levels_are_nested = true
bundle_may_declare_target_level = true
verifier_reports_achieved_level = true

[achievement]
requires_all_mandatory_claims_for_level_and_lower_to_pass = true
composite_claim_outcomes_resolved_by_rollup = true
fail_blocks_level = true
partial_blocks_level = true
cannot_verify_blocks_level = true
description = """
A level is achieved when every mandatory claim selected for that level and all
lower levels resolves to pass. Composite (multi-requirement) claims resolve to a
single outcome via the composite_claim_rollup rule in outcomes.toml before level
achievement is evaluated. Any non-pass outcome (fail, partial, cannot-verify)
on a mandatory claim blocks the level.
"""

[profile_rules]
profiles_may_define_additional_profile_conformance_rules = true
profiles_do_not_redefine_ar_achieved_level_semantics = true
''',
    )

    write_if_missing(
        conformance_dir / "report-semantics.toml",
        '''schema = "ar-conformance-report-semantics-1"

[report]
records_outcomes = true
records_evidence = true
records_not_run_metadata = true
records_declared_level = true
records_achieved_level = true

[evidence]
required_for_outcomes = [
  "fail",
  "partial",
]
missing_evidence_must_be_identified_for_outcomes = [
  "cannot-verify",
]
must_identify = [
  "what was checked",
  "which records were involved",
  "what failed",
  "what was partially satisfied",
  "what evidence was missing",
]
cites_bundle_elements_by_stable_identifiers = true
does_not_decide_truth_authority_or_domain_correctness = true
description = """
Outcomes that report a determinate negative result (fail, partial) require
positive evidence: the report must show what was checked and what did not hold.
The cannot-verify outcome is the absence of a determination; it cannot carry
positive evidence by definition, so the report must instead identify what
required evidence was missing.
"""

[structural_non_conformance]
mandatory_outcomes_that_block = [
  "fail",
  "partial",
  "cannot-verify",
]
verification_should_not_stop_at_first_failure = true
''',
    )

    write_if_missing(
        conformance_dir / "verifier-errors.toml",
        '''schema = "ar-verifier-errors-1"

[semantics]
verifier_level_errors_are_not_claim_outcomes = true

[[errors]]
id = "input-cannot-be-parsed"
label = "Input Cannot Be Parsed"

[[errors]]
id = "input-not-readable-document"
label = "Input Is Not a Readable Document"

[[errors]]
id = "required-external-profile-cannot-be-loaded"
label = "Required External Profile Cannot Be Loaded"

[[errors]]
id = "verifier-configuration-invalid"
label = "Verifier Configuration Invalid"

[boundary]
readable_bundle_missing_required_ar_fields_is_claim_outcome = true
if_bundle_can_be_read_and_claims_can_run_report_should_be_produced = true
''',
    )

    write_if_missing(
        conformance_dir / "compatibility.toml",
        '''schema = "ar-conformance-compatibility-1"

[implementations]
must_preserve_outcome_semantics = true

[equivalence]
same_inputs_should_produce_same_claim_outcomes = true
inputs = [
  "bundle",
  "profile",
  "claims",
  "traits",
  "AR contract version",
]

[allowed_differences]
not_conformance_differences = [
  "timestamps",
  "formatting",
  "diagnostic wording",
  "implementation-specific metadata",
]

[authority]
source = "AR contract repository"
includes = [
  "specifications",
  "schemas",
  "claim definitions",
  "trait definitions",
  "examples",
  "expected reports",
]
''',
    )


def scaffold_elements() -> None:
    """Scaffold the element files, which define the accountable record element types and their associated schemas, checks, and examples."""
    for group, elements in ELEMENTS_BY_GROUP.items():
        for element in elements:
            element_dir = ROOT / "data" / "elements" / group / element

            write_if_missing(
                element_dir / "element.toml", element_manifest(group, element)
            )
            write_if_missing(
                element_dir / "checks.toml", element_checks(group, element)
            )
            write_json_if_missing(
                element_dir / "schema.schema.json", element_schema(group, element)
            )
            write_json_if_missing(
                element_dir / "examples" / "valid.json",
                element_example(group, element),
            )


def scaffold_schemas() -> None:
    """Scaffold the schema files, which define the JSON schemas for accountable record elements, bundles, profiles, reports, claims, traits, and other artifacts."""
    for schema_file in SCHEMA_FILES:
        title = schema_file.removesuffix(".schema.json")
        write_json_if_missing(
            ROOT / "data" / "schemas" / schema_file, empty_schema(title)
        )


def scaffold_mappings() -> None:
    """Scaffold the mapping files, which define the mappings between external standards and the accountable record schema."""
    mapping_names = [
        "prov",
        "dublin-core",
        "schema-org",
        "nist-ai-rmf",
    ]

    for mapping_name in mapping_names:
        mapping_dir = ROOT / "data" / "mappings" / mapping_name
        write_if_missing(
            mapping_dir / "mapping-guide.toml",
            f'''schema = "ar-mapping-guide-1"

id = "{mapping_name}-to-accountable-record"
label = "{mapping_name} to Accountable Record"
status = "working-draft"

[source_standard]
id = "{mapping_name}"
label = "{mapping_name}"

[target]
id = "accountable-record"
label = "Accountable Record"
''',
        )
        write_if_missing(
            mapping_dir / "questions.toml", 'schema = "ar-mapping-questions-1"\n'
        )
        write_json_if_missing(
            mapping_dir / "examples" / f"{mapping_name}-input.json", {}
        )
        write_json_if_missing(mapping_dir / "examples" / "ar-output.json", {})


def scaffold_records() -> None:
    """Scaffold the record files, which define the progressive levels of accountable record maturity."""
    for level in range(6):
        write_json_if_missing(
            ROOT / "data" / "records" / "progressive" / f"level-{level}.json",
            {
                "schema": "ar-record-1",
                "maturity_level": level,
                "elements": [],
            },
        )


def scaffold_contracts() -> None:
    """Scaffold the contract files, which define the identity and package contracts for the accountable record ecosystem."""
    contracts_dir = ROOT / "data" / "contracts"

    write_if_missing(
        contracts_dir / "identity-contract.toml",
        '''schema = "ar-identity-contract-1"

[scope]
description = """
The identity contract defines how Accountable Record authorities, project
spaces, element types, element instances, element packages, schemas, exported
artifacts, and lock entries are identified.
"""

[principles]
identity_is_authority_based = true
identity_is_not_host_based = true
hosting_location_is_metadata = true
canonical_identity_does_not_include_version = true
released_identifiers_must_not_be_renamed = true
released_identifiers_must_not_be_repurposed = true

[namespace_authority]
description = """
A namespace authority is an organization, domain, registry, or owner
responsible for assigning stable names within a project space.
"""

[project_space]
description = """
A project space is a stable project, package, repository, product, standard,
or domain space within a namespace authority.
"""

[canonical_uri]
pattern = "https://<authority>/<project>/elements/<component-group>/<element-type>"
preferred_for_public_elements = true
version_included = false

[persistent_id]
pattern = "urn:ar:<authority-alias>:<project>:<component-group>:<element-type>"
allowed_for_private_archival_or_non_web_contexts = true
version_included = false

[compact_id]
pattern = "<authority-alias>.<project>.<component-group>.<element-type>"
requires_authority_alias_resolution = true
version_included = false

[versioned_reference]
pattern = "<compact-id>@<version>"

[element_identity]
package_independent = true
element_id_must_not_include_package_id = true
element_id_must_include_authority = true
element_id_must_include_project = true
element_id_must_include_component_group = true
element_id_must_include_element_type = true
description = """
A verifiable element type has stable identity independent of the element
packages that include it. Element packages include element types by reference.
Moving an element type from one package to another is a package composition
change, not an element identity change.
"""

[element_instance_id]
scope = "record-or-bundle"
description = """
Element instance identifiers identify concrete occurrences of element types
inside records, bundles, reports, fixtures, or examples.
"""

[package_identity]
separate_from_element_identity = true
description = """
An element package has its own identity. A package may include one or more
element types by reference. The package does not own the element identities
unless the same authority and project also define those element types.
"""

[catalog]
catalog_is_required_for_package_membership = true
description = """
Because element identity is package-independent, package membership and current
distribution provenance are resolved through package manifests, catalogs, and
lock files rather than inferred from the element ID alone.
"""

[hosting]
allowed_providers = [
  "github",
  "gitlab",
  "self-hosted-git",
  "institutional-repository",
  "private-registry",
  "public-registry",
  "local",
  "other",
]
''',
    )

    write_if_missing(
        contracts_dir / "package-contract.toml",
        '''schema = "ar-package-contract-1"

[scope]
description = """
The package contract defines what an Accountable Record element package
guarantees to downstream systems and how packages may be composed across
authority and project boundaries.
"""

[principles]
packages_are_versioned = true
released_package_versions_are_immutable = true
packages_may_depend_on_other_packages = true
packages_may_depend_on_element_types = true
packages_are_resolved_before_validation = true
validation_uses_resolved_dependencies = true

[package_identity]
required_fields = [
  "canonical_uri",
  "persistent_id",
  "compact_id",
  "local_name",
  "label",
  "version",
]

[package_contents]
may_include = [
  "element types",
  "schemas",
  "checks",
  "examples",
  "mappings",
  "fixtures",
  "expected reports",
  "verifier expectations",
  "claim sets",
  "trait libraries",
  "documentation targets",
  "rationale",
]

[dependencies]
supports_version_ranges = true
supports_exact_versions = true
supports_transitive_dependencies = true
conflicts_must_be_reported = true

[resolution]
authoring_may_use_version_ranges = true
resolution_produces_exact_versions = true
resolution_produces_digests = true
validation_uses_lock_file = true
range_conflicts_are_errors = true
one_major_version_per_identity_per_graph = true

[resolution.conflicts]
when_version_ranges_do_not_intersect = "hard-fail"
override_allowed = false
description = """
If two dependencies require incompatible version ranges for the same package or
element identity, resolution fails. AR does not silently choose one, override
the other, or allow ambiguous mixed semantics.
"""

[resolution.major_versions]
coexisting_major_versions_allowed = false
description = """
A resolved dependency graph may contain only one major version for a given
package or element identity. Major-version coexistence would require
major-version-qualified identifiers, which AR does not use.
"""

[digest]
algorithm = "sha256"
digest_target = "canonical-generated-json"
digest_values_may_be_blank_before_release = true
released_artifacts_must_have_digests = true
digest_is_published_not_resolver_computed = true
description = """
Package and element digests are computed over canonical generated JSON, not
authored TOML source. Authored TOML may contain comments, formatting, ordering,
and other non-semantic differences that must not change downstream resolution.

The authoritative digest is computed by the publisher at release time and
travels with the published package (package manifest and catalog). Resolution
verifies that a fetched artifact reproduces its published digest; resolution
does not originate the authoritative digest. A digest mismatch is a resolution
error.
"""

[digest.canonical_json]
canonicalization_scheme = "rfc8785"
encoding = "utf-8"
unicode_normalization = "nfc"
line_endings = "lf"
object_keys = "lexicographic"
insignificant_whitespace = "omitted"
arrays_preserve_order = true
numbers = "rfc8785-jcs"
absent_and_null_are_equivalent = true
null_fields = "omitted"
description = """
Canonical JSON follows RFC 8785 (JSON Canonicalization Scheme). The encoding,
key ordering, whitespace, and number serialization rules below restate RFC 8785
for readability and are subordinate to it; where this block and RFC 8785 differ,
RFC 8785 governs.

Numbers follow the RFC 8785 / JCS serialization (the ECMAScript Number-to-string
algorithm). Authored exports SHOULD avoid bare JSON numbers for identity-bearing
values (versions, identifiers, enumerations are strings) so that number
serialization is rarely on the digest path.

A field that is absent and a field whose value is null are treated as identical:
AR canonical exports do not distinguish null from absence. Null-valued fields are
omitted from the canonical form. This makes additive changes digest-neutral for
prior content: introducing a new optional field does not alter the canonical
export, and therefore does not alter the digest, of content that does not set it.
"""

[digest.coverage]
covers_package_manifest = true
covers_included_element_exports = true
covers_included_schema_exports = true
covers_included_check_exports = true
covers_included_example_exports = true
covers_included_mapping_exports = true
covers_included_fixture_exports = true
covers_expected_report_exports = true
covers_dependency_declarations = true
covers_lock_metadata = false

[digest.boundary]
description = """
A package digest commits to the canonical exported package closure: package
metadata, included element type exports, schemas, checks, examples, mappings,
fixtures, expected reports, and dependency declarations. It does not commit to
local file paths, comments, TOML formatting, generated timestamps, or lock-file
metadata.
"""

[lock_file]
path = "data/locks/elements.lock.json"
records_exact_versions = true
records_digests = true
records_sources = true

[distribution]
registry_required_for_initial_publication = false
registry_compatible_metadata_required = true
source_url_required_when_available = true
digest_required_for_released_artifacts = true

[trust]
digests_supported = true
signatures_supported = true
signature_required = false
''',
    )

    write_if_missing(
        contracts_dir / "change-contract.toml",
        '''schema = "ar-change-contract-1"

[scope]
description = """
The change contract defines additive, compatible, breaking, deprecated,
superseded, and withdrawn changes for Accountable Record elements, packages,
schemas, exported artifacts, and conformance semantics.
"""

[principles]
released_identifiers_are_stable = true
released_package_versions_are_immutable = true
breaking_changes_require_major_version = true
deprecated_identifiers_remain_citable = true
deprecated_identifiers_must_not_be_reused = true
successors_must_be_explicit_when_available = true

[additive_changes]
examples = [
  "adding an optional field",
  "adding a new optional check",
  "adding a new example",
  "adding a new mapping guide",
  "adding a new element type without changing existing semantics",
]

[compatible_changes]
examples = [
  "clarifying documentation without changing semantics",
  "adding non-required metadata",
  "adding a compatible schema annotation",
  "adding an optional package dependency",
]

[breaking_changes]
examples = [
  "removing a released required field",
  "renaming a released identifier",
  "repurposing a released identifier",
  "changing outcome semantics",
  "changing required claim behavior",
  "changing an element schema incompatibly",
  "removing a package dependency required for prior validation",
]

[major_versions]
one_major_version_per_identity_per_resolved_graph = true
major_version_not_in_identifier = true
major_version_conflicts_are_resolution_errors = true
description = """
AR identifiers do not include major versions. Therefore, a resolved graph may
not contain multiple major versions of the same package or element identity.
Consumers that require incompatible major versions must resolve the conflict
before validation.
"""

[package_version_severity]
package_version_reflects_most_severe_included_change = true
breaking_change_in_included_element_is_breaking_for_package = true
description = """
A package version must reflect the most severe change among the package manifest
and all element exports the package includes. If an included element undergoes a
breaking change, the package that includes it undergoes a breaking change and
requires a major version bump. A package's version therefore always corresponds
to its current canonical export and digest; a package's version may not remain
unchanged while its canonical export changes.
"""

[independent_versioning]
elements_and_packages_version_independently = true
element_version_distinct_from_package_version = true
description = """
Because element identity is package-independent, element types and the packages
that include them carry their own versions and may advance on separate timelines.
The one-major-version-per-identity-per-graph rule applies independently to
element identities and to package identities. The package_version_severity rule
binds the two timelines: a package's version must move whenever the canonical
export of any included element changes.
"""

[outcome_changes]
closed_vocabulary = true
adding_new_claim_outcome_is_breaking = true
renaming_claim_outcome_is_breaking = true
removing_claim_outcome_is_breaking = true
changing_claim_outcome_meaning_is_breaking = true
description = """
Claim outcomes are a closed vocabulary. Consumers may exhaustively handle the
defined outcomes. Adding, removing, renaming, or changing the meaning of an
outcome is a breaking change.
"""

[deprecation]
allowed = true
removal_implied = false
deprecated_items_remain_citable = true
successor_field_required_when_successor_exists = true

[supersession]
allowed = true
superseded_items_remain_resolvable = true
successor_required = true

[withdrawal]
allowed = true
withdrawn_items_must_not_be_reused = true
reason_required = true

[versioning]
major_for_breaking = true
minor_for_additive = true
patch_for_corrections = true
''',
    )


def scaffold_exports() -> None:
    """Scaffold the export files, which define the generated JSON exports for accountable record elements, packages, mappings, and other artifacts. These are the outputs of the build process and the inputs to downstream systems, so they are scaffolded as empty files to be populated by the build rather than authored directly."""
    export_dirs = [
        "vocabulary",
        "namespace",
        "component-groups",
        "elements",
        "mappings",
        "records",
    ]
    write_json_if_missing(
        ROOT / "data" / "export" / "index.json", {"schema": "ar-export-index-1"}
    )
    for export_dir in export_dirs:
        write_if_missing(ROOT / "data" / "export" / export_dir / ".gitkeep", "")

    for group in COMPONENT_GROUPS:
        write_if_missing(ROOT / "data" / "export" / "elements" / group / ".gitkeep", "")


def scaffold_catalog_and_locks() -> None:
    """Scaffold the catalog and lock files, which define the authorities, projects, elements, and their locks."""
    write_if_missing(
        ROOT / "data" / "catalog" / "authorities.toml",
        'schema = "ar-catalog-authorities-1"\n',
    )
    write_if_missing(
        ROOT / "data" / "catalog" / "projects.toml",
        'schema = "ar-catalog-projects-1"\n',
    )
    write_if_missing(
        ROOT / "data" / "catalog" / "elements.toml", 'schema = "ar-element-catalog-1"\n'
    )
    write_json_if_missing(
        ROOT / "data" / "locks" / "elements.lock.json",
        {
            "schema": "ar-element-lock-1",
            "elements": [],
        },
    )


def scaffold_python_package() -> None:
    """Scaffold the Python package files, which define the structure and modules for the Accountable Record tooling."""
    package_root = ROOT / "src" / "accountable_record"
    write_if_missing(
        package_root / "__init__.py", '"""Accountable Record tooling."""\n'
    )
    write_if_missing(package_root / "py.typed", "")
    write_if_missing(
        package_root / "cli.py",
        '"""Command-line interface for Accountable Record tooling."""\n',
    )
    write_if_missing(
        package_root / "paths.py",
        '"""Path helpers for Accountable Record tooling."""\n',
    )
    write_if_missing(
        package_root / "errors.py",
        '"""Error types for Accountable Record tooling."""\n',
    )

    for package_dir in PY_PACKAGE_DIRS:
        target = package_root / package_dir
        write_if_missing(target / "__init__.py", "")
        for module_name in ["load.py", "validate.py", "export.py"]:
            write_if_missing(
                target / module_name, f'"""TODO: {package_dir} {module_name}."""\n'
            )

    write_if_missing(
        package_root / "namespace" / "resolve.py",
        '"""Namespace resolution helpers."""\n',
    )
    write_if_missing(
        package_root / "elements" / "resolve.py", '"""Element resolution helpers."""\n'
    )
    write_if_missing(
        package_root / "elements" / "catalog.py", '"""Element catalog helpers."""\n'
    )
    write_if_missing(
        package_root / "elements" / "lock.py", '"""Element lock file helpers."""\n'
    )
    write_if_missing(
        package_root / "mappings" / "questions.py", '"""Mapping question helpers."""\n'
    )
    write_if_missing(
        package_root / "records" / "maturity.py", '"""Maturity assessment helpers."""\n'
    )
    write_if_missing(
        package_root / "build" / "export_data.py",
        '"""Build generated JSON exports."""\n',
    )
    write_if_missing(
        package_root / "build" / "render_docs.py",
        '"""Build generated Markdown docs."""\n',
    )
    write_if_missing(
        package_root / "build" / "check_generated.py",
        '"""Check generated files are current."""\n',
    )
    write_if_missing(
        package_root / "render" / "markdown.py", '"""Markdown rendering helpers."""\n'
    )
    write_if_missing(
        package_root / "render" / "tables.py", '"""Table rendering helpers."""\n'
    )


def scaffold_docs() -> None:
    """Scaffold the documentation files, which define the human-readable documentation for the accountable record ecosystem. The root index points to the English docs; other languages and top-level docs may be added later."""
    write_if_missing(
        ROOT / "docs" / "index.md", "# Accountable Record\n\nSee `docs/en/`.\n"
    )
    docs_en = ROOT / "docs" / "en"

    for name in [
        "index",
        "overview",
        "vocabulary",
        "namespaces",
        "contracts",
        "identity-contract",
        "package-contract",
        "change-contract",
        "component-groups",
        "verifiable-elements",
        "verification",
        "maturity-levels",
        "mappings",
        "conformance",
        "governance",
        "traits",
        "exports",
        "subjects",
        "subject-mappings",
        "transformations",
        "failure-modes",
        "scope",
        "non-goals",
        "when-to-use-ar",
    ]:
        write_if_missing(
            docs_en / f"{name}.md", f"# {name.replace('-', ' ').title()}\n"
        )

    for group in COMPONENT_GROUPS:
        write_if_missing(
            docs_en / "component-groups" / f"{group}.md",
            f"# {group.replace('-', ' ').title()}\n",
        )

    write_if_missing(docs_en / "elements" / "index.md", "# Verifiable Elements\n")

    for mapping_name in ["prov", "dublin-core", "schema-org", "nist-ai-rmf"]:
        write_if_missing(
            docs_en / "mappings" / f"{mapping_name}.md",
            f"# {mapping_name} Mapping\n",
        )


def scaffold_subject_mappings() -> None:
    """Scaffold the subject mapping files, which define the guides for mapping external subject vocabularies to AR subject structure."""
    subject_mappings_dir = ROOT / "data" / "subject-mappings"

    guide_lines = "\n".join(f'  "{guide["id"]}",' for guide in SUBJECT_MAPPING_GUIDES)

    write_if_missing(
        subject_mappings_dir / "index.toml",
        f'''schema = "ar-subject-mapping-index-1"

mapping_guides = [
{guide_lines}
]
''',
    )

    for system in SUBJECT_MAPPING_SYSTEMS:
        system_dir = subject_mappings_dir / system["id"]

        write_if_missing(
            system_dir / "mapping-guide.toml",
            f'''schema = "ar-subject-mapping-guide-1"

[identity]
id = "{system["id"]}"
label = "{system["label"]}"
status = "working-draft"

[definition]
description = """
{system["description"]}
"""

[semantics]
ar_owns_subject_structure = true
external_vocabulary_is_not_ar_canonical = true
profiles_may_map_external_vocabularies = true
mappings_are_explicit_machine_readable_and_citable = true

[files]
subject_kind_map = "subject-kind-map.toml"
questions = "questions.toml"
examples = "examples/"
''',
        )

        write_if_missing(
            system_dir / "subject-kind-map.toml",
            '''schema = "ar-subject-kind-map-1"

[semantics]
description = """
This file maps an external subject or identity vocabulary into AR subject
structure. It does not make the external vocabulary canonical for AR.
"""

[[mappings]]
external_id = ""
external_label = ""
ar_subject_kind = ""
mapping_status = "placeholder"
notes = """
Replace this placeholder with citable mappings when the external vocabulary is
selected by a profile.
"""
''',
        )

        write_if_missing(
            system_dir / "questions.toml",
            '''schema = "ar-subject-mapping-questions-1"

[[questions]]
id = "subject.what-is-the-record-about"
label = "What is the record about?"
description = """
Identify the subject the record preserves information about.
"""

[[questions]]
id = "subject.which-vocabulary-is-used"
label = "Which subject vocabulary is used?"
description = """
Identify whether the profile uses a local, domain, institutional, or external
subject vocabulary.
"""

[[questions]]
id = "subject.how-is-it-mapped"
label = "How is the subject kind mapped?"
description = """
Declare the mapping from the profile's subject vocabulary to AR subject
structure.
"""
''',
        )

        write_if_missing(system_dir / "examples" / ".gitkeep", "")


def scaffold_tests_and_tools() -> None:
    """Scaffold the test and tool files, which define the tests for validating the accountable record artifacts and the tools for building and checking generated outputs."""
    test_files = [
        "test_adoption_valid.py",
        "test_component_groups_valid.py",
        "test_conformance_valid.py",
        "test_contracts_valid.py",
        "test_element_examples_valid.py",
        "test_element_lock_valid.py",
        "test_elements_valid.py",
        "test_export_contract_valid.py",
        "test_exports_valid.py",
        "test_failure_modes_valid.py",
        "test_generated_docs_current.py",
        "test_governance_valid.py",
        "test_mappings_valid.py",
        "test_namespace_source_valid.py",
        "test_packages_valid.py",
        "test_progressive_records_valid.py",
        "test_subject_mappings_valid.py",
        "test_traits_valid.py",
        "test_transformations_valid.py",
        "test_verification_valid.py",
        "test_vocabulary_source_valid.py",
    ]

    for test_file in test_files:
        write_if_missing(ROOT / "tests" / test_file, f'"""TODO: {test_file}."""\n')

    write_if_missing(ROOT / "tests" / "fixtures" / "valid" / ".gitkeep", "")
    write_if_missing(ROOT / "tests" / "fixtures" / "invalid" / ".gitkeep", "")

    for tool_file in ["build_exports.py", "build_docs.py", "check_generated.py"]:
        write_if_missing(ROOT / "tools" / tool_file, f'"""TODO: {tool_file}."""\n')


def scaffold_verification() -> None:
    """Scaffold the verification files, which define the semantics and contracts for verifying accountable records and their claims."""
    verification_dir = ROOT / "data" / "verification"

    write_if_missing(
        verification_dir / "index.toml",
        '''schema = "ar-verification-index-1"

contract = "data/verification/verifier-contract.toml"
operations = "data/verification/operations.toml"
evidence = "data/verification/evidence-semantics.toml"
aggregation = "data/verification/aggregation.toml"
identity = "data/verification/verifier-identity.toml"
errors = "data/conformance/verifier-errors.toml"
''',
    )

    contract_entries = []
    for rule in VERIFIER_CONTRACT_RULES:
        contract_entries.append(
            f'''[[rules]]
id = "{rule["id"]}"
label = "{rule["label"]}"
description = """
{rule["description"]}
"""
'''
        )

    write_if_missing(
        verification_dir / "verifier-contract.toml",
        'schema = "ar-verifier-contract-1"\n\n'
        + "\n".join(contract_entries)
        + '''
[signature]
form = "verify(bundle, profile?, contract_version) -> report"

[claim_set]
selected_claims_are_run_once = true
profile_requirements_may_change_mandatory_status = true
profile_requirements_do_not_redefine_ar_claims = true
bundle_without_profile_uses_ar_core_claims_at_declared_level = true

[report]
every_emission_inspectable_by_identifier = true
complete_description_not_first_finding = true
''',
    )

    operation_entries = []
    for operation in VERIFIER_OPERATIONS:
        operation_entries.append(
            f'''[[operations]]
id = "{operation["id"]}"
label = "{operation["label"]}"
runs_claims = {str(operation["runs_claims"]).lower()}
produces_report = {str(operation["produces_report"]).lower()}
description = """
{operation["description"]}
"""
'''
        )

    write_if_missing(
        verification_dir / "operations.toml",
        'schema = "ar-verifier-operations-1"\n\n' + "\n".join(operation_entries),
    )

    write_if_missing(
        verification_dir / "evidence-semantics.toml",
        '''schema = "ar-evidence-semantics-1"

[evidence]
structured_data_collected_while_running_claim = true

[required_for_outcomes]
outcomes = [
  "fail",
  "partial",
  "cannot-verify",
]

[must_identify]
items = [
  "what failed",
  "what was partially satisfied",
  "what evidence was missing",
  "which records were involved",
]

[cannot_verify]
evidence_describes_missing_information = true

[partial]
evidence_describes_split = true
sub_results_required_when_individually_citable = true

[explanation]
separate_editorial_why_field_required = false
explanation_carried_by = [
  "claim identifiers",
  "outcomes",
  "findings",
  "evidence",
]
''',
    )

    write_if_missing(
        verification_dir / "aggregation.toml",
        '''schema = "ar-verification-aggregation-1"

[summary]
aggregates_by = [
  "claim shape",
  "level",
  "overall",
]

severity_order = [
  "fail",
  "partial",
  "cannot-verify",
  "pass",
]

[achieved_level]
description = """
The achieved level is the highest level such that every mandatory AR claim for
that level and all lower levels produced pass.
"""

[profile_rules]
profiles_may_define_acceptance_rules_for_profile_specific_claims = true
profiles_do_not_redefine_ar_achieved_level_semantics = true
''',
    )

    write_if_missing(
        verification_dir / "verifier-identity.toml",
        '''schema = "ar-verifier-identity-1"

[required_fields]
fields = [
  "id",
  "version",
]

[recommended_fields]
fields = [
  "implementation_url",
]

[compatibility]
same_inputs_should_produce_same_claim_outcomes = true
allowed_differences = [
  "timestamps",
  "formatting",
  "diagnostic wording",
  "implementation-specific metadata",
]
''',
    )


def package_manifest(package_id: str, package_data: dict[str, object]) -> str:
    """Generate the content of a package manifest file based on the provided package data."""
    label = str(package_data["label"])
    description = str(package_data["description"])
    elements = package_data["elements"]

    element_lines = "\n".join(f'  "{element}",' for element in elements)

    return f'''schema = "ar-element-package-1"

[identity]
canonical_uri = "https://structural-explainability.org/accountable-record/packages/{package_id}"
persistent_id = "urn:ar:se:accountable-record:packages:{package_id}"
compact_id = "se.accountable-record.packages.{package_id}"
local_name = "{package_id}"
label = "{label}"

[namespace]
authority = "structural-explainability.org"
authority_alias = "se"
project = "accountable-record"

[release]
version = "0.1.0"
status = "working-draft"
immutable = false

[definition]
description = """
{description}
"""
plain_language = """
A reusable package of related Accountable Record elements.
"""

[composition]
element_types = [
{element_lines}
]

[dependencies]
packages = []
element_types = []

[fixtures]
directory = "fixtures/"

[expected_reports]
directory = "expected-reports/"

[compatibility]
breaking_changes_require_new_major = true

[deprecation]
deprecated = false
successor = ""

[stewardship]
maintainer = "Structural Explainability"
status = "active"
'''


def scaffold_packages() -> None:
    """Scaffold the package files, which define the reusable packages of accountable record elements and their associated metadata, fixtures, expected reports, and dependencies."""
    packages_dir = ROOT / "data" / "packages"

    package_ids = "\n".join(f'  "{package_id}",' for package_id in PACKAGES)

    write_if_missing(
        packages_dir / "index.toml",
        f'''schema = "ar-element-package-index-1"

packages = [
{package_ids}
]
''',
    )

    for package_id, package_data in PACKAGES.items():
        package_dir = packages_dir / package_id
        write_if_missing(
            package_dir / "package.toml",
            package_manifest(package_id, package_data),
        )
        write_if_missing(package_dir / "fixtures" / ".gitkeep", "")
        write_if_missing(package_dir / "expected-reports" / ".gitkeep", "")


def scaffold_claims() -> None:
    """Scaffold the claim files, which define the claim shapes and core claim set for the accountable record ecosystem."""
    write_if_missing(
        ROOT / "data" / "claims" / "shapes.toml", 'schema = "ar-claim-shapes-1"\n'
    )
    write_if_missing(
        ROOT / "data" / "claims" / "core-claim-set.toml",
        'schema = "ar-core-claim-set-1"\n',
    )


def scaffold_failure_modes() -> None:
    """Scaffold the failure mode files, which define the known failure modes that arise from accountable record structural collapses, their detection sources, and their remediations."""
    failure_modes_dir = ROOT / "data" / "failure-modes"

    write_if_missing(
        failure_modes_dir / "index.toml",
        '''schema = "ar-failure-modes-index-1"

patterns = "data/failure-modes/patterns.toml"
detection = "data/failure-modes/detection.toml"
remediation = "data/failure-modes/remediation.toml"
profile_additions = "data/failure-modes/profile-additions.toml"
''',
    )

    pattern_entries = []
    for pattern in FAILURE_MODE_PATTERNS:
        pattern_entries.append(
            f'''[[patterns]]
id = "{pattern["id"]}"
label = "{pattern["label"]}"
status = "working-draft"
collapse = """
{pattern["collapse"]}
"""
'''
        )

    write_if_missing(
        failure_modes_dir / "patterns.toml",
        'schema = "ar-failure-mode-patterns-1"\n\n'
        + "\n".join(pattern_entries)
        + '''
[semantics]
failure_modes_are_not_exhaustive = true
failure_modes_are_structural = true
failure_modes_are_detected_by_claims_traits_or_profile_rules = true
description = """
A failure mode describes a structural collapse: a record fuses things that AR
requires to remain separable for inspection, verification, transformation, or
comparison.
"""
''',
    )

    write_if_missing(
        failure_modes_dir / "detection.toml",
        '''schema = "ar-failure-mode-detection-1"

[semantics]
detected_by = [
  "claims",
  "traits",
  "field mappings",
  "subject mappings",
  "transformation checks",
  "conformance checks",
  "profile rules",
]

[detection_boundary]
description = """
A detector reports a structural failure or risk. It does not decide truth,
authority, legitimacy, obligation, enforcement, or final domain meaning.
"""

[[detections]]
failure_mode = "source-vs-interpretation"
detection_sources = [
  "source traceability checks",
  "observation non-authority traits",
  "interpretation non-mutation checks",
]

[[detections]]
failure_mode = "name-vs-identity"
detection_sources = [
  "stable identifier checks",
  "subject identity checks",
  "identity-preserving transformation checks",
]

[[detections]]
failure_mode = "content-vs-status"
detection_sources = [
  "content/status separation traits",
  "status history checks",
  "interpretation non-mutation checks",
]

[[detections]]
failure_mode = "event-vs-record"
detection_sources = [
  "subject mapping checks",
  "transformation admissibility checks",
  "record correction lineage checks",
]

[[detections]]
failure_mode = "provenance-vs-authority"
detection_sources = [
  "authority non-assertion traits",
  "provenance traceability checks",
  "claim outcome checks",
]

[[detections]]
failure_mode = "context-vs-claim"
detection_sources = [
  "scope declaration traits",
  "context subject mappings",
  "claim outcome vocabulary checks",
]
''',
    )

    write_if_missing(
        failure_modes_dir / "remediation.toml",
        '''schema = "ar-failure-mode-remediation-1"

[semantics]
remediation_is_guidance = true
remediation_does_not_rewrite_records = true
remediation_may_require_profile_rules = true

[[remediations]]
failure_mode = "source-vs-interpretation"
guidance = """
Keep source-bearing fields faithful to source material. Express interpretation
in separate records, profile-specific interpretive records, or cross-referenced
claims.
"""

[[remediations]]
failure_mode = "name-vs-identity"
guidance = """
Use stable identifiers for records and subjects. Treat names, titles,
addresses, and labels as mutable fields rather than identifiers.
"""

[[remediations]]
failure_mode = "content-vs-status"
guidance = """
Keep content separable from status. Express repeal, supersession, limitation,
or current status as separate status structure or linked records.
"""

[[remediations]]
failure_mode = "event-vs-record"
guidance = """
Treat the event and the record describing the event as distinct. Corrections,
additions, and reinterpretations should be new records or declared
transformations.
"""

[[remediations]]
failure_mode = "provenance-vs-authority"
guidance = """
Record provenance as information about how the record came to be. Treat
authority as a separate interpretive or profile-specific claim.
"""

[[remediations]]
failure_mode = "context-vs-claim"
guidance = """
Keep context separate and citable. Claims may cite context; they should not
absorb it in a way that makes the claim appear stronger than it is.
"""
''',
    )

    write_if_missing(
        failure_modes_dir / "profile-additions.toml",
        '''schema = "ar-profile-failure-mode-additions-1"

[semantics]
profiles_may_define_additional_failure_modes = true
profile_failure_modes_compose_with_ar_failure_modes = true
profile_failure_modes_must_identify_detection_sources = true
profile_failure_modes_should_include_remediation = true

[required_structure]
fields = [
  "id",
  "label",
  "collapse",
  "where_it_shows_up",
  "detected_by",
  "remediation",
]

[boundary]
description = """
Profile-defined failure modes may name domain-specific collapses. They compose
with AR failure modes and must not redefine AR conformance semantics.
"""
''',
    )


def scaffold_traits() -> None:
    """Scaffold the trait files, which define the trait shapes and core trait library for the accountable record ecosystem."""
    traits_dir = ROOT / "data" / "traits"

    write_if_missing(
        traits_dir / "index.toml",
        '''schema = "ar-trait-library-index-1"

source = "data/traits/library.toml"
''',
    )

    trait_entries = []
    for trait in TRAIT_LIBRARY:
        applies_to_lines = "\n".join(f'  "{item}",' for item in trait["applies_to"])
        trait_entries.append(
            f'''[[traits]]
legacy_id = "{trait["legacy_id"]}"
compact_id = "{trait["compact_id"]}"
label = "{trait["label"]}"
status = "working-draft"
applies_to = [
{applies_to_lines}
]
'''
        )

    write_if_missing(
        traits_dir / "library.toml",
        'schema = "ar-trait-library-1"\n\n' + "\n".join(trait_entries),
    )

    write_if_missing(
        traits_dir / "declarations.toml",
        '''schema = "ar-trait-declarations-1"

# Trait declarations belong to profiles or record-type declarations.
# They do not belong to individual records.
''',
    )


def scaffold_transformations() -> None:
    """Scaffold the transformation files, which define the transformation behaviors, claim semantics, admissibility rules, and profile responsibilities for the accountable record ecosystem."""
    transformations_dir = ROOT / "data" / "transformations"

    write_if_missing(
        transformations_dir / "index.toml",
        '''schema = "ar-transformations-index-1"

behaviors = "data/transformations/behaviors.toml"
declarations = "data/transformations/declarations.toml"
admissibility = "data/transformations/admissibility.toml"
lineage = "data/transformations/lineage.toml"
profile_responsibilities = "data/transformations/profile-responsibilities.toml"
''',
    )

    behavior_entries = []
    for behavior in TRANSFORMATION_BEHAVIORS:
        behavior_entries.append(
            f'''[[behaviors]]
id = "{behavior["id"]}"
label = "{behavior["label"]}"
description = """
{behavior["description"]}
"""
'''
        )

    write_if_missing(
        transformations_dir / "behaviors.toml",
        'schema = "ar-transformation-behaviors-1"\n\n'
        + "\n".join(behavior_entries)
        + '''
[semantics]
closed_vocabulary = true
profiles_may_not_add_ar_behaviors = true
profiles_may_define_transformation_kinds = true
behavior_is_ar_defined = true
kind_is_profile_defined = true
''',
    )

    write_if_missing(
        transformations_dir / "declarations.toml",
        '''schema = "ar-transformation-declarations-1"

[semantics]
declaration_scope = "bundle"
not_part_of_single_source_or_target_record = true
records_describe_subjects = true
transformations_describe_declared_relationships_between_records = true

[required_fields]
fields = [
  "source_record_id",
  "target_record_id",
  "transformation_kind",
  "behavior",
]

[optional_fields]
fields = [
  "evidence",
  "lineage",
  "profile_context",
  "subject_mapping",
]

[field_semantics.transformation_kind]
profile_defined = true
description = """
The transformation kind is defined by the profile or package that selects the
transformation vocabulary.
"""

[field_semantics.behavior]
ar_defined = true
allowed_values = [
  "identity-preserving",
  "identity-breaking",
  "identity-inheriting",
  "no-identity-question",
]
description = """
The transformation behavior is selected from the closed AR transformation
behavior vocabulary.
"""
''',
    )

    write_if_missing(
        transformations_dir / "admissibility.toml",
        '''schema = "ar-transformation-admissibility-1"

[semantics]
admissibility_is_subject_mapping_sensitive = true
admissibility_is_profile_sensitive = true
admissibility_is_not_validity_proof = true
description = """
Admissibility states whether a claimed behavior is possible for the declared
subject structure and mapping context. It does not prove that a specific
transformation is valid.
"""

[inputs]
fields = [
  "source_record_id",
  "target_record_id",
  "source_subject_kind",
  "target_subject_kind",
  "subject_mapping",
  "transformation_kind",
  "claimed_behavior",
  "profile",
]

[default_policy]
unknown_subject_mapping = "cannot-verify"
unknown_transformation_kind = "cannot-verify"
inadmissible_behavior = "fail"

[profile_rules]
profiles_may_constrain_admissibility = true
profiles_may_not_redefine_ar_behaviors = true
profiles_may_not_claim_behavior_outside_ar_vocabulary = true
''',
    )

    write_if_missing(
        transformations_dir / "lineage.toml",
        '''schema = "ar-transformation-lineage-1"

[semantics]
required_for_identity_inheriting = true
description = """
Identity-inheriting transformations preserve accountability lineage from the
source subject to the successor subject.
"""

[required_for_identity_inheriting]
fields = [
  "source_record_id",
  "target_record_id",
  "lineage_relation",
]

[reference_behavior]
profile_may_permit_successor_resolution = true
silent_redirect_without_declared_lineage_forbidden = true

[boundary]
description = """
Lineage records successor accountability. It does not make the source and
target the same subject.
"""
''',
    )

    responsibility_lines = "\n".join(
        f'  "{item}",' for item in TRANSFORMATION_PROFILE_RESPONSIBILITIES
    )

    write_if_missing(
        transformations_dir / "profile-responsibilities.toml",
        f'''schema = "ar-transformation-profile-responsibilities-1"

responsibilities = [
{responsibility_lines}
]

[constraints]
profiles_may_define_domain_specific_transformation_kinds = true
profiles_may_not_redefine_ar_transformation_behaviors = true
profiles_may_not_violate_admissibility_rules = true
profiles_may_add_evidence_requirements = true
''',
    )


def scaffold_governance() -> None:
    """Scaffold the governance files, which define the scope, boundaries, and non-goals for the accountable record ecosystem, as well as the governance process for making changes to the AR contract and ecosystem."""
    governance_dir = ROOT / "data" / "governance"

    write_if_missing(
        governance_dir / "index.toml",
        '''schema = "ar-governance-index-1"

scope = "data/governance/scope.toml"
non_goals = "data/governance/non-goals.toml"
boundaries = "data/governance/boundaries.toml"
''',
    )

    write_if_missing(
        governance_dir / "scope.toml",
        '''schema = "ar-scope-1"

[purpose]
description = """
Accountable Record is a language-neutral contract for information systems
that must remain usable under persistent disagreement.
"""

[contract_defines]
items = [
  "record structure requirements",
  "exported artifact types",
  "verification artifacts",
  "conformance semantics",
  "subject structure",
  "subject mappings",
  "traits",
  "claims",
  "transformation behavior",
  "maturity levels",
  "field mappings",
  "failure modes",
]

[preservation_goals]
items = [
  "inspection",
  "contestation",
  "audit",
  "correction",
  "reinterpretation",
  "comparison",
  "reuse over time",
]

[applicability]
description = """
AR applies when records may be questioned later and the system must preserve
what was recorded, where it came from, what it refers to, how it changed, and
what interpretation was added.
"""

[domain_examples]
examples = [
  "legal records",
  "civic and institutional records",
  "scientific or technical records",
  "energy and infrastructure records",
  "procurement and contract records",
  "public data records",
  "standards and compliance records",
  "audit or oversight records",
]

[boundary_rule]
question = """
Does this system need records that remain inspectable, contestable, auditable,
correctable, and reusable even when people disagree about what the records
mean?
"""
if_yes = "AR may apply."
if_no = "Ordinary schema validation may be enough."

[standards_integration]
description = """
AR is designed to work with existing standards through mappings and profiles.
It does not replace existing standards.
"""
may_be_mapped_to_or_used_alongside = [
  "JSON Schema",
  "RDF",
  "OWL",
  "SHACL",
  "PROV-O",
  "DCAT",
  "legal citation standards",
  "archival standards",
  "domain-specific schemas and ontologies",
]
''',
    )

    boundary_entries = []
    for boundary in GOVERNANCE_BOUNDARIES:
        boundary_entries.append(
            f'''[[boundaries]]
id = "{boundary["id"]}"
label = "{boundary["label"]}"
description = """
{boundary["description"]}
"""
'''
        )

    write_if_missing(
        governance_dir / "boundaries.toml",
        'schema = "ar-governance-boundaries-1"\n\n'
        + "\n".join(boundary_entries)
        + '''
[semantics]
boundaries_are_contractual = true
boundaries_preserve_ar_neutrality = true
description = """
Governance boundaries define what AR does not decide or provide. They keep AR
focused on inspectable record structure rather than domain adjudication or
operational deployment.
"""
''',
    )

    write_if_missing(
        governance_dir / "non-goals.toml",
        '''schema = "ar-non-goals-1"

[semantics]
non_goals_are_contract_boundaries = true
non_goals_do_not_prevent_external_layers = true
description = """
AR non-goals identify responsibilities intentionally left outside the AR
contract. Operational systems, domain profiles, institutions, or external
layers may provide these capabilities, but AR does not require or define them.
"""

[out_of_scope]
items = [
  "domain truth",
  "domain correctness",
  "legal authority",
  "institutional legitimacy",
  "obligation enforcement",
  "causal explanation",
  "epistemic evaluation",
  "analytics",
  "optimization",
  "recommendation",
  "database design",
  "APIs",
  "authentication",
  "authorization",
  "access control",
  "cryptographic attestation",
  "operational deployment",
]

[layering]
description = """
Out-of-scope capabilities may be layered around AR. A system may use AR
exports while also providing databases, APIs, access control, cryptographic
attestation, workflow, analytics, or domain adjudication outside the AR
contract.
"""
''',
    )


def scaffold_adoption() -> None:
    """Scaffold the adoption files, which define the guidance for adopting AR, including when to use AR, readiness questions, and the maturity path."""
    adoption_dir = ROOT / "data" / "adoption"

    write_if_missing(
        adoption_dir / "index.toml",
        '''schema = "ar-adoption-index-1"

when_to_use_ar = "data/adoption/when-to-use-ar.toml"
readiness_questions = "data/adoption/readiness-questions.toml"
maturity_path = "data/adoption/maturity-path.toml"
''',
    )

    fit_entries = []
    for signal in ADOPTION_FIT_SIGNALS:
        fit_entries.append(
            f'''[[good_fit_signals]]
id = "{signal["id"]}"
label = "{signal["label"]}"
description = """
{signal["description"]}
"""
'''
        )

    poor_fit_entries = []
    for signal in ADOPTION_POOR_FIT_SIGNALS:
        poor_fit_entries.append(
            f'''[[poor_fit_signals]]
id = "{signal["id"]}"
label = "{signal["label"]}"
description = """
{signal["description"]}
"""
'''
        )

    write_if_missing(
        adoption_dir / "when-to-use-ar.toml",
        'schema = "ar-when-to-use-ar-1"\n\n'
        + "\n".join(fit_entries)
        + "\n"
        + "\n".join(poor_fit_entries)
        + '''
[central_question]
question = """
Does this system need records that remain inspectable, contestable, auditable,
correctable, and reusable even when people disagree about what the records
mean?
"""
if_yes = "AR may apply."
if_no = "AR may be more structure than the system needs."

[adoption_boundary]
description = """
AR is best suited for domains where persistent disagreement, source
traceability, subject mapping, verification, and export accountability matter.
It is not a workflow platform or a replacement for ordinary schema validation.
"""
''',
    )

    question_entries = []
    for question in READINESS_QUESTIONS:
        question_entries.append(
            f'''[[questions]]
id = "{question["id"]}"
question = """
{question["question"]}
"""
'''
        )

    write_if_missing(
        adoption_dir / "readiness-questions.toml",
        'schema = "ar-readiness-questions-1"\n\n'
        + "\n".join(question_entries)
        + '''
[interpretation]
description = """
The readiness questions help a team decide whether AR is a good fit and which
maturity level to target first. They are adoption guidance, not conformance
claims.
"""
''',
    )

    write_if_missing(
        adoption_dir / "maturity-path.toml",
        '''schema = "ar-adoption-maturity-path-1"

[semantics]
maturity_is_incremental = true
later_levels_extend_earlier_levels = true
later_levels_do_not_replace_earlier_levels = true

[[steps]]
level = "level-0"
label = "Bundle Shape"
starting_point = true
description = """
Start by exporting a valid AR bundle shape.
"""

[[steps]]
level = "level-1"
label = "Source Traceability"
description = """
Add source references and provenance links sufficient for inspection.
"""

[[steps]]
level = "level-2"
label = "Subject Structure"
description = """
Declare subject structure and subject mappings for relevant record types.
"""

[[steps]]
level = "level-3"
label = "Trait Declarations"
description = """
Declare traits and field mappings needed for trait conformance.
"""

[[steps]]
level = "level-4"
label = "Transformation-Aware Verification"
description = """
Declare transformations and verify their behavior under the selected profile.
"""

[[steps]]
level = "level-5"
label = "Domain Profile Conformance"
description = """
Satisfy a declared domain profile.
"""
''',
    )


def main() -> None:
    """Main function to scaffold the repository."""
    # root/index
    scaffold_root_files()
    scaffold_data_index()

    # vocabulary/namespace/contracts
    scaffold_vocabulary()
    scaffold_namespace()
    scaffold_contracts()
    scaffold_governance()
    scaffold_adoption()

    # component groups/elements
    scaffold_component_groups()
    scaffold_elements()

    # domain source data
    scaffold_claims()
    scaffold_traits()
    scaffold_conformance()
    scaffold_verification()
    scaffold_export_contract()
    scaffold_mappings()
    scaffold_subject_mappings()
    scaffold_transformations()
    scaffold_failure_modes()
    scaffold_records()

    # composes known element/package/export concepts
    scaffold_packages()

    # schemas/generated export dirs/catalogs
    scaffold_schemas()
    scaffold_exports()
    scaffold_catalog_and_locks()

    # Python/docs/tests
    scaffold_python_package()
    scaffold_docs()
    scaffold_tests_and_tools()

    print("Scaffold complete. Existing files were not overwritten.")


if __name__ == "__main__":
    main()
