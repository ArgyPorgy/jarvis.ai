function generateProductKey() {
    const keyLength = 16;
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let productKey = '';

    for (let i = 0; i < keyLength; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        productKey += characters.charAt(randomIndex);
    }

    return productKey;
}

// Example usage


const contract_abi = [
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "key",
				"type": "string"
			}
		],
		"name": "addProductKey",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "key",
				"type": "string"
			}
		],
		"name": "invalidateProductKey",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "key",
				"type": "string"
			}
		],
		"name": "ProductKeyAdded",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": false,
				"internalType": "string",
				"name": "key",
				"type": "string"
			}
		],
		"name": "ProductKeyInvalidated",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "productKeys",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "key",
				"type": "string"
			}
		],
		"name": "verifyProductKey",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
async function purchaseWithMetamask() {
    var email = document.getElementById('email').value;
    var name = document.getElementById('name').value;
    if (typeof window.ethereum === 'undefined') {
        alert('Please install MetaMask to proceed.');
        return;
    }

    try {
        // Get the current accounts from MetaMask
        const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });

        if (accounts.length === 0) {
            alert('No accounts found in MetaMask. Please check your setup.');
            return;
        }

        const senderAddress = accounts[0]; // Use the first account as the sender

        // Specify the recipient address
        const recipientAddress = '0x998F8Fca5845908E83FFe299b98eC3F5c05b3093'; // Replace with the recipient's address

        // Define transaction parameters
        const transactionParameters = {
            from: senderAddress,
            to: recipientAddress,
            value: '0x0', // Set value to 0 for token transfers
        };

        // Use MetaMask's built-in UI for sending transactions
        const transactionHash = await window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [transactionParameters],
        });
        const web3 = new Web3(window.ethereum);
        const contract_address = "0xf5a01b2c617Ff413E2d821B943E5Bf690bda064B"
        const contract = new web3.eth.Contract(contract_abi, contract_address);
        const pkey = generateProductKey();
        const result = await contract.methods.addProductKey(pkey).send({
            from: senderAddress,
          })
          .on('transactionHash', function(hash) {
              console.log('Transaction Hash:', hash);
          })
          .on('confirmation', function(confirmationNumber) {
              if (confirmationNumber === 1) { 
                alert("payment confirmed");
              }
            });

        console.log('Transaction sent! Transaction hash:', transactionHash);

        // Wait for the transaction to be mined (you might want to use a better solution in a production environment)
        await waitForTransactionConfirmation(transactionHash);

        // Retrieve the updated transaction details
        const transactionDetails = await window.ethereum.request({
            method: 'eth_getTransactionByHash',
            params: [transactionHash],
        });

        console.log('Transaction mined! Block number:', transactionDetails.blockNumber);
        
        sendTransactionDetailsToServer(pkey, email, name);

        // Create a Blob with the transaction hash content
        const blob = new Blob([transactionHash], { type: 'text/plain' });

        // Create a download link
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'fck.txt';

        // Append the link to the body and click it to trigger the download
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
        

        alert('Transaction successful! Transaction hash downloaded as a file.');
    } catch (error) {
        console.error(error);
        alert('Transaction failed. Please check your MetaMask and try again.');
    }
}

async function waitForTransactionConfirmation(transactionHash) {
    return new Promise((resolve, reject) => {
        const checkConfirmation = async () => {
            const receipt = await window.ethereum.request({
                method: 'eth_getTransactionReceipt',
                params: [transactionHash],
            });

            if (receipt && receipt.blockNumber) {
                resolve();
            } else {
                setTimeout(checkConfirmation, 1000); // Check again in 1 second
            }
        };

        checkConfirmation();
    });
}


document.getElementById('razorpayForm').addEventListener('submit', function (e) {
    // Prevent the form from submitting (Razorpay will handle it)
    e.preventDefault();
});

// Razorpay handler function
function razorpayHandler(response) {
    // Log payment success to the console
    console.log('Payment successful! Payment ID:', response.razorpay_payment_id);
    var email = document.getElementById('email').value;
    var name = document.getElementById('name').value;
    sendTransactionDetailsToServer(response.razorpay_payment_id, email, name)
}


function sendTransactionDetailsToServer(productKey, email, name) {
        fetch('/process-transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({productKey, email, name }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to notify server');
            }
            console.log('Notification sent to server');
        })
        .catch(error => {
            console.error('Error notifying server:', error.message);
        });
    }