def simplifyPath(path):
    parts = path.split('/')
    stack = []
    
    for part in parts:
        if part == '..':
            if stack:
                stack.pop()
        elif part and part != '.':
            stack.append(part)
    
    return parts

print(simplifyPath("/.../a/../b/c/../d/./"))