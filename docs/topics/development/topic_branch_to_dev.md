# Board `dev` branch via PR

> Merge `Topic Branch` via **PR** into `Integration Branch`

## `How-to` Open PR to `dev`

Prerequisites:

- Your git HEAD is on the `Topic Branch`

!!! Tip
    
    Adjust the instructions, using Inputs for `Default` and `Integration` Branches

    <div class="grid cards" markdown>
            
    -   **`INPUT`** Default Branch (ie main)
    
        ---
    
        <input type="text" id="input-default-branch-name" placeholder="Default Branch name; ie main" oninput="updateReferencesToDefaultBranch()">
    
    
    -   **`INPUT`** Integration Branch (ie dev)
    
        ---
    
        <input type="text" id="input-integration-branch-name" placeholder="Integration Branch name; ie dev" oninput="updateReferencesToIntegrationBranch()">
    
    </div>

<div class="annotate" markdown>

<ol start="1">
    <li>Define Default and Integration Branches (1)

        <pre><code class="language-sh">
            <span id="set-default-branch-name">export MAIN_BR=...</span>
            <span id="set-integration-branch-name">export DEV_BR=...</span>
        </code></pre>
    </li>

    <li><b>Open PR</b> to Integration Branch

        ```sh
        git push && git checkout ${DEV_BR} && git pull && git checkout - && gh pr create --base ${DEV_BR}
        ```

    </li>
    <li>Enable <b>Auto Merge</b>

        ```sh
        gh pr merge --merge --auto
        ```
    </li>
</ol>

<script> function updateReferencesToDefaultBranch() { var inputDefaultBranchName = document.getElementById('input-default-branch-name').value; document.getElementById('set-default-branch-name').innerText = 'export MAIN_BR=' + inputDefaultBranchName; } </script>

<script> function updateReferencesToIntegrationBranch() { var inputIntegrationBranchName = document.getElementById('input-integration-branch-name').value; document.getElementById('set-integration-branch-name').innerText = 'export DEV_BR=' + inputIntegrationBranchName; } </script>

</div>

**Congratulations** :smile: !  

Now the **PR** shall auto-merge once all Required Checks Pass !

## Next Steps

Watch the **PR Validation** `Workflow` "live":
```sh
gh run watch
```
