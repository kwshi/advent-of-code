open Containers
open Fun.Infix

type reindeer = {name: string; speed: int; duration: int; rest: int}
[@@deriving show]

let parse_line =
  function%pcre
  | "^(?<name>\\w+) can fly (?<speed>\\d+) km/s for (?<duration>\\d+) seconds, \
     but then must rest for (?<rest>\\d+) seconds.$" ->
      { name
      ; speed= Int.of_string_exn speed
      ; duration= Int.of_string_exn duration
      ; rest= Int.of_string_exn rest }
  | _ ->
      failwith "bad line"

let parse = IO.read_lines_iter %> Iter.map parse_line

let calc total r =
  let cycle = r.duration + r.rest in
  let rem = total mod cycle in
  r.speed * ((total / cycle * r.duration) + min rem r.duration)

let part1 () =
  parse stdin
  |> Iter.map (calc 2503)
  |> Iter.fold max 0 |> print_int |> print_newline

let part2 () = ()
