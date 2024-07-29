from django.db import models

class Medicacao(models.Model):
    nome = models.CharField(max_length=100)
    dosagem = models.CharField(max_length=100)
    posologia = models.TextField() 

    def __str__(self):
        return f"{self.nome} - {self.dosagem} - {self.posologia}"
    
class Alergia(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Diagnostico(models.Model):
    nome = models.CharField(max_length=100)
    codigo_cid = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Paciente(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
    ]
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True, null=True)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=11, blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, default='Masculino')
    medicacoes = models.ManyToManyField(Medicacao, blank=True)
    alergias = models.ManyToManyField(Alergia, blank=True)
    diagnosticos = models.ManyToManyField(Diagnostico, blank=True)
    data_admissao = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome
    