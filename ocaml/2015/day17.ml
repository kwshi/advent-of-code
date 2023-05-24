open Containers
open Fun.Infix

let parse = IO.read_lines_iter %> Iter.map Int.of_string_exn

(* copy-pasted from day 15; consider factoring into library *)
let partitions' =
  let rec go prefix = function
    | [], _ ->
        Iter.empty
    | [size], n ->
        if n mod size <> 0 then Iter.empty
        else Iter.singleton @@ List.rev ((n / size) :: prefix)
    | size :: rest, n ->
        Iter.int_range ~start:0 ~stop:(n / size)
        |> Iter.flat_map (fun i -> go (i :: prefix) (rest, n - (i * size)))
  in
  Fun.curry @@ go []

let fill =
  let rec go prefix = function
    | [], 0 ->
        Iter.singleton @@ List.rev prefix
    | [], _ ->
        Iter.empty
    | bucket :: rest, amount ->
        ( if bucket > amount then Fun.id
        else Iter.append @@ go (true :: prefix) (rest, amount - bucket) )
          (go (false :: prefix) (rest, amount))
  in
  Fun.curry @@ go []

let size = 150

let run filter () =
  let buckets = Iter.to_list @@ parse stdin in
  let ways = fill buckets size in
  filter (List.length buckets) ways |> Iter.length |> print_int |> print_newline

let part1 = run @@ Fun.const Fun.id

let part2 =
  run
  @@ fun n ways ->
  let count = Iter.map (List.count Fun.id) ways |> Iter.fold min n in
  Iter.filter (Int.equal count % List.count Fun.id) ways
