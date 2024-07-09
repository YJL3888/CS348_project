const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    // Navigate to the website
    // Navigate to the website
    await page.goto('https://www.ubereats.com/ca');

    // Wait for the search input to load
    await page.waitForSelector('#location-typeahead-home-input');

    // Type the address into the search input
    await page.type('#location-typeahead-home-input', '200 University Avenue, Waterloo, ON');

    // Wait for the search results to load
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Click the search result for "200 University Avenue West" in "Waterloo, ON"
    const searchResults = await page.$$('#location-typeahead-home-menu > li');
    for (let i = 0; i < searchResults.length; i++) {
        const text = await searchResults[i].evaluate(el => el.innerText);
        if (text.includes('200 University Ave W') && text.includes('Waterloo, Ontario')) {
            await searchResults[i].click();
            break;
        }
    }
    // Wait for the "Grocery" link to appear
    // Wait for the links to appear
    await page.waitForSelector('a[data-testid="shortcut-refresh-button"]');

    // Find all the links
    const links = await page.$$eval('a[data-testid="shortcut-refresh-button"]', anchors => {
        return anchors.map(anchor => {
            const span = anchor.querySelector('span[data-testid="rich-text"]');
            const category = span ? span.innerText : '';
            const href = anchor.getAttribute('href');
            return { category, href };
        });
    });

    // Filter out the "Grocery" link
    const filteredLinks = links.filter(link => link.category !== 'Grocery' && link.category !== 'Alcohol');

    const allLinks = new Set();
    const baseURL = 'https://www.ubereats.com';
    
    const categories = {};
    
    for (const link of filteredLinks) {
        // Navigate to the link
        await page.goto(baseURL + link.href);
    
        // Wait for the links to appear
        await page.waitForSelector('div[data-testid="store-card"] a[data-testid="store-card"]');
    
        // Find and collect all the links
        const storeLinks = await page.$$eval('div[data-testid="store-card"] a[data-testid="store-card"]', anchors => {
            return anchors.map(anchor => anchor.getAttribute('href'));
        });
    
        // Filter out the links that have already been added
        const uniqueLinks = storeLinks.filter(storeLink => !allLinks.has(storeLink));
    
        // Add the unique links to the category
        categories[link.category] = uniqueLinks;
    
        // Add the unique links to the Set
        for (const uniqueLink of uniqueLinks) {
            allLinks.add(uniqueLink);
        }
    
        // Write the categories to a JSON file
        fs.writeFileSync('restaurants.json', JSON.stringify(categories, null, 2));
    }
    await browser.close();
})();