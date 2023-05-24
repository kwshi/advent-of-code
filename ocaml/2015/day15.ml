open Containers
open Fun.Infix

type ingredient =
  {capacity: int; durability: int; flavor: int; texture: int; calories: int}
[@@deriving show]

let map f i =
  { capacity= f i.capacity
  ; durability= f i.durability
  ; flavor= f i.flavor
  ; texture= f i.texture
  ; calories= f i.calories }

let map2 f i i' =
  { capacity= f i.capacity i'.capacity
  ; durability= f i.durability i'.durability
  ; flavor= f i.flavor i'.flavor
  ; texture= f i.texture i'.texture
  ; calories= f i.calories i'.calories }

let zero = {capacity= 0; durability= 0; flavor= 0; texture= 0; calories= 0}

let score i =
  let pos = max 0 in
  pos i.capacity * pos i.durability * pos i.flavor * pos i.texture

let parse_ingredient =
  function%pcre
  | "(\\w+): capacity (?<cap>-?\\d+), durability (?<dur>-?\\d+), flavor \
     (?<fl>-?\\d+), texture (?<tex>-?\\d+), calories (?<cal>-?\\d+)" ->
      let i = Int.of_string_exn in
      { capacity= i cap
      ; durability= i dur
      ; flavor= i fl
      ; texture= i tex
      ; calories= i cal }
  | _ ->
      failwith "bad input"

let parse = IO.read_lines_iter %> Iter.map parse_ingredient

let partitions =
  let rec go prefix = function
    | 1, n ->
        Iter.singleton (n :: prefix)
    | k, 0 ->
        Iter.singleton @@ Fun.iterate k (List.cons 0) prefix
    | k, n ->
        Iter.int_range ~start:0 ~stop:n
        |> Iter.flat_map (fun i -> go (i :: prefix) (k - 1, n - i))
  in
  Fun.curry @@ go []

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

let combine mul add z ns qs = List.map2 mul ns qs |> List.fold_left add z

let combine_ints = combine ( * ) ( + ) 0

let combine_ingredients = combine (map % ( * )) (map2 ( + )) zero

let run f () =
  let ingredients = parse stdin |> Iter.to_list in
  partitions (List.length ingredients) 100
  |> Iter.filter @@ f ingredients
  |> Iter.map (fun ns -> score @@ combine_ingredients ns ingredients)
  |> Iter.fold max 0 |> print_int |> print_newline

let part1 = run @@ Fun.const @@ Fun.const true

let part2 =
  run
  @@ fun ingredients ->
  let calories = List.map (fun i -> i.calories) ingredients in
  fun ns -> combine_ints ns calories = 500

(*

  scratch idea:

   represent each ingredient as a vector (c, d, f, t).

   we wish to find 𝑛ᵢ integers subject to the constraint 𝐺(𝒏)=∑𝑛ᵢ=100, maximizing
     (∑𝑛ᵢ𝑐ᵢ) (∑𝑛ᵢ𝑑ᵢ) (∑𝑛ᵢ𝑓ᵢ) (∑𝑛ᵢ𝑡ᵢ).
   this is eiuivalent to maximizing its logarithm,
     𝐹(𝒏) = log(∑𝑛ᵢ𝑐ᵢ) + log(∑𝑛ᵢ𝑑ᵢ) + log(∑𝑛ᵢ𝑓ᵢ) + log(∑𝑛ᵢ𝑡ᵢ).

   take a gradient:
     (𝛁𝐹)ⱼ = 𝜕ⱼ𝐹 = 𝑐ⱼ/∑𝑛ᵢ𝑐ᵢ + 𝑑ⱼ/∑𝑛ᵢ𝑑ᵢ + 𝑓ⱼ/∑𝑛ᵢ𝑓ᵢ + 𝑡ⱼ/∑𝑛ᵢ𝑡ᵢ.

   meanwhile
     (𝛁𝐺)ⱼ = 1.
*)
