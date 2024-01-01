module Year2017.Day03 where

import qualified System.IO as IO

part1 :: IO.Handle -> IO Int
part1 = fmap (solve . read) . IO.hGetContents
  where
    solve n = l + s
      where
        sq k = (2 * k + 1) ^ 2
        l = head $ filter ((>= n) . sq) [0 ..]
        s = abs $ (sq l - n) `mod` (2 * l) - l

part2 :: IO.Handle -> IO Int
part2 = error "todo"
