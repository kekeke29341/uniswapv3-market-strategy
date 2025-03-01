require('dotenv').config();
const { ethers } = require("ethers");

const provider = new ethers.providers.JsonRpcProvider(process.env.INFURA_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);
const contract = new ethers.Contract(
    process.env.UNISWAP_POOL_ADDRESS,
    require("./UniswapV3PoolABI.json"),
    wallet
);

async function provideLiquidity() {
    const tx = await contract.mint(
        process.env.TOKEN0_ADDRESS,
        process.env.TOKEN1_ADDRESS,
        process.env.LOWER_TICK,
        process.env.UPPER_TICK,
        process.env.LIQUIDITY_AMOUNT,
        { gasLimit: 500000 }
    );
    console.log("Transaction hash:", tx.hash);
}

provideLiquidity();
