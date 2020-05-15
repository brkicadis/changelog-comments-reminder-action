# Container Action Template

Checks if the changelog version has been updated and if release release notes are either added in wrong format or do not exist. 
This can be used in an automated release workflow to check release notes, as seen [here](https://github.com/wirecard/woocommerce-ee/blob/master/.github/workflows/changelog-comments-reminder-action.yml)

## How to setup

Simply add the action to your workflow
````
- name: Check changelog comments
  uses: wirecard/changelog-comments-reminder-action@master
  with:
    repository: <repository-name>
````

## Short overview of the file structure

### main.py

The ```main.py``` file is the main file called through ```entrypoint.sh``` in the container.  
It calls the required objects in the correct order and executes the necessary methods.
