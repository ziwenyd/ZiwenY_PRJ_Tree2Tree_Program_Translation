function atomTest() {
    const symbols = new Map()
    symbols.set("I", 1)
    symbols.set("V", 5)
    key = "I"
    symbols.set(key, 8)
    new_value = symbols.get(key)
    return new_value
}
    