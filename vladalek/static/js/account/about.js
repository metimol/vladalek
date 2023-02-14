document.addEventListener('DOMContentLoaded', () => {
	const image = document.querySelector('.image')
	const bookmark = document.getElementById("bookmark")
	image.addEventListener('click', () => {
		document.querySelector('.edit_avatar').style.display = "block";
	});
	bookmark.addEventListener('click', () => {
		document.querySelector('.favourites').style.display = "block";
	});
})