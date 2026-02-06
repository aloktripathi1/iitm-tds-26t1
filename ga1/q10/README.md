

Task
----
replace all occurrences of the token `IITM` (any case) with `IIT Madras` across all files in a folder.

Approach
--------
- back up the folder before editing.
- preview matches with `grep` to see which files will change.
- use `sed` in-place with word-boundary and case-insensitive flags to replace only whole-token matches.
- verify no remaining matches and compute the concatenated sha256 as proof.

Commands
--------
make a backup:

```bash
cp -r q-replace q-replace-backup
```

preview matches:

```bash
grep -RIn --binary-files=without-match 'IITM' .
```

run safe in-place replace (creates `.bak` backups):

```bash
find . -type f -exec sed -i.bak 's/\bIITM\b/IIT Madras/Ig' {} +
```

verify there are no remaining matches:

```bash
grep -RIn --binary-files=without-match 'IITM' . || echo "no matches"
```

compute concatenated SHA-256 of all files (shell expansion order):

```bash
cat * | sha256sum
```

Solution
--------
The replacement command above performs the change safely and creates `.bak` backups for each file.

The concatenated SHA-256 result after running the commands in this folder was:

```
11df05e4415dec4fabe0e83f16d86a05bbbe8ca02136dd8a27150cc9216c91c5  -
```

Notes
-----
- test on a single file before mass-editing: `sed -n '1,200p' file.txt | sed 's/\bIITM\b/IIT Madras/Ig'`.
- keep `.bak` files until you have verified results; remove them with `find . -name '*.bak' -delete`.
- avoid tools that normalize line endings if preserving them is required.

