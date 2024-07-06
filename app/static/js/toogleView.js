function toggleView(view) {
    const scraperView = document.getElementById('scraperView');
    const parserView = document.getElementById('parserView');

    if (view === 'scraper') {
        scraperView.classList.remove('hidden');
        parserView.classList.add('hidden');
    } else if (view === 'parser') {
        scraperView.classList.add('hidden');
        parserView.classList.remove('hidden');
    }
}