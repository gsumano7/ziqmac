const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage();
  await p.goto('file://' + __dirname + '/index.html', { waitUntil: 'load' });
  await p.pdf({ path: __dirname + '/knitting-needle-case-drawings.pdf',
    preferCSSPageSize: true, printBackground: true });
  await b.close();
})();
