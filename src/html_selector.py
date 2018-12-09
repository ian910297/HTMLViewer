class HTMLSelector():
    def __init__(self, root):
        self.root = root
    
    def select(self, text):
        result = []
        rules = text.split(',')
        for i in range(len(rules)):
            rule = rules[i].strip()
            rule = rule.split(' ')
            
            j = 0
            walker = self.root
            while j < len(rule):
                walker = self.__walk(walker, rule[j])
                if walker is None:
                    print('walker is None')
                    break
                j += 1
            
            if j is not len(rule):
                result.append(None)
            else:
                result.append(walker)
        
        return result
    
    def __walk(self, root, rule):
        if rule[0] is '#':
            result = self.__get_by_id(root, rule[1:])
        elif rule[0] is '.':
            result = self.__get_by_classes(root, rule[1:])
        else:
            result = self.__get_by_name(root, rule)
        
        return result

    def __get_by_name(self, root, name):
        result = None
        stack = [root]
        while len(stack) > 0:
            node = stack[0]
            stack = stack[1:]
            for i in range(len(node.children)):
                stack.insert(i, node.children[i])
        
            if node.name == name:
                result = node
                break
        
        return result

    def __get_by_id(self, root, id):
        result = None
        stack = [root]
        while len(stack) > 0:
            node = stack[0]
            stack = stack[1:]
            for i in range(len(node.children)):
                stack.insert(i, node.children[i])
            
            if node.id == id:
                result = node
                break
        
        return result
    
    def __get_by_classes(self, root, classname):
        result = None
        stack = [root]
        while len(stack) > 0:
            node = stack[0]
            stack = stack[1:]
            for i in range(len(node.children)):
                stack.insert(i, node.children[i])
            
            i = 0
            while i < len(node.classes):
                if node.classes[i] == classname:
                    result = node
                    break

                i += 1
            
            if result is not None:
                break

        return result
        
    def select_all(self, text):
        result = []
        rules = text.split(',')
        for i in range(len(rules)):
            rule = rules[i].strip()
            rule = rule.split(' ')
            
            j = 0
            walker = [ self.root ]
            while j < len(rule):
                temp = []
                for k in range(len(walker)):
                    temp += self.__walk_all(walker[k], rule[j])
                    
                walker = temp
                j += 1
            
            result += walker

        return result

    def __walk_all(self, root, rule):
        if rule[0] is '#':
            result = self.__get_all_by_id(root, rule[1:])
        elif rule[0] is '.':
            result = self.__get_all_by_classes(root, rule[1:])
        else:
            result = self.__get_all_by_name(root, rule)
        
        return result

    def __get_all_by_name(self, root, name):
        result = []
        stack = [root]
        while len(stack) > 0:
            node = stack[0]
            stack = stack[1:]
            for i in range(len(node.children)):
                stack.insert(i, node.children[i])
        
            if node.name == name:
                result.append(node)
        
        return result

    def __get_all_by_id(self, root, id):
        result = []
        stack = [root]
        while len(stack) > 0:
            node = stack[0]
            stack = stack[1:]
            for i in range(len(node.children)):
                stack.insert(i, node.children[i])
            
            if node.id == id:
                result = [node]
                break
        
        return result
    
    def __get_all_by_classes(self, root, classname):
        result = []
        stack = [root]
        while len(stack) > 0:
            node = stack[0]
            stack = stack[1:]
            for i in range(len(node.children)):
                stack.insert(i, node.children[i])
            
            i = 0
            while i < len(node.classes):
                if node.classes[i] == classname:
                    result.append(node)
                    break

                i += 1

        return result