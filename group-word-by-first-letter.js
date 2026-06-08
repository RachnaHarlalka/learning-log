let arr = ["apple", "bat", "apricot", "banana"];
// let result = { a: ["apple", "apricot"], b: ["bat", "banana"] };

function groupByFirstLetter(arr) {
  let result = {};

  for (let word of arr) {
    const letterArr = result[word[0]];
    if (letterArr !== undefined) letterArr.push(word);
    else result[word[0]] = [word];
  }
  return result;
}

const result = groupByFirstLetter(arr);
console.log({ result });
