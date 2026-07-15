function sum(n) {
  if (n === 1) return 1;

  let s = n + sum(n - 1);
  return s;
}

console.log(sum(5));
