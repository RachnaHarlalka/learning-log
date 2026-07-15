function nestedSum(arr) {
  if (typeof arr === "number") return arr;
  let sum = 0;
  for (let item of arr) {
    sum += nestedSum(item);
  }

  return sum;
}

console.log(nestedSum([1, 2, [3, 4, [5]]]));
