#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运营WIP报表自动化汇总系统 - 主脚本
功能：
1. 网站WIP数据下载
2. 邮箱附件收集
3. 数据整合汇总
4. 邮件转发发送

作者：OpenClaw
日期：2026-05-15
"""
import json
import smtplib
import pandas as pd
from pathlib import Path
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ============================================================================
# 配置加载
# ============================================================================
CONFIG_FILE = Path(__file__).parent / 'config.json'

def load_config():
    """加载配置文件"""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 处理路径
    config['output']['dir'] = Path(config['output']['dir'].replace('~', '~'))
    config['logging']['dir'] = Path(config['logging']['dir'].replace('~', '~'))
    
    return config

# ============================================================================
# 数据处理模块
# ============================================================================
OUTPUT_COLS = [
    '供应商', '客户代码', '客户名称', '客户订单号', '封装形式',
    '产品型号', '芯片型号', '晶圆批次', '订单数量', '投产日期',
    '粘片', '焊线', '焊线2', '焊线批检', '塑封', '电镀',
    '切筋', '委外切筋', '包装', '测试', '测试编带', '包装入库',
    '在线合计', '入库良品', '入库不良品', '出库良品', '出库不良品',
    '库存', '状态'
]

def create_highlighted_excel(df, output_path, config):
    """创建高亮Excel表格"""
    wb = Workbook()
    ws = wb.active
    ws.title = "WIP汇总"
    
    # 从配置获取供应商颜色
    colors = {}
    font_colors = {}
    for op in config['operators']:
        colors[op['name']] = op.get('color', '#E0E0E0')
        font_colors[op['name']] = op.get('fontColor', '#000000')
    
    # 样式
    header_font = Font(bold=True, color='FFFFFF', size=11)
    header_fill = PatternFill(start_color='2E75B6', end_color='2E75B6', fill_type='solid')
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # 写表头
    for col_idx, col_name in enumerate(df.columns, 1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = thin_border
    
    # 写数据
    for row_idx, row in enumerate(df.values, 2):
        supplier = str(row[0])
        supplier_color = colors.get(supplier, '#E0E0E0')
        font_color = font_colors.get(supplier, '#000000')
        
        for col_idx, value in enumerate(row, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value if pd.notna(value) else '')
            cell.alignment = Alignment(horizontal='center', vertical='center')
            cell.border = thin_border
            
            # 整行供应商颜色
            cell.fill = PatternFill(start_color=supplier_color.lstrip('#'), 
                                    end_color=supplier_color.lstrip('#'), 
                                    fill_type='solid')
            cell.font = Font(color=font_color.lstrip('#'))
            
            # 状态列特殊高亮
            col_name = df.columns[col_idx-1]
            if col_name == '状态':
                status = str(value)
                if '完成' in status or '结批' in status:
                    cell.fill = PatternFill(start_color='00C853', end_color='00C853', fill_type='solid')
                    cell.font = Font(bold=True, color='FFFFFF')
                elif '生产' in status:
                    cell.fill = PatternFill(start_color='FFD600', end_color='FFD600', fill_type='solid')
                    cell.font = Font(bold=True, color='000000')
                elif '发货' in status:
                    cell.fill = PatternFill(start_color='00E676', end_color='00E676', fill_type='solid')
                    cell.font = Font(bold=True, color='FFFFFF')
    
    # 列宽
    for col_idx in range(1, len(df.columns)+1):
        ws.column_dimensions[ws.cell(row=1, column=col_idx).column_letter].width = 12
    
    ws.row_dimensions[1].height = 30
    ws.freeze_panes = 'A2'
    wb.save(output_path)

def process_file(file, supplier_hint=None):
    """处理单个Excel文件"""
    try:
        df = pd.read_excel(file)
        df.columns = [str(c).replace('\xa0', '').strip() for c in df.columns]
        
        n_rows = len(df)
        if n_rows == 0:
            return None
        
        # 创建结果DataFrame
        result = pd.DataFrame(index=range(n_rows), columns=OUTPUT_COLS)
        result['供应商'] = supplier_hint
        
        # 字段映射
        field_map = {
            '客户代码': ['客户代码'],
            '客户名称': ['客户名称'],
            '客户订单号': ['客户订单号', '工单号', '用户订单编号', '销售订单号'],
            '封装形式': ['封装形式', '封装类型', '工艺路线（封装形式）'],
            '产品型号': ['产品型号', '物料名称', '电路名'],
            '芯片型号': ['芯片型号', '芯片名', 'A芯片名称'],
            '晶圆批次': ['晶圆批次', '芯片批号', 'A晶圆批号'],
            '订单数量': ['订单数量', '批量数量', '订单数量(下单数量)', '来料数'],
            '投产日期': ['投产日期', '投产时间', '投料时间', '下线日期'],
            '粘片': ['粘片', 'Die_Bonding粘片', '上芯数'],
            '焊线': ['焊线', 'Wire_Bonding键合', '键合数'],
            '焊线2': ['焊线2'],
            '焊线批检': ['焊线批检', '批检'],
            '塑封': ['塑封', 'Mol_ding模封', '模封数'],
            '电镀': ['电镀', 'Plating电镀'],
            '切筋': ['切筋', 'Trim_Form切筋打弯'],
            '委外切筋': ['委外切筋', '委外'],
            '包装': ['包装', 'Packing包装'],
            '测试': ['测试', 'Testtu_bassembly测试管装', '测试数'],
            '测试编带': ['测试编带', '编带'],
            '包装入库': ['包装入库', '入库数量'],
            '在线合计': ['在线合计', '在线数量', '工单下线数'],
            '入库良品': ['入库良品', '入库合计（良品）', '入库数量'],
            '入库不良品': ['入库不良品', '入库合计（不良品）', '入库不良'],
            '出库良品': ['出库良品', '出库（良品）', '出库数量', '发货良品'],
            '出库不良品': ['出库不良品', '出库（不良品）', '出库不良', '发货不良'],
            '库存': ['库存', '库存数量', '库存良品'],
            '状态': ['状态', '是否结批', '订单状态'],
        }
        
        for target_col, source_cols in field_map.items():
            for src_col in source_cols:
                if src_col in df.columns:
                    result[target_col] = df[src_col].values
                    break
        
        return result.fillna('')
        
    except Exception as e:
        print(f"  ❌ 处理失败: {file.name} - {e}")
        return None

# ============================================================================
# 邮件发送模块
# ============================================================================
def send_email_with_attachment(config, attachment_path, summary_stats):
    """发送带附件的邮件"""
    email_cfg = config['emailConfig']['forward']
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = email_cfg['username']
    msg['To'] = ', '.join(email_cfg['recipients'])
    
    # 主题和正文
    date_str = datetime.now().strftime('%Y-%m-%d')
    msg['Subject'] = email_cfg['subjectTemplate'].replace('{date}', date_str)
    
    body = email_cfg['bodyTemplate'].replace('{date}', date_str)
    body = body.replace('{supplierCount}', str(summary_stats['supplierCount']))
    body = body.replace('{totalRows}', str(summary_stats['totalRows']))
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加附件
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 
                       f'attachment; filename="{attachment_path.name}"')
        msg.attach(part)
    
    # 发送
    try:
        server = smtplib.SMTP(email_cfg['smtpServer'], email_cfg['smtpPort'])
        server.starttls()
        server.login(email_cfg['username'], email_cfg['password'])
        server.send_message(msg)
        server.quit()
        print(f"✅ 邮件已发送至: {', '.join(email_cfg['recipients'])}")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

# ============================================================================
# 主流程
# ============================================================================
def main():
    print("=" * 70)
    print("运营WIP报表自动化汇总系统")
    print("=" * 70)
    print()
    
    # 加载配置
    config = load_config()
    output_dir = config['output']['dir']
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_data = []
    
    # 1. 处理现有数据文件
    print("1. 整合现有数据文件...")
    
    # 从输出文件夹收集
    for file in output_dir.glob('*'):
        if file.suffix in ['.xlsx', '.xls'] and '运营WIP' not in file.name:
            # 根据文件名识别供应商
            for op in config['operators']:
                if any(kw in file.name for kw in [op['name']] + op.get('keywords', [])):
                    mapped = process_file(file, op['name'])
                    if mapped is not None and len(mapped) > 0:
                        all_data.append(mapped)
                        print(f"  ✅ {op['name']}: {len(mapped)}行 ({file.name})")
                    break
    
    # 从Downloads收集最新下载
    downloads_dir = Path('~').expanduser() / 'Downloads'
    for file in downloads_dir.glob('*2026-05-15*.xlsx'):
        if '运营WIP' not in file.name:
            for op in config['operators']:
                keywords = []
                if op['type'] == 'email' and 'email' in op:
                    keywords = op['email'].get('keywords', [])
                if any(kw in file.name for kw in keywords):
                    mapped = process_file(file, op['name'])
                    if mapped is not None and len(mapped) > 0:
                        all_data.append(mapped)
                        print(f"  ✅ {op['name']}: {len(mapped)}行 ({file.name})")
                    break
    
    # 2. 生成汇总表
    if all_data:
        print("\n2. 生成汇总表...")
        
        final = pd.concat(all_data, ignore_index=True)
        
        # 生成文件名
        date_str = datetime.now().strftime('%Y-%m-%d')
        time_str = datetime.now().strftime('%H%M')
        filename = config['output']['filenameTemplate'].replace('{date}', date_str).replace('{time}', time_str)
        output_path = output_dir / filename
        
        create_highlighted_excel(final, output_path, config)
        
        print(f"  ✅ 文件已生成: {output_path}")
        print(f"     文件大小: {output_path.stat().st_size / 1024:.1f} KB")
        
        # 统计信息
        print("\n3. 数据统计:")
        supplier_counts = final['供应商'].value_counts()
        for supplier, count in supplier_counts.items():
            print(f"  {supplier}: {count}条")
        
        summary_stats = {
            'supplierCount': len(supplier_counts),
            'totalRows': len(final)
        }
        
        print(f"\n  总数据: {len(final)}条")
        
        # 3. 发送邮件
        print("\n4. 发送邮件转发...")
        success = send_email_with_attachment(config, output_path, summary_stats)
        
        if not success:
            print(f"  ⚠️  邮件发送失败，文件已保存在: {output_path}")
        
        print("\n" + "=" * 70)
        print("完成!")
        print("=" * 70)
        
        return output_path
    else:
        print("\n❌ 无有效数据可汇总")
        return None

if __name__ == '__main__':
    result = main()
    if result:
        print(f"\n📁 输出文件: {result}")