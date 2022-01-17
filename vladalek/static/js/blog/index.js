let loaded = true;

document.addEventListener('DOMContentLoaded', () => {
	const open = document.querySelector('.open')
	const categories = document.querySelector('.categories')
	
	open.addEventListener('click', () => {
		if (loaded){
			categories.style.height = "auto";
			open.style.borderBottomRightRadius = "0";
			open.style.borderBottomLeftRadius = "0";
			document.getElementById("ion").style.transform = "rotate(180deg)";
			loaded = false;
		} else {
			categories.style.height = "0";
			open.style.borderRadius = "8px";
			document.getElementById("ion").style.transform = "rotate(0deg)";
			loaded = true;
		}
	})
	
	window.addEventListener('click', e => {
		const target = e.target
		if (!target.closest('.open') && !target.closest('.categories')){
			categories.style.height = "0";
			open.style.borderRadius = "8px";
			document.getElementById("ion").style.transform = "rotate(0deg)";
			loaded = true;
		}
	})
})
