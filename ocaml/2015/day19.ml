(*open Containers
  open Fun.Infix

  type 'a input = {rules: 'a; string: string}

  let parse_chunks =
    Iter.fold (fun parsers line ->
      match parsers, line with
      | [], _ -> failwith "out of parsers"
      | _ :: parsers', "" -> _
          ) {rules=[]; string=""}

  let parse = IO.read_lines_iter %> Iter.fold
*)

let part1 () = ()

let part2 () = ()
