document.addEventListener('DOMContentLoaded', () => {
	const menu = document.querySelector('.menu')
	
	menu.addEventListener('click', () => {
		document.querySelector('.sidenav').style.width = "auto";
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