const fs = require('fs-extra');
const path = require('path');

/**
 * MVXWorld Manifest Automator
 * Automatically updates transmissions.json based on files in the /posts directory.
 */

const POSTS_DIR = path.join(__dirname, 'posts');
const MANIFEST_FILE = path.join(__dirname, 'transmissions.json');

async function automateManifest() {
  try {
    console.log('🚀 Starting MVXWorld Manifest Automation...');

    // 1. Read the posts directory
    const files = await fs.readdir(POSTS_DIR);
    const htmlFiles = files.filter(f => f.endsWith('.html') && /^\d{3}-/.test(f));

    if (htmlFiles.length === 0) {
      console.warn('⚠️ No valid transmissions found in /posts (expecting format: 00X-slug.html)');
      return;
    }

    console.log(`📦 Found ${htmlFiles.length} transmissions.`);

    // 2. Parse files to extract metadata
    // We assume the filename format: 003-on-the-nature-of-digital-rooms.html
    const transmissions = htmlFiles.map(file => {
      const parts = file.split('-');
      const num = parts[0]; // e.g., "003"
      const slug = parts.slice(1).join('-').replace('.html', ''); // e.g., "on-the-nature-of-digital-rooms"
      
      // Try to read the file to get the title from the <title> tag or <h1>
      const content = fs.readFileSync(path.join(POSTS_DIR, file), 'utf8');
      
      // Simple regex to grab the title from the <h1> tag
      const titleMatch = content.match(/<h1 class="title">([^<]+)<\/h1>/);
      const rawTitle = titleMatch ? titleMatch[1] : slug.replace(/-/g, ' ');
      
      // Format title: "The Unfair Advantage" -> title: "the unfair advantage", title_em: "advantage"
      const titleWords = rawTitle.toLowerCase().split(' ');
      const title_em = titleWords[titleWords.length - 1];

      return {
        num: num,
        date: new Date().toISOString().split('T')[0], // Defaults to today if not found
        title: rawTitle.toLowerCase(),
        title_em: title_em,
        kicker: "automated transmission", // Default kicker
        filed: "archive",
        frequency: "MVX",
        length: "2 minutes",
        status: "broadcast",
        url: `posts/${file}`
      };
    });

    // 3. Sort by number descending (newest first)
    transmissions.sort((a, b) => b.num.localeCompare(a.num));

    // 4. Update the manifest
    const manifest = await fs.readJson(MANIFEST_FILE);
    manifest.updated = new Date().toISOString().split('T')[0];
    manifest.transmissions = transmissions;

    await fs.writeJson(MANIFEST_FILE, manifest, { spaces: 2 });

    console.log('✅ transmissions.json successfully updated!');
    console.log(`✨ Total transmissions indexed: ${transmissions.length}`);

  } catch (error) {
    console.error('❌ Automation failed:', error);
  }
}

automateManifest();
