# perlin

I wrote this to understand how Perlin noise actually works, rather than import
a function that returns it.

## Why N-dimensional

The usual way to learn this is to implement the 2D case, but 2D is also the
case you can follow along to without really understanding — the corner and
gradient handling is short enough to copy without the reasoning behind it
landing. So the dimension count here comes from however many coordinates you
pass, and the lattice is built for that dimension at construction. Generalising
it means every piece has to be understood rather than transcribed:

- **Hashing.** The permutation table is the standard one, doubled to 512 so
  lookups can't run off the end. Each corner's gradient index comes from
  folding the coordinate of every dimension through it in turn.
- **Gradient selection.** Improved Perlin picks gradients from the edge
  midpoints of a cube. Generalising that needed the count: a d-dimensional
  hypercube has `d * 2^(d-1)` edges, which is 4 in 2D and 12 in 3D, matching
  the numbers in the original. The set is built by pairing opposite corners and
  taking midpoints.
- **Corners and distance vectors.** Both come from counting in binary to `2^d`
  and reading each bit as one dimension's offset, which is the trick that makes
  the whole thing dimension-agnostic.
- **The fade curve** `6t^5 - 15t^4 + 10t^3`, so the interpolation has zero
  first and second derivatives at the lattice points and the grid doesn't show
  up as visible creases.
- **Interpolation.** With `2^d` corner influences you interpolate along one
  dimension at a time, halving the number of values each pass until one is
  left. In 2D that's the familiar four-corner bilinear blend; the recursive
  form is the same thing for any d.

## State

The lattice, hashing and gradient generation work. The nested interpolation is
what I'm rewriting now — the recursion collapses to a single corner's influence
instead of blending pairs, so the output is currently values rather than noise.
The generalisation was the point of the exercise, and that part held up.

## Running

```sh
pip install numpy matplotlib
python main.py
```

Samples a 100x100 grid at a scale of 1/25 and renders it greyscale.
