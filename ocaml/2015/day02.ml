open Containers
open Fun.Infix

let parse =
  String.split_on_char 'x' %> List.map Int.of_string_exn %> function
  | [ l; w; h ] -> (l, w, h)
  | _ -> failwith "wrong number of elements"

let min3 x y = min x % min y
let min3' = ( %> ) min % ( % ) % min (* haha (same as `min3` but pointfree) *)

let calc1 (l, w, h) =
  let a, b, c = (l * w, w * h, h * l) in
  (2 * (a + b + c)) + min3 a b c

let calc2 (l, w, h) =
  let a, b, c = (l + w, w + h, h + l) in
  (2 * min3' a b c) + (l * w * h)

let run f () =
  IO.read_lines_iter stdin
  |> Iter.map (parse %> f)
  |> Iter.sum |> Int.to_string |> print_endline

let part1 = run calc1
let part2 = run calc2
