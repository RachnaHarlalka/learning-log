const arr = [1, 2, [3, 4, [5]]];

function nestedSum(arr) {
  if (!Array.isArray(arr)) {
    return arr;
  }

  for (let item of arr) {
    if (Array.isArray(item)) {
      sum = sum;
    }
  }
}

function print(n) {
  if (n <= 1) {
    console.log(n);
    return;
  }

  console.log(n);
  print(n - 1);
}

print(10);
