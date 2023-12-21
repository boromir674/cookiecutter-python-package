# Snapshots of Generator Output for Regression Testing

We maintain 2 `Biskotaki` Projects, Generated with input `User Config`, 
the [./.github/biskotaki.yaml](../../../.github/biskotaki.yaml) file.

Since, `rendering` is involved in the `Generation`, we call them `Snapshots`

- [biskotaki-no-input](./biskotaki-no-input/) Generated with `Interactive mode` OFF
- [biskotaki-interactive](./biskotaki-interactive/) Generated with `Interactive mode` ON

They should correspond to what gets `rendered`, using the latest `Generator`.

They should both correspond to output produced using using the **latest** version of `Generator` (ie latest python distribution release on PyPI).


## Maintaining the Snapshots

### Snapshot `biskotaki-no-input` -> Interactive Mode OFF

1. **Automatically Update Test Snapshot:**
    
    Optionally, first make sure env is OK: `tox -e dev -vv --notest`
    ```shell
    ./scripts/update-snapshot.sh
    ```
2. **Git Add:**
    ```shell
    git add tests/data/snapshots/biskotaki-no-input
    ```
3. **Git Commit:**
    ```shell
    git commit -m "tests(data): update biskotaki-no-input Snapshot, used for Regression Testing"
    ```

### Snapshot `biskotaki-interactive` -> Interactive Mode OFF

**TLDR**: copy-paste below into terminal prompt:
{"supported-interpreters": ["3.6", "3.7", "3.8", "3.9", "3.10"]}

when prompted with `interpreters [default]:`


1. **Interactively Generate Biskotaki and automatically Update Test Snapshot:**
    
    Optionally, first make sure env is OK: `tox -e dev -vv --notest`
    ```shell
    ./scripts/update-snapshot-interactive.sh
    ```
    When prompted with `interpreters [default]:`  
    Paste:  
    ```shell
        {"supported-interpreters": ["3.6", "3.7", "3.8", "3.9", "3.10"]}
    ```
2. **Git Add:**
    ```shell
    git add tests/data/snapshots/biskotaki-interactive
    ```
3. **Git Commit:**
    ```shell
    git commit -m "tests(data): update biskotaki-interactive Snapshot, used for Regression Testing"
    ```
