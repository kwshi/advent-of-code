open Containers
open Fun.Infix

let size = 1000

let parse_coord s =
  match String.split_on_char ',' s |> List.map Int.of_string_exn with
  | [x; y] ->
      (x, y)
  | _ ->
      failwith @@ Printf.sprintf "failed to parse coord %S" s

let run (on, off, toggle) () =
  let grid = Array.init (size * size) @@ Fun.const 0 in
  let step f = function
    | [p; "through"; p'] ->
        let x, y = parse_coord p in
        let x', y' = parse_coord p' in
        Iter.product Iter.(x -- x') Iter.(y -- y')
        |> Iter.iter (fun (x, y) ->
               let i = (1000 * y) + x in
               Array.set grid i (f @@ Array.get grid i) )
    | args ->
        failwith @@ Printf.sprintf "invalid command %S" (String.concat " " args)
  in
  IO.read_lines_iter stdin
  |> Iter.iter
       ( String.split_on_char ' '
       %> function
       | "turn" :: "on" :: rest ->
           step on rest
       | "turn" :: "off" :: rest ->
           step off rest
       | "toggle" :: rest ->
           step toggle rest
       | args ->
           failwith
           @@ Printf.sprintf "invalid command %S" (String.concat " " args) ) ;
  Array.to_iter grid |> Iter.sum |> Int.to_string |> print_endline

let part1 = run (Fun.const 1, Fun.const 0, ( - ) 1)

let part2 = run (( + ) 1, max 0 % ( + ) (-1), ( + ) 2)
