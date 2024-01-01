module Year2017.Day01 where

import Control.Monad
import Data.Char
import Data.List
import Data.List.Extra
import Data.Maybe
import qualified System.IO as IO

pair :: (Eq a) => a -> a -> Maybe a
pair a b
  | a == b = Just a
  | otherwise = Nothing

solve :: (Int -> Int) -> IO.Handle -> IO Int
solve rot input = do
  s <- IO.hGetLine input
  let n = rot $ length s
  pure . sumOn' digitToInt . catMaybes . zipWith pair s . drop n $ cycle s

part1 :: IO.Handle -> IO Int
part1 = solve $ const 1

part2 :: IO.Handle -> IO Int
part2 = solve (`div` 2)
