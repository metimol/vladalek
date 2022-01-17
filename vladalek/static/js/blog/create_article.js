document.addEventListener('DOMContentLoaded', () => {
	const categorie = document.querySelector('.categorie')
	var x = document.getElementsByClassName("category_radio");
	
	categorie.addEventListener('click', () => {
		document.querySelector('.categories').style.display = "block";
	})
	
	for (var i = 0; i < x.length; i++)
	{x[i].addEventListener('click', function(e){
		document.getElementById("name_category").innerHTML = this.innerHTML;
		document.querySelector('.categories').style.display = "none";
	});}
	
	window.addEventListener('click', e => {
		const target = e.target
		if (!target.closest('.categorie') && !target.closest('.categories')){
			document.querySelector('.categories').style.display = "none";
		}
	})
})
