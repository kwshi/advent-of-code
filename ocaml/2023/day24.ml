open Containers
open Fun.Infix

let part1 () = ()

let parse_line =
  function%pcre
  | {|(?<x>-?\d+),\s+(?<y>-?\d+),\s+(?<z>-?\d+)\s+@\s+(?<u>-?\d+),\s+(?<v>-?\d+),\s+(?<w>-?\d+)|}
    ->
      ( Int.of_string_exn x
      , Int.of_string_exn y
      , Int.of_string_exn z
      , Int.of_string_exn u
      , Int.of_string_exn v
      , Int.of_string_exn w )
  | l ->
      failwith @@ "invalid line: " ^ l

let parse = IO.read_lines_iter %> Iter.map parse_line

let part2 () =
  let open Z3 in
  let open Arithmetic in
  let ctx = mk_context [] in
  let solver = Solver.mk_solver ctx None in
  let ( == ) = Boolean.mk_eq ctx in
  let ( + ) a b = mk_add ctx [a; b] in
  let ( * ) a b = mk_mul ctx [a; b] in
  let x = Real.mk_const_s ctx "x" in
  let y = Real.mk_const_s ctx "y" in
  let z = Real.mk_const_s ctx "z" in
  let u = Real.mk_const_s ctx "u" in
  let v = Real.mk_const_s ctx "v" in
  let w = Real.mk_const_s ctx "w" in
  parse stdin
  |> Iter.iteri (fun i (xi, yi, zi, ui, vi, wi) ->
         let xi = Real.mk_numeral_i ctx xi in
         let yi = Real.mk_numeral_i ctx yi in
         let zi = Real.mk_numeral_i ctx zi in
         let ui = Real.mk_numeral_i ctx ui in
         let vi = Real.mk_numeral_i ctx vi in
         let wi = Real.mk_numeral_i ctx wi in
         let t = Real.mk_const_s ctx @@ "t" ^ Int.to_string i in
         Solver.add solver
           [ x + (u * t) == xi + (ui * t)
           ; y + (v * t) == yi + (vi * t)
           ; z + (w * t) == zi + (wi * t) ] ) ;
  match Solver.check solver [] with
  | SATISFIABLE ->
      let m = Solver.get_model solver |> Option.get_exn_or "never" in
      let x =
        Model.eval m x false |> Option.get_exn_or "missing x" |> Real.get_ratio
      in
      let y =
        Model.eval m y false |> Option.get_exn_or "missing y" |> Real.get_ratio
      in
      let z =
        Model.eval m z false |> Option.get_exn_or "missing z" |> Real.get_ratio
      in
      print_endline @@ Q.to_string Q.(x + y + z)
  | _ ->
      failwith "huh"
