# Q3 Solution: Git Time Travel

## Objective
Find the parent commit of the commit that changed the `timeout` value to `420` in `config.json`.

## Steps Taken

1.  **Extraction**:
    -   Extracted `q-git-time-travel.zip` to `repo/`.

2.  **Investigation**:
    -   Navigated to the repository: `repo/q-git-time-travel`.
    -   Used `git log -p config.json` to inspect the history of the file.
    -   Alternatively, used `git log -S "420" -- config.json` to find the specific commit introducing the value.

3.  **Findings**:
    -   Found commit `e4d61aefa6bd93146e2d583dd04f6dd1faf672f8` which updated the timeout.
    -   Identified its parent commit: `22d0c7990364695bdc918ffec30101075b20b1ea`.

4.  **Result**:
    -   The short hash of the parent commit is **22d0c79**.
