module Year2017.Day02 where

import Control.Applicative
import Data.List
import Data.Maybe
import qualified System.IO as IO

parse :: IO.Handle -> IO [[Int]]
parse =
  fmap (map (map read . words) . lines) . IO.hGetContents

solve :: ([Int] -> Int) -> IO.Handle -> IO Int
solve checksum =
  fmap (sum . map checksum) . parse

part1 :: IO.Handle -> IO Int
part1 = solve checksum1
  where
    checksum1 a = maximum a - minimum a

part2 :: IO.Handle -> IO Int
part2 = solve checksum2
  where
    checksum2 = head . findDiv . sort
    findDiv [] = []
    findDiv (first : rest) = mapMaybe (tryDiv first) rest <|> findDiv rest
    tryDiv a b
      | b `mod` a == 0 = Just $ b `div` a
      | otherwise = Nothing
