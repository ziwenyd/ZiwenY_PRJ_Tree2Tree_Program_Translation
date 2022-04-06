function isAnagram(s, t) {
    if (s.length !== t.length) {
        return false
    }
    const map = new Map();
    let count;
    for (let ch of s) {
        if (map.has(ch)) {
            count = map.get(ch);
            count++
        } else {
            count = 1;
        }
        map.set(ch, count);
    }
    for (let j of t) {
        if (map.has(j) && map.get(j)) {
            count = map.get(j);
            map.set(j, count-1);
        } else {
            return false;
        }
    }
    return true;
};