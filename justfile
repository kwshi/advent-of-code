set dotenv-load
set positional-arguments

fetch year day:
  curl -b "session=$AOC_SESSION" "https://adventofcode.com/$1/day/$2/input"
