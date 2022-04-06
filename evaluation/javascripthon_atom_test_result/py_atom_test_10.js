function atomTest() {
    var result, s;
    s = "()[]{}";
    result = [];
    for (var c, _pj_c = 0, _pj_a = s, _pj_b = _pj_a.length; (_pj_c < _pj_b); _pj_c += 1) {
        c = _pj_a[_pj_c];
        result.append(c);
    }
    return result;
}

