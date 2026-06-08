let nums = [2, 7, 11, 15];
let target = 9;

function twoSum(nums, target) {
  let myMap = new Map();

  for (let i = 0; i < nums.length; i++) {
    let secondNum = target - nums[i];
    if (myMap.get(secondNum) === undefined) {
      myMap.set(nums[i], i);
    } else return [i, myMap.get(secondNum)];
  }
  return null;
}

console.log(twoSum(nums, target));
