open Containers
open Fun.Infix

module type Container = sig
  type +'a t

  type +'a tuple

  type 'a constructor

  val make : 'a constructor

  val from_tuple : 'a tuple -> 'a t

  val to_tuple : 'a t -> 'a tuple

  val pure : 'a -> 'a t

  val map : ('a -> 'b) -> 'a t -> 'b t

  val map2 : ('a -> 'b -> 'c) -> 'a t -> 'b t -> 'c t

  val fold : ('b -> 'a -> 'b) -> 'b -> 'a t -> 'b

  val to_iter : 'a t -> 'a Iter.t
end

module type Num = sig
  type t

  val zero : t

  val neg : t -> t

  val abs : t -> t

  val add : t -> t -> t

  val sub : t -> t -> t

  val mul : t -> t -> t

  val div : t -> t -> t

  val compare : t -> t -> int

  val to_string : t -> string
end

module C2 = struct
  type 'a t = {x: 'a; y: 'a}

  type 'a tuple = 'a * 'a

  type 'a constructor = 'a -> 'a -> 'a t

  let make x y = {x; y}

  let from_tuple (x, y) = {x; y}

  let to_tuple {x; y} = (x, y)

  let pure x = {x; y= x}

  let map f v = {x= f v.x; y= f v.y}

  let map2 f v v' = {x= f v.x v'.x; y= f v.y v'.y}

  let fold f i v = f (f i v.x) v.y

  let to_iter v f = f v.x ; f v.y
end

module C3 = struct
  type +'a t = {x: 'a; y: 'a; z: 'a}

  type +'a tuple = 'a * 'a * 'a

  type 'a constructor = 'a -> 'a -> 'a -> 'a t

  let make x y z = {x; y; z}

  let from_tuple (x, y, z) = {x; y; z}

  let to_tuple {x; y; z} = (x, y, z)

  let pure x = {x; y= x; z= x}

  let map f v = {x= f v.x; y= f v.y; z= f v.z}

  let map2 f v v' = {x= f v.x v'.x; y= f v.y v'.y; z= f v.z v'.z}

  let fold f i v = f (f (f i v.x) v.y) v.z

  let to_iter v f = f v.x ; f v.y ; f v.z
end

module Make (C : Container) (N : Num) = struct
  include C

  type t = N.t C.t

  type tuple = N.t C.tuple

  type constructor = N.t C.constructor

  let zero = C.pure N.zero

  let neg = map N.neg

  let abs = map N.abs

  let scale = map % N.mul

  let scale_inv = map % Fun.flip N.div

  let add = map2 N.add

  let sub = map2 N.sub

  let mul = map2 N.mul

  let div = map2 N.div

  let sum = fold N.add N.zero

  let dot a b = sum @@ mul a b

  let norm1 = sum % abs

  let norm2_sq a = dot a a

  let compare a b =
    map2 Pair.make a b
    |> fold (fun c (i, j) -> match c with 0 -> N.compare i j | _ -> c) 0

  let to_list a = List.rev @@ fold List.cons' [] a

  let show =
    Printf.sprintf "{%s}" % String.concat " " % List.map N.to_string % to_list

  module Infix = struct
    let ( + ) = add

    let ( - ) = sub

    let ( * ) = mul

    let ( / ) = div

    let ( *. ) = scale

    let ( /. ) = Fun.flip scale_inv

    let ( *@ ) = dot
  end
end

module Make3 (N : Num) = struct
  include Make (C3) (N)

  let from_p2 ?z p =
    let open C3 in
    {x= p.x; y= p.y; z= Option.get_or ~default:N.zero z}

  let truncate p = C2.{x= p.C3.x; y= p.C3.y}
end

module P2 = Make (C2) (Int)
module P2f = Make (C2) (Stdlib.Float)
module P3 = Make (C3) (Int)
module P3f = Make (C3) (Stdlib.Float)
