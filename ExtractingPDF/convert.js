const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');
const axios = require('axios');

// Ensure that a directory exists, if not create it
function ensureDirectoryExists(directory) {
    if (!fs.existsSync(directory)) {
        fs.mkdirSync(directory, { recursive: true });
    }
}

// Fetch the HTML content of a URL
async function fetchUrlContent(url) {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error(`Error fetching URL content: ${error}`);
        return null;
    }
}

// Convert HTML to PDF using Puppeteer
async function convertHtmlToPdf(htmlContent, outputFile) {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();

        // If HTML content is a URL, navigate to it
        if (isValidUrl(htmlContent)) {
            await page.goto(htmlContent, { waitUntil: 'networkidle0' });
        } else {
            // If it's raw HTML, set it to the page's content
            await page.setContent(htmlContent);
        }

        await page.pdf({
            path: outputFile,
            format: 'A4',
            printBackground: true
        });

        console.log(`Successfully saved PDF to ${path.resolve(outputFile)}`);
        await browser.close();
    } catch (error) {
        console.error(`Error converting HTML to PDF for ${outputFile}: ${error}`);
    }
}

// Check if a string is a valid URL
function isValidUrl(str) {
    try {
        new URL(str);
        return true;
    } catch (_) {
        return false;
    }
}

// Main function to process links from the JSON and convert them to PDFs
async function processLinks(inputFile, outputDirectory) {
    ensureDirectoryExists(outputDirectory);

    const professors = JSON.parse(fs.readFileSync(inputFile, 'utf8'));

    for (const professor of professors) {
        const professorName = professor['Professor Name'];
        const professorFolder = path.join(outputDirectory, professorName);
        ensureDirectoryExists(professorFolder);

        let indexValue = 0;
        const mainUrl = professor['Main Website'];
        let htmlData = await fetchUrlContent(mainUrl);
        if (htmlData) {
            const outputFile = path.join(professorFolder, `${professorName}_${indexValue.toString().padStart(3, '0')}_main.pdf`);
            console.log(`Converting data in ${mainUrl} to PDF`);
            await convertHtmlToPdf(mainUrl, outputFile);
            indexValue++;
        }

        const subLinks = professor['Sub Links'];
        for (const subLink of subLinks) {
            htmlData = await fetchUrlContent(subLink);
            if (htmlData) {
                console.log(`Converting data in ${subLink} to PDF`);
                const outputFile = path.join(professorFolder, `${professorName}_${indexValue.toString().padStart(3, '0')}_sub.pdf`);
                await convertHtmlToPdf(subLink, outputFile);
                indexValue++;
            }
        }
    }
}

// Example usage
const inputFile = './ExtractingPDF/urls_folder/professor_data.json';
const outputDirectory = './ExtractingPDF/pdf_files';
processLinks(inputFile, outputDirectory);
