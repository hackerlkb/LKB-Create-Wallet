import sys, getopt
from web3 import Web3
from tqdm import tqdm
from mnemonic import Mnemonic  # Thư viện để tạo seed phrase
from eth_account import Account

# Get key from infura.io
KEY = "2c7d347514a44365aed6826b14faac88"
ethereumWallet = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{KEY}'))

# Khởi tạo đối tượng Mnemonic với ngôn ngữ English
mnemo = Mnemonic("english")

def search(searchText, inText):
    if searchText != '' and searchText in inText:
        return True
    return False

def writeWallet(file, data, seed_phrase):
    file.write("ACCOUNT %i: \n" % data.i)
    file.write("Seed Phrase: %s\n" % seed_phrase)  # Ghi seed phrase
    file.write("Public Key: %s\n" % data.address)
    file.write("Private Key: %s\n" % data._private_key.hex())
    file.write("===============================================\n\n")

def wallet(howManyWallet, outputfile, searchText=''):

    # Checking input 
    if howManyWallet == '' and outputfile == '':
        howManyWallet = int(input(" [-] Số lượng ví muốn tạo: ") or "50")
        outputfile = str(input(" [-] Nhập tên file lưu trữ (mặc định: wallet.txt)? ") or "wallet.txt")

    elif howManyWallet == '':
        howManyWallet = int(input(" [-] Số lượng ví muốn tạo: ") or "50")

    elif outputfile == '':
        outputfile = str(input(" [-] Nhập tên file lưu trữ (mặc định: wallet.txt)? ") or "wallet.txt")

    # Open filename
    walletFileName = open(outputfile, "w")

    # Loop creating wallet
    for i in tqdm(range(howManyWallet)):
        i = i + 1

        # Tạo seed phrase 24 từ
        seed_phrase = mnemo.generate(strength=256)  # 24 từ
        # Tạo private key từ seed phrase
        private_key = mnemo.to_seed(seed_phrase).hex()

        # Tạo account từ private key
        account = ethereumWallet.eth.account.create(private_key)
        account.i = i

        if search(searchText, account.address) == True:
            # Search Wallet Mode Enable
            tqdm.write(" Đã tìm thấy ví %s" % account.address)
            writeWallet(walletFileName, account, seed_phrase)

        elif searchText == '':
            # Normal Wallet Mode Enable
            tqdm.write(" Saving wallet: %s" % account.address)
            writeWallet(walletFileName, account, seed_phrase)

    walletFileName.close()
    print(f" [+] Hoàn tất lưu tại '{outputfile}'!")

def main(argv):

    howManyWallet = ''
    outputFile = ''
    searchText = ''
    errors = f'OPTIONS\n\
            Run Command: ./{sys.argv[0]} -i <numberwallet> -o <outputfile> -s <search>\n\
            Options:\n\
            [-i]: Số ví muốn tạo (định dạng số)\n\
            [-o]: Tên file muốn lưu\n\
            [-s]: Từ muốn tìm\
            '
    helpers = errors

    try:
        opts, args = getopt.getopt(argv, "hi:o:s:", ["numberwallet=", "outputfile=", "search="])

    except getopt.GetoptError:
        print(errors)
        sys.exit()

    for opt, arg in opts:

        if opt == '-h':
            print(helpers)
            sys.exit()

        elif opt in ("-i", "--numberwallet"):
            howManyWallet = arg

        elif opt in ("-o", "--outputfile"):
            outputFile = arg

        elif opt in ("-s", "--search"):
            searchText = arg

        elif opt not in ("-i", "-o", "-s", "--numberwallet", "--outputfile", "--search"):
            print(errors)

    try:
        howManyWallet = howManyWallet != '' and int(howManyWallet) or ''
    except ValueError as er:
        print(errors)
        sys.exit()

    wallet(howManyWallet, outputFile, searchText)

if __name__ == '__main__':
    main(sys.argv[1:])
