Privacy Policy (Demo)
=====================

This repository is a development scaffold for a local-only demo. It is not intended for production use.

Data Handling
-------------
- Uploaded files are stored locally under `data/uploads`.
- Extracted frames are stored locally under `data/frames/{job_id}`.
- Results may be written under `data/results`.
- MongoDB stores job metadata including filenames, type, timestamps, and inference outputs.

Retention and Deletion
----------------------
- Data persists until manually removed. Delete the `data/` directory and MongoDB collections for cleanup.

Security
--------
- No encryption at rest is provided in this scaffold.
- No authentication is implemented by default.
- Use only on trusted, local machines. Do not expose to the public internet.

Contact
-------
- For issues or questions, open a GitHub issue in your fork.
















