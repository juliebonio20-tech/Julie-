import os
path = r'C:\Users\suete\Documents\system for sale\visitor_log_system'
files = ['main_visitor.py', 'vis_ops.py', 'vis_db.py']
for f in files:
    full = os.path.join(path, f)
    with open(full, encoding='utf-8') as fh:
        for i,l in enumerate(fh, 1):
            if 'vis_db' in l or 'vis_ops' in l:
                print(f'{f}:{i}: {l.rstrip()}')
