function isSorted(arr, n) {
  if (n === 1) {
    console.log("hi");
    return true;
  }
  if (arr[n - 1] < arr[n - 2]) return false;

  return isSorted(arr, n - 1);
}

if (isSorted([1, 2, 3, 8, 5], 5)) {
  console.log("true");
} else console.log("false");
