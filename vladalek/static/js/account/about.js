document.addEventListener('DOMContentLoaded', () => {
	const image = document.querySelector('.image')
	const social = document.querySelector(".social_networks")
	image.addEventListener('click', () => {
		document.querySelector('.edit_avatar').style.display = "block";
	})
	social.addEventListener('click', () => {
		document.querySelector('.add_social').style.display = "block";
	})
})