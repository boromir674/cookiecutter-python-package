---
tags:
  - CICD
---

## CI/CD Pipeline

> Understand what Jobs are part of the CI/CD Pipeline

**CI/CD Pipeline** is implemented as `Github Actions Workflow` in a YAML file format.

### Workflow of Jobs: visualized as a Directed Acyclic Graph (DAG)

> Understand the Job Dependencies at "compile time"

**YAML Workflow: ./.github/workflows/cicd.yml**

{% raw %}{% include 'topics/development/cicd_mermaid.md' %}{% endraw %}

- `solid boxes` represent **Jobs** declared in the `jobs` array of the YAML Workflow
- `solid arrows` represent **Job Dependencies**; `job_A.needs: [job_b, job_c]` type of yaml objects


[//]: # (TODO add section to EXPLAIN the CI/CD Pipeline at runtime)

[//]: # (TODO make screenshot of CI Server run and paste here)

[//]: # (TODO add link to live CI server Pipeline RUNS)
