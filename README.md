# Static Site Project

I made an SSG in Python which will dynamically create webpages from Markdown. It was *super* fun trying to figure out which `regex` patterns worked for each markdown delimiter.

I also made this project using *only* the standard library--hence, why you see **no requirements.txt** file in the basedir.

All you need is Python(3.6+) to run this on your machine: simply `clone` the repo, `cd static-site`, and:

* (*Linux*) `./main.sh`
* (*Windows*) `python src/main.py && cd public && python3 -m http.server 8888`

Thank you to the team at [boot.dev](https://boot.dev) for this guided project--it really **humbled** me to avoid dependencies as much as possible, but I've found so much value in doing so.

> I'm a real boy!

## To-Do

1. Create Makefile
2. Sharpen Markdown comprehension for things like `***bold and italics***`, `tables` (*ooh la la...*)
3. Refactor src code
4. Implement >!spoilers!<
5. ???
6. PROFIT
