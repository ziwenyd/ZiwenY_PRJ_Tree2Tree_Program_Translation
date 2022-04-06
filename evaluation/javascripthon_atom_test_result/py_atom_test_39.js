function atomTest() {
    var a, s;
    s = [1, 2, 3, 4, 5];
    a = 0;
    for (var i = 0, _pj_a = s.length; (i < _pj_a); i += 1) {
        if (((i + 1) >= s.length)) {
            a = (- 1);
        }
        if ((s[i] < s[(i + 1)])) {
            a = s[i];
        } else {
            a = (- 1);
        }
    }
    return a;
}

