from lastversion import lastversion
import argparse
import sys
import git
import re
import itertools
from termcolor import colored


class Definition:
    # CONFIG_FILE_PATH = '/Users/adis.brkic/Desktop/woocommerce-ee/CHANGELOG.md'
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
    def get_current_release_notes() -> list:
        """
        Returns current release notes from CHANGELOG.md file for a specific release version
        :return: array
        """
        file_name = open(Definition.CONFIG_FILE_PATH, 'r')
        release_version = ReleaseVersion()

        current_release = list(itertools.takewhile(lambda x: '|' not in x, itertools.dropwhile(lambda x: release_version.get_current_release_version() not in x.strip(), file_name)))
        current_release_notes = list(filter(None, [item.strip() for item in current_release]))[1:]

        return current_release_notes

    @staticmethod
    def get_last_release_notes() -> list:
        """
        Returns last release notes from CHANGELOG.md file for a last released version
        :return: array
        """
        file_name = open(Definition.CONFIG_FILE_PATH, 'r')
        release_version = ReleaseVersion()

        last_release = list(itertools.takewhile(lambda x: '|' not in x, itertools.dropwhile(lambda x: release_version.get_last_released_version() not in x, file_name)))
        last_release_notes = list(filter(None, [item.strip() for item in last_release]))[1:]

        return last_release_notes

    @staticmethod
    def tag_exist():
        file_name = open(Definition.CONFIG_FILE_PATH, 'r')
        is_found = False
        release_version = ReleaseVersion()

        for file_line in file_name:
            if release_version.get_current_release_version() in file_line:
                is_found = True

        if is_found == False:
            print(colored('Current release tag does not exists!', 'red'), file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def release_notes_difference():
        changelog_release_notes = ChangelogReleaseNotes()
        if changelog_release_notes.get_current_release_notes() == changelog_release_notes.get_last_release_notes():
            print(colored('Current release tag exists, but the release notes are the same as for the previous release!!', 'red'), file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def release_notes_exist():
        changelog_release_notes = ChangelogReleaseNotes()
        if not changelog_release_notes.get_current_release_notes():
            print(colored('Current release tag exists, but the release notes are the empty!', 'red'), file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def release_notes_format():
        changelog_release_notes = ChangelogReleaseNotes()
        if not all(release_note.startswith('*') for release_note in changelog_release_notes.get_current_release_notes()):
            print(colored('Current release tag exists, the release notes exists, but the format is wrong!', 'red'), file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def validate_release_notes():
        changelog_release_notes = ChangelogReleaseNotes()

        changelog_release_notes.tag_exist()
        changelog_release_notes.release_notes_difference()
        changelog_release_notes.release_notes_exist()
        changelog_release_notes.release_notes_format()

        print(colored('You are good to release!', 'green'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Provide shop extension name as an argument.')
    parser.add_argument('repository', metavar='extension name', type=str, help='shop extension name e.g. woocommerce-ee')
    args = parser.parse_args()
    extension_name = args.repository
    changelog_release_notes = ChangelogReleaseNotes()
    changelog_release_notes.validate_release_notes()
