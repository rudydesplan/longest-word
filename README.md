# Continuous Integration

Having tests on a repository gives you a tremendous advantage: you can set up [**Continuous Integration**](https://en.wikipedia.org/wiki/Continuous_integration). The _Best Practices_ section of this Wikipedia article is worth a read.

The goal of this exercise is to link our version control software with a build automation tool. The idea is that you want the build automation to run every time a commit reaches the version control, in any branch, a build is triggered to give feedback to the developers as soon as possible if this commit is _green_ or _red_ (meaning the tests are passing / the build can complete).

## Tools

As for version control software, there are many tools available to achieve Continuous Integration:

- [Jenkins](https://jenkins.io/), the most popular on-premise CI software (you need to install it)
- [Github Actions](https://github.com/features/actions), the tool from Github to set up automated workflows and CI/CD
- [Travis](https://travis-ci.com/), the most popular **cloud** CI service
- [Many others](https://en.wikipedia.org/wiki/Comparison_of_continuous_integration_software)

To keep this exercise simple, we will use Github Actions, as it integrates perfectly with GitHub (and you'll see that's important) without any configuration effort on the developer's side. Plus, it's **free** for public GitHub repositories!

## Repository Initialisation and .gitignore

We will deploy the repository you created in the previous exercise, but this time we'll make sure we'll first commit an essential file for any git repository: `.gitignore`.

A `.gitignore` is a file where we can specify any files to ignored for tracking by git! There are a multiple reasons why you wouldn't want a file to be tracked by git:
- A file may contain secrets that you don't want to be public facing - like a `.env` file
- Bytecode or cache files that compiles scripts into bytecode - these files are machine generated and platform specific
- Virtual environment files that are unnecessary or inefficient to track
- Data, or very large files - the purpose of git and version control is to track changes in files, not changes in raw data.

First navigate to your `longest-word` directory and open VSCode:

```bash
cd ~/code/<user.github_nickname>/longest-word
code .
```

We'll want to create a `.gitignore` file and fill it with some relevant file types that we don't want to track. In a terminal inside your `/longest-word` project:

```bash
touch .gitignore
```

There are a number of files that we don't want tracked with git, but where do we start?

💡 Luckily GitHub has a fantastic [boilerplate `.gitignore`](https://github.com/github/gitignore/blob/main/Python.gitignore) for python projects (and multiple other languages!) based on commonly used python frameworks and tooling.

Copy the contents of GitHub's [`Python.gitignore` boilerplate](https://github.com/github/gitignore/blob/main/Python.gitignore) into your own `.gitignore` - you can access just the raw text of the `.gitignore` by clicking on `Raw` on GitHub and using your keyboard shortcut for `select all`. Make sure to save your `.gitignore`.

Now we're ready to initialise and commit our changes, but we'll do it in a few steps so that our `.gitignore` comes into effect. Make sure to copy the lines one by one and understand what each command is doing.

```bash
# Initialize project with git tracking
git init

# Commit your .gitignore
git add .gitignore
git commit -m "initial commit"
```

Now that our `.gitignore` is committed, git should be the ignoring relevant files for us.

```bash
# .gitignore should now ignore relevant files
git add .
git commit -m "Game development with TDD"

# Create GitHub repository
gh repo create --public --source=.

# Push local changes to GitHub
git push origin master
```

## Worfklow CI

You now need to write a CI configuration file. Those tools are _generic_, they can build programs in many languages, with many frameworks. We need to be specific and explain to Github Actions that our project is a Python 3 one, that we use `poetry` to handle external dependencies and that we use `pytest` to run tests.

In order to do that, Github reads the `.python-ci.yml` file located in the folder  `.github/workflows` :

```bash
mkdir -p .github/workflows
touch .github/workflows/.python-ci.yml
```

```yml
# .python-ci.yml

name: basic CI
on:
  push:
    branches: [ master, main ]
  pull_request:
    branches: [ master, main ]
jobs:
  build-and-run-pytest:
    runs-on: ubuntu-latest
    steps:
    # First step (unnamed here) is to checkout to the branch that triggered the event
    - uses: actions/checkout@v4.2.0
    # Second step: install python 3.12.6
    - name: Set up Python 3.12.6
      uses: actions/setup-python@v5.2.0
      with:
        python-version: "3.12.6"
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install
    - name: Run tests
      run: |
        poetry run pytest
```

Save this file in VS Code, and perform a commit:

```bash
git add .github
git commit -m "Configure Github Actions CI to run pytest"
```

Awesome! Before we actually push, go to this page:

[github.com/<user.github_nickname>/longest-word/commits/master](https://github.com/<user.github_nickname>/longest-word/commits/master)

You should have one commit. Now go back to the terminal:

```bash
git push origin master
```

When the push is done, go back to the page, and **reload** it. You should see the commit get a yellow circle, and then a green tick! This is the integration between GitHub and Github Actions. It will run everytime you push commits to GitHub.

You can view the actions in browser or through the cli with `gh run watch`!

📚 Take 10min to read this [Github Docs](https://docs.github.com/en/actions/using-workflows/about-workflows) to better understand how workflows work

## Continuous Integration & Pull Request

Let's enhance our Game with a refined validation. Right now, you can win with the following scenario:

```
Grid: KWIENFUQW
My proposition: FEUN
```

```python
new_game = Game()
new_game.grid = list('KWIENFUQW')
new_game.is_valid('FEUN')
# => true
```

Sure, it is syntatically valid (each letter of `FEUN` can be found in the grid), but this is not a valid English word from the dictionary!

Let's work on that in a new feature branch:

```bash
git checkout -b dictionary-api
```

Following the TDD paradigm, we need to add a test:

```python
# tests/test_game.py
# [...]
    def test_unknown_word_is_invalid(self):
        """A word that is not in the English dictionary should not be valid"""
        new_game = Game()
        new_game.grid = list('KWIENFUQW') # Force the grid to a test case:
        assert new_game.is_valid('FEUN') is False
```

Let's commit this right now:

```bash
git add tests/test_game.py
git commit -m "TDD: Check that attempt exists in the English dictionary"
git push origin dictionary-api
```

Now let's open a Pull Request on GitHub for this branch.
- 💡 To make a pull request quickly you can use `gh pr create` or to directly open the web page use `gh pr create --web`!
- You might find it a bit early but opening a Pull Request early is encouraged by the [GitHub flow](http://scottchacon.com/2011/08/31/github-flow.html). If you are stuck in the progress of your feature or branch and need help or advice, or if you are a developer and need a designer to review your work (or vice versa). Even if you have little or no code but some screenshots or general ideas, open a pull request.
- At Le Wagon, developers open Pull Request early on for their feature branches to show teammates what they are doing and solicit feedback early. No need to wait to be code-complete to open the Pull Request! Here is a screenshot of our main application. Using the `[WIP]` prefix in the pull request titles to showcase the fact that the branch is not ready yet to be merged:

<img src="https://res.cloudinary.com/wagon/image/upload/v1560714921/kitt-wip-prs_obp6e7.png" width=600>

Back to our Pull Request. If you scroll a bit below the PR description and the list of commits, you will see the Github Actions shine:

<img src="https://github.com/lewagon/fullstack-images/blob/master/reboot-python/github_actions_picture.png?raw=true" width="700">

The benefit is really important. You have a direct feedback, right in GitHub, about the build status of your branch. Of course here we actually _want_ to have a red branch as we added a test but did not implement the behavior yet. Still, you can imagine that someone pushing some code and forgetting to run the tests locally on their machine will be warned directly on GitHub that they broke the build.

---

❓ **Let's go back to the implementation of our feature: Try to pass the following test**

```python
poetry run pytest -k test_unknown_word_is_invalid
# 💡 See how we just run *one* test and not the whole suite?
```
Using Le Wagon's homemade simple [Dictionary API](https://dictionary.lewagon.com/)
  - [https://dictionary.lewagon.com/tomato](https://dictionary.lewagon.com/tomato)
  - [https://dictionary.lewagon.com/notomato](https://dictionary.lewagon.com/notomato)

💡 You can `poetry add requests` to make [HTTP requests](http://docs.python-requests.org/en/master/) to this API in Python

<details><summary markdown='span'>🎁 View solution
</summary>

We can implement a private `__check_dictionary` method to run an API call.

```python
# game.py
# [...]
import requests

class Game:
    # [...]

    def is_valid(self, word):
        # [...]

        return self.__check_dictionary(word)


    @staticmethod
    def __check_dictionary(word):
        response = requests.get(f"https://dictionary.lewagon.com/{word}")
        json_response = response.json()
        return json_response['found']
```

</details>

<br>

Don't forget to run the tests locally until you have 5 passing tests. When you are done, time to observe the effect on GitHub / Github Actions!

```bash
git add .
git commit -m "Feature complete: Dictionary check of attempt"
git push origin dictionary-api
```

Go back to your Pull Request page, you should see the icons turning from red crosses to yellow dots. It means that Github Actions is building the code against the latest commit. Wait a few seconds, and it should update the status. This is what you should see:

<img src="https://res.cloudinary.com/wagon/image/upload/v1560714701/github-travis-passing_vppc1l.png" width=500>

Awesome job 🎉! Invite your buddy as a repo collaborator to review the code in the Pull Request and **merge** it.

## 🏁 Conclusion

Adding tests to a repository and coupling GitHub with a service like Github Actions gives the developer peace of mind when adding code, checking for possible regressions, exercising the whole test suite for _every single_ commit!

Before pushing DevOps farther with the next exercise about Continuous Deployment, some final advice:

- Keep Pull Request diffs as short as possible. A good size is **less than 100 lines** in the diff (`Files changed` tab on the Pull Request)
- Keep Pull Request focused on a _single_ feature. Add at least a test for each pull request
- Before asking for a review, re-read your code in the `Files changed` tab. Seeing the code from this perspective (in a web browser under a diff format) will help you spot style issues, refactoring opportunities, etc. that you could not see directly in your text editor.
- Finally, your friends at GitHub wrote a great piece on [how to properly write](https://blog.github.com/2015-01-21-how-to-write-the-perfect-pull-request/) in a Pull Request (both for the reviewee and the reviewer).
