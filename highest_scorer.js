let scores = [
  { name: "Alice", score: 80 },
  { name: "Bob", score: 95 },
];
let result = { name: "Bob", score: 95 };

function findHighScorer(scores) {
  if (scores.length < 1) return null;
  return scores.reduce((acc, curr) => {
    if (curr.score > acc.score) {
      return curr;
    } else return acc;
  });
}

console.log(findHighScorer(scores));
