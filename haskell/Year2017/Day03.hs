module Year2017.Day03 where

import qualified Data.Map as Map
import qualified System.IO as IO

getInt :: IO.Handle -> IO Int
getInt = fmap read . IO.hGetContents

part :: (Int -> Int) -> IO.Handle -> IO Int
part = (. getInt) . fmap

part1 :: IO.Handle -> IO Int
part1 = part solve1

part2 :: IO.Handle -> IO Int
part2 = part solve2

solve1 :: Int -> Int
solve1 n = l + s
  where
    sq k = (2 * k + 1) ^ 2
    l = head $ filter ((>= n) . sq) [0 ..]
    s = abs $ (sq l - n) `mod` (2 * l) - l

solve2 :: Int -> Int
solve2 n = head $ filter (>= n) $ calc (Map.singleton (0, 0) 1) pos
  where
    moves =
      do
        k <- [1, 3 ..]
        replicate k (1, 0)
          <> replicate k (0, 1)
          <> replicate (k + 1) (-1, 0)
          <> replicate (k + 1) (0, -1)
    pairAdd (a, b) (c, d) = (a + c, b + d)
    pos = scanl pairAdd (0, 0) moves
    neighbors (x, y) = [(x + dx, y + dy) | dx <- [-1 .. 1], dy <- [-1 .. 1]]
    calc acc (p : rest) =
      let n = sum $ flip (Map.findWithDefault 0) acc <$> neighbors p
       in n : calc (Map.insert p n acc) rest
