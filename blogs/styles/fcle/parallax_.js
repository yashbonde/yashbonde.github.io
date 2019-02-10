const parallax = document.getElementById("parallax");

window.addEventListener("scroll", function(){
	// we add an event listener and get the offset of the page
	// we have an a vague function
	let offset = window.pageYOffset;

	// if our page moves by 100 px
	// image moves by 70px
	parallax.style.backgroundPositionY = (offset) * 0.5 + 'px';
	console.log("Offset:" + offset);
	console.log("Offset*0.7: " + offset * 0.7);
	console.log(document.body.clientHeight/20);
	
	// this is causing issues such as the nav bar moves along with the rest
	// of the page and thus creates white space

})