"""完整诊断 Flask 应用问题"""
import sys
import os

print("=" * 60)
print("Flask 应用完整诊断")
print("=" * 60)

# 1. 检查文件
print("\n1. 检查关键文件:")
files_to_check = [
    'app.py',
    'templates/index.html',
    'static/app.js',
    'config.py',
    'orchestrator.py'
]

for file in files_to_check:
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"  {status} {file}")

# 2. 尝试导入模块
print("\n2. 导入模块测试:")
try:
    import config
    print("  ✅ config 模块导入成功")
except Exception as e:
    print(f"  ❌ config 导入失败: {e}")
    sys.exit(1)

try:
    import orchestrator
    print("  ✅ orchestrator 模块导入成功")
except Exception as e:
    print(f"  ❌ orchestrator 导入失败: {e}")
    sys.exit(1)

try:
    import app
    print("  ✅ app 模块导入成功")
except Exception as e:
    print(f"  ❌ app 导入失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 3. 检查Flask应用
print("\n3. Flask 应用信息:")
print(f"  应用名: {app.app.name}")
print(f"  根路径: {app.app.root_path}")
print(f"  模板路径: {app.app.template_folder}")

# 4. 检查路由
print("\n4. 注册的路由:")
for rule in app.app.url_map.iter_rules():
    methods = ', '.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
    print(f"  {rule.endpoint:20s} {str(rule):40s} [{methods}]")

# 5. 测试视图函数
print("\n5. 测试视图函数:")
with app.app.test_request_context('/'):
    try:
        from flask import url_for
        print(f"  url_for('index'): {url_for('index')}")
        print(f"  url_for('health_check'): {url_for('health_check')}")
    except Exception as e:
        print(f"  ❌ url_for 错误: {e}")

# 6. 使用 test_client 测试
print("\n6. test_client 测试:")
with app.app.test_client() as client:
    # 测试首页
    response = client.get('/')
    print(f"  GET / : 状态码 {response.status_code}")
    if response.status_code != 200:
        print(f"    响应: {response.data.decode()[:100]}")
    
    # 测试健康检查
    response = client.get('/api/health')
    print(f"  GET /api/health : 状态码 {response.status_code}")
    if response.status_code == 200:
        import json
        data = json.loads(response.data)
        print(f"    响应: {data}")

# 7. 检查视图函数是否存在
print("\n7. 视图函数检查:")
view_functions = ['index', 'generate_course', 'health_check']
for func_name in view_functions:
    func = app.app.view_functions.get(func_name)
    if func:
        print(f"  ✅ {func_name}: {func}")
    else:
        print(f"  ❌ {func_name}: 未找到")

print("\n" + "=" * 60)
print("诊断完成")
print("=" * 60)
