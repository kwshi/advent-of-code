open Containers
open Fun.Infix

type tag = Start | InString | Escape | Hex | Hex1 of int | End

type state = {tag: tag; buf: char list}

let char_hex =
  let open Char in
  function
  | c when '0' <= c && c <= '9' ->
      to_int c - to_int '0'
  | c when 'a' <= c && c <= 'z' ->
      to_int c - to_int 'a'
  | c ->
      failwith @@ Printf.sprintf "invalid hexadecimal character %C" c

let parse =
  String.foldi
    (fun state i c ->
      match (state.tag, c) with
      | Start, '"' ->
          {state with tag= InString}
      | InString, '\\' ->
          {state with tag= Escape}
      | InString, '"' ->
          {state with tag= End}
      | InString, _ ->
          {tag= InString; buf= c :: state.buf}
      | Escape, '"' | Escape, '\\' ->
          {tag= InString; buf= c :: state.buf}
      | Escape, 'x' ->
          {state with tag= Hex}
      | Hex, _ ->
          {state with tag= Hex1 (char_hex c)}
      | Hex1 n, _ ->
          { tag= InString
          ; buf= Char.of_int_exn ((n lsl 4) + char_hex c) :: state.buf }
      | End, _ ->
          failwith
          @@ Printf.sprintf "reached end of string but got %C at position %d" c
               i
      | _ ->
          failwith @@ Printf.sprintf "invalid input at position %d" i )
    {tag= Start; buf= []}
  %> function
  | {tag= End; buf} ->
      List.rev buf |> String.of_list
  | _ ->
      "incomplete string (didn't reach end?)"

let encode =
  Printf.sprintf {|"%s"|}
  % String.flat_map (function
      | '"' ->
          {|\"|}
      | '\\' ->
          {|\\|}
      | c ->
          String.of_char c )

let run f () =
  IO.read_lines_iter stdin
  |> Iter.map (fun s -> abs @@ (String.length s - String.length (f s)))
  |> Iter.sum |> Int.to_string |> print_endline

let part1 = run parse

let part2 = run encode
