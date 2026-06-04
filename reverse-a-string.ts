function swapNumbers(a: number, b: number, strArr: string[]) {
  let temp;
  temp = strArr[a];
  strArr[a] = strArr[b];
  strArr[b] = temp;
}

function ReverseString(str: string) {
  let i = 0;
  let j = str.length - 1;
  const strArr = str.split("");
  while (i < j) {
    swapNumbers(i, j, strArr);
    i++;
    j--;
  }
  return strArr.join("");
}

const reversedStr = ReverseString("apple");
console.log({ reversedStr });
