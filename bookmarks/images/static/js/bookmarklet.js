const siteUrl = 'https://hendry.com:8000/';
const styleUrl = siteUrl + 'static/css/bookmarklet.css';
const minWidth = 100;
const minHeight = 100;

// Cargar CSS
const head = document.head;
const link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?r=' + Math.floor(Math.random()*9999999999999999);
head.appendChild(link);

// Cargar HTML
const body = document.body;
const boxHtml = `
  <div id="bookmarklet">
    <a href="#" id="close">&times;</a>
    <h1>Select an image to bookmark:</h1>
    <div class="images"></div>
  </div>`;
body.insertAdjacentHTML('beforeend', boxHtml);

function bookmarkletLaunch() {
  const bookmarklet = document.getElementById('bookmarklet');
  const imagesFound = bookmarklet.querySelector('.images');

  // Limpiar imágenes anteriores
  imagesFound.innerHTML = '';
  bookmarklet.style.display = 'block';

  // Evento para cerrar
  bookmarklet.querySelector('#close').addEventListener('click', () => {
    bookmarklet.style.display = 'none';
  });

  // Seleccionar TODAS las imágenes primero
  const allImages = document.querySelectorAll('img');
  
  // Filtrar imágenes válidas
  const validImages = Array.from(allImages).filter(image => {
    // Excluir imágenes Base64 (data:image)
    if (image.src.startsWith('data:')) return false;
    
    // Verificar dimensiones mínimas
    return (image.naturalWidth >= minWidth && 
            image.naturalHeight >= minHeight);
  });

  // Mostrar imágenes válidas
  validImages.forEach(image => {
    const imgElement = document.createElement('img');
    imgElement.src = image.src;
    imgElement.style.maxHeight = '200px';
    imgElement.style.margin = '5px';
    imgElement.style.border = '2px solid #ccc';
    imagesFound.appendChild(imgElement);
  });

  // Evento para seleccionar imagen
  imagesFound.querySelectorAll('img').forEach(img => {
    img.addEventListener('click', (event) => {
      const imageSelected = event.target;
      bookmarklet.style.display = 'none';
      
      // Verificar nuevamente que no sea Base64
      if (imageSelected.src.startsWith('data:')) {
        alert('No se pueden guardar imágenes embebidas (Base64)');
        return;
      }
      
      window.open(
        `${siteUrl}images/create/?url=${encodeURIComponent(imageSelected.src)}&title=${encodeURIComponent(document.title)}`,
        '_blank'
      );
    });
  });
}

// Ejecutar
bookmarkletLaunch();