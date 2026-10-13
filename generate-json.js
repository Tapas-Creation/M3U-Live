const fs = require('fs');
const path = require('path');

const rootDir = __dirname;
const excludeDirs = ['.git', '.github', 'images', 'node_modules'];

function extractHashId(filename) {
    let nameWithoutExt = filename.replace(/\.[^/.]+$/, "");
    let match = nameWithoutExt.match(/_([a-zA-Z0-9]+)$/);
    return match ? match[1].trim() : null;
}

function generateJSON() {
    let categories = fs.readdirSync(rootDir, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory() && !excludeDirs.includes(dirent.name))
        .map(dirent => dirent.name);

    let allPlaylistData = {};

    categories.forEach(cat => {
        let catPath = path.join(rootDir, cat);
        let items = fs.readdirSync(catPath, { withFileTypes: true });

        let validFiles = items.filter(item => {
            let nameLower = item.name.toLowerCase();
            let isImage = /\.(png|jpg|jpeg|webp)$/i.test(nameLower);
            return item.isFile() && !isImage && !nameLower.startsWith('.');
        });

        let imagesDir = path.join(catPath, 'images');
        let imagesList = [];
        if (fs.existsSync(imagesDir) && fs.statSync(imagesDir).isDirectory()) {
            imagesList = fs.readdirSync(imagesDir).filter(img => /\.(png|jpg|jpeg|webp)$/i.test(img));
        }

        let imagesMap = {};
        imagesList.forEach(img => {
            let hashId = extractHashId(img);
            if (hashId) {
                imagesMap[hashId] = `images/${img}`;
            }
        });

        let catFiles = validFiles.map((file, index) => {
            let fileHashId = extractHashId(file.name);
            let matchedImg = (fileHashId && imagesMap[fileHashId]) ? imagesMap[fileHashId] : (imagesList[index % imagesList.length] ? `images/${imagesList[index % imagesList.length]}` : null);

            let rawNameToClean = matchedImg ? path.basename(matchedImg) : file.name;
            let nameWithoutExt = rawNameToClean.replace(/\.[^/.]+$/, "");
            let cleanBaseName = nameWithoutExt.replace(/_[a-zA-Z0-9]+$/, "");
            let titleText = cleanBaseName.replace(/[-_]/g, " ").trim();

            let extMatch = file.name.match(/\.[^/.]+$/);
            let fileExt = extMatch ? extMatch[0] : "";
            let nameWithoutFileExt = file.name.replace(/\.[^/.]+$/, "");
            let cleanFileName = nameWithoutFileExt.replace(/_[a-zA-Z0-9]+$/, "") + fileExt;

            return {
                name: file.name,
                displayName: cleanFileName,
                download_url: `${cat}/${file.name}`,
                image: matchedImg ? `${cat}/images/${path.basename(matchedImg)}` : "https://via.placeholder.com/300x160?text=No+Preview",
                title: titleText || "Live Stream",
                category: cat
            };
        });

        allPlaylistData[cat] = catFiles;
    });

    fs.writeFileSync(path.join(rootDir, 'playlist.json'), JSON.stringify(allPlaylistData, null, 2));
    console.log("playlist.json generated successfully!");
}

generateJSON();
