function atomTest() {
    const symbols = new Map()
    symbols.set("I", 1)
    symbols.set("V", 5)
    key = "I"
    symbols.delete(key)
    if (symbols.has(key)){
        return true
    }
    return false
}
    