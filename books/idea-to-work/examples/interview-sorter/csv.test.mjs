import assert from 'node:assert/strict';
import { splitParagraphs, csvCell, toCsv } from './csv.mjs';

assert.deepEqual(splitParagraphs('第一段\r\n第二段\r第三行\n\n第四段'), ['第一段', '第二段', '第三行', '第四段']);
assert.throws(() => splitParagraphs(' \n '), /请输入/);
assert.equal(csvCell('他说：“先核对”，\n再决定'), '"他说：“先核对”，\n再决定"');
assert.equal(csvCell('a,"b"\nc'), '"a,""b""\nc"');
assert.equal(csvCell('=1+1'), '"\'=1+1"');
assert.equal(csvCell('-2+3'), '"\'-2+3"');
const result = toCsv([
  { text: '第一行\n第二行, 含“引号”', label: '事实' },
  { text: '这是个人观点', label: '观点' },
]);
assert.ok(result.startsWith('\ufeff"原文","标签"\r\n'));
assert.ok(result.includes('"第一行\n第二行, 含“引号”","事实"'));
assert.ok(result.endsWith('"这是个人观点","观点"'));
assert.throws(() => toCsv([]), /没有可导出/);
assert.throws(() => toCsv([{ text: '内容', label: '未定义' }]), /标签无效/);
assert.throws(() => toCsv([{ text: '', label: '事实' }]), /没有原文/);
console.log('12 项 CSV 与输入边界检查通过');
