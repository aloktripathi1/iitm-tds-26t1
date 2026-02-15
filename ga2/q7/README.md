# Q7 Solution: GitHub Action Cache

## Objective
Create a GitHub Actions workflow that uses caching with a specific key.

## Steps Taken

1.  **Workflow Creation**:
    -   Created `.github/workflows/caching.yml`.
    -   Used `actions/cache@v4`.
    -   Set cache path to `prime-numbers`.
    -   Set cache key to `cache-d18a326`.
    -   Added step `prime-cache-d18a326` to verify cache hits.

2.  **Repository Setup**:
    -   Initialized a new Git repository in `ga2/q7`.
    -   Added the remote: `https://github.com/aloktripathi1/q-github-action-cache`.

3.  **Deployment**:
    -   Configured git identity (aloktripathi1 / aloktripathe@gmail.com).
    -   Committed and pushed the workflow to the `main` branch.

4.  **Verification**:
    -   The workflow will run automatically on push.
    -   The first run will save the cache.
    -   Subsequent runs (if triggered) would restore the cache.
