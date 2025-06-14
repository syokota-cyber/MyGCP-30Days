#!/usr/bin/env python3
# エラー統計・サマリー生成スクリプト

import os
import re
from datetime import datetime
from collections import Counter, defaultdict

def analyze_error_patterns():
    """エラーパターンを分析してサマリーを生成"""
    
    error_dir = "error-solutions"
    if not os.path.exists(error_dir):
        print("📁 error-solutions ディレクトリが見つかりません")
        return
        
    error_files = [f for f in os.listdir(error_dir) if f.endswith('.md')]
    
    if not error_files:
        print("📝 エラーファイルが見つかりません")
        return
    
    error_counts = Counter()
    daily_errors = defaultdict(list)
    recent_errors = []
    
    for file in error_files:
        file_path = os.path.join(error_dir, file)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # エラータイトル抽出
                error_titles = re.findall(r'## 🚨 (.+)', content)
                
                # 日付別エラー抽出
                date_patterns = re.findall(r'\*\*発生日\*\*: Day(\d+)', content)
                
                for title in error_titles:
                    error_type = file.replace('-errors.md', '').replace('gcp-', '')
                    error_counts[error_type] += 1
                    recent_errors.append(f"[{error_type}] {title}")
                
                for day in date_patterns:
                    daily_errors[f"Day{day}"].append(file)
        except Exception as e:
            print(f"⚠️ ファイル読み取りエラー {file}: {e}")
    
    # サマリーレポート生成
    summary = f"""# エラー解決サマリーレポート

## 📊 生成日時
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🚨 エラータイプ別統計
"""
    
    if error_counts:
        for error_type, count in error_counts.most_common():
            summary += f"- **{error_type}**: {count}件\n"
    else:
        summary += "- まだエラーログがありません\n"
    
    summary += "\n## 📅 日別エラー発生状況\n"
    
    if daily_errors:
        for day in sorted(daily_errors.keys()):
            summary += f"- **{day}**: {len(daily_errors[day])}件\n"
    else:
        summary += "- まだ日別データがありません\n"
    
    summary += f"\n## 🔍 最近のエラー (最新{min(5, len(recent_errors))}件)\n"
    
    if recent_errors:
        for error in recent_errors[-5:]:
            summary += f"- {error}\n"
    else:
        summary += "- まだエラー記録がありません\n"
    
    summary += "\n## 💡 改善提案\n"
    
    if error_counts.get('api', 0) > 2:
        summary += "- API有効化チェックリスト作成を推奨\n"
    if error_counts.get('auth', 0) > 2:
        summary += "- 権限設定自動化スクリプト作成を推奨\n"
    if error_counts.get('general', 0) > 3:
        summary += "- 頻出エラーの事前チェック機能追加を推奨\n"
    
    if not any(error_counts.values()):
        summary += "- まだエラーが少ないため、継続的に記録を蓄積してください\n"
    
    # サマリーファイル保存
    os.makedirs(error_dir, exist_ok=True)
    summary_file = os.path.join(error_dir, 'ERROR_SUMMARY.md')
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"📊 エラーサマリーレポート生成完了: {summary_file}")

if __name__ == "__main__":
    analyze_error_patterns()
