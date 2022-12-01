open Containers
open Fun.Infix

module Edges = Map.Make (struct
  type t = string * string

  let compare = Pair.compare String.compare String.compare
end)

module Nodes = Set.Make (String)

let inserts a list f =
  let rec go (l, r) =
    f @@ List.rev_append l @@ (a :: r) ;
    match r with [] -> () | b :: r -> go (b :: l, r)
  in
  go ([], list)

let perms l f =
  let rec go l acc =
    match l with [] -> f acc | a :: rest -> inserts a acc @@ go rest
  in
  go l []

let consecutive_pairs l f =
  let rec go = function
    | a :: (b :: _ as rest) ->
        f (a, b) ;
        go rest
    | _ ->
        ()
  in
  go l

let run f () =
  let edges, nodes =
    IO.read_lines_iter stdin
    |> Iter.fold
         (fun (edges, nodes) line ->
           Scanf.sscanf line "%s to %s = %d"
           @@ fun a b n ->
           ( edges |> Edges.add (a, b) n |> Edges.add (b, a) n
           , nodes |> Nodes.add a |> Nodes.add b ) )
         (Edges.empty, Nodes.empty)
  in
  perms @@ Nodes.to_list nodes
  |> Iter.map (fun path ->
         consecutive_pairs path
         |> Iter.map (fun ((a, b) as edge) ->
                Edges.get edge edges
                |> Option.get_exn_or
                   @@ Printf.sprintf "undefined edge (%S, %S)" a b )
         |> Iter.sum )
  |> f |> Int.to_string |> print_endline

let part1 = run Iter.min_exn

let part2 = run Iter.max_exn
