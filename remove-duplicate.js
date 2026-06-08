function removeDuplicate(word) {
  const obj = {};
  let result = "";
  for (let ch of word) {
    if (obj[ch] === undefined) {
      obj[ch] = 1;
      result += ch;
    }
  }
  return result;
}

let word = "bananas";

const result = removeDuplicate(word);
console.log({ result });
