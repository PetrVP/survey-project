from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Наименование')
    startDate = models.DateField(verbose_name='Дата начала')
    endDate = models.DateField(verbose_name='Дата окончания')
    description = models.CharField(max_length=200, verbose_name='Описание', blank=True)
    status = models.BooleanField(default=False, verbose_name='Статус опроса')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['startDate']
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опрос'


class Questions(models.Model):
    EXAMPLE_QUESTION = (
        ('text', 'Текстовый ответ'),
        ('one', 'Выбор одного ответа'),
        ('multy', 'Выбор нескольктх ответов'),
    )
    survey = models.ForeignKey('Survey', to_field='name', verbose_name='Наименование отпроса', on_delete=models.CASCADE)
    text = models.CharField(max_length=200, verbose_name='Текст вопроса')
    answerType = models.CharField(max_length=5, choices=EXAMPLE_QUESTION, verbose_name='Тип ответа', default='text')
    changeAnswer = models.TextField(verbose_name='Текстовый ответ', null=True)

    def __str__(self):
        return f'{self.text}, опрос {self.survey}'

    class Meta:
        ordering = ['survey']
        verbose_name = 'Вопросы'
        verbose_name_plural = 'Вопросы'


class UserAnswer(models.Model):
    user = models.CharField(max_length=20, verbose_name='Пользователь')
    survey = models.ForeignKey(Survey, to_field='name', verbose_name='Наименование опроса', on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, verbose_name='Вопрос', on_delete=models.CASCADE)
    answer = models.TextField(verbose_name='Текстовый ответ')

    def __str__(self):
        return f'{self.user}, {self.question}'

    class Meta:
        ordering = ['user', 'survey']
        verbose_name = 'Результаты'
        verbose_name_plural = 'Результаты'
