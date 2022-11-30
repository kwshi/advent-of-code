open Containers
open Fun.Infix

module PairOrd = struct
  type t = int * int

  let compare = Stdlib.compare
end

module CoordSet = Set.Make (PairOrd)

let move (x, y) = function
  | '^' ->
      (x, y + 1)
  | 'v' ->
      (x, y - 1)
  | '<' ->
      (x - 1, y)
  | '>' ->
      (x + 1, y)
  | c ->
      failwith @@ Printf.sprintf "expecting one of '^' 'v' '<' '>', got %C" c

let origin = (0, 0)

let run f =
  read_line %> f %> snd %> CoordSet.cardinal %> Int.to_string %> print_endline

let part1 =
  run
  @@ String.fold
       (fun (pos, seen) dir ->
         let next = move pos dir in
         (next, CoordSet.add next seen) )
       (origin, CoordSet.singleton origin)

let part2 =
  run
  @@ String.fold
       (fun ((turn, santa, robo), seen) dir ->
         let santa', robo' =
           if turn then (move santa dir, robo) else (santa, move robo dir)
         in
         ( (not turn, santa', robo')
         , CoordSet.add santa' @@ CoordSet.add robo' seen ) )
       ((true, origin, origin), CoordSet.singleton origin)
