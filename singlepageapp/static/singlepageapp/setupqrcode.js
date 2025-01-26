const TEMP_CODE = 12345
const TEMP_ID = "131607b8-947c-4621-8bbe-2ee24c0dc43d"

const formatUrl = (code, price, id) =>
	"https://mobilepay.fi/Yrityksille/Maksulinkki/maksulinkki-vastaus"
	+ `?phone=${code}&amount=${price}&comment=Namubufferi-${id}&lock=1`

var code = new QRCode("qrcode", {correctLevel: QRCode.CorrectLevel.L});

function generateQR() {
	var price = document.getElementById('qrcode-price').value;
	code.makeCode(formatUrl(TEMP_CODE, price, TEMP_ID));
}

document.getElementById('qrcode-submit').onclick = generateQR;
