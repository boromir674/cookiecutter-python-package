# Dependabot

## Tutorial: Setting Up Dependabot for Python Projects

**Goal**: Automate dependency updates to manage vulnerabilities and keep dependencies up-to-date.

1. **Step:** Enabling Dependabot in Your Repository

    Navigate to your GitHub repository.
    Go to the Settings tab, then find the Security & analysis section on the left sidebar.
    **Enable Dependabot alerts and Dependabot security updates.**

2. **Step:** Configuring Dependabot

    **Create** a **`.github/dependabot.yml`** file in your repository to customize Dependabot settings:
    
    ```yaml
    
    version: 2
    updates:
      - package-ecosystem: "pip" # Set the package ecosystem to Python's pip
        directory: "/" # Location of the Python project in the repository
        schedule:
          interval: "daily" # How often to check for updates
        open-pull-requests-limit: 10 # Maximum number of open pull requests
        ignore:
          - dependency-name: "express" # Example of ignoring a dependency
            versions: ["4.0.0"] # Specify versions to ignore
    ```
    ```yaml
    version: 2
    updates:
      # Configure Dependabot for Python projects
      - package-ecosystem: "pip" # For Python projects using pip
        directory: "/" # Root directory of the project
        schedule:
          interval: "daily" # How often to check for updates
          # You can adjust the interval as needed (e.g., "weekly").
        open-pull-requests-limit: 10 # Limits the number of open pull requests
        # Prioritize security updates by setting them to open immediately
        security-updates: "auto" 
        # Enable version updates for all dependencies
        versioning-strategy: "increase" # Can be "lockfile-only", "increase", or "widen"
        # Example to ignore certain dependencies (commented out)
        # ignore:
        #   - dependency-name: "example-dependency"
        #     versions: ["1.0.0"]
        # This section is customizable and allows you to ignore specific dependencies or versions.
        # It's commented out for now, as per the instructions.
    ```

    Adjust package-ecosystem, directory, and schedule.interval as necessary for your project. The ignore field is optional.

3. **Step:** Merging Pull Requests

    Dependabot will create pull requests for dependency updates. Review and merge these PRs to keep your project up-to-date.

## How-to Guide: Advanced Dependabot Configuration

Scenario: Customize Dependabot to ignore specific versions or prioritize security updates.

Ignoring Dependencies: To ignore specific dependencies or versions, use the ignore field in your dependabot.yml.

Prioritizing Security Updates: Dependabot automatically prioritizes security updates. Ensure Dependabot security updates are enabled in the repository settings.

## Explanation: Understanding Dependabot's Value

Dependabot helps maintain project health by ensuring dependencies are up-to-date and secure.  
It reduces the manual effort of tracking vulnerabilities and dependency updates.  
Dependabot's integration into GitHub's ecosystem seamlessly enhances project security and dependency management.

## Reference: Dependabot Configuration Options

- version: The version of the configuration file format (currently 2).
- updates: A list of update configurations.
- package-ecosystem: The package manager to use (pip for Python).
- directory: The directory where dependency files are located.
- schedule.interval: How often to check for updates (daily, weekly, or monthly).
- open-pull-requests-limit: The maximum number of open pull requests for dependency updates.
- ignore: A list of dependencies to ignore.

For the complete Dependabot configuration options, refer to the GitHub documentation on Dependabot.
