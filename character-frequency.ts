export {};

function charFrequency(word: string) {
  const obj: Record<string, number> = {};
  let cleanedWord = word.toLowerCase().replaceAll(" ", "");
  for (let char of cleanedWord) {
    if (obj[char]) {
      obj[char] += 1;
    } else obj[char] = 1;
  }
  return obj;
}

let word = "hello";
const freq = charFrequency(word);
console.log({ freq });
