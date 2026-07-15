// Structure it like this:
const obj = { a: 1, b: { c: 2, d: { e: 1, f: 2, h: 3 } } };

function deepClone(obj) {
  if (typeof obj !== "object" || obj === null) return obj;

  let clone = {};

  for (let [key, value] of Object.entries(obj)) {
    clone[key] = deepClone(value);
  }
  return clone;
}

console.log(deepClone(obj));
