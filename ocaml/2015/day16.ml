open Containers
open Fun.Infix
module Detection = Map.Make (String)
module Sues = Map.Make (Int)

let parse_line =
  function%pcre
  | "^Sue (?<i>\\d+): (?<entries>.*)$" ->
      ( Int.of_string_exn i
      , String.split ~by:", " entries
        |> List.map
             (function%pcre
             | "(?<prop>\\w+): (?<n>\\d+)" ->
                 (prop, Int.of_string_exn n)
             | _ ->
                 failwith "bad entry" )
        |> Detection.of_list )
  | _ ->
      failwith "bad line"

let gift =
  Detection.of_list
    [ ("children", 3)
    ; ("cats", 7)
    ; ("samoyeds", 2)
    ; ("pomeranians", 3)
    ; ("akitas", 0)
    ; ("vizslas", 0)
    ; ("goldfish", 5)
    ; ("trees", 3)
    ; ("cars", 2)
    ; ("perfumes", 1) ]

let parse = IO.read_lines_iter %> Iter.map parse_line %> Sues.of_iter

let test op gift =
  Detection.for_all (fun k v -> op k v @@ Detection.find k gift)

let run op () =
  parse stdin |> Sues.to_list
  |> List.find_map (fun (i, mem) -> if test op gift mem then Some i else None)
  |> Option.get_exn_or "no match"
  |> print_int |> print_newline

let part1 = run @@ Fun.const ( = )

let part2 =
  run
  @@ function
  | "cats" | "trees" -> ( > ) | "pomeranians" | "goldfish" -> ( < ) | _ -> ( = )
