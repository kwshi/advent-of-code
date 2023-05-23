open Containers
open Fun.Infix

let is_red = function _, `String "red" -> true | _ -> false

let rec filter_red = function
  | `Assoc a ->
      if List.exists is_red a then `Null
      else `Assoc (List.map (Pair.map_snd filter_red) a)
  | `List l ->
      `List (List.map filter_red l)
  | a ->
      a

let rec sum_numbers = function
  | `Null | `Bool _ | `String _ ->
      0
  | `Int n ->
      n
  | `Float f ->
      Float.to_int f
  | `List l ->
      List.fold_left ( + ) 0 @@ List.map sum_numbers l
  | `Assoc a ->
      List.fold_left ( + ) 0 @@ List.map (sum_numbers % snd) a

let run f () =
  Yojson.Basic.from_channel stdin |> f %> sum_numbers |> print_int ;
  print_newline ()

let part1 = run Fun.id

let part2 = run filter_red
