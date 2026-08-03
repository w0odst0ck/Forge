// Wokwi diagram.json lint 脚本（交付前预验证）
// 用法: node lint.js <diagram.json> [<diagram2.json> ...]
// 依赖: npm i @wokwi/diagram-lint
// 说明: 校验部件类型/引脚有效性/重复ID/缺失部件，0 error 才可交付
const fs = require('fs');

(async () => {
  // @wokwi/diagram-lint 是纯 ESM 包：必须用动态 import()（require 在 Node <22.12 会 ERR_REQUIRE_ESM）
  const { DiagramLinter } = await import('@wokwi/diagram-lint');
  const files = process.argv.slice(2);
  if (files.length === 0) { console.error('usage: node lint.js <diagram.json> [...]'); process.exit(2); }

  const linter = new DiagramLinter();
  // 尝试加载最新板卡定义（GitHub Pages 域名，网络不通时用内置定义）
  try {
    const bundle = await fetch('https://wokwi.github.io/wokwi-boards/boards.json').then(r => r.json());
    linter.getRegistry().loadBoardsBundle(bundle);
  } catch { /* 用内置定义（已含主流板卡完整引脚） */ }

  let failed = 0;
  for (const file of files) {
    try {
      const diagram = JSON.parse(fs.readFileSync(file, 'utf8'));
      const result = linter.lint(diagram);
      if (result.valid) {
        console.log(`✅ ${file}: valid (${result.stats.total} issues, 0 errors)`);
      } else {
        failed++;
        console.log(`❌ ${file}: ${result.stats.errors} error(s), ${result.stats.warnings} warning(s)`);
        for (const i of result.issues) console.log(`  [${i.severity}] ${i.rule}: ${i.message}`);
      }
    } catch (e) {
      failed++;
      console.log(`❌ ${file}: ${e.message}`);
    }
  }
  process.exit(failed ? 1 : 0);
})();
