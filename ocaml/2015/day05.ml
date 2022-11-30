open Containers
open Fun.Infix

module PairSet = Set.Make (struct
  type t = char * char

  let compare = Stdlib.compare
end)

let nice1 s =
  let _, vowels, (double, bad) =
    String.fold
      (fun (prev, vowels, (double, bad)) c ->
        ( Some c
        , (vowels + match c with 'a' | 'e' | 'i' | 'o' | 'u' -> 1 | _ -> 0)
        , match prev with
          | None ->
              (double, bad)
          | Some prev -> (
              ( double || Char.equal c prev
              , match (prev, c) with
                | 'a', 'b' | 'c', 'd' | 'p', 'q' | 'x', 'y' ->
                    true
                | _ ->
                    bad ) ) ) )
      (None, 0, (false, false))
      s
  in
  vowels >= 3 && double && not bad

let nice2 s =
  let _, _, (_, a, b) =
    String.fold
      (fun (x, y, (pairs, a, b)) z ->
        ( y
        , Some z
        , match (x, y) with
          | Some x, Some y ->
              ( PairSet.add (x, y) pairs
              , a || PairSet.mem (y, z) pairs
              , b || Char.equal x z )
          | _ ->
              (pairs, a, b) ) )
      (None, None, (PairSet.empty, false, false))
      s
  in
  a && b

let run f () =
  IO.read_lines_iter stdin
  |> Iter.map (f %> Bool.to_int)
  |> Iter.sum |> Int.to_string |> print_endline

let part1 = run nice1

let part2 = run nice2
