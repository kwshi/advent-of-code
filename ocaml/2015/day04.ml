open Containers
open Fun.Infix

let find prefix s =
  let rec go n =
    let hex = Digest.to_hex @@ Digest.string @@ s ^ Int.to_string n in
    if String.starts_with ~prefix hex then n else go @@ (n + 1)
  in
  go 1

let run prefix = read_line %> find prefix %> Int.to_string %> print_endline

let part1 = run "00000"

let part2 = run "000000"
