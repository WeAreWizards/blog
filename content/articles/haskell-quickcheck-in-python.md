Title: Using Haskell's QuickCheck for Python
Date: 2015-03-19
Short_summary: We show how Python testing can be done via Haskell's QuickCheck.
Category: Hacks
Authors: Tom

Everyone I know who has ever used
[QuickCheck](http://hackage.haskell.org/package/QuickCheck/) in anger cannot live without it.
<!-- PELICAN_END_SUMMARY -->

The basic idea behind QuickCheck is that we write a proposition, e.g.:
*Reversing a list twice returns the same as the original list*. In
code:

```python
reverse(reverse(x)) == x
```

QuickCheck will try to find a counterexample to that proposition by
generating random values for `x`. And it is very good at finding mean values:

<blockquote class="twitter-tweet" lang="en"><p>Haskell Quickcheck enters a bar: asks for 1 beer, 42 beers, -Inifinity beers, shaves bartenders beard, sets off a tactical nuke.</p>&mdash; Michael Neale (@michaelneale) <a href="https://twitter.com/michaelneale/status/567532684595851264">February 17, 2015</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

### Shrinking

The really cool part is that when QuickCheck finds a counterexample it
will attempt to make the example smaller. Lets say we have a broken
reverse function that sorts the list instead. So for the input:
```
[2, 0, -1, 3, 9, 12]
```
our broken reverse returns:
```
[-1, 0, 2, 3, 9, 12]
```
instead of the correct:
```
[12, 9, 3, -1, 0, 2]
```

QuickCheck will shrink the input to `[2, 0, -1]` which still breaks
but is much easier to debug. Neat!


## Calling Python from Haskell

There is a relatively recent package on Hackage called
[pyfi](http://hackage.haskell.org/package/pyfi). It calls Python
through it's C FFI and passes values by converting them to and from
JSON. It comes with a great tutorial on its
[github page](https://github.com/Russell91/pyfi).


## QuickCheck

We start with a simple python module:

```python
# moremath.py
def square(x):
    return x * x
```

In Haskell every call to Python happens in the IO monad so we have to
use monadic QuickCheck:


```haskell
-- squarecheck.hs
import Python
import Test.QuickCheck
import Test.QuickCheck.Monadic

square :: Int -> IO Int
square = defVV "from moremath import square as export"

main = do
    quickCheck $ monadicIO $ do
    v <- pick arbitrary
    r <- run $ square v
    assert $ r == v * v
```

Now we can run the tests like so:

```console
$ runhaskell squarecheck.hs
+++ OK, passed 100 tests.
```

That's all there is to it!

**Edit:** Someone sent me a link to
[hypothesis](https://github.com/DRMacIver/hypothesis) which looks like
a really solid Python version of QuickCheck. The API has been adjusted
to fit into Python. Most importantly, it has a good shrinker!
