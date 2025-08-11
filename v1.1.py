import tkinter as tk
from tkinter import ttk, messagebox
import os

class MilitaryDamageCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("军事打击计算器")
        self.root.geometry("1000x700")
        
        # 初始化数据结构
        self.data = {"炮兵": {}, "步兵": {}, "骑兵": {}}
        self.load_data("炮兵.txt")
        
        # 初始化参数（全部使用DoubleVar支持浮点）
        self.init_parameters()
        
        # 创建紧凑界面
        self.create_compact_ui()
        
        # 存储选中单位
        self.selected_units = {"A": None, "B": None}

    def load_data(self, filename):
        """加载数据文件"""
        try:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"找不到文件: {filename}")
            
            with open(filename, 'r', encoding='utf-8') as file:
                current_category = None
                current_tech_group = None
                
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                        
                    if line in ["炮兵", "步兵", "骑兵"]:
                        current_category = line
                    elif any(line.startswith(group) for group in ["通用", "西欧", "土著", "非洲", "安纳托利亚", "CN", "东欧", "高美", "印度", "绿绿", "游牧"]):
                        current_tech_group = line
                        if current_category:
                            self.data[current_category][current_tech_group] = []
                    elif current_category and current_tech_group:
                        parts = line.split('\t')
                        if len(parts) >= 3:
                            self.data[current_category][current_tech_group].append({
                                'tech_level': parts[0],
                                'name': parts[1],
                                'values': [int(p.split()[0]) if 'pip' in p.lower() else 0 for p in parts[2:8]],
                                'total': int(parts[-1]) if parts[-1].isdigit() else 0
                            })
        except Exception as e:
            messagebox.showerror("错误", f"数据加载错误: {str(e)}")

    def init_parameters(self):
        """初始化所有参数变量（全部支持浮点）"""
        self.params = {
            "A": {name: tk.DoubleVar(value=0.0) for name in [
                'morale_impact_bonus', 'morale_impact_reduction', 'max_morale',
                'avg_max_morale', 'shock_damage_bonus', 'fire_damage_bonus',
                'shock_damage_reduction', 'fire_damage_reduction', 'dice',
                'dice_modifier', 'unit_count', 'shock_value', 'fire_value',
                'infantry_combat_bonus', 'cavalry_combat_bonus',
                'artillery_combat_bonus', 'training', 'time', 'military_tactics'
            ]},
            "B": {name: tk.DoubleVar(value=0.0) for name in [
                'morale_impact_bonus', 'morale_impact_reduction', 'max_morale',
                'avg_max_morale', 'shock_damage_bonus', 'fire_damage_bonus',
                'shock_damage_reduction', 'fire_damage_reduction', 'dice',
                'dice_modifier', 'unit_count', 'shock_value', 'fire_value',
                'infantry_combat_bonus', 'cavalry_combat_bonus',
                'artillery_combat_bonus', 'training', 'time', 'military_tactics'
            ]}
        }

    def create_compact_ui(self):
        """创建紧凑的单面板界面"""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 单位选择区域
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=5)
        
        # A军选择
        a_select_frame = ttk.LabelFrame(selection_frame, text="A军选择", padding=10)
        a_select_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.create_unit_selection(a_select_frame, "A")
        
        # B军选择
        b_select_frame = ttk.LabelFrame(selection_frame, text="B军选择", padding=10)
        b_select_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.create_unit_selection(b_select_frame, "B")
        
        # 参数输入区域
        param_frame = ttk.Frame(main_frame)
        param_frame.pack(fill=tk.X, pady=5)
        
        # A军参数
        a_param_frame = ttk.LabelFrame(param_frame, text="A军参数", padding=10)
        a_param_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.create_parameter_inputs(a_param_frame, "A")
        
        # B军参数
        b_param_frame = ttk.LabelFrame(param_frame, text="B军参数", padding=10)
        b_param_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.create_parameter_inputs(b_param_frame, "B")
        
        # 计算按钮（只在A军参数区域下方添加一个）
        btn_frame = ttk.Frame(param_frame)
        btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(btn_frame, text="开始计算", command=self.calculate_all, 
                  width=15).pack(pady=10, padx=5)
        
        # 结果区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.create_results_display(result_frame)

    def create_unit_selection(self, parent, army):
        """创建单位选择组件（属性显示在右侧）"""
        main_frame = ttk.Frame(parent)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧选择框架
        select_frame = ttk.Frame(main_frame)
        select_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 兵种选择
        ttk.Label(select_frame, text="兵种:").grid(row=0, column=0, sticky=tk.W)
        category_var = tk.StringVar()
        category_cb = ttk.Combobox(select_frame, textvariable=category_var, 
                                  values=list(self.data.keys()), state="readonly", width=12)
        category_cb.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        setattr(self, f"{army}_category_var", category_var)
        setattr(self, f"{army}_category_cb", category_cb)
        category_cb.bind("<<ComboboxSelected>>", lambda e: self.on_category_select(army))
        
        # 科技组选择
        ttk.Label(select_frame, text="科技组:").grid(row=1, column=0, sticky=tk.W)
        tech_group_var = tk.StringVar()
        tech_group_cb = ttk.Combobox(select_frame, textvariable=tech_group_var, state="readonly", width=12)
        tech_group_cb.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)
        setattr(self, f"{army}_tech_group_var", tech_group_var)
        setattr(self, f"{army}_tech_group_cb", tech_group_cb)
        tech_group_cb.bind("<<ComboboxSelected>>", lambda e: self.on_tech_group_select(army))
        
        # 科技等级选择
        ttk.Label(select_frame, text="科技等级:").grid(row=2, column=0, sticky=tk.W)
        tech_level_var = tk.StringVar()
        tech_level_cb = ttk.Combobox(select_frame, textvariable=tech_level_var, state="readonly", width=12)
        tech_level_cb.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)
        setattr(self, f"{army}_tech_level_var", tech_level_var)
        setattr(self, f"{army}_tech_level_cb", tech_level_cb)
        tech_level_cb.bind("<<ComboboxSelected>>", lambda e: self.on_tech_level_select(army))
        
        # 单位选择
        ttk.Label(select_frame, text="单位名称:").grid(row=3, column=0, sticky=tk.W)
        unit_var = tk.StringVar()
        unit_cb = ttk.Combobox(select_frame, textvariable=unit_var, state="readonly", width=12)
        unit_cb.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=2)
        setattr(self, f"{army}_unit_var", unit_var)
        setattr(self, f"{army}_unit_cb", unit_cb)
        unit_cb.bind("<<ComboboxSelected>>", lambda e: self.on_unit_select(army))
        
        # 右侧属性框架
        attr_frame = ttk.LabelFrame(main_frame, text="单位属性", padding=10)
        attr_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        attributes = ["火力进攻", "火力防御", "冲击进攻", "冲击防御", "士气进攻", "士气防御"]
        for i, attr in enumerate(attributes):
            ttk.Label(attr_frame, text=f"{attr}:").grid(row=i, column=0, sticky=tk.W, padx=2, pady=1)
            label = ttk.Label(attr_frame, text="", width=6)
            label.grid(row=i, column=1, sticky=tk.W, padx=2, pady=1)
            setattr(self, f"{army}_{attr}_label", label)
        
        ttk.Label(attr_frame, text="总和:").grid(row=6, column=0, sticky=tk.W, padx=2, pady=1)
        total_label = ttk.Label(attr_frame, text="", width=8)
        total_label.grid(row=6, column=1, sticky=tk.W, padx=2, pady=1)
        setattr(self, f"{army}_total_label", total_label)

    def create_parameter_inputs(self, parent, army):
        """创建参数输入组件"""
        # 第一列参数
        col1 = ttk.Frame(parent)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_param_row(col1, 0, "士气打击加成:", army, "morale_impact_bonus")
        self.create_param_row(col1, 1, "士气打击减成:", army, "morale_impact_reduction")
        self.create_param_row(col1, 2, "最大士气:", army, "max_morale")
        self.create_param_row(col1, 3, "平均士气:", army, "avg_max_morale")
        self.create_param_row(col1, 4, "冲击伤害加成:", army, "shock_damage_bonus")
        self.create_param_row(col1, 5, "火力伤害加成:", army, "fire_damage_bonus")
        
        # 第二列参数
        col2 = ttk.Frame(parent)
        col2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_param_row(col2, 0, "冲击伤害减成:", army, "shock_damage_reduction")
        self.create_param_row(col2, 1, "火力伤害减成:", army, "fire_damage_reduction")
        self.create_param_row(col2, 2, "骰子:", army, "dice")
        self.create_param_row(col2, 3, "骰子修正:", army, "dice_modifier")
        self.create_param_row(col2, 4, "团人数(K):", army, "unit_count")
        self.create_param_row(col2, 5, "冲击值:", army, "shock_value")
        
        # 第三列参数
        col3 = ttk.Frame(parent)
        col3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_param_row(col3, 0, "火力值:", army, "fire_value")
        self.create_param_row(col3, 1, "步兵作战加成:", army, "infantry_combat_bonus")
        self.create_param_row(col3, 2, "骑兵作战加成:", army, "cavalry_combat_bonus")
        self.create_param_row(col3, 3, "炮兵作战加成:", army, "artillery_combat_bonus")
        self.create_param_row(col3, 4, "训练度:", army, "training")
        self.create_param_row(col3, 5, "时间:", army, "time")
        self.create_param_row(col3, 6, "军事战术:", army, "military_tactics")

    def create_param_row(self, parent, row, label, army, param_name):
        """创建单个参数输入行"""
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, padx=2, pady=1)
        ttk.Entry(parent, textvariable=self.params[army][param_name], width=8).grid(
            row=row, column=1, sticky=tk.W, padx=2, pady=1)

    def create_results_display(self, parent):
        """创建结果展示区域"""
        # 火力打击结果
        fire_frame = ttk.LabelFrame(parent, text="火力打击", padding=5)
        fire_frame.pack(fill=tk.X, pady=2)
        
        self.create_result_row(fire_frame, 0, "A军士气打击:", "a_fire_morale")
        self.create_result_row(fire_frame, 1, "B军士气打击:", "b_fire_morale")
        self.create_result_row(fire_frame, 2, "A军人力打击:", "a_fire_manpower")
        self.create_result_row(fire_frame, 3, "B军人力打击:", "b_fire_manpower")
        
        # 冲击打击结果
        shock_frame = ttk.LabelFrame(parent, text="冲击打击", padding=5)
        shock_frame.pack(fill=tk.X, pady=2)
        
        self.create_result_row(shock_frame, 0, "A军士气打击:", "a_shock_morale")
        self.create_result_row(shock_frame, 1, "B军士气打击:", "b_shock_morale")
        self.create_result_row(shock_frame, 2, "A军人力打击:", "a_shock_manpower")
        self.create_result_row(shock_frame, 3, "B军人力打击:", "b_shock_manpower")

    def create_result_row(self, parent, row, label, result_name):
        """创建单个结果展示行"""
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, padx=2, pady=1)
        label = ttk.Label(parent, text="", width=10)
        label.grid(row=row, column=1, sticky=tk.W, padx=2, pady=1)
        setattr(self, f"{result_name}_label", label)

    def on_category_select(self, army):
        """兵种选择事件"""
        category = getattr(self, f"{army}_category_var").get()
        tech_group_cb = getattr(self, f"{army}_tech_group_cb")
        
        if category in self.data:
            tech_group_cb['values'] = list(self.data[category].keys())
            tech_group_cb.set('')
            getattr(self, f"{army}_tech_level_cb")['values'] = []
            getattr(self, f"{army}_tech_level_var").set('')
            getattr(self, f"{army}_unit_cb")['values'] = []
            getattr(self, f"{army}_unit_var").set('')
            self.clear_unit_attributes(army)

    def on_tech_group_select(self, army):
        """科技组选择事件"""
        category = getattr(self, f"{army}_category_var").get()
        tech_group = getattr(self, f"{army}_tech_group_var").get()
        tech_level_cb = getattr(self, f"{army}_tech_level_cb")
        
        if category in self.data and tech_group in self.data[category]:
            units = self.data[category][tech_group]
            tech_levels = sorted({unit['tech_level'] for unit in units}, key=int)
            tech_level_cb['values'] = tech_levels
            tech_level_cb.set('')
            getattr(self, f"{army}_unit_cb")['values'] = []
            getattr(self, f"{army}_unit_var").set('')
            self.clear_unit_attributes(army)

    def on_tech_level_select(self, army):
        """科技等级选择事件"""
        category = getattr(self, f"{army}_category_var").get()
        tech_group = getattr(self, f"{army}_tech_group_var").get()
        tech_level = getattr(self, f"{army}_tech_level_var").get()
        unit_cb = getattr(self, f"{army}_unit_cb")
        
        if category in self.data and tech_group in self.data[category]:
            units = self.data[category][tech_group]
            filtered_units = [unit for unit in units if unit['tech_level'] == tech_level]
            unit_names = [unit['name'] for unit in filtered_units]
            unit_cb['values'] = unit_names
            unit_cb.set('')
            self.clear_unit_attributes(army)

    def on_unit_select(self, army):
        """单位选择事件"""
        category = getattr(self, f"{army}_category_var").get()
        tech_group = getattr(self, f"{army}_tech_group_var").get()
        tech_level = getattr(self, f"{army}_tech_level_var").get()
        unit_name = getattr(self, f"{army}_unit_var").get()
        
        if not all([category, tech_group, tech_level, unit_name]):
            return
        
        if category in self.data and tech_group in self.data[category]:
            units = self.data[category][tech_group]
            unit_data = next((unit for unit in units 
                            if unit['tech_level'] == tech_level and unit['name'] == unit_name), None)
            
            if unit_data:
                self.selected_units[army] = unit_data
                attributes = unit_data['values']
                for i, attr in enumerate(["火力进攻", "火力防御", "冲击进攻", "冲击防御", "士气进攻", "士气防御"]):
                    getattr(self, f"{army}_{attr}_label").config(text=str(attributes[i]))
                getattr(self, f"{army}_total_label").config(text=str(unit_data['total']))

    def clear_unit_attributes(self, army):
        """清空单位属性显示"""
        for attr in ["火力进攻", "火力防御", "冲击进攻", "冲击防御", "士气进攻", "士气防御"]:
            getattr(self, f"{army}_{attr}_label").config(text="")
        getattr(self, f"{army}_total_label").config(text="")
        self.selected_units[army] = None

    def calculate_all(self):
        """执行所有计算"""
        try:
            # A军对B军的打击
            a_fire_morale, a_fire_manpower = self.calculate_damage("A", "B", "fire")
            a_shock_morale, a_shock_manpower = self.calculate_damage("A", "B", "shock")
            
            # B军对A军的打击
            b_fire_morale, b_fire_manpower = self.calculate_damage("B", "A", "fire")
            b_shock_morale, b_shock_manpower = self.calculate_damage("B", "A", "shock")
            
            # 更新结果
            self.a_fire_morale_label.config(text=f"{a_fire_morale:.2f}")
            self.a_fire_manpower_label.config(text=f"{a_fire_manpower:.2f}")
            self.a_shock_morale_label.config(text=f"{a_shock_morale:.2f}")
            self.a_shock_manpower_label.config(text=f"{a_shock_manpower:.2f}")
            
            self.b_fire_morale_label.config(text=f"{b_fire_morale:.2f}")
            self.b_fire_manpower_label.config(text=f"{b_fire_manpower:.2f}")
            self.b_shock_morale_label.config(text=f"{b_shock_morale:.2f}")
            self.b_shock_manpower_label.config(text=f"{b_shock_manpower:.2f}")
            
        except Exception as e:
            messagebox.showerror("计算错误", f"计算过程中出错: {str(e)}")

    def calculate_damage(self, attacker, defender, damage_type):
        """计算伤害值"""
        if not self.selected_units[attacker] or not self.selected_units[defender]:
            raise ValueError("请先选择双方单位")
        
        # 获取攻击方和防御方参数
        attacker_params = self.params[attacker]
        defender_params = self.params[defender]
        attacker_unit = self.selected_units[attacker]
        defender_unit = self.selected_units[defender]
        
        # 确定攻击类型对应的属性索引
        if damage_type == "fire":
            attacker_offensive = attacker_unit['values'][0]  # 火力进攻
            attacker_morale = attacker_unit['values'][4]     # 士气进攻
            defender_defensive = defender_unit['values'][1]  # 火力防御
            defender_morale = defender_unit['values'][5]     # 士气防御
            damage_bonus = attacker_params['fire_damage_bonus'].get()
            damage_reduction = defender_params['fire_damage_reduction'].get()
            attack_value = attacker_params['fire_value'].get()
        else:  # shock
            attacker_offensive = attacker_unit['values'][2]  # 冲击进攻
            attacker_morale = attacker_unit['values'][4]     # 士气进攻
            defender_defensive = defender_unit['values'][3]  # 冲击防御
            defender_morale = defender_unit['values'][5]     # 士气防御
            damage_bonus = attacker_params['shock_damage_bonus'].get()
            damage_reduction = defender_params['shock_damage_reduction'].get()
            attack_value = attacker_params['shock_value'].get()
        
        # 计算点数因子
        dice = attacker_params['dice'].get()
        dice_mod = attacker_params['dice_modifier'].get()
        point_factor = 15 + 5 * (dice + dice_mod + attacker_offensive + attacker_morale - 
                                defender_defensive - defender_morale)
        
        # 计算战力因子
        unit_count = attacker_params['unit_count'].get()
        military_tactics = defender_params['military_tactics'].get()
        training = attacker_params['training'].get()
        defender_training = defender_params['training'].get()
        time = attacker_params['time'].get()
        
        # 根据兵种类型获取作战加成
        category = getattr(self, f"{attacker}_category_var").get()
        if category == "步兵":
            combat_bonus = attacker_params['infantry_combat_bonus'].get()
        elif category == "骑兵":
            combat_bonus = attacker_params['cavalry_combat_bonus'].get()
        else:  # 炮兵
            combat_bonus = attacker_params['artillery_combat_bonus'].get()
        
        power_factor = (unit_count * attack_value / military_tactics * 
                       (1 + combat_bonus) * (1 + training / 100) * 
                       (1 + time / 100) / (1 + defender_training / 100))
        
        # 计算士气打击
        morale_bonus = attacker_params['morale_impact_bonus'].get()
        morale_reduction = defender_params['morale_impact_reduction'].get()
        max_morale = attacker_params['max_morale'].get()
        avg_morale = attacker_params['avg_max_morale'].get()
        
        morale_damage = (point_factor * power_factor * 
                        (1 + morale_bonus) * (1 - morale_reduction) * 
                        max_morale / 540 + 0.01 * avg_morale)
        
        # 计算人力打击
        manpower_damage = (point_factor * power_factor * 
                          (1 + damage_bonus) * (1 - damage_reduction))
        
        return morale_damage, manpower_damage

if __name__ == "__main__":
    root = tk.Tk()
    app = MilitaryDamageCalculator(root)
    root.mainloop()