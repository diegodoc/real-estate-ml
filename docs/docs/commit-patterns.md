# Commit Message Patterns

This repository follows a commit convention to keep history organized and standardized. Below are the accepted commit types:

## Commit Structure
Each commit must follow this format:

```
<type>: <brief description in the present tense>

<optional message explaining more details>
```

Example:
```
feat: add file upload functionality

Implements file upload functionality in the API using Django and S3.
```

## Commit Types

| Type       | Description |
|------------|------------|
| **feat**   | Adds a new feature |
| **fix**    | Fixes a bug |
| **docs**   | Documentation changes only |
| **style**  | Changes that don't affect code meaning (spacing, formatting, etc.) |
| **refactor** | Code refactoring without functionality changes |
| **perf**   | Performance improvements |
| **test**   | Adds or modifies tests |
| **build**  | Changes to build configuration or dependencies |
| **ci**     | CI/CD pipeline adjustments |
| **revert** | Reverts a previous commit |
| **other**  | Other changes that don't fit in the above categories |

## Commit Message Examples

- `feat: implement JWT authentication`
- `fix: correct validation error in registration`
- `docs: add installation instructions to README`
- `style: adjust code indentation`
- `refactor: improve serializers organization`
- `perf: optimize user listing query`
- `test: add tests for login API`
- `build: add Docker support`
- `revert: revert previous commit that broke the application`
- `other: update log messages`

