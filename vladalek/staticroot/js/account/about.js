document.addEventListener('DOMContentLoaded', () => {
	const image = document.querySelector('.image')
	const bookmark = document.getElementById("bookmark")
	const articles = document.getElementById("articles")
	image.addEventListener('click', () => {
		document.querySelector('.edit_avatar').style.display = "block";
	});
	bookmark.addEventListener('click', () => {
		document.querySelector('.favourites').style.display = "block";
	});
	articles.addEventListener('click', () => {
		document.querySelector('.articles').style.display = "block";
	});
})