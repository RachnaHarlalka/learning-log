"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
function charFrequency(word) {
    var obj = {};
    var cleanedWord = word.toLowerCase().replaceAll(" ", "");
    for (var _i = 0, cleanedWord_1 = cleanedWord; _i < cleanedWord_1.length; _i++) {
        var char = cleanedWord_1[_i];
        if (obj[char]) {
            obj[char] += 1;
        }
        else
            obj[char] = 1;
    }
    return obj;
}
var word = "hello";
var freq = charFrequency(word);
console.log({ freq: freq });
