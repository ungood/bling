- [ ] Update HISTORY.rst
- [ ] Commit the changes: 
```
git add HISTORY.rst
git commit -m "Changelog for upcoming release 0.1.1."
```
- [ ] Update version number (can also be minor or major)
```
bumpversion patch
```
- [ ] Install the package again for local development, but with the new version number:
```
python setup.py develop
```
- [ ] Run the tests:
```
tox
```
- [ ] Allow Travis to release to PyPi by pushing new tag.
```
git push
git push --tags
```

- [ ] Test that it pip installs:
```
mktmpenv
pip install my_project
<try out my_project>
deactivate
```

- [ ] Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy and paste the RestructuredText into http://rst.ninjs.org/ to find out what broke the formatting.
- [ ] Edit the release on GitHub (e.g. https://github.com/audreyr/cookiecutter/releases). Paste the release notes into the release's release page, and come up with a title for the release.