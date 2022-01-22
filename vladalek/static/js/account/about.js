document.addEventListener('DOMContentLoaded', () => {
	const image = document.querySelector('.image')
	const github = document.getElementById("github")
	image.addEventListener('click', () => {
		document.querySelector('.edit_avatar').style.display = "block";
	})
	github.addEventListener('click', () => {
		document.querySelector('.github').style.display = "block";
	})
})