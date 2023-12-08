set dotenv-load
set positional-arguments

fetch year day:
  #!/bin/bash
  set -euo pipefail
  file="input/$1/$(printf '%02d' "$2")"
  if [[ -e "$file" ]]; then
    echo $'\e[93;1m'"file ${file@Q} already exists; returning local copy."$'\e[m' >&2
    cat "$file"
  else
    echo $'\e[93;1m'"file ${file@Q} doesn't exist; fetching from AoC website."$'\e[m' >&2
    data="$(
      curl -fsS \
        -A 'github.com/kwshi/advent-of-code by shi.kye@gmail.com / justfile' \
        -b "session=$AOC_SESSION" \
        "https://adventofcode.com/$1/day/$(printf '%d' "$2")/input"
    )"
    mkdir -p "input/$1"
    echo "$data" | tee "$file"
  fi

download year day:
  #!/bin/bash
  set -euo pipefail
  tmp="${XDG_RUNTIME_DIR:-'/tmp'}/ks-aoc-$1-$2"
  curl -fsS -o "$tmp" -b "session=$AOC_SESSION" \
    "https://adventofcode.com/$1/day/$(printf '%d' "$2")/input"
  mkdir -p "input/$1"
  mv "$tmp" "input/$1/$(printf '%02d' "$2")"

ocaml *args:
  cd 'ocaml' && dune build main.exe
  ./ocaml/_build/default/main.exe "$@"

python *args:
  python -m 'python' -c './input' "$@"

pytest:
  pytest 'python'

edit-python year day:
  #!/bin/bash
  mkdir -p "python/$1"
  file="python/$1/$(printf '%02d' "$2").py"
  if [[ -e "$file" ]]; then
    echo $'\e[93;1m'"file ${file@Q} already exists; opening."$'\e[m' >& 2
  else
    echo $'\e[93;1m'"file ${file@Q} doesn't exist; initializing from template."$'\e[m' >& 2
    cp 'python/_template.py' "$file"
  fi
  nvim "$file"

edit-input year day:
  #!/bin/bash
  mkdir -p "input/$1"
  nvim "input/$1/$2"

submit year day part:
  #!/bin/bash
  set -euo pipefail
  read -r answer \
    && curl -fsS \
      -A 'github.com/kwshi/advent-of-code by shi.kye@gmail.com / justfile' \
      -b "session=$AOC_SESSION" \
      -d "level=$(printf '%d' "$3")" \
      -d "answer=$answer" \
      "https://adventofcode.com/$1/day/$(printf '%d' "$2")/answer" \
    | pup -p 'article text{}' # btw: https://github.com/ericchiang/pup/issues/93
