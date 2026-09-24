# Call viewer design QA

Status: passed for this change.

Reference: user-supplied Photo 4 screenshot. Implementation reviewed in local browser: dark wide panel, blue/gray bilingual bubbles, satellite endpoint map, caller metadata and visible audio footer. Adapted the reference call list to the existing single-record viewer. Arabic uses automatic text direction. At 390px viewport the workspace measures 327px without internal horizontal overflow.

Interactions verified: PCM WAV playback advances, English translation toggle, Call 2 missing-media state. MP3 crashed the embedded browser; original file is retained and playback uses a WAV derivative. No line-level timing is claimed. No remaining P0-P2 findings in the changed viewer.
