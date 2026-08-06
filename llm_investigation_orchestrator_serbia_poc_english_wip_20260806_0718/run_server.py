import sys
import os

tools_path = os.path.join(os.path.dirname(__file__), '..', '.tools', 'python')
sys.path.insert(0, os.path.normpath(tools_path))

sys.argv = [__file__, '8768']

exec(open(os.path.join(os.path.dirname(__file__), 'server.py'), encoding='utf-8').read())
