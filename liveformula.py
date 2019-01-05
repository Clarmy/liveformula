class Formula():
    '''公式对象'''
    def __init__(self):
        '''初始状态，等式左右项为空'''
        self.left_terms = []
        self.right_terms = []

    def __repr__(self):
        if self.left_terms == [] or self.right_terms == []:
            return 'Formula: None'
        else:
            return 'Formula: %s'%self.formula()

    def add_terms(self,terms,side):
        '''在等式中添加项

        输入参数
        -------
        terms : `list`
            包含项的列表，每个项为元组格式，元组内包含两个元素，第一个元素为序号(int)，
            第二个元素为项(str)。terms的格式类似于[(0,'+x'),(1,'+y'),(2,'+z')]

        side : `str`
            选择要在等号的那边加入该项，该参数应从'left'和'right'两个字符串中选择。
            若为'left'，则将项加入等号的左边；若为'right'，则加入等号的右边。

        示例
        ---
        >>> fml = Formula()
        >>> fml.add_terms([(0,'+3a'),(1,'+b')],'left')
        >>> fml.add_terms([(0,'+14')],'right')
        >>> fml
        Formula: 3a+b=14
        '''
        if side == 'left':
            existing_index = [term[0] for term in self.left_terms]
            for term in terms:
                if term[0] in existing_index:
                    raise ValueError('term %s\'s index has been existing.'%str(term))
            else:
                self.left_terms.extend(terms)
                self.left_terms.sort()
        elif side == 'right':
            existing_index = [term[0] for term in self.right_terms]
            for term in terms:
                if term[0] in existing_index:
                    raise ValueError('term %s\'s index has been existing.'%str(term))
            else:
                self.right_terms.extend(terms)
                self.right_terms.sort()

    def formula(self):
        '''返回当前状态的完整公式

        示例
        ----
        >>> fml = Formula()
        >>> fml.add_terms([(0,'+3a'),(1,'+b')],'left')
        >>> fml.add_terms([(0,'+14')],'right')
        >>> fml.formula()
        '3a+b=14'
        '''
        left_term0 = self.left_terms[0]
        if left_term0[1][0] in ['+','-']:
            left_head = left_term0[1][1:]
        else:
            left_head = left_term0[1]
        right_term0 = self.right_terms[0]
        if right_term0[1][0] in ['+','-']:
            right_head = right_term0[1][1:]
        else:
            right_head = right_term0[1]
        left_terms = [t[1] for t in self.left_terms[1:]]
        right_terms  = [t[1] for t in self.right_terms[1:]]
        formula = left_head + ''.join(left_terms)+'=' + right_head+''.join(right_terms)
        return formula
