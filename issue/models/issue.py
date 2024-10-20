from odoo import api,fields, models,_
from datetime import timedelta
from odoo.exceptions import UserError

class IssueModel(models.Model):
    _name = "issue"
    _description = "ISSUE main model for OpenPLM."    
    _inherit = ['mail.thread','mail.activity.mixin']

    item_number =fields.Char("问题編號" , default=lambda self: _('New'), copy=False , readonly=True )
    title=fields.Char("问题主旨")  
    issue_Source =fields.Selection(
        string="问题来源",
        selection=[('Customer','客户'),('Internal','内部'),('Supplier','供应商')],
        required=True
    )
    owner_id =fields.Many2one('res.users',string='问题回报人',default=lambda self: self.env.user)
    issue_product_id =fields.Many2one('product.template',string='问题产品')
    issue_bom_id =fields.Many2one('mrp.bom',string='问题物料清单') 
    external_number =fields.Char("外部单号")  
    priority = fields.Selection(
        [('0', 'Normal'),('1', 'Medium'),('2', 'High'),('3', 'Very High')],
        string='优先级', default='0')
    issue_stage= fields.Selection(
        [('Request Application', '需求申请'),('Design Fundamentals', '设计基础'),('Hierarchical structure', '层次结构'),
        ('Detailed design', '详细设计'),('Unique process', 'V项目独特工艺'),('Process standards', '工艺标准'),
        ('Build cycle', '构建周期'),('During testing', '测试中'),('In use', '使用中')],
        string='问题发生阶段')
    custoomer_id =fields.Many2one('res.company',string='受影响客户')
    description =fields.Text("问题描述") 
    environmental =fields.Text("环境说明") 
    reproduce = fields.Text("重现操作顺序")
    respond = fields.Selection(
        [('Y', 'Yes'),('N', 'No'),('NA', 'N/A')],
        string='回应')
    
    active =fields.Boolean("啟用",default=True) 
    quantity = fields.Integer("数量")
    issue_code_ids = fields.Many2many('issue.code', string='问题编码')
    state =fields.Selection(
        string="状态",
        selection=[('Submitted','提交'),('In Verification','验证中'),('Verified','已验证'),('Closed','关闭'),('Cancel','取消')],
        default="Submitted",readonly=True,tracking=1
    )
    #关联其他表单2024.9.25 Herbert增加
    project_id =fields.Many2one('project.project',string='关联专案')
    dco_id =fields.Many2many('dco',string='关联DCO')
    pco_id =fields.Many2many('pco',string='关联PCO')
    #增加栏位 2024.9.25 Herbert增加
    # solution =fields.Text("解决方案")
    vresults =fields.Selection(
        string="验证结果",
        selection=[('Acceptable','可接受'),('Observed','待观察')]
    ) 

    #增加欄位 2024.10.12 Herbert增加
    d3 =fields.Text("D3抑制措施")
    d4 =fields.Text("D4原因分析")
    d5 =fields.Text("D5纠正措施")
    d6 =fields.Text("D6执行问题改善")
    d7 =fields.Text("D7预防再发")
    team_id =fields.Many2many('res.users',string='团队人员')
    issue_image = fields.Image('圖片',max_width=128,max_height=128)
    
    # #上传单个档案写法
    # binary_field = fields.Binary("档案")
    # binary_file_name =fields.Char("档案名称")
    # #上传多个档案写法
    binary_fields =fields.Many2many("ir.attachment",string="Multi Files Upload")

    # Seqence 自动领号写法
    @api.model_create_multi
    def create(self, vals_list):
         """ Create a sequence for the requirement model """
         for vals in vals_list:
               if vals.get('item_number', _('New')) == _('New'):
                      vals['item_number'] = self.env['ir.sequence'].next_by_code('issue')
                      return super().create(vals_list)     
    
    #定义按钮
    def action_set_In_Verification(self):
        if self.state =='Submitted':
            self.write ({'state':'In Verification'})        
        elif self.state =='In Verification':
            raise UserError('已是"验证中"状态')
        else:
            raise UserError('不可以推到"验证中"状态')
    def action_set_Verified(self):
        if self.state =='In Verification':
            self.write({'state':'Verified'})
        elif self.state =='Verified':
            raise UserError('已是"已验证"状态')
        else:
            raise UserError('不可以推到"已验证"状态')
    def action_set_Closed(self):
        if self.state =='Verified':
            self.write({'state':'Closed'})          
        elif self.state =='Closed':
            raise UserError('已是"关闭"状态')          
        elif self.state =='Submitted':
            raise UserError('不可以推到"关闭"状态')          
        elif self.state =='In Verification':
            raise UserError('不可以推到"关闭"状态')        
        else:
            raise UserError('已取消,不能被关闭')
    def action_set_Cancel(self):
        if self.state =='Submitted':
            self.write({'state':'Cancel'})
        elif self.state =='In Verification':
            self.write({'state':'Cancel'}) 
        elif self.state =='Verified':
            self.write({'state':'Cancel'})             
        elif self.state =='Cancel':
            raise UserError('已是"取消"状态')
        else:
            raise UserError('已关闭,不能被取消')
