# QA Review

Status: Approved for execution by explicit user instruction.

Validation requires byte comparison against `deployment/SHA256SUMS-v162.txt`,
JavaScript syntax checking, compilation of promoted Python files, and the full
package regression suite. Any failed test must be classified as either a real
v162 regression or an obsolete assertion before modification. The final Git
diff must contain no secrets or runtime data.
