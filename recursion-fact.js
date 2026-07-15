function fact(n) {
  if (n === 0) {
    return 1;
  }

  let f = n * fact(n - 1);
  return f;
}

console.log(fact(5));
