module Year2017.Day05 where

import qualified Data.Map as Map
import qualified Data.Maybe as Maybe
import qualified System.IO as IO

parse :: IO.Handle -> IO [Int]
parse = fmap (map read . lines) . IO.hGetContents

solve :: (Int -> Int) -> [Int] -> Int
solve f ns =
  go 0 0 $ Map.fromList (zip [0 ..] ns)
  where
    go step i m =
      maybe step (\n -> go (step + 1) (i + n) (Map.adjust f i m)) $
        Map.lookup i m

part :: (Int -> Int) -> IO.Handle -> IO Int
part = (. parse) . fmap . solve

part1 :: IO.Handle -> IO Int
part1 = part (+ 1)

part2 :: IO.Handle -> IO Int
part2 = part (\k -> if k >= 3 then k - 1 else k + 1)
