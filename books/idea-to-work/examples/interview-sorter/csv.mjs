export function splitParagraphs(input) {
  if (typeof input !== 'string' || !input.trim()) {
    throw new Error('请输入至少一段文字');
  }
  return input.split(/\r\n|\r|\n/).map(s => s.trim()).filter(Boolean);
}

export function csvCell(value, protectSpreadsheet = true) {
  let text = String(value ?? '');
  if (protectSpreadsheet && /^[\s]*[=+\-@]/.test(text)) text = `'${text}`;
  return `"${text.replaceAll('"', '""')}"`;
}

export function toCsv(records, protectSpreadsheet = true) {
  if (!Array.isArray(records) || records.length === 0) {
    throw new Error('没有可导出的记录');
  }
  const allowed = new Set(['', '事实', '观点', '待问']);
  const rows = records.map((record, index) => {
    if (!record || typeof record.text !== 'string' || !record.text.trim()) {
      throw new Error(`第 ${index + 1} 条记录没有原文`);
    }
    if (!allowed.has(record.label)) throw new Error(`第 ${index + 1} 条标签无效`);
    return [record.text, record.label].map(v => csvCell(v, protectSpreadsheet)).join(',');
  });
  return '\ufeff' + [csvCell('原文', false) + ',' + csvCell('标签', false), ...rows].join('\r\n');
}
