![Build](https://github.com/julb/action-manage-branch/workflows/Build/badge.svg)

# GitHub Action to manage branches

The GitHub Action for managing branches of the GitHub repository.

- Create a new branch
- Move the branch to another commit
- Delete a branch

## Usage

### Example Workflow file

- Create a branch:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Create/Update the branch
        uses: julb/action-manage-branch@v1
        with:
          name: branch-name
          state: present
          from: ${{ github.ref }}
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- Delete a branch

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Delete the branch
        uses: julb/action-manage-branch@v1
        with:
          name: branch-name
          state: absent
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Inputs

| Name    | Type   | Default      | Description                                                                                                                                                 |
| ------- | ------ | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`  | string | `Not set`    | Name of the branch. **Required**                                                                                                                            |
| `state` | string | `present`    | Expected state of the branch. Valid values are `present` to create the branch or `absent` to delete the branch                                              |
| `from`  | string | `github.ref` | The reference from which to create or update the branch - could be a branch, a tag, a ref or a specific SHA. By default, it takes the commit that triggered the workflow. |

### Outputs

| Name   | Type   | Description                                                                       |
| ------ | ------ | --------------------------------------------------------------------------------- |
| `ref`  | string | Git ref of the branch `refs/heads/name`, or `none` in case the branch is deleted. |
| `name` | string | Name of the branch, or `none` in case the branch is deleted.                      |
| `sha`  | sha    | SHA Commit of the branch, or `none` in case the branch is deleted.                |

## Contributing

This project is totally open source and contributors are welcome.

When you submit a PR, please ensure that the python code is well formatted and linted.

```
$ make install.dependencies
$ make format
$ make lint
```
