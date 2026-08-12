# Developer Review

Status: Approved for execution by explicit user instruction.

The safe approach is a mechanical promotion of the 11 hash-pinned v162 files
into the package root, followed by removal of the duplicate source snapshot.
The checksum manifest remains as provenance and is rewritten to point at the
canonical files. Tests must be changed only where they assert the superseded
source shape; production code must not be altered merely to satisfy old tests.

Primary risks are line-ending drift, tests coupled to exact source strings, and
accidentally including runtime configuration. Byte hashes and focused staging
control address these risks.
