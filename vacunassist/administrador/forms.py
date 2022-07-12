from django import forms


CHART_CHOICES = (
    ('#1', 'Gráfico Barras'),
    ('#2', 'Gráfico Torta'),
    ('#3', 'Gráfico Líneas')
)
# RESULTS_CHOICES = (
#     ('#1', '# Vacunas Aplicadas'),
#     ('#2', '# Turnos Programados'),
#     ('#3', '# Solicitudes Recibidas'),
#     ('#4', 'Total Price')
# )
CENTROS_CHOICES = (
    ('Terminal', 'Terminal'),
    ('Cementerio', 'Cementerio'),
    ('Municipalidad', 'Municipalidad'),
)


class SalesSearchForm(forms.Form):
    date_from = forms.DateField(label='Desde', widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(label='Hasta', widget=forms.DateInput(attrs={'type': 'date'}))
    # centro_vacunatorio = forms.ChoiceField(label="Centro vacunatorio", choices=CENTROS_CHOICES, required=True, widget=forms.Select(attrs = {'class' : 'form-control','placeholder' : 'Centro Vacunatorio'}))
    # chart_type = forms.ChoiceField(label='Tipo de Gráfico', choices=CHART_CHOICES)
    # results_by = forms.ChoiceField(label='Agrupación por', choices=RESULTS_CHOICES)