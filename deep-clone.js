const obj = { a: 1, b: { c: 2, d: { e: 1, f: 2, h: 3 } } };

function deepClone(obj) {
  if (typeof obj !== "object" || obj === null) return obj;

  const clone = Array.isArray(obj) ? [] : {};

  for (let key in obj) {
    clone[key] = deepClone(obj[key]);
  }

  return clone;
}

const result = deepClone(obj);
console.log({ result });
