const slider = document.querySelector('.slider');
const beforeImage = document.querySelector('.before');
const afterImage = document.querySelector('.after');
const comparisonContainer = document.querySelector('.comparison-container');

const slide = (xPos) => {
    let containerRect = comparisonContainer.getBoundingClientRect();
    let offsetX = xPos - containerRect.left;

    if (offsetX < 0) offsetX = 0;
    if (offsetX > containerRect.width) offsetX = containerRect.width;

    slider.style.left = offsetX + 'px';
    afterImage.style.clipPath = `inset(0 0 0 ${offsetX}px)`;
}

slider.addEventListener('mousedown', () => {
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', () => {
        window.removeEventListener('mousemove', onMouseMove);
    });
});

const onMouseMove = (e) => slide(e.clientX);

comparisonContainer.addEventListener('touchstart', (e) => {
    window.addEventListener('touchmove', onTouchMove);
    window.addEventListener('touchend', () => {
        window.removeEventListener('touchmove', onTouchMove);
    });
});
document.getElementById('fileInput').addEventListener('change', function() {
    var fileName = this.files[0].name;
    document.getElementById('fileName').textContent = fileName;
});