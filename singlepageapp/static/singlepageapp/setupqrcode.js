const TEMP_CODE = 12345
const TEMP_ID = "131607b8-947c-4621-8bbe-2ee24c0dc43d"

const formatUrl = (code, price, message) =>
	"https://mobilepay.fi/Yrityksille/Maksulinkki/maksulinkki-vastaus"
	+ `?phone=${code}&amount=${price}&comment=${message}&lock=1`

var code = new QRCode('qrcode', {correctLevel: QRCode.CorrectLevel.L});

function generateQR() {
	var uuid = TEMP_ID

	const uuid_start = /^[0-9a-f]{8}/;
	if (!uuid_start.test(uuid)) { throw new TypeError("Given ID is not a UUID"); }

	/* The first 8 characters resulted in <0.02% collisions over 1,000,000 inserts
	 * This "Display Identifier" will not cause major issues in the rare collision
	 * 8 is therefore enough, and is easier to read (and is less data in the QR) */
	var message = "Namubufferi-" + uuid.slice(0,8).toUpperCase();

	var price_string = document.getElementById('qrcode-price').value;
	var price_float = parseFloat(price_string);
	var price = Math.floor(price_float * 100) / 100; // Concatenate to 2 decimals
	if (price < 5.0) { throw new Error("Minimum transfer amount is 5"); }

	var url = formatUrl(TEMP_CODE, price, message);
	code.makeCode(url);
	document.getElementById('qrcode-link').setAttribute('href', url);
}

document.getElementById('qrcode-submit').onclick = generateQR;
