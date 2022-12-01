open Containers
open Fun.Infix

let evolve =
  let say acc = function None -> acc | Some (reps, n) -> n :: reps :: acc in
  let rec go acc run = function
    | [] ->
        say acc run
    | a :: rest ->
        ( match run with
        | Some (reps, n) when n = a ->
            go acc (Some (reps + 1, n))
        | _ ->
            go (say acc run) (Some (1, a)) )
          rest
  in
  List.rev % go [] None

let parse =
  String.to_list
  %> List.map
       Char.(
         fun c ->
           if '0' <= c && c <= '9' then to_int c - to_int '0'
           else failwith @@ Printf.sprintf "invalid digit %C" c )

let run n =
  read_line %> parse %> Fun.iterate n evolve %> List.map Int.to_string
  %> String.concat "" %> String.length %> Int.to_string %> print_endline

let part1 = run 40

let part2 = run 50
