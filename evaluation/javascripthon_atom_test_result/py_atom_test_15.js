var _pj;
function _pj_snippets(container) {
    function in_es6(left, right) {
        if (((right instanceof Array) || ((typeof right) === "string"))) {
            return (right.indexOf(left) > (- 1));
        } else {
            if (((right instanceof Map) || (right instanceof Set) || (right instanceof WeakMap) || (right instanceof WeakSet))) {
                return right.has(left);
            } else {
                return (left in right);
            }
        }
    }
    container["in_es6"] = in_es6;
    return container;
}
_pj = {};
_pj_snippets(_pj);
function atomTest() {
    var key, symbols;
    symbols = {};
    symbols["I"] = 1;
    symbols["V"] = 5;
    key = "I";
    if (_pj.in_es6(key, symbols)) {
        return true;
    }
    return false;
}

