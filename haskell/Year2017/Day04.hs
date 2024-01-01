module Year2017.Day04 where

import Data.List
import qualified Data.Set as Set
import qualified System.IO as IO

dupFree :: (Ord a) => [a] -> Bool
dupFree ws = length (Set.fromList ws) == length ws

part :: (String -> String) -> IO.Handle -> IO Int
part f = fmap (length . filter (dupFree . map f . words) . lines) . IO.hGetContents

part1 :: IO.Handle -> IO Int
part1 = part id

part2 :: IO.Handle -> IO Int
part2 = part sort
