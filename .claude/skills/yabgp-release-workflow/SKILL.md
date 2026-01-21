---
name: yabgp-release-workflow
description: This document defines the development, version management, and release workflow for the yabgp project. All contributors and maintainers must adhere to these guidelines.
---

# YABGP Development Workflow and Versioning Standards

## Core Principles

1.  **Branch Management**:
    *   `master`: Main development branch, always contains the latest development code.
    *   `stable/X.Y.x`: Stable release branch, used for maintaining released versions (e.g., `stable/0.9.x`).
2.  **Versioning Standards**:
    *   Follows [PEP 440](https://packaging.pythonlang.cn/en/latest/specifications/version-specifiers/#) standards.
    *   Version number is defined in the `yabgp/__init__.py` file.

---

## Detailed Workflow

### I. Development Phase

*   **Current Status**: Working on the next feature release (e.g., `0.9.0`).
*   **Version Number**: The version on the `master` branch should have a `.dev0` suffix (e.g., `0.9.0.dev0`).
*   **Workflow**:
    1.  Developer forks the project to their personal repository.
    2.  Create a feature branch based on `master`.
    3.  After development is complete, submit a Pull Request (PR) to the `master` branch of `smartbgp/yabgp`.
    4.  Merge after review approval.

### II. Testing Phase

*   **Trigger**: Feature development is basically complete, ready for the code freeze and testing period.
*   **Workflow**:
    1.  **Tagging**: After code merge, create a TAG on the corresponding commit in the `master` branch (e.g., `v0.9.0a1`).
    2.  **Iteration**: If bugs are found, fix them and repeat the above step, incrementing the suffix (e.g., `0.9.0a2`, `0.9.0a3`, etc.).

### III. Release Phase

*   **Trigger**: Testing passed, ready to release the official version.
*   **Workflow**:
    1.  **Lock Version**: Maintainer submits a PR to change `yabgp/__init__.py` to the official version number (remove suffix, e.g., `0.9.0`).
    2.  **Merge and Branch**: After the PR is merged into `master`:
        *   Create a new stable branch based on this commit: `stable/0.9.x`.
        *   Create an official TAG on the `stable/0.9.x` branch: `v0.9.0`.
    3.  **Start Next Cycle**: Submit a new PR on the `master` branch to update the version number to the next development version (e.g., `0.10.0.dev0`) to distinguish released code from new development code.

### IV. Maintenance Phase (Hotfix)

*   **Scenario**: A serious bug is found in a released version (e.g., `0.9.0`).
*   **Workflow**:
    1.  Submit fix code on the `stable/0.9.x` branch.
    2.  Update the version number on `stable/0.9.x` to `0.9.1`.
    3.  Create TAG `v0.9.1` and release.
    4.  **Important**: Cherry-pick or merge the fix code back to the `master` branch (if `master` also has this bug).

---

### Version Lifecycle Table

| Phase | Branch | `__version__` | TAG | Action |
|---|---|---|---|---|
| Development | `master` | `0.9.0.dev0` | - | Developer fork → Develop → PR → Merge |
| Testing | `master` | `0.9.0.dev0` | `0.9.0a1`, `0.9.0a2` | Create TAG on stable commit |
| Release | `master` | `0.9.0` | - | Remove `.dev0`, Merge PR |
| Release | `stable/0.9.x` | `0.9.0` | `0.9.0` | Create stable branch, create official TAG |
| Next Version | `master` | `0.10.0.dev0` | - | Update version to next dev version |

---

### Flowchart

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         YABGP Release Workflow                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  master branch                                                              │
│  ═══════════════════════════════════════════════════════════════════════►  │
│  │         │         │         │         │         │                       │
│  │ 0.9.0   │ feat A  │ feat B  │ bugfix  │ 0.9.0   │ 0.10.0               │
│  │ .dev0   │         │         │         │ (remove │ .dev0                │
│  │         │         │         │         │  dev0)  │                       │
│  │         │         ▼         ▼         │         │                       │
│  │         │     TAG:0.9.0a1  TAG:0.9.0a2│         │                       │
│  │         │                             │         │                       │
│  │         │                             ▼         │                       │
│  │         │                    ┌────────┴────────┐│                       │
│  │         │                    │ stable/0.9.x    ││                       │
│  │         │                    │ ════════════►   ││                       │
│  │         │                    │       │         ││                       │
│  │         │                    │   TAG:0.9.0     ││                       │
│  │         │                    └─────────────────┘│                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Version Number Quick Reference

### Patch Release

```
Development:  0.9.1.dev0
Testing:      TAG 0.9.1a1, 0.9.1a2
Release:      Branch stable/0.9.x, TAG 0.9.1
```

### Minor Release

```
Development:  0.10.0.dev0
Testing:      TAG 0.10.0a1, 0.10.0a2
Release:      Branch stable/0.10.x, TAG 0.10.0
```

## Checklist

### Before Developer Submits PR

- [ ] Code is based on the latest `master` branch
- [ ] Local tests passed
- [ ] Version number not modified

### Before Maintainer Creates Test TAG

- [ ] Code is based on the latest `master` branch
- [ ] TAG name follows standards (e.g., `0.9.0a1`)

### Before Maintainer Releases Official Version

- [ ] Version number updated from `.dev0` to official version
- [ ] `stable/X.Y.x` branch created
- [ ] Official TAG created on `stable/X.Y.x` branch
- [ ] `master` branch version updated to next development version

## References

- [PEP 440 - Version Identification and Dependency Specification](https://peps.python.org/pep-0440/)
- [Python Packaging User Guide - Version Specifiers](https://packaging.python.org/en/latest/specifications/version-specifiers/)
- [Semantic Versioning 2.0.0](https://semver.org/)
