function toggleView(view) {
    const scraperView = document.getElementById('scraperView');
    const parserView = document.getElementById('parserView');
    const scraperButton = document.getElementById('scraperButton');
    const parserButton = document.getElementById('parserButton');

    if (view === 'scraper') {
        scraperView.classList.remove('hidden');
        parserView.classList.add('hidden');
        scraperButton.classList.add('active');
        parserButton.classList.remove('active');
        createScraperChart(scraperData);
    } else if (view === 'parser') {
        scraperView.classList.add('hidden');
        parserView.classList.remove('hidden');
        scraperButton.classList.remove('active');
        parserButton.classList.add('active');
        createParserChart(parserData);
    }
}