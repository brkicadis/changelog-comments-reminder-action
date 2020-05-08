from lastversion import lastversion
from collections import namedtuple
import os
import json
import argparse
import sys
import git
import re


class Definition:
    CONFIG_FILE_PATH = '/usr/bin/shop-extensions.json'
    SHOP_EXTENSION_PARTNER = 'wirecard'

    EXTENSION_NAMING_CONVENTION = {
        "paymentSDK-php": "paymentsdk",
        "prestashop-ee": "prestashop",
        "woocommerce-ee": "woocommerce",
        "opencart-ee": "opencart",
        "magento2-ee": "magento2",
        "shopware-ee": "shopware",
        "oxid-ee": "oxid",
        "magento-ee": "magento"
    }


class JsonFile:
    def __init__(self, json_file_name):
        self.json_file_name = json_file_name

    def get_json_file(self) -> dict:
        with open(os.path.abspath(self.json_file_name)) as file_name:
            return json.load(file_name)

    @staticmethod
    def json_decoder(extensions_parameters) -> tuple:
        return namedtuple('X', extensions_parameters.keys())(*extensions_parameters.values())

    def get_json_content(self) -> str:
        json_string = json.dumps(self.get_json_file(), indent=4)
        return json.loads(json_string, object_hook=JsonFile.json_decoder)


class ReleaseVersion:
    def __init__(self, file_name, file_content, version):
        self.file_name = file_name
        self.file_content = file_content
        self.version = version

    @staticmethod
    def get_last_released_version() -> str:
        """
        Returns last released version from GitHub tag
        :return: str
        """
        repository_name = sys.argv[1]
        repository_to_clone = Definition.SHOP_EXTENSION_PARTNER + "/" + repository_name
        latest_release_vrsion = 'v' + lastversion.latest(repository_to_clone, output_format='version', pre_ok=True)
        print('Latest release version')
        print(latest_release_vrsion)
        return latest_release_vrsion

    @staticmethod
    def get_current_release_version() -> str:
        """
        Returns current release version from branch name
        :return: str
        """
        repo = git.Repo(search_parent_directories=True)
        branch = repo.active_branch
        current_release_version = 'v' + re.sub('[^\d\.]', '', branch.name)
        print('Current release version')
        print(current_release_version)
        return current_release_version


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Provide shop extension name as an argument.')
    parser.add_argument('repository', metavar='extension name', type=str, help='shop extension name e.g. woocommerce-ee')
    args = parser.parse_args()
    extension_name = args.repository
