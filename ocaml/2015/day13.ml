open Containers
open Fun.Infix

let input_pattern =
  Re.Pcre.regexp
    "^(\\w+) would (gain|lose) (\\d+) happiness units by sitting next to \
     (\\w+).$"

module StringPair = struct
  type t = string * string

  let compare = Pair.compare String.compare String.compare
end

module PairMap = Map.Make (StringPair)
module PairSet = Set.Make (StringPair)
module StringSet = Set.Make (String)

let parse =
  IO.read_lines_iter
  %> Iter.fold
       (fun m l ->
         let group = Re.exec input_pattern l in
         PairMap.add
           (Re.Group.get group 1, Re.Group.get group 4)
           ( ( match Re.Group.get group 2 with
             | "gain" ->
                 Fun.id
             | "lose" ->
                 Int.neg
             | _ ->
                 failwith "bad" )
           @@ Int.of_string_exn @@ Re.Group.get group 3 )
           m )
       PairMap.empty

let adj = function
  | [] | [_] ->
      Iter.empty
  | first :: rest ->
      fun f ->
        f
          ( List.fold_left
              (fun prev this ->
                f (prev, this) ;
                this )
              first rest
          , first )

let run f () =
  let relations = f @@ parse stdin in
  let lookup k = PairMap.get_or ~default:0 k relations in
  let lookup' k = lookup k + lookup (Pair.swap k) in
  match
    PairMap.keys relations
    |> Iter.flat_map_l (fun (k, k') -> [k; k'])
    |> StringSet.of_iter |> StringSet.to_list
  with
  | [] ->
      failwith "empty"
  | first :: rest ->
      Ks.It.perms rest
      |> Iter.map
           (List.cons first %> adj %> Iter.map lookup' %> Iter.fold ( + ) 0)
      |> Iter.fold max 0 |> print_int ;
      print_newline ()

let part1 = run Fun.id

let part2 = run @@ PairMap.add ("", "") 0
