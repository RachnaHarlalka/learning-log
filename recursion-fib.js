// 0 1 1 2 3 5 8 13 21

// fib(0) + fib(1) = fib(2)

function fib(n) {
  if (n === 0 || n === 1) return n;
  return fib(n - 2) + fib(n - 1);
}

console.log(fib(6));
