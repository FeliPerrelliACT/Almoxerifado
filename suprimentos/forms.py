from .models import Request, Product, RequestProduct, CentroCusto, PlanoFinanceiro, Armazem, Funcionario
from django import forms

UNIT_CHOICES = [
    ('km', 'Quilômetro (km)'), ('m', 'Metro (m)'), ('cm', 'Centímetro (cm)'), ('mm', 'Milímetro (mm)'),
    ('in', 'Polegada (in)'), ('kg', 'Quilograma (kg)'), ('g', 'Grama (g)'), ('mg', 'Miligrama (mg)'),
    ('t', 'Tonelada (t)'), ('lb', 'Libras (lb)'), ('oz', 'Onça (oz)'), ('ct', 'Quilate (ct)'),
    ('m2', 'Metro quadrado (m²)'), ('km2', 'Quilômetro quadrado (km²)'), ('cm2', 'Centímetro quadrado (cm²)'),
    ('ha', 'Hectare (ha)'), ('acre', 'Acre'), ('mi2', 'Milha quadrada (mi²)'), ('L', 'Litro (L)'),
    ('mL', 'Mililitro (mL)'), ('m3', 'Metro cúbico (m³)'), ('cm3', 'Centímetro cúbico (cm³)'),
    ('galao', 'Galão'), ('fl_oz', 'Onça fluida (fl oz)'), ('barril', 'Barril'),
    ('un', 'Unidade'), ('dez', 'Dezena'), ('cen', 'Centena'), ('mil', 'Milhar'),
]

# Definindo as novas opções para categoria
CATEGORIA_CHOICES = [
    ('ferramenta', 'Ferramenta'),
    ('epi', 'EPI'),
    ('material', 'Material'),
]

# Formulário de Cadastro Produtos
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'unidade_medida', 'categoria']  # Alterando tipo para categoria
        widgets = {
            'product_name': forms.TextInput(attrs={'placeholder': 'Nome do produto', 'class': 'form-control'}),
            'unidade_medida': forms.Select(choices=UNIT_CHOICES, attrs={'class': 'form-control'}),
            'categoria': forms.Select(choices=CATEGORIA_CHOICES, attrs={'class': 'form-control'}),  # Alterando tipo para categoria
        }

    def clean(self):
        cleaned_data = super().clean()
        unidade_medida = cleaned_data.get('unidade_medida')
        categoria = cleaned_data.get('categoria')  # Alterando tipo para categoria

        # Garantir que a unidade de medida seja válida
        if unidade_medida not in dict(UNIT_CHOICES):
            self.add_error('unidade_medida', "Unidade de medida inválida.")

        # Garantir que a categoria seja válida
        if categoria not in dict(CATEGORIA_CHOICES):
            self.add_error('categoria', "Categoria de produto inválida.")  # Alterando tipo para categoria

        return cleaned_data


# Formulário de Solicitação
class RequestForm(forms.ModelForm):
    # A referência ao modelo Cotacao foi removida

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Garantir que pelo menos um produto será mostrado; default = 1
        num_products = kwargs.get('data', {}).get('num_products', 1)

        # Adicionar campos de produto e quantidade dinamicamente
        for i in range(1, int(num_products) + 1):
            self.fields[f'product_{i}'] = forms.ModelChoiceField(
                queryset=Product.objects.all(),
                required=True,
                label=f'Produto {i}'
            )
            self.fields[f'quantity_{i}'] = forms.IntegerField(
                min_value=1,
                required=True,
                label=f'Quantidade {i}'
            )

        # Adicionar o campo de cost_center
        self.fields['cost_center'] = forms.CharField(
            max_length=255,
            required=True,
            label='Centro de Custo'
        )

    def save(self, commit=True):
        # Criação da solicitação
        instance = super().save(commit=False)
        
        # Atribuir o valor do cost_center
        cost_center = self.cleaned_data.get('cost_center')
        if cost_center:
            instance.cost_center = cost_center

        if commit:
            instance.save()

            # Processar produtos e quantidades
            num_products = int(self.data.get('num_products', 1))
            for i in range(1, num_products + 1):
                product = self.cleaned_data.get(f'product_{i}')
                quantity = self.cleaned_data.get(f'quantity_{i}')

                if product and quantity:
                    RequestProduct.objects.create(
                        request=instance,
                        product=product,
                        quantity=quantity
                    )

        return instance

    class Meta:
        model = Request
        fields = ['request_text', 'status', 'cost_center']  # Adicionar cost_center ao meta

# Formulário para Produto na Solicitação
class RequestProductForm(forms.ModelForm):
    class Meta:
        model = RequestProduct
        fields = ['product', 'quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': '1', 'class': 'form-control'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("A quantidade deve ser maior que zero.")
        return quantity

# Formulário de Cotação
class QuotationForm(forms.Form):
    quotation_file = forms.FileField(label='Selecione o arquivo de cotação', required=True)

# Formulário de Centro Custo
class CentroCustoForm(forms.ModelForm):
    class Meta:
        model = CentroCusto
        fields = ['name']  # Apenas o nome será preenchido
        widgets = {
            'status': forms.HiddenInput(),  # Oculta o campo de status no formulário
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = True  # O status será sempre 'Ativo'
        instance.usuario_registrante = self.initial.get('usuario_registrante')  # Usa o usuário logado
        if commit:
            instance.save()
        return instance

# Formulário de Plano Financeiro
class PlanoFinanceiroForm(forms.ModelForm):
    class Meta:
        model = PlanoFinanceiro
        fields = ['name']  # Apenas o nome será preenchido
        widgets = {
            'status': forms.HiddenInput(),  # Oculta o campo de status no formulário
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = True  # O status será sempre 'Ativo'
        instance.usuario_registrante = self.initial.get('usuario_registrante')  # Usa o usuário logado
        if commit:
            instance.save()
        return instance

# Formulário de Centro Custo
class ArmazemForm(forms.ModelForm):
    class Meta:
        model = Armazem
        fields = ['name']  # Apenas o nome será preenchido
        widgets = {
            'status': forms.HiddenInput(),  # Oculta o campo de status no formulário
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = True  # O status será sempre 'Ativo'
        instance.usuario_registrante = self.initial.get('usuario_registrante')  # Usa o usuário logado
        if commit:
            instance.save()
        return instance

# Formulário de Funcionário
class FuncionarioForm(forms.ModelForm):
    EMPRESA_CHOICES = [
        ('ACT ENGENHARIA', 'ACT ENGENHARIA'),
        ('GREEN CIRCLE', 'GREEN CIRCLE'),
        ('TECH PAV', 'TECH PAV'),
    ]

    empresa = forms.ChoiceField(choices=EMPRESA_CHOICES, label="Empresa")

    class Meta:
        model = Funcionario
        fields = ['nome_completo', 'id_funcionario', 'cargo', 'empresa']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = True  # Define o status como ativo
        if commit:
            instance.save()
        return instance
