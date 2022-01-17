document.addEventListener('DOMContentLoaded', () => {
	const image = document.querySelector('.image')
	image.addEventListener('click', () => {
		document.querySelector('.edit_avatar').style.display = "block";
	})
})