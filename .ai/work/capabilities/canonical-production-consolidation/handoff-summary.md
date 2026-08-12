# Handoff Summary

The package root is now the only editable application source tree and is an
exact promotion of the captured production v162 source. The duplicate
`deployment/vm-production-v162/` tree is gone; its checksum manifest remains as
provenance. Development and future deployment work must use the package root.

The working production VM was intentionally untouched. Publishing this change
updates Git only and does not deploy it.
