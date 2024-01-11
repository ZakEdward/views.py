const siteURL = '//mysite.com:8000/';
const styleUrl = siteURL + 'static/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;

const head = document.getElementsByTagName('head')[0];
const link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random() * 9999999999999999);
link.async = true;

link.addEventListener('load', function () {
    bookmarkletLaunch();
});

head.appendChild(link);

let body = document.getElementsByTagName('body')[0], bookmarklet;
boxHtml = '<div id="bookmarklet"><a href="#" id="close">&times;</a><h1>Выберите для добавления в закладки:</h1>' +
    '<div class="images"></div></div>';
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
    bookmarklet = document.getElementById('bookmarklet');
    let imagesFound = bookmarklet.querySelector('.images');

    imagesFound.innerHTML = '';
    bookmarklet.style.display = 'block';
    bookmarklet.querySelector('#close').addEventListener('click', function(){
        bookmarklet.style.display = 'none';
    });

    let images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    images.forEach(image => {
        if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
            let imageFound = document.createElement('img');
            imageFound.src = image.src;
            imagesFound.append(imageFound);
        }
    });

    imagesFound.querySelectorAll('img').forEach(image => {
        image.addEventListener('click', function (event){
            let imageSelected = event.target;
            bookmarklet.style.display = 'none';
            window.open(siteURL + 'images/create/?url='
                + encodeURIComponent(imageSelected.src)+ '&title='
            + encodeURIComponent(document.title), '_blank');
        })
    })
}

bookmarkletLaunch();