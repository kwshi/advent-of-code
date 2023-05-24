open Containers
open Fun.Infix
module Scoreboard = Map.Make (String)

type reindeer = {name: string; speed: int; duration: int; rest: int}
[@@deriving show]

type state =
  { reindeer: reindeer
  ; position: int
  ; status: [`Flying | `Resting]
  ; elapsed: int
  ; points: int }
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

let calc_distance total r =
  let cycle = r.duration + r.rest in
  let rem = total mod cycle in
  r.speed * ((total / cycle * r.duration) + min rem r.duration)

let part1 () =
  parse stdin
  |> Iter.map (calc_distance 2503)
  |> Iter.fold max 0 |> print_int |> print_newline

let init reindeer =
  {reindeer; position= 0; status= `Flying; elapsed= 0; points= 0}

let timestep state =
  match state.status with
  | `Flying ->
      let state' =
        { state with
          position= state.position + state.reindeer.speed
        ; elapsed= state.elapsed + 1 }
      in
      if state'.elapsed < state'.reindeer.duration then state'
      else {state' with status= `Resting; elapsed= 0}
  | `Resting ->
      let state' = {state with elapsed= state.elapsed + 1} in
      if state'.elapsed < state'.reindeer.rest then state'
      else {state' with status= `Flying; elapsed= 0}

let get_leaders states =
  Scoreboard.fold
    (fun name {position; _} ((best, leaders) as current) ->
      if position = best then (position, name :: leaders)
      else if position > best then (position, [name])
      else current )
    states (0, [])
  |> snd

let add_points =
  List.fold_left (fun states leader ->
      let state = Scoreboard.find leader states in
      Scoreboard.add leader {state with points= state.points + 1} states )

let advance states =
  let states' = Scoreboard.map timestep states in
  add_points states' @@ get_leaders states'

let calc_points time =
  Fun.iterate time advance %> Scoreboard.values
  %> Iter.map (fun s -> s.points)
  %> Iter.fold max 0

let part2 () =
  parse stdin
  |> Iter.map (fun r -> (r.name, init r))
  |> Scoreboard.of_iter |> calc_points 2503 |> print_int |> print_newline
