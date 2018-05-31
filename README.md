Tools for converting a downloaded submit.cs assignment to a Gradescope assignment.

# Instructions

1. Visit the edit page for the assignment on Submit.cs and click the button that says 'Download Project'. You should get a zip file.
2. Clone this repo and cd into it.
3. Run `./convert.sh [zipfile] [outdir]` where:
   * zipfile is the absolute path for the zip file you downloaded
   * outdir is the directory you want the autograder to be written to (which must not previously exist)
4. Copy your reference solution into the REFERENCE-SOLUTION directory in outdir.
5. You have a Gradescope-compatible autograder!
6. (optional) cd into outdir and run `git init` to turn it into a git repo
7. (optional) use `git remote add origin [url]` where url is the url of an empty remote repository
8. (optional) run `git push origin master` to update the repo