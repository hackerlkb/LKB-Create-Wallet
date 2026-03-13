const { ethers } = require('ethers');
const fs = require('fs');

// Hàm tạo nhiều ví
function generateWallets(num) {
    let wallets = [];
    for (let i = 0; i < num; i++) {
        const wallet = ethers.Wallet.createRandom();
        wallets.push({
            address: wallet.address,
            privateKey: wallet.privateKey,
            mnemonic: wallet.mnemonic.phrase
        });
    }
    return wallets;
}

// Số lượng ví bạn muốn tạo
const numWallets = 50;

// Tạo các ví
const wallets = generateWallets(numWallets);

// Tạo nội dung file CSV
let fileContent = 'Address,Private Key,Mnemonic\n'; // Dòng tiêu đề
wallets.forEach(wallet => {
    fileContent += `"${wallet.address}","${wallet.privateKey}","${wallet.mnemonic}"\n`;
});

// Ghi nội dung vào file ETH_Wallet.csv
fs.writeFile('ETH_Wallet.csv', fileContent, (err) => {
    if (err) {
        console.error('Lỗi khi ghi file:', err);
    } else {
        console.log('File ETH_Wallet.csv đã được tạo với thông tin ví.');
    }
});