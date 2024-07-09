const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
    const browser = await puppeteer.launch({ headless: true });
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

    // Click on the "Now" element
    await page.waitForSelector('div[data-test="delivery-time"]');
    await page.click('div[data-test="delivery-time"]');

    // Wait for and click on the "Schedule" element
    await page.waitForSelector('a[data-testid="schedule-button"]');
    await page.click('a[data-testid="schedule-button"]');

    // Wait for and click on the "1:30 PM - 2:00 PM" element
    await page.waitForSelector('label[data-baseweb="radio"]');
    const timeSlots = await page.$$('label[data-baseweb="radio"]');
    for (let i = 0; i < timeSlots.length; i++) {
        const text = await timeSlots[i].evaluate(el => el.innerText);
        if (text.includes('1:30 PM - 2:00 PM')) {
            await timeSlots[i].click();
            break;
        }
    }

    // Click on the "Schedule" button
    await page.waitForSelector('div[data-testid="schedule-modal-button"] button');
    await page.click('div[data-testid="schedule-modal-button"] button');
    await new Promise(resolve => setTimeout(resolve, 3000));
    const data = JSON.parse(fs.readFileSync('restaurants.json', 'utf8'));

    for (let category in data) {
        for (let link of data[category]) {
            try {
                await page.goto(`https://www.ubereats.com${link}`);

                let name = await page.$eval('h1', el => el.innerText);
                let address = await page.$eval('ul > button:first-child', el => el.getAttribute('aria-label'));
                await page.click('button[aria-label="Open"]');
                await new Promise(resolve => setTimeout(resolve, 500));
                let hours = await page.$$eval('.hf > div', divs => {
                    let weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
                    let hours = {};
                    divs.forEach(div => {
                        let dayElement = div.querySelector('div[data-baseweb="typo-labelmedium"]');
                        let timeElement = div.querySelector('p[data-baseweb="typo-paragraphsmall"]');
                        if (dayElement && timeElement) {
                            let day = dayElement.innerText;
                            let time = timeElement.innerText.match(/\d{1,2}:\d{2} [a.p].m. - (\d{1,2}:\d{2} [a.p].m.|12:00 a.m.)/)[0];
                            let dayRange = day.split(' - ');
                            let startIndex, endIndex;
                            if (day === "Every Day") {
                                startIndex = 0;
                                endIndex = weekDays.length - 1;
                            } else if (dayRange.length === 1) {
                                startIndex = weekDays.indexOf(dayRange[0]);
                                endIndex = startIndex;
                            } else {
                                startIndex = weekDays.indexOf(dayRange[0]);
                                endIndex = dayRange[1] ? weekDays.indexOf(dayRange[1]) : startIndex;
                            }
                            for (let j = startIndex; j <= endIndex; j++) {
                                hours[weekDays[j]] = time || '';
                            }
                        }
                    });
                    return hours;
                });

                let menuItems = await page.$$eval('li[data-test^="store-item"]', items => {
                    return items.map(item => {
                        let textElements = Array.from(item.querySelectorAll('span[data-testid="rich-text"]'));
                        let name = textElements.length > 0 ? textElements[0].innerText : null;
                        let price = textElements.length > 1 ? textElements[1].innerText : null;

                        return { name, price };
                    });
                });
                console.log({ category, name, address, hours, menuItems })
                let restaurantData = { category, name, address, hours, menuItems };
                fs.appendFileSync('restaurantData.json', JSON.stringify(restaurantData, null, 2) + ',\n');
            } catch (error) {
                console.error(`Failed to process link: ${link}. Error: ${error}`);
                let errorData = { link, error: error.message };
                fs.appendFileSync('errors.json', JSON.stringify(errorData, null, 2) + ',\n');
            }
        }
    }

    await browser.close();
})();