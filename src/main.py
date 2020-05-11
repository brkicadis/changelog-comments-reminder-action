from lastversion import lastversion
import argparse
import sys
import git
import re


class Definition:
    CONFIG_FILE_PATH = 'CHANGELOG.md'
    SHOP_EXTENSION_PARTNER = 'brkicadis'


class ReleaseVersion:
    @staticmethod
    def get_last_released_version() -> str:
        """
        Returns last released version from GitHub tag
        :return: str
        """
        repository_name = sys.argv[1]
        repository_to_clone = Definition.SHOP_EXTENSION_PARTNER + "/" + repository_name
        return str(lastversion.latest(repository_to_clone, output_format='version', pre_ok=True))

    @staticmethod
    def get_current_release_version() -> str:
        """
        Returns current release version from branch name
        :return: str
        """
        repo = git.Repo(search_parent_directories=True)
        branch = repo.active_branch
        current_release_version = re.sub('[^\d\.]', '', branch.name)
        return current_release_version


class ChangelogReleaseNotes:
    @staticmethod
    def get_release_notes() -> dict:
        """
        Returns release notes from changelog file for a specific version
        :return: dict
        """
        release_notes = {}
        file_name = open(Definition.CONFIG_FILE_PATH, 'r')
        lines = file_name.readlines()
        is_found = False
        for index, line in enumerate(lines):
            if ReleaseVersion.get_last_released_version() in line:
                release_notes[ReleaseVersion.get_last_released_version()] = lines[index + 2].strip()

            if ReleaseVersion.get_current_release_version() in line:
                release_notes[ReleaseVersion.get_current_release_version()] = lines[index + 2].strip()
                is_found = True

        if is_found == False:
            print('Current release tag does not exists!', file=sys.stderr)
            sys.exit(1)

        return release_notes

    @staticmethod
    def validate_release_notes():
        current_release_notes, last_release_notes, *_ = ChangelogReleaseNotes.get_release_notes().values()
        if current_release_notes == '' or not current_release_notes.startswith('*'):
            print('Current release tag exists but the release notes are not added or in wrong format!', file=sys.stderr)
            sys.exit(1)

        if current_release_notes == last_release_notes:
            print('Current release tag exists but the release notes are the same as for the previous release!', file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Provide shop extension name as an argument.')
    parser.add_argument('repository', metavar='extension name', type=str, help='shop extension name e.g. woocommerce-ee')
    args = parser.parse_args()
    extension_name = args.repository
    release_notes_checker = ChangelogReleaseNotes
    release_notes_checker.validate_release_notes()
