# Field Mapping Guide

Field mappings connect local data fields to AR structural roles.

Authoritative mapping source data lives in:

```text
data/mappings/
```

## Purpose

A system can keep its local field names while declaring how those fields support
AR traits, claims, reports, and profile checks.

Field mappings are useful when a verifier needs to know which local field
supplies a required AR role.

## Support

Field mappings may support:

- trait conformance;
- claim checks;
- evidence lookup;
- report generation;
- profile-specific validation;
- compatibility fixtures;
- expected reports.

## Mapping is not Replacement

AR does not require a system to rename its local fields.

It requires the relationship between local fields and AR roles to be explicit
when those fields are used for verification.

## Boundary

A field mapping says how a local field is used structurally.

It does not decide whether the field value is true, authoritative, complete, or
legally effective.
