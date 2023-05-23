open Containers
(*open Iter.Infix*)

let slinky : 'a list -> ('a list * 'a list) Iter.t =
  let rec go left right =
    Iter.cons (left, right)
    @@
    match right with [] -> Iter.empty | mid :: right -> go (mid :: left) right
  in
  fun a -> go [] a

let slinky1 : 'a list -> ('a list * 'a * 'a list) Iter.t =
  let rec go left = function
    | [] ->
        Iter.empty
    | mid :: right ->
        Iter.cons (left, mid, right) @@ go (mid :: left) right
  in
  function a -> go [] a

let perms : 'a list -> 'a list Iter.t =
  let rec go prefix = function
    | [] ->
        Iter.singleton @@ List.rev prefix
    | items ->
        Iter.flat_map (fun (left, mid, right) ->
            go (mid :: prefix) @@ List.rev_append left right )
        @@ slinky1 items
  in
  fun l -> go [] l
