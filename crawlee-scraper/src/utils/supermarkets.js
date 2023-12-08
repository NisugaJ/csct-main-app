
const SupermarketType = {
    TESCO :"TESCO",
    ASDA :"ASDA",
    SAINSBURYS :"SAINSBURYS",
    MORRISONS :"MORRISONS",
    WAITROSE :"WAITROSE",
    ALDI :"ALDI",
    LIDL :"LIDL",
    CO_OP :"CO-OP"
}

const supermarketPrefix = (supermarket_enum) => {
    return supermarket_enum + "_"
}

export {
    SupermarketType,
    supermarketPrefix
}