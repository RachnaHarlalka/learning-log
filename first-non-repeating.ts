export {};

function nonRepeating(word: string) {
  let myMap = new Map();
  for (let ch of word) {
    const val = myMap.get(ch);
    if (val === undefined) {
      myMap.set(ch, 1);
    } else myMap.set(ch, val + 1);
  }
  for (const [char, count] of myMap) {
    if(count===1) return char
  }
  return null
}

const word = "";
const result = nonRepeating(word);
console.log({ result });
