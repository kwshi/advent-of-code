open Containers
open Fun.Infix
module P2 = Ks.Pt.P2
module Grid = Set.Make (P2)

let parse =
  let parse_row (i, row) =
    String.to_iter row
    |> Iter.filter_mapi
       @@ fun j c -> Option.return_if (Char.equal c '#') @@ P2.make i j
  in
  IO.read_lines_iter %> Iter.zip_i %> Iter.flat_map parse_row %> Grid.of_iter

let bounds grid =
  Grid.fold
    (fun k (p, p') -> (P2.map2 min p k, P2.map2 max p' k))
    grid (P2.zero, P2.zero)

let show grid =
  let p, p' = bounds grid in
  Iter.int_range ~start:p.x ~stop:p'.x
  |> Iter.map (fun i ->
         Iter.int_range ~start:p.y ~stop:p'.y
         |> Iter.map (fun j ->
                if Grid.mem (P2.make i j) grid then '#' else '.' )
         |> Iter.to_str )
  |> Iter.intersperse "\n" |> Iter.concat_str

let neighbors p =
  [(1, 0); (1, 1); (0, 1); (-1, 1); (-1, 0); (-1, -1); (0, -1); (1, -1)]
  |> List.map (P2.from_tuple %> P2.add p)

let count grid p = neighbors p |> List.count (Fun.flip Grid.mem grid)

let rule grid p =
  let n = count grid p in
  n = 3 || (Grid.mem p grid && n = 2)

let advance patch grid =
  let p, p' = bounds grid in
  Iter.product
    (Iter.int_range ~start:p.x ~stop:p'.x)
    (Iter.int_range ~start:p.y ~stop:p'.y)
  |> Iter.map P2.from_tuple
  |> Iter.filter @@ rule grid
  |> Grid.of_iter |> patch p p'

let run patch () =
  parse stdin
  |> Fun.iterate 100 (advance patch)
  |> Grid.cardinal |> print_int |> print_newline

let part1 = run @@ Fun.const @@ Fun.const Fun.id

let part2 =
  run
  @@ fun p p' grid ->
  List.product P2.make [p.x; p'.x] [p.y; p'.y]
  |> List.fold_left (Fun.flip Grid.add) grid
