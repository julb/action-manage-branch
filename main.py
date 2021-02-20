#!/usr/bin/python3
import os
from github import Github


def main():
    """ The main method executed. """

    # Github  variables
    github_token = os.environ.get('GITHUB_TOKEN')
    github_repository = os.environ.get('GITHUB_REPOSITORY')
    github_sha = os.environ.get('GITHUB_SHA')

    # Input variables
    input_branch_name = os.environ.get('INPUT_NAME')
    input_branch_state = os.environ.get('INPUT_STATE', 'create')
    input_branch_from = os.environ.get('INPUT_FROM', '')

    # Post-process date-time.
    branch_name = input_branch_name
    branch_git_ref_name = f'refs/heads/{branch_name}'
    branch_state = input_branch_state
    branch_from = github_sha
    if input_branch_from != '':
        branch_from = input_branch_from

    # Get repository.
    github = Github(github_token)
    github_repo = github.get_repo(github_repository)

    # Check if already exists.
    existing_github_ref = None
    for github_ref in github_repo.get_git_refs():
        # Check if the target branch exists.
        if github_ref.ref.lower() == branch_git_ref_name.lower():
            existing_github_ref = github_ref

        # Determine if the source is a branch, a tag or a ref.
        if branch_from and github_ref.ref.lower() in (f'refs/heads/{branch_from}'.lower(), f'refs/tags/{branch_from}'.lower(), branch_from.lower()):
            branch_from = github_ref.object.sha

    # Manage state.
    if branch_state in ('create', 'present'):
        # Source sha.
        if not existing_github_ref:
            print('::debug::Creating the branch.')
            existing_github_ref = github_repo.create_git_ref(ref=branch_git_ref_name, sha=branch_from)
        else:
            print('::debug::Updating the branch with the given SHA.')
            existing_github_ref.edit(sha=branch_from, force=True)

        # Return milestone number.
        print(f'::set-output name=ref::{existing_github_ref.ref}')
        print(f'::set-output name=name::{branch_name}')
        print(f'::set-output name=sha::{existing_github_ref.object.sha}')
    elif branch_state in ('deleted', 'absent'):
        # Delete if repo exists.
        if existing_github_ref is not None:
            print('::debug::Deleting the branch.')
            existing_github_ref.delete()
        else:
            print('::debug::Skipping branch deletion as it does not exist.')

        # Return 0 as number.
        print('::set-output name=ref::none')
        print('::set-output name=name::none')
        print('::set-output name=sha::none')


if __name__ == '__main__':
    main()
