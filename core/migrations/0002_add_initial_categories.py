from django.db import migrations

def create_initial_categories(apps, schema_editor):
    Category = apps.get_model('core', 'Category')
    categorias = [
        'Acessórios',
        'Documentos pessoais',
        'Eletrônicos',
        'Cartão de crédito',
        'Pets',
        'Outros',
    ]
    for nome in categorias:
        Category.objects.create(name=nome)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_categories),
    ]