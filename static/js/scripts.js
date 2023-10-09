const up = document.getElementById("up")
let scrolled = false

function toUp() {
  let duration = 500
  let scrollStep = -window.scrollY / (duration / 25)
  const scrollInterval = setInterval(function() {
    if (window.scrollY !== 0) {
      window.scrollBy(0, scrollStep);
    } else {
      clearInterval(scrollInterval);
    }
  }, 15);
}

up.addEventListener('click', toUp)

function handleScroll() {
  const scrollToTopButton = document.getElementById('up');
  // Если пользователь прокрутил вниз более, чем на 40 пикселей, показать кнопку, иначе скрыть
  if (window.scrollY > 40) {
    scrollToTopButton.classList.add('visible');
  } else {
    scrollToTopButton.classList.remove('visible');
  }
}

window.addEventListener('scroll', handleScroll);

