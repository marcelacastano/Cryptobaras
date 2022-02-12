const layersOrder = [
    { name: 'backgroundS', number: 6 },
    { name: 'faces', number: 6 },
    { name: 'hats', number: 50 },
    { name: 'glasses', number: 25 },

];
  
const format = {
    width: 500,
    height: 500
};

const rarity = [
    { key: "", val: "original" },
    { key: "_r", val: "rare" },
    { key: "_sr", val: "super rare" },
];

const defaultEdition = 100;

module.exports = { layersOrder, format, rarity, defaultEdition };