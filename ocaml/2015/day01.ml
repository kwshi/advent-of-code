open Containers
open Fun.Infix

let step = function
  | '(' -> 1
  | ')' -> -1
  | _ -> failwith "expecting '(' or ')'"

let run f = read_line %> f %> Int.to_string %> print_endline
let part1 = run @@ String.fold (fun n -> ( + ) n % step) 0

let part2 =
  run
  @@ String.foldi
       (fun (n, found) i c ->
         let next = n + step c in
         ( next,
           match (found, next) with
           | Some _, _ -> found
           | None, -1 -> Some (i + 1)
           | None, _ -> None ))
       (0, None)
     %> snd
     %> Option.get_exn_or "never reaches -1"
