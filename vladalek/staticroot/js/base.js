document.addEventListener('DOMContentLoaded', () => {
	const menu = document.querySelector('.menu')
	const closebtn = document.getElementById("closebtn")
	
	closebtn.addEventListener('click', () => {
		document.querySelector('.sidenav').style.width = "0";
		document.body.style.removeProperty('overflow');
	})
	
	menu.addEventListener('click', () => {
		document.querySelector('.sidenav').style.width = "250px";
		document.body.style.overflow = "hidden";
	})
	
	window.addEventListener('click', e => {
		const target = e.target
		if (!target.closest('.sidenav') && !target.closest('.menu')){
			document.querySelector('.sidenav').style.width = "0";
			document.body.style.removeProperty('overflow');
		}
	})
})