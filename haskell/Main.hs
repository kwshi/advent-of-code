{-# LANGUAGE NamedFieldPuns #-}

module Main where

import qualified GHC.Read
import Options.Applicative
import qualified System.IO as IO
import qualified Year2017.Day01
import qualified Year2017.Day02
import qualified Year2017.Day03

data Args = Args {year :: Int, day :: Int, part :: Part}

data Part = Part1 | Part2

instance Read Part where
  readPrec = intToPart <$> GHC.Read.readPrec
    where
      intToPart 1 = Part1
      intToPart 2 = Part2
      intToPart _ = error "invalid part (must be 1 or 2)"

main :: IO ()
main =
  execParser (info args $ progDesc "advent of code") >>= run
  where
    run (Args {year, day, part}) = getSolver year day part IO.stdin >>= print
    args =
      Args
        <$> argument auto (metavar "year")
        <*> argument auto (metavar "day")
        <*> argument auto (metavar "part")

    getSolver 2017 1 Part1 = Year2017.Day01.part1
    getSolver 2017 1 Part2 = Year2017.Day01.part2
    getSolver 2017 2 Part1 = Year2017.Day02.part1
    getSolver 2017 2 Part2 = Year2017.Day02.part2
    getSolver 2017 3 Part1 = Year2017.Day03.part1
    getSolver 2017 3 Part2 = Year2017.Day03.part2
    getSolver _ _ _ = error "solution not implemented"
