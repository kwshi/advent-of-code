open Containers
open Fun.Infix

type atom = Literal of int | Variable of string

type bop = And | Or | ShiftL | ShiftR

type expr = Atom of atom | Not of atom | Bop of bop * atom * atom

type instruction = {target: string; expr: expr}

module Parser = struct
  open Angstrom

  let is_digit c =
    let open Char.Infix in
    '0' <= c && c <= '9'

  let is_alpha c =
    let open Char.Infix in
    'a' <= c && c <= 'z'

  let sym = take_while1 is_alpha

  let atom =
    (fun a -> Literal a)
    <$> (Int.of_string_exn <$> take_while1 is_digit)
    <|> ((fun a -> Variable a) <$> sym)

  let space = skip_while @@ Char.equal ' '

  let bop =
    return And <* string "AND"
    <|> (return Or <* string "OR")
    <|> (return ShiftL <* string "LSHIFT")
    <|> (return ShiftR <* string "RSHIFT")

  let expr =
    (fun a o b -> Bop (o, a, b))
    <$> atom <* space <*> bop <* space <*> atom
    <|> (return (fun a -> Not a) <* string "NOT" <* space <*> atom)
    <|> ((fun a -> Atom a) <$> atom)

  let instruction =
    (fun expr target -> {target; expr})
    <$> expr <* space <* string "->" <* space <*> sym
end

module Scope = Map.Make (struct
  type t = string

  let compare = String.compare
end)

let eval_atom scope = function
  | Literal n ->
      n
  | Variable s ->
      Scope.get s scope
      |> Option.get_exn_or @@ Printf.sprintf "undefined variable %S" s

let bop = function
  | And ->
      ( land )
  | Or ->
      ( lor )
  | ShiftL ->
      ( lsl )
  | ShiftR ->
      ( lsr )

let eval def =
  let rec go seen sym =
    match Scope.get sym seen with
    | Some n ->
        (seen, n)
    | None ->
        let seen, n =
          match
            Scope.get sym def
            |> Option.get_exn_or @@ Printf.sprintf "variable %S undefined" sym
          with
          | Atom a ->
              atom seen a
          | Not a ->
              Pair.map_snd lnot @@ atom seen a
          | Bop (o, a, b) ->
              let seen, na = atom seen a in
              let seen, nb = atom seen b in
              (seen, bop o na nb)
        in
        (Scope.add sym n seen, n)
  and atom seen = function Literal n -> (seen, n) | Variable s -> go seen s in
  go Scope.empty %> snd

let parse () =
  let update def {target; expr} = Scope.add target expr def in
  IO.read_lines_iter stdin
  |> Iter.fold
       (fun scope line ->
         Angstrom.parse_string ~consume:Angstrom.Consume.All Parser.instruction
           line
         |> Result.get_exn |> update scope )
       Scope.empty

let part1 () = eval (parse ()) "a" |> Int.to_string |> print_endline

let part2 () =
  let def = parse () in
  let def = Scope.add "b" (Atom (Literal (eval def "a"))) def in
  eval def "a" |> Int.to_string |> print_endline
