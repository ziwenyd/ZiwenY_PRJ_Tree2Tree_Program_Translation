function atomTest() {
    var key, new_value, symbols;
    symbols = {};
    symbols["I"] = 1;
    symbols["V"] = 5;
    key = "I";
    symbols[key] = 8;
    new_value = symbols["V"];
    return new_value;
}

