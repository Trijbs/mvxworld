const fs = require('fs-extra');
const path = require('path');
const { execSync } = require('child_process');

/**
 * MVXWorld Global Sync
 * 1. Updates the transmissions manifest.
 * 2. Calculates the "Interesting Idea" counter based on the last git commit.
 */

const MANIFEST_FILE = path.join(__dirname, 'transmissions.json');
const INDEX_FILE = path.join(__dirname, 'index.html');

async function syncUniverse() {
  try {
    console.log('🌌 Synchronizing MVXWorld Universe...');

    // --- 1. Update Manifest (Reuse existing logic) ---
    const POSTS_DIR = path.join(__dirname, 'posts');
    const files = await fs.readdir(POSTS_DIR);
    const htmlFiles = files.filter(f => f.endsWith('.html') && /^\d{3}-/.test(f));
    
    const transmissions = htmlFiles.map(file => {
      const parts = file.split('-');
      const num = parts[0];
      const slug = parts.slice(1).join('-').replace('.html', '');
      const content = fs.readFileSync(path.join(POSTS_DIR, file), 'utf8');
      const titleMatch = content.match(/<h1 class="title">([^<]+)<\/h1>/);
      const rawTitle = titleMatch ? titleMatch[1] : slug.replace(/-/g, ' ');
      const titleWords = rawTitle.toLowerCase().split(' ');
      const title_em = titleWords[titleWords.length - 1];

      return {
        num: num,
        date: new Date().toISOString().split('T')[0],
        title: rawTitle.toLowerCase(),
        title_em: title_em,
        kicker: "automated transmission",
        filed: "archive",
        frequency: "MVX",
        length: "2 minutes",
        status: "broadcast",
        url: `posts/${file}`
      };
    });
    transmissions.sort((a, b) => b.num.localeCompare(a.num));

    const manifest = await fs.readJson(MANIFEST_FILE);
    manifest.updated = new Date().toISOString().split('T')[0];
    manifest.transmissions = transmissions;
    await fs.writeJson(MANIFEST_FILE, manifest, { spaces: 2 });
    console.log('✅ Manifest updated.');

    // --- 2. The Counter Logic ---
    // Get the date of the last commit on the current branch
    const lastCommitDateStr = execSync('git log -1 --format=%cd').toString().trim();
    // Format: "Fri Sep 18 14:00:00 2026 +0200"
    const lastCommitDate = new Date(lastCommitDateStr);
    const today = new Date();
    
    const diffTime = Math.abs(today - lastCommitDate);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    const formattedDate = lastCommitDate.getFullYear() + ' · ' + 
                           String(lastCommitDate.getMonth() + 1).padStart(2, '0') + ' · ' + 
                           String(lastCommitDate.getDate()).padStart(2, '0');

    // Update index.html directly
    let indexContent = await fs.readFile(INDEX_FILE, 'utf8');
    
    // Replace the counter number
    indexContent = indexContent.replace(/id="idea-counter">\d+<\/span>/, `id="idea-counter">${diffDays}</span>`);
    // Replace the reset date
    indexContent = indexContent.replace(/id="reset-date" datetime="[^"]*"[^>]*>([^<]+)<\/time>/, 
      `id="reset-date" datetime="${lastCommitDate.toISOString().split('T')[0]}" >${formattedDate}</time>`);

    await fs.writeFile(INDEX_FILE, indexContent, 'utf8');
    console.log(`✅ Counter updated: ${diffDays} days since last interesting idea (${formattedDate}).`);

  } catch (error) {
    console.error('❌ Universe Sync failed:', error);
  }
}

syncUniverse();
