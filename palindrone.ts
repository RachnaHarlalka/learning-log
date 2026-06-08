export {};

function isPallindrone(word: string) {
  let i = 0;
  let cleanedWord = word.toLowerCase().replaceAll(" ", "");
  let j = cleanedWord.length - 1;

  while (i < Math.floor(cleanedWord.length / 2)) {
    if (cleanedWord[i].toLowerCase() !== cleanedWord[j].toLowerCase()) {
      return false;
    }
    i++;
    j--;
  }
  return true;
}

let word = "abccba";
const result = isPallindrone(word);
console.log({ result });
