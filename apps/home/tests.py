from django.test import TestCase
from django.core.urlresolvers import reverse_lazy  # reverse
#import uuid
# from testing_demo import DemoTestCase error


class HomeTests(TestCase):

    """docstring for HomeTests"""

    def setUp(self):
        pass

    def test_saludo_hola_view(self):
        # print uuid.uuid4().hex
        #import ipdb
        # ipdb.set_trace()
        nombre = 'Juan'
        #response = self.client.get('/home/saludo_hola/%s/' % nombre)
        #response = self.client.get(reverse('saludo-hola', kwargs={'nombre': nombre}))
        response = self.client.get(reverse_lazy('saludo-hola', args=(nombre,)))
        #(reverse('promote',args=(self.lark.pk)),follow=True)
        # para /home/juan/?saludo=chau&age=7
        # response = self.client.get('/home/saludo_hola/%s/' % nombre, {'saludo': 'chau'})
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/
        a = nombre
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hola')
        self.assertEqual(response.content, 'Hola Juan')  # %s' % nombre

        # 18.46 https://www.youtube.com/watch?v=ScjhonARTvU
        #self.assertRedirects(response, reverse('list'))

        # 24 test_admin

    def test_saludo_hola_template_view(self):

        nombre = 'Juan'
        #response = self.client.get('/home/saludo_hola_template/%s/' % nombre)
        response = self.client.get(
            reverse_lazy('saludo-hola-template', args=(nombre,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/saludo/hola.html')
        self.assertContains(response, 'Hola')
        self.assertTrue('nombre' in response.context)
        nombre_r = response.context['nombre']
        self.assertEqual(nombre_r, 'Juan')
        self.assertContains(response, 'Hola Juan')
