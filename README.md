<h1 align="center">NFT - Digital Art</h1>

<p align="center">
  <img width="1000" height="700" src="https://user-images.githubusercontent.com/78571802/154812018-2119ef56-643d-4372-84b0-219848b5c279.png">
</p>

In this project, we showcase our journey from creating our NFT idea to the full minting and deployment of our smart contract and Dapp.

## The source code for nft creation:

``` sh
https://github.com/HashLips/hashlips_art_engine/blob/main/src/config.js
```

## The latest version of node installed:
``` sh
node -v  # To check node js version
v16.14.0 # version installed
```

## Layers Created:
We developed our concept and determined how many layers we added to our capybara. Then, we utilized canva.com to design the layers and format them appropriately. Next, the different layers were created and named as folders in the 'layers' directory. Finally, we included all the layer assets. 

## Layers added:
``` sh
- Backgrounds
- Faces
- Glasses
- Hats
```
The assets were named with a rarity weight attached in the file name like so: `green_bg#10.png`. Where the variable, `rarityDelimiter`, is denoted by the delimiter `#`
The layer assets labeled with `#10` (for regular), `#5` (for rare assets), and `#2` (for super rare).

<p align="center">
  <img width="1000" height="700" src="https://user-images.githubusercontent.com/78571802/154819392-b3d478ea-14cf-4655-a8d1-f7680734b97f.png">
</p>

## Layer Configurations
Multiple different `layerConfigurations` were added to the collection. 
```js
const layerConfigurations = [
  {
    // Creates up to 60 artworks
    growEditionSizeTo: 60,
    layersOrder: [
      { name: "Backgrounds" },
      { name: "Faces" },
      { name: "Glasses" },
      { name: "Hats" },
    ],
  },
  {
    // Creates an additional 20 artworks with hats omitted
    growEditionSizeTo: 80,
    layersOrder: [
      { name: "Backgrounds" },
      { name: "Faces" },
      { name: "Glasses" },
    ],
  },
  {
    // Creates an additional 20 artworks with glasses omitted
    growEditionSizeTo: 100,
    layersOrder: [
      { name: "Backgrounds" },
      { name: "Faces" },
      { name: "Hats" },
    ],
  },
];
```
We mixed up the `layerConfigurations` order on how the images are saved by setting the variable `shuffleLayerConfigurations` in the `config.js` file to true. 
This meant that the images would be saved in a shuffle order.

<p align="center">
  <img width="1000" height="400" src="https://user-images.githubusercontent.com/78571802/154820397-f0c3df48-cfd8-4f35-ac67-abdab8b4c907.png">
</p>

## Build
The images to be created were outputted to the `build/images` directory and the json in the `build/json` directory:

```sh
node index.js
```

The program will output all the images in the `build/images` directory along with the metadata files in the `build/json` directory. Each collection will have a `_metadata.json` file that consists of all the metadata in the collection inside the `build/json` directory. 

<p align="center">
  <img width="1000" height="700" src="https://user-images.githubusercontent.com/78571802/154820290-c4372a19-af6e-492b-8f41-63a4950b490b.png">
</p>

The `build/json` folder also will contain all the single json files that represent each image file. The single json file of a image looks like this:
```json
{
  "name": "Cryptobaras #1",
  "description": "To Be Or Not To Be Cryptobara",
  "image": "ipfs://QmXwnf99NoKwVvKpJ5WnrEmbbqtpEarJqF6jUXUzmkSZhk/1.png",
  "dna": "a350a741f5ee6e5a6242ff9fe1e360faa3672d7f",
  "edition": 1,
  "date": 1644770031593,
  "attributes": [
    {
      "trait_type": "Backgrounds",
      "value": "yellow_bg"
    },
    {
      "trait_type": "Faces",
      "value": "moss_capy"
    },
    {
      "trait_type": "Glasses",
      "value": "blue_shades"
    },
    {
      "trait_type": "Hats",
      "value": "pink_sun_hat"
    }
  ],
  "compiler": "HashLips Art Engine"
}
```
## General Metadata
Metadata is particularly important in creating NFTs. It is the image’s information - it contains information such as the name, description, image IPSF, DNA, edition attributes, etc. This information will be displayed on OpenSea attributes.

```js
// General metadata for Ethereum
const namePrefix = "CryptoBara_TestRun";
const description = "To Be Or Not To Be A CryptoBara";
const baseUri = "ipfs://QmXwnf99NoKwVvKpJ5WnrEmbbqtpEarJqF6jUXUzmkSZhk"
```

### Generate a preview image!

Create a preview image collage of your collection, run:
```sh
npm run preview
```
<p align="center">
  <img width="1000" height="500" src="https://user-images.githubusercontent.com/78571802/154804730-d64e30d5-3760-436e-83e1-b2cc989acace.png">
</p>

### Generate GIF images from collection

In order to export gifs based on the layers created, we set the export on the `gif` object in the `src/config.js` file to `true`. 
Setting the `repeat: -1` will produces a one time render and `repeat: 0` produces loop forever.
```js
const gif = {
  export: true,
  repeat: 0,
  quality: 100,
  delay: 500,
};
```
<p align="center">
  <img width="1000" height="800" src="https://user-images.githubusercontent.com/78571802/154199809-dd13384c-8ae4-4c1f-a687-fa89d9217263.gif">
</p>

## Printing rarity data (Experimental feature)
To see the percentages of each attribute across the collection, run:
```sh
npm run rarity
```

For example, the red glasses has a weight of #10, tricolor glasses has a weight of #2 (which makes them super rare), and the yellow shades has a weight of #5 (which makes them rate). The output looks like this:

```sh
...
Trait type: Glasses
{
  trait: 'red_frame',
  weight: '10',
  occurrence: '19 in 100 editions (19.00 %)'
}
{
  trait: 'tricolor_glasses_sr',
  weight: '2',
  occurrence: '2 in 100 editions (2.00 %)'
}
{
  trait: 'yellow_shades_r',
  weight: '5',
  occurrence: '5 in 100 editions (5.00 %)'
}
...
```
## Pixelated Images
Pixelate.js will take your current images and pixalate them, by running the code below. The pixalated images are stored in a new images folder.

```sh
node utils/pixelate.js
```

### Here is a pixelated image

![1](https://user-images.githubusercontent.com/78571802/154820995-17ee3e3b-34bf-4cb4-8cde-45f428f177cc.png)



The images folder was then uploaded to ![pinata](https://user-images.githubusercontent.com/78571802/154200040-ed70f0aa-9aad-4c77-99d2-7e4a721f9f23.png)
We used Pinata to host and upload our images; here we obtained the images' CID

![Screen Shot 2022-02-16 at 12 13 20 AM](https://user-images.githubusercontent.com/78571802/154200646-e71212bf-0639-4138-bba1-be1ced303e24.png)


# Creation of Smart Contract
   
## Open Zeppelin Imports
```sh
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
```
## Smart Contract
https://user-images.githubusercontent.com/78571802/154875417-5b312d2a-9862-4e02-869b-00d95a132886.mov

## Dapp Code
https://user-images.githubusercontent.com/78571802/154873863-e78323f3-f775-488e-bdd0-368490172596.mov


## Contract on Rinkeby Network
![Screen Shot 2022-02-16 at 12 21 00 AM](https://user-images.githubusercontent.com/78571802/154201646-77b48027-2d23-42cb-a850-d87abcc71676.png)

## Minted Collection on Opensea Testnet
![Screen Shot 2022-02-16 at 12 22 55 AM](https://user-images.githubusercontent.com/78571802/154201705-7686d1d3-f17a-4c64-b833-7d8ec0bc7215.png)

<h1 align="center">✨✨The Cryptobara Collection✨✨</h1>

![preview](https://user-images.githubusercontent.com/78571802/154811191-6f7aa3cb-5dd7-4927-8b89-b02a54e77ebc.png)
