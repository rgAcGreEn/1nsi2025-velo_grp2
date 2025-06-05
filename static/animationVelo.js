const canvas = document.getElementById("canvas");
const contexte = canvas.getContext("2d");
const image = document.createElement("img");

const tempsAnimation = 5;
canvas.style.left = "0px";

image.src = "/static/vélo.png";
image.onload = (() => {
	contexte.drawImage(image,0,0);
	const animationVelo = setInterval(() => {
		const positionCanvas = parseInt(canvas.style.left.slice(0,-2));
		if (positionCanvas+canvas.width+1 >= window.innerWidth) {
			clearInterval(animationVelo);
		}
		canvas.style.left = (parseInt(canvas.style.left)+1).toString() + "px";
	},tempsAnimation/(window.innerWidth-canvas.width));
});