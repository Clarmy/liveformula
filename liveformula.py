# coding : utf-8
from namedlist import namedlist

class Term(namedlist('Term', 'position label symbol content')):
    '''代数项对象'''
    __slots__ = ()

    def __init__(self,position=None,label=None,symbol=None,content=None):
        self.position = position
        self.label = label
        self.symbol = symbol
        self.content = content

    @property
    def __str__(self):
        return 'Term: position=%s  '\
               'label=$%s  symbol=%s  '\
               'content=%s  ' % (self.position, self.label,
                                 self.symbol,self.content)

    def change_label(self,newlabel):
        self.label = newlabel

    def change_symbol(self):
        self.symbol *= -1

    def change_position(self,newpositon):
        self.position = newpositon

    def change_content(self,newcontent):
        self.content = newcontent


class Formula():
    '''Formula对象'''
    def __init__(self,left_terms=None,right_terms=None):
        '''初始状态'''
        self.left_terms = left_terms
        for n in range(len(left_terms)):
            self.left_terms[n].position = n

        self.right_terms = right_terms
        for n in range(len(right_terms)):
            self.right_terms[n].position = n

    def __repr__(self):
        if not self.left_terms:
            return 'Formula: Not Equation(lack left terms)'
        elif not self.right_terms:
            return 'Formula: Not Equation(lack right terms)'
        else:
            return 'Formula: %s'%self.formula

    def add_terms(self,terms,side):
        '''在等式中添加项

        输入参数
        -------
        terms : `list`
            包含代数项的列表，每个代数项都为Term对象

        side : `str`
            选择要在等号的那边加入该项，该参数应从'left'和'right'两个字符串中选择。
            若为'left'，则将项加入等号的左边；若为'right'，则加入等号的右边。

        示例
        ---
        >>> left_terms = [Term(symbol=1,content='x'),Term(symbol=1,content='y')]

        >>> right_terms = [Term(symbol=1,content='15')]

        >>> fml = Formula(left_terms,right_terms)

        >>> fml
        Formula: x+y=15

        >>> fml.add_terms([Term(symbol=-1,content='z')],side='left')

        >>> fml
        Formula: x+y-z=15
        '''
        if side == 'left':
            if self.left_terms:
                existing_positions = [term.position for term in self.left_terms]
            else:
                existing_positions = []
            self.left_terms.extend(terms)
            for n in range(len(self.left_terms)):
                self.left_terms[n].position = n

        elif side == 'right':
            if self.right_terms:
                existing_positions = [term.position for term in self.right_terms]
            else:
                existing_positions = []
            self.right_terms.extend(terms)
            for n in range(len(self.right_terms)):
                self.right_terms[n].position = n

        else:
            raise ValueError('side parameter must be selected '
                             'from \'left\' and \'right\'')

    def drop_terms(self,indexs,side):
        '''删除项方法

        输入参数
        -------
        indexs : `list`
            需要删除的项的序号，例如要删除序号为1的项，则indexs参数设为[1]。
            若要删除1、2、3项，则将indexs设置为[1,2,3]

        side : `str`
            选择要删除等号哪边的项，须从'left'和'right'中选择
        '''
        def standarlize_indexs(indexs,side):
            std_indexs = []
            for idx in indexs:
                if idx < 0:
                    if side == 'left':
                        idx += len(self.left_terms)
                    elif side == 'right':
                        idx += len(self.right_terms)
                    std_indexs.append(idx)
                std_indexs.append(idx)
            return std_indexs

        if side == 'left':
            indexs = standarlize_indexs(indexs,side='left')
            new_terms = []
            for n, term in enumerate(self.left_terms):
                if n not in indexs:
                    new_terms.append(term)
            self.left_terms = new_terms
        elif side == 'right':
            indexs = standarlize_indexs(indexs,side='right')
            new_terms = []
            for n, term in enumerate(self.right_terms):
                if n not in indexs:
                    new_terms.append(term)
            self.right_terms = new_terms

    @property
    def terms(self):
        '''返回当前所有代数项'''
        return {'left':self.left_terms,'right':self.right_terms}

    @property
    def formula(self):
        '''返回当前状态的完整公式'''
        left_term0 = self.left_terms[0]
        if left_term0.symbol == 1:
            left_head = left_term0.content
        elif left_term0.symbol == -1:
            left_head = '-'+left_term0.content
        else:
            raise ValueError('symbol must be 1 or -1.')

        right_term0 = self.right_terms[0]
        if right_term0.symbol == 1:
            right_head = right_term0.content
        elif right_term0.symbol == -1:
            right_head = '-'+right_term0.content
        else:
            raise ValueError('symbol must be 1 or -1.')

        sym = {1:'+',-1:'-'}
        left_terms = [sym[term.symbol]+term.content for \
                      term in self.left_terms[1:]]
        right_terms  = [sym[term.symbol]+term.content for \
                      term in self.right_terms[1:]]
        formula = left_head + ''.join(left_terms)+'=' + right_head+''.join(right_terms)
        return formula

if __name__ == '__main__':
    pass
