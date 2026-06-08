let arr = [1, [2, 3], 4, [5, [3, 8, [9, 5, 0]]]];

// function flatten(arr, output = []) {
//   for (let item of arr) {
//     if (Array.isArray(item)) {
//       flatten(item, output);
//     } else output.push(item);
//   }
//   return output;
// }

// const result = flatten(arr);
// console.log({ result });

function flatten(arr) {
  const output = [];
  function helper(arr) {
    for (let item of arr) {
      if (Array.isArray(item)) {
        helper(item);
      } else output.push(item);
    }
    return output;
  }
  helper(arr);
  return output;
}

const result = flatten(arr);
console.log(result);
