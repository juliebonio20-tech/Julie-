import os
base = r'C:\Users\suete\Documents\system for sale\visitor_log_system'
for fname in ['main_visitor.py', 'vis_ops.py', 'vis_db.py']:
    p = os.path.join(base, fname)
    with open(p, encoding='utf-8-sig') as f:
        for i,line in enumerate(f,1):
            if 'vis_db' in line or 'vis_ops' in line:
                print(fname + ':' + str(i) + ': ' + line.rstrip())
